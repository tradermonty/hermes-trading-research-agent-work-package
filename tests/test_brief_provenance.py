"""Issue #1: static instructions plus offline checks of synthetic brief outputs.

These tests do not imply Hermes generation or live-provider migration acceptance.
"""

from pathlib import Path
import json
import subprocess
import sys

import pytest
import yaml

from scripts.validate_brief_provenance import HEADER, validate_brief

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/brief_provenance"


@pytest.mark.parametrize("routine", ["pre-market-routine", "after-close-review"])
def test_manual_and_cron_paths_share_writer_contract(routine):
    writer = (ROOT / "skills/trading-cron-brief-writer/SKILL.md").read_text()
    marker = "Input provenance contract (morning and evening briefs):"
    contract = writer.split(marker, 1)[1].strip()
    prompt = (ROOT / f"prompts/{routine}.md").read_text()
    bundle = yaml.safe_load((ROOT / f"skill-bundles/{routine}.yaml").read_text())
    for text in (prompt, bundle["instruction"]):
        assert marker in text
        assert contract in text
    assert " | ".join(HEADER) in contract
    assert bundle["x-generated"] is False
    presets = yaml.safe_load((ROOT / "data/schedule-presets.yaml").read_text())
    preset = next(
        p for p in presets["presets"].values() if p["prompt_file"] == f"prompts/{routine}.md"
    )
    assert "trading-cron-brief-writer" in preset["skills"]


@pytest.mark.parametrize("routine", ["pre-market-routine", "after-close-review"])
@pytest.mark.parametrize(
    "scenario,status",
    [
        ("stale_dashboard", "stale"),
        ("failed_elite", "unavailable"),
        ("valid_empty", "valid_empty"),
    ],
)
def test_scenarios_keep_distinct_states_and_independent_data(routine, scenario, status):
    text = (FIXTURES / f"{routine}_{scenario}.md").read_text()
    assert validate_brief(text) == []
    assert f"| {status} |" in text
    independent_state = "carried_forward" if routine == "pre-market-routine" else "fresh"
    assert f"| {independent_state} |" in text  # independent input survives the degraded section
    assert "observation date" in text
    if scenario == "stale_dashboard":
        assert "No local key is required" in text
        assert "| unknown |" in text  # undated sector data cannot borrow overall date
    if scenario == "valid_empty":
        assert "0 validated rows" in text


def test_holiday_latest_completed_session_is_carried_forward():
    text = (FIXTURES / "holiday_carry_forward.md").read_text()
    assert validate_brief(text) == []
    assert "carried forward from 2026-05-22" in text
    assert "| carried_forward |" in text
    assert "| stale |" not in text
    assert text.index("Session state:") < text.index("Posture basis:") < text.index("Risk posture:")


@pytest.mark.parametrize(
    "before,after",
    [
        ("| stale |", "| fresh |"),
        ("| stale |", "| carried_forward |"),
        ("| stale |", "| valid_empty |"),
        ("| stale |", "| success |"),
        ("2026-11-12", "2026-02-30"),
        ("2026-11-12", "2026-11-17"),
        ("2026-11-12", "unknown"),
        ("| unknown | 2026-11-13 | unknown |", "| — | 2026-11-13 | unknown |"),
        ("| unknown | 2026-11-13 | unknown |", "| unknown | 2026-11-13 / week ahead | unknown |"),
        ("| unknown | 2026-11-13 | unknown |", "| unknown | 2026-11-13 | fresh |"),
        ("### Source / Skill provenance", "### Other"),
        ("| Source / Skill |", "| Source |"),
        ("| stale |", "| |"),
    ],
)
def test_inconsistent_or_incomplete_tables_fail(before, after):
    text = (FIXTURES / "pre-market-routine_stale_dashboard.md").read_text()
    assert before in text
    assert validate_brief(text.replace(before, after))


