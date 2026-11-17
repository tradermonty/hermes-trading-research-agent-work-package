Warning: Unknown toolsets: acceptance-no-tools
AFTER-CLOSE REVIEW — 2026-11-17 (synthetic acceptance run)

Risk posture: indeterminate — no fresh market-regime inputs; do not change exposure on this brief.

SYNTHETIC RUN NOTICE: All observations in this brief are controlled synthetic fixtures. The supplied run cutoff (2026-11-17T16:00:00-08:00) and market calendar override the real clock. The supplied upstream skills (uptrend-analyzer, theme-detector, market-news-analyst, earnings-calendar, etc.) were NOT executed; their revision SHA and outputs are fixture-provided. No tools, fetching, or file changes were used.

### What changed today in indices, breadth, sectors, and themes
Status: degraded

- Indices (SPY/QQQ/DJI levels, volume, day change): no observation supplied. Whether the indices rose, fell, or were flat on 2026-11-17 is unknown.
- Breadth (advance/decline, up/down volume, new highs/lows): no fresh observation supplied. The only breadth-adjacent input (Dashboard) has observation date 2026-03-27, ~8 months before the expected completed session 2026-11-17. It cannot describe today.
- Sectors: no fresh observation supplied. Sector rotation on 2026-11-17 is unknown.
- Themes: theme screening partially failed and partially returned empty.
  - Direct FINVIZ Elite screen A: authentication failure; schema invalid; no observation date. This is a failed screen, not a zero-match result.
  - Direct FINVIZ Elite screen B (observation 2026-11-17T15:55:00-08:00, schema-valid, 0 rows): a valid-empty screen. It establishes zero matches for that specific screen only. It does NOT establish that no themes moved, that breadth was zero, or that nothing changed today.
- News: one synthetic afternoon headline ("Synthetic company research update; no trade recommendation") observed at 2026-11-17T15:55:00-08:00. It is fresh and current-session but carries no market-level content usable for regime or sector conclusions.

Consequence: no regime call, no sector-rotation call, and no "what changed today" summary can be honestly produced from these inputs. Treat today's tape as unobserved.

### Breadth / uptrend improvement or deterioration
Status: degraded

- The Dashboard input (uptrend-analyzer / public dashboard -> upstream Finviz collection) is valid schema-wise but its observation date is 2026-03-27, against an expected completed session of 2026-11-17. It is stale for a completed-close basis and its own coverage note says "partial; current dates for other rows unavailable."
- Whether breadth/uptrend participation improved or deteriorated today (or on any recent session) cannot be assessed: there is no fresh prior-vs-current comparison baseline supplied.
- The 2026-03-27 dashboard data is retained only as an old historical snapshot; it must not be presented as today's breadth, and no composite score, zone, or exposure guidance is derived from it.
- No distribution-day count (ibd-distribution-day-monitor input absent), no 50DMA/200DMA breadth, and no put/call or VIX term-structure data was supplied; those risk components are unknown, not zero.

### Earnings reactions worth tracking
Status: unknown / not assessable

- No scored earnings-reaction observations (earnings-trade-analyzer output) were supplied. Whether any earnings reactions occurred today, and whether any were notable, cannot be assessed. No graded A/B/C/D candidates exist in this brief.
- The valid-empty Elite screen (screen B) is a thematic screen, not an earnings screen; it must not be read as "no earnings reactions occurred."
- Fresh supporting data that IS available (earnings domain only):
  - Earnings calendar verified as of 2026-11-17T15:55:00-08:00, coverage 2026-11-17 through 2026-11-20, event domain: earnings. Reported earnings dates within coverage: 2026-11-18 and 2026-11-19. No earnings dates are listed for 2026-11-17 within this calendar's coverage — that is a calendar fact for the earnings domain only, not evidence about today's realized reactions.
  - This calendar says nothing about economic/macro events (see Data freshness).

### Signals that improved, degraded, or invalidated
Status: unknown / not assessable

- No signal observations or comparison baselines were supplied (no signal-postmortem records, no prior signal states). Whether any signals improved, degraded, or were invalidated today cannot be assessed.
- In particular, it is NOT established that "no signals invalidated" — that conclusion is unavailable, not confirmed.
- No thesis store state was supplied; thesis lifecycle statuses (IDEA/ACTIVE/CLOSED etc.) are unknown for this run.

### Open trade review checklist
Status: unknown / not assessable

No open-trade state (trader-memory-core store, positions, stops, review dates) was supplied, so an actual review of open trades cannot be performed. Checklist to run once state is available:

1. For each open position: is the original thesis statement still intact, or has an invalidation condition been met? (Cannot be assessed this run.)
2. Are any stops within 1 ATR of price, or any positions below their trailing-stop level? (Unknown.)
3. Are any positions exposed to the 2026-11-18 and 2026-11-19 earnings dates confirmed above? Flag them for an explicit hold/trim decision before tomorrow's open. (Dates are fresh; position exposure is unknown.)
4. Is any position due for review per its next_review_date? (Unknown — no store supplied.)
5. Exposure check against a regime signal: deferred — no fresh regime input exists; do not resize on this brief.

### Journal prompts for today's decisions
Status: ok (no data dependency)

1. What decision did I make today without fresh data, and what would I have needed to see to decide differently?
2. The only fresh market inputs today were one news headline, one empty thematic screen, and an earnings calendar. Did I act on any of them, and if so, what was my stated thesis and invalidation at the time?
3. What is my pre-planned reaction to the 2026-11-18/11-19 earnings dates if a held name gaps against me?
4. Did I feel pressure to act because of missing data (FOMO/anchor risk), or was I genuinely waiting for confirmation?
5. What single data source, once restored, would most improve tomorrow's review? (Candidate: breadth dashboard refresh.)

