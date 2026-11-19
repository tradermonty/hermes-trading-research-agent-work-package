"""Audit real Hermes responses and prove common misclassifications are rejected.

Network-free CI replays captured outputs. The opt-in runner generates NEW
responses from raw input cases; these tests never masquerade as live runs.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from scripts.run_provenance_acceptance import (
    audit_calendar_scope,
    audit_response,
    audit_unobserved_outcomes,
    expected_status,
    parse_provenance_rows,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/input_provenance"
GENERATED = FIXTURES / "generated"


@pytest.mark.parametrize("workflow", ("pre-market-routine", "after-close-review"))
@pytest.mark.parametrize("surface", ("bundle", "cron"))
def test_captured_hermes_response(workflow, surface):
    case = json.loads((FIXTURES / f"{workflow}__inputs.json").read_text())
    text = (GENERATED / f"{workflow}__{surface}.md").read_text()
    metadata = json.loads((GENERATED / f"{workflow}__{surface}.metadata.json").read_text())
    assert metadata["response_sha256"] == hashlib.sha256(text.encode()).hexdigest()
    for relative, digest in metadata["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest
    audit_response(text, case)


@pytest.mark.parametrize(
    "section,column,replacement",
    (
        ("Failed Elite", 5, "valid-empty"),
        ("Empty Elite", 5, "unavailable"),
        ("Morning news", 5, "stale"),
        ("Dashboard", 3, "2026-11-17T06:00:00-08:00"),
        ("Morning news", 6, "No timing policy supplied"),
        ("Morning news", 6, "Freshness basis: completed-close 2026-11-16"),
        ("Earnings calendar", 6, "Freshness basis: completed-close 2026-11-16"),
        ("Dashboard", 2, "unknown"),
    ),
)
def test_actual_response_audit_rejects_bad_outcomes(section, column, replacement):
    case = json.loads((FIXTURES / "pre-market-routine__inputs.json").read_text())
    text = (GENERATED / "pre-market-routine__bundle.md").read_text()
    audit_response(text, case)
    mutated = []
    for line in text.splitlines():
        cells = [
            cell.strip().replace("**", "").replace("`", "")
            for cell in line.strip().strip("|").split("|")
        ]
        if len(cells) in (6, 7) and cells[0] == section:
            cells = list(parse_provenance_rows(text)[section])
            cells[column] = replacement
            line = "| " + " | ".join(cells) + " |"
        mutated.append(line)
    with pytest.raises(AssertionError):
        audit_response("\n".join(mutated), case)


@pytest.mark.parametrize(
    "change,expected",
    (
        ({"observation_timestamp": "2026-11-17T06:01:00-08:00"}, "unavailable"),
        ({"observation_timestamp": "2026-11-17T05:00:00-08:00"}, "stale"),
        ({"observation_timestamp": None}, "unavailable"),
    ),
)
def test_timestamp_basis_uses_cutoff_and_age_limit(change, expected):
    case = json.loads((FIXTURES / "pre-market-routine__inputs.json").read_text())
    item = deepcopy(next(row for row in case["inputs"] if row["section"] == "Morning news"))
    item.update(change)
    assert expected_status(item, case["run_cutoff"]) == expected


def test_future_event_date_is_not_calendar_observation_time():
    case = json.loads((FIXTURES / "pre-market-routine__inputs.json").read_text())
    item = next(row for row in case["inputs"] if row["section"] == "Earnings calendar")
    assert all(event > case["run_cutoff"][:10] for event in item["event_dates"])
    assert expected_status(item, case["run_cutoff"]) == "fresh"
    stale = dict(item, verified_as_of="2026-11-16T05:55:00-08:00")
    assert expected_status(stale, case["run_cutoff"]) == "stale"
    assert (
        expected_status(dict(item, coverage_end="2026-11-18"), case["run_cutoff"]) == "unavailable"
    )


def test_actual_response_audit_requires_inline_disclosure():
    case = json.loads((FIXTURES / "pre-market-routine__inputs.json").read_text())
    text = (GENERATED / "pre-market-routine__bundle.md").read_text()
    audit_response(text, case)
    table_only = (
        "Source / Skill provenance\n"
        + "\n".join(
            line
            for line in text.splitlines()
            if "|" in line or line.startswith("Skill revision for all rows:")
        )
        + "\nDegraded, no matches, human decision gate, invalidation."
    )
    with pytest.raises(AssertionError, match="inline disclosure"):
        audit_response(table_only, case)


@pytest.mark.parametrize(
    "observed,expected",
    (
        ("2026-11-16", "valid-empty"),
        ("2026-11-13", "stale"),
        ("2026-11-17", "unavailable"),
    ),
)
def test_empty_completed_close_screen_respects_its_basis(observed, expected):
    item = dict(
        fetch="success",
        schema_valid=True,
        row_count=0,
        observation_date=observed,
        basis={"kind": "completed-close", "expected_session": "2026-11-16"},
    )
    assert expected_status(item, "2026-11-17T06:00:00-08:00") == expected


def test_real_regression_earnings_does_not_prove_macro_events_absent():
    case = json.loads((FIXTURES / "pre-market-routine__inputs.json").read_text())
    text = (FIXTURES / "regressions/earnings_not_economic.md").read_text()
    metadata = json.loads(
        (FIXTURES / "regressions/earnings_not_economic.metadata.json").read_text()
    )
    assert hashlib.sha256(text.encode()).hexdigest() == metadata["response_sha256"]
    with pytest.raises(AssertionError, match="economic-calendar availability"):
        audit_calendar_scope(text, case)


def test_real_regression_missing_signal_inputs_are_not_zero_changes():
    case = json.loads((FIXTURES / "after-close-review__inputs.json").read_text())
    text = (FIXTURES / "regressions/missing_observations_not_zero.md").read_text()
    metadata = json.loads(
        (FIXTURES / "regressions/missing_observations_not_zero.metadata.json").read_text()
    )
    assert hashlib.sha256(text.encode()).hexdigest() == metadata["response_sha256"]
    with pytest.raises(AssertionError, match="Missing observations"):
        audit_unobserved_outcomes(text, case)


@pytest.mark.parametrize("workflow", ("pre-market-routine", "after-close-review"))
def test_current_table_semantic_audit_and_expected_date(workflow):
    # Deterministic adaptation exercises the merged auditor, not new inference.
    from scripts.validate_brief_provenance import HEADER

    case = json.loads((FIXTURES / f"{workflow}__inputs.json").read_text())
    text = (GENERATED / f"{workflow}__bundle.md").read_text()
    rows = parse_provenance_rows(text)
    normalized_rows = []
    for item in case["inputs"]:
        row = rows[item["section"]]
        observed = (
            item.get("observation_date")
            or item.get("observation_timestamp")
            or item.get("verified_as_of")
            or "unknown"
        )
        expected = item["basis"].get("expected_session", case["run_cutoff"][:10])
        normalized = [
            *row[:3],
            observed[:10] if observed != "unknown" else observed,
            expected,
            expected_status(item, case["run_cutoff"]).replace("-", "_"),
            row[6] + f"; observation timestamp {observed}; Retrieved at {item['retrieved_at']}",
        ]
        normalized_rows.append("| " + " | ".join(normalized) + " |")
    prose = "\n".join(line for line in text.splitlines() if "|" not in line)
    text = (
        prose
        + "\n### Source / Skill provenance\n| "
        + " | ".join(HEADER)
        + " |\n|"
        + "---|" * 7
        + "\n"
        + "\n".join(normalized_rows)
    )
    text = text.replace("valid-empty", "valid_empty")
    audit_response(text, case, current_contract=True)
    # Free-text cells may contain escaped pipes without adding table columns.
    for column in (1, 6):
        for backslashes in (1, 2, 3, 4):
            escaped_lines = []
            for line in text.splitlines():
                if line.startswith("| Dashboard |"):
                    cells = list(parse_provenance_rows(text)["Dashboard"])
                    cells[column] += " additional caveat A " + "\\" * backslashes + "| B"
                    line = "| " + " | ".join(cells) + " |"
                escaped_lines.append(line)
            audit_response("\n".join(escaped_lines), case, current_contract=True)
    # A correct timestamp in impact must not hide an incorrect date cell.
    with pytest.raises(AssertionError, match="wrong observation date"):
        audit_response(
            text.replace("| 2026-03-27 |", "| 2026-03-26 |"), case, current_contract=True
        )
    # Prompt echo cannot supply provenance missing from the actual response.
    with pytest.raises(AssertionError):
        audit_response(text + "\n## Response\nNo provenance provided.", case, current_contract=True)
    bad = text.replace("| unavailable |", "| valid_empty |")
    with pytest.raises(AssertionError):
        audit_response(bad, case, current_contract=True)
    with pytest.raises(AssertionError):
        audit_response(
            text.replace(
                f"| {case['calendar']['expected_completed_session']} | stale |",
                "| 2026-11-15 | stale |",
            ),
            case,
            current_contract=True,
        )


def test_generation_request_uses_current_date_cells_without_expected_labels():
    from scripts.run_provenance_acceptance import build_acceptance_request

    case = json.loads((FIXTURES / "pre-market-routine__inputs.json").read_text())
    request = build_acceptance_request(case)
    assert (
        "Keep Observation date and Expected observation date cells as YYYY-MM-DD or unknown"
        in request
    )
    assert "Put full ISO observation/retrieval timestamps" in request
    assert "in Impact / next step" in request
    assert request.endswith(json.dumps(case, indent=2))
