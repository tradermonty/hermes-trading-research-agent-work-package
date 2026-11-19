

# Pre-market routine — 2026-11-17

Session state: **normal session day** for the US cash market.
Posture basis: **pending fresh data / degraded** — expected latest completed regular-session close is **2026-11-16**, but the only supplied completed-close dashboard observation is **2026-03-27**; supplied upstream skills were **not executed** in this controlled synthetic run.

**Risk posture:** research-only
**Primary reason:** Completed-close market posture inputs are stale or unavailable, so new-entry conclusions require fresh confirmation before any human trading decision.

## 1. Macro calendar

- **Economic calendar availability:** unavailable in this synthetic run; no high-impact economic events can be confirmed for today or this week.
- **Earnings calendar availability:** fresh synthetic local earnings calendar verified as of **2026-11-17T05:55:00-08:00**, covering **2026-11-17 to 2026-11-20**, with event dates supplied for **2026-11-18** and **2026-11-19**.
- **High-impact events today:** unknown for economic events; no detailed earnings names/times supplied for today.
- **High-impact events this week:** unknown for economic events; earnings-calendar event dates exist on **2026-11-18** and **2026-11-19**, but no tickers or impact ranking were supplied.
- **Event risk around market open:** degraded / unknown. Do not infer a quiet open from missing economic-calendar data.

## 2. Market regime

- **Breadth:** degraded. The supplied dashboard observation date is **2026-03-27**, stale versus expected completed session **2026-11-16**.
- **Uptrend participation:** degraded. Uptrend dashboard data cannot establish a current regime change because the observation is stale.
- **Distribution and top-risk signals:** unavailable. No fresh market-top, IBD distribution-day, or distribution-count inputs were supplied.
- **Exposure posture:** research-only. Exposure Coach was not executed and critical upstream posture inputs are stale or unavailable.

## 3. Earnings movers

- **Major gap-up and gap-down reactions:** unavailable. No earnings-trade-analyzer output, live/pre-market quote data, or gap screen was supplied.
- **PEAD and watchlist candidates:** unavailable. PEAD screener was not executed, and no earnings-reaction candidate JSON was supplied.
- **Names requiring manual chart review:** none supplied. Earnings calendar confirms only that synthetic earnings events exist on **2026-11-18** and **2026-11-19**; ticker-level review cannot be generated from the provided data.

## 4. Themes and sectors

- **Themes showing strength:** none validated. One FINVIZ Elite screen failed authentication, and one validated Elite screen returned **0 rows** as of **2026-11-17T05:55:00-08:00**.
- **Themes showing weakness:** none validated from supplied data.
- **Contradictory signals:** fresh timestamped synthetic news exists, but it contains only a generic company research update and no actionable ticker/theme detail. Theme conclusions remain degraded.

## 5. Watchlist candidates

| Ticker | Setup | Thesis | Invalidation | Risk notes | Follow-up |
|---|---|---|---|---|---|
| None supplied | Research-only / no validated candidate | No ticker-level earnings, theme, PEAD, or gap-mover candidate was supplied in the synthetic input set. | Any candidate generated without fresh ticker-level data is invalid for this run. | Market regime inputs are stale/unavailable; avoid treating this as a clean candidate day. | Human reviewer should wait for fresh screens, live/pre-market movers, and chart confirmation before considering any setup. |

## 6. Human next actions

- Confirm fresh market breadth / uptrend dashboard data for **2026-11-16** before changing exposure posture.
- Check the economic calendar from a fresh source before assuming no high-impact macro events.
- Review live/pre-market earnings movers manually if trading around the open.
- Re-run theme and earnings reaction workflows with valid credentials/data if candidates are needed.
- Keep all new ideas in **research-only** status until fresh regime and ticker-level confirmation are available.

## 7. Data freshness and degraded mode

