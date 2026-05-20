# Skill Integration Strategy

## Canonical upstream files

Use these upstream files as the source of truth:

- `skills-index.yaml`: complete skill metadata and workflow membership.
- `workflows/*.yaml`: canonical workflow manifests when present.
- `skills/*/SKILL.md`: actual skill instructions.

## Initial adapter strategy

This repo should not rewrite all trading skills for Hermes. Instead, it adds:

1. Bundles that combine upstream skills.
2. Hermes-native orchestrator skills.
3. Cron prompts and report templates.
4. Validation and sync scripts.

## Mapping rules

- Bundle names should be task-oriented and user-friendly.
- Bundle names should remain stable across releases.
- Skill names must match upstream directory names.
- If upstream workflow manifests exist, prefer their skill order.
- If a missing skill is optional, report degraded mode.
- If a missing skill is essential, fail validation in strict mode.

## Minimal recommended upstream skills for MVP

| Purpose | Skills |
|---|---|
| Navigation | `trading-skills-navigator` |
| Market regime | `market-breadth-analyzer`, `uptrend-analyzer`, `market-top-detector`, `exposure-coach` |
| Macro/calendar | `economic-calendar-fetcher`, `earnings-calendar` |
| Earnings | `earnings-trade-analyzer`, `pead-screener` |
| Candidate planning | `vcp-screener`, `canslim-screener`, `technical-analyst`, `position-sizer`, `breakout-trade-planner` |
| Memory/journal | `trader-memory-core`, `signal-postmortem`, `trade-hypothesis-ideator` |
| Portfolio | `portfolio-manager`, `kanchi-dividend-review-monitor`, `value-dividend-screener` |

## Degraded mode behavior

| Missing component | Behavior |
|---|---|
| `CLAUDE_TRADING_SKILLS_REPO` | Use only Hermes adapter skills; instruct user to set path. |
| `FMP_API_KEY` | Skip FMP-backed fetches; use public/local/manual inputs only. |
| `FINVIZ_API_KEY` | Use Finviz URLs/manual flow rather than API-backed results. |
| Alpaca keys | Skip holdings/portfolio fetch; ask for manual snapshot or CSV. |
| Chart image | Ask user to upload screenshot or skip chart interpretation. |

## Vendoring rules

When implementing vendored mode:

- Copy skills exactly into `skills/vendor/<skill-name>` or `skills/<skill-name>` after deciding which Hermes path resolves best.
- Write `vendor-manifest.json` with upstream repo path, commit SHA if available, selected skills, and timestamp.
- Never silently patch upstream skill files.
- If compatibility patches are needed, store patch files under `patches/` and apply them explicitly.
