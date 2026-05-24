# Hermes Compatibility Notes

This file is updated by the coding agent against the installed Hermes version.

**Last verified:** Hermes Agent v0.14.0 (2026.5.16) on macOS Darwin 25.2.0.

## Features assumed by this package

- Profile Distributions can package a complete agent profile as a git repository.
- Profiles isolate their own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and gateway state.
- Skills can be loaded as slash commands.
- Hermes can scan external skill directories through `skills.external_dirs`.
- Skill Bundles live under `skill-bundles/` / profile-local equivalent and group several skills into one slash command.
- Cron jobs can attach multiple skills and run scheduled routines.
- Cron jobs run in fresh sessions, so prompts must be self-contained.
- Cron delivery can target local files or messaging platforms.

## Verification status (v0.14.0)

| Item | Status | Notes |
|---|---|---|
| `distribution_owned` accepts `skill-bundles/` | ✓ verified | `hermes profile install` copies `skill-bundles/` into `~/.hermes/profiles/<name>/skill-bundles/` along with other manifest-owned paths. |
| Profile-local bundle path | ✓ verified | `~/.hermes/profiles/<name>/skill-bundles/*.yaml` (or `$HERMES_HOME/profiles/<name>/skill-bundles/`). |
| `config.yaml` environment expansion for `skills.external_dirs` | ✓ verified | In isolated install, `trading-research-test-tmp` resolved 55 upstream skills + 3 profile-local skills via `${CLAUDE_TRADING_SKILLS_REPO}/skills` expansion at skill discovery time. |
| CLI syntax for `cron create --skill` | ✓ verified | `--skill` is repeatable. Positional args: `schedule prompt`. Options: `--name`, `--deliver`, `--repeat`, `--script`, `--workdir`, `--profile`. No `-p` shorthand on `cron create`. |
| CLI syntax for `cron run <job_id>` | ✓ verified | `job_id` is the 12-char hex string from `cron list`, not the human name. `--accept-hooks` skips TTY prompt. |
| CLI for `profile install` | ✓ verified | `hermes profile install <source> [--name <name>] [--alias] [--force] [-y]`. `--alias` is **boolean** (no value). `<source>` accepts local directory; `file://` prefix is **not** required. `-y` skips manifest preview confirmation. |
| CLI for `profile delete` | ✓ verified | `hermes profile delete <name> [-y]`. There is **no** `hermes profile uninstall` in v0.14.0. |
| CLI for `cron delete` | ✓ verified, no `-y` | `hermes cron delete <job_id>`. The `-y`/`--yes` flag is **not** supported on `cron delete` in v0.14.0 (unlike `profile delete`). |
| `bundles reload` CLI syntax | ✓ verified | `hermes bundles reload` takes no arguments. Profile aliases such as `trading-research-assistant bundles reload` scan that profile's `skill-bundles/`; the default profile scanned 0 bundles, while this profile reported `No changes. 9 bundle(s) loaded.` |
| MCP config schema | ✓ verified, keep `mcp.json` empty | In v0.14.0, `hermes mcp add/list/test/configure` read and write `config.yaml` under the `mcp_servers:` key, not this distribution's `mcp.json`. `mcp.json` remains an empty distribution-owned placeholder; do not put unverified servers there. |
| Toolset restrictions for cron | ✓ verified | `cron create` has no `--toolsets` flag. Cron uses per-job `enabled_toolsets` when created/updated by the cronjob tool/API, otherwise the profile's `platform_toolsets.cron` from `hermes tools enable/disable --platform cron ...`. Scheduler still hard-disables `cronjob`, `messaging`, and `clarify` for cron agent runs. |

## Operational findings (v0.14.0 smoke test)

### Cron jobs require the gateway to fire automatically

`cron create` registers jobs as `active`, but they do not run on schedule until the gateway is up. Profile install does not start the gateway. Observed banner:

```
⚠ Gateway is not running — jobs won't fire automatically.
```

