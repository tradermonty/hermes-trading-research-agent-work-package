
# After-close review — 2026-11-16

**Risk posture change:** unknown
**Primary reason:** Overall uptrend participation is fresh for 2026-11-16 and weak/down, but full distribution-day, market-top, earnings, sector-date, and portfolio inputs were not executed in this rendering run.

**Skills used or intended:** trading-research-orchestrator, trading-cron-brief-writer, uptrend-analyzer input rendering; market-top-detector, ibd-distribution-day-monitor, sector-analyst, earnings-trade-analyzer, trader-memory-core intended but not executed in this isolated verification run.
**Human decision gate:** Research-only / pending confirmation. The human reviewer makes all entry, exit, sizing, and overnight-risk decisions.

## 1. Market action summary

- **Indices:** Fresh independent SPY EOD row for 2026-11-16: price `739.95`, volume `69207282`. Broader index set was not fetched in this run, so index-level comparison is degraded.
- **Breadth:** Fresh overall uptrend-dashboard input for 2026-11-16: `508` of `2730`, ratio `0.18608058608058609`, 10MA `0.22475028429728994`, slope `-0.004619148338395801`, trend `down`.
- **Uptrend participation:** Participation remains narrow on the provided overall metric. This supports a defensive/research-only review stance until confirmed by the full regime stack.
- **Distribution and top-risk changes:** Full market-top-detector and IBD distribution-day monitor were not executed. No fresh distribution-day count, top-risk score, or exposure-coach synthesis is available from this run.

## 2. Sector and theme rotation

- **Leading groups:** Not confirmed. Sector summary was available only with unknown observation date, so leadership claims are degraded.
- **Lagging groups:** Not confirmed. Do not infer current sector laggards from undated sector rows.
- **Notable rotation:** Theme/sector rotation remains pending confirmation because the sector heatmap has no verified per-row as-of date and no separate theme ranking was executed.

## 3. Earnings reactions

- **Names worth tracking:** Earnings calendar and post-earnings scorer were not fetched/executed in this rendering run.
- **PEAD candidates:** None validated in this run. This is not a “no candidates” conclusion; it is an unavailable-input condition.
- **Reactions that failed or reversed:** Not assessed. A follow-up earnings-trade-analyzer or manual earnings-reaction review is required before naming tickers.

## 4. Open trade review checklist

- **Thesis still valid?** Portfolio/open-trade state was not supplied; review each active thesis against its original catalyst and current price action.
- **Invalidation hit?** Check stops, thesis-break conditions, and any post-close news manually.
- **Position risk still acceptable?** Given weak/down overall participation, confirm that open risk matches the intended risk budget before adding new exposure.
- **Any overnight event risk?** Macro calendar and earnings calendar were not fetched; verify scheduled catalysts before carrying concentrated overnight risk.

## 5. Journal prompts

- What decision today deserves a note: Did weak participation change your willingness to pursue fresh setups?
- What did the process do well: It preserved dated facts and refused to promote unknown-date sector or screener outputs into current candidates.
- What should be avoided tomorrow: Avoid treating unexecuted or undated inputs as confirmation of fresh leadership, earnings strength, or distribution risk.

## 6. Tomorrow preparation

- Re-run full market-regime stack with same-session provenance: uptrend, breadth, market-top, and IBD distribution-day monitor.
- Confirm whether overall participation improves from `508` / `2730` or continues trending down.
- Refresh sector summary with verifiable observation dates before using sector rotation for watchlist decisions.
- Run earnings-trade-analyzer or verified fallback before naming PEAD candidates.
- Review open positions manually against invalidation levels and overnight catalysts.

## 7. Data freshness and degraded mode

- **Fresh data used:** Overall uptrend participation for 2026-11-16 and independent SPY EOD row for 2026-11-16.
- **Unknown/stale-risk data:** Sector summary and FINVIZ migration comparison lack verified session/as-of metadata.
- **Unavailable in this model run:** Macro calendar, earnings calendar/scorer, full market-top analysis, IBD distribution-day monitor, portfolio/open trades, and theme/watchlist confirmation.
- **Credential note:** Credentials were not checked by the model in this isolated rendering run. Unexecuted analyses are reported as unavailable/not executed, not as missing-key failures.

### Source / Skill provenance

| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Overall uptrend participation | Finviz -> uptrend-dashboard CSV -> uptrend-analyzer | d604308942bc606523ff90dfeb9bcc727055ed3a clean | 2026-11-16 | 2026-11-16 | fresh | Fresh overall participation input: count `508`, total `2730`, ratio `0.18608058608058609`, trend `down`. Use as dated breadth evidence, but confirm with the full regime stack. |
| SPY EOD index proxy | FMP stable historical-price-eod/light -> validation harness; upstream skill consumer not executed | unknown | 2026-11-16 | 2026-11-16 | fresh | Fresh independent SPY row: price `739.95`, volume `69207282`. Broader index analysis was not executed. |
| Sector and theme rotation | Finviz -> uptrend-dashboard CSV -> sector-analyst / uptrend-analyzer sector summary | d604308942bc606523ff90dfeb9bcc727055ed3a clean | unknown | 2026-11-16 | unknown | Published sector summary has no verified per-row as-of date. Do not borrow the overall timeseries date; sector heatmap conclusions remain degraded. |
| FINVIZ Elite screener migration comparison | FINVIZ Elite -> patched screener consumer comparison | d604308942bc606523ff90dfeb9bcc727055ed3a clean | unknown | 2026-11-16 | unknown | Legacy/new ticker sets matched in verification, but export has no verified session/as-of metadata. Do not list screened tickers or treat row counts as current candidates. |
| Market breadth composite | TraderMonty breadth CSV -> market-breadth-analyzer | unknown | unknown | 2026-11-16 | unavailable | Not executed in this isolated rendering run. Run the analyzer to obtain a dated composite breadth score before making regime-change claims. |
| Distribution-day / IBD risk | FMP OHLCV -> ibd-distribution-day-monitor | unknown | unknown | 2026-11-16 | unavailable | Not executed. No fresh QQQ/SPY distribution-day count or TQQQ/QQQ exposure policy output is available. |
| Market top-risk composite | FMP + manual/web breadth/sentiment inputs -> market-top-detector | unknown | unknown | 2026-11-16 | unavailable | Not executed. No current top-risk score, distribution component, leading-stock deterioration score, or defensive rotation score is available. |
| Earnings reactions / PEAD | FMP earnings calendar and prices -> earnings-trade-analyzer | unknown | unknown | 2026-11-16 | unavailable | Earnings calendar and scorer were not fetched. Do not interpret this as zero earnings candidates; run earnings workflow or verified fallback. |
| Macro calendar and event risk | Economic calendar / news inputs -> after-close review | unknown | unknown | 2026-11-16 | unavailable | Not fetched. Human reviewer should check next-session macro and earnings catalysts before carrying overnight risk. |
| Portfolio / open trade review | User portfolio/thesis state -> trader-memory-core | unknown | unknown | unknown | unavailable | Portfolio/open trades were not supplied. Checklist remains procedural only; no position-specific thesis or invalidation review was performed. |
