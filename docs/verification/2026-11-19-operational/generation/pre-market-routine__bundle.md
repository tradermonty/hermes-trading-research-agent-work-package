Warning: Unknown toolsets: acceptance-no-tools
  ⚠ tirith security scanner enabled but not available — command scanning will use pattern matching only
# Pre-market routine — controlled synthetic acceptance run
Run cutoff: 2026-11-17T06:00:00-08:00
Mode: Synthetic fixture only. Supplied upstream skills were not executed. No tools, browsing, fetching, file writes, or live market data were used.

Session state: normal session day
Posture basis: pending fresh data / degraded — expected completed regular-session close is 2026-11-16, but supplied completed-close dashboard observation is 2026-03-27 and key breadth/regime inputs are unavailable.

Risk posture: risk-off / research-only
Primary reason: no fresh completed-close posture can be established; the only completed-close dashboard input is stale, and most breadth, distribution, macro, earnings-reaction, and theme inputs were not collected.

## 1. Market posture

### Dashboard
Status: stale

Facts:
- Supplied Dashboard source: uptrend-analyzer / public dashboard -> upstream Finviz collection.
- Observation date: 2026-03-27.
- Expected completed session: 2026-11-16.
- Coverage note: partial; current dates for other rows unavailable.
- No fresh uptrend score, sector participation score, or exposure ceiling was supplied.

Model / skill output:
- Uptrend-analyzer was not executed in this run.
- The supplied dashboard fixture is stale relative to the expected completed session.

Synthesis:
- Market posture cannot be upgraded to risk-on or neutral from the supplied data.
- Treat regime conclusions as degraded and research-only.
- Missing fresh breadth data establishes no fresh regime change.

## 2. Macro calendar

### Economic calendar
Status: unavailable

Facts:
- No economic-calendar observation was supplied.
- economic-calendar-fetcher was not executed.
- Therefore high-impact macro events today and this week are unknown, not “none.”

Degraded consequence:
- Do not assume a clean macro tape.
- Event-risk sizing and holding decisions require a fresh economic-calendar check before any trade decision.

Recovery / setup step:
- Run economic-calendar-fetcher or provide a verified dated economic-calendar source covering 2026-11-17 through the desired weekly window.

### Earnings calendar
Status: fresh

Facts:
- Supplied earnings calendar verified_as_of: 2026-11-17T05:55:00-08:00.
- Coverage window: 2026-11-17 to 2026-11-20.
- Event dates supplied: 2026-11-18 and 2026-11-19.
- No company-level tickers, estimates, or timing details were supplied.

Model / skill output:
- earnings-calendar was not executed; fixture data only.

Synthesis:
- Earnings-calendar availability is fresh for the requested fixture window, but it is event-date-only.
- Earnings risk exists on 2026-11-18 and 2026-11-19, but no ticker-level earnings candidates can be named from this fixture.

## 3. Earnings movers

### Earnings calendar
Status: fresh

Facts:
- Fresh synthetic local event-calendar coverage exists for 2026-11-17 through 2026-11-20.
- Supplied event dates: 2026-11-18 and 2026-11-19.

Unavailable inputs:
- earnings-trade-analyzer was not executed.
- pead-screener was not executed.
- No earnings-reaction list, gap size, volume, grade, PEAD stage, or post-earnings drift screen was supplied.

Synthesis:
- No large earnings movers can be identified from the supplied observations.
- No PEAD/watchlist candidates are confirmed.
- Any earnings-reaction work remains pending a fresh post-earnings screen.

## 4. Breadth and uptrend participation

### Dashboard
Status: stale

Facts:
- Observation date: 2026-03-27.
- Expected observation date: 2026-11-16.
- The dashboard is stale and partial.

Unavailable inputs:
- market-breadth-analyzer was not supplied.
- IBD distribution-day monitor was not supplied.
- market-top-detector was not supplied.
- exposure-coach was not supplied.

