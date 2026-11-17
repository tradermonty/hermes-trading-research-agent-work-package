"""Offline prompt contract and synthetic acceptance examples; no LLM/live test.

This distribution delegates fetching to upstream skills. These checks pin the
instructions on manual/cron paths and audit example briefs, not upstream CSV
parsers or actual Hermes rendering.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ("pre-market-routine", "after-close-review")
FIXTURES = ROOT / "tests/fixtures/input_provenance"


def instructions(workflow: str, surface: str) -> str:
    if surface == "bundle":
        return yaml.safe_load((ROOT / "skill-bundles" / f"{workflow}.yaml").read_text())[
            "instruction"
        ]
    return (ROOT / "prompts" / f"{workflow}.md").read_text()


@pytest.mark.parametrize("workflow", WORKFLOWS)
@pytest.mark.parametrize("surface", ("bundle", "cron"))
def test_input_contract_reaches_each_invocation(workflow, surface):
    text = instructions(workflow, surface)
    for rule in (
        "Section | Source / upstream dependency | Skill revision | Observation date | "
        "Retrieved at | Status | Impact / follow-up",
        "installed claude-trading-skills commit SHA and local modifications",
        "omit auth query strings and credentials",
        "per row/series",
        "Declare Freshness basis",
        "source-specific age limit",
        "future event dates are not observation timestamps",
        "Reject future observation timestamps",
        "keep it separate from completed-close posture",
        "mixed-age rows",
        "fresh (validated input meeting",
        "stale (observation older",
        "unavailable (fetch/auth/schema failure",
        "valid-empty (successful, schema-valid screen with zero matches meeting its declared freshness basis)",
        "Before the close use the latest completed regular session",
        "after the close expect today's completed session",
        "holiday/weekend carry-forward rule",
        "retain independent fresh data",
        "A valid-empty screen alone does not degrade the brief",
        "Missing FINVIZ_API_KEY affects direct Elite screens",
        "not independently validated dashboard data",
        "Manual/public fallback needs its own source and observation date",
        "Do not enable optional MCPs",
    ):
        assert rule in text


def test_contract_is_identical_on_manual_and_cron_paths():
    blocks = []
    for workflow in WORKFLOWS:
        for surface in ("bundle", "cron"):
            text = instructions(workflow, surface)
            block = text.split("Input provenance and freshness (required", 1)[1]
            blocks.append(block.split("\n\n", 2)[:2])
    assert all(block == blocks[0] for block in blocks)


def provenance_rows(text: str) -> dict[str, list[str]]:
    rows = [line for line in text.splitlines() if line.startswith("| ")]
    assert rows[0] == (
        "| Section | Source / upstream dependency | Skill revision | Observation date | "
        "Retrieved at | Status | Impact / follow-up |"
    )
    parsed = [[cell.strip() for cell in row.strip("|").split("|")] for row in rows[1:]]
    assert len(parsed) == 2
    assert all(len(row) == 7 and all(row) for row in parsed)
    return {row[0]: row for row in parsed}


@pytest.mark.parametrize("workflow", WORKFLOWS)
@pytest.mark.parametrize(
    "scenario,status,date",
    (
        ("stale_dashboard", "stale", "2026-03-27"),
        ("failed_elite", "unavailable", "unknown"),
        ("valid_empty", "valid-empty", "2026-11-16"),
        ("holiday_carry_forward", "fresh", "2026-05-22"),
    ),
)
def test_acceptance_examples_distinguish_outcomes(workflow, scenario, status, date):
    text = (FIXTURES / f"{workflow}__{scenario}.md").read_text()
    rows = provenance_rows(text)
    affected = rows["Affected section"]
    assert affected[3] == date
    assert affected[5] == status
    assert f"observation date: {date}" in text
    assert f": {status};" in text  # Inline disclosure, not only a footer.
    assert rows["Independent earnings calendar"][5] == "fresh"
    assert "Retain independent data" in rows["Independent earnings calendar"][6]
    for concept in ("Thesis:", "Invalidation:", "Risk notes:", "Human decision gate:"):
        assert concept in text
    if scenario == "stale_dashboard":
        assert "public dashboard -> upstream Finviz collection" in affected[1]
        assert "no local key required" in affected[6]
        assert "withhold dependent posture change" in affected[6]
        assert date not in affected[4]  # Download time must not replace observation date.
    elif scenario == "failed_elite":
        assert "authentication failure" in affected[6]
        assert "degraded" in affected[6]
        assert "no matches" not in text
    elif scenario == "valid_empty":
        assert "successful schema-valid screen; 0 matches; no matches" in affected[6]
        assert "no degradation from this input" in affected[6]
    else:
        assert "latest completed regular session" in affected[6]
        assert "carried forward from 2026-05-22" in text
        assert "pending fresh data / degraded" not in text


def test_credentials_and_optional_mcps_remain_optional():
    requirements = yaml.safe_load((ROOT / "data/api-requirements.yaml").read_text())
    assert "uptrend-analyzer" in requirements["no_key_or_local_data"]
    assert requirements["providers"]["finviz"]["env_var"] == "FINVIZ_API_KEY"
    manifest = yaml.safe_load((ROOT / "distribution.yaml").read_text())
    finviz = next(item for item in manifest["env_requires"] if item["name"] == "FINVIZ_API_KEY")
    assert finviz["required"] is False
    assert json.loads((ROOT / "mcp.json").read_text()) == {"mcpServers": {}}
    # Templates remain parseable examples, never activated by these instructions.
    example = json.loads((ROOT / "mcp.example.json").read_text())
    assert "finviz" in example["mcpServers"]
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    assert "mcp_servers" not in config
