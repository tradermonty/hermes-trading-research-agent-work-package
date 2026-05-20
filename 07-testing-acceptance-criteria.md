# Testing and Acceptance Criteria

## Automated tests

Minimum tests (`make test` / `pytest`, 87 tests in v0.1.0):

- Distribution manifest has the expected name and includes `.env.EXAMPLE`, `README.ja.md`, and `CHANGELOG.md` in `distribution_owned` (`tests/test_package_structure.py`).
- All bundles have non-empty skill lists and instructions (`tests/test_package_structure.py`).
- Prompt files referenced by schedules exist and contain the expected sections (`tests/test_package_structure.py`).
- `SOUL.md` contains the non-execution guardrail strings (`tests/test_package_structure.py`).
- No forbidden execution phrases (EN + JA, trading-context-only forms like `利益確定`) appear in SOUL.md, prompts, or bundle instructions (`tests/test_output_safety.py`).
- Every bundle instruction covers data freshness, source provenance, thesis, invalidation, risk, and a human decision gate (`tests/test_required_sections.py`).
- Fixture sanity: `tests/fixtures/sample_outputs/good_example.md` does not trigger forbidden patterns; `bad_example.md` does (`tests/test_required_sections.py`).
- Canonical upstream index validator (`scripts/validate_upstream_index.py`) exits 0 when every referenced skill resolves against `skills-index.yaml`, exit 2 on unresolved missing references. `--strict` mode forces nonzero on any missing reference regardless of `docs/MISSING_SKILLS.md`. Run via `make validate-upstream` (requires `CLAUDE_TRADING_SKILLS_REPO`).

### Out of scope for v0.1.0 (tracked under TICKET-004 follow-up)

- "Generated bundles are deterministic" (re-running `sync_claude_trading_skills.py --write` produces no diff).
- `x-generated: false` manual-edit protection during regeneration.
- `sync-external-write` writing only into bundles without manual-edit markers.

## Manual Hermes smoke tests

### Test 1: Profile install (isolated)

`--alias` writes a wrapper to `$HOME/.local/bin/<name>`, so isolate HOME and PATH to avoid touching the real user environment. See `docs/03-hermes-compatibility-notes.md`.

```bash
TEST_PROFILE_NAME="trading-research-test-tmp"
ORIG_HOME="$HOME"; ORIG_PATH="$PATH"
export TEST_HOME="$(mktemp -d /tmp/hermes-trading-home.XXXXXX)"
export HOME="$TEST_HOME"; export HERMES_HOME="$TEST_HOME/.hermes"
export PATH="$HOME/.local/bin:$PATH"
trap '
  hermes profile alias "$TEST_PROFILE_NAME" --remove 2>/dev/null || true
  hermes profile delete "$TEST_PROFILE_NAME" -y 2>/dev/null || true
  rm -rf "$TEST_HOME"
  export HOME="$ORIG_HOME"; export PATH="$ORIG_PATH"; unset HERMES_HOME
' EXIT

hermes profile install "$(pwd)" --name "$TEST_PROFILE_NAME" --alias -y
"$TEST_PROFILE_NAME" config set model    claude-opus-4-7
"$TEST_PROFILE_NAME" config set provider anthropic
"$TEST_PROFILE_NAME" chat
```

Expected:

- Profile starts.
- Assistant behavior reflects `SOUL.md`.

### Test 2: Bundle discovery

```bash
trading-research-assistant bundles list
trading-research-assistant bundles show pre-market-routine
```

Expected:

- Bundles appear.
- Missing upstream skills are obvious if external repo is not configured.

### Test 3: Manual pre-market run (via cron run, not chat -q)

In v0.14.0 `trading-research-assistant chat -q '/pre-market-routine'` exits 0 but returns only a session_id — not the bundle output. Use the cron path for end-to-end dogfood:

```bash
HERMES_PROFILE_CMD="$TEST_PROFILE_NAME" bash cron/create_cron_jobs.sh
hermes -p "$TEST_PROFILE_NAME" cron list   # capture <pre_market_job_id>
hermes -p "$TEST_PROFILE_NAME" cron run <pre_market_job_id> --accept-hooks
hermes -p "$TEST_PROFILE_NAME" cron tick --accept-hooks
cat "$HERMES_HOME/profiles/$TEST_PROFILE_NAME/cron/output/<pre_market_job_id>/"*.md
```

Expected sections in the generated `.md`:

- Risk posture.
- Macro calendar (may be degraded if `FMP_API_KEY` is unset — must say so).
- Market regime (breadth, uptrend).
- Earnings movers (may be degraded — must say so).
- Watchlist / review queue.
- Human next actions.
- Data freshness with as-of timestamps.

Forbidden:

- Direct buy/sell instruction (caught by `tests/test_output_safety.py` over inputs; reviewer also spot-checks the output).
- Fabricated prices/events — when data is missing the section must enter degraded mode and cite which key/skill is unavailable.

### Test 4: Trade journal run

```text
/trade-journal I entered XYZ long at 100, stop 95, target 115 because of VCP breakout. Risk 0.5%.
```

Expected:

- Structured journal entry.
- Thesis and invalidation captured.
- Review plan created.

### Test 5: Cron creation

```bash
export HERMES_CRON_DELIVER=local
HERMES_PROFILE_CMD="$TEST_PROFILE_NAME" bash cron/create_cron_jobs.sh
hermes -p "$TEST_PROFILE_NAME" cron list
# Pick a job_id (12-char hex) from the output and run manually:
hermes -p "$TEST_PROFILE_NAME" cron run <pre_market_job_id>
hermes -p "$TEST_PROFILE_NAME" cron run <after_close_job_id>
```

Expected:

- Four jobs are listed.
- Manual run produces output files for pre-market and after-close, each containing the required sections (data freshness, thesis, invalidation, risk, human decision gate).

Note: cron prompts in `prompts/` are written in positive form to avoid Hermes' `deception_hide` threat scanner blocking them at submission time. See `docs/03-hermes-compatibility-notes.md`.

## Release acceptance

MVP is done when a new user can install, configure `.env`, run `/pre-market-routine`, run `/after-close-review`, and use `/trade-journal` without knowing the internal skill list.
