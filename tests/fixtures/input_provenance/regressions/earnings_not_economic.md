Warning: Unknown toolsets: acceptance-no-tools
# Pre-market routine — 2026-11-17

Session state: normal session day — Tuesday 2026-11-17, US cash market session scheduled today; run is pre-open (cutoff 2026-11-17T06:00:00-08:00).
Posture basis: pending fresh data / degraded — the latest usable completed-close observation is dated 2026-03-27, which is older than the expected completed regular session 2026-11-16; no fresh completed-close posture can be established for today.

**Risk posture:** research-only
**Primary reason:** The completed-close regime dataset is stale (2026-03-27 vs expected session 2026-11-16) and one direct FINVIZ Elite screen failed authentication, so no regime, breadth, or posture conclusion is supported; only calendar and news inputs are fresh.

---

## 1. Macro calendar

Status basis: fresh (synthetic local event calendar, verified-as-of 2026-11-17T05:55:00-08:00, covering 2026-11-17 through 2026-11-20).

- High-impact events today: None listed. The calendar covers 2026-11-17 but lists no event dates on 2026-11-17 itself.
- High-impact events this week: Earnings events on 2026-11-18 and 2026-11-19 (synthetic calendar; no tickers or impact tiers supplied).
- Event risk around market open: No scheduled high-impact events on today's date in the supplied calendar; unscheduled/open risk cannot be assessed because gap and reaction data were not supplied.

## 2. Market regime
### Market regime
Status: degraded (stale completed-close input)

- Breadth: Not determinable — the only regime input (uptrend-analyzer public dashboard) is dated 2026-03-27, far older than the expected completed session 2026-11-16, with partial coverage. No breadth conclusion is drawn.
- Uptrend participation: Not determinable — same stale observation; participation is not inferred from ~7.5-month-old data.
- Distribution and top-risk signals: Not determinable — no current completed-close data.
- Exposure posture: No exposure posture is stated. The stale dashboard must not be read as a current regime, and the failed Elite screen must not be read as a bearish or zero-breadth signal. Human reviewer sets all exposure decisions.

## 3. Earnings movers
### Earnings movers
Status: degraded (required earnings-reaction dataset not supplied)

- Major gap-up and gap-down reactions: Unavailable — no earnings-reaction or gap dataset was provided for this run.
- PEAD and watchlist candidates: None can be identified without reaction data; nothing is invented.
- Names requiring manual chart review: None listed, because no names are supported by supplied data. The 2026-11-18/19 calendar events are forward dates only and are not observation timestamps.

## 4. Themes and sectors
### Themes and sectors
Status: degraded (one Elite screen unavailable; one valid-empty)

- Themes showing strength: Not determinable. Direct FINVIZ Elite screen A failed authentication (missing/invalid FINVIZ_API_KEY); this is a fetch failure, not "no matches."
- Themes showing weakness: Not determinable. Screen B completed successfully and returned zero rows (valid-empty, 2026-11-17T05:55:00-08:00, within freshness limit); a valid-empty screen means "no matches" and is not itself evidence of weakness or a degraded brief.
- Contradictory signals: None assessable. A synthetic morning news item ("Synthetic company research update; no trade recommendation", 2026-11-17T05:55:00-08:00) is fresh but is unfinished pre-open data and is not used to infer any sector regime.

## 5. Watchlist candidates
### Watchlist candidates
Status: degraded (no candidates retained; underlying regime and screen inputs degraded)

No candidates are retained. With current inputs, any setup, thesis, invalidation, or ranking would be unsupported.

| Ticker | Setup | Thesis | Invalidation | Risk notes | Follow-up |
| --- | --- | --- | --- | --- | --- |
| — (none retained) | — | — | — | — | Re-run after fresh 2026-11-16 completed-close data and restored FINVIZ key; human decision gate remains closed for entries. |

## 6. Human next actions

