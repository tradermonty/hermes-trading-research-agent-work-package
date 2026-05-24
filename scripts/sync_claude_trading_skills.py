#!/usr/bin/env python3
"""Generate Hermes bundles and optional vendored skills from claude-trading-skills.

Usage:
    python scripts/sync_claude_trading_skills.py \
      --source /path/to/claude-trading-skills \
      --profile-root . \
      --mode external \
      --write

External mode validates and generates bundles that reference external skills.
Vendor mode also copies selected canonical skills into this profile.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc


@dataclass
class SyncResult:
    generated_bundles: list[Path]
    missing_skills: dict[str, list[str]]
    vendored_skills: list[str]
    wrote: list[Path] = field(default_factory=list)
    skipped_protected: list[Path] = field(default_factory=list)
    skipped_legacy: list[Path] = field(default_factory=list)
    skipped_unchanged: list[Path] = field(default_factory=list)
    forced: list[Path] = field(default_factory=list)
    config_written: bool = False


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class _BlockScalarStr(str):
    """Marker subclass — represented as a YAML literal block scalar (|)."""


def _block_scalar_representer(dumper, data):  # type: ignore[no-untyped-def]
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(_BlockScalarStr, _block_scalar_representer, Dumper=yaml.SafeDumper)


def dump_yaml(data: Any) -> str:
    """Dump YAML preserving block scalar style for `instruction` fields.

    Strings under top-level `instruction` are emitted as literal block
    scalars so the file remains human-editable. Other multi-line strings
    fall back to PyYAML defaults.
    """
    if isinstance(data, dict) and isinstance(data.get("instruction"), str):
        body = data["instruction"]
        # Block scalars require a trailing newline to render cleanly.
        if not body.endswith("\n"):
            body = body + "\n"
        data = {**data, "instruction": _BlockScalarStr(body)}
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def discover_skills(source: Path) -> set[str]:
    skills_dir = source / "skills"
    if not skills_dir.exists():
        raise SystemExit(f"No skills directory found: {skills_dir}")
    return {p.name for p in sorted(skills_dir.iterdir()) if (p / "SKILL.md").exists()}


def workflow_mapping(profile_root: Path) -> dict[str, Any]:
    return load_yaml(profile_root / "data" / "skill-mapping.yaml").get("workflows", {})


def render_bundle(slug: str, spec: dict[str, Any]) -> dict[str, Any]:
    """Build the rendered dict for a generated bundle.

    `x-generated: true` is set so newly created files always declare
    ownership explicitly. The sync orchestration decides whether to
    write — render_bundle itself only computes the canonical body.
    """
    return {
        "name": slug,
        "description": spec.get("title", slug),
        "x-generated": True,
        "x-canonical-source": spec.get("canonical_source", "unknown"),
        "skills": spec.get("skills", []),
        "instruction": build_instruction(slug, spec),
    }


def build_instruction(slug: str, spec: dict[str, Any]) -> str:
    """Render a bundle instruction body.

    Must match the required-concepts contract enforced by
    tests/test_required_sections.py: data freshness, source provenance,
    thesis, invalidation, risk, and a human decision gate. Phrased in
    positive form so Hermes' cron threat scanner (`deception_hide`) does not
    reject the generated prompt — see docs/03-hermes-compatibility-notes.md.
    """
    outputs = spec.get("required_outputs", [])
    output_lines = (
        "\n".join(f"  - {item}" for item in outputs)
        if outputs
        else "  - concise structured result"
    )
    return f"""Run the {spec.get('title', slug)} workflow.

Category: {spec.get('category', 'unknown')}
Cadence: {spec.get('cadence', 'manual')}

Required outputs:
{output_lines}

