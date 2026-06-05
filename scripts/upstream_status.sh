#!/usr/bin/env bash
#
# upstream_status.sh — working-tree-safe inspection of the external-linked
# claude-trading-skills checkout BEFORE any user or agent pulls upstream.
#
# It fetches remote metadata only (remote-tracking refs / FETCH_HEAD may be
# updated) and NEVER modifies skill files, the working tree, or local history.
# It does not pull, merge, rebase, or stash. See TICKET-015 in
# docs/09-coding-tickets.md and the "Upstream status inspection" note in
# docs/03-hermes-compatibility-notes.md.
#
# Exit status: 0 when the report prints (even if the upstream ref is
# UNRESOLVED — the report is still useful); non-zero only when the repo
# itself cannot be resolved.
#
# Optional env:
#   UPSTREAM_STATUS_REF=<remote>/<branch>   explicit remote-tracking ref to
#                                           compare against (e.g. upstream/main).
set -euo pipefail

REPO="${CLAUDE_TRADING_SKILLS_REPO:-}"
if [ -z "$REPO" ]; then
  echo "ERROR: CLAUDE_TRADING_SKILLS_REPO is not set." >&2
  echo "       Point it at your local claude-trading-skills checkout." >&2
  exit 2
fi
if [ ! -d "$REPO" ] || ! git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
  echo "ERROR: '$REPO' is not a git repository." >&2
  exit 2
fi

git_q() { git -C "$REPO" "$@" 2>/dev/null || true; }

# --- severity (0 NONE / 1 LOW / 2 MEDIUM / 3 HIGH) -------------------------
sev=0
bump() { if [ "$1" -gt "$sev" ]; then sev="$1"; fi; }

# --- step 2: detached HEAD (independent of upstream resolution) ------------
detached=false
if ! git -C "$REPO" symbolic-ref -q HEAD >/dev/null 2>&1; then
  detached=true
  bump 3
fi

head_sha="$(git_q rev-parse --short HEAD)"
branch="$(git_q rev-parse --abbrev-ref HEAD)"
[ "$branch" = "HEAD" ] && branch="DETACHED @ ${head_sha}"

# --- step 3: resolve the upstream ref to compare against ------------------
ref=""
ref_remote=""
resolution_source="none"   # none | tracking | originhead | override
override_no_remote=false

if [ -n "${UPSTREAM_STATUS_REF:-}" ]; then
  cand="$UPSTREAM_STATUS_REF"
  rpart="${cand%%/*}"
  if [ "$rpart" != "$cand" ] && git -C "$REPO" remote | grep -qx "$rpart"; then
    ref="$cand"; ref_remote="$rpart"; resolution_source="override"
  else
    # tag / SHA / local branch / refs/... long form: no extractable remote.
    override_no_remote=true
    bump 2
    if git -C "$REPO" rev-parse --verify -q "${cand}^{commit}" >/dev/null 2>&1; then
      ref="$cand"; resolution_source="override"
    fi
  fi
else
  u="$(git_q rev-parse --abbrev-ref --symbolic-full-name '@{u}')"
  if [ -n "$u" ]; then
    ref="$u"; ref_remote="${u%%/*}"; resolution_source="tracking"
  else
    oh="$(git_q symbolic-ref --short refs/remotes/origin/HEAD)"
    if [ -n "$oh" ]; then
      # No tracking upstream on the current branch; only origin/HEAD resolved.
      ref="$oh"; ref_remote="${oh%%/*}"; resolution_source="originhead"
      bump 2   # tracking_upstream=false → operator judgement needed
    fi
  fi
fi

[ -z "$ref" ] && { resolution_source="none"; bump 2; }

# --- step 4: fetch BEFORE any ref-relative numbers ------------------------
fetch_note=""
if [ -n "$ref_remote" ] && [ "$override_no_remote" = false ] && [ -n "$ref" ]; then
  if git -C "$REPO" fetch --quiet "$ref_remote" 2>/dev/null; then
    fetch_note="ok"
  else
    fetch_note="FAILED (showing last-known remote refs)"
    bump 2
  fi
fi

