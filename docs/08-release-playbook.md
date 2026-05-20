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
- [ ] Inspect `mcp.json` and ensure no unverified MCP servers are enabled.
- [ ] Confirm `.env` is not committed (`.gitignore` covers it; `.env.EXAMPLE` is the user-facing template and IS shipped via `distribution_owned`).
- [ ] Confirm `distribution.yaml` `distribution_owned` includes `.env.EXAMPLE`, `README.md`, `README.ja.md`, and `CHANGELOG.md` (`tests/test_package_structure.py::test_distribution_manifest_includes_user_docs_and_env_example`).
- [ ] Update `CHANGELOG.md` (move `[Unreleased]` items into the new version, add release date).
- [ ] Update `distribution.yaml` `version` field.

## Tagging

```bash
git status
git add .
git commit -m "v0.1.0: Hermes trading research assistant MVP"
git tag v0.1.0
git push origin main --tags
```

## Post-release verification

```bash
# Fresh test home so the public install path is exercised end-to-end.
export TEST_HOME="$(mktemp -d /tmp/hermes-trading-release-test.XXXXXX)"
export HOME="$TEST_HOME"; export HERMES_HOME="$TEST_HOME/.hermes"
export PATH="$HOME/.local/bin:$PATH"

hermes profile install github.com/tradermonty/hermes-trading-research-agent-work-package \
  --name trading-research-assistant --alias -y
trading-research-assistant config set model    claude-opus-4-7
trading-research-assistant config set provider anthropic
trading-research-assistant chat
trading-research-assistant bundles list

# Cleanup
hermes profile alias trading-research-assistant --remove
hermes profile delete trading-research-assistant -y
rm -rf "$TEST_HOME"
```

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
- MCP config (`mcp.json`) ships empty; examples are in `mcp.example.json` until verified.
- No live brokerage execution.
```
