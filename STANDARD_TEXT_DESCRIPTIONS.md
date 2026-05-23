# Text Description Specification

**Lifetime:** Read when writing or expanding text descriptions. Layer 3 (Operational Standards).

**Authority:** If this contradicts `docs/SCHEMA.json`, the schema wins.

**Prerequisite:** Read `CONCEPTUAL_FRAMEWORK.md` — text descriptions require understanding of textual transmission, the Actor/Analyst distinction, and historiographical significance.

---

## Word Count by Text Type

**Format:** Valid HTML — `<p>`, `<h2>`, `<i>`, `<b>` tags only

| `text_type` | Word Count (excl. Literature) |
|------------|-------------------------------|
| PRIMARY_SOURCE | 1,000–1,800 words |
| COMMENTARY | 800–1,200 words |
| COMPILATION | 800–1,400 words |
| TREATISE | 1,000–1,800 words |
| SCHOLARSHIP | 800–1,200 words |
| ENCYCLOPEDIA | 1,000–1,600 words |

---

## Opening Paragraph (200–300 words)

Begin with the full title of the text in italics. Include:
- Full title in original language if known, italicized: *Summa Perfectionis*, *Kitāb al-Ḥāsib*
- Date of composition or earliest attestation
- Original language (Latin, Arabic, Greek, Hebrew, English)
- `text_type` (PRIMARY_SOURCE, COMMENTARY, etc.)
- Author or tradition attribution
- One sentence of historical significance

Do **not** begin with "This text..." Begin with the title.

**Example opening:**

> *The Summa Perfectionis* (attributed to Jabir ibn Hayyan; also known as *Liber Claritatis*) is a foundational medieval Latin alchemical text of disputed authorship and composition date. Most modern scholars (William R. Newman, Michela Pereira) argue for 13th-century Latin European authorship rather than 8th-century Jabir attribution, though the text itself claims Jabir tradition. Composed in Latin and widely copied in European monastery libraries, the *Summa* systematically presents alchemical operations — distillation, sublimation, calcination — as reproducible laboratory procedures with measurable results, establishing alchemy in medieval Europe as a legitimate natural philosophy.

---

## Required Sections

### `<h2>Content and Theory</h2>` (300–500 words)

- What arguments or doctrines does the text present?
- Key chapters or sections cited by historians
- Specific operations described (distillation, sublimation, fermentation)
- Theoretical claims about matter, transmutation, causation
- Integration with contemporary philosophy or theology
- Be specific — cite actual text passages or sections by name

### `<h2>Composition and Textual Tradition</h2>` (200–400 words) — Required for PRIMARY_SOURCE, COMMENTARY, TREATISE, COMPILATION

- How did this text survive and circulate?
- Manuscript tradition: copies, versions, variants
- Translations and intermediaries (who translated? when? what languages?)
- Key transmitters: scribes, translators, scholars
- Modern editions and translations (cite by scholar name and date)

### `<h2>Modern Scholarship</h2>` (150–300 words)

- Which scholars have produced authoritative editions or translations?
- Current scholarly debates about authorship, dating, significance
- Name specific scholars and their specific arguments
- If authorship is contested, present evidence for competing views

---

## Literature Section (5–12 references)

**DGWE format:**
```
Newman, William R. The Summa Perfectionis of Pseudo-Geber. Brill, 1991.

Pereira, Michela. The Alchemical Corpus Attributed to Ray Lull. Brill, 2007.
```

Rules: Author last name first; full title in italics; full publisher name; year; alphabetized; no URLs.

---

## Italics Policy

- **Text titles:** *Summa Perfectionis*, *Emerald Tablet*, *Kitāb al-Ḥāsib*
- **Foreign terms on first use:** *calcination*, *sublimatio*, *dhiqa*
- **NOT italicized:** names of persons, places, institutions, scribes

---

## Validation Checklist

- [ ] Word count in range for `text_type` (see table above)?
- [ ] Opens with title in italics (not "This text...")?
- [ ] Opening includes date, language, type, author, significance?
- [ ] Content and Theory section present (300–500 words)?
- [ ] Textual Tradition section present (for primary sources)?
- [ ] Modern Scholarship section present?
- [ ] Literature: 5–12 references in DGWE format?
- [ ] Text titles italicized throughout?
- [ ] Specific scholars named in each section?
- [ ] All entity names marked `[LINK:slug]` where applicable?
- [ ] At least 3 entity links total?
- [ ] No markdown artifacts?
- [ ] Provenance metadata: `source_method`, `review_status`, `confidence`?
- [ ] `text_type` value from `docs/VOCABULARY.md`?

---

## What Fails Validation

- **Begins with "This text is..."** — start with the title
- **No textual tradition section for primary sources** — provenance of the manuscript tradition is essential
- **No named scholars** — generic "scholars argue" without attribution fails the standard
- **Conflates authorship attribution with historical authorship** — "Jabir wrote this" vs. "the text is attributed to Jabir by medieval tradition"
- **Modern scholarship section missing** — required for all content types

---

*For historiographical context (textual transmission, Actor/Analyst distinction, scholarly authorities), see `CONCEPTUAL_FRAMEWORK.md`. For enum values, see `docs/SCHEMA.json`.*
