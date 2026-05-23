#!/usr/bin/env python3
"""Create the Hermes cron jobs defined in data/schedule-presets.yaml.

This script is the single runtime entry point for cron job creation. It is
invoked by `cron/create_cron_jobs.sh` (a thin wrapper) and reads the schedule,
job name, prompt file, and skill list from the YAML preset file rather than
hard-coding them in shell.

Operator-facing behaviour:

- Warns (stderr) when the host's IANA timezone differs from the preset
  timezone, since Hermes v0.14.0 has no per-job `--tz` flag and the cron
  expression fires in the host OS local timezone. The warning is
  non-interactive — the script continues regardless. See
  docs/03-hermes-compatibility-notes.md.
- `HERMES_TRADING_TIMEZONE` is intentionally NOT consulted here. Per the
  project docs, that env var is a report-body label only and has no
  effect on the scheduler.
- `--dry-run` prints the Hermes CLI invocations instead of executing them.

Exits:
- 0 on success.
- 1 if `$HERMES_PROFILE_CMD` is not on PATH.
- 2 if PyYAML is not installed.
"""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERROR: PyYAML is required for cron/create_cron_jobs.py. "
        "Install with: python3 -m pip install pyyaml\n"
    )
    sys.exit(2)

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError as exc:  # pragma: no cover - Python <3.9
    sys.stderr.write(f"ERROR: zoneinfo is required (Python 3.9+): {exc}\n")
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
PRESET_FILE = ROOT / "data" / "schedule-presets.yaml"
COMPAT_DOC = "docs/03-hermes-compatibility-notes.md"


def _emit_warning(lines: list[str]) -> None:
    """Write a multi-line WARNING block to stderr."""
    sys.stderr.write("WARNING: " + lines[0] + "\n")
    for line in lines[1:]:
        sys.stderr.write("         " + line + "\n")


def _zoneinfo_or_none(name: str) -> ZoneInfo | None:
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return None


def _resolve_host_zone() -> str | None:
    """Return the host IANA zone name, or None when unknown.

    Resolution order:
    1. `TZ` env var when set — accept any string `ZoneInfo` can resolve
       (slash optional). If `ZoneInfo(TZ)` raises, the host zone is
       unknown; do NOT fall through to /etc/localtime (that would mask
       a deliberately bad `TZ`).
    2. `TZ` env var unset — inspect /etc/localtime:
       - Try `os.readlink` first (target is typically un-versioned).
       - Fall back to `Path.resolve()` if it is a regular file.
       - Take everything after the last `/zoneinfo/` segment as the
         IANA name and confirm via `ZoneInfo`.
    3. Otherwise unknown.
    """
    tz_env = os.environ.get("TZ")
    if tz_env is not None:
        return tz_env if _zoneinfo_or_none(tz_env) is not None else None

    localtime = Path("/etc/localtime")
    if not localtime.exists():
        return None

    candidates: list[str] = []
    try:
        candidates.append(os.readlink(localtime))
    except OSError:
        pass
    try:
        candidates.append(str(localtime.resolve()))
    except OSError:
        pass

    for raw in candidates:
        marker = "/zoneinfo/"
        idx = raw.rfind(marker)
        if idx == -1:
            continue
        name = raw[idx + len(marker):]
        if _zoneinfo_or_none(name) is not None:
            return name
    return None


