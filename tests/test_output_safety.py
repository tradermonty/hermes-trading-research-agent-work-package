"""Forbidden-phrase checks for SOUL.md, prompts, and bundle instructions.

These are static lints that fail if direct execution language (buy/sell at
$price, place orders, guaranteed-return claims) leaks into the materials
the agent reads at runtime.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]

# (regex_pattern, label_for_error_message)
EN_FORBIDDEN: list[tuple[str, str]] = [
    (r"\bbuy at \$", "explicit-buy-price"),
    (r"\bsell at \$", "explicit-sell-price"),
    (r"\bplace a (market|limit) order\b", "order-placement"),
    (r"\benter (now|immediately)\b", "urgency-entry"),
    (r"\baccumulate (shares )?now\b", "urgency-accumulate"),
    (r"\b(guaranteed|sure) (return|setup|profit)\b", "guaranteed-claim"),
    (r"\bcan('?| no)t lose\b", "no-loss-claim"),
]

JA_FORBIDDEN: list[tuple[str, str]] = [
    (r"成行で買え", "ja-market-buy"),
    (r"指値で売れ", "ja-limit-sell"),
    (r"今すぐ買い", "ja-buy-now"),
    (r"今すぐ売り", "ja-sell-now"),
    (r"買うべき", "ja-should-buy"),
    (r"売るべき", "ja-should-sell"),
    (r"買いを検討すべき局面", "ja-buy-consideration-phrase"),
    (r"売りを検討すべき局面", "ja-sell-consideration-phrase"),
    (r"全力で?入(れ|る)", "ja-all-in-enter"),
    (r"全力買い", "ja-all-in-buy"),
    (r"今入(れ|る)", "ja-enter-now"),
    (r"確実に儲かる", "ja-sure-profit"),
    (r"絶対に勝てる", "ja-sure-win-absolute"),
    (r"必ず勝てる", "ja-sure-win"),
    (r"損切り(は)?不要", "ja-no-stop-loss"),
    # trading-context-only 確定 forms (bare 確定 has too many false positives)
    (r"利益確定", "ja-profit-fixed"),
    (r"勝ち確定", "ja-win-fixed"),
    (r"上昇確定", "ja-rise-fixed"),
    (r"儲かる.*確定", "ja-profit-confirmed"),
]


def _collect_targets() -> list[Path]:
    """Files to scan: SOUL.md, all bundle instructions (via yaml), all prompts.

    Bundle YAML files are returned and the instruction body is extracted when
    scanning. SOUL.md and prompts/*.md are scanned in full.
    """
    targets: list[Path] = []
    soul = ROOT / "SOUL.md"
    if soul.exists():
        targets.append(soul)
    targets.extend(sorted((ROOT / "prompts").glob("*.md")))
    targets.extend(sorted((ROOT / "skill-bundles").glob("*.yaml")))
    return targets


def _read_scannable_text(path: Path) -> str:
    """Return the text to scan. For bundle YAMLs, just instruction body.

    For Markdown files, return the raw file content.
    """
    if path.suffix == ".yaml":
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return str(data.get("instruction", ""))
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("pattern,label", EN_FORBIDDEN + JA_FORBIDDEN)
def test_no_forbidden_phrases(pattern: str, label: str) -> None:
    regex = re.compile(pattern, re.IGNORECASE)
    hits: list[str] = []
    for path in _collect_targets():
        text = _read_scannable_text(path)
        for match in regex.finditer(text):
            hits.append(f"{path.relative_to(ROOT)}: '{match.group(0)}'")
    assert not hits, (
        f"Forbidden pattern '{label}' (/{pattern}/) found in:\n  "
        + "\n  ".join(hits)
    )