Workaround documented in `cron/README.md`:
- managed service: `trading-research-assistant gateway install && trading-research-assistant gateway start`
- foreground: `trading-research-assistant gateway run`
- manual-only: `trading-research-assistant cron pause <job_id>` per job and trigger via `cron run` + `cron tick`.

### `chat -q '/bundle-name'` is not a useful dogfood path

In v0.14.0, `trading-research-assistant chat -Q --yolo -q '/pre-market-routine'` exits 0 but only emits a session_id, not the bundle output. End-to-end dogfood should go through `cron run <job_id> --accept-hooks` followed by `cron tick --accept-hooks`, then inspect `cron/output/<job_id>/<timestamp>.md`. Updated in `docs/07-testing-acceptance-criteria.md` and `cron/README.md`.

### `trader-memory-core` needs `jsonschema` at runtime

Observed in `after-close-review` cron output:

```
trader-memory-core CLI failed because jsonschema is not installed
```

The skill itself ships under `claude-trading-skills` and resolves Python deps at the upstream level — this profile cannot fix it directly. Workarounds for users:

```bash
python3 -m pip install jsonschema
# or, if the skill is run via uv:
uv pip install jsonschema
```

A skill-side fix is to wrap the entry-point with `uv run --with jsonschema`. Tracked as an upstream issue rather than a TICKET in this repo. Listed in `docs/04-skill-integration-strategy.md` degraded-mode notes.



### Threat scanner blocks negative-form cron prompts

`hermes cron create` runs each prompt through a threat scanner. Prompt phrases that combine **conditional + negation + "do not fabricate / hide"** semantics can match the `deception_hide` pattern and be rejected at submission time. Symptoms observed:

```
Failed to create job: Blocked: prompt matches threat pattern 'deception_hide'.
Cron prompts must not contain injection or exfiltration payloads.
```

Workaround applied to `prompts/pre-market-routine.md` and `prompts/after-close-review.md`:

- Rewrote `If required data/API keys are missing, ... do not fabricate data` as positive form (`When data or API keys are unavailable, mark the relevant section as degraded mode and cite the missing input`).
- Removed direct `Do not tell the user to buy or sell` from cron prompts. The hard-constraint lives in `SOUL.md` and is reinforced by the QA harness (`tests/test_output_safety.py`).
- Keep cron prompts neutral and outcome-oriented; let `SOUL.md` carry the prohibitions.

If a future prompt edit triggers `deception_hide` again, rewrite the offending sentence in positive form before tightening the SOUL guardrail.

### `--alias` is HOME-bound, not HERMES_HOME-bound

`hermes profile install --alias` writes a wrapper to `~/.local/bin/<name>` (i.e. `$HOME/.local/bin/<name>`), **not** to `$HERMES_HOME/.local/bin`. For isolated testing, override `HOME` and `PATH` as well as `HERMES_HOME`:

```bash
export TEST_HOME="$(mktemp -d /tmp/hermes-trading-home.XXXXXX)"
export HOME="$TEST_HOME"
export HERMES_HOME="$TEST_HOME/.hermes"
export PATH="$HOME/.local/bin:$PATH"
```

Restore `HOME`/`PATH` from saved originals in cleanup (otherwise subsequent phases run against a deleted HOME).

### `model` / `provider` are root-level config keys

`hermes config set inference.model claude-opus-4-7` does **not** affect the `Model:` field shown by `hermes config show`. The correct keys are `model` and `provider`:

```bash
trading-research-test-tmp config set model    claude-opus-4-7
trading-research-test-tmp config set provider anthropic
trading-research-test-tmp config show           # Model: {'default': ..., 'provider': ...}
```

This applies to both `chat` and `cron` runs. `HERMES_INFERENCE_MODEL` / `HERMES_INFERENCE_PROVIDER` env vars are invocation overrides (one-shot / TUI) and do not appear in `config show`.

### Cron timezone interpretation

