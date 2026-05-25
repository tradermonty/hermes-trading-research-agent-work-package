# Skill Integration Strategy

## Canonical upstream files

Use these upstream files as the source of truth:

- `skills-index.yaml`: complete skill metadata and workflow membership.
- `workflows/*.yaml`: canonical workflow manifests when present.
- `skills/*/SKILL.md`: actual skill instructions.

### Current bundle-composition SoT (as of B-2b)

3 overlap workflows (`market-regime-daily` / `swing-opportunity-daily` /
`monthly-performance-review`) について B-2b で SoT 分担を明文化した:

- **upstream `workflows/*.yaml` = canonical intent** — 上流 maintainer が
  review している workflow shape (`required_skills`, `optional_skills`,
  `artifacts`, `steps`, `decision_gate`, `manual_review`, `when_to_run`)。
- **`data/skill-mapping.yaml` = Hermes distribution contract** — この
  profile が実行に使う superset。Hermes 側で追加した skill や、Hermes UX
  に合わせた `required_outputs` / refined `title` / refined `cadence` を
  含む。
- **drift test (`tests/test_upstream_workflow_adapter.py`) = 機械的
  ガード** — 上流 required/optional が mapping skills の subset、
  canonical_source marker が一致、upstream `workflows/` 全 slug が
  overlap か ignore に classify されていることを検証。x-generated 値に
  関係なく drift check は走る (自動修正なし、operator 判断)。

#### projection 対象 (v0.1.x)

| upstream field | mapping field | drift-checked? |
|---|---|---|
| `required_skills` + `optional_skills` | `skills` (superset 許可) | yes (subset relation) |
| canonical_source marker | `canonical_source == claude-trading-skills-workflow` | yes |
| `display_name` | `title` | **documented but not drift-checked** — mapping may refine upstream for Hermes UX (e.g. `market-regime-daily` upstream `Market Regime Daily` → mapping `15-minute daily market check`) |
| `cadence` | `cadence` | **documented but not drift-checked** — mapping may refine for Hermes execution semantics (e.g. `swing-opportunity-daily` upstream `daily` → mapping `daily_when_risk_allows`) |

#### Not projected in v0.1.x (B-2c 候補)

- `artifacts` → `required_outputs` の direct 1:1 mapping。上流 artifacts は
  internal pipeline ID (`market_breadth_report` 等)、Hermes
  `required_outputs` は user-facing 項目 (`regime_label` 等) で抽象度が
  違う。
- `steps` / `decision_gate` の bundle instruction への展開。
- `manual_review` / `when_to_run` の prompt body への projection。

#### Upstream workflow inventory classification

`scripts/sync_claude_trading_skills.py:UPSTREAM_OVERLAP_SLUGS` と
`UPSTREAM_IGNORED_WORKFLOW_SLUGS` の 2 frozenset で、上流
`workflows/*.yaml` 全 slug を classify している。**新規 upstream workflow
が追加された場合、どちらかへの分類が無いと drift test が fail する** —
これは feature であり、上流の進化を見逃さないためのガード。

現在の classification:

| upstream slug | classification | 理由 |
|---|---|---|
| `market-regime-daily` | overlap | Hermes 同名 bundle として adopt |
| `swing-opportunity-daily` | overlap | Hermes 同名 bundle として adopt |
| `monthly-performance-review` | overlap | Hermes 同名 bundle として adopt |
| `core-portfolio-weekly` | ignored | Hermes は slug を `weekly-portfolio-review` に rename + `required_outputs` を Hermes UX 用に refine。上流 file は reference-only。 |
| `trade-memory-loop` | ignored | Hermes は bundle 化していない。operator が `trader-memory-core` を `/trade-journal` / `/monthly-performance-review` 経由 (or 直接) で駆動する想定。上流 file は reference-only。 |

`x-generated: false` 維持 — 3 overlap bundles は operator owned
(TICKET-009 で `swing-opportunity-daily` に escalation pointer 追加など)。
adapter regen は走らず、drift test だけが両 SoT の整合をガードする。

