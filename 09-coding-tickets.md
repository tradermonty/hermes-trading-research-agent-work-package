# Coding Tickets

## TICKET-001 — Validate skeleton

- Run package validator and tests.
- Fix any local path or YAML problems.
- Output a short report.

Done when:

- `make validate` passes.
- `make test` passes.

## TICKET-002 — Hermes profile distribution smoke test

- Create a local git repo from this package.
- Install via Hermes profile distribution.
- Verify alias and chat.

Done when:

- `trading-research-assistant chat` works.
- `SOUL.md` is active.

## TICKET-003 — External skills validation

- Clone `claude-trading-skills`.
- Set `CLAUDE_TRADING_SKILLS_REPO`.
- Validate bundle skill references.
- Document missing skills if any.

Done when:

- Validator can check upstream skill dirs.

## TICKET-004 — Bundle generator hardening

Split into two follow-up tickets to keep release boundaries clean
once the first half started shipping in v0.1.x.

### TICKET-004a — Generator ownership + determinism (✓ shipped in B-2a)

- Preserve manual bundle edits when `x-generated: false`.
- Treat missing `x-generated` key as legacy-unknown and skip with WARN.
- Write-if-changed for `x-generated: true` bundles (no spurious mtime).
- `update_external_config()` is also idempotent: no-op when the
  `${CLAUDE_TRADING_SKILLS_REPO}/skills` entry is already present.
- `--force-overwrite` escape hatch + `make sync-external-write-force`
  double-gated by `REQUIRE_SYNC_WRITE=1` and `REQUIRE_FORCE_OVERWRITE=1`.
- `tests/test_sync_determinism.py` covers skip / force / write-if-changed
  / new-file / `update_external_config` idempotency / real-repo
  second-run-noop.

Done when:

- Re-run of `make sync-external-write` produces no diff (mtime + content
  invariant) for both `skill-bundles/*.yaml` and `config.yaml`.

### TICKET-004b — Upstream workflows adapter (✓ shipped in B-2b)

(On `main`; folds into the next release alongside TICKET-010. Closes
Phase 2 — Bundle generation. Implementation footprint stays small
because all 3 overlap bundles are `x-generated: false` and the adapter
is a read-only drift guard, not a regenerator.)

Scope (rev3 final, after rev1 → rev3 review iteration):

- 3 overlap slugs (`market-regime-daily` / `swing-opportunity-daily` /
  `monthly-performance-review`) declared in
  `scripts/sync_claude_trading_skills.py:UPSTREAM_OVERLAP_SLUGS`.
  Adopted as canonical-intent upstream; mapping is the
  distribution-contract superset (Hermes adds `ibd-distribution-day-monitor`,
  `ftd-detector`, `exposure-coach`, `trade-hypothesis-ideator`).
- 2 ignored slugs (`core-portfolio-weekly` /  `trade-memory-loop`)
  declared in `UPSTREAM_IGNORED_WORKFLOW_SLUGS` with reasons documented
  in `docs/04` "Upstream workflow inventory classification" table.
  (`core-portfolio-weekly` is renamed to `weekly-portfolio-review` in
  Hermes; `trade-memory-loop` is driven by the operator via
  `trader-memory-core` directly.)
- `sync()` write path **unchanged** — adapter does not regenerate
  bundles. B-2a `x-generated: false` SKIP contract is preserved
  (10 SKIP / 0 rewrite against the shipped tip).

Drift-check scope (machine-enforced):

- `upstream required_skills ⊆ mapping.skills`
- `upstream optional_skills ⊆ mapping.skills`
- `mapping.canonical_source == "claude-trading-skills-workflow"` for
  the 3 overlap slugs (SoT marker)
- Every upstream `workflows/*.yaml` file is in
  `UPSTREAM_OVERLAP_SLUGS ∪ UPSTREAM_IGNORED_WORKFLOW_SLUGS`
  (filesystem enumeration; new upstream files force an explicit
  classification decision)
- `UPSTREAM_OVERLAP_SLUGS ∩ UPSTREAM_IGNORED_WORKFLOW_SLUGS == ∅`
  (rev3 Low fold; catches accidental dual-classification)

Documented but not drift-checked (mapping refinement is allowed):

- `display_name` ↔ `title`
- `cadence` (e.g. upstream `daily` → mapping `daily_when_risk_allows`)

Not projected at all in v0.1.x (B-2c candidates):

