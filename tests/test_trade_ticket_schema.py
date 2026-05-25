"""B-3 / TICKET-009: `/trade-ticket` schema + bundle contract tests.

Locks in three layers of the trade ticket contract:

1. **Schema layer** (JSON Schema draft/2020-12). Top-level required
   fields, status enum exact membership + order,
   `approval.required` is constant `true`, and each status branch
   in the schema's `allOf`/`if`/`then` enforces its own required
   approval fields (APPROVED also tightens numeric fields to
   no-null).
2. **Business-invariant layer**. The reviewer's `approval.confirmed.*`
   values must match the ticket body (`candidate.*`, `plan.*`,
   `risk.*`) and, on APPROVED, all of them must be non-null /
   non-empty. JSON Schema cannot express cross-field equality
   cleanly, so the helper owns that check. Defence in depth:
   even if the schema is loosened in a future edit, this layer
   still catches a regression.
3. **Bundle instruction layer**. The bundle prompt must literally
   document the five status values, the five operator verbs, the
   positive-form boundary statements, the `confirmed.*`
   re-type requirement, and the mismatch-handling rule.

In-process throughout (no subprocess) — these are static contract
checks. `jsonschema` is a `[dev]` dep declared in `pyproject.toml`
and pinned to a Draft2020-12-capable version (>=4.22).
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path

import jsonschema
import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "trade-ticket.schema.json"
BUNDLE_PATH = REPO_ROOT / "skill-bundles" / "trade-ticket.yaml"
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "trade_tickets"
ENV_EXAMPLE_PATH = REPO_ROOT / ".env.EXAMPLE"

EXPECTED_STATUS_ENUM = ["DRAFT", "REVIEW_READY", "APPROVED", "REJECTED", "EXPIRED"]
EXPECTED_OPERATOR_VERBS = ["new", "review", "APPROVE", "REJECT", "EXPIRE"]
EXPECTED_BOUNDARY_PHRASES = [
    "ticket output only",
    "execution is out of scope",
    "broker submission is out of scope",
]
EXPECTED_CONFIRMED_FIELDS = [
    "confirmed.ticker",
    "confirmed.direction",
    "confirmed.entry",
    "confirmed.stop",
    "confirmed.risk_per_trade_pct",
]


def _load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _load_fixture(name: str) -> dict:
    return yaml.safe_load((FIXTURES_DIR / name).read_text(encoding="utf-8"))


def _load_bundle_instruction() -> str:
    bundle = yaml.safe_load(BUNDLE_PATH.read_text(encoding="utf-8"))
    return bundle.get("instruction", "")


def _validator() -> jsonschema.Draft202012Validator:
    """Build the canonical validator used by every fixture test.

    `format_checker=FORMAT_CHECKER` upgrades `format: date-time` from
    annotation-only to an actual check, so a fixture with
    `created_at: "not-an-iso-date"` is rejected even before the
    explicit `pattern` fires. Defence in depth: schema carries both
    `format` and `pattern`; the validator honours both.
    """
    schema = _load_schema()
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.Draft202012Validator.FORMAT_CHECKER,
    )


def _assert_confirmed_matches_ticket(ticket: dict) -> None:
    """Helper used by the business-invariant test.

    Enforces value equality between approval.confirmed.* and the
    ticket body (candidate.*, plan.*, risk.*). On APPROVED tickets,
    also enforces that the load-bearing fields are non-null /
    non-empty so the schema's APPROVED tightening can't be
    silently regressed in a future edit.
    """
    confirmed = ticket["approval"]["confirmed"]
    candidate = ticket["candidate"]
    plan = ticket["plan"]
    risk = ticket["risk"]

    assert confirmed["ticker"] == candidate["ticker"], (
        f"confirmed.ticker={confirmed['ticker']!r} != "
        f"candidate.ticker={candidate['ticker']!r}"
    )
    assert confirmed["direction"] == candidate["direction"], (
        f"confirmed.direction={confirmed['direction']!r} != "
        f"candidate.direction={candidate['direction']!r}"
    )
    assert confirmed["entry"] == plan["entry"]["value"], (
        f"confirmed.entry={confirmed['entry']!r} != "
        f"plan.entry.value={plan['entry']['value']!r}"
    )
    assert confirmed["stop"] == plan["stop"]["value"], (
        f"confirmed.stop={confirmed['stop']!r} != "
        f"plan.stop.value={plan['stop']['value']!r}"
    )
    assert confirmed["risk_per_trade_pct"] == risk["risk_per_trade_pct"], (
        f"confirmed.risk_per_trade_pct={confirmed['risk_per_trade_pct']!r} != "
        f"risk.risk_per_trade_pct={risk['risk_per_trade_pct']!r}"
    )

    if ticket.get("status") == "APPROVED":
        non_null_fields = {
            "candidate.ticker": candidate["ticker"],
            "candidate.direction": candidate["direction"],
            "plan.entry.value": plan["entry"]["value"],
            "plan.stop.value": plan["stop"]["value"],
            "risk.risk_per_trade_pct": risk["risk_per_trade_pct"],
            "approval.confirmed.ticker": confirmed["ticker"],
            "approval.confirmed.direction": confirmed["direction"],
            "approval.confirmed.entry": confirmed["entry"],
            "approval.confirmed.stop": confirmed["stop"],
            "approval.confirmed.risk_per_trade_pct": confirmed["risk_per_trade_pct"],
        }
        for path, value in non_null_fields.items():
            assert value is not None and value != "", (
                f"APPROVED ticket must have non-null {path}; got {value!r}"
            )


# --- structural ------------------------------------------------------------


def test_schema_is_valid_draft_2020_12():
    schema = _load_schema()
    jsonschema.Draft202012Validator.check_schema(schema)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_status_enum_is_exactly_the_five_values_in_order():
    schema = _load_schema()
    assert schema["properties"]["status"]["enum"] == EXPECTED_STATUS_ENUM


def test_approval_required_is_constant_true():
    schema = _load_schema()
    required_prop = schema["properties"]["approval"]["properties"]["required"]
    assert required_prop.get("const") is True, (
        "approval.required must be {'const': True} at the base schema; "
        f"got {required_prop!r}"
    )


# --- positive fixtures -----------------------------------------------------


def test_initial_draft_fixture_is_valid_and_unapproved():
    validator = _validator()
    ticket = _load_fixture("draft.yaml")
    validator.validate(ticket)
    assert ticket["status"] == "DRAFT"
    assert ticket["approval"]["required"] is True
    assert ticket["approval"]["approved"] is False
    assert "reviewer" not in ticket["approval"]


def test_approved_fixture_is_valid_with_confirmed_block():
    validator = _validator()
    ticket = _load_fixture("approved.yaml")
    validator.validate(ticket)
    assert ticket["status"] == "APPROVED"
    assert ticket["approval"]["approved"] is True
    assert ticket["approval"]["reviewer"]
    datetime.fromisoformat(ticket["approval"]["decided_at"].replace("Z", "+00:00"))
    confirmed = ticket["approval"]["confirmed"]
    for key in ("ticker", "direction", "entry", "stop", "risk_per_trade_pct"):
        assert confirmed.get(key) is not None, f"approval.confirmed.{key} must be non-null"


def test_rejected_fixture_requires_reason():
    validator = _validator()
    ticket = _load_fixture("rejected.yaml")
    validator.validate(ticket)
    assert ticket["status"] == "REJECTED"
    assert ticket["approval"]["approved"] is False
    assert ticket["approval"]["reason"]


def test_expired_fixture_records_decided_at():
    validator = _validator()
    ticket = _load_fixture("expired.yaml")
    validator.validate(ticket)
    assert ticket["status"] == "EXPIRED"
    assert ticket["approval"]["approved"] is False
    datetime.fromisoformat(ticket["approval"]["decided_at"].replace("Z", "+00:00"))


# --- negative fixtures -----------------------------------------------------


@pytest.mark.parametrize(
    "fixture_name",
    [
        "bad_no_approval.yaml",
        "bad_required_false.yaml",
        "bad_approved_with_approved_false.yaml",
        "bad_approved_missing_confirmed.yaml",
        "bad_approved_null_entry_or_risk.yaml",
        "bad_approved_blank_reviewer.yaml",
        "bad_invalid_timestamp.yaml",
        "bad_rejected_no_reason.yaml",
        "bad_expired_no_decided_at.yaml",
        "bad_journal_bridge_invalid_action.yaml",
    ],
)
def test_negative_fixture_fails_schema(fixture_name: str):
    validator = _validator()
    ticket = _load_fixture(fixture_name)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        validator.validate(ticket)


# --- business invariant ----------------------------------------------------


def test_business_invariant_approved_confirmed_matches_ticket_body():
    ticket = _load_fixture("approved.yaml")
    _assert_confirmed_matches_ticket(ticket)


def test_negative_approved_confirmed_mismatch_caught_by_invariant():
    # The mismatch fixture is intentionally schema-valid; the schema
    # cannot express cross-field equality. The invariant helper must.
    validator = _validator()
    ticket = _load_fixture("bad_approved_confirmed_mismatch.yaml")
    validator.validate(ticket)  # schema OK by design
    with pytest.raises(AssertionError):
        _assert_confirmed_matches_ticket(ticket)


# --- journal_bridge (TICKET-010) --------------------------------------------


def test_journal_bridge_valid_fixture_accepts():
    """approved_with_journal_bridge.yaml carries the optional
    `journal_bridge` block and must validate against the schema.
    Sanity-check the three fields the schema requires plus the
    business invariant (confirmed.* equals ticket body).
    """
    validator = _validator()
    ticket = _load_fixture("approved_with_journal_bridge.yaml")
    validator.validate(ticket)
    assert ticket["status"] == "APPROVED"
    assert ticket["journal_bridge"]["target"] == "trader-memory-core"
    assert ticket["journal_bridge"]["action"] in {
        "register_thesis",
        "update_thesis",
        "postmortem",
    }
    _assert_confirmed_matches_ticket(ticket)


def test_env_expansion_yields_absolute_path():
    """`.env.EXAMPLE` declares
    `HERMES_TRADE_TICKET_DIR=${HOME}/trading-research/tickets`. The
    bundle emits the literal; the operator (or a downstream tool)
    expands it. Lock the expansion contract here so a parser regression
    that returns the literal unexpanded is caught.
    """
    raw = None
    for line in ENV_EXAMPLE_PATH.read_text(encoding="utf-8").splitlines():
        if line.startswith("HERMES_TRADE_TICKET_DIR="):
            raw = line.split("=", 1)[1].strip()
            break
    assert raw is not None, ".env.EXAMPLE must declare HERMES_TRADE_TICKET_DIR"
    assert "${HOME}" in raw, (
        f"expected literal ${{HOME}} in raw .env value, got {raw!r}"
    )
    expanded = os.path.expandvars(os.path.expanduser(raw))
    assert os.path.isabs(expanded), expanded
    assert "${HOME}" not in expanded, expanded
    assert "trading-research/tickets" in expanded, expanded


# --- bundle instruction contract -------------------------------------------


def test_bundle_instruction_documents_five_status_values_and_five_operator_verbs():
    text = _load_bundle_instruction()
    for status in EXPECTED_STATUS_ENUM:
        assert status in text, f"bundle instruction missing status value {status!r}"
    for verb in EXPECTED_OPERATOR_VERBS:
        assert verb in text, f"bundle instruction missing operator verb {verb!r}"


def test_bundle_instruction_states_positive_boundary():
    # Case-insensitive match: the bundle naturally capitalises the
    # first letter of a sentence ("Execution is out of scope.") while
    # the boilerplate footer carries the same phrase lowercased
    # ("execution and broker submission are out of scope"). Both
    # forms count as documenting the boundary.
    text_lc = _load_bundle_instruction().lower()
    for phrase in EXPECTED_BOUNDARY_PHRASES:
        assert phrase in text_lc, (
            f"bundle instruction missing positive boundary phrase {phrase!r}"
        )


def test_bundle_instruction_requires_confirmed_fields_on_approve():
    text = _load_bundle_instruction()
    for field in EXPECTED_CONFIRMED_FIELDS:
        assert field in text, (
            f"bundle instruction missing confirmed field marker {field!r}; "
            "the reviewer must be told to re-type ticker / direction / entry / stop / risk_per_trade_pct"
        )


def test_bundle_instruction_documents_confirmed_mismatch_handling():
    text = _load_bundle_instruction()
    # The instruction must explain the demote-on-mismatch path. Look
    # for the marker phrase, the re-emit verb, and the target status
    # all appearing in the same instruction body.
    assert re.search(r"Mismatch handling", text), (
        "bundle instruction missing literal 'Mismatch handling' marker"
    )
    assert "re-emit" in text.lower(), (
        "bundle instruction must say it re-emits the ticket on mismatch"
    )
    assert "REVIEW_READY" in text, (
        "bundle instruction must say it demotes to REVIEW_READY on mismatch"
    )


def test_bundle_instruction_documents_save_path_hint():
    """TICKET-010: the instruction must teach the LLM to append a
    suggested-save-path comment that uses HERMES_TRADE_TICKET_DIR
    and the `.ticket.yaml` basename suffix (matches `.gitignore`).
    """
    text = _load_bundle_instruction()
    for needle in (
        "HERMES_TRADE_TICKET_DIR",
        "Suggested save path",
        "<ticket_id>.ticket.yaml",
    ):
        assert needle in text, (
            f"bundle instruction missing save-path-hint literal {needle!r}"
        )


def test_bundle_instruction_documents_journal_bridge_handoff():
    """TICKET-010: the instruction must document the optional
    `journal_bridge` block and the three accepted actions so the
    LLM can guide operators to a structured trader-memory-core
    handoff without inventing field names.
    """
    text = _load_bundle_instruction()
    for needle in (
        "journal_bridge",
        "trader-memory-core",
        "register_thesis",
        "update_thesis",
        "postmortem",
    ):
        assert needle in text, (
            f"bundle instruction missing journal-bridge literal {needle!r}"
        )


def test_bundle_instruction_states_silent_write_prohibited_in_positive_form():
    """TICKET-010: the instruction must state in *positive* form
    that the bundle emits YAML only and that persistence is
    operator-confirmed. The v0.1.5 positive-boundary discipline
    is preserved — we do not grep for negation phrases like
    "do not write" because the bundle is allowed to phrase
    boundary rules either positively or via the existing
    "ticket output only" boilerplate.
    """
    text_lc = _load_bundle_instruction().lower()
    for needle in ("operator-confirmed", "emits yaml only"):
        assert needle in text_lc, (
            f"bundle instruction missing positive silent-write literal {needle!r}"
        )