Synthesis:
- Breadth and uptrend participation are unavailable for a fresh 2026-11-17 pre-market decision.
- No fresh exposure ceiling can be calculated.
- No conclusion about broadening, narrowing, distribution-day risk, or top risk should be drawn from this run.

## 5. Sectors/themes worth watching

### Failed Elite
Status: unavailable

Facts:
- Source: theme-detector / direct FINVIZ Elite screen A.
- Fetch result: authentication_failure.
- Schema valid: false.
- Observation date: unknown.

Degraded consequence:
- Direct FINVIZ Elite screen A cannot support fresh sector/theme conclusions.
- This is unavailable, not a zero-candidate result.

Recovery / setup step:
- Verify FINVIZ Elite authentication before using this screen in a live routine.

### Empty Elite
Status: valid_empty

Facts:
- Source: theme-detector / direct FINVIZ Elite screen B.
- Fetch result: success.
- Schema valid: true.
- Row count: 0.
- Observation timestamp: 2026-11-17T05:55:00-08:00.
- Run cutoff: 2026-11-17T06:00:00-08:00.
- Timing policy: max_age_minutes 30, synthetic acceptance policy.

Model / skill output:
- The screen is a valid empty result: 0 validated rows.
- theme-detector was not executed beyond the supplied fixture.

Synthesis:
- Screen B produced no validated theme rows, but this alone does not degrade the whole brief.
- Because Screen A failed and full theme detection was not executed, no ranked sector/theme leadership list is available.

### Morning news
Status: fresh

Facts:
- Source: market-news-analyst / synthetic timestamped news.
- Observation timestamp: 2026-11-17T05:55:00-08:00.
- Headline: “Synthetic company research update; no trade recommendation.”

Synthesis:
- The fresh news item is generic and contains no ticker, sector, or tradable theme.
- It does not support a watchlist candidate.

## 6. Watchlist candidates with thesis, invalidation, and required follow-up

No confirmed watchlist candidates from supplied observations.

Reason:
- No ticker-level earnings movers were supplied.
- No fresh breadth/uptrend posture was supplied.
- No fresh theme ranking was supplied.
- The only fresh news headline is generic and explicitly states no trade recommendation.
- Empty Elite screen B returned 0 validated rows.
- Failed Elite screen A is unavailable due to authentication_failure.

Candidate queue:
| Ticker | Company | Setup type | Skill/data source | Thesis | Invalidation | Risk notes | Follow-up required | Next human action |
|---|---|---|---|---|---|---|---|---|
| None | None | None | Synthetic fixture only | No ticker-level candidate supported by supplied observations | Any candidate would require unsupported inference | Stale regime data; macro unknown; earnings reactions unavailable | Run fresh breadth/uptrend, economic calendar, earnings reaction, and theme screens | Human reviewer should withhold candidate escalation until fresh confirmation |

/trade-ticket readiness:
- No candidate is ready for /trade-ticket.
- If future candidates are confirmed, include source_bundle: pre-market-routine and a stable source_candidate_ref such as TICKER-2026-11-17-setup.

## 7. Risk gate

Risk gate: no new trades / research-only

Rationale:
- Completed-close posture is degraded because the supplied dashboard observation is stale versus expected_session 2026-11-16.
- Economic calendar is unavailable; high-impact macro events are unknown.
- Earnings calendar is fresh only at event-date coverage level, with no ticker details.
- Earnings movers and PEAD screens are unavailable.
- Theme screen A failed authentication; theme screen B is valid_empty.
- Fresh news is generic and non-actionable.

Human decision gate:
- The human reviewer makes all entry and exit decisions.
- This synthetic bundle does not place orders and does not provide buy/sell instructions.
- Before considering new exposure, the reviewer should obtain fresh completed-close regime/breadth data, a dated economic calendar, and ticker-level candidate confirmation.

