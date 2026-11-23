Warning: Unknown toolsets: acceptance-no-tools
# After-Close Review — US Equities — Synthetic Acceptance Run

Run cutoff: 2026-11-17T16:00:00-08:00
Calendar override: normal session day
Expected completed regular session: 2026-11-17

Important: This is a controlled synthetic acceptance run. Only the supplied observations were used. No tools, browsing, fetching, file writes, upstream skill execution, or live market-data collection were performed. Supplied upstream skills were not executed; the listed revision SHA values are fixture-provided.

Risk posture: research-only / unknown
Primary reason: completed-close breadth/uptrend dashboard data is stale, index/price/breadth/sector closes were not supplied, and earnings-reaction / signal / open-position observations were not supplied.

Human decision gate: No entries, exits, adds, reductions, or stop changes should be made from this synthetic brief alone. The human reviewer must confirm fresh market data, position state, earnings reactions, and risk posture before any trading action.

## 1. What changed today in indices, breadth, sectors, and themes

Facts from supplied observations:
- Dashboard completed-close observation date: 2026-03-27.
- Expected completed session: 2026-11-17.
- Failed Elite screen: authentication_failure; no schema-valid data.
- Empty Elite screen: successful, schema-valid, 0 rows, observation timestamp 2026-11-17T15:55:00-08:00.
- Afternoon news: one synthetic headline at 2026-11-17T15:55:00-08:00: "Synthetic company research update; no trade recommendation."
- Earnings calendar: synthetic earnings event-calendar verified as of 2026-11-17T15:55:00-08:00, covering 2026-11-17 through 2026-11-20, with event dates 2026-11-18 and 2026-11-19.

Skill/model output status:
- Indices: unavailable. No index close, percent change, volume, or intraday reversal data was supplied.
- Breadth/uptrend: stale. Dashboard observation is 2026-03-27 versus expected completed session 2026-11-17.
- Sectors: unavailable / not assessable. No fresh sector uptrend rows or sector performance observations were supplied.
- Themes:
  - Failed Elite: unavailable due to authentication failure.
  - Empty Elite: valid_empty for that screen only; 0 validated rows does not imply no themes existed elsewhere.
  - Afternoon news: fresh synthetic timestamped company research update, but no ticker, price reaction, or trade recommendation.

Synthesis:
- Today’s actual index change cannot be assessed.
- Fresh breadth/uptrend improvement or deterioration cannot be established.
- Sector rotation cannot be assessed.
- Theme-screen conclusions are degraded: one Elite screen failed, one Elite screen returned 0 validated rows, and the only fresh news item is synthetic and non-actionable.

### Dashboard
Status: stale

Observation date: 2026-03-27.
Impact: The uptrend/dashboard input predates the expected completed session 2026-11-17, so it cannot establish today’s breadth, trend participation, sector leadership, or risk posture. Recovery step: rerun the dashboard/uptrend collection against the latest completed session and verify row-level observation dates.

### Failed Elite
Status: unavailable

Observation date: unknown.
Impact: Direct FINVIZ Elite screen A failed with authentication_failure and schema_valid=false. This is unavailable, not a zero-result screen. Recovery step: verify FINVIZ Elite access/authentication for this screen, then rerun and validate schema before using it for theme conclusions.

### Empty Elite
Status: valid_empty

Observation date: 2026-11-17.
Impact: Direct FINVIZ Elite screen B succeeded with schema_valid=true and row_count=0 at 2026-11-17T15:55:00-08:00. This establishes 0 validated rows for this specific screen only. It does not establish that no themes, no setups, or no earnings reactions existed elsewhere.

### Afternoon news
Status: fresh

Observation date: 2026-11-17.
Impact: Synthetic timestamped news is fresh under the supplied 30-minute timestamp policy. It provides only one company-research headline and no ticker, market reaction, or trade recommendation. Treat as context only.

## 2. Breadth/uptrend improvement or deterioration

Facts:
- Dashboard source: uptrend-analyzer / public dashboard -> upstream Finviz collection.
- Observation date: 2026-03-27.
- Expected observation date: 2026-11-17.
- Status: stale.

Skill/model output:
- uptrend-analyzer was not executed.
- market-breadth-analyzer was not executed.
- market-top-detector was not executed.
- ibd-distribution-day-monitor was not executed.

Synthesis:
- Breadth/uptrend improvement: unknown.
- Breadth/uptrend deterioration: unknown.
- Distribution-day pressure: unknown.
- Market-top risk: unknown.
- Any exposure guidance based on breadth is research-only and pending fresh completed-close data.

