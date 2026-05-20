#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE_CMD="${HERMES_PROFILE_CMD:-trading-research-assistant}"
DELIVER="${HERMES_CRON_DELIVER:-local}"

command -v "$PROFILE_CMD" >/dev/null 2>&1 || {
  echo "Profile command '$PROFILE_CMD' not found. Install with --alias or set HERMES_PROFILE_CMD." >&2
  exit 1
}

create_job() {
  local schedule="$1"
  local name="$2"
  local prompt_file="$3"
  shift 3
  local prompt
  prompt="$(cat "$ROOT_DIR/$prompt_file")"
  echo "Creating cron job: $name"
  "$PROFILE_CMD" cron create "$schedule" "$prompt" \
    --name "$name" \
    --deliver "$DELIVER" \
    "$@"
}

create_job "0 6 * * 1-5" "Pre-market routine" "prompts/pre-market-routine.md" \
  --skill trading-research-orchestrator \
  --skill trading-cron-brief-writer \
  --skill trading-skills-navigator \
  --skill economic-calendar-fetcher \
  --skill earnings-calendar \
  --skill market-breadth-analyzer \
  --skill uptrend-analyzer \
  --skill market-top-detector \
  --skill ibd-distribution-day-monitor \
  --skill exposure-coach \
  --skill earnings-trade-analyzer \
  --skill pead-screener \
  --skill theme-detector

create_job "15 13 * * 1-5" "After-close review" "prompts/after-close-review.md" \
  --skill trading-research-orchestrator \
  --skill trading-cron-brief-writer \
  --skill market-breadth-analyzer \
  --skill uptrend-analyzer \
  --skill market-top-detector \
  --skill ibd-distribution-day-monitor \
  --skill sector-analyst \
  --skill market-news-analyst \
  --skill earnings-trade-analyzer \
  --skill trader-memory-core \
  --skill signal-postmortem

create_job "0 9 * * 6" "Weekly portfolio review" "prompts/weekly-portfolio-review.md" \
  --skill trading-research-orchestrator \
  --skill portfolio-manager \
  --skill kanchi-dividend-review-monitor \
  --skill kanchi-dividend-sop \
  --skill value-dividend-screener \
  --skill dividend-growth-pullback-screener \
  --skill kanchi-dividend-us-tax-accounting \
  --skill trader-memory-core

create_job "0 9 1 * *" "Monthly performance review" "prompts/monthly-performance-review.md" \
  --skill trading-research-orchestrator \
  --skill trader-memory-core \
  --skill signal-postmortem \
  --skill trade-hypothesis-ideator \
  --skill backtest-expert \
  --skill dual-axis-skill-reviewer

echo "Done. Run: $PROFILE_CMD cron list"