def test_only_actual_response_can_satisfy_the_contract():
    good = (FIXTURES / "after-close-review_valid_empty.md").read_text()
    assert validate_brief(good + "\n## Response\nMissing all provenance.")
    assert validate_brief("Prompt without table\n## Response\n" + good) == []
    assert validate_brief(good + "\n" + good)  # duplicate tables are ambiguous


@pytest.mark.parametrize("field", ["source", "impact"])
@pytest.mark.parametrize("backslashes", [1, 2, 3, 4])
def test_escaped_pipes_remain_inside_free_text_cells(field, backslashes):
    text = (FIXTURES / "pre-market-routine_valid_empty.md").read_text()
    before = "FINVIZ Elite export" if field == "source" else "0 validated rows; expected"
    after = before + " filter A " + "\\" * backslashes + "| B"
    assert before in text
    assert validate_brief(text.replace(before, after)) == []


def test_unescaped_pipes_still_add_columns():
    text = (FIXTURES / "pre-market-routine_valid_empty.md").read_text()
    after = "FINVIZ Elite export A | B"
    assert validate_brief(text.replace("FINVIZ Elite export", after))


@pytest.mark.parametrize("routine", ["pre-market-routine", "after-close-review"])
def test_live_rendering_corrections_are_in_both_invocation_paths(routine):
    prompt = (ROOT / f"prompts/{routine}.md").read_text()
    instruction = yaml.safe_load((ROOT / f"skill-bundles/{routine}.yaml").read_text())[
        "instruction"
    ]
    for text in [prompt, instruction]:
        assert "Em dashes, N/A, date ranges, and prose are invalid in date cells" in text
        assert "use `carried_forward` consistently" in text
        assert "Report a missing key only when its absence is verified" in text
        assert "Copy supplied numeric facts exactly or omit them" in text


@pytest.mark.parametrize("location", ["start", "end"])
@pytest.mark.parametrize("extra_pipes", [1, 2])
def test_extra_boundary_pipes_do_not_hide_empty_columns(location, extra_pipes):
    text = (FIXTURES / "pre-market-routine_valid_empty.md").read_text()
    lines = text.splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith("| Themes |"))
    if location == "start":
        lines[index] = "|" * extra_pipes + lines[index]
    else:
        lines[index] += "|" * extra_pipes
    assert validate_brief("\n".join(lines))


def test_cli_without_credentials_or_optional_mcps(tmp_path):
    # Shipped examples retain optional market keys and an empty MCP registry.
    assert json.loads((ROOT / "mcp.json").read_text()) == {"mcpServers": {}}
    distribution = yaml.safe_load((ROOT / "distribution.yaml").read_text())
    assert all(not entry["required"] for entry in distribution["env_requires"])
    example = (ROOT / ".env.EXAMPLE").read_text()
    assert "FMP_API_KEY=\n" in example and "FINVIZ_API_KEY=\n" in example
    script = ROOT / "scripts/validate_brief_provenance.py"
    for name, expected_code in [("after-close-review_failed_elite.md", 0), ("bad.md", 1)]:
        path = FIXTURES / name
        if name == "bad.md":
            path = tmp_path / name
            path.write_text("No provenance")
        result = subprocess.run(
            [sys.executable, str(script), str(path)], env={}, capture_output=True, text=True
        )
        assert result.returncode == expected_code, result.stderr


@pytest.mark.parametrize("status", ["fresh", "stale", "valid_empty"])
def test_same_day_timestamp_basis_keeps_current_table(status):
    text = (FIXTURES / "pre-market-routine_valid_empty.md").read_text()
    text = text.replace("| valid_empty |", f"| {status} |")
    text = text.replace(
        "0 validated rows; expected",
        "Freshness basis: timestamp; observation 2026-11-13T05:00:00-08:00; cutoff 2026-11-13T06:00:00-08:00; policy 30 minutes; 0 validated rows; expected",
    )
    assert validate_brief(text) == []
