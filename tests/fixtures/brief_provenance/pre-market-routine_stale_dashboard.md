# pre-market-routine — 2026-11-16

Synthetic acceptance fixture, not a live bundle invocation or a Finviz migration test.

Session state: normal session day (2026-11-16).
Posture basis: pending fresh data / degraded for uptrend participation (2026-11-12); independent latest completed regular-session close 2026-11-13 retained across the weekend.
**Risk posture:** research-only
**Primary reason:** Await human review of input coverage.

## 1. Macro calendar
Fixture scope: no additional market claims; human review pending.

## 2. Market regime
Uptrend participation: stale; observation date 2026-11-12. No local key is required; upstream Finviz collection is delayed. Uptrend-dependent posture is pending confirmation; independent distribution signals remain available. Independent distribution signals: carried_forward; observation date 2026-11-13.

## 3. Earnings movers
Fixture scope: no additional market claims; human review pending.

## 4. Themes and sectors
Sector participation: unknown; observation date unknown. Undated rows are degraded pending row-level metadata; no fresh heatmap inference.

## 5. Watchlist candidates
Thesis: wait for verified coverage; invalidation: refreshed inputs contradict the review premise. Risk: incomplete participation/theme evidence. No candidate is ready for confirmation.

## 6. Human next actions
Fixture scope: no additional market claims; human review pending.

## 7. Data freshness and degraded mode

### Source / Skill provenance
| Input / section | Source / Skill | Skill revision | Observation date | Expected observation date | Status | Impact / next step |
|---|---|---|---|---|---|---|
| Uptrend participation | Finviz -> uptrend-dashboard CSV -> uptrend-analyzer | 6e9a635e5259601d79bb7a97085784f8b37742b5 | 2026-11-12 | 2026-11-13 | stale | Calendar: latest completed session due; verify upstream collection and refresh before interpreting posture. |
| Sector participation | Finviz -> uptrend-dashboard sector CSV -> uptrend-analyzer | 6e9a635e5259601d79bb7a97085784f8b37742b5 | unknown | 2026-11-13 | unknown | Degraded: undated sector rows; verify row-level observation metadata before using the heatmap. |
| Independent distribution signals | FMP daily bars -> ibd-distribution-day-monitor | 6e9a635e5259601d79bb7a97085784f8b37742b5 | 2026-11-13 | 2026-11-13 | carried_forward | Latest completed session due under verified calendar; independent result retained for human review. |

Human decision gate: the human reviewer makes all entry and exit decisions.
