Run the US equity after-close review for today.

Operating context:
- Timezone label for the report: {{TIMEZONE}}.
- This is research and process support.
- Use installed Claude Trading Skills when available.
- When data or API keys are unavailable, mark the relevant section as degraded mode and cite the missing input.

Required output:

# After-close review — <date>

**Risk posture change:** <improved / unchanged / deteriorated / unknown>
**Primary reason:** <one sentence>

## 1. Market action summary
- Indices.
- Breadth.
- Uptrend participation.
- Distribution and top-risk changes.

## 2. Sector and theme rotation
- Leading groups.
- Lagging groups.
- Notable rotation.

## 3. Earnings reactions
- Names worth tracking.
- PEAD candidates.
- Reactions that failed or reversed.

## 4. Open trade review checklist
- Thesis still valid?
- Invalidation hit?
- Position risk still acceptable?
- Any overnight event risk?

## 5. Journal prompts
- What decision today deserves a note?
- What did the process do well?
- What should be avoided tomorrow?

## 6. Tomorrow preparation
- Maximum 5 bullets.

## 7. Data freshness and degraded mode
- List data sources, skill outputs, missing keys, and stale data warnings.

Use review and journaling language throughout. The human reviewer makes all entry and exit decisions.