## 8. Data freshness and missing-data warnings

Synthetic data notice:
- This was a controlled synthetic acceptance run.
- Only supplied observations were used.
- Supplied upstream skills were not executed.
- All non-supplied inputs are unavailable for this brief.

### Dashboard
Status: stale
- Observation date: 2026-03-27.
- Expected observation date: 2026-11-16.
- Impact: stale completed-close dashboard cannot establish a fresh market posture or fresh uptrend participation.

### Failed Elite
Status: unavailable
- Observation date: unknown.
- Expected observation date: 2026-11-17.
- Impact: authentication_failure; unavailable theme input, not a valid empty result.

### Empty Elite
Status: valid_empty
- Observation date: 2026-11-17.
- Expected observation date: 2026-11-17.
- Impact: successful schema-valid timestamped screen returned 0 validated rows.

### Morning news
Status: fresh
- Observation date: 2026-11-17.
- Expected observation date: 2026-11-17.
- Impact: fresh synthetic timestamped headline, but no ticker-level candidate.

### Earnings calendar
Status: fresh
- Observation date: 2026-11-17.
- Expected observation date: 2026-11-17.
- Impact: fresh event-calendar coverage for earnings, but only event dates were supplied.

### Economic calendar
Status: unavailable
- Observation date: unknown.
- Expected observation date: 2026-11-17.
- Impact: no supplied economic-calendar source and economic-calendar-fetcher not executed; macro events unknown.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-16 | stale | Freshness basis basis.kind=completed-close expected_session=2026-11-16. Retrieved at 2026-11-17T06:00:00-08:00. Stale versus expected completed regular session; coverage partial; cannot establish fresh posture or fresh uptrend participation. Next step: rerun/verify dashboard with 2026-11-16 observation before using for exposure. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown | 2026-11-17 | unavailable | Freshness basis basis.kind=timestamp run_cutoff=2026-11-17T06:00:00-08:00 max_age_minutes=30 policy_source=synthetic acceptance policy. Retrieved at 2026-11-17T06:00:00-08:00. Authentication failure and invalid schema; unavailable, not zero candidates. Next step: verify FINVIZ Elite authentication before relying on screen A. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | valid_empty | Freshness basis basis.kind=timestamp run_cutoff=2026-11-17T06:00:00-08:00 max_age_minutes=30 policy_source=synthetic acceptance policy. Observation timestamp 2026-11-17T05:55:00-08:00. Retrieved at 2026-11-17T06:00:00-08:00. 0 validated rows; valid empty screen does not by itself degrade the brief. |
| Morning news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis basis.kind=timestamp run_cutoff=2026-11-17T06:00:00-08:00 max_age_minutes=30 policy_source=synthetic acceptance policy. Observation timestamp 2026-11-17T05:55:00-08:00. Retrieved at 2026-11-17T06:00:00-08:00. Headline supplied: Synthetic company research update; no trade recommendation. No ticker candidate generated. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis basis.kind=event-calendar event_domain=earnings requested_start=2026-11-17 requested_end=2026-11-20 run_cutoff=2026-11-17T06:00:00-08:00 max_age_minutes=30 policy_source=synthetic acceptance policy. Verified as of 2026-11-17T05:55:00-08:00. Retrieved at 2026-11-17T06:00:00-08:00. Coverage includes event dates 2026-11-18 and 2026-11-19; no ticker-level details supplied. |
| Economic calendar | economic-calendar-fetcher / not supplied; upstream skill not executed | unknown | unknown | 2026-11-17 | unavailable | Freshness basis basis.kind=event-calendar event_domain=economic requested_start=2026-11-17 requested_end=2026-11-20 run_cutoff=2026-11-17T06:00:00-08:00 max_age_minutes=30 policy_source=synthetic acceptance policy. No supplied observation and skill not executed; high-impact macro events are unknown. Next step: fetch or provide a verified dated economic-calendar source. |
