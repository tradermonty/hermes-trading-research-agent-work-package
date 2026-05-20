"""Required-concept checks for skill-bundle instructions.

Each bundle's `instruction:` must reference the research-process concepts
that justify presenting output to a human reviewer: data freshness, source
provenance, thesis, invalidation, risk, and a human decision gate.

These checks complement test_output_safety.py: safety blocks bad output;
required-concept tests ensure good structure.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

# Each concept maps to a list of regex patterns; ANY hit counts as satisfied.
REQUIRED_CONCEPTS: dict[str, list[str]] = {
    "data_freshness": [
        r"data\s+freshness",
        r"freshness",
        r"as of\b",
        r"stale.*data",
        r"missing[-\s]?data",
        r"データ鮮度",
        r"最新",
    ],
    "source_provenance": [
        r"data\s+sources?",
        r"skill\s+outputs?",
        r"provenance",
        r"cite",
        r"\bsource[s]?\b",
        r"出典",
    ],
    "thesis": [
        r"\bthesis\b",
        r"投資仮説",
        r"仮説",
    ],
    "invalidation": [
        r"invalidation",
        r"無効化",
        r"破綻条件",
    ],
    "risk": [
        r"\brisk\b",
        r"リスク",
    ],
    "human_decision_gate": [
        r"human\s+(decision|next\s+action|review)",
        r"human\s+gate",
        r"decision\s+gate",
        r"manual\s+(review|approval)",
        r"do\s+not\s+(suggest|recommend)\s+execution",
        r"do\s+not\s+(execute|place|provide).{0,40}(order|execution|buy|sell)",
        r"do\s+not\s+(produce|tell|recommend).{0,40}(buy|sell)",
        r"人間.*判断",
        r"最終判断",
    ],
}


def _bundle_paths() -> list[Path]:
    return sorted((ROOT / "skill-bundles").glob("*.yaml"))


def _instruction_of(path: Path) -> str:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return str(data.get("instruction", ""))


@pytest.mark.parametrize("bundle_path", _bundle_paths(), ids=lambda p: p.stem)
@pytest.mark.parametrize("concept", list(REQUIRED_CONCEPTS.keys()))
def test_bundle_instruction_covers_concept(bundle_path: Path, concept: str) -> None:
    text = _instruction_of(bundle_path)
    assert text, f"{bundle_path.relative_to(ROOT)} has empty instruction"
    patterns = REQUIRED_CONCEPTS[concept]
    matched = any(re.search(p, text, re.IGNORECASE) for p in patterns)
    assert matched, (
        f"{bundle_path.relative_to(ROOT)} instruction is missing required "
        f"concept '{concept}'. Add wording matching one of: {patterns}"
    )


def test_fixture_negative_example_triggers_safety() -> None:
    """Sanity: the 'bad' fixture must hit at least one forbidden pattern.

    This guards against silent regression of test_output_safety.py: if the
    forbidden patterns ever stop matching real bad text, this test fails.
    """
    import re as _re
    from tests.test_output_safety import EN_FORBIDDEN, JA_FORBIDDEN

    bad = (ROOT / "tests" / "fixtures" / "sample_outputs" / "bad_example.md").read_text(
        encoding="utf-8"
    )
    hits = [
        label
        for pattern, label in EN_FORBIDDEN + JA_FORBIDDEN
        if _re.search(pattern, bad, _re.IGNORECASE)
    ]
    assert hits, "bad_example.md should trigger forbidden patterns but did not"


def test_fixture_good_example_clean() -> None:
    """Sanity: the 'good' fixture must NOT trigger forbidden patterns."""
    import re as _re
    from tests.test_output_safety import EN_FORBIDDEN, JA_FORBIDDEN

    good = (ROOT / "tests" / "fixtures" / "sample_outputs" / "good_example.md").read_text(
        encoding="utf-8"
    )
    hits = [
        f"{label} -> '{_re.search(pattern, good, _re.IGNORECASE).group(0)}'"
        for pattern, label in EN_FORBIDDEN + JA_FORBIDDEN
        if _re.search(pattern, good, _re.IGNORECASE)
    ]
    assert not hits, f"good_example.md unexpectedly triggered: {hits}"