Output must always include:
- data freshness (as-of timestamps for each input and any stale data warnings)
- source provenance for each data point (which skill or data source produced it)
- thesis behind each watchlist or candidate item
- invalidation criteria for each thesis
- risk considerations (exposure impact, drawdown sensitivity, event risk)
- a human decision gate — the human reviewer makes all entry and exit decisions; this bundle does not place orders
""".rstrip()


def update_external_config(profile_root: Path, source: Path, write: bool) -> bool:
    """Ensure ${CLAUDE_TRADING_SKILLS_REPO}/skills is in skills.external_dirs.

    Returns True iff the file was actually written. Short-circuits when the
    entry is already present (no write, mtime preserved). This is the
    config.yaml side of the B-2a determinism contract.
    """
    config_path = profile_root / "config.yaml"
    env_ref = "${CLAUDE_TRADING_SKILLS_REPO}/skills"
    config = load_yaml(config_path) if config_path.exists() else {}
    existing_dirs = (config.get("skills") or {}).get("external_dirs") or []
    if env_ref in existing_dirs:
        return False
    config.setdefault("skills", {})
    config["skills"].setdefault("external_dirs", []).append(env_ref)
    if write:
        config_path.write_text(dump_yaml(config), encoding="utf-8")
        return True
    return False


def copy_vendor_skills(profile_root: Path, source: Path, selected: set[str], write: bool) -> list[str]:
    dest_root = profile_root / "skills" / "vendor"
    vendored: list[str] = []
    for skill in sorted(selected):
        src = source / "skills" / skill
        if not src.exists():
            continue
        dest = dest_root / skill
        vendored.append(skill)
        if write:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
    if write:
        manifest = {
            "source_repo": str(source),
            "mode": "vendor",
            "skills": vendored,
        }
        (profile_root / "vendor-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return vendored


_PROTECTED_WARN = (
    "SKIP protected bundle: {name} (x-generated: false); "
    "pass --force-overwrite to bypass\n"
)
_LEGACY_WARN = (
    "SKIP legacy bundle {name} (x-generated key missing); "
    "commit explicit x-generated: true/false before regenerating, "
    "or pass --force-overwrite to bypass\n"
)


def sync(
    source: Path,
    profile_root: Path,
    mode: str,
    write: bool,
    force_overwrite: bool = False,
) -> SyncResult:
    available = discover_skills(source)
    mapping = workflow_mapping(profile_root)
    bundle_dir = profile_root / "skill-bundles"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    generated: list[Path] = []
    missing: dict[str, list[str]] = {}
    selected: set[str] = set()
    wrote: list[Path] = []
    skipped_protected: list[Path] = []
    skipped_legacy: list[Path] = []
    skipped_unchanged: list[Path] = []
    forced: list[Path] = []

    for slug, spec in mapping.items():
        skills = list(spec.get("skills", []))
        selected.update(s for s in skills if not s.startswith("trading-"))
        unresolved = [s for s in skills if s not in available and not (profile_root / "skills" / s).exists()]
        if unresolved:
            missing[slug] = unresolved
        bundle = render_bundle(slug, spec)
        out = bundle_dir / f"{slug}.yaml"
        generated.append(out)
        if not write:
            continue

        new_text = dump_yaml(bundle)

        if not out.exists():
            # New mapping entry — generator owns it.
            out.write_text(new_text, encoding="utf-8")
            wrote.append(out)
            continue

        existing_text = out.read_text(encoding="utf-8")
        existing_data = yaml.safe_load(existing_text) or {}
        existing_flag = existing_data.get("x-generated", None)

        if not force_overwrite:
            if existing_flag is False:
                sys.stderr.write(_PROTECTED_WARN.format(name=out.name))
                skipped_protected.append(out)
                continue
            if existing_flag is None:
                sys.stderr.write(_LEGACY_WARN.format(name=out.name))
                skipped_legacy.append(out)
                continue
            # x-generated: true → write-if-changed
            if existing_text == new_text:
                skipped_unchanged.append(out)
                continue
            out.write_text(new_text, encoding="utf-8")
            wrote.append(out)
            continue

        # force_overwrite=True: collapse every branch to unconditional write.
        # Still skip when content is unchanged so mtime stays put.
        if existing_text == new_text:
            skipped_unchanged.append(out)
            continue
        out.write_text(new_text, encoding="utf-8")
        forced.append(out)

    vendored: list[str] = []
    config_written = False
    if mode == "external":
        config_written = update_external_config(profile_root, source, write)
    elif mode == "vendor":
        vendored = copy_vendor_skills(profile_root, source, selected, write)
    else:
        raise SystemExit(f"Unknown mode: {mode}")

    return SyncResult(
        generated_bundles=generated,
        missing_skills=missing,
        vendored_skills=vendored,
        wrote=wrote,
        skipped_protected=skipped_protected,
        skipped_legacy=skipped_legacy,
        skipped_unchanged=skipped_unchanged,
        forced=forced,
        config_written=config_written,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, help="Path to claude-trading-skills repo")
    parser.add_argument("--profile-root", default=".")
    parser.add_argument("--mode", choices=["external", "vendor"], default="external")
    parser.add_argument("--write", action="store_true", help="Actually write files")
    parser.add_argument("--strict", action="store_true", help="Fail if any mapped skill is missing")
    parser.add_argument(
        "--force-overwrite",
        action="store_true",
        help=(
            "Ignore `x-generated: false` and missing-key protection on existing "
            "bundles and rewrite them. Hand edits will be lost. Reserved for "
            "the make sync-external-write-force escape hatch."
        ),
    )
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    profile_root = Path(args.profile_root).expanduser().resolve()

    if not (source / "skills").exists():
        raise SystemExit(f"Source repo missing skills/: {source}")
    if not (profile_root / "data" / "skill-mapping.yaml").exists():
        raise SystemExit(f"Profile root missing data/skill-mapping.yaml: {profile_root}")

    result = sync(
        source,
        profile_root,
        args.mode,
        args.write,
        force_overwrite=args.force_overwrite,
    )

    print(f"Generated bundles: {len(result.generated_bundles)}")
    for path in result.generated_bundles:
        print(f"  - {path.relative_to(profile_root)}")

    if result.missing_skills:
        print("Missing skills:", file=sys.stderr)
        for workflow, skills in result.missing_skills.items():
            print(f"  - {workflow}: {', '.join(skills)}", file=sys.stderr)
        if args.strict:
            raise SystemExit(2)

    if result.vendored_skills:
        print(f"Vendored skills: {len(result.vendored_skills)}")

    if args.write:
        print(
            f"wrote={len(result.wrote)} "
            f"skipped_protected={len(result.skipped_protected)} "
            f"skipped_legacy={len(result.skipped_legacy)} "
            f"skipped_unchanged={len(result.skipped_unchanged)} "
            f"forced={len(result.forced)} "
            f"config_written={1 if result.config_written else 0}"
        )
    else:
        print("Dry run only. Re-run with --write to update files.")


if __name__ == "__main__":
    main()