## Initial adapter strategy

This repo should not rewrite all trading skills for Hermes. Instead, it adds:

1. Bundles that combine upstream skills.
2. Hermes-native orchestrator skills.
3. Cron prompts and report templates.
4. Validation and sync scripts.

## Mapping rules

- Bundle names should be task-oriented and user-friendly.
- Bundle names should remain stable across releases.
- Skill names must match upstream directory names.
- If upstream workflow manifests exist, prefer their skill order.
- If a missing skill is optional, report degraded mode.
- If a missing skill is essential, fail validation in strict mode.

## Minimal recommended upstream skills for MVP

| Purpose | Skills |
|---|---|
| Navigation | `trading-skills-navigator` |
| Market regime | `market-breadth-analyzer`, `uptrend-analyzer`, `market-top-detector`, `exposure-coach` |
| Macro/calendar | `economic-calendar-fetcher`, `earnings-calendar` |
| Earnings | `earnings-trade-analyzer`, `pead-screener` |
| Candidate planning | `vcp-screener`, `canslim-screener`, `technical-analyst`, `position-sizer`, `breakout-trade-planner` |
| Memory/journal | `trader-memory-core`, `signal-postmortem`, `trade-hypothesis-ideator` |
| Portfolio | `portfolio-manager`, `kanchi-dividend-review-monitor`, `value-dividend-screener` |

## Degraded mode behavior

| Missing component | Behavior |
|---|---|
| `CLAUDE_TRADING_SKILLS_REPO` | Use only Hermes adapter skills; instruct user to set path. |
| `FMP_API_KEY` | Skip FMP-backed fetches; use public/local/manual inputs only. |
| `FINVIZ_API_KEY` | Use Finviz URLs/manual flow rather than API-backed results. |
| Alpaca keys | Skip holdings/portfolio fetch; ask for manual snapshot or CSV. |
| Chart image | Ask user to upload screenshot or skip chart interpretation. |
| `jsonschema` Python module missing | `trader-memory-core` CLI degrades. Install via `python3 -m pip install jsonschema` (or `uv pip install jsonschema`). Skill output continues with reduced validation. |

## Trade ticket primitive (as of B-3 / TICKET-009)

The `/trade-ticket` bundle introduces a single operator-visible primitive between research output and post-hoc journaling: the **trade ticket**. A ticket is a JSON-Schema-validated YAML object (`schemas/trade-ticket.schema.json`) that captures one candidate, the operator-confirmed plan and risk, and an explicit `approval` state (`DRAFT` / `REVIEW_READY` / `APPROVED` / `REJECTED` / `EXPIRED`).

Boundaries (codified by the schema, the bundle instruction, and `tests/test_trade_ticket_schema.py`):

- **`approval.required` is constant `true`** on every ticket — the bundle never produces un-gated artifacts.
- On `APPROVED`, the reviewer must re-type ticker, direction, entry, stop, and `risk_per_trade_pct` into `approval.confirmed.*`. The business-invariant test asserts the values match the ticket body (`candidate.*`, `plan.*`, `risk.*`) and are non-null. A mismatch demotes the ticket back to `REVIEW_READY`.
- **Output surface is the ticket YAML only.** The bundle does not place orders, submit to brokers, or schedule executions. The instruction states this in positive form ("ticket output only; execution and broker submission are out of scope") and the boundary phrase is asserted by test.
- **Persistence is operator-owned.** The bundle is stateless across invocations. The operator either commits ticket files under an external `tickets/` directory or hands them to `trader-memory-core` via its own storage interface.
- **Lineage** is carried through `provenance.source_bundle` and `provenance.source_candidate_ref` (a stable composite like `NVDA-2026-05-24-VCP`). The `/swing-opportunity-daily` and `/pre-market-routine` bundles' instructions are updated to require both fields when escalating a candidate to `/trade-ticket`.

Out of scope for B-3 / TICKET-009 (deferred to a future ticket): multi-session ticket lifecycle, archive directory, id allocator, automatic expiration trigger, broker submission of any kind. The SOUL perimeter (`SOUL.md`) remains authoritative.

