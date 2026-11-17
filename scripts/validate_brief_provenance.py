#!/usr/bin/env python3
"""Offline check of the declared provenance table in a research brief.

This checks report consistency, not provider truth or calendar correctness.
Expected observation dates must come from the input's schedule/session calendar.
No credentials, network access, Hermes, or optional MCPs are needed.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

HEADER = (
    "Input / section", "Source / Skill", "Skill revision", "Observation date",
    "Expected observation date", "Status", "Impact / next step",
)
STATUSES = {"fresh", "carried_forward", "stale", "unavailable", "valid_empty", "unknown"}


def _cells(line: str) -> tuple[str, ...]:
    """Split unescaped pipes, preserving extra empty boundary columns."""
    line = line.strip()
    cells: list[str] = []
    start = 0
    for index, char in enumerate(line):
        # GFM tables keep a pipe preceded by a backslash inside the cell,
        # including after consecutive backslashes (cmark-gfm table scanner).
        if char == "|" and (index == 0 or line[index - 1] != "\\"):
            cells.append(line[start:index])
            start = index + 1
    cells.append(line[start:])
    # Markdown permits one optional delimiter at each edge. Removing more
    # would hide empty columns in malformed rows such as `|| value |`.
    if line.startswith("|"):
        cells = cells[1:]
    if start == len(line) and line.endswith("|"):
        cells = cells[:-1]
    return tuple(cell.strip() for cell in cells)


def _date(value: str) -> date | None:
    if value == "unknown":
        return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("expected YYYY-MM-DD or unknown")
    return date.fromisoformat(value)


def validate_brief(text: str) -> list[str]:
    """Return errors in the response's declared table; never validate prompt echo."""
    # Hermes cron artifacts can echo a full prompt before the actual response.
    response = re.split(r"(?m)^## Response\s*$", text)
    text = response[-1]
    lines = text.splitlines()
    headers = [i for i, line in enumerate(lines) if _cells(line) == HEADER]
    if len(headers) != 1:
        return ["expected exactly one Source / Skill provenance table with the required header"]
    start = headers[0]
    if not any(line.strip() == "### Source / Skill provenance" for line in lines[:start]):
        return ["missing ### Source / Skill provenance heading"]
    if start + 1 >= len(lines) or not all(
        re.fullmatch(r":?-{3,}:?", cell) for cell in _cells(lines[start + 1])
    ) or len(_cells(lines[start + 1])) != len(HEADER):
        return ["missing Markdown table separator"]
    errors: list[str] = []
    count = 0
    for line in lines[start + 2:]:
        if not line.strip().startswith("|"):
            break
        count += 1
        cells = _cells(line)
        label = f"row {count}"
        if len(cells) != len(HEADER) or not all(cells):
            errors.append(f"{label}: all seven fields must be nonempty; use unknown explicitly")
            continue
        _, _, _, observation, expected, status, _ = cells
        if status not in STATUSES:
            errors.append(f"{label}: invalid status {status!r}")
            continue
        try:
            observed_date, expected_date = _date(observation), _date(expected)
        except ValueError:
            errors.append(f"{label}: dates must be valid YYYY-MM-DD or unknown")
            continue
        if status in {"fresh", "carried_forward", "valid_empty"}:
            if observed_date is None or expected_date is None or observed_date != expected_date:
                errors.append(f"{label}: {status} requires the expected observation date")
        elif status == "stale":
            if observed_date is None or expected_date is None or observed_date >= expected_date:
                errors.append(f"{label}: stale requires an observation older than expected")
        if observed_date and expected_date and observed_date > expected_date:
            errors.append(f"{label}: observation is later than the expected observation date")
    if not count:
        errors.append("provenance table has no input rows")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_brief(args.brief.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: cannot read brief: {exc}", file=sys.stderr)
        return 1
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if not errors:
        print("PASS: declared provenance table is consistent (source truth not verified)")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
