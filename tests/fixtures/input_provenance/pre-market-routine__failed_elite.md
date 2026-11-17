# pre-market-routine — 2026-11-17

Synthetic offline acceptance example; skill revision is illustrative, not a live invocation.
Expected completed session: 2026-11-16.
Session state: normal session day.
Posture basis: pending fresh data / degraded.

## Affected section
theme-detector / direct FINVIZ Elite screen: unavailable; observation date: unknown. degraded; authentication failure; candidates withheld; verify credentials or dated manual fallback.
Elite-dependent theme candidates unavailable; independent data retained.

## Independent earnings calendar
fresh; observation date: 2026-11-16. Earnings dates remain available for research.

## Risk and human decision gate
Thesis: retain independently supported earnings-event watchlist observations.
Invalidation: verify the event calendar and any subsequent source revision.
Risk notes: event gaps and missing theme/uptrend confirmation limit conclusions.
Human decision gate: the human reviewer decides any follow-up or trade action.

## Data freshness and degraded mode
### Source / Skill provenance
| Section | Source / upstream dependency | Skill revision | Observation date | Retrieved at | Status | Impact / follow-up |
|---|---|---|---|---|---|---|
| Affected section | theme-detector / direct FINVIZ Elite screen | 6e9a635e5259601d79bb7a97085784f8b37742b5 (clean; illustrative) | unknown | 2026-11-17T06:00:00-08:00 | unavailable | degraded; authentication failure; candidates withheld; verify credentials or dated manual fallback |
| Independent earnings calendar | earnings-calendar / synthetic local dated calendar | unknown (fixture) | 2026-11-16 | 2026-11-17T06:00:00-08:00 | fresh | Retain independent data; verify events before review |
