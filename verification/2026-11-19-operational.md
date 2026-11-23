# Post-PR3 operational verification — 2026-11-19 PT

## Result and scope

Fresh controlled Hermes generation, profile installation/discovery, SOUL loading,
and isolated real-time scheduled generation were exercised after PR #3 merged.
This follow-up fixes one runtime compatibility issue and three acceptance-auditor
false negatives. An actual footer-only disclosure failure drove a clearer shared
instruction and a fresh successful morning scheduled run.

**Production is not restored:** all four production jobs last failed with HTTP
400 because this account's Codex route rejects its configured `gpt-5.5` model.
The gateway exists and jobs have fired; that does not establish report delivery.
A choice between a supported Codex model and separately billed API transport is
pending. Production configuration, auth, jobs and gateway were not modified.

Evidence: [artifact directory](2026-11-19-operational/), including original response
hashes, source snapshots, runtime preflight, scheduler timestamps, provider
summaries and the rejected response. Query expansions and credentials remain
private; no runtime config/auth or diagnostic logs are published.

## Exact materials

- Package base: merge `127136533e36b24d7021b5ae048050a562199026` (PR #3), with this follow-up's SOUL/auditor/inline-disclosure edits.
- Hermes v0.17.0, upstream `5db1430a`, existing installed Python 3.11.15.
- Generation: `gpt-5.5` via `custom:openai-direct`, OpenAI API-key transport.
  This does **not** validate production Codex OAuth transport.
- Resolved external skill payloads: clean public `6e9a635e5259601d79bb7a97085784f8b37742b5`; installed external skills were not updated.
- Live Finviz comparison: clean isolated clone of public upstream main `f95e770591b56fd83b9917175f5a7e8fe9ac47dc`. This is distinct from the installed skill revision used in generation.
- Generation inputs are synthetic and dated November 17 by design, independent of today's real clock. Live provider checks below are separate evidence.

Both source repositories and the exact external revision were verified public
before inference. The initial inference attempt was rejected by automatic
approval review over possible non-public payloads; after checking public
visibility, clean source, synthetic inputs, zero tools and empty MCP/hooks,
execution was approved. No rejection was bypassed.

## SOUL and installation

The existing safety sentence `You do not tell the user to buy or sell` matched
Hermes' broad `deception_hide` pattern, so SOUL was blocked. The sentence now
assigns buy/sell decisions to the human trader and explicitly excludes imperative
trading instructions from the assistant's role. Research-only, no-execution,
paper/read-only and human decision gates remain intact. The filter and its
configuration are unchanged.

Hermes' actual context scanner reported zero findings and `load_soul_md()`
returned the exact SOUL content. The runtime preflight records its SHA-256.
A separate fresh `hermes profile install <local-worktree> --name operational-check -y`
succeeded under an isolated HERMES_HOME without an alias. The installed profile
loads the same SOUL, contains 10 bundles and creates no cron jobs automatically.
This checks the local install path, not a published release or production update.

## Fresh inference and scheduled generation

| Check | Result | Boundary |
|---|---|---|
| Pre-market bundle and cron prompt | PASS | Two fresh inference calls; public skills + synthetic inputs; no upstream fetchers executed |
| After-close bundle and cron prompt | PASS | Two fresh inference calls; independent freshness and unavailable/empty semantics audited |
| Real-time one-shot scheduler probe | PASS | Fires once after due time; no forced `cron run`; no repeat execution |
| Scheduled after-close model job | PASS | Actual scheduler → model → local artifact, zero executable model tools |
| Scheduled pre-market first attempt | FAIL, retained | Themes section lacked explicit status/date disclosure; footer alone is insufficient |
| Scheduled pre-market after clarification | PASS | New original output; no hand editing; exact source/output boundary recorded |

The four initial fresh captures precede the final inline-disclosure clarification.
Their exact instruction bytes are archived and checked by hashes. The later
morning scheduled response tests that clarification. The initial evening scheduled
response already contains the required inline disclosure. These are bounded
observations, not a claim of deterministic future model behavior.

Auditor corrections retain strict status/date and failure checks while accepting:

1. Economic-calendar availability under nested headings within Macro calendar.
2. Explicit negation of a zero-change/zero-reaction inference, including quoted claims.
3. `run_cutoff` as well as `Run cutoff` spelling, with the exact timestamp required.

Published scheduled responses remove trailing whitespace only; original artifact and response hashes are retained. No prose was edited into a passing result.

A failed local retry-controller assertion expected two jobs after scope was
reduced to one. The original single-job output was retained and independently
re-audited as PASS; no replacement output was fabricated or inference rerun to
hide that controller error. One-shot jobs completed; no active verification jobs
remain. No gateway was installed or started and no external messages were sent.
This is isolated scheduler verification, **not production overnight gateway soak**.

## Read-only real providers

Public dashboard at `3a47b934aaea9c05aaa3d27d98c9cfa280c8c555`:
latest overall row November 18, **394 / 2709**. Sector summary lacks a verified
row observation date and remains unknown. Independent FMP SPY retrieval succeeded.
It includes a November 19 intraday row; that row is unfinished at the morning
cutoff and cannot replace November 18 completed-session posture. The verified
NYSE calendar and raw observations are in `market-input-context.json`.

Current public upstream Finviz consumers were called read-only against both
endpoints. All eight responses were HTTP 200 and schema-valid:

| Case | New rows | Legacy rows | Ticker sets |
|---|---:|---:|---|
| Value dividend | 23 | 23 | Equal |
| Dividend growth pullback | 12 | 12 | Equal |
| Theme, semiconductors | 9 | 9 | Equal |
| Theme, software application | 60 | 60 | Equal |

Theme parsed cap/change matched the actual new CSV; new and legacy change values
matched. Both Elite endpoints returned unsuffixed market cap in **millions**.
The preliminary comparison mistakenly used a generic dollar parser for legacy
Elite values. Offline review of every retained raw cap pair confirms exact raw
value equality (9 and 60 pairs). The corrected review records the original
comparison hash and that analysis error rather than claiming it was a provider
or upstream-code defect. The summary publishes aggregate/schema/parameter
facts only; full local raw comparison evidence is retained by hash.

No verified session/as-of metadata exists in these Elite exports. Their
observation date remains **unknown**; successful downloads and equal values do
not certify freshness. This is before the December 7 cutover, not post-cutover
acceptance. No live valid-empty result was observed; failed/empty distinctions
are exercised using controlled model inputs and fixtures.

## Remaining work

- Restore production model/provider only after the pending connection choice; verify the chosen transport/model with an isolated smoke before changing the profile/job snapshots.
- Update installed production distribution and explicitly reconcile existing job prompts; updating repository files does not update already-stored cron prompts.
- Observe a successful scheduled production brief and inspect the actual artifact. Existing task timing is evidence of firing, not successful generation.
- Re-run deployed-skill/provider comparisons on or after December 7. Keep Issue #1 open until its outstanding acceptance is independently recorded and closure is authorized.
