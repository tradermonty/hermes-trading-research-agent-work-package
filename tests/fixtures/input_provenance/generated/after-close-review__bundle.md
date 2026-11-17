Warning: Unknown toolsets: acceptance-no-tools
AFTER-CLOSE REVIEW — US EQUITIES
Session: 2026-11-17 (normal session day, expected completed session per supplied calendar)
Run cutoff: 2026-11-17T16:00:00-08:00

*** CONTROLLED SYNTHETIC ACCEPTANCE RUN ***
All observations are synthetic fixtures. No tools were run, nothing was fetched, and the supplied upstream skills (uptrend-analyzer, theme-detector/FINVIZ screens, market-news-analyst, earnings-calendar) were NOT executed. This brief exercises the reporting/provenance contract only. It does not place orders and does not make entry/exit decisions — all decisions remain with the human reviewer.

Risk posture: UNDETERMINED / BLOCKED — no fresh completed-close regime input is available for the expected session (2026-11-17), so no posture change can be supported.

--------------------------------------------------------------------
1. WHAT CHANGED TODAY (INDICES, BREADTH, SECTORS, THEMES)
Status: degraded

- Index moves: unknown. No index OHLC/close input was supplied for 2026-11-17. No level, % change, or volume can be reported.
- Breadth: cannot be assessed for today. The only breadth/dashboard input carries observation date 2026-03-27, which does not satisfy the completed-close basis (expected_session 2026-11-17). It is stale and is not used as today's reading.
- Sectors: cannot be assessed. No sector dataset was supplied.
- Themes: the only theme input is the "Empty Elite" screen, which is schema-valid with zero rows observed at 2026-11-17T15:55:00-08:00. This is a valid-empty result ("no matches for the screen criteria as of that timestamp") — it is NOT a failed screen, NOT zero breadth, and NOT a bearish signal. The second Elite screen (A) failed authentication and yields no theme information at all.

Consequence: the "what changed today" summary is empty of substantive market content by design. Nothing is inferred to fill the gaps.

--------------------------------------------------------------------
2. BREADTH / UPTREND IMPROVEMENT OR DETERIORATION
Status: degraded (stale input)

- Dashboard observation date: 2026-03-27. Expected completed session: 2026-11-17. Age ≈ 8 months on a completed-close basis → stale; do not compare against any prior run, do not compute a trend, and do not carry the March reading forward as a proxy for November.
- Partial coverage: the fixture states "current dates for other rows unavailable," so even within the dashboard some rows lack a known observation date. Those rows are treated as unknown-age and excluded from any freshness claim.
- No improvement/deterioration determination is possible this run. Pending fresh data.

--------------------------------------------------------------------
3. EARNINGS REACTIONS WORTH TRACKING
Status: degraded (calendar fresh; reaction data absent)

- No earnings-trade-analyzer output was supplied for this run, so there are no scored post-earnings reactions, grades, or candidates. Do not fabricate names.
- The supplied event calendar is fresh (verified_as_of 2026-11-17T15:55:00-08:00) and covers the requested window 2026-11-17 through 2026-11-20, with event dates 2026-11-18 and 2026-11-19 (both future dates — they are calendar entries, not observations). Tomorrow's session carries scheduled earnings events; prepare for event risk rather than reacting to unverified reactions.

--------------------------------------------------------------------
4. SIGNALS IMPROVED / DEGRADED / INVALIDATED
Status: unavailable

- No signal records, thesis state, or prior-run outputs were supplied. No signal can be promoted, demoted, or invalidated. Prior theses/signals cannot be evaluated against today's close because today's close data itself is absent. This is an explicit gap, not a clean signal.

--------------------------------------------------------------------
5. OPEN TRADE REVIEW CHECKLIST
Status: degraded (checklist usable; verification inputs absent)

