# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `tests/test_sync_determinism.py` (new, 7 tests): locks in the B-2a generator-ownership contract — `x-generated: false` and missing-key bundles are skipped with stderr WARN, `--force-overwrite` is the only way to rewrite them, `x-generated: true` bundles use write-if-changed (no spurious mtime), `update_external_config()` is idempotent, and a real-repo second-run-noop test asserts the shipped tip is byte- and mtime-identical after two consecutive `sync(write=True)` calls (for both `skill-bundles/*.yaml` and `config.yaml`). Real-repo case skips when `CLAUDE_TRADING_SKILLS_REPO` is unset.
- `scripts/sync_claude_trading_skills.py`: `--force-overwrite` CLI flag (escape hatch — reserved for the `sync-external-write-force` make target).
- `Makefile`: `sync-external-write-force` target, double-gated by `REQUIRE_SYNC_WRITE=1` **and** `REQUIRE_FORCE_OVERWRITE=1`; passes `--force-overwrite` and re-runs `tests/test_output_safety.py` + `tests/test_required_sections.py` after writing.

### Changed

- `scripts/sync_claude_trading_skills.py:sync()` no longer overwrites existing `skill-bundles/*.yaml` unconditionally. For each preset, it inspects the on-disk bundle's `x-generated:` key: `false` → SKIP + WARN, missing key → SKIP + WARN (legacy unknown), `true` → write-if-changed (compare rendered bytes; skip the write entirely when identical so mtime is preserved). New mapping entries (file absent) still produce `x-generated: true` files automatically. `--force-overwrite` collapses every branch to "rewrite if content differs".
- `scripts/sync_claude_trading_skills.py:update_external_config()` is now idempotent: short-circuit (no write) when `${CLAUDE_TRADING_SKILLS_REPO}/skills` is already in `skills.external_dirs[]`. Returns `True` only on the rare write path. This closes the `config.yaml`-side hole in the determinism contract.
- `scripts/sync_claude_trading_skills.py:SyncResult` carries counts for `wrote` / `skipped_protected` / `skipped_legacy` / `skipped_unchanged` / `forced`; `main()` prints a one-line summary on `--write`.
- All nine shipped `skill-bundles/*.yaml` are retroactively annotated `x-generated: false` so the generator no longer owns them. They will not be touched by `make sync-external-write` against the shipped tip.
- `Makefile sync-external-write`: behavior change — was "rewrite every bundle", now "skip protected + legacy bundles; only touch new or `x-generated: true` bundles whose rendered content differs". The `REQUIRE_SYNC_WRITE=1` gate stays. Against the shipped tip the target is a no-op (nine SKIP lines, zero rewrites).

### Documentation

- `docs/04-skill-integration-strategy.md`: new "Current bundle-composition SoT" subsection explains that `data/skill-mapping.yaml` is the authoritative source for bundle composition; upstream `workflows/*.yaml` is intentionally not adopted as a primary source yet (shape + coverage mismatch) and tracked as TICKET-004b / B-2b.
- `docs/09-coding-tickets.md`: TICKET-004 split into TICKET-004a (done in this round) and TICKET-004b (upstream workflows adapter, open).
- `AGENTS.md`: Status table Phase 2 entry updated — B-2a done, B-2b open, with file pointers. TICKET-004 row split into 004a (done) and 004b (open).

## [0.1.3] - 2026-05-24

Prompt timezone label envsubst (`{{TIMEZONE}}`) + verified Hermes v0.14.0 docs for `bundles reload`, MCP config location, and cron toolset restriction paths. No scheduler behavior change.

### Added

- `cron/create_cron_jobs.py`: `_resolve_report_timezone()`, `_read_env_file_value()` (stdlib `.env` parser), `_expand_prompt_template()`. At cron-create time, the new `{{TIMEZONE}}` token in scheduled prompts is expanded using priority **shell env `HERMES_TRADING_TIMEZONE` > `<repo-root>/.env` > `data/schedule-presets.yaml:timezone` > literal `America/Los_Angeles`** (with a one-shot fallback WARNING). Reading `.env` directly is required because `bash cron/create_cron_jobs.sh` does not auto-source the profile `.env`.
- `tests/test_prompt_template.py` (new, 11 tests): preset-derived `{{TIMEZONE}}` contract for the four schedule-bound prompts and zero-token assertion for the event-driven ones (`earnings-movers-triage.md`, `trade-journal.md`); subprocess matrix for default / shell-env-override / scheduler-warning-regression / token-leak; in-process unit tests for `.env` override, shell-wins-over-`.env`, monkeypatched `ENV_FILE` honored at call time, and direct `_resolve_report_timezone` unit. Total suite now 118 passing.
- `distribution.yaml:env_requires`: declared `HERMES_TRADING_TIMEZONE` as optional (default `America/Los_Angeles`) with a description spelling out the priority stack and that it is a label-only override (not a scheduler input). `tests/test_package_structure.py` extended to assert the entry exists and `required: false`.

