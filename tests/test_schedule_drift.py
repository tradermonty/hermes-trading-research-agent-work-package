"""Drift tests between data/schedule-presets.yaml and cron/create_cron_jobs.py.

These lock in two contracts:
1. `data/schedule-presets.yaml` is the single source of truth for the four
   cron jobs (schedule + name + skills + prompt_file + timezone). The
   Python entry point reads everything from the YAML; it must not
   hard-code schedules or skill lists in its own body.
2. The runtime host-TZ check warns on IANA-zone mismatch with the
   preset timezone, even when the offset coincides (Phoenix vs LA).

Tests that exercise `cron/create_cron_jobs.py` use `HERMES_PROFILE_CMD=true`
to point the wrapper at the POSIX `true` binary, then pass `--dry-run` so
no actual Hermes CLI call is made.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[assignment]
    ZoneInfoNotFoundError = Exception  # type: ignore[assignment, misc]

ROOT = Path(__file__).resolve().parents[1]
PRESET_FILE = ROOT / "data" / "schedule-presets.yaml"
SCRIPT_FILE = ROOT / "cron" / "create_cron_jobs.py"
EXPECTED_PRESETS = (
    "pre-market-routine",
    "after-close-review",
    "weekly-portfolio-review",
    "monthly-performance-review",
)
EXPECTED_SCHEDULES = ("0 6 * * 1-5", "15 13 * * 1-5", "0 9 * * 6", "0 9 1 * *")
EXPECTED_TZ = "America/Los_Angeles"


def _load_presets() -> dict:
    return yaml.safe_load(PRESET_FILE.read_text(encoding="utf-8")) or {}


def _tzdata_available(zone: str = EXPECTED_TZ) -> bool:
    if ZoneInfo is None:
        return False
    try:
        ZoneInfo(zone)
    except Exception:
        return False
    return True


def _run_dry(env_overrides: dict[str, str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    # Make sure the script's PyYAML / zoneinfo lookups don't depend on the
    # caller's TZ unless the test explicitly sets one.
    env.pop("TZ", None)
    env.update(env_overrides)
    env["HERMES_PROFILE_CMD"] = env.get("HERMES_PROFILE_CMD", "true")
    return subprocess.run(
        [sys.executable, str(SCRIPT_FILE), "--dry-run"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


# --- shape ----------------------------------------------------------------


def test_preset_count_is_four():
    presets = _load_presets().get("presets") or {}
    assert tuple(presets.keys()) == EXPECTED_PRESETS, (
        f"unexpected preset keys or order: {list(presets.keys())}"
    )


def test_top_level_timezone_set():
    data = _load_presets()
    assert data.get("timezone") == EXPECTED_TZ


@pytest.mark.parametrize("slug", EXPECTED_PRESETS)
def test_each_preset_has_required_fields(slug: str):
    presets = _load_presets().get("presets") or {}
    preset = presets.get(slug)
    assert preset is not None, f"missing preset: {slug}"
    for field in ("name", "schedule", "prompt_file"):
        assert preset.get(field), f"{slug}: missing or empty `{field}`"
    skills = preset.get("skills")
    assert isinstance(skills, list) and skills, (
        f"{slug}: skills must be a non-empty list"
    )


@pytest.mark.parametrize("slug", EXPECTED_PRESETS)
def test_prompt_files_exist(slug: str):
    presets = _load_presets().get("presets") or {}
    preset = presets[slug]
    prompt_path = ROOT / preset["prompt_file"]
    assert prompt_path.exists(), f"prompt missing: {prompt_path}"


# --- no-hardcode guard ----------------------------------------------------


def test_script_does_not_hardcode_schedules():
    body = SCRIPT_FILE.read_text(encoding="utf-8")
    leaked = [s for s in EXPECTED_SCHEDULES if s in body]
    assert not leaked, (
        f"create_cron_jobs.py hard-codes cron schedules {leaked}; "
        "they should come from data/schedule-presets.yaml only"
    )


def test_script_does_not_hardcode_skill_lists():
    body = SCRIPT_FILE.read_text(encoding="utf-8")
    # Pull every skill name from the YAML and confirm none appear as
    # literal strings in the script body.
    presets = _load_presets().get("presets") or {}
    all_skills = {skill for preset in presets.values() for skill in preset["skills"]}
    leaked = sorted(s for s in all_skills if f'"{s}"' in body or f"'{s}'" in body)
    assert not leaked, (
        f"create_cron_jobs.py hard-codes skill names {leaked}; "
        "they should come from data/schedule-presets.yaml only"
    )


# --- dry-run ordering -----------------------------------------------------


def test_create_cron_jobs_dry_run_emits_each_job_in_order():
    if shutil.which("true") is None:
        pytest.skip("`true` not on PATH")
    if not _tzdata_available():
        pytest.skip("tzdata for America/Los_Angeles not available")
    # Force the host TZ to match the preset so we don't compete with
    # stderr noise from the warning path.
    result = _run_dry({"TZ": EXPECTED_TZ})
    assert result.returncode == 0, result.stderr
    lines = [line for line in result.stdout.splitlines() if line.startswith("# JOB: ")]
    expected_names = [
        "# JOB: Pre-market routine",
        "# JOB: After-close review",
        "# JOB: Weekly portfolio review",
        "# JOB: Monthly performance review",
    ]
    assert lines == expected_names, (
        f"dry-run jobs out of order or missing: {lines}"
    )


# --- host-TZ warning matrix ----------------------------------------------


@pytest.mark.skipif(not _tzdata_available(), reason="tzdata missing")
def test_host_tz_silent_when_match():
    result = _run_dry({"TZ": EXPECTED_TZ})
    assert result.returncode == 0, result.stderr
    assert "WARNING" not in result.stderr, (
        "WARNING emitted when host TZ matches preset:\n" + result.stderr
    )


@pytest.mark.skipif(not _tzdata_available("Etc/UTC"), reason="tzdata missing for Etc/UTC")
def test_host_tz_warning_on_offset_mismatch():
    result = _run_dry({"TZ": "Etc/UTC"})
    assert result.returncode == 0, result.stderr
    assert "WARNING" in result.stderr
    assert "Etc/UTC" in result.stderr
    assert EXPECTED_TZ in result.stderr


@pytest.mark.skipif(
    not _tzdata_available("America/Phoenix"),
    reason="tzdata missing for America/Phoenix",
)
def test_host_tz_warning_on_same_offset_different_zone():
    # Regression for the rev2 finding: Phoenix and Los_Angeles share an
    # offset in summer (both UTC-7) but Phoenix has no DST, so an
    # offset-only check would let this slip through.
    result = _run_dry({"TZ": "America/Phoenix"})
    assert result.returncode == 0, result.stderr
    assert "WARNING" in result.stderr
    assert "America/Phoenix" in result.stderr
    assert EXPECTED_TZ in result.stderr


@pytest.mark.skipif(not _tzdata_available(), reason="tzdata missing")
def test_host_tz_unknown_warning_when_tz_unresolvable():
    # Per the rev3 resolver, an explicit-but-bad TZ short-circuits to
    # unknown (no /etc/localtime fallthrough).
    result = _run_dry({"TZ": "Etc/NotAZone"})
    assert result.returncode == 0, result.stderr
    assert "WARNING" in result.stderr
    assert "could not verify" in result.stderr
    assert EXPECTED_TZ in result.stderr


# --- doc caveat parity ---------------------------------------------------


@pytest.mark.parametrize(
    "rel",
    [
        "cron/README.md",
        "docs/03-hermes-compatibility-notes.md",
        "README.md",
    ],
)
def test_timezone_caveat_in_docs(rel: str):
    path = ROOT / rel
    assert path.exists(), f"{rel} missing"
    text = path.read_text(encoding="utf-8")
    assert "host OS local timezone" in text or "host local timezone" in text, (
        f"{rel} should document the host-local-timezone caveat so the runtime "
        "warning is consistent with the docs"
    )