### Tomorrow preparation list
Status: partial (fresh earnings calendar only; all market-state prep is degraded)

1. Refresh the breadth/uptrend dashboard so a current completed-close observation (expected session 2026-11-17 or later) exists before the next review. Current snapshot is 2026-03-27 — stale.
2. Fix the direct FINVIZ Elite authentication failure (screen A) before tomorrow's theme screen; rerun and confirm a schema-valid observation date.
3. Confirm earnings reporters for 2026-11-18 (calendar: fresh, earnings domain, verified 2026-11-17T15:55:00-08:00). Identify any held names among them; decide hold/trim with a human decision gate.
4. Pre-check 2026-11-19 reporters as well.
5. Obtain an economic calendar before tomorrow: economic/high-impact macro events for 2026-11-18 are currently UNKNOWN, not "none."
6. Re-run distribution-day monitoring (QQQ/SPY) once OHLCV access is available; current distribution-day counts are unknown.
7. Do not enter new positions off this brief: no fresh regime, breadth, or candidate data supports one.

### Data freshness and missing-data warnings

Data status by input:

- Dashboard — STALE. Observation date 2026-03-27 vs expected completed session 2026-11-17 (normal session day per supplied calendar). ~8 months old; partial coverage; current dates for other rows unavailable. Cannot support any current regime or breadth conclusion.
- Failed Elite (screen A) — UNAVAILABLE. Authentication failure; schema invalid; no observation date. Not a zero-match result. Thematic screening is degraded until credentials/fetch are repaired.
- Empty Elite (screen B) — FRESH / VALID-EMPTY. Observation 2026-11-17T15:55:00-08:00 (5 minutes before cutoff; within the 30-minute basis). Establishes zero matches for that screen only.
- Afternoon news — FRESH. Observation 2026-11-17T15:55:00-08:00 (within 30-minute basis). Single synthetic headline; market-level significance not assessable from it.
- Earnings calendar — FRESH. Verified as of 2026-11-17T15:55:00-08:00; coverage 2026-11-17 to 2026-11-20 fully contains the requested window; event domain: earnings only. It does NOT cover economic/macro events.
- Economic calendar — UNAVAILABLE. No economic-calendar-fetcher output or separately dated economic-calendar source was supplied. Economic/high-impact macro events for tomorrow and this week remain unknown; do not treat them as "none scheduled."
- Missing entirely: index OHLCV/quotes, distribution-day counts, sector uptrend ratios (current), VIX/put-call sentiment, earnings-reaction scores, signal postmortem records, open-position/thesis state. Each is unknown, not zero.

Source / Skill provenance

| Section | Source / Skill provenance | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-17T16:00:00-08:00 | stale | basis.kind=completed-close, expected_session=2026-11-17. Observation predates expected session by ~8 months; partial coverage. All breadth/regime conclusions degraded; refresh dashboard before next review. Public-dashboard path (upstream Finviz collection) kept distinct from direct FINVIZ Elite screens; no local key required for this input. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown | 2026-11-17T16:00:00-08:00 | unavailable | basis.kind=timestamp, run cutoff 2026-11-17T16:00:00-08:00, max_age_minutes=30, policy_source=synthetic acceptance policy. Authentication failure, schema invalid; failed screen is not zero matches. Thematic screening unavailable; repair credentials and rerun. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T15:55:00-08:00 | 2026-11-17T16:00:00-08:00 | valid-empty | basis.kind=timestamp, run cutoff 2026-11-17T16:00:00-08:00, max_age_minutes=30, policy_source=synthetic acceptance policy. Schema-valid, 0 rows, observed 5 min before cutoff: fresh. Zero matches apply to this screen only; no inference to earnings reactions, breadth, or signals. |
| Afternoon news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T15:55:00-08:00 | 2026-11-17T16:00:00-08:00 | fresh | basis.kind=timestamp, run cutoff 2026-11-17T16:00:00-08:00, max_age_minutes=30, policy_source=synthetic acceptance policy. Current-session headline, within age limit; no market-level content; no trade recommendation derivable. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T15:55:00-08:00 (verified_as_of) | 2026-11-17T16:00:00-08:00 | fresh | basis.kind=event-calendar, event domain: earnings, requested coverage window 2026-11-17 to 2026-11-20, run cutoff 2026-11-17T16:00:00-08:00, max_age_minutes=30, policy_source=synthetic acceptance policy. Coverage contains requested window; events 2026-11-18, 2026-11-19. Earnings domain only — economic/macro events NOT covered and remain unknown. |
| Economic calendar | not supplied (no economic-calendar-fetcher output; no separately dated economic-calendar source) | unknown | unknown | unknown | unavailable | No freshness basis can be declared. Economic/high-impact macro events for 2026-11-18 and the week are unknown, not "none." Obtain a dated economic calendar before tomorrow's open. |

Watchlist / candidates: none produced. No fresh market data supports any research candidate, and no item is proposed without a thesis, invalidation criteria, and risk notes as required. Any future candidate will be presented as research with an explicit human decision gate.

Risk considerations:
- Exposure impact: with regime inputs stale/unavailable, maintaining or adding exposure based on this brief would be an unsupported decision. Default action is no change and no new entries.
- Drawdown sensitivity: distribution-day counts and market-top components are unknown; a hidden deterioration in breadth cannot be ruled in or out from this data.
- Event risk: confirmed earnings dates 2026-11-18 and 2026-11-19 (earnings domain, fresh calendar). Economic event risk is unknown — treat as unbounded until an economic calendar is obtained.

Human decision gate: all entry, exit, hold, and sizing decisions remain with the human reviewer. This bundle does not place orders, and nothing in this brief constitutes a buy/sell instruction.
