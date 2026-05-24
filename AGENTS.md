# Work Order for Coding Agents

## Status (as of v0.1.4 — 2026-05-24)

This document was originally written as a pre-v0.1.0 coding handoff. The MVP (v0.1.0), CI / docs polish (v0.1.1), cron timezone single-source refactor (v0.1.2), the `{{TIMEZONE}}` prompt template + verified-Hermes-v0.14.0 docs round (v0.1.3), and the generator-ownership + determinism round (v0.1.4 / TICKET-004a / B-2a) have all shipped. The Phase / Ticket structure below is kept for historical context — it captures the original intent and the canonical source-of-truth ordering. **For current state, this table is authoritative; the Phase bodies below are not.**

| Phase / Ticket | Status | Where it landed |
|---|---|---|
| Phase 0 — Verify Hermes capabilities | ✓ done | `docs/03-hermes-compatibility-notes.md` (verified table + operational findings, Hermes v0.14.0; v0.1.3 added verified entries for `bundles reload`, MCP config location, and cron toolset restrictions) |
| Phase 1 — External-linked skill integration | ✓ done | `config.yaml:skills.external_dirs`, `scripts/validate_upstream_index.py`, `docs/04-skill-integration-strategy.md` |
| Phase 2 — Bundle generation | **partial** (B-2a done, B-2b open) | Canonical index validation (`scripts/validate_upstream_index.py`) + generator ownership (`x-generated:` contract, write-if-changed, `update_external_config` idempotent, `--force-overwrite` escape hatch double-gated by `REQUIRE_SYNC_WRITE=1` + `REQUIRE_FORCE_OVERWRITE=1`) + 7 determinism tests in `tests/test_sync_determinism.py` all shipped as TICKET-004a / B-2a. **Open: TICKET-004b / B-2b** — adopt upstream `workflows/*.yaml` as primary source for the 3 overlap workflows. |
| Phase 3 — Cron presets | ✓ done | `data/schedule-presets.yaml` (single source of truth for schedule / name / skills / prompt_file / timezone), `cron/create_cron_jobs.py` (host-TZ warning + `{{TIMEZONE}}` prompt template expansion from v0.1.3, priority shell env > `.env` > preset YAML > LA), `cron/create_cron_jobs.sh` wrapper, `tests/test_schedule_drift.py`, `tests/test_prompt_template.py`. `cron run` requires a `job_id` rather than a human name in Hermes v0.14.0 — documented in `docs/03-hermes-compatibility-notes.md`. |
| Phase 4 — Safety and policy gates | ✓ done | `SOUL.md`, `tests/test_output_safety.py`, `tests/test_required_sections.py`, `tests/fixtures/sample_outputs/` |
| Phase 5 — Optional vendored mode | **out of scope (deferred)** | TICKET-008 — sync script skeleton exists but vendored-mode operations + `vendor-manifest.json` + drift detection are not implemented. Planned to follow TICKET-004 (B-2). |
| Phase 6 — Release and documentation | ✓ done | v0.1.0 / v0.1.1 / v0.1.2 / v0.1.3 / v0.1.4 published on GitHub Releases. README + README.ja + CHANGELOG ship with each release. |
| TICKET-001..003, 005..007 | ✓ done | See [v0.1.0 changelog](CHANGELOG.md). |
| TICKET-004a (generator ownership + determinism) | ✓ done (shipped in v0.1.4) | See the [0.1.4] section of `CHANGELOG.md`; `docs/09-coding-tickets.md` for the 004a/004b split rationale; `tests/test_sync_determinism.py` for the contract tests. |
| TICKET-004b (upstream workflows adapter) | open | See `docs/04-skill-integration-strategy.md` "Current bundle-composition SoT" subsection and `docs/09-coding-tickets.md`. |
| TICKET-008 (vendored mode) | open | See Phase 5 above. |

Open work items are reflected in `CHANGELOG.md` under `[Unreleased]` once a fix lands; right now `[Unreleased]` is empty (v0.1.4 just shipped). Next planned work — per the review handoff after v0.1.4 — is **D: prod-alias operational soak** (start the Hermes gateway under the prod `trading-research-assistant` alias, observe one real cron firing). After that, **TICKET-004b / B-2b** — adopt upstream `workflows/*.yaml` as primary source — finishes Phase 2.

For a current-state walkthrough, start with `README.md` → `docs/01-architecture.md` → `docs/03-hermes-compatibility-notes.md`. Use this file for the original intent.

---

## Mission

Build a Hermes Profile Distribution named `trading-research-assistant` that packages a disciplined US equity trading research assistant. It must integrate with `tradermonty/claude-trading-skills` and expose opinionated presets so users do not need to decide which individual skill to use.

## Primary source of truth

Use this priority order whenever sources disagree:

1. Current Hermes official docs and CLI behavior.
2. `tradermonty/claude-trading-skills/skills-index.yaml`.
3. `tradermonty/claude-trading-skills/workflows/*.yaml`.
4. This package's `data/skill-mapping.yaml` and docs.
5. README copy and human-facing prose.

Do not invent skill names when the canonical index is available. Missing skills should be reported clearly and skipped only when the workflow can still produce a degraded result.

## Hard constraints

- The product is a research/process assistant, not a signal service.
- Do not add live trading execution as a default capability.
- If Alpaca support is implemented, default to paper mode and read-only portfolio/risk review unless the user explicitly opts into something else.
- Scheduled jobs must be explicit, listable, and disabled until the user intentionally enables them if Hermes distribution behavior does not auto-enable jobs.
- Secrets must live in `.env` or provider-specific secret stores, never in committed config.
- Keep `claude-trading-skills` canonical; this repo should orchestrate, not fork silently.
- Output must include data freshness and source/skill provenance.
- All user-facing trading content must include thesis, invalidation, risk considerations, and a clear human decision gate.

