# ALCHEMYTIMELINEMAP Content Style Guide

**MANDATORY:** All agents, scripts, and contributors must consult this file before writing any prose for the database. This guide is the single source of truth for all content standards.

---

## § 1: The Core Standard — Encyclopedia Prose

Every entry — whether a timeline event, person biography, text description, or concept definition — must read like a **scholarly encyclopedia article**.

**Model:** *Dictionary of Gnosis and Western Esotericism* (Hanegraaff, Brill, 2006) and *The Cambridge History of Science*

**Tone:** Authoritative, precise, readable, provenance-aware. Third person. No typographic artifacts.

---

## Absolute Prohibitions

The following are **never acceptable** in any prose field:

- **Hashtags:** `#` in any context
- **Square brackets (except [LINK:slug]):** `[text]` or `[[text]]`
- **Curly braces:** `{placeholder}` or `{{field}}`
- **Asterisks for emphasis:** `*text*` or `**text**`
- **Markdown headers:** `## Heading` (use `<h2>` HTML instead)
- **Bullet points:** `- item` or `* item`
- **Emoji or decorative symbols:** ☿ 🜍 ⚗ (use text instead)
- **Template strings:** `entity["people", "Name", 0]`
- **Placeholder text:** "To be added," "N/A," "TBD"

**All prose must be plain text or valid HTML (`<p>`, `<h2>`, `<i>`, `<b>` tags only).**

---

## § 2: Person Biographies (bio_html field)

### General Requirements

**Length:** 1,200–2,200 words (excluding Literature section)  
**Format:** Valid HTML with `<p>`, `<h2>`, `<i>`, `<b>` tags only

Every biography must contain:

### 2.1: Opening Paragraph (200–350 words)

Begin with the person's full name. Include:
- Full name (with alternate names/transliterations if applicable)
- Birth–death dates or floruit period (e.g., "fl. c. 1290")
- Geographic origin and primary location(s)
- Primary role: See docs/VOCABULARY.md (ALCHEMIST, CHEMIST, SCHOLAR, PHILOSOPHER, PHYSICIAN, TRANSLATOR, MATHEMATICIAN, POET, PATRON, CLERICAL)
- Era: See docs/VOCABULARY.md (ANTIQUITY, LATE_ANTIQUE, MEDIEVAL, RENAISSANCE, EARLY_MODERN, MODERN)
- One sentence establishing historical significance to alchemy/chemistry

Do NOT begin with "This figure was..." or "This person is..." Begin with the name.

**Example Opening:**

> Jabir ibn Hayyan (c. 722–815), known to Western alchemists as *Geber*, was an Arab polymath and alchemist active in the 8th century whose vast corpus of works on alchemy, medicine, and natural philosophy shaped the development of practical chemistry for over a millennium. Whether Jabir authored all texts attributed to him remains contested among modern scholars (Lawrence Principe argues for multiple authors; William Newman defends substantial Jabir authorship), but the *Corpus Jabirianum* collectively established systematic distillation, acid production, and metal-working as core alchemical operations rooted in reproducible chemical reactions rather than mystical speculation.

### 2.2: Main Sections for Historical Alchemists/Chemists (250–400 words each)

Include at least two `<h2>` sections:

**`<h2>Works and Intellectual Context</h2>`**
- Specific treatises authored or major compilations
- Key arguments and doctrines presented
- Sources and influences (what did this person draw from?)
- Institutional context (court, university, monastery, workshop)
- Integration with contemporary philosophy, medicine, or natural history
- Cite specific texts and sections by name

**`<h2>Alchemical Significance</h2>`**
- Specific contributions to operational chemistry (distillation, sublimation, etc.)
- Transmutation theory and claims
- Laboratory apparatus and methods (material grounding)
- Innovations or refinements to technique
- Relationship between practical operations and theoretical claims
- **Ground in material reality:** What was actually being done in the laboratory? What equipment? What dangers (toxins, explosions, burns)? What observable results?

**`<h2>Transmission and Reception</h2>`**
- How were this person's texts transmitted (manuscript, print, translation)?
- Key medieval or Renaissance interpreters
- Citation history (who quoted them and why?)
- Influence on successors (name them)
- Modern editions and translations

**`<h2>Scholarly Debates</h2>`**
- Historiographical disagreements about authorship, dating, significance
- Modern reassessments vs. traditional narratives
- Contested claims (transmutation, sources, influences)
- Contemporary scholarship positions (name specific scholars: Newman vs. Principe, for example)
- State disagreements explicitly; present evidence for competing views

### 2.3: Main Sections for Modern Scholars (250–400 words each)

Include at least two `<h2>` sections:

