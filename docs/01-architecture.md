# Architecture

## System overview

```text
User / Gateway / Cron
        |
        v
Hermes profile: trading-research-assistant
        |
        +-- SOUL.md: persistent policy and persona
        +-- skill-bundles/: task-level slash commands
        +-- skills/: Hermes-native adapter/orchestrator skills
        +-- config.yaml: external skill dirs + env passthrough
        +-- cron/: scheduled routine enablement
        +-- prompts/: long routine prompts
        +-- data/: skill mapping, schedules, guardrails
        |
        v
External canonical skills repo
tradermonty/claude-trading-skills
        |
        +-- skills-index.yaml
        +-- workflows/*.yaml
        +-- skills/*/SKILL.md
```

## Responsibility split

| Component | Responsibility |
|---|---|
| `claude-trading-skills` | Canonical domain skills, scripts, references, workflow manifests |
| This repo | Hermes profile distribution, bundles, cron, orchestration, install UX |
| Hermes | Profile isolation, skill loading, gateways, cron execution, tool/runtime management |
| Human trader | Final decisions, broker execution, compliance, account risk |

## Two integration modes

### External-linked mode

Best for MVP.

- `config.yaml` contains `skills.external_dirs: [${CLAUDE_TRADING_SKILLS_REPO}/skills]`.
- Bundles reference upstream skill names.
- No duplicated skill content.
- Requires local clone of `claude-trading-skills`.

### Vendored mode

Best for broad distribution after MVP.

- `scripts/sync_claude_trading_skills.py --mode vendor` copies selected upstream skills.
- Generate `vendor-manifest.json` with source metadata.
- Add drift detection to keep upstream and vendored skills aligned.

## Workflow invocation

There are three invocation surfaces:

1. Manual slash commands:
   - `/pre-market-routine`
   - `/after-close-review`
   - `/trade-journal`

2. Natural language:
   - User asks vague trading question.
   - `SOUL.md` routes to `trading-research-orchestrator`.
   - Orchestrator selects a bundle or skill path.

3. Scheduled cron:
   - `cron/create_cron_jobs.sh` creates jobs.
   - Each job attaches multiple skills and uses a prompt file.
   - Delivery target is controlled by `HERMES_CRON_DELIVER`.

## Data flow

```text
Market data APIs / public CSVs / user notes / charts
        |
        v
Claude Trading Skills scripts and references
        |
        v
Hermes bundle/orchestrator synthesis
        |
        v
Brief / watchlist / journal / review artifact
        |
        v
Human decision gate
```

## Why not make every routine a single giant skill?

Hermes bundles are a better fit for recurring tasks because they group already-existing skills under a single slash command. This avoids duplicating domain logic and keeps `claude-trading-skills` canonical.

## Why include Hermes-native adapter skills?

The adapter skills define Hermes-specific behavior that does not belong in the canonical trading skills repo:

- Selection/routing across skill families.
- Cron-friendly brief formatting.
- Risk-gate language and non-execution constraints.
- Degraded-mode guidance for missing external repo or API keys.