### Changed

- Prompt files: `prompts/pre-market-routine.md` and `prompts/after-close-review.md` swap hard-coded `America/Los_Angeles` for `{{TIMEZONE}}`; `prompts/weekly-portfolio-review.md` and `prompts/monthly-performance-review.md` gain a `Timezone label for the report: {{TIMEZONE}}.` line. Event-driven prompts (`earnings-movers-triage.md`, `trade-journal.md`) intentionally unchanged.
- `cron/create_cron_jobs.py:build_command()` now takes a `report_timezone` argument and expands `{{TIMEZONE}}` in the prompt body before handing it to Hermes. `main()` resolves the report timezone once per invocation.

### Documentation

- `cron/README.md`: new "Report-label `{{TIMEZONE}}` expansion" subsection explaining the override priority and that it is separate from the scheduler comparison.
- `docs/03-hermes-compatibility-notes.md`: extended the `deception_hide` subsection with the `{{TIMEZONE}}` vs `${TIMEZONE}` convention rationale.
- `README.md` / `README.ja.md`: cron-enablement section now mentions the `{{TIMEZONE}}` expansion + override priority + label-only scope.
- `docs/03-hermes-compatibility-notes.md`: verify and document `bundles reload`, active MCP config location (`config.yaml:mcp_servers`), and cron toolset restriction paths (`platform_toolsets.cron` / per-job `enabled_toolsets`).
- `README.md` / `README.ja.md` / `docs/08-release-playbook.md`: remove stale MCP-schema TODO wording and clarify that `mcp.json` remains empty while real MCP servers are configured through `hermes mcp add ...` / `config.yaml:mcp_servers`.

## [0.1.2] - 2026-05-23

Cron timezone polish + post-v0.1.1 doc generalization. No profile-distribution behavior change for callers who keep the default schedule — only when a host is **not** in the preset timezone, the new runtime now emits a stderr WARNING (non-blocking).

### Added

- `cron/create_cron_jobs.py` (new): YAML-driven runtime for cron job creation. Reads `data/schedule-presets.yaml` as the single source of truth (schedule, name, prompt_file, skills, timezone) instead of hard-coding them in the shell script. Supports `--dry-run` to preview Hermes CLI invocations without executing.
- **Host-TZ warning**: the runtime resolves the host IANA timezone (`TZ` env, then `/etc/localtime` via `readlink` / `resolve()` + `/zoneinfo/` split) and compares it to the preset timezone by IANA name. Emits a `WARNING` on stderr — but continues — when the names differ (so `America/Phoenix` is flagged against `America/Los_Angeles` even when offsets coincide), or when the host zone cannot be verified. `HERMES_TRADING_TIMEZONE` is intentionally not consulted: it remains a report-body label per the existing docs.
- `tests/test_schedule_drift.py` (new): pytest suite that locks in the preset shape (4 jobs, required fields, prompt files exist, top-level timezone), the no-hard-code contract for the runtime script, the dry-run ordering, the host-TZ warning matrix (silent / offset-mismatch / same-offset-different-zone / unknown), and the documentation parity check for the "host OS local timezone" caveat.
- `data/schedule-presets.yaml`: added a human-readable `name:` field per preset so it (not the shell script) is the source of the job name passed to Hermes via `--name`.

### Changed

- `cron/create_cron_jobs.sh`: collapsed from ~73 lines of hard-coded schedules + `--skill` flags to a 6-line wrapper that `exec`s the Python entry point. The documented `bash cron/create_cron_jobs.sh` invocation and `HERMES_PROFILE_CMD` / `HERMES_CRON_DELIVER` env var contract are preserved.
- `scripts/validate_package.py:validate_prompts_and_schedules`: now also requires the top-level `timezone:` and a non-empty `name`/`skills` for each preset.
- `cron/README.md` / `docs/03-hermes-compatibility-notes.md` / `README.md` / `README.ja.md`: documented the new source-of-truth model, the IANA-name TZ comparison (vs. offset-only), the runtime WARNING semantics, and the additional `pyyaml` runtime dependency added to the Quick Start install line alongside `jsonschema`. The "rewrite cron expressions for your host timezone" recipe and the no-hidden-cron-jobs non-goal now point at `data/schedule-presets.yaml` instead of the wrapper script.

### Fixed

- `pyproject.toml`: sync `project.version` to `0.1.2` (kept in step with `distribution.yaml:version`, since `pip install -e ".[dev]"` is on the CI install path and a stale package version is otherwise visibly drift-prone).

### Documentation

- `README.md` / `README.ja.md`: generalize the reproducible-install recipe from a hard-coded `git checkout v0.1.0` to `git checkout v0.1.2   # or any tag from \`git tag -l\``, with a link to the GitHub Releases page for the current latest.
- `PACKAGE_MANIFEST.md`: drop the hard-coded "v0.1.0 MVP" framing; describe the repo as the Hermes Profile Distribution with initial MVP at v0.1.0 and current release tracked in GitHub Releases.
- `docs/MISSING_SKILLS.md`: rephrase "The v0.1.0 release resolves..." as "The current release resolves..." so the doc does not need editing on each tag bump.