For each open position, the human reviewer should confirm:
1. Position thesis statement still intact (no thesis-level invalidation observed — but note: no market data this run to confirm either way).
2. Stop level and trailing logic unchanged; no data-driven adjustment possible this run.
3. Event exposure: does the position have an earnings date on 2026-11-18 or 2026-11-19? The fresh calendar shows events on those dates; check your own holdings against them before tomorrow's open.
4. Size/exposure: no regime signal is available to justify any exposure change; default is to make no change pending fresh data.
5. Journal any decision made tonight with the data caveat recorded (see section 6).

--------------------------------------------------------------------
6. JOURNAL PROMPTS FOR TODAY'S DECISIONS
Status: available (process section, not data-dependent)

- Did I make any decision today based on the 2026-03-27 dashboard? If so, flag it — that input was stale and should not have driven anything.
- What would I have needed to see (breadth, Elite screen output, index close) before changing exposure — and did I have it?
- The Elite screen A failed on authentication, not on logic. Does my workflow have a fallback that I trust, and is it labelled as a fallback?
- The empty Elite screen returned zero rows. Did I (or would I) have misread "no matches" as a market signal? Record the distinction.
- With earnings on 11-18/11-19: which positions or watchlist names have event risk, and what is my plan for each?

--------------------------------------------------------------------
7. TOMORROW PREPARATION LIST
Status: available (process section)

1. Fix FINVIZ Elite authentication (screen A failed auth) and re-run the theme screen after the next close; treat the re-run as the first valid theme observation.
2. Obtain a completed-close breadth/uptrend dataset with observation date 2026-11-17 (or the then-current expected session) before any regime or posture conclusion.
3. Re-check the earnings calendar for updates; events are scheduled for 2026-11-18 and 2026-11-19 — verify names/timings before the open.
4. If the news pipeline produces only low-impact single-name items again, note that in the routine rather than inflating it.
5. Do not act on the 2026-03-27 dashboard; replace it.

--------------------------------------------------------------------
8. DATA FRESHNESS AND MISSING-DATA WARNINGS

Per-input status:
- Dashboard: STALE — observation 2026-03-27 vs expected completed session 2026-11-17; partial coverage (some row dates unknown). Excluded from all conclusions.
- Failed Elite (screen A): UNAVAILABLE — authentication_failure, schema invalid, no observation timestamp. Not a zero-match result. Requires credential fix.
- Empty Elite (screen B): FRESH / VALID-EMPTY — schema-valid, 0 rows, observed 2026-11-17T15:55:00-08:00 (5 min before retrieval; within the 30-minute timestamp basis). Means "no screen matches," nothing more.
- Afternoon news: FRESH — timestamped 2026-11-17T15:55:00-08:00, within 30-minute basis. Single synthetic company-research headline; no market-level or trade content.
- Earnings calendar: FRESH — verified_as_of 2026-11-17T15:55:00-08:00, coverage 2026-11-17 to 2026-11-20 fully covering the requested window; event dates 2026-11-18, 2026-11-19 are future schedule entries, not observations.

Missing entirely (not supplied, not inferred): index closes/volume for 2026-11-17, distribution-day counts, market-top score, sector ratios, scored earnings reactions, open thesis state.

--------------------------------------------------------------------
### Dashboard
Status: stale

Observation date 2026-03-27 against a completed-close basis expecting session 2026-11-17. Coverage partial (other row dates unavailable). Impact: no breadth/uptrend/sector conclusion is drawn; breadth and regime sections are degraded and marked pending fresh data.

### Failed Elite
Status: unavailable

Direct FINVIZ Elite screen A failed authentication (no valid observation timestamp, schema invalid). Impact: no theme observation from this screen; the failure is NOT converted into "no matches," zero breadth, or any directional signal. Follow-up: fix FINVIZ_API_KEY / credentials and re-run.

### Empty Elite
Status: fresh (valid-empty)

Schema-valid screen with 0 rows observed 2026-11-17T15:55:00-08:00, retrieved 2026-11-17T16:00:00-08:00. Impact: recorded as "no matches for the screen criteria"; contributes no theme candidates and no market signal. A valid-empty screen alone does not degrade the brief.

