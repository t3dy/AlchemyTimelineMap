# Person Biography Specification

**Lifetime:** Read when writing or expanding person biographies. Layer 3 (Operational Standards).

**Authority:** If this contradicts `docs/SCHEMA.json`, the schema wins.

**Prerequisite:** Read `CONCEPTUAL_FRAMEWORK.md` before writing — biographies require historiographical judgment (Actor/Analyst distinction, material culture grounding, scholarly dispute framing).

---

## Word Count

**1,200–2,200 words** (excluding Literature section)  
**Format:** Valid HTML — `<p>`, `<h2>`, `<i>`, `<b>` tags only

---

## Opening Paragraph (200–350 words)

Begin with the person's full name. Include:
- Full name with alternate names/transliterations (e.g., *Geber* for Jabir ibn Hayyan)
- Birth–death dates or floruit period ("fl. c. 1290")
- Geographic origin and primary location(s)
- Primary role (`role_primary` enum value) and era (`era` enum value)
- One sentence of historical significance to alchemy/chemistry

Do **not** begin with "This figure was..." or "This person is..." Begin with the name.

**Example opening:**

> Jabir ibn Hayyan (c. 722–815), known to Western alchemists as *Geber*, was an Arab polymath and alchemist active in the 8th century whose vast corpus shaped the development of practical chemistry for over a millennium. Whether Jabir authored all texts attributed to him remains contested — Lawrence Principe argues for multiple authors; William Newman defends substantial Jabir authorship — but the *Corpus Jabirianum* collectively established systematic distillation, acid production, and metal-working as core alchemical operations rooted in reproducible chemical reactions.

---

## Main Sections

### For Historical Alchemists/Chemists (minimum 2 of these, 250–400 words each)

**`<h2>Works and Intellectual Context</h2>`**
- Specific treatises authored or major compilations
- Key arguments and doctrines presented
- Sources and influences; institutional context (court, university, monastery, workshop)
- Integration with contemporary philosophy, medicine, or natural history
- Cite specific texts and sections by name

**`<h2>Alchemical Significance</h2>`**
- Specific contributions to operational chemistry
- Transmutation theory and claims
- Material grounding: what was actually done in the laboratory? What equipment (furnaces, retorts, crucibles)? What dangers (toxins, explosions, burns)? What observable results?
- Innovations or refinements to technique

**`<h2>Transmission and Reception</h2>`**
- How were texts transmitted (manuscript, print, translation)?
- Key medieval or Renaissance interpreters
- Citation history; influence on successors (name them)
- Modern editions and translations

**`<h2>Scholarly Debates</h2>`**
- Historiographical disagreements about authorship, dating, significance
- Name scholars explicitly and state their specific positions
- Present evidence for competing views; do not hide disagreement

### For Modern Scholars (minimum 2 of these, 250–400 words each)

**`<h2>Central Thesis</h2>`** — distinctive argument, what interpretations challenged, which sources emphasized

**`<h2>Key Works</h2>`** — 2–4 major publications with dates and brief description of each work's argument

**`<h2>Methodological Approach</h2>`** — theoretical framework, primary vs. secondary sources, geographic or temporal focus, interdisciplinary methods

**`<h2>Scholarly Disputes</h2>`** — influences, challenges, agreements, evolution of thinking

---

## Literature Section (5–12 references)

**DGWE format:**
```
Newman, William R. Atoms and Alchemy: Chymistry and the Transformation of Matter. University of Chicago Press, 2006.

Principe, Lawrence M. The Secrets of Alchemy. University of Chicago Press, 2013.
```

Rules: Author last name first; full title in italics; full publisher name; year of publication; alphabetized by author; no URLs or DOIs.

---

## Italics Policy

- **Text titles:** *Summa Perfectionis*, *Emerald Tablet*, *Atalanta Fugiens*
- **Foreign terms on first use:** *calcination*, *sublimatio*, *quinta essentia*
- **NOT italicized:** proper names of persons, places, institutions

---

## Validation Checklist

- [ ] Total word count 1,200–2,200 (excluding Literature)?
- [ ] Opens with person's name (not "This figure...")?
- [ ] Opening paragraph includes dates, role, era, significance?
- [ ] At least 2 main `<h2>` sections present?
- [ ] Each main section 250–400 words?
- [ ] Material grounding included for historical figures?
- [ ] Scholarly disputes named with specific scholars and positions?
- [ ] Literature section: 5–12 references in DGWE format?
- [ ] Text titles italicized; proper names NOT italicized?
- [ ] All claims traced to named sources?
- [ ] All entity names marked `[LINK:slug]` where applicable?
- [ ] At least 3 entity links total?
- [ ] No markdown artifacts?
- [ ] Provenance metadata: `source_method`, `review_status`, `confidence`?
- [ ] `role_primary` and `era` values from `docs/VOCABULARY.md`?

---

## What Fails Validation

- **Under 1,200 words** — insufficient depth; reject
- **No scholarly disputes section** — even well-documented figures have historiographical debate
- **Hagiographic tone** — treating historical alchemists as heroes, not historical subjects
- **No material grounding for historical figures** — biography without operational chemistry is incomplete
- **"As a pioneering genius..."** — avoid evaluative language without grounding in scholarship

---

*For historiographical principles (Actor/Analyst distinction, material culture, scholarly authorities), see `CONCEPTUAL_FRAMEWORK.md`. For enum values, see `docs/SCHEMA.json`.*