Risk implication:
- Because fresh breadth data is missing/stale, the posture should remain research-only / unknown rather than risk-on.
- Missing breadth data does not establish no regime change.

## 3. Earnings reactions worth tracking

### Earnings calendar
Status: fresh

Facts:
- Source: earnings-calendar / synthetic local event calendar.
- Verified as of: 2026-11-17T15:55:00-08:00.
- Coverage window: 2026-11-17 to 2026-11-20.
- Event dates supplied: 2026-11-18 and 2026-11-19.
- Event domain: earnings.
- Status: fresh.

Macro calendar availability:
- Earnings-calendar availability: fresh for the supplied synthetic event-calendar coverage window.
- Economic-calendar availability: unavailable. No economic-calendar-fetcher result or separately dated economic-calendar source was supplied. Therefore high-impact macro events are unknown, not “none.”

Earnings-reaction observations:
- Not supplied.
- earnings-trade-analyzer was not executed.
- No post-earnings price gaps, volume reactions, grades, tickers, or PEAD candidates were supplied.

Synthesis:
- Earnings reactions worth tracking: unknown / not assessable from supplied data.
- The fresh earnings calendar only tells us that synthetic earnings events exist on 2026-11-18 and 2026-11-19 within the requested window.
- It does not identify which companies reported, how stocks reacted, or whether any reaction qualifies as a trade setup.

Follow-up data required:
- Company-level earnings calendar rows with ticker, timing, and report date.
- Post-report price/volume reaction after announcements.
- Fresh earnings-trade-analyzer scoring or equivalent validated manual review.
- Any human-maintained earnings watchlist.

## 4. Signals that improved, degraded, or invalidated

Facts:
- No signal observations were supplied.
- No open thesis state, edge-signal output, screener output, or postmortem records were supplied.
- signal-postmortem was not executed.
- trader-memory-core was not executed.

Skill/model output:
- Improved signals: unknown / not assessable.
- Degraded signals: unknown / not assessable.
- Invalidated signals: unknown / not assessable.

Synthesis:
- Do not conclude that no signals improved, no signals degraded, or nothing was invalidated.
- The absence of supplied signal observations means signal status cannot be assessed in this run.

Recovery step:
- Provide or fetch current signal/thesis records, prior signal baselines, current prices, stops/invalidation levels, and any new post-close observations.
- Then compare each signal against its thesis, invalidation condition, and market regime.

## 5. Open trade review checklist

Open-position data status: unavailable.
No account holdings, open trades, thesis YAML, broker export, or journal state was supplied.

Use this checklist manually after confirming real position data:

1. Position inventory
   - List all open positions, size, entry, current price, unrealized P&L, and exposure by sector/theme.
   - Confirm whether any position has earnings, guidance, FDA, legal, macro, or analyst-event risk within the next 1-5 sessions.

2. Thesis check
   - Is the original thesis still intact?
   - What changed today that supports the thesis?
   - What changed today that contradicts the thesis?
   - Did the stock close above/below key moving averages, pivot levels, or stop areas?

3. Invalidation check
   - Has price violated the pre-defined stop or thesis invalidation condition?
   - Has volume confirmed institutional selling or support?
   - Has the market regime degraded enough to require tighter risk?

4. Risk/exposure check
   - Total long exposure.
   - Leveraged exposure, if any.
   - Single-name concentration.
   - Sector/theme concentration.
   - Drawdown sensitivity if tomorrow gaps against the position.
   - Correlation risk among similar names.

5. Event-risk check
   - Earnings calendar: fresh synthetic earnings coverage exists for 2026-11-17 to 2026-11-20, but company-level rows are not supplied.
   - Economic calendar: unavailable; macro event risk is unknown.
   - News: only one synthetic company-research headline supplied; no ticker or reaction.

6. Human decision gate
   - The human reviewer decides whether any position needs action.
   - This synthetic brief does not authorize entries, exits, adds, trims, hedges, or stop changes.

## 6. Journal prompts for today’s decisions

Because actual trades and decisions were not supplied, use these prompts for manual journaling:

1. Market read
   - Did I treat today as risk-on, neutral, or defensive?
   - Was that view based on fresh data or stale/incomplete data?
   - Did I notice any conflict between price action and breadth?

2. Process quality
   - Did I make any decisions without a fresh market regime check?
   - Did I distinguish valid_empty screens from unavailable screens?
   - Did I avoid assuming “nothing happened” where data was missing?

3. Trade management
   - For each open position, did the thesis improve, degrade, or remain unchanged?
   - What is the exact invalidation level?
   - Did I move any stop? If yes, was it rules-based or emotional?