- `artifacts → required_outputs` direct 1:1 mapping (abstraction
  mismatch — upstream artifacts are internal pipeline IDs, Hermes
  required_outputs are user-facing items)
- `steps` / `decision_gate` / `manual_review` / `when_to_run` bundle
  instruction projection

Files touched:

- `scripts/sync_claude_trading_skills.py`: +3 public symbols
  (`UPSTREAM_OVERLAP_SLUGS`, `UPSTREAM_IGNORED_WORKFLOW_SLUGS`,
  `load_upstream_workflow()`). No write-path change.
- `tests/test_upstream_workflow_adapter.py` (new): 5 named tests,
  13 parametrize cases. Module-level skip without
  `CLAUDE_TRADING_SKILLS_REPO`.
- `docs/04-skill-integration-strategy.md`: rewrote "Current
  bundle-composition SoT" subsection from "(as of B-2a)" to
  "(as of B-2b)" with SoT split + projection table + drift-check
  table + inventory classification table.
- `Makefile`: `sync-external-write` comment "nine SKIP lines" →
  "ten SKIP lines" (stale since TICKET-010 added `/trade-ticket`).

Done when:

- All 13 drift cases pass under `CLAUDE_TRADING_SKILLS_REPO=...`.
- Without `CLAUDE_TRADING_SKILLS_REPO`, the module skips cleanly
  (suite stays at 162).
- `make sync-external-write` SKIP count stays 10 (no `x-generated`
  flip on any of the 3 overlap bundles).
- `docs/04` carries the SoT split, the projection-vs-drift-check
  table, and the upstream inventory classification table.

## TICKET-005 — Cron UX

- Verify current Hermes cron syntax.
- Update script if needed.
- Test `local` delivery.
- Add Telegram notes if relevant.

Done when:

- Four default jobs are created and listable.

## TICKET-006 — Output QA harness

- Add sample inputs.
- Add expected section checks.
- Add forbidden phrase checks.

Done when:

- `pytest` fails if direct buy/sell language appears in prompts or SOUL.

## TICKET-007 — Release docs

- Add final README.
- Add Japanese README section.
- Add changelog.

Done when:

- A new user can follow README without private context.

## TICKET-008 — Vendored mode

- Copy selected upstream skills.
- Generate `vendor-manifest.json`.
- Add drift detection.

Done when:

- Profile works without external repo.

## TICKET-009 — `/trade-ticket` bundle + Trade Ticket schema (B-3)

(Shipped in v0.1.5 on 2026-05-24; the v0.1.5 release also folded the
audit-field polish — `reviewer.minLength: 1`, ISO-8601 `pattern` on
`created_at` / `decided_at`, validator built with `format_checker`.)

- New `schemas/trade-ticket.schema.json` (JSON Schema draft/2020-12).
  Top-level required: `ticket_id`, `created_at`, `status`,
  `approval`, `candidate`, `plan`, `risk`, `provenance`. Status
  enum exactly `[DRAFT, REVIEW_READY, APPROVED, REJECTED,
  EXPIRED]`. `approval.required` is `{"const": true}` at the base
  level. `allOf` + `if`/`then` enforce per-status approval
  invariants; the APPROVED branch tightens numeric fields
  (`plan.entry.value`, `plan.stop.value`,
  `risk.risk_per_trade_pct`, `approval.confirmed.entry`,
  `approval.confirmed.stop`,
  `approval.confirmed.risk_per_trade_pct`) to non-null.
