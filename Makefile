.PHONY: validate validate-upstream validate-all test sync-external sync-external-write sync-external-write-force sync-vendor sync-vendor-write

PYTHON ?= python3
SYNC_SCRIPT := scripts/sync_claude_trading_skills.py
UPSTREAM_VALIDATOR := scripts/validate_upstream_index.py

# Structural validation only. No upstream repo required.
validate:
	$(PYTHON) scripts/validate_package.py --profile-root .

# Canonical upstream index integrity check. Requires CLAUDE_TRADING_SKILLS_REPO.
validate-upstream:
	@test -n "$${CLAUDE_TRADING_SKILLS_REPO}" || \
	  (echo "CLAUDE_TRADING_SKILLS_REPO is required for validate-upstream" >&2; exit 2)
	$(PYTHON) $(UPSTREAM_VALIDATOR) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root .

# Full release-gate: structural + upstream + tests. Requires CLAUDE_TRADING_SKILLS_REPO.
validate-all: validate validate-upstream test

test:
	$(PYTHON) -m pytest -q

# Diagnostic dry-run. Safe by default — does not touch skill-bundles/*.yaml.
sync-external:
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode external

# Safe writer (post-B-2a): only writes new bundles or `x-generated: true` bundles
# whose rendered content actually differs from disk. Bundles marked
# `x-generated: false` (or missing the key entirely) are SKIPPED with a stderr
# WARNING. Against the shipped tip, this target is a no-op: ten SKIP lines and
# zero rewrites. Use sync-external-write-force to bypass protection.
sync-external-write:
	@test -n "$${REQUIRE_SYNC_WRITE}" || \
	  (echo "Refusing to run sync-external-write without REQUIRE_SYNC_WRITE=1" >&2; exit 2)
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode external --write
	@echo "Re-running safety + required-concepts tests in case anything was rewritten..."
	$(PYTHON) -m pytest -q tests/test_output_safety.py tests/test_required_sections.py

# DANGEROUS: --force-overwrite ignores `x-generated: false` and the missing-key
# legacy guard. Every bundle the mapping references will be rewritten. Hand
# edits will be lost. Double-gated to make a accidental run virtually impossible.
sync-external-write-force:
	@echo "WARNING: --force-overwrite ignores x-generated: false and bypasses legacy-unknown protection."
	@echo "         All matching bundles will be rewritten and lose hand edits."
	@test -n "$${REQUIRE_SYNC_WRITE}" || \
	  (echo "Refusing to run sync-external-write-force without REQUIRE_SYNC_WRITE=1" >&2; exit 2)
	@test -n "$${REQUIRE_FORCE_OVERWRITE}" || \
	  (echo "Refusing to run sync-external-write-force without REQUIRE_FORCE_OVERWRITE=1" >&2; exit 2)
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode external --write --force-overwrite
	@echo "Re-running safety + required-concepts tests against regenerated bundles..."
	$(PYTHON) -m pytest -q tests/test_output_safety.py tests/test_required_sections.py

sync-vendor:
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode vendor

sync-vendor-write:
	@echo "WARNING: --write copies upstream skills into skills/vendor/ and (re)writes vendor-manifest.json."
	@echo "         Bundle-side writes still honor B-2a ownership: x-generated: false / legacy bundles are SKIPPED;"
	@echo "         use sync-external-write-force (or pass --force-overwrite) to bypass bundle protection."
	@test -n "$${REQUIRE_SYNC_WRITE}" || \
	  (echo "Refusing to run sync-vendor-write without REQUIRE_SYNC_WRITE=1" >&2; exit 2)
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode vendor --write
