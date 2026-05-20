---
name: trading-risk-gate
description: "Apply a human-first trading risk gate before candidate generation, sizing, or journal review."
version: 0.1.0
metadata:
  hermes:
    tags: [trading, risk, guardrail]
    category: finance
---

# Trading Risk Gate

Use this skill before generating any candidate list or trade-plan style output.

## Risk gate states

- `FULL_RISK_ALLOWED`: broad participation, favorable trend, no major immediate event risk.
- `SELECTIVE_ONLY`: mixed evidence; only strongest setups, smaller size, tighter review.
- `CASH_PRIORITY`: risk-off or deteriorating breadth; no new discretionary swing candidates.
- `RESEARCH_ONLY`: missing data or uncertain regime; research and journaling only.

## Required checks

1. Market breadth.
2. Uptrend participation.
3. Distribution/top-risk signals.
4. Macro/earnings event risk.
5. Portfolio heat / current exposure if available.
6. Data quality/freshness.

## Output

```yaml
risk_gate:
  state: SELECTIVE_ONLY
  confidence: medium
  reasons:
    - ...
  blocked_actions:
    - ...
  allowed_actions:
    - ...
  missing_data:
    - ...
```

Do not use the risk gate to make an execution recommendation. It is a decision-support gate for the human trader.
