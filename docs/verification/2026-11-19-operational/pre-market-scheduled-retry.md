

# Pre-market routine — 2026-11-17

Session state: normal session day.
Posture basis: pending fresh data / degraded — no valid completed-close posture for expected 2026-11-16; supplied dashboard observation date is 2026-03-27 and all other regime inputs are unavailable in this synthetic run.

**Risk posture:** research-only
**Primary reason:** The only completed-close dashboard input is stale versus the expected 2026-11-16 session, while economic calendar, distribution/top-risk, earnings movers, and exposure synthesis inputs were not supplied or executed.

Synthetic acceptance run: using only supplied observations; no tools, browsing, fetching, file changes, or execution were performed. Supplied upstream skills were not executed.

## 1. Macro calendar

### Earnings calendar
Status: fresh
- Facts supplied: synthetic earnings event calendar verified as of 2026-11-17T05:55:00-08:00, coverage window 2026-11-17 to 2026-11-20, event dates supplied for 2026-11-18 and 2026-11-19.
- High-impact events today: no ticker, timing, or impact metadata supplied; cannot classify as high-impact.
- High-impact events this week: earnings dates exist on 2026-11-18 and 2026-11-19, but company-level details are unavailable.
- Event risk around market open: unknown from supplied data.

### Economic calendar
Status: unavailable
- Economic-calendar availability is separate from earnings-calendar availability.
- No economic-calendar observation was supplied; high-impact macro events today/this week are unknown, not “none.”
- Degraded consequence: pre-market event-risk assessment is incomplete until a fresh economic calendar is verified.

## 2. Market regime

### Dashboard
Status: stale
- Breadth: stale dashboard observation date 2026-03-27 versus expected completed session 2026-11-16; cannot establish a fresh breadth regime.
- Uptrend participation: unavailable for current session basis; dashboard input is stale.
- Distribution and top-risk signals: unavailable; market-top-detector and IBD distribution-day monitor were not supplied/executed.
- Exposure posture: research-only; exposure-coach was not supplied/executed and cannot synthesize a ceiling from missing/stale upstream inputs.

**Synthesis:** No fresh regime change should be inferred. Treat any stock-specific research as pending confirmation from fresh completed-close breadth/uptrend and distribution data.

## 3. Earnings movers

### Earnings calendar
Status: fresh
- Calendar coverage is fresh for synthetic event-calendar purposes, but it contains only event dates, not reporting tickers, estimates, or timing.
- Major gap-up and gap-down reactions: unavailable; no earnings-trade-analyzer output, live quotes, or post-earnings movers were supplied.
- PEAD and watchlist candidates: unavailable; PEAD screener was not supplied/executed.
- Names requiring manual chart review: none can be named from supplied data.

**Degraded consequence:** Earnings section is calendar-aware only, not reaction-aware. Any earnings-mover shortlist requires fresh post-earnings price/volume confirmation.

## 4. Themes and sectors

### Failed Elite
Status: unavailable
- Direct FINVIZ Elite screen A failed authentication and schema validation.
- Impact: this screen cannot support theme/sector strength, weakness, or candidate ranking.
- Recovery: verify FINVIZ Elite authentication outside this synthetic run before using this screen.

### Empty Elite
Status: valid_empty
- Direct FINVIZ Elite screen B succeeded with schema validation and 0 validated rows at 2026-11-17T05:55:00-08:00.
- Impact: this is a valid empty screen, not a failure; it provides no candidates from that specific screen.

### Morning news
Status: fresh
- Synthetic timestamped news headline supplied: “Synthetic company research update; no trade recommendation.”
- Impact: current within the synthetic timestamp policy, but no ticker, sector, or tradable setup was supplied.

- Themes showing strength: unavailable from supplied data.
- Themes showing weakness: unavailable from supplied data.
- Contradictory signals: valid empty Elite screen B versus authentication failure in Elite screen A; stale dashboard prevents broad confirmation.

## 5. Watchlist candidates

No validated ticker candidates were produced from the supplied observations.