## Ticket persistence and journal bridge (as of TICKET-010)

TICKET-010 extends the trade ticket primitive with two contract-level additions that close the **Research → Human Go/No-Go → Trade Ticket → Journal** loop without crossing the execution boundary. The bundle still emits YAML only; persistence and journal handoff remain operator-confirmed.

**Lifecycle figure** (the five statuses unchanged, plus the optional bridge that fires when the operator wants to register / update / postmortem a thesis):

```
DRAFT ──/trade-ticket review──▶ REVIEW_READY
          │
          ├─/trade-ticket APPROVE──▶ APPROVED ──(optional journal_bridge)──▶ trader-memory-core
          │
          ├─/trade-ticket REJECT───▶ REJECTED
          │
          └─/trade-ticket EXPIRE───▶ EXPIRED
```

Suggested save filename: `<ticket_id>.ticket.yaml` under `${HERMES_TRADE_TICKET_DIR}` (default `${HOME}/trading-research/tickets`). The operator expands `${HOME}` themselves; the bundle prints the literal. The `.ticket.yaml` suffix matches the repo's `.gitignore` safety net so an accidental in-repo save is caught.

**Three role split for persistence** — no role silently writes on behalf of another:

1. **Bundle** — emits the ticket YAML and a single trailing comment of the form `# Suggested save path: ${HERMES_TRADE_TICKET_DIR}/<ticket_id>.ticket.yaml`. Never writes to disk.
2. **Operator** — reads the YAML and saves it at the suggested path (or anywhere else they prefer), after expanding `${HOME}` themselves. The Hermes runtime does not bridge bundle output to disk.
3. **`trader-memory-core`** — when the ticket carries an optional `journal_bridge` block, the operator hands the payload to `trader-memory-core` via its own storage interface to register, update, or postmortem the thesis. The ticket bundle does not call `trader-memory-core` directly.

**`HERMES_TRADE_TICKET_DIR` expansion** — declared as a profile env in `distribution.yaml:env_requires` (optional, default `${HOME}/trading-research/tickets`) and pre-seeded in `.env.EXAMPLE`. The `.env` parser used by `cron/create_cron_jobs.py` (and by extension any helper that reads the same file) returns the literal `${HOME}/...`; consumers expand with `os.path.expandvars(os.path.expanduser(value))`. `tests/test_trade_ticket_schema.py::test_env_expansion_yields_absolute_path` locks that contract.

**`journal_bridge` shape** — optional top-level object on any ticket. `target` is `{"const": "trader-memory-core"}` so typos (`trader_memory_core`) are rejected. `action` is one of `register_thesis | update_thesis | postmortem`. `thesis_status` (optional) is one of `IDEA | ENTRY_READY | ACTIVE | CLOSED`. `notes` (optional) is a non-empty string. Unknown fields inside `journal_bridge` are rejected (`additionalProperties: false`) so a `thesis_statuz` typo fails validation. The field is **recommended on APPROVED tickets but not required** — APPROVED is already heavy with the `confirmed.*` re-type contract, and forcing `journal_bridge` would break v0.1.5 fixtures. A future v0.2 series may add a `JOURNALED` status (6th value) and tighten `journal_bridge` on APPROVED as a deliberate breaking change.

Out of scope for TICKET-010 (deferred): broker submission of any kind; LLM-side silent disk write; runtime ticket files committed to this repo; the cross-check between `journal_bridge.action` and `thesis_status` (e.g. `postmortem` → `CLOSED`); the `JOURNALED` status enum value; making `journal_bridge` required on APPROVED.

## Vendoring rules

When implementing vendored mode:

- Copy skills exactly into `skills/vendor/<skill-name>` or `skills/<skill-name>` after deciding which Hermes path resolves best.
- Write `vendor-manifest.json` with upstream repo path, commit SHA if available, selected skills, and timestamp.
- Never silently patch upstream skill files.
- If compatibility patches are needed, store patch files under `patches/` and apply them explicitly.
