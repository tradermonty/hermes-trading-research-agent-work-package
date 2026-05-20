# Missing Skills / Degraded-Mode Acceptances

This file documents intentionally accepted missing upstream skills.

`scripts/validate_upstream_index.py` reads this file and treats any skill name
listed here as an accepted degraded-mode entry, allowing the validator to exit 0
even though the skill is not present in `claude-trading-skills/skills-index.yaml`.

## Current status

No accepted missing skills. The v0.1.0 release resolves all 9 bundle / mapping
references against the upstream index (55 skills + 3 profile-local skills).

## Format

When adding an accepted miss, use one entry per line with the skill name in
backticks and the word `degraded` (any case) on the same line:

```
- `some-removed-skill` — degraded-mode accepted. Reason: upstream rename pending, bundle falls back to manual chart review.
- `another-skill` — degraded mode is fine; users without this key fall back to public sources.
```

The validator matches the skill name inside backticks; the rest of the line is
free-form prose. See `scripts/validate_upstream_index.py:documented_missing()`
for the exact parser.
