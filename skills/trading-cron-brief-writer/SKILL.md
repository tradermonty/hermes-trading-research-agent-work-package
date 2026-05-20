---
name: trading-cron-brief-writer
description: "Format scheduled trading research runs into concise, delivery-friendly briefs for Telegram, Slack, Discord, or local files."
version: 0.1.0
metadata:
  hermes:
    tags: [trading, cron, brief, reporting]
    category: finance
---

# Trading Cron Brief Writer

Use this skill whenever a scheduled trading routine is running.

## Formatting rules

- Start with a one-line status: `Risk posture: ...`
- Use compact Markdown.
- Avoid long essays in messaging channels.
- Include a `Data freshness` section.
- Include a `Human next actions` section.
- If no significant change exists and the job prompt permits silence, output exactly `[SILENT]` as the first token.

## Brief template

```markdown
# <Routine name> — <date>

**Risk posture:** <risk-on / neutral / risk-off / blocked>
**Primary reason:** <one sentence>

## 1. Key changes
- ...

## 2. Market regime
- Breadth:
- Uptrend participation:
- Distribution/top risk:

## 3. Events / earnings
- ...

## 4. Watchlist / review queue
| Ticker | Setup | Thesis | Invalidation | Follow-up |
|---|---|---|---|---|

## 5. Human next actions
- ...

## Data freshness
- ...
```

## Degraded mode

If market data, API keys, or external skills are unavailable:

1. Say which component is missing.
2. Provide what can be done offline.
3. Provide setup steps.
4. Do not fabricate numbers.
