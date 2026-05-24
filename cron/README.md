# Cron presets

Hermes cron jobs are enabled explicitly by the installer. This directory contains scripts and prompt files for creating the default routines.

## Source of truth

`data/schedule-presets.yaml` defines the four cron jobs: top-level `timezone`, plus a `name` / `schedule` / `prompt_file` / `skills` per preset. The runtime (`cron/create_cron_jobs.py`, invoked via the `bash cron/create_cron_jobs.sh` wrapper) reads everything from that file — schedules and skill lists are no longer duplicated in the shell script.

## Timezone semantics (IMPORTANT)

Cron expressions in `data/schedule-presets.yaml` are written assuming `America/Los_Angeles`. Hermes Agent v0.14.0 **does not have a per-job timezone flag** on `cron create`; cron expressions are interpreted in the **host OS local timezone**. The `HERMES_TRADING_TIMEZONE` env var (`config.yaml`) is a **report-body label only**, consumed by skills — it does not affect scheduler firing times, and the runtime does **not** consult it for the host-TZ check below.

On startup the runtime resolves the host IANA zone (via `TZ` env, then `/etc/localtime`) and compares it to the preset `timezone` **by IANA name**, not by UTC offset alone. So `America/Phoenix` is still flagged against `America/Los_Angeles` in summer even though both are UTC-7 — because the DST rules differ. The check emits a `WARNING` on stderr but continues; it never blocks job creation. PyYAML is required at runtime (`python3 -m pip install pyyaml`).

### Report-label `{{TIMEZONE}}` expansion (separate from scheduler)

Scheduled prompts (`prompts/pre-market-routine.md`, `after-close-review.md`, `weekly-portfolio-review.md`, `monthly-performance-review.md`) contain a `Timezone label for the report: {{TIMEZONE}}.` line. At cron-create time the runtime expands `{{TIMEZONE}}` using this priority — **shell env > `<repo-root>/.env` > `data/schedule-presets.yaml:timezone` > literal `America/Los_Angeles`** — so an operator can re-label reports to e.g. `Asia/Tokyo` without editing the prompt files.

This expansion path is intentionally separate from the scheduler comparison above: `HERMES_TRADING_TIMEZONE` only changes the report label, never when cron fires. Drop the override into the installed-profile `.env` for persistent behavior, or set it in the shell for an ad-hoc run. The runtime uses a Jinja-like `{{TIMEZONE}}` marker (not `${TIMEZONE}`) so the prompt body never carries a `$`-style env reference that could edge-case the Hermes threat scanner.

To run these schedules at the intended local times:

- Run the host in `America/Los_Angeles`, **or**
- Recompute each cron expression in `data/schedule-presets.yaml` to the host's local timezone before enabling.

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

Preview the commands without touching Hermes:

```bash
HERMES_PROFILE_CMD=true python3 cron/create_cron_jobs.py --dry-run
```

## Verify (dogfood without waiting for the schedule)

`chat -q '/pre-market-routine'` exits 0 in v0.14.0 but returns only a `session_id`, so it is **not** sufficient for end-to-end dogfood. Use `cron run` + `cron tick` instead:

```bash
trading-research-assistant cron list
# Pick a job_id (12-char hex) from the output, then:
trading-research-assistant cron run <job_id> --accept-hooks
trading-research-assistant cron tick --accept-hooks
# Inspect the generated brief:
ls ~/.hermes/profiles/trading-research-assistant/cron/output/<job_id>/
```

## Automatic firing requires the gateway

`hermes profile install` registers cron jobs as `active`, but **they do not fire automatically until the gateway is running**. After enabling, you will see:

```
⚠ Gateway is not running — jobs won't fire automatically.
```

Choose one of:

```bash
# A) Run the gateway as a managed background service (recommended for prod use).
trading-research-assistant gateway install
trading-research-assistant gateway start

# B) Run the gateway in the foreground (useful for local testing).
trading-research-assistant gateway run

# C) Manual-only mode — pause every job, run them only via `cron run`.
for jid in $(trading-research-assistant cron list | awk '/^  [a-f0-9]{12}/ {print $1}'); do
  trading-research-assistant cron pause "$jid"
done
```

## Notes

- Delivery defaults to `local` for safety.
- Prompts are stored under `prompts/` to avoid fragile shell quoting and to let `tests/test_output_safety.py` lint them.
- Hermes' cron submission runs each prompt through a threat scanner; prompts with conditional+negation+"do not fabricate" semantics can match the `deception_hide` pattern and be rejected. Keep prompts in **positive** form and put hard prohibitions in `SOUL.md` instead. See `docs/03-hermes-compatibility-notes.md`.
- If Hermes CLI syntax changes, update `cron/create_cron_jobs.py` (the body, not the shell wrapper) and `docs/03-hermes-compatibility-notes.md`.
- Tests in `tests/test_schedule_drift.py` guard the preset-vs-runtime contract: schedule values, skill names, and the host-TZ warning matrix.
