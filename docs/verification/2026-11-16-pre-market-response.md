
# Pre-market routine — 2026-11-16

Session state: normal session day.
Posture basis: carried forward from 2026-11-13 — Monday pre-market posture is propagated from the most recent completed regular-session close after a weekend bridge, not presented as a fresh regime change.

**Risk posture:** research-only
**Primary reason:** Overall uptrend participation is weak and declining on the carried-forward 2026-11-13 close, while macro, earnings, top-risk, exposure, and theme inputs were not executed in this rendering run.

## 1. Macro calendar
- **High-impact events today:** unavailable — macro calendar was not fetched in this isolated rendering run.
- **High-impact events this week:** unavailable — no economic-calendar input was executed or supplied.
- **Event risk around market open:** pending confirmation. Treat event-risk conclusions as degraded until a current economic calendar is fetched and verified.

## 2. Market regime
- **Breadth:** degraded / partial. Overall uptrend participation from the supplied dashboard snapshot was **626 / 2775**, ratio **0.22558558558558559**, 10-period MA **0.2314838414262527**, slope **-0.005173437141907211**, trend **down**. Status: **carried_forward**, observation date **2026-11-13**.
- **Uptrend participation:** weak and declining on the carried-forward latest completed close. This supports a defensive research posture, but not a fresh Monday regime change because the basis crossed a weekend.
- **Distribution and top-risk signals:** unavailable — full market-top detector and IBD distribution-day monitor were not executed in this run.
- **Exposure posture:** research-only pending confirmation. Exposure Coach was not executed, so no validated exposure ceiling is available.

## 3. Earnings movers
- **Major gap-up and gap-down reactions:** unavailable — earnings calendar and post-earnings reaction scans were not fetched or executed.
- **PEAD and watchlist candidates:** unavailable — no scored earnings-trade-analyzer JSON or PEAD screener output was supplied.
- **Names requiring manual chart review:** none validated from this run. Any earnings-related review should wait for a fresh earnings calendar, gap list, and chart confirmation.

## 4. Themes and sectors
- **Themes showing strength:** unavailable — theme ranking was not executed.
- **Themes showing weakness:** unavailable — theme ranking was not executed.
- **Contradictory signals:** sector summary exists only with **unknown** observation date; do not borrow the overall uptrend timeseries date for sector heatmap conclusions. Theme/sector conclusions remain degraded and research-only.

## 5. Watchlist candidates

| Ticker | Setup | Thesis | Invalidation | Risk notes | Follow-up |
|---|---|---|---|---|---|
| None validated | No fresh candidate screen | Candidate generation is blocked because earnings, theme, sector, and exposure inputs were unavailable or unknown in this rendering run. | Any unverified ticker thesis is invalid until supported by fresh source data and chart review. | Weak carried-forward participation plus missing top-risk/exposure inputs increases false-positive risk. | Human reviewer should fetch current macro, earnings, PEAD, theme, and exposure inputs before adding names to an actionable watchlist. |

## 6. Human next actions
- Confirm today’s macro calendar and any market-open event risk before making intraday plans.
- Run fresh earnings calendar, earnings-mover, and PEAD screens before reviewing post-earnings names.
- Run market-top / distribution-day and Exposure Coach inputs before setting any exposure ceiling.
- Treat the weak 2026-11-13 uptrend participation as a caution flag, not a standalone trading signal.
- Keep all candidate work in research/watchlist mode until fresh inputs are verified.

## 7. Data freshness and degraded mode
- This was a **historical pre-market replay** for **2026-11-16 06:00 America/Los_Angeles**.
- No new market-data fetches or tool actions were performed in this model run.
- Credentials were not checked by the model; unexecuted analyses are reported as **not executed / unavailable**, not as missing-key failures.
- Latest completed regular-session close expected for posture: **2026-11-13**, carried across the weekend into Monday pre-market.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Session calendar / posture basis | Supplied verification calendar | unknown | 2026-11-16 | 2026-11-16 | fresh | Calendar indicates 2026-11-16 is a normal session day and 2026-11-13 is the latest completed regular-session close before the Monday pre-market run. |
| Overall uptrend participation | Finviz -> uptrend-dashboard CSV -> uptrend-analyzer | d604308942bc606523ff90dfeb9bcc727055ed3a clean | 2026-11-13 | 2026-11-13 | carried_forward | Participation facts are usable as weekend-carried posture basis: 626 / 2775, ratio 0.22558558558558559, MA 0.2314838414262527, slope -0.005173437141907211, trend down. |
| SPY latest completed close cross-check | FMP stable historical-price-eod/light -> validation harness | unknown | 2026-11-13 | 2026-11-13 | carried_forward | Independent SPY daily snapshot supports the latest completed close date; upstream skill consumer was not executed, so revision is unknown. |
| Sector summary / sector heatmap | Finviz -> uptrend-dashboard CSV -> uptrend-analyzer | d604308942bc606523ff90dfeb9bcc727055ed3a clean | unknown | 2026-11-13 | unknown | Published sector summary has no per-row as-of dates. Do not borrow the overall timeseries date; sector conclusions remain degraded pending dated sector data. |
| FINVIZ migration comparison | FINVIZ Elite -> patched screener consumer validation | d604308942bc606523ff90dfeb9bcc727055ed3a clean | unknown | 2026-11-13 | unknown | Later validation showed matching ticker sets, but export had no verified session/as-of metadata and cannot establish pre-market candidates for this replay. |
| Macro calendar | economic-calendar-fetcher not executed | unknown | unknown | 2026-11-16 | unavailable | Economic events were not fetched in this run. Fetch current FMP economic calendar before assessing event risk. |
| Earnings calendar | earnings-calendar not executed | unknown | unknown | 2026-11-16 | unavailable | Earnings calendar was not fetched. Run a fresh calendar before naming reporting companies or expected reactions. |
| Earnings movers / 5-factor scoring | earnings-trade-analyzer not executed | unknown | unknown | 2026-11-16 | unavailable | No scored post-earnings candidates were produced. Do not infer gap-up/gap-down movers from this run. |
| PEAD candidates | pead-screener not executed | unknown | unknown | 2026-11-16 | unavailable | No PEAD Mode B or Mode A output was supplied. PEAD watchlist remains pending fresh screened input. |
| Distribution / top-risk signals | market-top-detector and ibd-distribution-day-monitor not executed | unknown | unknown | 2026-11-13 | unavailable | Top-risk and distribution conclusions are unavailable. Run these before increasing conviction in risk posture. |
| Exposure synthesis | exposure-coach not executed | unknown | unknown | 2026-11-13 | unavailable | No validated exposure ceiling or recommendation was generated. Posture remains research-only. |
| Themes and sectors | theme-detector not executed; sector summary undated | unknown | unknown | 2026-11-13 | unavailable | No fresh theme ranking or dated sector confirmation is available. Keep theme conclusions pending confirmation. |
| Portfolio / open trades | No portfolio artifact supplied | unknown | unknown | 2026-11-16 | unavailable | No holdings, risk, or open-trade review was possible. Human reviewer must reconcile positions separately. |

**Human decision gate:** This brief is research and process support only. The human reviewer makes all entry, exit, sizing, and risk decisions after confirming fresh data.