## [0.1.1] - 2026-05-20

Post-release polish on top of v0.1.0. No profile-distribution behavior changes; this release is CI + docs + validator polish only.

### Added

- `.github/workflows/ci.yml`: GitHub Actions CI that runs `make validate`, `make validate-upstream` (against a checked-out `tradermonty/claude-trading-skills`), and `make test`. Triggers: push to `main`, push of `v*` tags, pull requests (any branch), and manual `workflow_dispatch`. Uses `actions/checkout@v6` and `actions/setup-python@v6` (Node 24 runtime, no deprecation warnings).
- `docs/MISSING_SKILLS.md`: empty template documenting the validator's degraded-mode-acceptance format. Current status notes that no skills are accepted-missing in v0.1.0.

### Fixed

- `pyproject.toml`: explicitly set `[tool.setuptools] packages = []` and `py-modules = []`. Without this, setuptools' automatic flat-layout discovery picks up top-level dirs like `cron/`, `data/`, `skills/`, `schemas/`, `prompts/` and aborts `pip install -e ".[dev]"` with `Multiple top-level packages discovered in a flat-layout`. This broke the new GitHub Actions CI; verified locally via fresh venv (`pip install -e ".[dev]"` succeeds, 87 tests pass).

### Changed

- `PACKAGE_MANIFEST.md`: rewritten as a pointer file — the original "coding-agent handoff scaffolding" framing was stale once the v0.1.0 MVP shipped.
- `README.md` / `README.ja.md`: added a "Versioning and reproducible installs" section explaining that `hermes profile install github.com/...` tracks the default branch (no Git-ref pinning yet), with a clone + `git checkout v0.1.0` + local install recipe for reproducible pinned installs.
- `README.md` / `README.ja.md`: added an "MCP servers" section warning that `mcp.example.json` placeholders (`finviz-mcp-server`, etc.) are unverified.


## [0.1.0] - 2026-05-20

Initial Hermes Profile Distribution MVP. Verified against Hermes Agent v0.14.0, including live-install dogfood (`hermes profile install` from GitHub → `cron run` + `cron tick` with output files generated for pre-market and after-close routines).

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

### Fixed

- `scripts/validate_package.py`: trailing-slash-insensitive check for `distribution_owned`. Hermes' installed copy strips trailing slashes from `skills/` / `skill-bundles/` / `cron/`, so running the validator inside an installed profile no longer emits spurious WARNs.

### Documentation

- README.md / README.ja.md: Quick Start now includes `python3 -m pip install jsonschema` so `trader-memory-core` (upstream skill that imports `jsonschema` directly) runs in full mode rather than degraded; also added provider-switch examples (`openai-codex` with `model.base_url`) and the note that dotted config keys (`model.default`, `model.provider`) work alongside the root-level forms.
- README.md / README.ja.md / cron/README.md / docs/03 / docs/08: cron jobs register as `active` but **do not fire automatically until the Hermes gateway is running**; documented `gateway install && gateway start` (managed) and `cron pause` (manual-only) flows.
- README.md / README.ja.md / docs/07 Test 5 / docs/08: the verified dogfood path is `cron run <job_id> --accept-hooks` followed by `cron tick --accept-hooks`, then inspect `cron/output/<job_id>/<timestamp>.md`. `chat -q '/bundle-name'` in v0.14.0 returns only a session_id and is **not** sufficient for end-to-end verification.
- docs/03-hermes-compatibility-notes.md: captured the above as operational findings; recorded `trader-memory-core` jsonschema dependency.
- docs/04-skill-integration-strategy.md: added `jsonschema` to the degraded-mode trigger table with install hint.
- docs/08 pre-release checklist: explicit step for `hermes profile update` so installed users pick up doc fixes (e.g. corrected repo name) after publish.
- docs/00-executive-brief.ja.md / docs/08-release-playbook.md / docs/10-user-facing-readme-draft.ja.md / PACKAGE_MANIFEST.md: corrected stale GitHub repo name to `hermes-trading-research-agent-work-package`.

### Notes

- Hermes profile install uses `--alias` as a boolean (no value); the wrapper is written to `$HOME/.local/bin/<name>`, not to `$HERMES_HOME`. Isolated testing therefore requires `HOME`, `HERMES_HOME`, and `PATH` to all be temp-redirected; see `docs/03-hermes-compatibility-notes.md`.
- `model` and `provider` are root-level config keys (`hermes config set model claude-opus-4-7`), not `inference.*`.
- TICKET-004 is **only partially implemented** in this release: canonical index validation is shipped (`validate_upstream_index.py`), generator now respects the safety + required-concepts contract, but `x-generated: false` manual-edit protection and the "re-run produces no diff" determinism test remain open for a future release.
- TICKET-008 (vendored mode) is out of scope for v0.1.0.
