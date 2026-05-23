#!/usr/bin/env bash
# Thin wrapper around cron/create_cron_jobs.py — that file is the source
# of truth for cron job creation. See docs/03-hermes-compatibility-notes.md
# and cron/README.md.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT_DIR/cron/create_cron_jobs.py" "$@"