| Ticker | Setup | Thesis | Invalidation | Risk notes | Follow-up |
|---|---|---|---|---|---|
| — | No validated setup | No supplied ticker-level price/volume, earnings reaction, PEAD, or theme-leadership data | Any candidate requires fresh chart and data confirmation | Research-only posture; stale regime input and missing macro/economic calendar | Re-run with fresh regime, economic calendar, earnings movers, and authenticated screens |

## 6. Human next actions

- Verify a fresh economic calendar before assessing open-risk around macro events.
- Re-run completed-close regime inputs for the expected 2026-11-16 session before changing exposure assumptions.
- Review the synthetic earnings calendar dates 2026-11-18 and 2026-11-19 once ticker-level details are available.
- Investigate FINVIZ Elite authentication for screen A; treat screen B as a valid 0-row result.
- Keep any ticker research in watchlist/manual-review mode until fresh price, volume, and event data confirm a setup.

## 7. Data freshness and degraded mode

- Controlled synthetic acceptance run; no live tools or upstream skills were executed.
- All non-supplied inputs are unavailable by instruction.
- No actual API-key environment was checked. The fixture reports an authentication failure for one FINVIZ Elite screen; do not infer which credential is missing from this run alone.
- Stale warning: dashboard/uptrend observation date 2026-03-27 predates expected completed session 2026-11-16, so it cannot establish current posture.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-16 | stale | Freshness basis: basis.kind=completed-close; expected_session=2026-11-16; Retrieved at 2026-11-17T06:00:00-08:00; coverage partial; observation predates expected completed close, so breadth/uptrend posture is degraded and research-only pending fresh dashboard data. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown | 2026-11-17 | unavailable | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; Retrieved at 2026-11-17T06:00:00-08:00; authentication_failure and schema_valid=false, so this screen cannot support themes, sectors, or candidates; verify FINVIZ Elite authentication. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | valid_empty | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; observation_timestamp=2026-11-17T05:55:00-08:00; Retrieved at 2026-11-17T06:00:00-08:00; 0 validated rows, so no candidates from this screen but no degradation from this screen alone. |
| Morning news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; observation_timestamp=2026-11-17T05:55:00-08:00; Retrieved at 2026-11-17T06:00:00-08:00; headline supplied was synthetic company research update with no trade recommendation; no ticker-level action inferred. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17 | 2026-11-17 | fresh | Freshness basis: basis.kind=event-calendar; event_domain=earnings; requested coverage window=2026-11-17 to 2026-11-20; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; verified_as_of=2026-11-17T05:55:00-08:00; Retrieved at 2026-11-17T06:00:00-08:00; event dates supplied for 2026-11-18 and 2026-11-19 but no ticker/timing details. |
| Economic calendar | economic-calendar-fetcher / unavailable in synthetic acceptance run | unknown | unknown | 2026-11-17 | unavailable | Freshness basis: basis.kind=event-calendar; event_domain=economic; requested coverage window=2026-11-17 to 2026-11-20; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; no observation supplied and skill not executed, so high-impact macro events are unknown; fetch fresh economic calendar before open-risk decisions. |
| Distribution and top-risk signals | market-top-detector + ibd-distribution-day-monitor / unavailable in synthetic acceptance run | unknown | unknown | 2026-11-16 | unavailable | Freshness basis: basis.kind=completed-close; expected_session=2026-11-16; Retrieved at 2026-11-17T06:00:00-08:00; no distribution-day/top-risk output supplied and skills not executed, so top-risk assessment is unavailable; rerun with required data before exposure changes. |
| Earnings movers and PEAD | earnings-trade-analyzer + pead-screener / unavailable in synthetic acceptance run | unknown | unknown | 2026-11-17 | unavailable | Freshness basis: basis.kind=timestamp; run_cutoff=2026-11-17T06:00:00-08:00; max_age_minutes=30; policy_source=synthetic acceptance policy; no post-earnings reaction or PEAD output supplied and skills not executed, so no gap-up/gap-down candidates can be validated. |
| Exposure posture | exposure-coach / unavailable in synthetic acceptance run | unknown | unknown | 2026-11-16 | unavailable | Freshness basis: basis.kind=completed-close; expected_session=2026-11-16; Retrieved at 2026-11-17T06:00:00-08:00; exposure synthesis not executed and critical upstream inputs are stale/unavailable, so posture remains research-only pending fresh inputs. |
