"""B-2b / TICKET-004b drift tests for the 3 overlap workflows.

This module enforces the SoT split documented in docs/04
"Current bundle-composition SoT (as of B-2b)":

- Upstream `workflows/<slug>.yaml` is the canonical intent.
- `data/skill-mapping.yaml` is the Hermes distribution contract.
- These tests are the mechanical guard — no auto-rewrite.

Drift-check scope (v0.1.x):

- `upstream required_skills ⊆ mapping.skills` (mapping may be a superset)
- `upstream optional_skills ⊆ mapping.skills`
- `mapping.canonical_source == "claude-trading-skills-workflow"` for the 3
  overlap slugs (machine-readable SoT marker)
- Every upstream `workflows/*.yaml` file is classified as either
  `UPSTREAM_OVERLAP_SLUGS` (adopted) or `UPSTREAM_IGNORED_WORKFLOW_SLUGS`
  (documented exception). A new upstream file forces an explicit
  decision.

Not drift-checked in v0.1.x (Hermes mapping may refine upstream):

- `display_name` / `title`
- `cadence` (e.g. upstream `daily` → mapping `daily_when_risk_allows`)

Not projected at all in v0.1.x (B-2c candidates):

- `artifacts → required_outputs` (abstraction-level mismatch)
- `steps` / `decision_gate` / `manual_review` / `when_to_run`
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from scripts.sync_claude_trading_skills import (
    UPSTREAM_OVERLAP_SLUGS,
    UPSTREAM_IGNORED_WORKFLOW_SLUGS,
    load_upstream_workflow,
    workflow_mapping,
)

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def upstream_source() -> Path:
    """Resolve the upstream claude-trading-skills repo path.

    B-2b drift tests need the actual upstream yaml on disk. Without
    `CLAUDE_TRADING_SKILLS_REPO`, skip the whole module (matches the
    convention used by `tests/test_upstream_index.py`).
    """
    src = os.environ.get("CLAUDE_TRADING_SKILLS_REPO")
    if not src:
        pytest.skip(
            "CLAUDE_TRADING_SKILLS_REPO not set; B-2b drift tests need the upstream repo"
        )
    return Path(src).expanduser().resolve()


@pytest.mark.parametrize("slug", sorted(UPSTREAM_OVERLAP_SLUGS))
def test_upstream_workflow_file_exists(slug: str, upstream_source: Path):
    """Every entry in `UPSTREAM_OVERLAP_SLUGS` must point at a real
    upstream `workflows/<slug>.yaml`. A missing file means we declared
    an overlap that no longer exists upstream — explicit failure forces
    a decision (rename, drop, or move to the ignore list with a docs
    note)."""
    assert load_upstream_workflow(upstream_source, slug) is not None, (
        f"upstream workflows/{slug}.yaml missing"
    )


@pytest.mark.parametrize("slug", sorted(UPSTREAM_OVERLAP_SLUGS))
def test_upstream_required_skills_subset_of_mapping_skills(
    slug: str, upstream_source: Path
):
    """Hermes mapping may be a superset of upstream — Hermes-side
    composition routinely adds skills (e.g. `exposure-coach` in
    `swing-opportunity-daily`). It must NOT drop a skill that upstream
    declares required."""
    workflow = load_upstream_workflow(upstream_source, slug)
    assert workflow is not None
    mapping_skills = set(workflow_mapping(REPO)[slug]["skills"])
    upstream_required = set(workflow.get("required_skills") or [])
    missing = upstream_required - mapping_skills
    assert not missing, (
        f"{slug}: mapping.skills missing upstream required_skills: {sorted(missing)}"
    )


@pytest.mark.parametrize("slug", sorted(UPSTREAM_OVERLAP_SLUGS))
def test_upstream_optional_skills_present_in_mapping(
    slug: str, upstream_source: Path
):
    """Upstream optional skills must remain visible in mapping. If a
    skill is dropped here, the operator may not realise that an
    optional upstream capability was lost; explicit failure forces a
    docs note."""
    workflow = load_upstream_workflow(upstream_source, slug)
    assert workflow is not None
    mapping_skills = set(workflow_mapping(REPO)[slug]["skills"])
    upstream_optional = set(workflow.get("optional_skills") or [])
    missing = upstream_optional - mapping_skills
    assert not missing, (
        f"{slug}: mapping.skills missing upstream optional_skills: {sorted(missing)}"
    )


@pytest.mark.parametrize("slug", sorted(UPSTREAM_OVERLAP_SLUGS))
def test_upstream_canonical_source_marker_in_mapping(
    slug: str, upstream_source: Path
):
    """The 3 overlap entries must mark upstream as canonical via
    `canonical_source: claude-trading-skills-workflow`. This is the
    machine-readable signal that the entry is reviewed against upstream
    workflow yaml."""
    cs = workflow_mapping(REPO)[slug].get("canonical_source")
    assert cs == "claude-trading-skills-workflow", (
        f"{slug}: canonical_source should be 'claude-trading-skills-workflow' "
        f"(canonical intent marker); got {cs!r}"
    )


def test_upstream_workflow_inventory_is_classified(upstream_source: Path):
    """Enumerate upstream `workflows/*.yaml` from the filesystem.

    Every upstream slug must be in `UPSTREAM_OVERLAP_SLUGS` (adopted as
    a Hermes bundle) or `UPSTREAM_IGNORED_WORKFLOW_SLUGS` (documented
    exception). A new upstream file forces an explicit classification —
    either promote into overlap or add to the ignore list with a docs/04
    note.

    rev3 Low fix: also assert the two sets are disjoint (catches a
    regression where a slug ends up in both classifications). This
    runs inside the upstream-gated test because the rest of the test
    body needs the filesystem; the disjoint check is essentially free
    once we are here.
    """
    overlap_ignored_intersection = (
        UPSTREAM_OVERLAP_SLUGS & UPSTREAM_IGNORED_WORKFLOW_SLUGS
    )
    assert not overlap_ignored_intersection, (
        f"slugs classified as BOTH overlap and ignored: "
        f"{sorted(overlap_ignored_intersection)}. Pick one classification."
    )
    upstream_dir = upstream_source / "workflows"
    upstream_slugs = {p.stem for p in upstream_dir.glob("*.yaml")}
    classified = UPSTREAM_OVERLAP_SLUGS | UPSTREAM_IGNORED_WORKFLOW_SLUGS
    unclassified = upstream_slugs - classified
    assert not unclassified, (
        f"upstream workflow file(s) unclassified: {sorted(unclassified)}. "
        "Promote into UPSTREAM_OVERLAP_SLUGS (adopt as Hermes bundle) "
        "or add to UPSTREAM_IGNORED_WORKFLOW_SLUGS (and document the "
        "reason in docs/04 'Upstream workflow inventory classification')."
    )
