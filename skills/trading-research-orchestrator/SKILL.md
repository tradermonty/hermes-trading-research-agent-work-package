---
name: trading-research-orchestrator
description: "Front-door skill for selecting and coordinating Claude Trading Skills inside Hermes for market research, earnings triage, risk review, and journaling."
version: 0.1.0
required_environment_variables:
  - name: CLAUDE_TRADING_SKILLS_REPO
    prompt: "Absolute path to claude-trading-skills repository"
    help: "Used in external-linked mode to discover canonical skills and workflow manifests."
    required_for: "external skill discovery and workflow validation"
  - name: FMP_API_KEY
    prompt: "Financial Modeling Prep API key"
    help: "Required for FMP-backed earnings, economic calendar, fundamentals, and OHLCV skills."
    required_for: "full market data functionality"
  - name: FINVIZ_API_KEY
    prompt: "FINVIZ Elite API key"
    help: "Optional for FINVIZ-backed screener workflows."
    required_for: "faster or richer screener functionality where supported"
metadata:
  hermes:
    tags: [trading, equities, research, orchestrator, finance]
    category: finance
---

# Trading Research Orchestrator

Use this skill as the front door for all trading research tasks.

## Mission

Select the right trading workflow and coordinate installed skills without making the user remember individual skill names.

## First decision

Classify the request into one of these routes:

| User intent | Preferred bundle / skills |
|---|---|
| "Morning", "pre-market", "before open" | `pre-market-routine` |
| "after close", "EOD", "what changed today" | `after-close-review` |
| "earnings", "gap", "PEAD" | `earnings-movers-triage` |
| "market regime", "risk-on", "breadth" | `market-regime-daily` |
| "find swing candidates", "VCP", "CANSLIM" | `swing-opportunity-daily` |
| "journal", "log trade", "postmortem" | `trade-journal` |
| "weekly portfolio", "dividend", "holdings" | `weekly-portfolio-review` |
| "monthly review", "process improvement" | `monthly-performance-review` |

If `trading-skills-navigator` is available, consult it before selecting the route. If it is not available, use the table above.

## Skill-selection principles

1. Start with market regime before candidate generation.
2. Only generate candidate lists when risk posture is not blocked.
3. Use earnings-specific skills for post-earnings movers instead of generic stock analysis.
4. Use `trader-memory-core` whenever a decision, thesis, or review artifact should persist.
5. Use `position-sizer` only for sizing calculations, not to imply a trade should be taken.

## Required output discipline

Every research output must include:

- Skill(s) used or intended.
- Data freshness / missing data.
- Degraded-mode caveats if any API or external repo is unavailable.
- Human decision gate.

For ticker candidates, include:

- Ticker.
- Setup type.
- Thesis.
- Invalidation condition.
- Risk notes.
- Next human action.

## Forbidden behavior

Do not output commands such as "Buy", "Sell", "Short", "Enter now", or "Place this order" as direct instructions. Use watchlist/research language.