- New `skill-bundles/trade-ticket.yaml` (`x-generated: false`).
  Five operator verbs (`new` / `review` / `APPROVE` / `REJECT` /
  `EXPIRE`). APPROVE requires the reviewer to re-type
  `confirmed.{ticker,direction,entry,stop,risk_per_trade_pct}`;
  any mismatch demotes the ticket to `REVIEW_READY`. Positive
  boundary statements ("ticket output only", "execution is out of
  scope", "broker submission is out of scope") appear in the
  instruction body. Persistence is operator-owned.
- `data/skill-mapping.yaml`: new `trade-ticket` workflow entry
  (`cadence: manual`, `category: trade-planning`).
- `/swing-opportunity-daily` and `/pre-market-routine` bundles
  gain an escalation pointer requiring `source_bundle` and
  `source_candidate_ref` when forwarding a candidate.
- `tests/test_trade_ticket_schema.py` (20 cases — 3 structural,
  4 positive fixtures, 8 negative fixtures, 1 business-invariant
  positive, 4 boundary / instruction contract) plus 12 fixtures
  under `tests/fixtures/trade_tickets/`.

Done when:

- `schemas/trade-ticket.schema.json` is a valid draft/2020-12
  schema with the exact 5-value status enum and the four
  status-conditional `if`/`then` blocks.
- `tests/test_trade_ticket_schema.py` (20 cases) all pass; the
  `tests/test_required_sections.py` matrix grows to 10 × 6 = 60
  and all pass.
- `make sync-external-write` against the shipped tip prints 10
  `SKIP protected bundle:` lines (the new bundle is owned by
  the operator from day one).
- `make validate-all` is green.

## TICKET-010 — Trade ticket persistence + journal bridge

(On `main`; folds into the next release. Extends TICKET-009 without
crossing the execution boundary or introducing silent disk writes.)

- `.gitignore` adds `tickets/` and `*.ticket.yaml` as a safety net
  for accidental in-repo ticket placement. (`reports/` was already
  ignored, so `reports/trade_tickets/` is implicitly covered.)
- `.env.EXAMPLE` adds `HERMES_TRADE_TICKET_DIR=${HOME}/trading-research/tickets`
  with a comment explaining operator-confirmed expansion.
- `distribution.yaml:env_requires` declares `HERMES_TRADE_TICKET_DIR`
  (optional, default `${HOME}/trading-research/tickets`) in the same
  form as `HERMES_TRADING_TIMEZONE`. `tests/test_package_structure.py::test_distribution_manifest_declares_hermes_trade_ticket_dir`
  locks the declaration.
- `schemas/trade-ticket.schema.json` adds an optional top-level
  `journal_bridge` object: `target: const trader-memory-core`,
  `action: enum [register_thesis, update_thesis, postmortem]`,
  optional `thesis_status: enum [IDEA, ENTRY_READY, ACTIVE, CLOSED]`,
  optional `notes: string minLength 1`. `additionalProperties: false`
  inside `journal_bridge` (typo guard for fields like
  `thesis_statuz`). Top-level `required` unchanged; `$id` remains
  absent.
- `skill-bundles/trade-ticket.yaml` instruction body gains three
  rule blocks: save path hint (`<ticket_id>.ticket.yaml` suffix),
  journal bridge handoff (recommended on APPROVED, never required),
  silent-write prohibition in positive form (`emits YAML only` /
  `operator-confirmed`).
- `tests/test_trade_ticket_schema.py` adds 5 new tests plus 1
  parametrize row: `test_journal_bridge_valid_fixture_accepts`,
  `test_env_expansion_yields_absolute_path`,
  `test_bundle_instruction_documents_save_path_hint`,
  `test_bundle_instruction_documents_journal_bridge_handoff`,
  `test_bundle_instruction_states_silent_write_prohibited_in_positive_form`,
  and `bad_journal_bridge_invalid_action.yaml` appended to
  `test_negative_fixture_fails_schema` (matrix 9 → 10).
- New fixtures
  `tests/fixtures/trade_tickets/approved_with_journal_bridge.yaml`
  (positive) and `bad_journal_bridge_invalid_action.yaml` (negative)
  bring the fixture count from 14 to 16.

Done when:

- `journal_bridge` is optional and rejects unknown fields (typo
  guard); `target` is const `trader-memory-core`; `action` enum
  is exact; the matching positive and negative fixtures load.
- `.env.EXAMPLE` literal `${HOME}/trading-research/tickets`
  expands to an absolute path via `expandvars` + `expanduser`.
- `distribution.yaml:env_requires` declares the env with the
  canonical default; the manifest test passes.
- Bundle instruction carries the save path hint, journal bridge
  handoff, and silent-write positive form; all three contract
  tests pass.
- `make validate-all` is green; total suite 155 → 162.
- `make sync-external-write` SKIP count is still 10 (no
  `x-generated: false` flip on `/trade-ticket`).

Out of scope (deferred):

- Broker execution, auto-submit, paper / live Alpaca.
- LLM-side silent disk write.
- Cross-check between `journal_bridge.action` and `thesis_status`
  (e.g. `postmortem` → `CLOSED`).
- `JOURNALED` 6th status enum value.
- Making `journal_bridge` required on APPROVED (deferred to a
  future v0.2 breaking change).
