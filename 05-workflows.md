# Workflow Definitions

## 1. Pre-market routine

Goal: provide a fast, structured view of the trading day before US market open.

Inputs:

- Economic calendar.
- Earnings calendar and recent earnings reactions.
- Breadth and uptrend data.
- Market top/distribution risk.
- Theme/sector signals.

Outputs:

- Risk posture.
- Macro event risk.
- Earnings movers.
- Breadth/uptrend summary.
- Watchlist candidates.
- Human next actions.

Human gate:

- User decides whether to do nothing, review charts, reduce risk, or prepare possible orders in a separate execution system.

## 2. After-close review

Goal: close the process loop after the trading day.

Inputs:

- Daily market action.
- Breadth/uptrend changes.
- Sector/theme rotation.
- Earnings reactions.
- Open thesis records if available.

Outputs:

- What changed.
- What invalidated.
- What needs journaling.
- Tomorrow preparation list.

Human gate:

- User confirms journal entries and decides whether any portfolio/trade changes are needed elsewhere.

## 3. Earnings movers triage

Goal: turn a noisy earnings list into a small review queue.

Inputs:

- Earnings announcements.
- Gap/reaction data.
- Volume/trend data.
- News context.

Outputs:

- Ignore/watchlist/PEAD/manual-review classification.
- Candidate thesis.
- Invalidation.
- Follow-up data.

Human gate:

- User performs chart review and separate risk planning.

## 4. Trade journal

Goal: capture process memory.

Inputs:

- User trade note.
- Market regime.
- Setup source.
- Entry/stop/target/size when available.

Outputs:

- Structured journal entry.
- Thesis record.
- Postmortem trigger.

Human gate:

- User approves the final journal entry.

## 5. Weekly portfolio review

Goal: maintain long-term portfolio discipline.

Inputs:

- Holdings snapshot.
- Dividend data.
- Allocation/concentration.
- Forced-review triggers.

Outputs:

- Review queue.
- Risk and concentration notes.
- Watchlist updates.

Human gate:

- User chooses whether to rebalance or research further.

## 6. Monthly performance review

Goal: improve the trading process.

Inputs:

- Trade journal.
- Postmortems.
- Candidate outcomes.
- Backtest/research notes.

Outputs:

- Pattern summary.
- Mistake taxonomy.
- Next-month operating rules.
- Skills/workflow improvement backlog.
