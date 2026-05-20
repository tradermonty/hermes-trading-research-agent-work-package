Run the US equity pre-market routine for today.

Operating context:
- Timezone label for the report: America/Los_Angeles.
- This is research and process support.
- Use installed Claude Trading Skills when available.
- When data or API keys are unavailable, mark the relevant section as degraded mode and cite the missing input.

Required output:

# Pre-market routine — <date>

**Risk posture:** <risk-on / neutral / risk-off / research-only>
**Primary reason:** <one sentence>

## 1. Macro calendar
- High-impact events today.
- High-impact events this week.
- Event risk around market open.

## 2. Market regime
- Breadth.
- Uptrend participation.
- Distribution and top-risk signals.
- Exposure posture.

## 3. Earnings movers
- Major gap-up and gap-down reactions.
- PEAD and watchlist candidates.
- Names requiring manual chart review.

## 4. Themes and sectors
- Themes showing strength.
- Themes showing weakness.
- Contradictory signals.

## 5. Watchlist candidates
Use a table:
| Ticker | Setup | Thesis | Invalidation | Risk notes | Follow-up |

## 6. Human next actions
- Maximum 5 bullets.

## 7. Data freshness and degraded mode
- List data sources, skill outputs, missing keys, and stale data warnings.

Use research and watchlist language throughout. The human reviewer makes all entry and exit decisions.
