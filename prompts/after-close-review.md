Run the US equity after-close review for today.

Operating context:
- Timezone label for the report: {{TIMEZONE}}.
- This is research and process support.
- Use installed Claude Trading Skills when available.
- When data or API keys are unavailable, mark the relevant section as degraded mode and cite the missing input.

Input provenance and freshness (required in both the affected section and the final Data freshness section):

- Render a "Source / Skill provenance" table with columns: Section | Source / upstream dependency | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up. Record the installed claude-trading-skills commit SHA and local modifications (or package version/hash); use unknown when unavailable, never infer the revision from a skill name. Identify public dashboard -> upstream Finviz collection separately from a direct FINVIZ Elite screen. Record only safe source URLs/paths; omit auth query strings and credentials.
- Observation date means the underlying market session, per row/series where available. Retrieved at means download time. A successful HTTP response, a recent download, or no local key required establishes neither freshness nor coverage. Unknown observation dates or partial coverage must remain explicit; do not invent dates or treat mixed-age rows as a fresh aggregate.
- Use these statuses: fresh (validated input for the expected completed session); stale (observation predates that session); unavailable (fetch/auth/schema failure, missing input, or unverifiable observation date); valid-empty (successful, schema-valid, current-session screen with zero matches). When the observation date is unavailable write unknown and explain the reason; preserve any known cached observation date separately. Valid-empty means "no matches", never a failed screen, missing column, unexpected HTML, malformed CSV, or a missing key. HTTP 200 and credentials alone do not validate a screen.
- Determine the expected completed session from the cash-market calendar and the run's cutoff, not calendar age alone. Before the close use the latest completed regular session; after the close expect today's completed session on a regular session day; on holidays/weekends use the most recent completed regular session. If the calendar or completion cutoff is uncertain, label freshness unknown / unavailable and explain. Preserve the pre-market "Session state" / "Posture basis" holiday/weekend carry-forward rule: the latest completed session across a calendar bridge is not stale merely because it is calendar-old. Older or missing required inputs still mean pending fresh data / degraded.
- Mark only affected sections and dependent conclusions as degraded for stale/unavailable inputs; retain independent fresh data with its own provenance. Withhold unsupported rankings, candidates, and posture changes; do not turn a failed Elite screen into "no matches", zero breadth, or a bearish signal. A valid-empty screen alone does not degrade the brief. Keep thesis, invalidation, risk notes, and the human decision gate for any retained research candidate.
- Local credential requirements and upstream provenance are separate: uptrend-analyzer needs no local key to read the public dashboard, whose collection depends on Finviz. Missing FINVIZ_API_KEY affects direct Elite screens, not independently validated dashboard data. Manual/public fallback needs its own source and observation date and must be labelled as a fallback rather than a successful Elite run. Do not enable optional MCPs to satisfy this contract.

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
- List data sources, skill outputs, missing keys, and stale data warnings.

Use review and journaling language throughout. The human reviewer makes all entry and exit decisions.
