"""TICKET-013: pre-market-routine bundle/prompt must carry the
Session state / Posture basis / Source-provenance literal wording.

This is a lightweight existence check — we do NOT regex over real
LLM output. The contract is that both the bundle instruction
(chat invocation path) and the cron prompt body (auto-fire path)
carry the required literal phrases so the LLM receives them in
both invocation modes.

The phrases are bundle/prompt-side; the test asserts they are
present in both files. LLM rendering of the eventual output is
not constrained by this test — that is intentionally left free
so the assistant can adapt wording while staying inside the
contract pinned here.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO / "skill-bundles" / "pre-market-routine.yaml"
PROMPT_PATH = REPO / "prompts" / "pre-market-routine.md"

REQUIRED_PHRASES = [
    "Session state",
    "Posture basis",
    "latest completed regular-session close",
    "carried forward",
    "pending fresh data",
    "Source / Skill provenance",
]


def _bundle_instruction() -> str:
    data = yaml.safe_load(BUNDLE_PATH.read_text(encoding="utf-8"))
    return data.get("instruction", "")


def _prompt_body() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


@pytest.mark.parametrize("phrase", REQUIRED_PHRASES)
def test_bundle_instruction_carries_phrase(phrase: str):
    text = _bundle_instruction()
    assert phrase in text, (
        f"skill-bundles/pre-market-routine.yaml instruction missing "
        f"required TICKET-013 phrase {phrase!r}"
    )


@pytest.mark.parametrize("phrase", REQUIRED_PHRASES)
def test_prompt_body_carries_phrase(phrase: str):
    text = _prompt_body()
    assert phrase in text, (
        f"prompts/pre-market-routine.md missing required TICKET-013 "
        f"phrase {phrase!r}"
    )
