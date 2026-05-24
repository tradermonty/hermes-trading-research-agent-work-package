from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_distribution_manifest_has_expected_name():
    data = yaml.safe_load((ROOT / "distribution.yaml").read_text())
    assert data["name"] == "trading-research-assistant"
    assert "skill-bundles/" in data["distribution_owned"]


def test_distribution_manifest_includes_user_docs_and_env_example():
    """Quick Start in README depends on .env.EXAMPLE being copied into the
    installed profile. README.ja.md and CHANGELOG.md are also user-facing."""
    data = yaml.safe_load((ROOT / "distribution.yaml").read_text())
    owned = set(data["distribution_owned"])
    for required in (".env.EXAMPLE", "README.ja.md", "CHANGELOG.md"):
        assert required in owned, f"distribution_owned missing {required}"
        assert (ROOT / required).exists(), f"{required} listed but not on disk"


def test_distribution_manifest_declares_hermes_trading_timezone():
    """`cron/create_cron_jobs.py` reads HERMES_TRADING_TIMEZONE to expand
    the `{{TIMEZONE}}` token in scheduled prompts; the manifest must
    declare it as an optional env so the installer surfaces it."""
    data = yaml.safe_load((ROOT / "distribution.yaml").read_text())
    entries = data.get("env_requires") or []
    by_name = {e.get("name"): e for e in entries if isinstance(e, dict)}
    entry = by_name.get("HERMES_TRADING_TIMEZONE")
    assert entry is not None, "env_requires missing HERMES_TRADING_TIMEZONE"
    assert entry.get("required") is False, (
        "HERMES_TRADING_TIMEZONE should be optional (required: false)"
    )


def test_bundles_have_required_shape():
    for path in (ROOT / "skill-bundles").glob("*.yaml"):
        data = yaml.safe_load(path.read_text())
        assert data.get("name")
        assert isinstance(data.get("skills"), list) and data["skills"]
        assert data.get("instruction")


def test_safety_language_present():
    soul = (ROOT / "SOUL.md").read_text().lower()
    assert "not a signal service" in soul
    assert "do not place trades" in soul
    assert "do not tell the user to buy or sell" in soul


def test_pre_market_prompt_has_required_sections():
    prompt = (ROOT / "prompts" / "pre-market-routine.md").read_text().lower()
    for section in ["market regime", "earnings movers", "watchlist", "data freshness"]:
        assert section in prompt
