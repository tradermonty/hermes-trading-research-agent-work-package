#!/usr/bin/env python3
"""Validate the Hermes Trading Research Agent starter package.

This validator intentionally checks structure and integration assumptions without
requiring Hermes itself to be installed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def warn(msg: str) -> None:
    print(f"WARN: {msg}", file=sys.stderr)


def validate_distribution(root: Path) -> None:
    path = root / "distribution.yaml"
    if not path.exists():
        fail("distribution.yaml is missing")
    data = load_yaml(path)
    for key in ["name", "version", "description", "hermes_requires", "env_requires"]:
        if key not in data:
            fail(f"distribution.yaml missing required key: {key}")
    if data["name"] != "trading-research-assistant":
        warn("distribution.yaml name is not trading-research-assistant")
    # Normalize trailing slashes before comparing: Hermes' installed copy
    # strips them, so the source-side `skills/` and the installed-side
    # `skills` should both pass.
    owned_norm = {entry.rstrip("/") for entry in data.get("distribution_owned", [])}
    for rel in ["SOUL.md", "config.yaml", "skills", "skill-bundles", "cron"]:
        if rel not in owned_norm:
            warn(f"distribution_owned does not include {rel}")


def validate_bundles(root: Path, external_skills: set[str] | None) -> None:
    bundle_dir = root / "skill-bundles"
    if not bundle_dir.exists():
        fail("skill-bundles/ is missing")
    found = False
    for path in sorted(bundle_dir.glob("*.yaml")):
        found = True
        data = load_yaml(path)
        name = data.get("name") or path.stem
        skills = data.get("skills")
        if not isinstance(skills, list) or not skills:
            fail(f"{path}: skills must be a non-empty list")
        if "instruction" not in data:
            warn(f"{path}: missing instruction")
        if external_skills is not None:
            missing = [s for s in skills if s not in external_skills and not (root / "skills" / s).exists()]
            if missing:
                warn(f"bundle {name} references missing skills: {', '.join(missing)}")
    if not found:
        fail("No skill bundles found")


def discover_external_skills(source: Path | None) -> set[str] | None:
    if source is None:
        return None
    if not source.exists():
        warn(f"CLAUDE_TRADING_SKILLS_REPO does not exist: {source}")
        return set()
    skills_dir = source / "skills"
    if not skills_dir.exists():
        warn(f"External repo has no skills/ directory: {skills_dir}")
        return set()
    skill_names = {p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists()}
    index = source / "skills-index.yaml"
    if not index.exists():
        warn(f"External repo has no skills-index.yaml: {index}")
    return skill_names


def validate_json_files(root: Path) -> None:
    for path in [root / "mcp.json", root / "mcp.example.json"]:
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                fail(f"Invalid JSON in {path}: {exc}")


def validate_prompts_and_schedules(root: Path) -> None:
    schedules = load_yaml(root / "data" / "schedule-presets.yaml")
    if not schedules.get("timezone"):
        fail("schedule-presets.yaml is missing the top-level `timezone:` field")
    for slug, preset in (schedules.get("presets") or {}).items():
        prompt_file = root / preset.get("prompt_file", "")
        if not prompt_file.exists():
            fail(f"Schedule preset {slug} references missing prompt: {prompt_file}")
        if not preset.get("schedule"):
            fail(f"Schedule preset {slug} missing schedule")
        if not preset.get("name"):
            fail(f"Schedule preset {slug} missing human-readable `name:`")
        skills = preset.get("skills")
        if not isinstance(skills, list) or not skills:
            fail(f"Schedule preset {slug} missing non-empty `skills:` list")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-root", default=".", help="Path to repository/profile root")
    parser.add_argument("--external-skills-repo", default=os.environ.get("CLAUDE_TRADING_SKILLS_REPO"))
    args = parser.parse_args()

    root = Path(args.profile_root).resolve()
    if not root.exists():
        fail(f"profile root does not exist: {root}")

    external = Path(args.external_skills_repo).expanduser().resolve() if args.external_skills_repo else None
    external_skills = discover_external_skills(external)

    validate_distribution(root)
    validate_json_files(root)
    validate_prompts_and_schedules(root)
    validate_bundles(root, external_skills)

    print("OK: package structure validated")


if __name__ == "__main__":
    main()
