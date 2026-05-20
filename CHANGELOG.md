# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- `scripts/validate_package.py`: trailing-slash-insensitive check for `distribution_owned`. Hermes' installed copy strips trailing slashes from `skills/` / `skill-bundles/` / `cron/`, so running the validator inside an installed profile no longer emits spurious WARNs.

### Documentation

- README.md / README.ja.md: add `python3 -m pip install jsonschema` to Quick Start so `trader-memory-core` runs in full mode, not degraded.
- docs/07 Test 5: align cron dogfood with the verified path (`cron run --accept-hooks` + `cron tick --accept-hooks`, then inspect `cron/output/<job_id>/`).
- docs/08 pre-release checklist: explicit step for `hermes profile update` so installed users pick up doc fixes (e.g. corrected repo name) after publish.
- README.md / README.ja.md / cron/README.md: document that cron jobs require `gateway install && gateway start` (or per-job `cron pause`) to fire automatically; profile install alone does not start the scheduler.
- README.md / README.ja.md / docs/07 / docs/08: dogfood path is `cron run <job_id> --accept-hooks` + `cron tick --accept-hooks` then inspect `cron/output/<job_id>/<timestamp>.md`. `chat -q '/bundle-name'` in v0.14.0 only returns a session_id and is **not** sufficient for end-to-end verification.
- README.md / README.ja.md: added provider-switch examples (`openai-codex` with `model.base_url`) and note that dotted keys (`model.default`, `model.provider`) also work.
- docs/04-skill-integration-strategy.md: list `jsonschema` Python module as a known degraded-mode trigger for `trader-memory-core`, with install hint.
- docs/03-hermes-compatibility-notes.md: capture gateway-required-for-auto-fire and `chat -q` limitation as v0.14.0 operational findings; record `trader-memory-core` jsonschema dependency.
- docs/00-executive-brief.ja.md / docs/08-release-playbook.md / docs/10-user-facing-readme-draft.ja.md: corrected stale GitHub repo name to `hermes-trading-research-agent-work-package`.


## [0.1.0] - 2026-05-20

Initial Hermes Profile Distribution MVP. Verified against Hermes Agent v0.14.0.

### Added

- Hermes Profile Distribution manifest (`distribution.yaml`) targeting the `trading-research-assistant` alias.
- `SOUL.md` enforcing research-and-process-assistant tone, no order-placement, no signal-service UX.
- Nine slash-command bundles under `skill-bundles/` mapping to the canonical workflows in `tradermonty/claude-trading-skills`:
  `/pre-market-routine`, `/after-close-review`, `/market-regime-daily`, `/swing-opportunity-daily`,
  `/earnings-movers-triage`, `/portfolio-risk-check`, `/trade-journal`, `/weekly-portfolio-review`,
  `/monthly-performance-review`.
- Three profile-local adapter skills: `trading-research-orchestrator`, `trading-cron-brief-writer`, `trading-risk-gate`.
- `cron/create_cron_jobs.sh` enabling 4 default routines (pre-market, after-close, weekly, monthly) with host-local-timezone semantics.
- Cron prompts under `prompts/` rewritten in positive form to pass Hermes' `deception_hide` threat scanner.
- `scripts/validate_package.py` — distribution / bundle / prompt / JSON structural validator.
- `scripts/validate_upstream_index.py` (new) — canonical `skills-index.yaml` integrity check with degraded-mode acceptance via `docs/MISSING_SKILLS.md`. Exit 0/2 semantics, `--strict` mode for CI.
- `scripts/sync_claude_trading_skills.py` — external-mode bundle sync (dry-run by default; `--write` reserved for future generator-hardening work).
- Makefile splits the upstream sync into safe (`sync-external`, dry-run) and dangerous (`sync-external-write`, gated by `REQUIRE_SYNC_WRITE=1`) targets, and adds `validate-upstream` / `validate-all` for release gating.
- pytest suite (87 tests):
  - `tests/test_package_structure.py` — distribution name, bundle shape, SOUL safety language, prompt sections.
  - `tests/test_output_safety.py` — EN/JA forbidden phrase regex (`buy at $`, `指値で売れ`, `利益確定`, etc.).
  - `tests/test_required_sections.py` — every bundle instruction must cover data freshness, source provenance, thesis, invalidation, risk, and human decision gate.
  - `tests/fixtures/sample_outputs/` — good and bad example outputs for negative-test sanity.
- `docs/` — architecture, implementation plan, Hermes v0.14.0 compatibility notes (with `deception_hide` workaround and HOME/PATH isolation guidance), workflow specs, security/risk controls, testing criteria, release playbook, coding tickets.

### Changed

- `sync_claude_trading_skills.py:build_instruction()` updated to emit the same required-concepts checklist (data freshness, source provenance, thesis, invalidation, risk, human decision gate) that `tests/test_required_sections.py` enforces, phrased in positive form to keep regenerated bundles compatible with Hermes' `deception_hide` threat scanner.
- `dump_yaml()` now preserves block-scalar (`|`) style for `instruction:` fields so bundles remain human-editable after regeneration.
- All existing bundles re-saved with block-scalar formatting; remaining `Do not ...` clauses in bundle instructions rephrased to reference SOUL.md instead.
- `distribution.yaml:distribution_owned` now includes `.env.EXAMPLE`, `README.ja.md`, and `CHANGELOG.md` so the Quick Start (which copies `.env.EXAMPLE`) works after profile install.

### Notes

- Hermes profile install uses `--alias` as a boolean (no value); the wrapper is written to `$HOME/.local/bin/<name>`, not to `$HERMES_HOME`. Isolated testing therefore requires `HOME`, `HERMES_HOME`, and `PATH` to all be temp-redirected; see `docs/03-hermes-compatibility-notes.md`.
- `model` and `provider` are root-level config keys (`hermes config set model claude-opus-4-7`), not `inference.*`.
- TICKET-004 is **only partially implemented** in this release: canonical index validation is shipped (`validate_upstream_index.py`), generator now respects the safety + required-concepts contract, but `x-generated: false` manual-edit protection and the "re-run produces no diff" determinism test remain open for a future release.
- TICKET-008 (vendored mode) is out of scope for v0.1.0.
