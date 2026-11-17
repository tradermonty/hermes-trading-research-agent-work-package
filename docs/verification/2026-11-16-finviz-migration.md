# Finviz migration / brief provenance verification — 2026-11-16 PT

## Scope and revisions

- Package under test: PR #2, starting at `65ab8eaf5fabcd3fd96f839c247c780906bfa3f9`, plus the live-rendering instruction corrections included with this record.
- Actual migrated upstream skill code: clean `d604308942bc606523ff90dfeb9bcc727055ed3a`, [upstream PR #806](https://github.com/tradermonty/claude-trading-skills/pull/806), checked out in a separate temporary clone.
- Upstream main at inspection: `aa97abfeb5c36c1fd1f3022a704680cc5f78cb69`, still using the legacy export. PR #806 was **open**, not deployed or merged by this verification.
- Existing installed external checkout: `6e9a635e5259601d79bb7a97085784f8b37742b5`; unchanged. Testing a candidate does not update installed users' skills.
- Hermes: v0.17.0 (2026.6.19), reported upstream `5db1430a`. Earlier v0.14.0 compatibility notes are historical, not the tested version here.

## Actual provider comparison: PASS before cutover

Read-only authenticated calls ran 2026-11-17 06:40:34–06:40:42 UTC
(2026-11-16 22:40 PT). Each patched consumer made the real new request;
an instrumented transport retained the request parameters and response for
comparison with a real legacy request using the same filters.

| Consumer / case | Legacy rows | New rows | Ticker set | Other values |
|---|---:|---:|---|---|
| value-dividend-screener | 20 | 20 | SHA-256 equal | Patched result matches validated CSV |
| dividend-growth-pullback-screener | 7 | 7 | SHA-256 equal | Patched result matches validated CSV |
| theme-detector, Semiconductors, bullish | 12 | 12 | SHA-256 equal | Market Cap and Change identical by ticker |
| theme-detector, Software - Application, bearish | 39 | 39 | SHA-256 equal | Market Cap and Change identical by ticker |

All eight responses were HTTP 200 and passed required-header, duplicate-header,
row-shape and unique-ticker checks. New requests used `/export/screener` and
`type=stocks`; theme requests pinned `c=1,6,66`. Filters, `v=151` and `ft=4`
remained unchanged. API keys and authentication query parameters are omitted
from the [machine evidence](2026-11-16-finviz-live-comparison.json).

The CSV provides no verified session/as-of metadata. Its observation date is
therefore **unknown**, even though current legacy/new values match. Retrieval
timestamps are recorded separately. This run does not establish a valid-empty
live observation; failed/empty distinctions remain covered by offline fixtures.

Commands against the candidate clone, using the existing upstream development
Python environment, were run separately to avoid skill-local import collisions:

```text
python -m pytest -q skills/value-dividend-screener/scripts/tests
  234 passed
python -m pytest -q skills/dividend-growth-pullback-screener/scripts/tests
  210 passed
python -m pytest -q skills/theme-detector/scripts/tests
  571 passed, 1 skipped (optional finvizfinance import)
python scripts/package_skills.py --check --skill value-dividend-screener \
  --skill dividend-growth-pullback-screener --skill theme-detector
  all three archives match source
```

The live-comparison harness remains in the local evidence directory
`/private/tmp/hermes-migration-evidence/verify_finviz.py`. It invoked the two
`FINVIZClient.screen_stocks()` implementations and theme selector's
`_fetch_finviz_elite()` directly; this was not a full FMP dividend ranking or
full theme-analysis run. It did not change upstream code or credentials.

## Actual public observations and independent input

The dashboard snapshot was pinned to
`be3ef00168bee14adc406a7ab64e77922d60540f`:

- Overall timeseries: latest row `2026-11-16`, 508 / 2730 uptrending.
- Published sector summary: 11 rows; **no row-level observation date**. It stays unknown/degraded rather than borrowing the overall date.
- An actual `uptrend-analyzer --output-dir <temporary-directory> --run-id hermes-pr2-migration-check` run completed. Its computed composite cannot by itself establish freshness of undated sector inputs; the brief check used dated raw observations separately.
- Independent FMP SPY daily input: dated rows for `2026-11-13` and `2026-11-16`, retrieved via `stable/historical-price-eod/light`.
- Expected sessions were checked with `pandas-market-calendars` XNYS/NYSE. The November 16 session opened 14:30 UTC and closed 21:00 UTC; the preceding completed session was Friday November 13.

## Isolated Hermes runtime check

Installed the local profile into
`/private/tmp/hermes-migration-runtime/profiles/migration-check`, without an
alias or gateway. The shipped cron creation script registered the presets;
only the morning/evening jobs were manually exercised, with local delivery.
Optional MCPs and model tool actions were disabled. Existing production
profiles, schedules and external skills were unchanged.

The model rendered reports from the actual externally collected snapshots,
appended as evidence to the installed cron prompts. This
tests real Hermes prompt/skill attachment and output rendering; it does **not**
claim that the model autonomously executed every market-data skill.

- Morning: explicit historical replay of 2026-11-16 06:00 PT using only observations on/before November 13. Later migration-comparison data cannot create pre-market candidates.
- Evening: November 16 completed-session observations, retaining independent SPY/overall facts while sector/Elite dating stays unknown.
- Macro, earnings, portfolio and full corroborating analyses were intentionally not executed. This is execution scope, not proof of missing credentials.

The first unauthenticated local-provider attempts failed HTTP 401. Correct
registered-provider authentication was then used in process memory only. The
first successful Spark-generated outputs still failed acceptance: date cells used
em dashes/date ranges, morning rows said fresh across a weekend bridge, and
the morning narrative included a malformed numeric denominator and inferred
missing keys. Original artifacts were retained locally; none were hand-edited
into passing examples.

Those failures drove the included instruction corrections and regression
cases. A second Spark run passed date/table validation but still mistranscribed
integer counts. It is retained as failed UX evidence, not a passing example.

Final runs explicitly pinned **gpt-5.5** through a configured OpenAI-compatible
provider (`custom:openai-direct`, `https://api.openai.com/v1`). This is the
production profile's configured model, but uses API-key transport rather than
the production profile's Codex OAuth transport. Credentials remained in
process memory. Hermes rejected a bare `openai` provider name and correctly
blocked the unpinned model change; those setup attempts made no inference
call. Both test jobs were then explicitly pinned before the final runs.

### Final generated outputs: PASS

The linked files extract the original `## Response` sections, with only
trailing whitespace removed for publication; the report content is unchanged. [Artifact paths and SHA-256 hashes](2026-11-16-output-manifest.json)
retain the relationship to full local cron artifacts. The actual supplied
observations and calendar are in [the input evidence](2026-11-16-market-input-context.json).

| Routine | Actual successful output | Result |
|---|---|---|
| Morning replay | `8888845e88fb/2026-11-16_23-00-34.md` — [response](2026-11-16-pre-market-response.md) | PASS: 626 / 2775 preserved; dated facts carried forward across weekend; unknown inputs remain degraded |
| Evening | `07ae940b1638/2026-11-16_23-00-35.md` — [response](2026-11-16-after-close-response.md) | PASS: 508 / 2730 and independent SPY facts preserved; same-session facts fresh; undated sector/Elite inputs unknown |

Both passed `python scripts/validate_brief_provenance.py <full-cron-output.md>`.
Independent review additionally compared counts/ratios/MA/slopes with the source
evidence, checked source lineage and observation dates, and confirmed that
unexecuted analyses were not zero-candidate or missing-key diagnoses. Human
decision gates remained explicit. No screened ticker was promoted from the
undated Elite comparison into a current candidate.

The corrected contract/fixture/test changes also received independent review.
Package tests: **233 passed, 14 skipped** without an external checkout;
structural validation and all canonical skill references resolved against the
actual migration candidate. Optional MCPs remained disabled. All four test
cron jobs were paused after verification; no gateway was started and no
external messages were delivered.

With that same candidate supplied to the workflow-drift tests, both unchanged
main `9598a9c` and this branch produced **10 passed, 3 failed**: missing required
and optional skills in `swing-opportunity-daily`, plus unclassified upstream
workflows. These are reproduced pre-existing drift, not introduced here. No
full external-linked suite PASS is claimed.

## Remaining limits

This is **pre-cutover** verification. A post-2026-12-07 comparison must record
the actual deployed skill revision and repeat the provider/schema and brief
checks. Upstream PR #806 merge/deployment and existing workflow-mapping drift
are separate work. This package PR may improve traceability while that work
remains open; it does not certify future provider behavior or close Issue #1's
remaining operational acceptance automatically.
