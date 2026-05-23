# Complete Text Analysis Agent Prompt

## Your Task

Expand text `analysis_html` fields from stubs (50–300 words) to **1,000–1,800 words** of comprehensive scholarly analysis.

## Structure (MANDATORY)

**Opening (200–300 words):**
- Full title in italics
- Author/attribution (note if contested)
- Date of composition or earliest attestation
- Original language
- Type: PRIMARY_SOURCE, COMMENTARY, COMPILATION, TREATISE, SCHOLARSHIP, ENCYCLOPEDIA
- One sentence on significance

**`<h2>Content and Theory</h2>`** (300–500 words):
- What does the text argue or teach?
- Key doctrines, operations, theoretical claims
- Specific sections or chapters cited by historians
- Be specific—quote or paraphrase actual content

**`<h2>Composition and Textual Tradition</h2>`** (200–400 words):
- How did this text survive?
- Manuscript tradition, translations, versions
- Key transmitters (scribes, translators, scholars)
- Authorship questions if contested

**`<h2>Modern Scholarship</h2>`** (150–300 words):
- Which scholars produced authoritative editions/translations?
- Current scholarly debates about authenticity, dating, significance
- If contested, name scholars and their positions

**`<h2>Literature</h2>`** (5–12 entries):
Format: Author. *Title*. Publisher, Year.

## Historiographical Standards

- **Ground claims in named sources**: "Newman's 1991 edition argues that..."
- **Distinguish primary from scholarship**: Explicit about which is which
- **Medieval continuity**: Trace transmission chains
- **Chemical operations are real**: Describe distillation, sublimation as genuine chemistry
- **Proper attribution**: Distinguish authorial attribution from scholarly consensus

## HTML Structure

Valid tags: `<p>`, `<h2>`, `<i>` (titles, foreign terms), `<b>` (sparingly)
NO markdown, bullets, hashtags.

## Entity Linking

`[LINK:slug]` for persons, texts, concepts. Do NOT link generic terms.

## Example Output Structure

```json
{
  "slug": "summa-perfectionis",
  "analysis_html": "[FULL 1,000-1,800 WORD HTML ANALYSIS]",
  "metadata": {
    "word_count": 1450,
    "sections_included": ["opening", "Content and Theory", "Composition and Textual Tradition", "Modern Scholarship", "Literature"],
    "entities_linked": 8,
    "confidence": "HIGH",
    "review_status": "DRAFT"
  }
}
```

## Validation

- [ ] Word count: 1,000–1,800?
- [ ] Opening: 200–300 words?
- [ ] Named sections: 200–500 words each?
- [ ] Literature: 5–12 DGWE entries?
- [ ] All titles italicized?
- [ ] Entity links: `[LINK:slug]` format?
- [ ] No markdown/bullets/hashtags?
- [ ] Claims grounded in sources?
- [ ] Valid HTML?

---

**Begin writing comprehensive text analyses.**
