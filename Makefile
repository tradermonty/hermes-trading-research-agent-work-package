.PHONY: validate validate-upstream validate-all test sync-external sync-external-write sync-vendor sync-vendor-write

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

# DANGEROUS: regenerates bundle instructions from data/skill-mapping.yaml.
# Manual instruction edits in skill-bundles/*.yaml will be overwritten.
# Phase 3b prompts/ were rewritten to pass Hermes' deception_hide threat scanner;
# build_instruction() now uses positive-form required-concepts wording, so the
# regenerated output should still satisfy tests/test_required_sections.py and
# tests/test_output_safety.py — but always re-run `make test` after this target.
sync-external-write:
	@echo "WARNING: --write regenerates bundle instructions from data/skill-mapping.yaml."
	@echo "         Manual instruction edits will be lost. Run 'make test' after this."
	@test -n "$${REQUIRE_SYNC_WRITE}" || \
	  (echo "Refusing to run sync-external-write without REQUIRE_SYNC_WRITE=1" >&2; exit 2)
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode external --write
	@echo "Re-running safety + required-concepts tests against regenerated bundles..."
	$(PYTHON) -m pytest -q tests/test_output_safety.py tests/test_required_sections.py

sync-vendor:
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode vendor

sync-vendor-write:
	@echo "WARNING: --write copies upstream skills into skills/vendor/ and overwrites bundles."
	@test -n "$${REQUIRE_SYNC_WRITE}" || \
	  (echo "Refusing to run sync-vendor-write without REQUIRE_SYNC_WRITE=1" >&2; exit 2)
	$(PYTHON) $(SYNC_SCRIPT) --source "$${CLAUDE_TRADING_SKILLS_REPO}" --profile-root . --mode vendor --write
