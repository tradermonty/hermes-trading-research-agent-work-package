Warning: Unknown toolsets: acceptance-no-tools
  ⚠ tirith security scanner enabled but not available — command scanning will use pattern matching only
# Pre-market routine — 2026-11-17

Session state: normal session day (US cash market open today, 2026-11-17; run cutoff 2026-11-17T06:00:00-08:00, pre-open).
Posture basis: pending fresh data / degraded — the only regime input on file (dashboard, observation 2026-03-27) is far older than the expected completed session 2026-11-16; no validated completed-close posture is available for today.

**Risk posture:** research-only
**Primary reason:** Regime data is stale (2026-03-27 vs expected 2026-11-16) and the direct theme screens could not be validated, so no exposure posture or candidate ranking is supportable this morning.

SYNTHETIC RUN NOTICE: All observations below are synthetic acceptance fixtures. The supplied upstream skills were NOT executed; skill revisions are fixture-provided, not observed from a run.

## 1. Macro calendar
- Status: degraded for economic events.
- High-impact economic events today: unknown — no economic-calendar-fetcher output and no separately dated economic-calendar source was supplied. Per contract, this is reported as unknown/unavailable, never as "no scheduled high-impact events".
- High-impact economic events this week: unknown (same missing input).
- Event risk around market open: cannot be assessed for the economic domain. Earnings-domain calendar (fresh, see section 7) lists no earnings dates on 2026-11-17 within its covered window (2026-11-17 to 2026-11-20); scheduled earnings dates on file are 2026-11-18 and 2026-11-19. Earnings-calendar coverage does not extend to the economic domain.

## 2. Market regime
- Status: degraded — no validated regime inputs for the expected session 2026-11-16.
- Breadth: unavailable. The dashboard observation is dated 2026-03-27 with partial coverage; current-date breadth rows were not supplied.
- Uptrend participation: unavailable (same stale input; no fresh completed-close series).
- Distribution and top-risk signals: unavailable. No distribution data supplied; do not infer a bearish signal from the data gap.
- Exposure posture: unchanged / not determinable. No REDUCE_ONLY or exposure-ceiling recommendation is issued; the human reviewer owns all sizing and exposure decisions.

## 3. Earnings movers
- Status: degraded — no earnings-reaction data supplied.
- Major gap-up and gap-down reactions: none on file; no pre-market gap data was provided.
- PEAD and watchlist candidates: none can be derived from the available inputs.
- Names requiring manual chart review: none can be nominated without reaction data; this is a data gap, not a clean screen.

## 4. Themes and sectors
- Status: degraded for direct theme screens.
- Direct FINVIZ Elite screen A: authentication failure (missing/unusable FINVIZ_API_KEY). No results; this is unavailable, not "no matches", and produces no zero-breadth or bearish inference.
- Direct FINVIZ Elite screen B: schema-valid screen with zero rows, observed 2026-11-17T05:55:00-08:00 (5 minutes before cutoff). This is a valid-empty result — it means "no matches for this screen", not a failed screen; it does not by itself degrade the brief, but it also supplies no theme rankings.
- Themes showing strength: not rankable.
- Themes showing weakness: not rankable.
- Contradictory signals: not assessable; do not combine the failed screen with the valid-empty screen into a composite view.

## 5. Watchlist candidates
No candidates are retained this run — withheld pending validated regime and theme inputs. This is a data-availability withhold, not a rejection of any setup.

| Ticker | Setup | Thesis | Invalidation | Risk notes | Follow-up |
| --- | --- | --- | --- | --- | --- |
| — | none retained (insufficient validated data) | — | — | — | re-run after inputs refreshed |

## 6. Human next actions
- Re-pull the uptrend dashboard and confirm a 2026-11-16 observation date before any regime or posture inference.
- Verify the FINVIZ_API_KEY credential, then re-run direct Elite screens A and B.
- Source a dated economic calendar (economic-calendar-fetcher or equivalent) to cover sections 1's economic domain.
- Manually review the single synthetic morning headline; it carries no trade recommendation.
- All entry/exit and sizing decisions remain with the human reviewer.

## 7. Data freshness and degraded mode

Degraded sections this run: 1 (economic domain), 2 (entire regime), 3, 4. Sections fed only by fresh inputs (earnings-domain calendar, morning news) are retained independently. Missing key: FINVIZ_API_KEY (affects direct Elite screens only; the uptrend-analyzer public dashboard path requires no local key, but its data is stale on age). All data is synthetic; supplied upstream skills were not executed.

### Source / Skill provenance

| Section | Source / upstream dependency | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-17T06:00:00-08:00 | stale | Freshness basis: completed-close (expected_session: 2026-11-16). Observation 2026-03-27 predates the expected session; coverage partial, current dates for other rows unavailable. Sections 2 and any regime-dependent conclusions degraded; posture set to pending fresh data / degraded. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown (authentication failure; no observation produced) | 2026-11-17T06:00:00-08:00 | unavailable | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy). Auth failure — likely missing FINVIZ_API_KEY. No theme results; do not read as "no matches" or a bearish/zero-breadth signal. Section 4 rankings withheld. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T05:55:00-08:00 (timestamp; session-level observation date n/a for a screen) | 2026-11-17T06:00:00-08:00 | valid-empty | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy). Schema-valid, zero rows, 5 minutes old — within limit. Supplies no theme matches; valid-empty alone does not degrade the brief. |
| Morning news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T05:55:00-08:00 | 2026-11-17T06:00:00-08:00 | fresh | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy). 5 minutes old; current-morning pre-market item, treated as unfinished/live data and kept separate from completed-close posture. Headline is synthetic company research with no trade recommendation. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T05:55:00-08:00 (verified-as-of; event dates 2026-11-18, 2026-11-19) | 2026-11-17T06:00:00-08:00 | fresh | Freshness basis: event-calendar (event domain: earnings; requested coverage window 2026-11-17 to 2026-11-20; run cutoff 2026-11-17T06:00:00-08:00, max age 30 minutes, policy source: synthetic acceptance policy). Verified 5 minutes before cutoff and covers the full requested window in the earnings domain only; economic-domain events remain unknown (no economic-calendar source supplied). |

### Dashboard
Status: stale (observation 2026-03-27 vs expected completed session 2026-11-16; partial coverage) — degrades sections 2 and 3 and the posture basis.

### Failed Elite
Status: unavailable (authentication failure; no observation timestamp exists to evaluate against the 30-minute basis) — degrades section 4 theme rankings; consequences: no direct theme strength/weakness output this run.

### Empty Elite
Status: valid-empty (schema-valid, 0 rows, observed 2026-11-17T05:55:00-08:00, within the 30-minute basis) — not degraded and not a failure; yields no matches and no rankings.

### Morning news
Status: fresh (observed 2026-11-17T05:55:00-08:00, 5 minutes old against the 30-minute basis) — usable as unfinished pre-market context only; must not replace the completed-close posture.

### Earnings calendar
Status: fresh (verified-as-of 2026-11-17T05:55:00-08:00, within the 30-minute basis; earnings domain; covers requested window 2026-11-17 to 2026-11-20) — usable for earnings-domain scheduling only; economic-domain availability is separately unavailable.
