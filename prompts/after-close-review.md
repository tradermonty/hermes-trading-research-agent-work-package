Run the US equity after-close review for today.

Operating context:
- Timezone label for the report: {{TIMEZONE}}.
- This is research and process support.
- Use installed Claude Trading Skills when available.
- When data or API keys are unavailable, mark the relevant section as degraded mode and cite the missing input.

Input provenance contract (morning and evening briefs):

- In the data-freshness section, render `### Source / Skill provenance` and this table, with one row per input used or attempted, including missing inputs:
  | Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
  |---|---|---|---|---|---|---|
- Source / Skill identifies the actual provider or artifact and consuming skill. For `uptrend-analyzer`, show `Finviz -> uptrend-dashboard CSV -> uptrend-analyzer`; no local key is required, but this is still an upstream Finviz dependency. Record the actual external skill checkout commit (and dirty state), or `unknown` if unverifiable. A configured key or successful download establishes neither revision nor freshness. Use redacted source identifiers without authentication query strings or secrets.
- Observation date is the underlying data's session/as-of date in `YYYY-MM-DD`, never the download time, report-generation time, or filename date. Expected observation date is the latest observation due under that input's publication schedule and the verified US market calendar. Use `unknown` for an unverified date, including undated sector/industry rows; assess each input separately rather than borrowing a newer overall dashboard date.
- Date cells contain exactly one `YYYY-MM-DD` or the literal `unknown`; use `unknown` for unverified dates, including unavailable inputs; retain a known expected date. Em dashes, N/A, date ranges, and prose are invalid in date cells. Put publication windows and calendar explanations in Impact / next step. For otherwise-fresh prior-session data carried across a weekend/holiday, use `carried_forward` consistently in both the table and affected section, rather than `fresh`.
- Status is exactly one of `fresh`, `carried_forward`, `stale`, `unavailable`, `valid_empty`, `unknown`. `fresh` means the expected observation is present. `carried_forward` means the expected latest completed session is present across a holiday/weekend bridge, preserving the existing posture-basis wording. `stale` means the observed session predates the expected session. For after-close, today's completed close is expected only after its publication is due; on holidays/weekends use the latest completed session. State the calendar/publication basis in Impact / next step; if it cannot be verified use `unknown` and degraded mode.
- `unavailable` means a missing key/skill, failed request, authentication/HTTP error, invalid CSV or missing required columns; it is never a zero-candidate result. `valid_empty` means a successful, schema-validated screen returned 0 rows for the expected observation date; state `0 validated rows`. With unverified observation metadata use `unknown` instead. An empty response body or login HTML is unavailable, not valid_empty. A stale empty screen is stale.
- In each affected report section, repeat the input's status and observation date; explain the missing/stale input and its impact plus a recovery/setup step. Preserve independently available data with its own provenance. Restrict conclusions dependent on stale/unavailable/unknown inputs to research-only or pending confirmation; missing breadth data establishes no fresh regime change. Preserve thesis, invalidation, risk notes and the human decision gate.
- Distinguish analyses not executed in this run from missing credentials. Report a missing key only when its absence is verified; otherwise describe the execution/tool scope and the input not collected. Copy supplied numeric facts exactly or omit them; keep integer counts as ungrouped source digits (for example, 2730), without inserting thousands separators; preserve source counts and units without retyping approximations as exact values.
- The table can be checked offline with `python3 scripts/validate_brief_provenance.py <brief.md>` from the installed profile root. This checks declared fields/date consistency only; source truth, calendar choice, completeness and dependent conclusions still require human review.
- Declare Freshness basis in Impact / next step for every input, per row/series; mixed-age rows cannot establish a fresh aggregate. Record Retrieved at (download timestamp with timezone) there separately from observation metadata. Use the installed claude-trading-skills commit SHA and local modifications; omit auth query strings and credentials.
- Completed-close series use the expected completed regular session, allowing for the source publication schedule. Before the close use the latest completed regular session; after the close expect today's completed session only once publication is due. Preserve the holiday/weekend carry-forward rule and use `carried_forward` for current completed-close inputs across that bridge.
- Timestamp-based news, earnings releases, pre-market/live quotes and screens use their own observation timestamp, timezone, run cutoff, and a source-specific age limit (state the limit and its source). Put full observation timestamps and timing policy in Impact / next step; the date cells contain their observation and expected-as-of dates only. Date equality alone cannot establish freshness: same-day expired data is `stale`, including an empty screen. If the policy or observation time is unverifiable, use `unknown` and degraded mode. Reject future observation timestamps beyond the run cutoff as `unavailable`. A valid current-morning input can be fresh; keep it separate from completed-close posture and label live/premarket data as unfinished.
- Event calendars use their verified-as-of timestamp and coverage of the requested event window; future event dates are not observation timestamps. Record the event domain (earnings, economic, etc.) in the freshness basis. Without economic-calendar-fetcher or a separately dated economic-calendar source, economic/high-impact macro events remain unknown / unavailable, never "none" or "no scheduled high-impact events". Disclose economic-calendar availability separately from fresh earnings coverage.
- A `valid_empty` screen must meet its declared timing basis as well as date/schema checks. A valid_empty screen alone does not degrade the brief. Retain independent fresh data; withhold unsupported rankings, candidates and posture changes. Manual/public fallback needs its own source and observation date and must be labelled as fallback. Missing FINVIZ_API_KEY affects direct Elite screens, not independently validated dashboard data, and only report the key missing when verified. Do not enable optional MCPs to satisfy this contract.
- Put screen disclosures inside the affected themes/sectors or candidate section before Data freshness: `<screen name>: <status>; observation date: <date or unknown>; <impact and recovery step>`. An authentication failure uses `unavailable`; a verified zero-row screen uses `valid_empty`. A disclosure present only in the Data freshness footer does not satisfy this inline requirement.

Required output:

# After-close review — <date>

**Risk posture change:** <improved / unchanged / deteriorated / unknown>
**Primary reason:** <one sentence>

## 1. Market action summary
- Indices.
- Breadth.
- Uptrend participation.
- Distribution and top-risk changes.

## 2. Sector and theme rotation
- Leading groups.
- Lagging groups.
- Notable rotation.

## 3. Earnings reactions
- Names worth tracking.
- PEAD candidates.
- Reactions that failed or reversed.

## 4. Open trade review checklist
- Thesis still valid?
- Invalidation hit?
- Position risk still acceptable?
- Any overnight event risk?

## 5. Journal prompts
- What decision today deserves a note?
- What did the process do well?
- What should be avoided tomorrow?

## 6. Tomorrow preparation
- Maximum 5 bullets.

## 7. Data freshness and degraded mode
- Include the input provenance table above, plus missing keys and stale data warnings.

Use review and journaling language throughout. The human reviewer makes all entry and exit decisions.
