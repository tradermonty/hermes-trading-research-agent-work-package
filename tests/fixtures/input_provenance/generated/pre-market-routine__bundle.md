Warning: Unknown toolsets: acceptance-no-tools
Pre-Market Research Brief — 2026-11-17 (synthetic acceptance run)

Note: This is a controlled synthetic acceptance run. All inputs are fixture-supplied; no upstream skills were executed, no network fetches or tools were run, and no files were changed. Do not treat any figure below as real market data.

### 1. Market posture
Status: degraded

Session state: normal session day (2026-11-17, pre-market; US cash session opens 09:30 ET today).
Posture basis: pending fresh data / degraded — the only completed-close input (Dashboard) has observation date 2026-03-27, which is older than the expected completed regular session 2026-11-16. The posture is therefore NOT presented as a fresh or carried-forward regime; it is degraded pending a validated 2026-11-16 completed-close observation.

Risk posture: no reliable risk-on/neutral/risk-off determination is possible. Per the exposure-coach "safety first" principle, the conservative default applies until fresh completed-close data arrives (see Risk gate).

### 2. Macro calendar
Status: partial / degraded

- Economic calendar (FMP-backed): no input supplied for this run → today's and this week's high-impact macro events are UNKNOWN. No high-impact event list can be produced and none should be inferred.
- Earnings calendar (synthetic local event calendar): verified-as-of 2026-11-17T05:55:00-08:00; coverage 2026-11-17 through 2026-11-20; scheduled event dates present on 2026-11-18 and 2026-11-19. The fixture provides dates only (no named companies), so no per-name event risk can be assessed. Future event dates are schedule entries, not observations.

Follow-up: obtain a fresh economic-calendar fetch and a named earnings calendar before open.

### 3. Earnings movers
Status: unavailable

- Earnings-trade-analyzer and pead-screener were not run and supplied no data → no post-earnings reactions, no grades, no PEAD candidates. "No movers" is NOT a valid conclusion; the correct state is no-data.
- Morning news (synthetic timestamped item, 2026-11-17T05:55:00-08:00): "Synthetic company research update; no trade recommendation." This is unfinished pre-market news context only and carries no candidate or posture implication.

### 4. Breadth and uptrend participation
Status: stale

- The sole completed-close input (uptrend-analyzer / public dashboard -> upstream Finviz collection) observes 2026-03-27 — approximately 8 months older than the expected completed session 2026-11-16 (basis kind: completed-close, expected_session 2026-11-16). It is STALE, not fresh.
- No composite breadth or uptrend score is computed. No breadth number, participation percentage, or distribution-day count is reported, and none should be inferred from the March observation (it describes a different market regime entirely).
- ibd-distribution-day-monitor and market-top-detector: no data supplied → distribution-day counts and top-risk score are unavailable/unknown.

### 5. Sectors/themes worth watching
Status: valid-empty (screen B) / unavailable (screen A)

- Direct FINVIZ Elite screen A (theme-detector): authentication_failure → unavailable. This is a failed screen; it must not be read as "no themes" or as a bearish signal. Likely cause: missing/invalid FINVIZ_API_KEY.
- Direct FINVIZ Elite screen B (theme-detector): successful, schema-valid, 0 rows, observed 2026-11-17T05:55:00-08:00 (5 minutes before the 06:00 cutoff; within the 30-minute max age). This is a genuine valid-empty result for that specific screen only — "no matches" — and does not by itself degrade the brief or establish an absence of market themes.
- No positive theme, sector-ranking, or leadership evidence exists in this run. Withholding all theme conclusions.

### 6. Watchlist candidates
Status: withheld / unavailable

No watchlist candidates are presented. Candidate generation depends on stale (dashboard) or missing (earnings-trade-analyzer, pead-screener, theme-detector screen A) inputs, so all candidate rankings are withheld rather than fabricated. No `/trade-ticket` escalation applies this run (no `source_bundle: pre-market-routine` candidates exist).

