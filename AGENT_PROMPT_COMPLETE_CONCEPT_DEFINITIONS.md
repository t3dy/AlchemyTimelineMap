# Complete Concept Definition Agent Prompt

## Your Task

Expand concept definitions to **1,500–2,500 words** of comprehensive encyclopedia-length content.

## Structure (MANDATORY)

**Opening (150–250 words):**
- Term in primary language (*Distillatio*, *Sublimatio*, etc.)
- Category: ACTOR_TERM (used by historical figures) or ANALYST_TERM (used by modern scholars)
- Historical period of primary use
- One sentence of foundational significance

**`<h2>Historical Development</h2>`** (300–400 words):
- Origins of the term/concept
- Evolution through different periods (Islamic, Medieval, Renaissance, Early Modern)
- Key figures associated with development
- Transmission history

**`<h2>Operational Definition</h2>`** (350–450 words):
- For ACTOR_TERMS (operations): Describe the actual laboratory procedure
- Apparatus used
- Materials and proportions
- Expected results
- Variations and modifications across different alchemists
- How did this operation relate to transmutation theory?

**`<h2>Theoretical Significance</h2>`** (300–400 words):
- What did this concept mean philosophically?
- Relationship to natural philosophy (Aristotelian, Neo-Platonic, etc.)
- Cosmological implications
- Integration with medicine, theology, or other fields
- How did theory justify practice?

**`<h2>Modern Scholarship and Interpretation</h2>`** (250–350 words):
- How do modern historians understand this concept?
- Has interpretation changed?
- Key scholarly works on this concept
- Current debates
- Relationship to modern chemistry (for operations)

**`<h2>Related Concepts</h2>`** (150–250 words):
- How does this concept relate to other alchemical concepts?
- Cross-references to distillation, sublimation, calcination, etc.
- Integration with larger theoretical systems

**`<h2>Literature</h2>`** (5–10 entries):
Format: Author. *Title*. Publisher, Year.

## Content Standards

### For Operational Concepts (Distillation, Sublimation, Calcination, etc.):

Describe the actual chemistry:
- Equipment (alembics, retorts, furnaces)
- Procedure (heating sequence, materials, proportions)
- Observable results (color changes, phase transitions)
- Documented variations
- Success/failure rates and what determined them

Example: *Distillation* involved heating a liquid in a vessel with a condensing apparatus (alembic), collecting the vaporized and re-condensed liquid. Used for preparing aqua vitae (alcohol), aqua fortis (nitric acid), aqua regia, and various plant/mineral extracts.

### For Theoretical Concepts (Transmutation, Quintessence, Spirit, etc.):

- Historical definitions
- Philosophical underpinnings
- Integration with cosmology
- Relationship to practice
- Evolution of understanding

Example: *Transmutation* theory held that base metals (lead, copper, tin) differed from gold only in the purity and proportion of their fundamental components (sulfur and mercury in Islamic tradition; primary and secondary qualities in scholastic terms). If one could alter these proportions, base metals could become gold.

## Historiographical Standards

- **Ground in named sources**: "As William Newman argues in *Atoms and Alchemy*..."
- **Distinguish historical from modern understanding**: "Alchemists believed X; modern chemistry shows Y"
- **Operations as real chemistry**: Describe distillation as genuine chemical process with measurable results
- **Trace transmission**: Show how concepts evolved and transmitted across cultures
- **Actor/analyst distinction**: Note whether term is from historical sources or modern scholarly invention

## HTML Structure

Valid tags: `<p>`, `<h2>`, `<i>`, `<b>`
NO markdown, bullets, hashtags.

## Entity Linking

`[LINK:jabir-ibn-hayyan]` for persons
`[LINK:summa-perfectionis]` for texts
`[LINK:distillation]` for related concepts

## Example Output

```json
{
  "slug": "distillation",
  "definition_long": "[FULL 1,500-2,500 WORD HTML DEFINITION]",
  "definition_short": "[60-120 WORD INDEX CARD]",
  "metadata": {
    "word_count": 2100,
    "sections_included": ["opening", "Historical Development", "Operational Definition", "Theoretical Significance", "Modern Scholarship", "Related Concepts", "Literature"],
    "entities_linked": 12,
    "category_type": "ACTOR_TERM",
    "confidence": "HIGH",
    "review_status": "DRAFT"
  }
}
```

## Validation Checklist

- [ ] Word count: 1,500–2,500?
- [ ] Opening: 150–250 words?
- [ ] All sections 250–450 words?
- [ ] Literature: 5–10 DGWE entries?
- [ ] Entity links: `[LINK:slug]` format?
- [ ] All titles italicized?
- [ ] No markdown/bullets/hashtags?
- [ ] Claims grounded in sources?
- [ ] Valid HTML?
- [ ] Short definition (index card): 60–120 words?

---

**Begin writing comprehensive concept definitions.**
