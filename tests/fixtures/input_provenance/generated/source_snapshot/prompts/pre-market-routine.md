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

Input provenance and freshness (required in both the affected section and the final Data freshness section):

- Render a "Source / Skill provenance" table with columns: Section | Source / upstream dependency | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up. Record the installed claude-trading-skills commit SHA and local modifications (or package version/hash); use unknown when unavailable, never infer the revision from a skill name. Identify public dashboard -> upstream Finviz collection separately from a direct FINVIZ Elite screen. Record only safe source URLs/paths; omit auth query strings and credentials.
- Observation date means the underlying market session, per row/series where available. Retrieved at means download time. A successful HTTP response, a recent download, or no local key required establishes neither freshness nor coverage. Unknown observation dates or partial coverage must remain explicit; do not invent dates or treat mixed-age rows as a fresh aggregate.
- Use these statuses against each input's declared freshness basis: fresh (validated input meeting that basis); stale (observation older than that basis permits); unavailable (fetch/auth/schema failure, missing input, or unverifiable observation time/basis); valid-empty (successful, schema-valid screen with zero matches meeting its declared freshness basis). When the observation date is unavailable write unknown and explain the reason; preserve any known cached observation date separately. Valid-empty means "no matches", never a failed screen, missing column, unexpected HTML, malformed CSV, or a missing key. HTTP 200 and credentials alone do not validate a screen.
- Declare Freshness basis in the Impact / follow-up cell for every input. Completed-close series use the expected completed regular session. Timestamp-based news, earnings releases, pre-market/live quotes and screens use their own observation timestamp, timezone, run cutoff, and a source-specific age limit (state the limit and its source; if no limit is known, report unavailable rather than invent one). Event calendars use their verified-as-of timestamp and explicit coverage of the requested event window; future event dates are not observation timestamps. Calendar coverage also has an event domain (earnings, economic, etc.); state that domain in the freshness basis and never extend its coverage to a different domain. An earnings-calendar establishes earnings coverage only. Without economic-calendar-fetcher or a separately dated economic-calendar source, economic/high-impact macro events remain unknown / unavailable, never "none" or "no scheduled high-impact events". A fresh earnings calendar does not make the Macro calendar section wholly fresh; disclose economic-calendar availability separately. Reject future observation timestamps beyond the run cutoff. A valid current-morning news/release/screen can be fresh before the open even when its date is later than the posture close; keep it separate from completed-close posture and label live/premarket data as unfinished. Never use it to replace the completed close or infer a completed-session regime change.
- For completed-close series only, determine the expected completed session from the cash-market calendar and the run's cutoff, not calendar age alone. Before the close use the latest completed regular session; after the close expect today's completed session on a regular session day; on holidays/weekends use the most recent completed regular session. If the calendar or completion cutoff is uncertain, label freshness unknown / unavailable and explain. Preserve the pre-market "Session state" / "Posture basis" holiday/weekend carry-forward rule: the latest completed session across a calendar bridge is not stale merely because it is calendar-old. Older or missing required inputs still mean pending fresh data / degraded.
- Mark only affected sections and dependent conclusions as degraded for stale/unavailable inputs; retain independent fresh data with its own provenance. Withhold unsupported rankings, candidates, and posture changes; do not turn a failed Elite screen into "no matches", zero breadth, or a bearish signal. A valid-empty screen alone does not degrade the brief. Keep thesis, invalidation, risk notes, and the human decision gate for any retained research candidate.
- Local credential requirements and upstream provenance are separate: uptrend-analyzer needs no local key to read the public dashboard, whose collection depends on Finviz. Missing FINVIZ_API_KEY affects direct Elite screens, not independently validated dashboard data. Manual/public fallback needs its own source and observation date and must be labelled as a fallback rather than a successful Elite run. Do not enable optional MCPs to satisfy this contract.

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