4. Earnings/event awareness
   - Did any holding have earnings or company-specific event risk?
   - Was the earnings calendar verified, and were company-level details checked?

5. Emotional/process notes
   - Did I chase, freeze, revenge trade, over-size, or ignore a stop?
   - What one behavior should be repeated tomorrow?
   - What one behavior should be avoided tomorrow?

6. Postmortem trigger
   - Which trades or signals need a 5-day or 20-day review?
   - Which decisions today should be revisited after the next close?

## 7. Tomorrow preparation list

Macro calendar:
- Economic calendar: unavailable. Do not assume no high-impact macro events.
- Earnings calendar: fresh synthetic event-calendar coverage for 2026-11-17 through 2026-11-20, with event dates 2026-11-18 and 2026-11-19.
- Action needed: obtain company-level earnings rows and an independently dated economic calendar before tomorrow’s pre-market plan.

Market data:
- Refresh index closes, index volume, and key ETF levels for SPY, QQQ, IWM, DIA if relevant.
- Refresh breadth/uptrend dashboard for expected completed session 2026-11-17.
- Refresh distribution-day status if using IBD-style risk management.
- Refresh sector rotation/uptrend data before drawing sector conclusions.

Screens/themes:
- Rerun Failed Elite screen after resolving authentication/access.
- Confirm Empty Elite screen remains valid if used tomorrow; today’s valid_empty result applies only to that specific screen at 2026-11-17T15:55:00-08:00.
- Do not infer broad theme absence from one valid_empty screen.

Earnings:
- Convert the fresh earnings-calendar window into a ticker-level watchlist.
- After reports occur, collect gap size, volume, relative strength, moving-average position, and guidance reaction.
- Label any candidates as research candidates until post-earnings reaction data is confirmed.

Open trades:
- Pull current holdings and compare each with thesis/invalidation.
- Identify positions with event risk through 2026-11-20.
- Prepare “if/then” scenarios, but leave all trading decisions to the human reviewer.

## 8. Data freshness and missing-data warnings

This report is synthetic and degraded. Only supplied observations were used. All other inputs are unavailable unless explicitly listed as fresh, stale, unavailable, or valid_empty below.

Missing / unavailable categories not established by supplied observations:
- Index closes and volume: unavailable.
- Fresh breadth composite: unavailable.
- Fresh uptrend dashboard for 2026-11-17: unavailable; supplied Dashboard is stale.
- Sector rotation rows: unavailable.
- Distribution-day monitor: unavailable.
- Market-top detector output: unavailable.
- Earnings reactions: unavailable / not assessable.
- Signal observations and baselines: unavailable / not assessable.
- Open positions and thesis state: unavailable.
- Economic calendar: unavailable.

Consequences:
- No fresh market-regime change can be concluded.
- No “no earnings reactions occurred” conclusion can be made.
- No “signals improved/degraded/invalidated” conclusion can be made.
- No open-trade action can be derived.
- Valid_empty applies only to Empty Elite screen B with 0 validated rows.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-17 | stale | Freshness basis: basis.kind=completed-close; expected_session=2026-11-17; Retrieved at 2026-11-17T16:00:00-08:00. Observation predates expected completed session; coverage is partial and current dates for other rows are unavailable. Cannot establish current breadth/uptrend, sector participation, or risk posture. Next step: rerun/refresh dashboard for 2026-11-17 and verify row-level observation dates. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown | 2026-11-17 | unavailable | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; Retrieved at 2026-11-17T16:00:00-08:00. Fetch failed with authentication_failure and schema_valid=false. This is unavailable, not a zero-result screen. Next step: verify FINVIZ Elite authentication/access and rerun schema validation. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | valid_empty | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; Observation timestamp 2026-11-17T15:55:00-08:00; Retrieved at 2026-11-17T16:00:00-08:00. Successful schema-validated screen returned 0 validated rows for this screen only. Does not imply no themes or no candidates elsewhere. |
| Afternoon news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; Observation timestamp 2026-11-17T15:55:00-08:00; Retrieved at 2026-11-17T16:00:00-08:00. Synthetic headline: "Synthetic company research update; no trade recommendation." Context only; no ticker, price reaction, or trade setup supplied. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis: basis.kind=event-calendar; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; event_domain=earnings; requested coverage window=2026-11-17 to 2026-11-20; Verified as of 2026-11-17T15:55:00-08:00; Retrieved at 2026-11-17T16:00:00-08:00. Event dates supplied: 2026-11-18 and 2026-11-19. Company-level rows and post-earnings reactions are not supplied; economic-calendar availability remains unavailable separately. |