**`<h2>Central Thesis</h2>`**
- What distinctive argument did this scholar advance?
- What existing interpretations did they challenge?
- What sources or archives did they emphasize or discover?

**`<h2>Key Works</h2>`**
- 2–4 major publications with dates
- Brief description of each work's argument and evidence
- How each refined or changed the field

**`<h2>Methodological Approach</h2>`**
- Theoretical framework (actor/analyst distinction, material culture, etc.)
- Primary vs. secondary sources used
- Geographic or temporal focus
- Interdisciplinary methods (textual, experimental, social history, etc.)

**`<h2>Scholarly Disputes</h2>`**
- Who influenced them? What traditions do they challenge?
- What do other scholars agree/disagree with?
- Evolution of their thinking over time if applicable

### 2.4: Italics Policy

- **Titles of texts:** *Summa Perfectionis*, *Emerald Tablet*, *Atalanta Fugiens*
- **Foreign technical terms on first use:** *calcination*, *sublimatio*, *quinta essentia*
- Do NOT italicize proper names of persons, places, or institutions

### 2.5: Literature Section (5–12 references)

**Format (DGWE model):**
```
Author Last Name. *Full Title of Work*. Publisher, Year.

Example:
Newman, William R. *Atoms and Alchemy: Chymistry and the Transformation of Matter in the Early Modern World*. University of Chicago Press, 2006.

Principe, Lawrence M. *The Secrets of Alchemy*. University of Chicago Press, 2013.
```

---

## § 3: Text Descriptions (analysis_html field)

### General Requirements

**Length:** 1,000–1,800 words (excluding Literature section)  
**Format:** Valid HTML with `<p>`, `<h2>`, `<i>`, `<b>` tags only

### 3.1: Opening Paragraph (200–300 words)

Include:
- Full title in italics: *Kitāb al-Ḥāsib*, *Summa Perfectionis*, etc.
- Date of composition or earliest attestation
- Original language (Latin, Arabic, Greek, Hebrew, English, etc.)
- Type: PRIMARY_SOURCE, COMMENTARY, COMPILATION, TREATISE, SCHOLARSHIP, ENCYCLOPEDIA (see docs/VOCABULARY.md)
- Author or tradition attribution
- One sentence of historical significance

Do NOT begin with "This text..." Begin with the title.

**Example Opening:**

> *The Summa Perfectionis* (attributed to Jabir ibn Hayyan; also known as *Liber Claritatis*) is a foundational medieval Latin alchemical text of disputed authorship, composition date, and origin. Most modern scholars (William R. Newman, Michela Pereira) argue for 13th-century Latin European authorship rather than 8th-century Jabir attribution, though the text itself claims Jabir tradition. Composed in Latin, the *Summa* systematically presents alchemical operations (distillation, sublimation, calcination) as reproducible laboratory procedures with measurable results, establishing alchemy in medieval Europe as a legitimate natural philosophy rather than mystical speculation.

### 3.2: Content and Theory (300–500 words)

- What arguments or doctrines does the text present?
- Key chapters or sections cited by historians
- Specific operations described (distillation, sublimation, fermentation, etc.)
- Theoretical claims about matter, transmutation, causation
- Integration with contemporary philosophy or theology
- Be specific and cite actual text passages

### 3.3: Composition and Textual Tradition (200–400 words) [For Primary Sources]

- How did this text survive and circulate?
- Manuscript tradition, copies, versions, variants
- Translations and intermediaries (who translated? when? what languages?)
- Key transmitters (scribes, translators, scholars)
- Modern editions and translations (cite by scholar name and date)

### 3.4: Modern Scholarship (150–300 words)

- Which scholars have produced authoritative editions or translations?
- What are current scholarly debates about authorship, dating, significance?
- Name specific scholars and their specific arguments
- If authorship is contested, present the evidence for competing views

### 3.5: Literature Section (5–12 references)

**Format (DGWE model):** See § 2.5 above.

---

## § 4: Timeline Events (description field)

### General Requirements

**Length:** 100–250 words (plain text)  
**Format:** Plain text, no HTML tags

Every timeline event **must** include:

1. **Exact date or date range:** "c. 1320," "1492–1495," "6th century"
2. **Named location with region:** City preferably; region at minimum
3. **Named actors:** At least one person, text, or institution
4. **Historiographical significance:** Final sentence explaining why this matters to the history of alchemy/chemistry

### Structure

```
[Date], [Location]: [Main narrative: what happened, who did it, what was discovered].

[Scholarly contextualization: why it matters]. [Connection to broader developments]. 
[How this event fits into transmission or theory].
```

