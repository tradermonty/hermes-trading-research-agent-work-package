# Release Playbook

## Pre-release checklist

- [ ] Verify Hermes version and update `docs/03-hermes-compatibility-notes.md` (verified table + operational findings).
- [ ] Run `make validate` (= `python3 scripts/validate_package.py --profile-root .`).
- [ ] Run `make test` (= `python3 -m pytest -q`). All 87+ tests must pass.
- [ ] Run `make validate-upstream` (requires `CLAUDE_TRADING_SKILLS_REPO`). Confirm zero unresolved missing skills, or that every miss is documented in `docs/MISSING_SKILLS.md` as degraded-mode accepted.
- [ ] In an isolated temp HOME (see `docs/07-testing-acceptance-criteria.md` Test 1), exercise both `/pre-market-routine` and `/after-close-review` via `cron run <job_id> --accept-hooks` + `cron tick --accept-hooks` (do **not** rely on `chat -q '/bundle'` — in v0.14.0 it only returns a session_id, not the bundle output).
- [ ] Confirm the generated `cron/output/<job_id>/<timestamp>.md` for each contains every required section (risk posture, regime, watchlist, human next actions, data freshness with as-of timestamps) and explicitly marks any missing-API-key section as degraded.
- [ ] If `trader-memory-core` is in scope for the release, confirm the host has `jsonschema` installed (`python3 -m pip install jsonschema` or `uv pip install jsonschema`); without it the skill enters degraded mode. Filed upstream as a feature request for `claude-trading-skills` to either declare the runtime dep or self-bootstrap via `uv run --with jsonschema`.
- [ ] When publishing an updated profile, remind installed users to run `hermes profile update trading-research-assistant -y` — installed copies otherwise keep stale docs (e.g. older repo name in `~/.hermes/profiles/.../docs/08-release-playbook.md`).
- [ ] Decide gateway mode for the release: documented "managed" (`gateway install && gateway start`) for production, or "manual-only" (pause every cron job) for dry-runs.
- [ ] Confirm `cron/create_cron_jobs.sh` runs cleanly with `HERMES_PROFILE_CMD="$TEST_PROFILE_NAME"` and no prompt is rejected by the `deception_hide` threat scanner.
- [ ] Confirm `mcp.json` remains empty; real MCP servers should be added via `hermes mcp add ...` / `config.yaml:mcp_servers` only after server package, command, env, and permissions are verified.
- [ ] Confirm `.env` is not committed (`.gitignore` covers it; `.env.EXAMPLE` is the user-facing template and IS shipped via `distribution_owned`).
- [ ] Confirm `distribution.yaml` `distribution_owned` includes `.env.EXAMPLE`, `README.md`, `README.ja.md`, and `CHANGELOG.md` (`tests/test_package_structure.py::test_distribution_manifest_includes_user_docs_and_env_example`).
- [ ] Update `CHANGELOG.md` (move `[Unreleased]` items into the new version, add release date).
- [ ] Update `distribution.yaml` `version` field.

## Tagging and release

Pre-release commits (CHANGELOG fold, `distribution.yaml:version` bump, etc.) should already be on `main`. Use annotated tags so `git describe` and GitHub Releases show a meaningful message, and push the tag separately from `main` so a tag-only re-push is possible later.

```bash
git status                                      # working tree clean
git log --oneline -5                            # verify HEAD is the release commit

git tag -a v0.1.0 -m "v0.1.0 MVP — see CHANGELOG.md"
git push origin v0.1.0                          # push the tag (not main --tags)

# Minimal:
gh release create v0.1.0 --notes-file CHANGELOG.md
# Or with an explicit title (preferred for readability on the Releases page):
# gh release create v0.1.0 --title "v0.1.0 MVP" --notes-file CHANGELOG.md
```

