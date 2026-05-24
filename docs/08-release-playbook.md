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
