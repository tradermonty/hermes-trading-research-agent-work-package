

# After-close review — 2026-11-17

**Risk posture change:** unknown
**Primary reason:** Synthetic after-close review used only supplied observations; the only completed-close dashboard input is stale versus the expected 2026-11-17 session, so no fresh regime change can be confirmed.

Synthetic acceptance run: supplied upstream skills were **not executed**. No browsing, fetching, tools, file changes, or live data were used. All observations below are fixture-provided.

## 1. Market action summary

- **Indices:** Unavailable in this synthetic run. No index close, percent change, volume, or intraday reversal data was supplied.
- **Breadth:** Degraded. Dashboard input is **stale** with observation date 2026-03-27 versus expected completed session 2026-11-17.
- **Uptrend participation:** Research-only. The supplied Dashboard/uptrend-style source is stale, so it cannot establish today’s participation.
- **Distribution and top-risk changes:** Unavailable. No fresh distribution-day monitor, market-top detector, or index OHLCV data was supplied.

### Dashboard
Status: stale
- Impact: Cannot use this input to confirm current breadth, uptrend participation, or risk posture change for 2026-11-17.
- Recovery: Re-run the actual uptrend/dashboard workflow after close with fresh completed-close data.

## 2. Sector and theme rotation

- **Leading groups:** Not confirmed. No fresh sector rotation dataset was supplied.
- **Lagging groups:** Not confirmed.
- **Notable rotation:** Afternoon synthetic news was fresh but contained only a company research update and no trade recommendation. Direct FINVIZ Elite screen A failed authentication. Direct FINVIZ Elite screen B was valid but empty.

### Failed Elite
Status: unavailable
- Impact: Theme screen A cannot contribute to sector/theme ranking because the synthetic observation reports authentication failure.
- Recovery: Verify FINVIZ Elite credentials only in a real run if this screen is required.

### Empty Elite
Status: valid_empty
- Impact: Screen B returned 0 validated rows within the synthetic freshness window. This is not a failure, but it provides no candidates or themes.
- Recovery: Keep as a valid empty screen; do not infer broad absence of opportunities from this screen alone.

### Afternoon news
Status: fresh
- Impact: Fresh synthetic timestamped news only: “Synthetic company research update; no trade recommendation.” This supports no actionable sector or theme conclusion.
- Recovery: In a real run, execute the market-news workflow or provide timestamped news inputs.

## 3. Earnings reactions

- **Names worth tracking:** None supplied.
- **PEAD candidates:** None supplied; no post-earnings price/volume reaction data was provided.
- **Reactions that failed or reversed:** Unknown; no intraday or post-earnings reversal data was supplied.
- **Earnings calendar availability:** Fresh synthetic local earnings calendar is available for coverage window 2026-11-17 to 2026-11-20, with event dates 2026-11-18 and 2026-11-19.
- **Economic / macro calendar availability:** Unavailable separately. No economic-calendar input was supplied, so do not report “no macro events.”

### Earnings calendar
Status: fresh
- Impact: Earnings event calendar coverage is available, but no earnings-reaction scoring or PEAD analysis was supplied.
- Recovery: For a real review, run earnings-trade-analyzer or provide scored earnings reactions.

### Macro calendar
Status: unavailable
- Impact: Economic-calendar availability is not established in this synthetic run. Macro event risk remains unknown.
- Recovery: Provide a dated economic-calendar source or run an economic-calendar fetcher in a real workflow.

## 4. Open trade review checklist

Use this as a human review gate; no trade action is implied.

- **Thesis still valid?** Review each open thesis against today’s actual close only after fresh price/action data is available.
- **Invalidation hit?** Cannot confirm from supplied observations; no fresh ticker-level OHLCV was supplied.
- **Position risk still acceptable?** Treat as unknown until fresh index, breadth, and position-level data are reviewed.
- **Any overnight event risk?** Earnings calendar shows upcoming synthetic event dates on 2026-11-18 and 2026-11-19. Economic-calendar risk is unavailable.

## 5. Journal prompts

- What decision today deserves a note despite incomplete data?
- Did the process correctly avoid drawing conclusions from stale breadth data?
- Did any position require a manual thesis/invalidation review outside automated inputs?
- What should be avoided tomorrow: treating unavailable economic-calendar data as “no events.”
- What did the process do well: separated stale, unavailable, valid-empty, and fresh inputs.

## 6. Tomorrow preparation

- Re-run completed-close breadth/uptrend data and confirm whether 2026-11-17 observations are available.
- Verify any direct FINVIZ Elite authentication before relying on theme screens.
- Treat Screen B’s valid-empty result as narrow evidence only, not a market-wide conclusion.
- Review upcoming earnings dates from 2026-11-18 and 2026-11-19.
- Obtain a dated economic calendar before making overnight macro-risk assumptions.

## 7. Data freshness and degraded mode

Degraded-mode summary:
- This was a **controlled synthetic acceptance run**.
- Supplied upstream skills were **not executed**.
- All non-supplied inputs are unavailable.
- Fresh market regime cannot be confirmed because the only completed-close dashboard observation is stale.
- Economic-calendar availability is unavailable separately from the fresh synthetic earnings calendar.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-17 | stale | basis.kind=completed-close; expected_session=2026-11-17; Retrieved at 2026-11-17T16:00:00-08:00; Freshness basis: completed-close observation date 2026-03-27 predates expected completed session 2026-11-17; impact: cannot confirm current breadth/uptrend/risk posture; next step: rerun with fresh completed-close dashboard data. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown | 2026-11-17 | unavailable | basis.kind=timestamp; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; Retrieved at 2026-11-17T16:00:00-08:00; Freshness basis: authentication_failure with invalid schema; impact: screen unusable for theme detection; next step: verify FINVIZ Elite access in a real run. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | valid_empty | basis.kind=timestamp; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; observation_timestamp=2026-11-17T15:55:00-08:00; Retrieved at 2026-11-17T16:00:00-08:00; Freshness basis: schema-valid screen within 30 minutes returned 0 validated rows; impact: no candidates from this screen, no degradation by itself. |
| Afternoon news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | basis.kind=timestamp; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; observation_timestamp=2026-11-17T15:55:00-08:00; Retrieved at 2026-11-17T16:00:00-08:00; Freshness basis: timestamped synthetic news within 30 minutes; impact: headline only, “Synthetic company research update; no trade recommendation”; next step: use real news workflow for market-moving context. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | basis.kind=event-calendar; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; event_domain=earnings; requested_coverage=2026-11-17 to 2026-11-20; verified_as_of=2026-11-17T15:55:00-08:00; Retrieved at 2026-11-17T16:00:00-08:00; Freshness basis: verified synthetic earnings calendar covers requested window with event dates 2026-11-18 and 2026-11-19; impact: calendar available, but no reaction scoring supplied. |
| Macro calendar | not supplied / economic-calendar unavailable in synthetic acceptance run | unknown | unknown | 2026-11-17 | unavailable | basis.kind=event-calendar; run_cutoff=2026-11-17T16:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; event_domain=economic; requested_coverage=unknown; Retrieved at 2026-11-17T16:00:00-08:00; Freshness basis: no economic-calendar input supplied; impact: macro event risk unknown and must not be reported as none; next step: provide dated economic-calendar source in real run. |

**Human decision gate:** Review fresh market, position, and event data before making any entry, exit, add, trim, or hedge decision.
