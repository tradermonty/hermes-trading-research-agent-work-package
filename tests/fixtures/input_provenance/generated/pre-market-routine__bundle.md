Warning: Unknown toolsets: acceptance-no-tools
  ⚠ tirith security scanner enabled but not available — command scanning will use pattern matching only
PRE-MARKET RESEARCH BRIEF — 2026-11-17 (synthetic acceptance run)
workflow: pre-market-routine | run cutoff: 2026-11-17T06:00:00-08:00

Session state: normal session day (pre-market; US cash open later today)
Posture basis: pending fresh data / degraded — the expected completed session (2026-11-16) is not available; the only breadth/dashboard observation is dated 2026-03-27, so no fresh completed-close posture can be established. No regime change is being asserted.

### 1. Market posture
Status: degraded

Risk posture: UNDETERMINABLE — pending fresh data / degraded.
The only completed-close input (Dashboard) observes 2026-03-27, far older than the expected 2026-11-16 session, so no current risk-on/neutral/risk-off determination is supported. Per policy, a stale aggregate is not converted into a posture, and missing data is not read as bearish or bullish. No exposure ceiling can be responsibly published this run.

### 2. Macro calendar (high-impact events today and this week)
Status: degraded

- Economic calendar: UNAVAILABLE. No economic-calendar-fetcher output was supplied and no separately dated economic-calendar source exists. High-impact macro events for today and this week are therefore UNKNOWN — this is explicitly not "no scheduled events". No FOMC/CPI/NFP/GDP conclusions are drawn.
- Earnings calendar (separate domain): available and fresh — earnings-domain coverage 2026-11-17 through 2026-11-20, verified as of 2026-11-17T05:55:00-08:00, with scheduled event dates 2026-11-18 and 2026-11-19. This freshness applies to the earnings domain only and does not extend to economic events.

### 3. Earnings movers (large reactions, PEAD / watchlist candidates)
Status: degraded / unavailable

No earnings-trade-analyzer or PEAD screener output was supplied, and no post-earnings price/volume observations exist in this fixture. No earnings movers, PEAD candidates, or grades (A/B/C/D) are reported. The fresh earnings dates (2026-11-18, 2026-11-19) are calendar facts only, not reactions, and produce no candidates by themselves.

### 4. Breadth and uptrend participation
Status: stale

The sole breadth input (uptrend-analyzer public dashboard, sourced from an upstream Finviz collection) observed 2026-03-27 against an expected session of 2026-11-16. It is stale by the completed-close freshness basis and is NOT presented as current participation. No composite score, zone, sector heatmap, or exposure guidance is derived from it. Consequence: breadth/uptrend participation is unknown for the current posture; no breadth-based risk signal (in either direction) is asserted.

### 5. Sectors / themes worth watching
Status: degraded

- Direct FINVIZ Elite screen A: FAILED (authentication failure, schema invalid). This is an unavailable input, not a finding. It does not mean "no themes" and produces no bearish or bullish inference.
- Direct FINVIZ Elite screen B: valid-empty — a successful, schema-valid screen with zero matches, observed 2026-11-17T05:55:00-08:00 (5 minutes before cutoff, within the 30-minute basis). It is reported as "no matches this screen" and, standing alone, does not degrade the brief.
- Morning news: one synthetic headline ("Synthetic company research update; no trade recommendation"), observed 2026-11-17T05:55:00-08:00 — fresh as unfinished pre-market/news input. It is kept separate from completed-close posture and is not used to infer any completed-session regime change.
Net: no theme or sector conclusion is supportable this run. No themes are named.

### 6. Watchlist candidates
Status: withheld

None. With a degraded posture basis, no breadth data, no earnings-reaction scoring, and no theme screen output, generating watchlist candidates (thesis, invalidation, follow-up) would be unsupported. Per policy, candidate generation is withheld rather than fabricated. No /trade-ticket escalation is performed and no source_candidate_ref is issued.

### 7. Risk gate
Status: NO NEW TRADES

Risk gate: NO NEW TRADES (degraded-data gate, not a market view).
- All entry/exit decisions remain with the human reviewer; this bundle places no orders.
- Exposure impact: no new commitments until a fresh 2026-11-16 completed-close posture is available.
- Drawdown sensitivity: unknown — without current breadth/top-risk inputs, drawdown sensitivity cannot be estimated; this uncertainty itself justifies the gate.
- Event risk: earnings events on 2026-11-18 and 2026-11-19 are within the week; macro event risk is unquantified (economic calendar unavailable), which adds asymmetric uncertainty.

### 8. Data freshness and missing-data warnings
Status: degraded

Freshness basis for each input is stated in the provenance table below. Warnings:

