Warning: Unknown toolsets: acceptance-no-tools
# Pre-market routine — 2026-11-17

Session state: normal session day.
Posture basis: pending fresh data / degraded — latest usable completed-close breadth/dashboard input is 2026-03-27, older than expected completed regular session 2026-11-16.

**Risk posture:** research-only
**Primary reason:** Completed-close regime/breadth data is stale, one direct screen is unavailable from authentication failure, and economic calendar coverage is unavailable; fresh timestamped inputs are limited to synthetic news, a valid-empty screen, and earnings-calendar coverage.

Synthetic acceptance run note: This brief uses only the supplied synthetic observations. No tools, browsing, fetching, file changes, or upstream skills were executed.

## 1. Macro calendar

Economic-calendar availability:
- Status: unavailable.
- Observation date: unknown.
- Impact: No supplied economic-calendar-fetcher output or separately dated economic-calendar source was provided. High-impact economic events today and this week are unknown; do not infer “none.”

Earnings-calendar availability:
- Status: fresh.
- Observation date: 2026-11-17.
- Coverage: synthetic earnings calendar verified as of 2026-11-17T05:55:00-08:00, covering 2026-11-17 through 2026-11-20.
- Supplied event dates: 2026-11-18 and 2026-11-19.
- Impact: Earnings event-window awareness is available, but no individual company names or reactions were supplied.

High-impact events today:
- Economic: unknown / unavailable.
- Earnings: calendar coverage is fresh, but no specific earnings names for today were supplied.

High-impact events this week:
- Economic: unknown / unavailable.
- Earnings: supplied synthetic event dates include 2026-11-18 and 2026-11-19 within requested coverage.

Event risk around market open:
- Economic open-risk: unknown due unavailable economic calendar.
- Earnings open-risk: no specific pre-market earnings releases or company-level event details supplied.
- Research implication: treat event risk as unresolved until a fresh economic calendar and company-level earnings list are reviewed.

## 2. Market regime

Breadth:
- Status: stale.
- Observation date: 2026-03-27.
- Expected completed session: 2026-11-16.
- The supplied dashboard/uptrend input is too old to establish current breadth.

Uptrend participation:
- Status: stale.
- Observation date: 2026-03-27.
- Current uptrend participation cannot be concluded from this fixture.

Distribution and top-risk signals:
- Status: degraded.
- The supplied completed-close dashboard is stale and partial.
- No fresh distribution-day, index trend, volatility, leadership, or risk-signal series was supplied.

Exposure posture:
- Research-only posture.
- No fresh completed-close regime change is established.
- Missing breadth data establishes no fresh risk-on/risk-off transition.
- Human decision gate: any exposure decision requires fresh completed-close market data and manual chart/index review.

## 3. Earnings movers

Major gap-up and gap-down reactions:
- Status: unavailable.
- No pre-market quotes, earnings reaction screen, or company-level movers were supplied.

PEAD and watchlist candidates:
- Status: unavailable.
- Fresh earnings calendar coverage exists, but it does not include tickers, reaction magnitude, guidance details, volume, or post-earnings drift inputs.

Names requiring manual chart review:
- No company-level earnings names were supplied.
- Manual review should wait for a fresh earnings movers source or broker/platform scan.

Research implication:
- Earnings calendar is usable only for awareness of the 2026-11-17 to 2026-11-20 event window.
- It cannot produce earnings-reaction watchlist candidates in this run.

## 4. Themes and sectors

Themes showing strength:
- Status: degraded.
- Empty Elite screen B returned 0 validated rows as of 2026-11-17T05:55:00-08:00, within the synthetic 30-minute policy window.
- This is valid_empty, not a data failure.
- However, one separate Elite screen A failed authentication, and the broader dashboard is stale, so no broad strength ranking is supported.

Themes showing weakness:
- Status: degraded.
- No validated weakness screen, sector performance table, industry breadth, or fresh dashboard detail was supplied.

Contradictory signals:
- Fresh valid_empty screen: direct FINVIZ Elite screen B produced 0 validated rows.
- Unavailable screen: direct FINVIZ Elite screen A failed authentication.
- Stale dashboard: completed-close dashboard observation is 2026-03-27 versus expected 2026-11-16.
- Fresh news: synthetic timestamped company research update exists but contains no trade recommendation and no actionable ticker-level setup.

## 5. Watchlist candidates

| Ticker | Setup | Thesis | Invalidation | Risk notes | Follow-up |
|---|---|---|---|---|---|
| None supplied | No validated candidate | No ticker-level setup can be formed from the supplied synthetic observations | N/A | Completed-close regime data is stale; earnings movers and economic calendar are unavailable; one direct screen failed authentication | Obtain fresh market dashboard, economic calendar, earnings movers, and validated screens before considering candidates |

## 6. Human next actions