`hermes cron create --help` shows **no timezone flag** in v0.14.0. Cron expressions are interpreted in the **host OS local timezone**. The `HERMES_TRADING_TIMEZONE: America/Los_Angeles` value in `config.yaml` is a **report-body label only** consumed by skills — it does not affect scheduler firing times, and the runtime cron script intentionally does **not** read it for the host-TZ check.

Runtime behaviour (`cron/create_cron_jobs.py`, invoked via the `bash cron/create_cron_jobs.sh` wrapper):

- The expected timezone comes from `data/schedule-presets.yaml:timezone` (the YAML is the single source of truth for schedule, name, prompt_file, skills, and timezone).
- On startup the script resolves the host IANA zone: (1) `TZ` env var when set — accept any value `zoneinfo.ZoneInfo` can resolve; (2) otherwise `os.readlink("/etc/localtime")` then fallback to `Path.resolve()`, splitting on `/zoneinfo/` to extract the IANA suffix; (3) otherwise unknown.
- It emits a `WARNING` on stderr in two cases and continues regardless:
  - Host zone resolved but differs from the preset zone — compared **by IANA name**, so `America/Phoenix` is still flagged against `America/Los_Angeles` in summer even though both are UTC-7 (DST rules differ).
  - Host zone could not be verified (e.g. `TZ=Etc/NotAZone`, or `/etc/localtime` is missing) — the message says the host TZ is unknown and names the expected zone.

Deployment guidance:
- Run the host in `America/Los_Angeles` (or whichever timezone matches the cron expressions in `data/schedule-presets.yaml`).
- If running in a different timezone, rewrite the cron expressions in `data/schedule-presets.yaml` for your host. The runtime will pick the new values up automatically.

If a future Hermes release adds a `--tz` flag, update `cron/create_cron_jobs.py` and `cron/README.md` accordingly.


### Bundle reload syntax

`hermes bundles reload` has no positional arguments or options beyond `-h/--help`. It re-scans the active profile's bundle directory and reports added/removed bundles. Verified examples:

```bash
trading-research-assistant bundles reload
# No changes. 9 bundle(s) loaded.

hermes bundles reload
# No changes. 0 bundle(s) loaded.  # default profile has no bundles
```

### MCP config location

The active MCP configuration path in Hermes v0.14.0 is `config.yaml` under `mcp_servers:`, managed by `hermes mcp add/remove/list/test/configure`. A stdio server added with:

```bash
hermes mcp add demo-stdio --command true --args hello world
```

is persisted as:

```yaml
mcp_servers:
  demo-stdio:
    command: "true"
    args:
      - hello
      - world
    enabled: false
```

The `--env KEY=VALUE` option is supported for stdio MCP servers (`--command` or stdio presets), but not HTTP/SSE URL servers. `mcp.json` is distribution-owned by Hermes profile installs/updates, but the v0.14.0 `hermes mcp` CLI did not read it during verification. Keep this package's `mcp.json` empty and use `hermes mcp add ...` or profile `config.yaml` for real server enablement after validating the server package and permissions.

### Cron toolset restrictions

`hermes cron create --help` exposes `--skill`, `--script`, `--no-agent`, `--workdir`, and `--profile`, but no toolset flag. Cron tool restrictions are available through two lower-level paths:

- Per-job `enabled_toolsets`, created/updated by the Hermes cronjob tool/API, has first priority.
- Profile-wide platform settings are stored in `config.yaml` under `platform_toolsets.cron` and can be edited non-interactively with commands such as `hermes tools disable --platform cron browser image_gen tts`.

If neither is configured, the scheduler resolves the default cron platform toolset. In the scheduler, `cronjob`, `messaging`, and `clarify` are still passed as disabled toolsets for cron agent runs, even if they appear enabled in `hermes tools list --platform cron`.

## Known conservative choices

- `mcp.json` is empty by default; active MCP servers should be configured via `hermes mcp add ...` / `config.yaml:mcp_servers` after validation.
- Cron creation is a script (`cron/create_cron_jobs.sh`), not committed active jobs, to keep user consent explicit.
- Default cron delivery is `local`.
- External-linked mode is preferred until vendored mode has drift detection.