1. SYNTHETIC DATA: every input in this run is a controlled synthetic fixture. No upstream skill was executed; no network, file, or tool access occurred. All figures and dates come solely from the supplied JSON.
2. Dashboard observation is 2026-03-27 — stale versus the expected 2026-11-16 completed session. Coverage is partial; current dates for other rows are unavailable. All breadth/posture conclusions are degraded.
3. FINVIZ Elite screen A failed authentication (schema invalid). Treat as unavailable; the likely cause is a missing/invalid FINVIZ_API_KEY. Follow-up: verify the Elite key and re-run. Note: a dashboard credential gap would not by itself block this input — the dashboard path requires no local key — but the direct Elite screen does.
4. Economic calendar is absent entirely: macro events are unknown, not "none". Follow-up: run economic-calendar-fetcher (requires FMP_API_KEY) or supply a separately dated economic-calendar source before claiming any macro coverage.
5. No earnings-reaction analytics (earnings-trade-analyzer / PEAD) were supplied; the earnings-movers section is unavailable rather than empty.
6. The fresh pre-market inputs (news headline, empty Elite screen B) are unfinished-intraday/pre-market observations and are deliberately not collapsed into completed-close posture.
7. Expected completed session per supplied calendar: 2026-11-16 (normal session day); today is a normal session day pre-open, so the 2026-11-16 close is the correct posture basis — it is simply not available.

Source / Skill provenance

Skill revision for all rows: 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed). No local modifications reported.

Section          | Source / upstream dependency                                  | Observation date        | Retrieved at              | Status      | Freshness basis and impact / follow-up
-----------------|---------------------------------------------------------------|-------------------------|---------------------------|-------------|----------------------------------------
Dashboard        | uptrend-analyzer / public dashboard -> upstream Finviz collection | 2026-03-27 (partial; current dates for other rows unavailable) | 2026-11-17T06:00:00-08:00 | stale | basis.kind=completed-close; expected_session=2026-11-16. Observation predates expected session by ~8 months → stale. Impact: breadth, uptrend participation, and market posture degraded; no score, zone, or exposure guidance published; re-fetch current dashboard before next run.
Failed Elite     | theme-detector / direct FINVIZ Elite screen A                 | unknown (auth failure; no observation) | 2026-11-17T06:00:00-08:00 | unavailable | basis.kind=timestamp; run cutoff 2026-11-17T06:00:00-08:00; max age 30 minutes; policy source: synthetic acceptance policy. Authentication failure, schema invalid — a failed screen, not "no matches". Impact: theme/sector detection unavailable; no theme conclusions drawn; verify FINVIZ_API_KEY and re-run.
Empty Elite      | theme-detector / direct FINVIZ Elite screen B                 | 2026-11-17T05:55:00-08:00 (observation timestamp; 0 rows) | 2026-11-17T06:00:00-08:00 | valid-empty | basis.kind=timestamp; run cutoff 2026-11-17T06:00:00-08:00; max age 30 minutes; policy source: synthetic acceptance policy. Observation is 5 min old → fresh. Zero matches meeting the basis; screen alone does not degrade the brief and is not a failure. No theme signal either way.
Morning news     | market-news-analyst / synthetic timestamped news              | 2026-11-17T05:55:00-08:00 (observation timestamp) | 2026-11-17T06:00:00-08:00 | fresh | basis.kind=timestamp; run cutoff 2026-11-17T06:00:00-08:00; max age 30 minutes; policy source: synthetic acceptance policy. Observation 5 min old, pre-open → fresh as unfinished pre-market news; kept separate from completed-close posture; no regime inference. Single headline: "Synthetic company research update; no trade recommendation" — no trade recommendation.
Earnings calendar | earnings-calendar / synthetic local event calendar           | verified as of 2026-11-17T05:55:00-08:00 (future event dates 2026-11-18, 2026-11-19 are not observation timestamps) | 2026-11-17T06:00:00-08:00 | fresh | basis.kind=event-calendar; event domain: earnings; requested coverage window 2026-11-17 to 2026-11-20; run cutoff 2026-11-17T06:00:00-08:00; max age 30 minutes; policy source: synthetic acceptance policy. Verified-as-of is within the age limit and the domain matches the request → fresh for earnings events 2026-11-18 and 2026-11-19. Coverage is earnings-only; it does NOT cover economic/macro events, which remain unknown.

Missing inputs (not supplied, therefore unavailable): economic-calendar-fetcher, market-breadth-analyzer, market-top-detector, ibd-distribution-day-monitor, exposure-coach, earnings-trade-analyzer, pead-screener outputs.

Human next actions
- Decide whether to accept the NO NEW TRADES gate or manually re-run the degraded inputs (fresh dashboard, FINVIZ Elite screen, economic calendar, earnings-reaction analytics) before the open.
- Note earnings dates 2026-11-18 and 2026-11-19 for personal event-risk planning.
- All entry and exit decisions remain with the human reviewer; nothing in this brief is an order instruction.

Remainder: this entire brief is synthetic acceptance output; no upstream skill was executed and no live data was accessed.