- Verify a fresh economic calendar before the open; do not assume absence of high-impact events.
- Refresh completed-close breadth/uptrend data for expected session 2026-11-16.
- Review fresh pre-market earnings movers and company-level reactions if available from the trading platform.
- Investigate FINVIZ Elite authentication for the failed direct screen.
- Keep any ticker decisions gated behind manual chart review and updated risk posture.

## 7. Data freshness and degraded mode

### Dashboard
Status: stale
- Observation date: 2026-03-27.
- Expected observation date: 2026-11-16.
- Source: uptrend-analyzer / public dashboard -> upstream Finviz collection.
- Impact: Completed-close breadth/uptrend dashboard is stale versus expected completed session 2026-11-16. Current market regime, breadth, uptrend participation, and exposure posture are degraded. Freshness basis: basis.kind=completed-close; expected_session=2026-11-16; retrieved_at=2026-11-17T06:00:00-08:00.

### Failed Elite
Status: unavailable
- Observation date: unknown.
- Expected observation date: 2026-11-17.
- Source: theme-detector / direct FINVIZ Elite screen A.
- Failure: authentication_failure; schema_valid=false.
- Impact: This direct theme screen cannot support current-morning theme candidates or rankings. Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00.

### Empty Elite
Status: valid_empty
- Observation date: 2026-11-17.
- Expected observation date: 2026-11-17.
- Source: theme-detector / direct FINVIZ Elite screen B.
- Result: 0 validated rows.
- Impact: Successful schema-validated current-morning screen returned no rows; this is not a missing-data condition by itself. Freshness basis: basis.kind=timestamp; observation_timestamp=2026-11-17T05:55:00-08:00; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00.

### Morning news
Status: fresh
- Observation date: 2026-11-17.
- Expected observation date: 2026-11-17.
- Source: market-news-analyst / synthetic timestamped news.
- Headline: Synthetic company research update; no trade recommendation.
- Impact: Fresh synthetic timestamped news is available, but it does not provide a trade recommendation or enough ticker-level setup detail for watchlist inclusion. Freshness basis: basis.kind=timestamp; observation_timestamp=2026-11-17T05:55:00-08:00; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00.

### Earnings calendar
Status: fresh
- Observation date: 2026-11-17.
- Expected observation date: 2026-11-17.
- Source: earnings-calendar / synthetic local event calendar.
- Coverage: 2026-11-17 through 2026-11-20.
- Event dates supplied: 2026-11-18, 2026-11-19.
- Impact: Earnings-calendar coverage is fresh for the requested window, but no company-level release names, surprise data, guidance, or pre-market reactions were supplied. Freshness basis: basis.kind=event-calendar; event_domain=earnings; requested_start=2026-11-17; requested_end=2026-11-20; verified_as_of=2026-11-17T05:55:00-08:00; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00.

### Economic calendar
Status: unavailable
- Observation date: unknown.
- Expected observation date: 2026-11-17.
- Source: not supplied in synthetic fixture; upstream skill not executed.
- Impact: Economic-calendar availability is unavailable; high-impact macro events today, this week, and around the market open remain unknown. Freshness basis: basis.kind=event-calendar; event_domain=economic; requested_start=2026-11-17; requested_end=2026-11-20; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-16 | stale | Freshness basis: basis.kind=completed-close; expected_session=2026-11-16; retrieved_at=2026-11-17T06:00:00-08:00. Observation predates expected completed session; breadth/uptrend posture is degraded and cannot establish a fresh regime change. Next step: refresh dashboard/current completed-close data. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown | 2026-11-17 | unavailable | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00. Authentication failure and invalid schema; screen cannot support theme candidates. Next step: fix FINVIZ Elite authentication or use validated fallback. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | valid_empty | Freshness basis: basis.kind=timestamp; observation_timestamp=2026-11-17T05:55:00-08:00; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00. 0 validated rows; valid empty screen, not a data failure. |
| Morning news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis: basis.kind=timestamp; observation_timestamp=2026-11-17T05:55:00-08:00; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00. Fresh synthetic company research update; no trade recommendation and insufficient setup detail for a candidate. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis: basis.kind=event-calendar; event_domain=earnings; requested_start=2026-11-17; requested_end=2026-11-20; verified_as_of=2026-11-17T05:55:00-08:00; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; retrieved_at=2026-11-17T06:00:00-08:00. Coverage includes event dates 2026-11-18 and 2026-11-19; no company-level movers supplied. |
| Economic calendar | not supplied in synthetic fixture; upstream skill not executed | unknown | unknown | 2026-11-17 | unavailable | Freshness basis: basis.kind=event-calendar; event_domain=economic; requested_start=2026-11-17; requested_end=2026-11-20; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy. Economic/high-impact macro events are unknown, not none. Next step: collect a dated economic-calendar source before market open. |
