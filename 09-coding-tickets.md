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

- Improve sync script to read upstream `workflows/*.yaml` if available.
- Preserve manual bundle edits when `x-generated: false`.
- Add deterministic-output test.

Done when:

- Re-run produces no diff.

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
