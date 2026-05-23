# Concept Definition Specification

**Lifetime:** Read when writing or expanding concept definitions. Layer 3 (Operational Standards).

**Authority:** If this contradicts `SCHEMA.json`, the schema wins.

**Prerequisite:** Read `CONCEPTUAL_FRAMEWORK.md` §§ 3.2 and 3.4 — the Actor/Analyst distinction and material culture framework are essential for this content type.

---

## Word Count

**`definition_short`:** 60–120 words (index card, plain text)  
**`definition_long`:** 1,500–2,500 words (encyclopedia article, valid HTML)  
**Format:** Valid HTML — `<p>`, `<h2>`, `<i>`, `<b>` tags only

---

## CRITICAL: ACTOR_TERM vs. ANALYST_TERM

**Every concept definition must explicitly declare which type in the opening paragraph.**

### ACTOR_TERM
A term used by historical practitioners who would recognize it.
- Examples: *distillatio*, *calcination*, *transmutatio*, *coagulatio*, *quintessence*
- Requires material grounding: what equipment, what dangers, what observable results
- Grounds the term in primary sources describing actual laboratory practice

### ANALYST_TERM
A retrospective scholarly category. Historical actors may not have recognized this rubric.
- Examples: *Hermeticism*, *esotericism*, *alchemy* (as a modern historiographical category)
- Requires attention to historiographical disputes: who invented this category? Is it coherent?
- Named scholars must debate the term's validity and boundaries

---

## Opening Paragraph (150–250 words)

State the term, ideally in its primary language. **Explicitly declare ACTOR_TERM or ANALYST_TERM.** Give earliest attestation. Establish significance.

Do **not** begin with "This term..." Begin with the term itself.

**Example — ACTOR_TERM:**

> Distillatio (Latin; also *distillation* in English, *dhiqa* in some Arabic texts) was an operational term used by medieval and early modern alchemists to describe the separation of substances by heating and condensation. This is an ACTOR_TERM — historical practitioners explicitly used this word and would recognize the concept. One of the oldest recorded alchemical procedures, distillation appears in Zosimos's 3rd-century texts and is central to the *Corpus Jabirianum*. It produced reproducible, observable results — volatile essences, concentrated liquids, refined metals — and became foundational to both alchemical theory and the practical chemistry that would eventually emerge from it.

**Example — ANALYST_TERM:**

> Hermeticism is a modern scholarly category for a complex of ideas ostensibly derived from the Hermetic corpus (*Corpus Hermeticum*), though Wouter J. Hanegraaff and others have questioned whether historical actors would have recognized themselves under this rubric. This is an ANALYST_TERM — a retrospective category imposed after the fact. The term gained currency in 20th-century esotericism studies, though contemporary usage masks significant historiographical disputes about periodization, boundaries, and whether "Hermeticism" is a coherent tradition or a scholarly fiction.

---

## Required Sections

### `<h2>Historical Usage</h2>` (400–600 words)

Trace the term from earliest attestation through Late Antiquity, medieval Islam, medieval Latin, Renaissance, and early modernity.
- Name specific texts and authors
- Show shifts in meaning over time

**For ACTOR_TERMs — material grounding (required):**
- What tools or equipment? (furnaces, retorts, crucibles, glass apparatus)
- What dangers? (toxins, explosions, burns, respiratory hazards)
- What sensory experiences? (heat, smell, color changes in distillates)
- What observable results? (vapors, precipitates, refined metals)
- How did practitioners learn and transmit this knowledge?

**For ANALYST_TERMs — terminological history (required):**
- Show how the term traveled across cultures and languages
- How did translations alter meaning?
- How did practitioners in different contexts understand it differently?

### `<h2>Scholarly Significance</h2>` (400–600 words)

**Name scholars explicitly. State their specific arguments.** This is non-negotiable.
- William R. Newman's view?
- Lawrence Principe's view?
- Pamela Smith's view?
- Hanegraaff's view?
- Where do they disagree? What evidence does each cite?

Example structure: "William R. Newman has argued that distillation was primarily an operational technique... However, Lawrence Principe emphasizes that many alchemists also attributed transmutational significance to distillation... Pamela Smith's work on artisanal epistemology suggests this disagreement reflects a false binary..."

### `<h2>Transmission and Variant Forms</h2>` (200–400 words) — Optional

Include if the term has Greek, Arabic, Latin, or Hebrew variants, or if its meaning shifted significantly in translation.

### `<h2>Related Concepts</h2>` (100–200 words)

Link to 3–5 related entries using **prose sentences**, not a bullet list. Explain the relationships.

Example: "Distillation is closely related to [LINK:sublimation], which also involves vaporization but produces a solid directly without an intermediate liquid state. Both operations were understood as forms of separation and refinement in medieval alchemy. Distillation also connects to [LINK:calcination] and [LINK:dissolution]..."

---

## Literature Section (8–15 references)

**DGWE format:**
```
Newman, William R. Atoms and Alchemy: Chymistry and the Transformation of Matter. University of Chicago Press, 2006.

Hanegraaff, Wouter J., editor. Dictionary of Gnosis and Western Esotericism. Brill, 2006.
```

Concept definitions warrant slightly longer bibliographies (8–15) than other content types.

---

## Validation Checklist

### General
- [ ] `definition_short` 60–120 words (plain text)?
- [ ] `definition_long` 1,500–2,500 words (HTML)?
- [ ] ACTOR_TERM or ANALYST_TERM declared explicitly in opening paragraph?
- [ ] All required sections present?
- [ ] Named scholars with specific arguments in Scholarly Significance?
- [ ] Literature: 8–15 references in DGWE format?
- [ ] Related Concepts written as prose (not bullets)?
- [ ] At least 3 entity links marked `[LINK:slug]`?
- [ ] No markdown artifacts?
- [ ] Provenance metadata: `source_method`, `review_status`, `confidence`?
- [ ] `category_type` value is ACTOR_TERM or ANALYST_TERM?

### ACTOR_TERM additional checks
- [ ] Material grounding present (equipment, dangers, observable results)?
- [ ] Grounded in primary source texts (cited by name)?
- [ ] Sensory/embodied dimension present?

### ANALYST_TERM additional checks
- [ ] Terminological history present (who invented this category)?
- [ ] Historiographical disputes discussed?
- [ ] Whether historical actors used the term is addressed?

---

## What Fails Validation

- **No ACTOR_TERM/ANALYST_TERM declaration** — reject immediately; this is non-negotiable
- **No material grounding for ACTOR_TERMs** — operational terms without laboratory context are incomplete
- **"Scholars agree that..."** without naming scholars — generic attribution fails the standard
- **Related Concepts as a bullet list** — must be prose sentences with `[LINK:slug]` markup
- **Under 1,500 words** — concept definitions require encyclopedic depth

---

*For the theoretical foundation of the Actor/Analyst distinction and material culture framework, see `CONCEPTUAL_FRAMEWORK.md` §§ 3.2 and 3.4. For enum values, see `SCHEMA.json`.*
