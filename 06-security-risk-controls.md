# Security and Risk Controls

## Secrets

- Commit `.env.EXAMPLE`, never `.env`.
- Use Hermes/env secret handling for provider keys.
- Do not ask for secrets in chat messages.
- Do not expose raw secret values in logs or reports.

## Brokerage safety

Default: `ALPACA_PAPER=true`.

This profile should not ship with live order placement. Any future execution integration must be separated into a different profile or require explicit opt-in with additional safeguards.

Recommended stages:

1. No brokerage access.
2. Paper/read-only account context.
3. Paper order template generation only.
4. Separate execution system with human confirmation.

## Cron safety

- Default delivery is `local`.
- Installer explicitly enables cron jobs.
- Routine prompts are self-contained.
- Jobs must be visible in `cron list`.
- Avoid hidden high-frequency jobs.
- Avoid expensive or token-heavy hourly loops unless gated.

## Data integrity

- Never fabricate market data.
- State missing API keys.
- State stale data.
- Separate retrieved facts from synthesis.
- Include skill/source provenance.

## Financial communication safety

Use:

- "research candidate"
- "watchlist"
- "requires manual confirmation"
- "risk gate"
- "invalidation"

Avoid:

- "buy now"
- "sell now"
- "guaranteed"
- "safe trade"
- "must enter"

## Distribution trust

Profile distributions are powerful because they can package `SOUL.md`, skills, config, MCP, and cron assets. Users should be told to inspect the repo before installing, especially `SOUL.md`, `skills/`, `cron/`, and `mcp.json`.
