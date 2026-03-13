---
name: product-strategy-doc
description: Generate comprehensive product strategy documents covering vision, market analysis, OKRs, strategies, roadmap, and risks. Use when the user asks to create a product strategy, product plan, strategic roadmap, or any document that defines product direction with market context and measurable goals. Triggers on requests like "write a product strategy", "create a strategy doc", "help me plan product direction", or "draft a product roadmap".
---

# Product Strategy Document

Generate structured, decision-driven product strategy documents.

## Workflow

1. **Gather context** — Ask the user for: product name, current stage (idea/MVP/growth/mature), target market, and any existing vision or constraints. Do not proceed without at least the product name and target market.

2. **Load template** — Read `references/template.md` for the full 6-section structure.

3. **Draft section by section** — Work through each section in order:
   - **Vision & Mission** — Must be stable over years, not quarters
   - **Market Analysis** — Require specific data/trends, reject generic observations
   - **OKRs** — Must ladder from vision to measurable outcomes with baselines and targets
   - **Strategies** — Cover product dev, marketing/sales, and customer success
   - **Roadmap** — Include sequencing rationale explaining why this order
   - **Risks & Success Criteria** — Define 3/6/12 month checkpoints

4. **Review and refine** — Present the draft, iterate on user feedback.

## Quality Rules

- Every section must contain decisions or insights that change behavior — no filler
- Market analysis needs specific data, not generic industry platitudes
- OKRs must have concrete metrics with baselines and targets
- Roadmap must explain sequencing rationale — why this order matters
- Connect every section back to the product vision

## Output Format

Default to Markdown. If the user requests .docx or .pdf, use the appropriate document skill.

## References

- **Full template with all section prompts**: See [references/template.md](references/template.md)