- Re-pull the uptrend-analyzer public dashboard to obtain completed-close data for expected session 2026-11-16 before drawing any regime conclusion.
- Restore or supply FINVIZ_API_KEY and re-run direct FINVIZ Elite screen A; treat the current failure as unavailable, not as "no matches."
- Re-run screen B alongside screen A so the current valid-empty result can be confirmed against a working screen rather than standing alone.
- Obtain a current earnings-reaction/gap dataset for PEAD screening; today's brief contains none.
- Make all entry/exit decisions at the human gate; this brief is research-only and supports no trade actions.

## 7. Data freshness and degraded mode

### Source / Skill provenance

| Section | Source / upstream dependency | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| Dashboard | uptrend-analyzer / public dashboard -> upstream Finviz collection | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-03-27 | 2026-11-17T06:00:00-08:00 | stale | Freshness basis: completed-close (expected_session: 2026-11-16). Observation 2026-03-27 predates the expected completed session; coverage partial, current dates for other rows unavailable. Consequence: Market regime (Section 2) degraded; no breadth, participation, distribution, or exposure posture conclusions. Follow-up: re-pull dashboard for 2026-11-16. |
| Failed Elite | theme-detector / direct FINVIZ Elite screen A | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | unknown (authentication_failure; no observation produced) | 2026-11-17T06:00:00-08:00 | unavailable | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00; max age 30 minutes; policy source: synthetic acceptance policy). Fetch failed on auth (missing/invalid FINVIZ_API_KEY); schema not validated. Consequence: Themes (Section 4) degraded for screen A; failure must not be read as zero matches or a bearish signal. Follow-up: restore key and re-run. |
| Empty Elite | theme-detector / direct FINVIZ Elite screen B | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T05:55:00-08:00 | 2026-11-17T06:00:00-08:00 | valid-empty (fresh) | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00; max age 30 minutes; policy source: synthetic acceptance policy). Observation 5 minutes old, within limit; schema-valid with 0 rows — a genuine "no matches", not a failed screen. A valid-empty screen alone does not degrade the brief. Follow-up: re-confirm alongside screen A once the key is restored. |
| Morning news | market-news-analyst / synthetic timestamped news | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | 2026-11-17T05:55:00-08:00 | 2026-11-17T06:00:00-08:00 | fresh | Freshness basis: timestamp (run cutoff 2026-11-17T06:00:00-08:00; max age 30 minutes; policy source: synthetic acceptance policy). Observation 5 minutes old; a current-morning pre-open item may be fresh even though it postdates the 2026-11-16 posture close — it is labeled unfinished pre-market data and is kept separate from completed-close posture, never substituting for it. |
| Earnings calendar | earnings-calendar / synthetic local event calendar | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; fixture-provided, not executed) | verified-as-of 2026-11-17T05:55:00-08:00 (event dates 2026-11-18 and 2026-11-19 are future event dates, not observation timestamps) | 2026-11-17T06:00:00-08:00 | fresh | Freshness basis: event-calendar (requested coverage window 2026-11-17 through 2026-11-20; max age 30 minutes; policy source: synthetic acceptance policy). Verified-as-of 05:55 PT is within limit and coverage spans the full requested window; no events listed for 2026-11-17 itself. |

### Degraded mode summary

- All content in this brief is synthetic acceptance-run data. Supplied upstream skills were not executed; skill revisions are fixture-provided identifiers, and no live fetch, browsing, or file changes occurred.
- Degraded sections: Market regime (stale 2026-03-27 dashboard vs expected session 2026-11-16), Earnings movers (no reaction dataset supplied), Themes and sectors (Elite screen A auth failure; screen B valid-empty), Watchlist candidates (nothing retained).
- Fresh sections: Macro calendar (event calendar) and the timestamped morning news item; both are used only for their own scope.
- Missing input: FINVIZ_API_KEY (affects direct Elite screens only; the public dashboard path requires no local key, but its own observation is stale).
- No ranking, candidate, breadth, or posture conclusion is drawn from failed or stale inputs. The human reviewer retains all entry and exit decisions.
