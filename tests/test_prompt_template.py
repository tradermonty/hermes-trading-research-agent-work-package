"""Tests for the `{{TIMEZONE}}` prompt template expansion.

Locks in two contracts:

1. Schedule-bound prompts (derived from
   `data/schedule-presets.yaml:presets[*].prompt_file`) must contain
   exactly one `{{TIMEZONE}}` token. Event-driven / manual prompts
   (currently `earnings-movers-triage.md`, `trade-journal.md`) must
   contain zero tokens. The set is derived, not hard-coded, so the
   contract auto-adapts as prompts are added.
2. At cron-create time the runtime expands `{{TIMEZONE}}` using a
   priority stack: shell env > `<repo-root>/.env` > preset YAML
   > literal `America/Los_Angeles`. The scheduler-side host-TZ
   warning intentionally ignores `HERMES_TRADING_TIMEZONE` (v0.1.2
   separation) — overriding the report label must NOT trigger that
   warning.

Subprocess cases reuse the `_run_dry` pattern from
`tests/test_schedule_drift.py:_run_dry()`. `.env`-honoring cases are
in-process (no subprocess) because `ENV_FILE` is derived from
`__file__`; a subprocess + `cwd=` mirror would silently read the
real repo `.env`.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
PRESET_FILE = ROOT / "data" / "schedule-presets.yaml"
SCRIPT_FILE = ROOT / "cron" / "create_cron_jobs.py"
PROMPTS_DIR = ROOT / "prompts"
TOKEN = "{{TIMEZONE}}"
EXPECTED_TZ = "America/Los_Angeles"


def _tzdata_available(zone: str = EXPECTED_TZ) -> bool:
    if ZoneInfo is None:
        return False
    try:
        ZoneInfo(zone)
    except Exception:
        return False
    return True


def _schedule_bound_prompt_files() -> set[Path]:
    """Resolve the prompt_file paths used by the schedule presets."""
    data = yaml.safe_load(PRESET_FILE.read_text(encoding="utf-8")) or {}
    presets = data.get("presets") or {}
    return {(ROOT / p["prompt_file"]).resolve() for p in presets.values() if p.get("prompt_file")}


def _all_prompt_files() -> set[Path]:
    return {p.resolve() for p in PROMPTS_DIR.glob("*.md")}


def _run_dry(env_overrides: dict[str, str]) -> subprocess.CompletedProcess[str]:
    """Subprocess-invoke create_cron_jobs.py --dry-run with controlled env.

    Matches tests/test_schedule_drift.py:_run_dry() so the two suites
    share the same execution pattern.
    """
    env = os.environ.copy()
    env.pop("TZ", None)
    env.pop("HERMES_TRADING_TIMEZONE", None)
    env.update(env_overrides)
    env.setdefault("HERMES_PROFILE_CMD", "true")
    return subprocess.run(
        [sys.executable, str(SCRIPT_FILE), "--dry-run"],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _import_runtime_module():
    """Import cron/create_cron_jobs.py for in-process tests.

    `cron/` has no __init__.py, so we load via importlib.
    Module is cached after the first call.
    """
    spec = importlib.util.spec_from_file_location(
        "cron_create_cron_jobs_module", SCRIPT_FILE
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- contract: which prompts carry the token ---------------------------------


def test_schedule_bound_prompts_use_token():
    schedule_bound = _schedule_bound_prompt_files()
    assert schedule_bound, "no schedule-bound prompts found in preset YAML"
    for path in sorted(schedule_bound):
        assert path.exists(), f"preset references missing prompt: {path}"
        body = path.read_text(encoding="utf-8")
        count = body.count(TOKEN)
        assert count == 1, (
            f"{path.relative_to(ROOT)}: expected exactly one {TOKEN}, found {count}"
        )


def test_non_schedule_prompts_have_no_timezone_token():
    schedule_bound = _schedule_bound_prompt_files()
    extras = sorted(_all_prompt_files() - schedule_bound)
    # Sanity: there should be at least one event-driven prompt today
    # (earnings-movers-triage.md, trade-journal.md). If this list ever
    # becomes empty, the assertion below trivially passes — which is
    # also fine.
    for path in extras:
        body = path.read_text(encoding="utf-8")
        assert TOKEN not in body, (
            f"{path.relative_to(ROOT)} is event-driven; must not contain {TOKEN}"
        )


# --- expansion matrix (subprocess) ------------------------------------------


@pytest.mark.skipif(not _tzdata_available(), reason="tzdata for America/Los_Angeles missing")
def test_default_expansion_uses_preset_timezone(tmp_path: Path):
    # Default-branch test: no shell env, no .env shadowing. We can't
    # remove the real repo .env in CI, but on this repo there is none
    # by design. If a contributor introduces one locally, skip.
    if (ROOT / ".env").exists():
        pytest.skip("local .env shadows preset-YAML branch")
    result = _run_dry({"TZ": EXPECTED_TZ})
    assert result.returncode == 0, result.stderr
    assert f"Timezone label for the report: {EXPECTED_TZ}." in result.stdout
    assert TOKEN not in result.stdout, "raw token leaked into dry-run output"


@pytest.mark.skipif(not _tzdata_available(), reason="tzdata for America/Los_Angeles missing")
def test_shell_env_overrides_report_label():
    result = _run_dry(
        {"TZ": EXPECTED_TZ, "HERMES_TRADING_TIMEZONE": "Asia/Tokyo"}
    )
    assert result.returncode == 0, result.stderr
    assert "Timezone label for the report: Asia/Tokyo." in result.stdout
    assert TOKEN not in result.stdout


@pytest.mark.skipif(not _tzdata_available(), reason="tzdata for America/Los_Angeles missing")
def test_env_override_does_not_trigger_scheduler_warning():
    # Regression for the v0.1.2 separation: HERMES_TRADING_TIMEZONE
    # must NOT shift the scheduler's host-TZ comparison.
    result = _run_dry(
        {"TZ": EXPECTED_TZ, "HERMES_TRADING_TIMEZONE": "Asia/Tokyo"}
    )
    assert result.returncode == 0, result.stderr
    assert "WARNING" not in result.stderr, (
        "scheduler warning should not fire when host TZ matches preset, "
        f"even with HERMES_TRADING_TIMEZONE override:\n{result.stderr}"
    )


@pytest.mark.skipif(not _tzdata_available(), reason="tzdata for America/Los_Angeles missing")
def test_dry_run_does_not_leak_token():
    if (ROOT / ".env").exists():
        pytest.skip("local .env shadows preset-YAML branch")
    result = _run_dry({"TZ": EXPECTED_TZ})
    assert result.returncode == 0, result.stderr
    assert TOKEN not in result.stdout, "raw token must not appear in cron-create args"


# --- .env handling (in-process unit tests) -----------------------------------


def test_dotenv_overrides_report_label_when_shell_env_unset(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    mod = _import_runtime_module()
    monkeypatch.delenv("HERMES_TRADING_TIMEZONE", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("HERMES_TRADING_TIMEZONE=Europe/London\n", encoding="utf-8")
    # Pass env_path explicitly — covers the threaded-argument path and
    # avoids global-state mutation.
    assert (
        mod._resolve_report_timezone("America/Los_Angeles", env_path=env_file)
        == "Europe/London"
    )


def test_shell_env_wins_over_dotenv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    mod = _import_runtime_module()
    monkeypatch.setenv("HERMES_TRADING_TIMEZONE", "Asia/Tokyo")
    env_file = tmp_path / ".env"
    env_file.write_text("HERMES_TRADING_TIMEZONE=Europe/London\n", encoding="utf-8")
    assert (
        mod._resolve_report_timezone("America/Los_Angeles", env_path=env_file)
        == "Asia/Tokyo"
    )


def test_monkeypatched_env_file_is_honored(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """When env_path is not passed explicitly, _resolve_report_timezone
    must consult the module-level ENV_FILE at call time (not bind it at
    function-definition time). Regression for the rev3/rev4 default-arg
    trap."""
    mod = _import_runtime_module()
    monkeypatch.delenv("HERMES_TRADING_TIMEZONE", raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text("HERMES_TRADING_TIMEZONE=Europe/London\n", encoding="utf-8")
    monkeypatch.setattr(mod, "ENV_FILE", env_file)
    # No env_path argument — must still resolve via the patched ENV_FILE.
    assert (
        mod._resolve_report_timezone("America/Los_Angeles") == "Europe/London"
    )


def test_resolve_report_timezone_unit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    mod = _import_runtime_module()
    monkeypatch.delenv("HERMES_TRADING_TIMEZONE", raising=False)

    # preset present → preset wins (when no env / no .env)
    nonexistent_env = tmp_path / "no-such-.env"
    assert (
        mod._resolve_report_timezone("America/Los_Angeles", env_path=nonexistent_env)
        == "America/Los_Angeles"
    )

    # everything empty → fallback + warning
    capsys.readouterr()  # drain
    result = mod._resolve_report_timezone("", env_path=nonexistent_env)
    assert result == "America/Los_Angeles"
    err = capsys.readouterr().err
    assert "WARNING" in err and "falling back" in err