For the record, any future escalation would require `source_bundle: pre-market-routine` and a stable `source_candidate_ref` of the form `<TICKER>-<YYYY-MM-DD>-<setup>`.

### 7. Risk gate
Status: degraded

Risk gate: NO NEW TRADES.

Rationale: the posture basis is pending fresh data / degraded; required completed-close inputs are stale and candidate inputs are absent. Exposure-impact: treat effective equity exposure ceiling as reduced pending re-validation; drawdown sensitivity is elevated because no validated breadth, top-risk, or distribution-day control is available; event risk is unquantified (economic calendar missing; unnamed earnings events on 11-18/11-19).

The human reviewer retains all entry and exit decisions; this bundle places no orders.

### 8. Data freshness and missing-data warnings
Status: degraded (stale + unavailable inputs)

Source / Skill provenance

| Section | Source / upstream dependency | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection (public dashboard path; distinct from direct Elite screens) | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-17T06:00:00-08:00 | stale | Freshness basis: completed-close (expected_session 2026-11-16). Observation is ~8 months older than the expected session → stale. Sections 1 and 4 degraded; no breadth/uptrend score computed; no regime change inferred. Refetch the 2026-11-16 completed-close series. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown (no observation; auth failed before data) | 2026-11-17T06:00:00-08:00 | unavailable | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00, max age 30 min, policy: synthetic acceptance policy). Fetch = authentication_failure, schema invalid → unavailable. Cause: missing/invalid FINVIZ_API_KEY. Section 5 partially degraded; screen A yields no conclusion either way. Fix key and re-run. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T05:55:00-08:00 | 2026-11-17T06:00:00-08:00 | valid-empty | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00, max age 30 min, policy: synthetic acceptance policy). Observation is 5 min old → fresh. Schema-valid screen with 0 rows: a genuine "no matches" for this screen only; does not represent failed collection and does not alone establish absence of market themes. |
| Morning news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T05:55:00-08:00 | 2026-11-17T06:00:00-08:00 | fresh | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00, max age 30 min, policy: synthetic acceptance policy). Observation is 5 min old → fresh. Unfinished pre-market news context; explicitly carries no trade recommendation and is kept separate from completed-close posture. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | verified-as-of 2026-11-17T05:55:00-08:00 (event dates 2026-11-18, 2026-11-19 are schedule entries, not observation timestamps) | 2026-11-17T06:00:00-08:00 | fresh | Freshness basis: event-calendar (requested coverage window 2026-11-17 to 2026-11-20; max age 30 min; policy: synthetic acceptance policy). Verified-as-of is 5 min old and declared coverage fully spans the requested window → fresh. Date-only fixture: no named companies, so no per-name event risk. |
| — (not supplied) | economic-calendar-fetcher (FMP) | n/a — input not provided in fixture | unknown | unknown | unavailable | Freshness basis: n/a (input absent). Section 2 high-impact macro events unknown; do not infer a quiet calendar. Fetch before open. |
| — (not supplied) | earnings-trade-analyzer, pead-screener, ibd-distribution-day-monitor, market-top-detector, exposure-coach | n/a — inputs not provided in fixture | unknown | unknown | unavailable | Sections 3, 4, 6 depend on these; all dependent conclusions withheld. No graded movers, PEAD stages, distribution-day counts, top-risk score, or exposure ceiling produced. |

Missing-data summary:
- Stale: Dashboard completed-close series (2026-03-27 vs expected 2026-11-16) → Sections 1, 4 degraded.
- Unavailable: Elite screen A (auth failure), economic calendar, earnings movers, PEAD, distribution days, top risk, exposure inputs → Sections 2, 3, 5 (partial), 6 affected.
- Fresh: Morning news (timestamp), Earnings calendar (event-calendar), Empty Elite screen B (valid-empty).
- Global caveat: all data are synthetic fixture values; supplied upstream skills were not executed. Nothing in this brief should be actioned as market data.
