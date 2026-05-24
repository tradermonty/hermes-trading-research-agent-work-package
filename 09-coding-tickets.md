# Coding Tickets

## TICKET-001 — Validate skeleton

- Run package validator and tests.
- Fix any local path or YAML problems.
- Output a short report.

Done when:

- `make validate` passes.
- `make test` passes.

## TICKET-002 — Hermes profile distribution smoke test

- Create a local git repo from this package.
- Install via Hermes profile distribution.
- Verify alias and chat.

Done when:

- `trading-research-assistant chat` works.
- `SOUL.md` is active.

## TICKET-003 — External skills validation

- Clone `claude-trading-skills`.
- Set `CLAUDE_TRADING_SKILLS_REPO`.
- Validate bundle skill references.
- Document missing skills if any.

Done when:

- Validator can check upstream skill dirs.

## TICKET-004 — Bundle generator hardening

Split into two follow-up tickets to keep release boundaries clean
once the first half started shipping in v0.1.x.

### TICKET-004a — Generator ownership + determinism (✓ shipped in B-2a)

- Preserve manual bundle edits when `x-generated: false`.
- Treat missing `x-generated` key as legacy-unknown and skip with WARN.
- Write-if-changed for `x-generated: true` bundles (no spurious mtime).
- `update_external_config()` is also idempotent: no-op when the
  `${CLAUDE_TRADING_SKILLS_REPO}/skills` entry is already present.
- `--force-overwrite` escape hatch + `make sync-external-write-force`
  double-gated by `REQUIRE_SYNC_WRITE=1` and `REQUIRE_FORCE_OVERWRITE=1`.
- `tests/test_sync_determinism.py` covers skip / force / write-if-changed
  / new-file / `update_external_config` idempotency / real-repo
  second-run-noop.

Done when:

- Re-run of `make sync-external-write` produces no diff (mtime + content
  invariant) for both `skill-bundles/*.yaml` and `config.yaml`.

### TICKET-004b — Upstream workflows adapter (open, B-2b)

- Read upstream `workflows/*.yaml` when present and adopt it as the
  primary source for the workflows it covers (`market-regime-daily`,
  `swing-opportunity-daily`, `monthly-performance-review`).
- Define how the upstream `steps[]` / `artifacts[]` shape projects
  onto our flat `skills[]` + `required_outputs[]` bundle shape.
- Keep `data/skill-mapping.yaml` as the SoT for the bundles that have
  no upstream workflow (6 of 9 today).
- Add validator checks that catch drift between upstream and the
  generated bundle.

Done when:

- For the three overlap workflows, regenerating from upstream and
  regenerating from `data/skill-mapping.yaml` produce byte-identical
  bundles.
- The other six bundles continue to regenerate from
  `data/skill-mapping.yaml` only.
- A test fails when upstream and the local override disagree on
  fields the bundle exposes.

## TICKET-005 — Cron UX

- Verify current Hermes cron syntax.
- Update script if needed.
- Test `local` delivery.
- Add Telegram notes if relevant.

Done when:

- Four default jobs are created and listable.

## TICKET-006 — Output QA harness

- Add sample inputs.
- Add expected section checks.
- Add forbidden phrase checks.

Done when:

- `pytest` fails if direct buy/sell language appears in prompts or SOUL.

## TICKET-007 — Release docs

- Add final README.
- Add Japanese README section.
- Add changelog.

Done when:

- A new user can follow README without private context.

## TICKET-008 — Vendored mode

- Copy selected upstream skills.
- Generate `vendor-manifest.json`.
- Add drift detection.

Done when:

- Profile works without external repo.