### Afternoon news
Status: fresh

Timestamped 2026-11-17T15:55:00-08:00 (within the 30-minute basis). Content: "Synthetic company research update; no trade recommendation." Impact: single low-impact item; no market regime inference; no watchlist addition.

### Earnings calendar
Status: fresh

Verified as of 2026-11-17T15:55:00-08:00; coverage 2026-11-17 through 2026-11-20 fully satisfies the requested window; events listed for 2026-11-18 and 2026-11-19 (future dates = schedule, not observations). Impact: earnings section is limited to forward event risk; no reactions to track without analyzer output.

--------------------------------------------------------------------
Source / Skill provenance

| Section | Source / upstream dependency | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 (partial; current dates for other rows unavailable) | 2026-11-17T16:00:00-08:00 | stale | Freshness basis: completed-close, expected_session 2026-11-17. Observation predates expected session by ~8 months and does not satisfy the basis; partial row-date coverage. All breadth/uptrend/sector conclusions withheld; regime posture UNDETERMINED; replace dataset before next run. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown (authentication_failure — no observation possible) | 2026-11-17T16:00:00-08:00 | unavailable | Freshness basis: timestamp, run cutoff 2026-11-17T16:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy. Auth failure → schema invalid → no data. Consequences: no theme signal from screen A; do not interpret as valid-empty; fix credentials and re-run. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T15:55:00-08:00 (observation timestamp) | 2026-11-17T16:00:00-08:00 | fresh (valid-empty, 0 rows) | Freshness basis: timestamp, run cutoff 2026-11-17T16:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy. Observation is 5 minutes old → fresh. Zero rows = no matches for screen criteria only; contributes no theme candidates and no directional signal. |
| Afternoon news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T15:55:00-08:00 (observation timestamp) | 2026-11-17T16:00:00-08:00 | fresh | Freshness basis: timestamp, run cutoff 2026-11-17T16:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy. Headline explicitly carries no trade recommendation; single-name item only — no market/regime inference drawn. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | verified_as_of 2026-11-17T15:55:00-08:00 (event dates 2026-11-18, 2026-11-19 are future schedule entries, not observations) | 2026-11-17T16:00:00-08:00 | fresh | Freshness basis: event-calendar, verified-as-of within run cutoff 2026-11-17T16:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy, requested coverage window 2026-11-17 to 2026-11-20 — fully covered. Used only for forward event-risk preparation; no reaction data exists, so the earnings-reactions section stays degraded. |

Provenance notes:
- Public dashboard path (uptrend-analyzer → TraderMonty/public dashboard → upstream Finviz collection) is recorded separately from the direct FINVIZ Elite screens (theme-detector), as required; a dashboard observation and an Elite screen are independent inputs with independent freshness.
- The installed claude-trading-skills revision is recorded exactly as supplied: 6e9a635e5259601d79bb7a97085784f8b37742b5, clean, fixture-provided, not executed. No local modifications claimed beyond what the fixture states.
- No credentials, auth strings, or non-public URLs are included. No optional MCPs were enabled.

--------------------------------------------------------------------
Risk considerations (run-level)
- Exposure impact: with regime UNDETERMINED, no data-driven exposure change is supportable in either direction; default is hold-and-wait.
- Drawdown sensitivity: absent fresh breadth/distribution inputs, drawdown-control triggers (stops, trailing logic) must run on position-level rules only, not market-regime signals.
- Event risk: confirmed scheduled earnings on 2026-11-18 and 2026-11-19; any position or candidate overlapping those dates carries gap risk that this run could not quantify.

Human decision gate: this bundle produces research and checklists only. All entry, exit, sizing, and exposure decisions are made by the human reviewer. No orders were placed or proposed for execution.

Synthetic data disclaimer: every observation above is a supplied synthetic fixture for acceptance testing; the upstream skills were not executed, and no real market data was accessed.