### Example (Complete)

> c. 1250, Andalusia: The scholar Gerard of Cremona, traveling in Muslim Spain, completes his Latin translation of the *Kitāb al-Ḥāsib* (attributed to Jabir ibn Hayyan), a foundational Arabic alchemical text that teaches distillation of alkalis and mineral acids. This translation represents the first systematic introduction of Arabic practical alchemical knowledge into the Latin West and will circulate widely among European alchemists for the next three centuries. The operations described in Jabir's texts were immediately replicable and produced observable effects, establishing alchemy in medieval universities as a legitimate natural philosophy.

### Checklist

- [ ] Date is specific (exact year or "c. [year]")?
- [ ] Location is named with region?
- [ ] At least one person, text, or institution is named?
- [ ] Final sentence states historiographical significance?
- [ ] Word count is 100–250?
- [ ] No markdown, no hashtags, no bullets?
- [ ] At least one entity name is marked for [LINK:slug] conversion?

---

## § 5: Concept Definitions (definition_long field)

### General Requirements

**Length:** 1,500–2,500 words (excluding Literature section)  
**Format:** Valid HTML with `<p>`, `<h2>`, `<i>`, `<b>` tags only

**Critical:** All concept definitions MUST explicitly distinguish ACTOR_TERM vs. ANALYST_TERM. See docs/VOCABULARY.md for definitions.

### 5.1: Opening Paragraph (150–250 words)

State the term in original language if applicable. **Explicitly declare ACTOR_TERM or ANALYST_TERM.** Give earliest attestation. Establish significance. Do NOT begin with "This term..." Begin with the term itself.

**Example for ACTOR_TERM:**

> Distillatio (Latin; also *distillation* in English, *dhiqa* in some Arabic texts) was an operational term used by medieval and early modern alchemists to describe the separation of substances by heating and condensation, producing volatile essences or refined products. This is an ACTOR_TERM—historical practitioners explicitly used this word and would recognize the concept. The operation is one of the oldest recorded alchemical procedures, appearing in Zosimos's 3rd-century texts and central to the *Corpus Jabirianum*. Distillation produced reproducible, observable results (volatile essences, concentrated liquids, refined metals) and became foundational to both alchemical theory and practical chemistry.

**Example for ANALYST_TERM:**

> Hermeticism is a modern scholarly category for a complex of ideas, texts, and practices ostensibly derived from the Hermetic corpus (Corpus Hermeticum), though Wouter J. Hanegraaff and others have questioned whether historical actors would have recognized themselves under this rubric. This is an ANALYST_TERM—a retrospective scholarly category imposed after the fact. The term gained currency in 20th-century esotericism studies to describe a tradition spanning from Late Antiquity through the present, though contemporary usage masks significant historiographical disputes about periodization, boundaries, and whether "Hermeticism" is a coherent tradition or a scholarly fiction.

### 5.2: Historical Usage (400–600 words)

Trace the term's evolution from earliest attestation through Late Antiquity, medieval Islam, medieval Latin, Renaissance, and early modernity.

- Name specific texts and authors
- Show shifts in meaning over time
- **For ACTOR_TERMs especially:** Ground the term in material reality
  - What was the actual operation or substance?
  - What tools or equipment were involved?
  - What dangers (toxins, explosions, burns)?
  - What sensory experiences were involved?
  - What observable results?
  - How did practitioners learn and transmit this knowledge?
- **For transmission:** Show how the term traveled across cultures and languages
  - How did translations alter meaning?
  - How did practitioners in different contexts understand it differently?

### 5.3: Scholarly Significance (400–600 words)

How have modern scholars debated this term? This section MUST name scholars by name and state their specific arguments.

**Example structure:**

> William R. Newman has argued that distillation was primarily an operational technique rooted in reproducible chemistry, citing specific passages from the *Corpus Jabirianum* (e.g., *Summa Perfectionis* II.7) where the apparatus is described with technical precision. However, Lawrence Principe emphasizes that many alchemists also attributed transmutational significance to distillation, suggesting the operation and the transmutational belief were inseparable in practitioners' minds. Pamela Smith's work on artisanal epistemology suggests that this disagreement reflects a false binary: alchemists learned through embodied, practical engagement with the apparatus itself, which produced both observable chemical effects and theoretical speculation about matter's nature.

### 5.4: Transmission and Variant Forms (200–400 words) [OPTIONAL]

Include for terms with Greek, Arabic, Latin, or Hebrew variants, or for terms whose meaning shifted significantly in translation.

### 5.5: Related Concepts (100–200 words of prose, NOT a bullet list)

Link to 3–5 related entries using prose sentences, not lists.