This is a **controlled synthetic acceptance run**. Only the supplied observations were used. No tools, browsing, fetching, file changes, or script execution occurred. Supplied upstream skills were **not executed**; the provenance below reflects fixture-provided observations only.

### Dashboard

Status: **stale**

- Observation date **2026-03-27** is older than expected completed regular-session close **2026-11-16**.
- Impact: current breadth/uptrend posture cannot be inferred from this dashboard.

### Failed Elite

Status: **unavailable**

- Direct FINVIZ Elite screen failed authentication.
- Impact: theme/sector screen A cannot contribute to strength/weakness conclusions.

### Empty Elite

Status: **valid_empty**

- Valid schema and successful fetch with **0 validated rows** as of **2026-11-17T05:55:00-08:00**.
- Impact: this specific screen produced no candidates, but it does not validate the broader theme universe.

### Morning news

Status: **fresh**

- Synthetic timestamped news observed at **2026-11-17T05:55:00-08:00**.
- Impact: headline was generic and did not provide ticker-level trade candidates.

### Earnings calendar

Status: **fresh**

- Synthetic local earnings calendar verified as of **2026-11-17T05:55:00-08:00**.
- Impact: earnings event dates were supplied, but no tickers, timing, or estimated impact were provided.

### Economic calendar

Status: **unavailable**

- No economic-calendar observation was supplied.
- Impact: high-impact macro events today/this week are unknown; this section is degraded.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-16 | stale | basis.kind=completed-close; expected_session=2026-11-16; Retrieved at=2026-11-17T06:00:00-08:00; Freshness basis: completed-close posture requires latest completed regular session; supplied observation is stale and partial, so breadth/uptrend posture is research-only pending fresh dashboard data. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown | 2026-11-17 | unavailable | basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; Retrieved at=2026-11-17T06:00:00-08:00; authentication_failure means this theme screen cannot support sector/theme conclusions; fix FINVIZ Elite authentication before reuse. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | valid_empty | basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; observation_timestamp=2026-11-17T05:55:00-08:00; Retrieved at=2026-11-17T06:00:00-08:00; Freshness basis met with 0 validated rows, so no candidates from this screen only. |
| Morning news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; observation_timestamp=2026-11-17T05:55:00-08:00; Retrieved at=2026-11-17T06:00:00-08:00; headline was “Synthetic company research update; no trade recommendation,” so no ticker-level setup generated. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | basis.kind=event-calendar; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; event_domain=earnings; requested coverage window=2026-11-17 to 2026-11-20; verified_as_of=2026-11-17T05:55:00-08:00; Retrieved at=2026-11-17T06:00:00-08:00; event dates supplied for 2026-11-18 and 2026-11-19, but ticker details are unavailable. |
| Economic calendar | economic-calendar-fetcher / not supplied in synthetic run | unknown | unknown | 2026-11-17 | unavailable | basis.kind=event-calendar; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; event_domain=economic; requested coverage window=2026-11-17 to 2026-11-20; no verified-as-of timestamp supplied; high-impact macro events remain unknown until a fresh economic-calendar source is available. |
| Earnings movers / PEAD | earnings-trade-analyzer + pead-screener / not supplied in synthetic run | unknown | unknown | 2026-11-17 | unavailable | basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; no gap/reaction screen or PEAD candidate file supplied; earnings mover conclusions are unavailable. |
| Distribution and top-risk | market-top-detector + ibd-distribution-day-monitor / not supplied in synthetic run | unknown | unknown | 2026-11-16 | unavailable | basis.kind=completed-close; expected_session=2026-11-16; no completed-close distribution/top-risk reports supplied; top-risk and distribution-day posture cannot be assessed. |
| Exposure posture | exposure-coach / not supplied in synthetic run | unknown | unknown | 2026-11-16 | unavailable | basis.kind=completed-close; expected_session=2026-11-16; Exposure Coach was not executed and upstream posture inputs are stale/unavailable; exposure ceiling remains research-only pending fresh inputs. |
