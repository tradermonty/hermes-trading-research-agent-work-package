# Cron presets

Hermes cron jobs are enabled explicitly by the installer. This directory contains scripts and prompt files for creating the default routines.

## Timezone semantics (IMPORTANT)

Cron expressions below are written assuming `America/Los_Angeles`. Hermes Agent v0.14.0 **does not have a per-job timezone flag** on `cron create`; cron expressions are interpreted in the **host OS local timezone**. The `HERMES_TRADING_TIMEZONE` env var (`config.yaml`) is a **report-body label only**, consumed by skills — it does not affect scheduler firing times.

To run these schedules at the intended local times:

- Run the host in `America/Los_Angeles`, **or**
- Recompute each cron expression to the host's local timezone before enabling.

See `docs/03-hermes-compatibility-notes.md` for verification details.

## Default schedules

| Job | Schedule | Intended local time (America/Los_Angeles) |
|---|---:|---|
| Pre-market routine | `0 6 * * 1-5` | Weekdays 06:00 |
| After-close review | `15 13 * * 1-5` | Weekdays 13:15 |
| Weekly portfolio review | `0 9 * * 6` | Saturday 09:00 |
| Monthly performance review | `0 9 1 * *` | First day of month 09:00 |

## Enable

```bash
export HERMES_PROFILE_CMD=trading-research-assistant
export HERMES_CRON_DELIVER=local   # or telegram / discord / slack / origin
bash cron/create_cron_jobs.sh
```

For isolated smoke testing, override `HERMES_PROFILE_CMD` to a test alias (e.g. `trading-research-test-tmp`) — see `docs/07-testing-acceptance-criteria.md`.

## Verify

```bash
trading-research-assistant cron list
# Pick a job_id from the output (12-char hex), then:
hermes -p trading-research-assistant cron run <job_id>
# Note: cron run requires job_id, not job name.
```

## Notes

- Delivery defaults to `local` for safety.
- Prompts are stored under `prompts/` to avoid fragile shell quoting and to let `tests/test_output_safety.py` lint them.
- Hermes' cron submission runs each prompt through a threat scanner; prompts with conditional+negation+"do not fabricate" semantics can match the `deception_hide` pattern and be rejected. Keep prompts in **positive** form and put hard prohibitions in `SOUL.md` instead. See `docs/03-hermes-compatibility-notes.md`.
- If Hermes CLI syntax changes, update `cron/create_cron_jobs.sh` and `docs/03-hermes-compatibility-notes.md`.
