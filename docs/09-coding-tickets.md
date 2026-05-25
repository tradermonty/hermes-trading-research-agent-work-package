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

### TICKET-004b — Upstream workflows adapter (open, B-2b)

- Read upstream `workflows/*.yaml` when present and adopt it as the
  primary source for the workflows it covers (`market-regime-daily`,
  `swing-opportunity-daily`, `monthly-performance-review`).
- Define how the upstream `steps[]` / `artifacts[]` shape projects
  onto our flat `skills[]` + `required_outputs[]` bundle shape.
- Keep `data/skill-mapping.yaml` as the SoT for the bundles that have
  no upstream workflow (6 of 9 today).
- Add validator checks that catch drift between upstream and the
  generated bundle.

Done when:

- For the three overlap workflows, regenerating from upstream and
  regenerating from `data/skill-mapping.yaml` produce byte-identical
  bundles.
- The other six bundles continue to regenerate from
  `data/skill-mapping.yaml` only.
- A test fails when upstream and the local override disagree on
  fields the bundle exposes.

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
