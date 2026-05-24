# Hermes Trading Research Agent

A Hermes Profile Distribution that turns `tradermonty/claude-trading-skills` into an always-on research and process-support assistant for a human US-equity trader.

**This is not an automated trading system.** It is a research, journaling, and risk-review assistant. The human reviewer makes all entry and exit decisions. There is no order placement, no signal service, and no hidden scheduled jobs.

- Target Hermes alias: `trading-research-assistant`
- Hermes version verified: **v0.14.0** (2026.5.16)
- Default schedule timezone: `America/Los_Angeles` (see [Timezone semantics](#timezone-semantics-important))

---

## Quick Start (5 minutes)

```bash
# 1. Clone this repo and the upstream skills repo.
git clone <this-repo-url> hermes-trading-research-agent
git clone https://github.com/tradermonty/claude-trading-skills.git
cd hermes-trading-research-agent

# 2. Tell this profile where the upstream skills live.
export CLAUDE_TRADING_SKILLS_REPO="$(realpath ../claude-trading-skills)"

# 3. Validate skeleton (Phase 1 of the implementation plan).
make validate          # python3 scripts/validate_package.py
make test              # 87 tests pass

# 4. Validate that every referenced skill exists upstream.
python3 scripts/validate_upstream_index.py \
  --source "$CLAUDE_TRADING_SKILLS_REPO" --profile-root .

# 5. Install the profile (or install from GitHub directly).
hermes profile install "$(pwd)" --name trading-research-assistant --alias -y
# Or:
#   hermes profile install github.com/tradermonty/hermes-trading-research-agent-work-package \
#     --name trading-research-assistant --alias -y

# Configure model + provider. Pick whichever your Hermes setup supports:
trading-research-assistant config set model    claude-opus-4-7
trading-research-assistant config set provider anthropic
# Examples for other providers:
#   trading-research-assistant config set provider     openai-codex
#   trading-research-assistant config set model        gpt-5.5
#   trading-research-assistant config set model.base_url https://chatgpt.com/backend-api/codex
# (Dotted keys like `model.default` / `model.provider` also work.)

# 6. Configure API keys (copy and edit).
cp ~/.hermes/profiles/trading-research-assistant/.env.EXAMPLE \
   ~/.hermes/profiles/trading-research-assistant/.env
# (open the .env in your editor and fill in keys)

# 6b. Install runtime Python deps that some skills / scripts import directly.
#     - `trader-memory-core` (upstream) imports `jsonschema`.
#     - `cron/create_cron_jobs.py` imports `pyyaml` to read schedule presets.
python3 -m pip install jsonschema pyyaml
# (or: uv pip install jsonschema pyyaml)

# 7. Use it.
trading-research-assistant chat
# Then in the chat session:
#   /pre-market-routine
#   /after-close-review
#   /trade-journal
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Hermes Agent CLI v0.12.0+ (verified on v0.14.0) | https://hermes-agent.nousresearch.com/ |
| Python 3.11+ | For validators and tests. |
| `tradermonty/claude-trading-skills` repo, cloned locally | External-linked mode references it via `CLAUDE_TRADING_SKILLS_REPO`. |

### API keys

Every key is **optional** at install time (`distribution.yaml` marks them `required: false`). If a key is missing, the relevant skill enters **degraded mode** and the output marks the affected section.

- **Recommended** — without these, several skill outputs are degraded:
  - `FMP_API_KEY` — Financial Modeling Prep. Powers earnings / economics / fundamentals / OHLCV-backed skills.
  - `FINVIZ_API_KEY` — FINVIZ Elite. Powers screener skills.
- **One of these** is needed for the chat / cron LLM calls themselves:
  - `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `OPENROUTER_API_KEY` (matched with `provider` setting above).
- **Optional**:
  - `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` — paper / read-only by default (`ALPACA_PAPER=true`).

---

## Slash command bundles

| Slash command | Default cron | Purpose |
|---|---|---|
| `/pre-market-routine` | Weekdays 06:00 PT | Macro calendar, market regime, earnings movers, breadth, watchlist candidates, risk gate. |
| `/after-close-review` | Weekdays 13:15 PT | What changed, sector rotation, open-trade review, journal prompts, tomorrow prep. |
| `/market-regime-daily` | Manual / on-demand | 15-minute regime check: breadth, uptrend participation, exposure ceiling. |
| `/swing-opportunity-daily` | Manual when risk gate allows | Disciplined swing candidates: thesis, invalidation, position-sizing assumptions. |
| `/earnings-movers-triage` | Event-driven | Classifies gap-up / gap-down earnings names and PEAD candidates. |
| `/portfolio-risk-check` | Manual | Exposure, concentration, portfolio heat, open-thesis validity. |
| `/trade-journal` | Manual | Structures trade notes into journal entries with thesis / invalidation / risk record. |
| `/weekly-portfolio-review` | Saturday 09:00 PT | Long-term holdings, dividends, allocation drift, forced-review triggers. |
| `/monthly-performance-review` | First of month 09:00 PT | Process review, signal postmortem, next-month operating rules. |

Each bundle's instruction enforces that the output include **data freshness**, **source provenance**, **thesis**, **invalidation**, **risk considerations**, and a **human decision gate**. See `tests/test_required_sections.py`.

---

## Enabling scheduled jobs

```bash
export HERMES_PROFILE_CMD=trading-research-assistant
export HERMES_CRON_DELIVER=local   # or telegram / discord / slack / origin
bash cron/create_cron_jobs.sh
trading-research-assistant cron list
```

`data/schedule-presets.yaml` is the **single source of truth** for the four cron jobs (schedule + name + skills + prompt file + expected timezone). The shell script is a thin wrapper around `cron/create_cron_jobs.py`, which reads the YAML, runs each `cron create` invocation in preset order, and **emits a WARNING on stderr** when the host's IANA timezone differs from the preset (IANA-name comparison, not just UTC offset — so e.g. `America/Phoenix` is flagged against `America/Los_Angeles` even when offsets coincide). Pass `--dry-run` to `cron/create_cron_jobs.py` to preview the commands without executing.

Cron jobs register as `active` but **do not fire automatically until the Hermes gateway is running**. After `cron list` shows the four jobs, choose:

```bash
# Managed background service (recommended for prod use):
trading-research-assistant gateway install
trading-research-assistant gateway start

# Manual-only mode (no auto-fire, run each job by hand):
for jid in $(trading-research-assistant cron list | awk '/^  [a-f0-9]{12}/ {print $1}'); do
  trading-research-assistant cron pause "$jid"
done
```

To verify a job end-to-end without waiting for the schedule:

```bash
# `chat -q '/pre-market-routine'` only returns a session_id in v0.14.0,
# so use cron run + cron tick for dogfood instead:
trading-research-assistant cron run <pre_market_job_id> --accept-hooks
trading-research-assistant cron tick --accept-hooks
ls ~/.hermes/profiles/trading-research-assistant/cron/output/<pre_market_job_id>/
```

### Timezone semantics (IMPORTANT)

Hermes v0.14.0 has **no `--tz` flag** on `cron create`. Cron expressions are interpreted in the **host OS local timezone**. The `HERMES_TRADING_TIMEZONE` env var is a report-body label only — it does **not** affect when cron fires.

To run the default schedules at `America/Los_Angeles` local times, either:
- set the host OS timezone to `America/Los_Angeles`, **or**
- recompute each cron expression in `data/schedule-presets.yaml` for your host timezone (the runtime reads it directly; no script edit is needed).

See `cron/README.md` and `docs/03-hermes-compatibility-notes.md`.

---

## Versioning and reproducible installs

Hermes Profile Distribution install (`hermes profile install github.com/<owner>/<repo>`) currently tracks the repository's **default branch**, not a specific tag. GitHub Releases exist for changelog and reference (latest: see https://github.com/tradermonty/hermes-trading-research-agent-work-package/releases), but `github.com/...#<tag>` ref pinning is not (yet) supported by Hermes' installer.

For a reproducible install of a specific release — pinned, no surprise updates — clone locally, check out the tag, and install from the directory:

```bash
git clone https://github.com/tradermonty/hermes-trading-research-agent-work-package.git
cd hermes-trading-research-agent-work-package
git checkout v0.1.2   # or any tag from `git tag -l`
hermes profile install "$(pwd)" --name trading-research-assistant --alias -y
```

When Hermes adds Git-ref pinning to its installer, this section will be replaced with the direct GitHub-ref-pinned form.

## MCP servers

`mcp.json` ships **empty by default** and should stay empty unless a future Hermes release documents it as an active MCP config source. In Hermes v0.14.0, the verified MCP CLI path is `hermes mcp add ...`, which writes profile `config.yaml` under `mcp_servers:`. The example file `mcp.example.json` remains a placeholder/reference file only; package names, command invocations, and permissions all need to be checked against the actual MCP server you intend to run before enabling.

Recommended: leave `mcp.json` empty, add real servers with `hermes mcp add ...` or explicit `config.yaml:mcp_servers`, then use `hermes tools enable/disable --platform cron ...` if you want to narrow cron-visible tool surfaces.

## Repository layout

```text
.
├── AGENTS.md                  Coding-agent work order
├── distribution.yaml          Hermes Profile Distribution manifest
├── SOUL.md                    Persistent personality / operating policy
├── config.yaml                Profile config (external skills path, timezone label)
├── mcp.json                   Safe empty MCP config
├── mcp.example.json           MCP server examples to adapt
├── .env.EXAMPLE               Required / optional keys and toggles
├── skill-bundles/             Hermes bundle YAMLs (9 slash commands)
├── skills/                    Profile-local adapter/orchestrator skills
├── cron/                      Cron enablement scripts and notes
├── prompts/                   Self-contained prompts used by scheduled routines
├── data/                      Skill / workflow mappings and guardrails
├── docs/                      Architecture, implementation, testing, release notes
├── scripts/                   Validators and upstream-sync helpers
├── schemas/                   JSON schemas for outputs and configs
└── tests/                     pytest suite (structure, output safety, required concepts)
```

---

## Non-goals

- No automatic brokerage order placement.
- No promise of profitability.
- No signal-service UX.
- No collection of live account credentials beyond the user-configured paper / read-only Alpaca keys.
- No hidden cron jobs. Every schedule is declared in `data/schedule-presets.yaml` and only created when you explicitly run `cron/create_cron_jobs.sh` (a thin wrapper around `cron/create_cron_jobs.py`).

---

## Most important acceptance criterion

A new user should be able to install the profile, configure `.env`, and run:

```text
/pre-market-routine
```

The assistant produces a structured research brief built from the right Claude Trading Skills — without the user having to know which individual skill to invoke — and every output section ends with a clear human decision gate.

---

## Further reading

- `docs/01-architecture.md` — system layout and responsibility split.
- `docs/03-hermes-compatibility-notes.md` — Hermes v0.14.0 verification results, including the `deception_hide` threat-scanner workaround and timezone semantics.
- `docs/04-skill-integration-strategy.md` — degraded-mode rules and bundle naming.
- `docs/07-testing-acceptance-criteria.md` — what each test layer guarantees.
- `docs/08-release-playbook.md` — pre-release checklist.
- `CHANGELOG.md` — version history.
- `README.ja.md` — 日本語版。