# --- step 5: local working-tree state (ref-relative values are post-fetch) -
porcelain="$(git_q status --porcelain)"
sw_local=false      # dirty/untracked under skills/ or workflows/  → HIGH
other_tracked=false # tracked change outside those dirs            → MEDIUM
other_untracked=false # untracked outside those dirs               → LOW
if [ -n "$porcelain" ]; then
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    code="${line:0:2}"
    path="${line:3}"
    # rename: "old -> new"; classify on the destination path.
    case "$path" in *" -> "*) path="${path##* -> }";; esac
    case "$path" in
      skills/*|workflows/*) sw_local=true ;;
      *) if [ "$code" = "??" ]; then other_untracked=true; else other_tracked=true; fi ;;
    esac
  done <<EOF
$porcelain
EOF
fi
[ "$sw_local" = true ] && bump 3
[ "$other_tracked" = true ] && bump 2
[ "$other_untracked" = true ] && bump 1

ahead=0
if [ -n "$ref" ]; then
  ahead="$(git_q rev-list --count "${ref}..HEAD")"
  [ -z "$ahead" ] && ahead=0
fi
[ "$ahead" -gt 0 ] && bump 3

# --- step 6: incoming (merge-base range) ----------------------------------
incoming_commits=""
incoming_files=""
mb_unresolved=false
if [ -n "$ref" ]; then
  incoming_commits="$(git_q log --oneline "HEAD..${ref}")"
  base="$(git_q merge-base HEAD "$ref")"
  if [ -z "$base" ]; then
    mb_unresolved=true
    bump 2
  else
    incoming_files="$(git_q diff --name-status "${base}..${ref}" -- skills/ workflows/)"
  fi
fi

# --- assemble report ------------------------------------------------------
remote_url="$(git_q remote get-url "${ref_remote:-origin}")"
ref_disp="${ref:-UNRESOLVED}"
ref_sha=""
[ -n "$ref" ] && ref_sha="$(git_q rev-parse --short "$ref")"

echo "==> Upstream status for: $REPO"
echo "Branch:        $branch"
echo "HEAD:          ${head_sha}"
if [ -n "$ref_sha" ]; then
  echo "Upstream ref:  ${ref_disp} (${ref_sha}) [source: ${resolution_source}]"
else
  echo "Upstream ref:  ${ref_disp} [source: ${resolution_source}]"
fi
[ "$override_no_remote" = true ] && echo "               (override had no extractable remote — fetch skipped)"
echo "Remote URL:    ${remote_url:-<none>} (display only)"
[ -n "$fetch_note" ] && echo "Fetch:         ${fetch_note}"
echo

echo "Local working-tree state:"
if [ -n "$porcelain" ]; then
  echo "$porcelain" | sed 's/^/  /'
else
  echo "  (clean)"
fi
echo "  Local commits ahead of upstream: ${ahead}"
echo

echo "Incoming from ${ref_disp}:"
if [ -z "$ref" ]; then
  echo "  (skipped — no trackable upstream ref)"
else
  if [ -n "$incoming_commits" ]; then
    echo "  Commits:"
    echo "$incoming_commits" | sed 's/^/    /'
  else
    echo "  Commits: (none — up to date with ${ref_disp})"
  fi
  if [ "$mb_unresolved" = true ]; then
    echo "  merge-base: UNRESOLVED (incoming file list skipped)"
  elif [ -n "$incoming_files" ]; then
    echo "  Changed files under skills/ and workflows/:"
    echo "$incoming_files" | sed 's/^/    /'
  else
    echo "  Changed files under skills/ and workflows/: (none)"
  fi
fi
echo

case "$sev" in
  0) label="NONE" ; action="safe to 'git pull' manually after reviewing the incoming list above." ;;
  1) label="LOW" ; action="review the untracked files, then pull." ;;
  2) label="MEDIUM"; action="judgement needed before pull — resolve the flags above first." ;;
  3) label="HIGH" ; action="do NOT pull. Review local edits first (Hermes-edited skills may live here)." ;;
esac
echo "Local-edit risk: ${label}"
echo "Recommended:     ${action}"
echo

echo "Notes:"
echo "  - This report is working-tree safe: it fetched remote metadata only and"
echo "    did not pull / merge / rebase / stash or touch any skill file."
echo "  - The TICKET-004b drift guard (make test / make validate-all) catches"
echo "    mapping/upstream divergence AFTER you pull; this is the before-pull"
echo "    counterpart."
echo "  - For permanent ownership separation between upstream tracking and your"
echo "    local edits, see vendored mode (TICKET-008) in"
echo "    docs/04-skill-integration-strategy.md."

exit 0
