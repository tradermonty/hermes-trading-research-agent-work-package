#!/usr/bin/env python3
"""Opt-in real Hermes generation using synthetic input and no executable tools.

Requires an operator-prepared isolated HERMES_HOME with inference configured.
Never uses the caller's normal profile implicitly; outputs contain only the
supplied synthetic case. Offline CI audits the captured real model responses.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def expected_status(item: dict, cutoff: str) -> str:
    if item["fetch"] != "success" or not item["schema_valid"]:
        return "unavailable"
    basis = item["basis"]
    if basis["kind"] == "completed-close":
        observed = item.get("observation_date")
        if not observed or observed > basis["expected_session"]:
            return "unavailable"
        if observed < basis["expected_session"]:
            return "stale"
        return "valid-empty" if item.get("row_count") == 0 else "fresh"
    observed = item.get("observation_timestamp") or item.get("verified_as_of")
    if not observed or not basis.get("policy_source") or "max_age_minutes" not in basis:
        return "unavailable"
    delta = (datetime.fromisoformat(cutoff) - datetime.fromisoformat(observed)).total_seconds()
    if delta < 0:
        return "unavailable"
    if delta > basis["max_age_minutes"] * 60:
        return "stale"
    if basis["kind"] == "event-calendar" and (
        not basis.get("event_domain")
        or not (
            item["coverage_start"] <= basis["requested_start"]
            and item["coverage_end"] >= basis["requested_end"]
        )
    ):
        return "unavailable"
    return "valid-empty" if item.get("row_count") == 0 else "fresh"


def parse_provenance_rows(text: str) -> dict[str, list[str]]:
    rows = {}
    shared = re.search(r"(?im)^Skill revision for all rows:\s*(.+)$", text)
    for line in text.splitlines():
        if "|" not in line:
            continue
        cells = [
            cell.strip().replace("**", "").replace("`", "")
            for cell in line.strip().strip("|").split("|")
        ]
        if len(cells) == 6 and shared:
            cells.insert(2, shared.group(1))
        if len(cells) == 7:
            rows[cells[0]] = cells
    return rows


def audit_response(text: str, case: dict) -> None:
    """Check observed status/date/basis in actual provenance rows, fail closed."""
    rows = parse_provenance_rows(text)
    prose = "\n".join(line for line in text.splitlines() if "|" not in line)
    # Inspect the affected content sections, not status summaries in the footer.
    main_prose = re.split(r"(?im)^#{1,4}[^\n]*data freshness", prose)[0]
    blocks = re.split(r"(?m)^#{1,4} ", main_prose)[1:]
    for item in case["inputs"]:
        label = item["section"]
        assert label in rows, f"Missing provenance row: {label}"
        row = rows[label]
        # Expected outcomes are derived from controlled raw inputs, not
        # hand-written expected brief text and not supplied to the LLM.
        expected = expected_status(item, case["run_cutoff"])
        displayed = row[5].lower()
        if "valid-empty" in displayed and not any(
            word in displayed for word in ("unavailable", "stale")
        ):
            status = "valid-empty"  # Accept explicit "fresh (valid-empty, 0 rows)".
        else:
            status = displayed.split()[0]
        assert status == expected, f"{label}: expected {expected}, got {row[5]}"
        observation = (
            item.get("observation_date")
            or item.get("observation_timestamp")
            or item.get("verified_as_of")
            or "unknown"
        )
        assert observation in row[3], f"{label}: missing observation time {observation}"
        assert item["retrieved_at"] in row[4], f"{label}: missing retrieval time"
        assert item["source"] in row[1], f"{label}: missing source lineage"
        assert item["skill_revision"].split()[0] in row[2], f"{label}: missing skill revision"
        impact = row[6]
        basis = item["basis"]
        assert basis["kind"] in impact.lower(), f"{label}: wrong freshness basis kind"
        if basis["kind"] == "completed-close":
            assert basis["expected_session"] in impact, f"{label}: missing expected session"
        else:
            # One report-wide cutoff can apply to several timestamp inputs.
            assert re.search(r"(?i)run cutoff[ :=]*" + re.escape(case["run_cutoff"]), text), (
                f"{label}: missing declared report cutoff"
            )
            assert str(basis["max_age_minutes"]) in impact, f"{label}: missing age limit"
            assert basis["policy_source"] in impact, f"{label}: missing policy source"
            if basis["kind"] == "event-calendar":
                assert basis["event_domain"] in impact.lower(), (
                    f"{label}: calendar domain missing/wrong"
                )
                for key in ("requested_start", "requested_end"):
                    assert basis[key] in impact, f"{label}: missing event window"
        if item["fetch"] != "success":
            assert "auth" in impact.lower(), f"{label}: failure reason missing"
        # Affect-specific status disclosure may live under the normal report
        # headings; exact fixture labels need not become product headings.
        if expected in ("stale", "unavailable", "valid-empty"):
            anchor = (
                "screen " + item["source"].rsplit("screen ", 1)[1]
                if "screen " in item["source"]
                else item["source"].split(" / ")[0]
            )
            relevant = [
                block
                for block in blocks
                if anchor.lower() in block.lower() or label.lower() in block.lower()
            ]
            assert relevant, f"{label}: missing inline disclosure"
            explicit_status = any(expected in block.lower() for block in relevant)
            unavailable_context = (
                expected == "unavailable"
                and item["fetch"] != "success"
                and any("degraded" in block.lower() for block in relevant)
                and any(
                    "auth" in block.lower() and "no observation" in block.lower()
                    for block in relevant
                )
            )
            assert explicit_status or unavailable_context, f"{label}: wrong inline status"
            if expected == "stale":
                assert any(observation in block for block in relevant), (
                    f"{label}: inline date missing"
                )
            if item["fetch"] != "success":
                assert any("auth" in block.lower() for block in relevant), (
                    f"{label}: inline failure reason missing"
                )
    audit_calendar_scope(text, case)
    audit_unobserved_outcomes(text, case)
    assert "Source / Skill provenance" in text
    assert "degraded" in text.lower()
    assert "human" in text.lower()


def audit_calendar_scope(text: str, case: dict) -> None:
    prose = "\n".join(line for line in text.splitlines() if "|" not in line)
    main_prose = re.split(r"(?im)^#{1,4}[^\n]*data freshness", prose)[0]
    blocks = re.split(r"(?m)^#{1,4} ", main_prose)[1:]
    if case.get("workflow") == "pre-market-routine" and not any(
        item["basis"].get("event_domain") == "economic"
        and expected_status(item, case["run_cutoff"]) in ("fresh", "valid-empty")
        for item in case["inputs"]
    ):
        macro = [block for block in blocks if "macro calendar" in block.splitlines()[0].lower()]
        assert macro, "Missing economic-calendar availability disclosure"
        economic = "\n".join(macro).lower()
        assert "economic" in economic and re.search(r"\b(unknown|unavailable)\b", economic), (
            "Missing economic-calendar availability disclosure"
        )
        for line in economic.splitlines():
            if re.search(
                r"no scheduled high-impact events|high-impact events today:\s*(none|no events)",
                line,
            ):
                assert re.search(
                    r"never as|do not (claim|infer|assume)|must not (claim|infer|assume)", line
                ), "Earnings coverage cannot establish absence of economic events"


def audit_unobserved_outcomes(text: str, case: dict) -> None:
    # These controlled cases provide no reaction series or signal comparisons.
    # Missing records cannot establish a zero-count/change outcome.
    if case.get("workflow") != "after-close-review":
        return
    pattern = r"no earnings reactions occurred|no signals improved|no signals degraded|nothing is invalidated"
    for line in text.splitlines():
        if re.search(pattern, line, re.IGNORECASE) and not re.search(
            r"unknown|not assessable|cannot|do not (assume|claim|infer)|must not (assume|claim|infer)|must not be (read|interpreted|treated) as",
            line,
            re.IGNORECASE,
        ):
            raise AssertionError(
                "Missing observations cannot prove zero reactions or signal changes"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-home", required=True, type=Path)
    parser.add_argument("--hermes-source", required=True, type=Path)
    parser.add_argument("--hermes-python", required=True, type=Path)
    parser.add_argument(
        "--workflow", choices=["pre-market-routine", "after-close-review"], required=True
    )
    parser.add_argument("--surface", choices=["bundle", "cron"], required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    runtime = args.runtime_home.resolve()
    default_home = (Path.home() / ".hermes").resolve()
    if (
        runtime == default_home
        or default_home in runtime.parents
        or not (runtime / "config.yaml").is_file()
    ):
        parser.error("Provide a prepared isolated runtime home, not the default profile")
    case = json.loads(
        (ROOT / "tests/fixtures/input_provenance" / f"{args.workflow}__inputs.json").read_text()
    )
    request = (
        "Controlled synthetic acceptance run. Use only the supplied observations; "
        "no tools, browsing, fetching, file changes, or execution. The supplied run cutoff "
        "and market calendar override the real clock for this simulation. Produce the "
        "complete research brief. All other inputs are unavailable. In the final provenance "
        "table use the exact supplied section names, source strings, revision SHA, and full "
        "ISO observation/retrieval timestamps (unknown for absent dates); place Freshness "
        "basis and impact in the last column. Include an inline status for each affected "
        "section using a heading '### <exact section name>' and a 'Status: <status>' line. "
        "For each Impact cell include the basis.kind literally; completed-close includes "
        "expected_session, other bases include the full run cutoff, max age in minutes, "
        "and policy source; event-calendar also includes the event domain and requested coverage window. "
        "For Macro calendar, report economic-calendar availability separately from earnings-calendar availability. "
        "Explain failures and degraded consequences. State synthetic data and that supplied upstream skills were not executed.\n"
        + json.dumps(case, indent=2)
    )
    env = dict(os.environ, HERMES_HOME=str(runtime), HERMES_INFERENCE_MAX_RETRIES="0")
    entrypoint = [
        str(args.hermes_python),
        "-c",
        "import sys; sys.path.insert(0, sys.argv.pop(1)); from hermes_cli.main import main; main()",
        str(args.hermes_source),
    ]
    # Verify the inspected runtime really resolves the requested set to zero tools.
    no_tools = subprocess.run(
        [
            str(args.hermes_python),
            "-c",
            "import sys; sys.path.insert(0, sys.argv[1]); "
            "from model_tools import get_tool_definitions; "
            "assert not get_tool_definitions(enabled_toolsets=['acceptance-no-tools'], quiet_mode=True)",
            str(args.hermes_source),
        ],
        env=env,
        cwd=runtime,
        capture_output=True,
        text=True,
    )
    if no_tools.returncode:
        raise SystemExit("Cannot verify tools are disabled; aborting acceptance run")
    if args.surface == "bundle":
        bundle = Path("skill-bundles") / (args.workflow + ".yaml")
        if (runtime / bundle).read_bytes() != (ROOT / bundle).read_bytes():
            raise SystemExit("Runtime bundle differs from checkout; refresh the isolated copy")
        # Use the same installed Hermes builder as interactive slash commands.
        # CLI chat -q itself does not dispatch slash commands in v0.17.0.
        code = (
            "import sys; sys.path.insert(0, sys.argv[1]); "
            "from agent.skill_bundles import build_bundle_invocation_message; "
            "r=build_bundle_invocation_message(sys.argv[2], sys.stdin.read()); "
            'assert r is not None, "bundle did not load"; print(r[0])'
        )
        built = subprocess.run(
            [str(args.hermes_python), "-c", code, str(args.hermes_source), "/" + args.workflow],
            input=request,
            text=True,
            capture_output=True,
            env=env,
            cwd=runtime,
            check=True,
        )
        # The CLI builder places loaded skills after the user text; repeat the
        # fixture request last so long upstream guidance does not obscure it.
        query = built.stdout + "\n\n" + request
    else:
        query = (
            (ROOT / "prompts" / f"{args.workflow}.md")
            .read_text()
            .replace("{{TIMEZONE}}", "America/Los_Angeles")
            + "\n\n"
            + request
        )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = args.workflow + "__" + args.surface
    (args.output_dir / (stem + ".query.txt")).write_text(query)
    # An unknown toolset resolves to zero tools in the inspected Hermes version.
    try:
        result = subprocess.run(
            [
                *entrypoint,
                "chat",
                "--quiet",
                "--toolsets",
                "acceptance-no-tools",
                "--max-turns",
                "1",
                "--query",
                query,
            ],
            env=env,
            cwd=runtime,
            text=True,
            capture_output=True,
            timeout=args.timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit("Hermes generation timed out; no successful acceptance result recorded")
    if result.returncode:
        raise SystemExit(
            f"Hermes failed with exit {result.returncode}; inspect the isolated runtime logs locally"
        )
    response = result.stdout
    (args.output_dir / (stem + ".md")).write_text(response)
    metadata = {
        "hermes_version": subprocess.run(
            entrypoint + ["--version"],
            env=env,
            cwd=runtime,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()[0],
        "workflow": args.workflow,
        "surface": args.surface,
        "generated_at": datetime.now().astimezone().isoformat(),
        "query_sha256": hashlib.sha256(query.encode()).hexdigest(),
        "response_sha256": hashlib.sha256(response.encode()).hexdigest(),
        "source_sha256": {
            relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            for relative in [
                f"tests/fixtures/input_provenance/{args.workflow}__inputs.json",
                f"prompts/{args.workflow}.md"
                if args.surface == "cron"
                else f"skill-bundles/{args.workflow}.yaml",
            ]
        },
    }
    (args.output_dir / (stem + ".metadata.json")).write_text(json.dumps(metadata, indent=2) + "\n")
    # stderr is deliberately not persisted: backend diagnostics can carry URLs.
    audit_response(response, case)
    print(f"PASS: {stem}; response: {args.output_dir / (stem + '.md')}")


if __name__ == "__main__":
    main()
