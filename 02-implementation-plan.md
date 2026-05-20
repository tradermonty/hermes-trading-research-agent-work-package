# Implementation Plan

## Milestone 1 — Skeleton validation

Tasks:

1. Initialize git repository.
2. Install Python dev dependencies.
3. Run `python scripts/validate_package.py --profile-root .`.
4. Run `pytest -q`.
5. Fix any YAML/JSON/schema issues.

Acceptance:

- Validator passes without `CLAUDE_TRADING_SKILLS_REPO`.
- Validator warns but does not fail when external skills are missing.
- Tests pass.

## Milestone 2 — Hermes install smoke test

Tasks:

1. Create a temporary Hermes home or test user profile.
2. Install this repo using profile distribution install from local git path.
3. Verify alias creation.
4. Start a chat and confirm `SOUL.md` behavior.
5. Run `/trading-research-orchestrator`.

Acceptance:

- Profile installs.
- Profile can chat.
- Built-in adapter skills load.

## Milestone 3 — External skills integration

Tasks:

1. Clone `tradermonty/claude-trading-skills` locally.
2. Set `CLAUDE_TRADING_SKILLS_REPO`.
3. Run validator.
4. Run sync generator in external mode.
5. Verify `bundles list` and individual bundle invocation.

Acceptance:

- Upstream skills are discoverable.
- Missing skills are only Hermes-native adapter skills or are resolved.
- `/pre-market-routine` loads the expected upstream skills.

## Milestone 4 — Cron enablement

Tasks:

1. Set `HERMES_CRON_DELIVER=local`.
2. Run `bash cron/create_cron_jobs.sh`.
3. Run `trading-research-assistant cron list`.
4. Manually trigger pre-market and after-close jobs.
5. Verify output structure.

Acceptance:

- Jobs are created with correct schedules and skill attachments.
- Manual run produces structured brief.
- Missing data produces degraded-mode warnings.

## Milestone 5 — Safety/output QA

Tasks:

1. Add sample prompts and expected output snapshots.
2. Check that direct imperative buy/sell language is absent.
3. Check required sections exist.
4. Check data freshness section exists.
5. Check human next action section exists.

Acceptance:

- Automated tests cover guardrails.
- Manual review signs off on sample reports.

## Milestone 6 — Optional vendored mode

Tasks:

1. Implement copy mode in sync script fully.
2. Add `vendor-manifest.json` generation with source commit if available.
3. Add drift detection.
4. Add tests for vendor path.

Acceptance:

- Profile works without external repo.
- Release notes explain duplication and drift risk.

## Milestone 7 — v0.1.0 release

Tasks:

1. Update README with final install instructions.
2. Update `distribution.yaml` version.
3. Create release tag.
4. Test install from GitHub URL.
5. Add changelog.

Acceptance:

- New user can install and run the three primary commands:
  - `/pre-market-routine`
  - `/after-close-review`
  - `/trade-journal`
