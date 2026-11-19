# Rejected real-output regression

`earnings_not_economic.md` is an unedited real pre-market cron-body response
captured during review of local commit `06239f25d56b7facab0ca34949e33341f1998d42`.
It was rejected: an earnings-only event calendar was described as showing no
scheduled high-impact macro events. Economic-calendar input was absent, so that
conclusion was unsupported. Its original metadata/source hashes are retained;
they describe the older tested materials, not the current prompt/input files.

This is intentionally a failing output example, not acceptance evidence.
`test_real_regression_earnings_does_not_prove_macro_events_absent` verifies the
calendar-scope auditor rejects it. Accepted current captures are under
`../generated/`.

`missing_observations_not_zero.md` is another unedited real after-close bundle
response, captured after the event-domain correction but before the explicit
missing-observation guard. It claimed no signals improved/degraded despite no
signal/comparison inputs. Its negative test rejects that unsupported zero-change
claim. Source/response hashes remain in the original metadata sidecar.