**Example:**

> Distillation is closely related to sublimation, which also involves vaporization but produces a solid directly without an intermediate liquid state. Both operations were understood as forms of separation and refinement in medieval alchemy. Distillation also connects to calcination (reduction to ash) and dissolution (breaking down of solids), which together formed the core operational taxonomy of the alchemical laboratory.

### 5.6: Literature Section (8–15 references)

**Format (DGWE model):** See § 2.5 above. Concept definitions warrant slightly longer bibliographies than other types.

---

## § 6: Bibliography Format (DGWE Model)

All Literature sections must follow this format. No variation.

**Basic Format:**
```
Author Last Name. *Full Title of Work*. Publisher, Year.
```

**Examples:**

```
Newman, William R. *Atoms and Alchemy: Chymistry and the Transformation of Matter in the Early Modern World*. University of Chicago Press, 2006.

Pereira, Michela. *The Alchemical Corpus Attributed to Ray Lull*. Brill, 2007.

Fowden, Garth. *The Egyptian Hermes: A Historical Approach to the Late Pagan Mind*. Princeton University Press, 1986.

Hanegraaff, Wouter J., editor. *Dictionary of Gnosis and Western Esotericism*. Brill, 2006.

Principe, Lawrence M., and William R. Newman. *George Starkey: Alchemy, Medicine, and Craft Knowledge in Early Modern Europe*. University of Chicago Press, 2004.
```

**Rules:**
- Author last name first
- Full title in italics (not truncated)
- Full publisher name (not abbreviated)
- Year of publication
- No URLs or DOIs
- Alphabetize by author last name
- Use semicolon to separate multiple authors (rare; see multi-editor example above)

---

## § 7: Validation Checklist

Before committing any work:

- [ ] **Word count:** Meets minimum for type (timeline: 100–250 | persons: 1,200–2,200 | texts: 1,000–1,800 | concepts: 1,500–2,500)
- [ ] **Sections:** All required `<h2>` sections present (see type-specific requirements)
- [ ] **Bibliography:** All Literature sections follow DGWE format (5–15 items depending on type)
- [ ] **Foreign terms:** All non-English terms italicized on first use
- [ ] **Book titles:** All text titles italicized
- [ ] **Proper names:** NOT italicized (persons, places, institutions)
- [ ] **Claims grounded:** Every substantive assertion traces to a named scholar or primary source
- [ ] **Entity links:** Every entry links to ≥3 other entities (persons, texts, concepts)
  - Mark entity names with `[LINK:slug]` for main session to convert to `<a href>`
- [ ] **No markdown artifacts:** No `#`, `*`, `**`, `-`, `[ ]`, `{ }`, emoji, hashtags
- [ ] **No placeholders:** No "To be added," "N/A," "TBD"
- [ ] **Provenance metadata complete:**
  - source_method: MANUAL | AI_ASSISTED | SCHOLARSHIP_BASED
  - review_status: DRAFT | REVIEWED | VERIFIED
  - confidence: HIGH | MEDIUM | LOW
- [ ] **Enum values valid:** All role, era, text_type, category_type values from docs/VOCABULARY.md (NO invention)
- [ ] **ACTOR_TERM/ANALYST_TERM:** Explicitly declared for all concepts (§ 5)
- [ ] **HTML valid:** All tags are `<p>`, `<h2>`, `<i>`, `<b>` only; no other tags

---

## Appendix A: Complete Example Entries

### Example 1: Person Biography (Historical Alchemist)

[See docs/reference/examples/WILLIAM_NEWMAN_EXAMPLE.md for full worked example of modern scholar — 900 words]

### Example 2: Text Description (Primary Source)

[See docs/reference/examples/SUMMA_PERFECTIONIS_EXAMPLE.md for full worked example — 1,200 words]

### Example 3: Concept Definition (ACTOR_TERM)

[See docs/reference/examples/DISTILLATION_EXAMPLE.md for full worked example with material grounding — 1,800 words]

### Example 4: Concept Definition (ANALYST_TERM)

[See docs/reference/examples/HERMETICISM_EXAMPLE.md for full worked example showing historiographical dispute — 1,600 words]

### Example 5: Timeline Event

See § 4 for complete example (150 words).

---

## Questions?

- **What are the allowed enum values?** See docs/VOCABULARY.md
- **Which files do I need to read before writing?** See docs/agents/TASK_ROUTING.md
- **What's the historiographical framework?** See PROMPTS.md
- **What's the current project status?** See PHASESTATUS.md

---

**This is the single source of truth for all prose standards. All other files reference this file; nothing duplicates it.**

*Last updated: 2026-05-22*
