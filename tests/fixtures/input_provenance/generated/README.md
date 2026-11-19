# Controlled real-generation evidence

The four workflow/surface captures below are **raw Hermes CLI stdout**, not hand-written briefs.
The input cases are synthetic; no live Finviz/dashboard observation was fetched
and upstream analysis scripts were not executed. Supplied skill revision fields
are fixture provenance, explicitly labelled as such in the responses.

Generation used Hermes Agent v0.17.0 (`5db1430a`) and the configured
`deepseek-v4-flash-vision-exp` inference model. The clean upstream skill checkout
was `6e9a635e5259601d79bb7a97085784f8b37742b5`. Bundle captures include all
resolved skill payloads via Hermes' own bundle builder; cron captures render the
expanded prompt body, without registering or firing a scheduled job. Both
zero-tool preflight and generation used the same Hermes Python/source.

Each metadata sidecar records generation time, source/query/response SHA-256,
and the observed Hermes version. Full expanded queries remain local; the input
JSON and prompt/bundle hashes identify the tested materials. CI audits the
captured outputs and the same auditor can validate newly generated responses.

The runtime was a private disposable HERMES_HOME with inference credentials,
empty MCP configuration, no configured hooks, and no executable tools. The
initial stdout warning about the intentionally empty/unknown toolset is retained
verbatim. The installed Hermes v0.17 context filter also reported that it blocked
SOUL.md (`deception_hide`); that file was not changed or the filter bypassed.
Consequently these captures demonstrate bundle/prompt rendering and provenance
classification, **not SOUL loading, full-profile acceptance, scheduler behavior,
or the December 7 live migration**. The latter checks remain separate gates.

These captures are historical pre-merge evidence. `source_snapshot/` preserves the exact prompt/bundle bytes checked by the original source hashes. They are not inference evidence for the current merged contract; new runs validate the current table plus semantic requirements.
