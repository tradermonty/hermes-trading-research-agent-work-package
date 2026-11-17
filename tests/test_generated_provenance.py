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

from scripts.run_provenance_acceptance import audit_response, expected_status

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
        if len(cells) == 7 and cells[0] == section:
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
        + "\n".join(line for line in text.splitlines() if "|" in line)
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
