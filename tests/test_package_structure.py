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
