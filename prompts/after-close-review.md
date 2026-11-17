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
- Status is exactly one of `fresh`, `carried_forward`, `stale`, `unavailable`, `valid_empty`, `unknown`. `fresh` means the expected observation is present. `carried_forward` means the expected latest completed session is present across a holiday/weekend bridge, preserving the existing posture-basis wording. `stale` means the observed session predates the expected session. For after-close, today's completed close is expected only after its publication is due; on holidays/weekends use the latest completed session. State the calendar/publication basis in Impact / next step; if it cannot be verified use `unknown` and degraded mode.
- `unavailable` means a missing key/skill, failed request, authentication/HTTP error, invalid CSV or missing required columns; it is never a zero-candidate result. `valid_empty` means a successful, schema-validated screen returned 0 rows for the expected observation date; state `0 validated rows`. With unverified observation metadata use `unknown` instead. An empty response body or login HTML is unavailable, not valid_empty. A stale empty screen is stale.
- In each affected report section, repeat the input's status and observation date; explain the missing/stale input and its impact plus a recovery/setup step. Preserve independently available data with its own provenance. Restrict conclusions dependent on stale/unavailable/unknown inputs to research-only or pending confirmation; missing breadth data establishes no fresh regime change. Preserve thesis, invalidation, risk notes and the human decision gate.
- The table can be checked offline with `python3 scripts/validate_brief_provenance.py <brief.md>` from the installed profile root. This checks declared fields/date consistency only; source truth, calendar choice, completeness and dependent conclusions still require human review.

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