## Implementation phases

### Phase 0 — Verify Hermes capabilities

1. Install or update Hermes in a test environment.
2. Verify the exact CLI syntax for:
   - profile distribution install/update
   - bundles list/show/reload
   - cron create/list/run/pause/resume/remove
   - profile-scoped `.env`, `config.yaml`, and `SOUL.md`
3. Run a minimal local profile from this skeleton.
4. Document any changes required in `docs/03-hermes-compatibility-notes.md`.

Exit criteria:

- `hermes profile install <local git repo> --alias` works in a fresh test home.
- `trading-research-assistant chat` loads `SOUL.md`.
- At least one bundle appears in `bundles list`.

### Phase 1 — External-linked skill integration

1. Use `${CLAUDE_TRADING_SKILLS_REPO}/skills` as `skills.external_dirs` in `config.yaml`.
2. Add validation that the path exists and contains `skills-index.yaml` in the parent repo.
3. Ensure bundle skill names resolve against Hermes skill discovery.
4. Add a clear degraded-mode message when the external repo is missing.

Exit criteria:

- `python scripts/validate_package.py --profile-root .` passes with `CLAUDE_TRADING_SKILLS_REPO` set.
- Missing external skills are reported by bundle name and missing skill name.

### Phase 2 — Bundle generation from canonical workflows

1. Parse `skills-index.yaml`.
2. Parse `workflows/*.yaml` when present.
3. Use `data/skill-mapping.yaml` to generate Hermes `skill-bundles/*.yaml`.
4. Preserve manual bundle edits only if marked with `x-generated: false`; otherwise overwrite generated bundles.

Exit criteria:

- `python scripts/sync_claude_trading_skills.py --source ... --mode external --write` regenerates bundles deterministically.
- Re-running the generator without changes produces no diff.

### Phase 3 — Cron presets

1. Keep cron job enablement user-controlled.
2. Use `cron/create_cron_jobs.sh` to create the default scheduled jobs.
3. Default schedule timezone is America/Los_Angeles.
4. Provide delivery targets via `HERMES_CRON_DELIVER`, defaulting to `local` for safest first run.
5. Use `prompts/*.md` for long cron prompts instead of giant one-line shell strings.

Exit criteria:

- Script can create pre-market and after-close jobs in a clean profile.
- `cron list` shows human-readable names.
- `cron run "Pre-market routine"` produces a structured brief.

### Phase 4 — Safety and policy gates

Implement these checks in prompts, `SOUL.md`, and tests:

- Never output direct imperative buy/sell orders.
- Always state whether the result is research, watchlist, risk posture, or journal output.
- For candidates, require: ticker, setup, thesis, invalidation, risk notes, data freshness, next human action.
- For missing API keys, output degraded-mode behavior and setup steps.
- For brokerage-related skills, paper/read-only is the default.

Exit criteria:

- Tests cover safety phrases and required report sections.
- Manual review of sample outputs passes `docs/07-testing-acceptance-criteria.md`.

### Phase 5 — Optional vendored mode

Implement after external-linked mode is stable.

1. Add `--mode vendor` to copy selected canonical skills into `skills/vendor/` or `skills/`.
2. Preserve upstream source metadata in `vendor-manifest.json`.
3. Do not mutate vendored skills except via an explicit compatibility patch step.
4. Add drift detection against upstream `skills-index.yaml`.

Exit criteria:

- Vendored install works without `CLAUDE_TRADING_SKILLS_REPO`.
- Drift report shows added/removed/changed upstream skills.

### Phase 6 — Release and documentation

1. Update `distribution.yaml` version.
2. Tag release `v0.1.0`.
3. Add install commands to README.
4. Provide a Japanese README section if the public audience includes Japanese traders.
5. Make release notes explicit about API key requirements and non-goals.

Exit criteria:

- Fresh install from GitHub works.
- User can run `/trading-research-orchestrator`, `/pre-market-routine`, `/after-close-review`, and `/trade-journal`.

## Suggested first implementation ticket sequence

1. `TICKET-001`: Make this skeleton a valid git repo and run validator.
2. `TICKET-002`: Verify Hermes profile distribution install/update behavior.
3. `TICKET-003`: Implement external skill discovery validation.
4. `TICKET-004`: Generate bundles from `data/skill-mapping.yaml`.
5. `TICKET-005`: Wire cron creation script and prompts.
6. `TICKET-006`: Add safety/report-format tests.
7. `TICKET-007`: Dogfood with one pre-market and one after-close run.
8. `TICKET-008`: Add optional vendored mode.
9. `TICKET-009`: Publish v0.1.0.

## Pull request requirements

Every PR must include:

- Summary of changed behavior.
- Commands run.
- Any Hermes CLI/version assumptions.
- Whether external-linked mode and/or vendored mode was tested.
- Screenshots or pasted output for at least one bundle invocation if UX changed.
- No secrets in diff.

## Definition of done for MVP

A clean machine can:

1. Install Hermes.
2. Clone `claude-trading-skills`.
3. Install this profile distribution.
4. Set model and optional market-data API keys.
5. Run `/pre-market-routine` manually.
6. Enable cron jobs via `cron/create_cron_jobs.sh`.
7. Receive structured research briefs without knowing individual skill names.
