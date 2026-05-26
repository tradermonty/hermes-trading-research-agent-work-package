Run the US equity pre-market routine for today.

Operating context:
- Timezone label for the report: {{TIMEZONE}}.
- This is research and process support.
- Use installed Claude Trading Skills when available.
- When data or API keys are unavailable, mark the relevant section as degraded mode and cite the missing input.

Session state and posture basis (mandatory two-line preamble to any risk-posture statement):

- Session state: state today's date relative to the US cash market in one of: "normal session day", "US market holiday", "weekend", "unknown". This is a calendar fact about today, not a regime label.
- Posture basis: state the latest completed regular-session close used for the posture, with the date, and label the relationship in one of three forms:
  - "based on fresh latest completed regular-session close" — the expected most recent regular-session close is available with no holiday/weekend bridge (e.g. a normal Tuesday pre-market run where Monday's close is the basis). Unfinished intraday or pre-market data is described separately from completed-close posture, not collapsed into this label.
  - "carried forward from <YYYY-MM-DD>" — the close used is calendar-old only because today follows a weekend or market holiday (e.g. a Tuesday pre-market run after a Monday holiday where the basis is the prior Friday's close). State explicitly that the posture is propagated from the most recent completed session rather than presented as a fresh regime change. This label is not mutually exclusive with the underlying truth that the close itself is the latest completed regular-session close — use this label whenever a holiday/weekend bridge sits between today and that close, so the operator does not read a structural regime change into a calendar gap.
  - "pending fresh data / degraded" — used only when the latest usable close is older than the previous regular cash-market session, or when a required data source is missing. In every other case prefer one of the two labels above.

Render these two lines before any "Risk posture:" / "REDUCE_ONLY" / "exposure ceiling" statement so that the operator reads the state and the basis before the conclusion.

Source / Skill provenance: within section 7 (Data freshness and degraded mode), render an explicit "Source / Skill provenance" sub-heading that lists which skill or data source produced each non-trivial item in the brief. Listing skills implicitly inside an unrelated section reduces operator traceability — give it its own sub-heading under section 7.

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