If you also need to push `main` (e.g. the release commit hasn't been pushed yet):

```bash
git push origin main
```

Avoid `git push origin main --tags` in one shot — it bundles unrelated tag refs and is harder to reason about during release.

## Post-release verification

Acceptance test in an isolated HOME so the public install path is exercised end-to-end without touching the real user environment. **This calls a paid LLM**, so run it deliberately.

### Anthropic-key path (matches the default Quick Start)

```bash
# Preflight: API key must already be exported in the caller env. A fresh
# HOME starts without one, so check before isolating.
: "${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY must be exported before acceptance test}"

# Isolation
TEST_PROFILE_NAME="trading-research-acceptance"
ORIG_HOME="$HOME"; ORIG_PATH="$PATH"
export TEST_HOME="$(mktemp -d /tmp/hermes-trading-release-test.XXXXXX)"
export HOME="$TEST_HOME"; export HERMES_HOME="$TEST_HOME/.hermes"
export PATH="$HOME/.local/bin:$PATH"
trap '
  hermes profile alias "$TEST_PROFILE_NAME" --remove 2>/dev/null || true
  hermes profile delete "$TEST_PROFILE_NAME" -y 2>/dev/null || true
  rm -rf "$TEST_HOME"
  export HOME="$ORIG_HOME"; export PATH="$ORIG_PATH"; unset HERMES_HOME
' EXIT

# Public install path
hermes profile install github.com/tradermonty/hermes-trading-research-agent-work-package \
  --name "$TEST_PROFILE_NAME" --alias -y
"$TEST_PROFILE_NAME" config set model    claude-opus-4-7
"$TEST_PROFILE_NAME" config set provider anthropic
"$TEST_PROFILE_NAME" config show

# Runtime dep for trader-memory-core (upstream skill imports jsonschema directly)
python3 -m pip install jsonschema

# Sanity
"$TEST_PROFILE_NAME" bundles list                  # 9 entries
python3 "$HOME/.hermes/profiles/$TEST_PROFILE_NAME/scripts/validate_package.py" \
  --profile-root "$HOME/.hermes/profiles/$TEST_PROFILE_NAME"

# Cron dogfood
HERMES_PROFILE_CMD="$TEST_PROFILE_NAME" \
  bash "$HOME/.hermes/profiles/$TEST_PROFILE_NAME/cron/create_cron_jobs.sh"
hermes -p "$TEST_PROFILE_NAME" cron list           # 4 jobs, capture job_ids
hermes -p "$TEST_PROFILE_NAME" cron run <pre_market_job_id>  --accept-hooks
hermes -p "$TEST_PROFILE_NAME" cron tick --accept-hooks
ls "$HERMES_HOME/profiles/$TEST_PROFILE_NAME/cron/output/"
```

### OAuth-based providers (openai-codex etc.)

Fresh `HOME`/`HERMES_HOME` starts with **no auth state**, so OAuth-based providers need an explicit login inside the isolated environment:

```bash
hermes login --provider openai-codex   # opens browser, writes auth to $HERMES_HOME
"$TEST_PROFILE_NAME" config set provider     openai-codex
"$TEST_PROFILE_NAME" config set model        gpt-5.5
"$TEST_PROFILE_NAME" config set model.base_url https://chatgpt.com/backend-api/codex
```

For the Anthropic-key path above no `hermes login` is needed — the key is read from the env var on each invocation.

## Operational soak (prod alias, real-time gateway)

The Post-release verification above runs in an isolated temp HOME and triggers cron jobs by hand (`cron run <job_id>`). That validates the install path and the prompt body. It does **not** validate that the Hermes scheduler actually fires a job at its scheduled time, and it does not exercise the production `trading-research-assistant` alias on the real `~/.hermes`.

This section is a separate soak procedure for that. It is **not** part of the per-release pre-flight — run it once per significant gateway / cron change, then re-run any time a real-user incident points back at the scheduler.

Trigger history:

- **v0.1.4** — first soak (B-2a generator-ownership + determinism shipped).
- **v0.1.5** — `/trade-ticket` added but manual-only; cron/gateway surface unchanged, so the procedure did **not** auto-retrigger.
- **v0.1.6** — TICKET-010 (`/trade-ticket` persistence + journal bridge) and TICKET-004b (read-only upstream drift guard) both keep the cron/gateway surface untouched (`sync()` write path is unchanged and no scheduled bundle was modified), so the procedure does **not** auto-retrigger here either. Recommended **once** as a latest-tag soak so the prod-alias profile version matches the published release tag — running this once after each release keeps the prod alias and the latest tag in lockstep, which simplifies incident comparison; future incident reports then reference v0.1.6 as the running version.
- **Next auto-retrigger** — when anything in `cron/` or `scripts/sync_claude_trading_skills.py` write path shifts, or when `data/schedule-presets.yaml` semantics change.

**Cost / time note:** the soak waits for at least one scheduled cron firing in wall-clock time and produces a real LLM-backed brief. Budget at least one trading-day window plus a small per-firing LLM cost.

### 0. Preconditions

- v0.1.4+ profile already installed under the prod alias `trading-research-assistant` against the **real** `~/.hermes` (not the isolated soak HOME used in Post-release verification).
- Provider auth is valid for whatever `<alias> config show` reports. For API-key providers (Anthropic, OpenAI raw, OpenRouter), the matching key is set in the profile `.env`. For OAuth providers (e.g. `openai-codex`), `hermes login --provider <name>` has already been run against the **real** `~/.hermes` so the auth state is on the host.
- `python3 -m pip install jsonschema pyyaml` already run on the host (otherwise `trader-memory-core` degrades and `cron/create_cron_jobs.py` fails to import).
- Host IANA timezone matches the preset (`America/Los_Angeles`). If it does not, the runtime will already have warned during cron creation — recompute the schedules per `cron/README.md` before starting the soak.
- Decide a soak window long enough to cover at least one scheduled job (e.g. an overnight window covering the next weekday `0 6 * * 1-5` pre-market firing).

### 1. Start the gateway

```bash
# Confirm the prod profile is installed and the wrapper is on PATH.
hermes profile list | grep -F "trading-research-assistant"
command -v trading-research-assistant

# Cron jobs should already exist from `bash cron/create_cron_jobs.sh`.
trading-research-assistant cron list   # expect 4 active jobs with Next run timestamps

# Managed gateway (recommended):
trading-research-assistant gateway install
trading-research-assistant gateway start
trading-research-assistant gateway status   # expect "running" / similar
```

If you prefer a foreground run for live tailing, `trading-research-assistant gateway run` works but blocks the terminal.

### 2. Wait for a scheduled firing

The point of the soak is to confirm the scheduler fires **without** `cron run`. Do not trigger anything by hand during the window.

While waiting, occasionally check:

```bash
trading-research-assistant gateway status
trading-research-assistant cron list                  # Next run timestamp should advance after a firing
ls -la ~/.hermes/profiles/trading-research-assistant/cron/output/
```

### 3. Inspect the firing

After the expected wall-clock time, the matching `cron/output/<job_id>/<timestamp>.md` should exist. Confirm:

- File creation time is after the scheduled wall-clock time and matches the expected `America/Los_Angeles` cron expression. Record both timestamps (scheduler fire vs. output file mtime) — LLM execution can add seconds-to-minutes of latency, and tracking the delta over multiple soak runs is more useful than picking a fixed tolerance.
- The brief contains every required section (risk posture, regime, watchlist, human next actions, data freshness with as-of timestamps).
- Missing-API-key sections are explicitly marked as degraded mode rather than fabricated.
- `Timezone label for the report: <timezone>` matches `HERMES_TRADING_TIMEZONE` (or the preset YAML fallback).
- The brief does not contain forbidden execution language (cross-check against `tests/test_output_safety.py` patterns).

### 4. Record the run in the soak log

Append one row per firing to a soak log (kept locally; do **not** commit the soak log to this repo — it can contain account-flavored context). Suggested template:

```text
# Operational soak log — trading-research-assistant

| Soak date | Hermes ver | Profile ver | Job id | Job name | Schedule | Actual fire (UTC) | Actual fire (local) | Deliver | Output file | Required sections OK? | Degraded sections | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-05-26 | v0.14.0 | v0.1.4 | ec09df0e0f94 | Pre-market routine | 0 6 * * 1-5 | 2026-05-26T13:00:12Z | 2026-05-26T06:00:12-07:00 | local | cron/output/ec09df0e0f94/2026-05-26_06-00-12.md | yes | FMP earnings calendar (key absent) | first soak after v0.1.4 |
```

Failure rows (gateway crashed, no firing, threat scanner reject, missing output file, missing required section, regression on `{{TIMEZONE}}` expansion, etc.) are the **valuable** ones — capture them with as much context as possible.

### 5. Decide stop / continue

After the planned window:

```bash
# Stop the gateway for the soak window (optional — leave running for prod use).
trading-research-assistant gateway stop      # or `gateway uninstall` to remove the managed service entirely
```

Do **not** delete the profile after the soak — that is a separate decommission step.

### 6. Promote findings

For every failure row in the soak log:

- If the cause is in this repo, open a ticket and update `docs/03-hermes-compatibility-notes.md` "Operational findings" with a new subsection (mirroring the existing `gateway not running`, `chat -q`, `jsonschema`, `deception_hide`, `--alias is HOME-bound`, `model/provider keys`, `cron timezone interpretation` pattern).
- If the cause is upstream (`claude-trading-skills` or Hermes Agent), file the issue there and link it from `docs/03` so the next reader sees the boundary.
- If the cause is operator setup (timezone mismatch, missing API key), reinforce the relevant Quick Start / `cron/README.md` line.

### 7. Soak-exit checklist

- [ ] At least one scheduled job fired at the expected wall-clock time without `cron run` intervention.
- [ ] The corresponding `cron/output/<job_id>/<timestamp>.md` contains all required sections.
- [ ] Degraded-mode sections (if any) are explicit, not fabricated.
- [ ] The soak log captures the firing (success or failure rows).
- [ ] Any new operational findings are folded into `docs/03-hermes-compatibility-notes.md` and pointed at from the next release CHANGELOG.

## Release notes template

```markdown
# v0.1.0

Initial Hermes Trading Research Assistant profile distribution. Verified against Hermes Agent v0.14.0.

Includes:
- SOUL.md trading research policy (research and process assistant, no order placement).
- Nine slash-command bundles: pre-market, after-close, market regime, swing opportunity, earnings movers triage, portfolio risk check, trade journal, weekly portfolio review, monthly performance review.
- Three profile-local adapter skills: trading-research-orchestrator, trading-cron-brief-writer, trading-risk-gate.
- External-linked integration with tradermonty/claude-trading-skills via `CLAUDE_TRADING_SKILLS_REPO`.
- Cron creation script for the four scheduled routines with host-local-timezone semantics documented.
- Canonical upstream index validator (`scripts/validate_upstream_index.py`) with `--strict` mode for CI.
- pytest suite (87 tests): structure, EN/JA output safety, required concepts per bundle, fixtures.
- Hermes v0.14.0 compatibility notes including `deception_hide` threat-scanner workaround and HOME/HERMES_HOME/PATH isolation guidance.

Known limitations (deferred to a future release):
- External-linked mode is the only supported integration. Vendored mode (TICKET-008) is not shipped.
- `sync_claude_trading_skills.py --write` regenerates bundles from `data/skill-mapping.yaml` + `build_instruction()`; manual `instruction:` edits are preserved only as long as you do not run the writer. Generator hardening, `x-generated: false` protection, and deterministic-output tests remain as TICKET-004 follow-up.
- MCP config ships with `mcp.json` empty. In Hermes v0.14.0, active MCP servers belong in profile `config.yaml:mcp_servers` via `hermes mcp add ...`; `mcp.example.json` is placeholder reference only.
- No live brokerage execution.
```