def check_host_timezone(expected_zone: str) -> None:
    """Emit a stderr WARNING when host IANA zone differs from `expected_zone`.

    Does not raise or exit — operator-visible feedback only.
    """
    if _zoneinfo_or_none(expected_zone) is None:
        _emit_warning([
            f"preset timezone '{expected_zone}' is not a recognised IANA zone.",
            "Cron will still be created using the host's local time.",
            f"See {COMPAT_DOC} for context.",
        ])
        return

    host_zone = _resolve_host_zone()
    if host_zone is None:
        _emit_warning([
            "could not verify the host IANA timezone.",
            f"Preset expects '{expected_zone}'; cron expressions will fire "
            "in whatever local time this host actually uses.",
            "Confirm the host TZ before relying on the schedule.",
            f"See {COMPAT_DOC} for context.",
        ])
        return

    if host_zone == expected_zone:
        return

    # Best-effort: also report whether today's UTC offsets happen to
    # match, since a same-offset mismatch (Phoenix vs LA in summer) is the
    # most surprising case.
    now = datetime.now()
    host_offset = now.astimezone(ZoneInfo(host_zone)).utcoffset()
    expected_offset = now.astimezone(ZoneInfo(expected_zone)).utcoffset()
    offset_note = (
        "same UTC offset today, but DST rules differ"
        if host_offset == expected_offset
        else "different UTC offset"
    )
    _emit_warning([
        f"host timezone '{host_zone}' differs from preset timezone "
        f"'{expected_zone}' ({offset_note}).",
        "Hermes v0.14.0 has no per-job --tz flag; cron expressions fire "
        "in the host local timezone.",
        "Either set the host to the preset timezone, or rewrite the cron "
        "expressions in data/schedule-presets.yaml for your host.",
        f"See {COMPAT_DOC} for context.",
    ])


def load_presets() -> tuple[str, dict[str, dict]]:
    """Return (expected_timezone, ordered_presets_dict)."""
    if not PRESET_FILE.exists():
        sys.stderr.write(f"ERROR: preset file missing: {PRESET_FILE}\n")
        sys.exit(1)
    data = yaml.safe_load(PRESET_FILE.read_text(encoding="utf-8")) or {}
    timezone = data.get("timezone")
    presets = data.get("presets") or {}
    if not isinstance(timezone, str) or not timezone:
        sys.stderr.write(f"ERROR: top-level 'timezone' missing in {PRESET_FILE}\n")
        sys.exit(1)
    if not presets:
        sys.stderr.write(f"ERROR: no presets defined in {PRESET_FILE}\n")
        sys.exit(1)
    return timezone, presets


def build_command(
    profile_cmd: str,
    deliver: str,
    preset: dict,
) -> list[str]:
    prompt_path = ROOT / preset["prompt_file"]
    prompt_body = prompt_path.read_text(encoding="utf-8")
    cmd = [
        profile_cmd,
        "cron",
        "create",
        preset["schedule"],
        prompt_body,
        "--name",
        preset["name"],
        "--deliver",
        deliver,
    ]
    for skill in preset["skills"]:
        cmd.extend(["--skill", skill])
    return cmd


def _shell_quote_cmd(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print Hermes CLI commands without executing them.",
    )
    args = parser.parse_args(argv)

    expected_tz, presets = load_presets()
    check_host_timezone(expected_tz)

    profile_cmd = os.environ.get("HERMES_PROFILE_CMD", "trading-research-assistant")
    deliver = os.environ.get("HERMES_CRON_DELIVER", "local")

    if shutil.which(profile_cmd) is None:
        sys.stderr.write(
            f"Profile command '{profile_cmd}' not found. "
            "Install with --alias or set HERMES_PROFILE_CMD.\n"
        )
        return 1

    for slug, preset in presets.items():
        missing = [k for k in ("name", "schedule", "prompt_file", "skills") if k not in preset]
        if missing:
            sys.stderr.write(f"ERROR: preset {slug} missing fields: {missing}\n")
            return 1
        cmd = build_command(profile_cmd, deliver, preset)
        if args.dry_run:
            # Print a shell-safe one-liner per job, in preset order.
            # `# JOB:` prefix distinguishes the header from `#` lines
            # that may appear inside the quoted prompt body.
            print(f"# JOB: {preset['name']}")
            print(_shell_quote_cmd(cmd))
            continue
        print(f"Creating cron job: {preset['name']}")
        subprocess.run(cmd, check=True)

    if not args.dry_run:
        print(f"Done. Run: {profile_cmd} cron list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
