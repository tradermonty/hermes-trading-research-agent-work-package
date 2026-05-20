#!/usr/bin/env python3
"""Validate skill references against the upstream claude-trading-skills index.

Reads upstream `skills-index.yaml` (canonical source) and checks that every
skill referenced in `skill-bundles/*.yaml` and `data/skill-mapping.yaml`
resolves to an upstream skill id. Profile-local skills (prefix `trading-`)
are accepted via `<profile-root>/skills/<name>/SKILL.md`.

Usage:
    python3 scripts/validate_upstream_index.py \
        --source /path/to/claude-trading-skills \
        --profile-root . \
        [--missing-doc docs/MISSING_SKILLS.md] \
        [--strict]

Exit codes:
    0 - all references resolved, or every missing skill is documented in
        --missing-doc as "degraded-mode accepted".
    2 - one or more unresolved missing skills (or --strict overrides docs).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML required. Install with: pip install pyyaml") from exc


PROFILE_LOCAL_PREFIX = "trading-"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def upstream_skill_ids(source: Path) -> set[str]:
    index_path = source / "skills-index.yaml"
    if not index_path.exists():
        raise SystemExit(f"Upstream skills-index.yaml not found: {index_path}")
    data = load_yaml(index_path)
    skills = data.get("skills") or []
    ids: set[str] = set()
    for entry in skills:
        if isinstance(entry, dict):
            skill_id = entry.get("id") or entry.get("name")
            if skill_id:
                ids.add(skill_id)
        elif isinstance(entry, str):
            ids.add(entry)
    if not ids:
        raise SystemExit(f"No skills found in {index_path}")
    return ids


def profile_local_skills(profile_root: Path) -> set[str]:
    skills_dir = profile_root / "skills"
    if not skills_dir.exists():
        return set()
    return {
        p.name
        for p in skills_dir.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    }


def collect_bundle_references(profile_root: Path) -> dict[str, list[str]]:
    bundles_dir = profile_root / "skill-bundles"
    refs: dict[str, list[str]] = {}
    if not bundles_dir.exists():
        return refs
    for bundle_path in sorted(bundles_dir.glob("*.yaml")):
        data = load_yaml(bundle_path)
        skills = data.get("skills") or []
        if not isinstance(skills, list):
            continue
        refs[bundle_path.stem] = [s for s in skills if isinstance(s, str)]
    return refs


def collect_mapping_references(profile_root: Path) -> dict[str, list[str]]:
    mapping_path = profile_root / "data" / "skill-mapping.yaml"
    refs: dict[str, list[str]] = {}
    if not mapping_path.exists():
        return refs
    data = load_yaml(mapping_path)
    workflows = data.get("workflows") or {}
    for slug, spec in workflows.items():
        if not isinstance(spec, dict):
            continue
        skills = spec.get("skills") or []
        if isinstance(skills, list):
            refs[f"mapping:{slug}"] = [s for s in skills if isinstance(s, str)]
    return refs


def resolved_missing(
    refs: dict[str, list[str]],
    upstream_ids: set[str],
    local_ids: set[str],
) -> dict[str, list[str]]:
    """Return mapping of source -> missing skill names (unresolved)."""
    missing: dict[str, list[str]] = {}
    for source, skill_list in refs.items():
        unresolved: list[str] = []
        for skill in skill_list:
            if skill in upstream_ids:
                continue
            if skill.startswith(PROFILE_LOCAL_PREFIX) and skill in local_ids:
                continue
            if skill in local_ids:
                continue
            unresolved.append(skill)
        if unresolved:
            missing[source] = unresolved
    return missing


_DOC_NAME_RE = re.compile(r"`([a-z0-9][a-z0-9_\-]*)`")
_DEGRADED_TOKENS = ("degraded", "degraded-mode", "degraded mode")


def documented_missing(missing_doc: Path) -> set[str]:
    """Parse MISSING_SKILLS.md and return skill names marked as degraded-mode accepted.

    A skill is "documented" if its name appears in a backtick (e.g. `skill-name`)
    on a line that also mentions "degraded" (any case). This keeps the format
    flexible while requiring an explicit acceptance marker.
    """
    if not missing_doc.exists():
        return set()
    accepted: set[str] = set()
    for raw_line in missing_doc.read_text(encoding="utf-8").splitlines():
        line_lower = raw_line.lower()
        if not any(token in line_lower for token in _DEGRADED_TOKENS):
            continue
        for match in _DOC_NAME_RE.findall(raw_line):
            accepted.add(match)
    return accepted


def flatten(missing: dict[str, list[str]]) -> set[str]:
    out: set[str] = set()
    for names in missing.values():
        out.update(names)
    return out


def print_summary(
    refs: dict[str, list[str]],
    missing: dict[str, list[str]],
) -> None:
    for source, skill_list in sorted(refs.items()):
        miss = missing.get(source, [])
        resolved = len(skill_list) - len(miss)
        if miss:
            print(f"  {source}: resolved={resolved}, missing={miss}")
        else:
            print(f"  {source}: resolved={resolved}, missing=[]")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Path to claude-trading-skills repo")
    parser.add_argument("--profile-root", default=".")
    parser.add_argument(
        "--missing-doc",
        default="docs/MISSING_SKILLS.md",
        help="Doc file recording accepted degraded-mode missing skills",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any missing skill regardless of missing-doc",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    source = Path(args.source).expanduser().resolve()
    profile_root = Path(args.profile_root).expanduser().resolve()
    missing_doc = (profile_root / args.missing_doc).resolve()

    upstream_ids = upstream_skill_ids(source)
    local_ids = profile_local_skills(profile_root)

    bundle_refs = collect_bundle_references(profile_root)
    mapping_refs = collect_mapping_references(profile_root)
    all_refs = {**bundle_refs, **mapping_refs}

    missing = resolved_missing(all_refs, upstream_ids, local_ids)

    print("Upstream index skills:", len(upstream_ids))
    print("Profile-local skills:", len(local_ids))
    print("\nBundle references:")
    print_summary(bundle_refs, missing)
    print("\nMapping references:")
    print_summary(mapping_refs, missing)

    missing_set = flatten(missing)
    if not missing_set:
        print("\nResult: all skill references resolved (exit 0)")
        return 0

    accepted = documented_missing(missing_doc)
    unresolved = missing_set - accepted
    print(f"\nMissing total: {len(missing_set)}")
    print(f"Documented as degraded-mode accepted: {len(accepted & missing_set)}")
    if unresolved:
        print(f"Unresolved (not in {missing_doc.name}):")
        for name in sorted(unresolved):
            print(f"  - {name}")

    if args.strict and missing_set:
        print("\nResult: --strict, missing skills present (exit 2)", file=sys.stderr)
        return 2
    if unresolved:
        print(
            f"\nResult: unresolved missing skills present (exit 2). "
            f"Document them in {missing_doc.name} or fix the references.",
            file=sys.stderr,
        )
        return 2

    print("\nResult: all missing skills accepted via degraded-mode doc (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
