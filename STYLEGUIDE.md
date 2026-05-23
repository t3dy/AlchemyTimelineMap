# ALCHEMYTIMELINEMAP Content Style Guide

**MANDATORY: All agents, scripts, and LLM sessions contributing content must consult this file before writing any prose for the database. This guide governs `description`, `analysis_html`, `bio_html`, and `definition_long` fields.**

---

## The Core Standard: Encyclopedia Prose

Every entry — whether a timeline event, a biography, a text description, or a concept definition — must read like a **scholarly encyclopedia article**. The model is the *Dictionary of Gnosis and Western Esotericism* (Hanegraaff, Brill, 2006) and *The Cambridge History of Science*: authoritative, precise, readable, and free of typographic artifacts.

Write in full, flowing sentences in the third person. Do not use bullet points, numbered lists, hashtags, markdown symbols, emoji, or template placeholders. Every paragraph must contain substantive historical or scholarly content.

---

## Absolute Prohibitions

The following are **never acceptable** in any prose field:

- **Hashtags**: `#` in any context
- **Square brackets**: `[text]` or `[[text]]` (except `[LINK:slug]` for agent markup)
- **Curly braces**: `{placeholder}` or `{{field}}`
- **Asterisks for emphasis**: `*text*` or `**text**`
- **Markdown headers**: `## Heading` — use `<h2>` HTML instead
- **Bullet points or hyphens as list markers**: `- item` or `* item`
- **Emoji or Unicode symbols used decoratively**: ☿ 🜍 ⚗
- **Template artifact strings**: `entity["people", "Name", 0]`
- **Placeholder text**: "To be added," "N/A," "TBD"

---

## Timeline Events (Primary Content Type)

**Length:** 100–250 words.
**Format:** Plain text, no HTML tags.

Every timeline event **must** include:

1. **Exact date or date range** (CE/BCE): "c. 1320," "1492–1495," "6th century"
2. **Named location with coordinates**: City, ideally; region at minimum
3. **Named actors**: At least one person, text, or institution
4. **Historiographical significance** (final sentence): Why does this matter to the history of alchemy/chemistry?

### Structure

```
[Date], [Location]: [Main narrative establishing what happened, who did it, what was discovered or created].

[Scholarly significance and contextualization]. [Connection to broader alchemical or chemical developments]. [How this event fits into the transmission of knowledge or the history of theory.]
```

### Example (Proper)

> "c. 1250, Andalusia: The scholar Gerard of Cremona, traveling in Muslim Spain, completes his Latin translation of the *Kitāb al-Ḥāsib* (attributed to Jabir ibn Hayyan), a foundational Arabic alchemical text that teaches distillation of alkalis and mineral acids. This translation represents the first systematic introduction of Arabic practical alchemical knowledge into the Latin West and will circulate widely among European alchemists for the next three centuries. The operations described in Jabir's texts were immediately replicable and produced observable effects, establishing alchemy in medieval universities as a legitimate natural philosophy."

### Checklist

- [ ] Date is specific (exact year or "c. [year]")?
- [ ] Location is named with region specified?
- [ ] At least one person or text is named?
- [ ] Final sentence states historiographical significance?
- [ ] Word count is 100–250?
- [ ] No markdown, no hashtags, no bullets?

---

## Person Biographies (bio_html field)

**Length target:** 1,200–2,200 words (excluding Literature section).
**Format:** Valid HTML with `<p>`, `<h2>`, `<i>`, `<b>` tags only.
**Bibliographic minimum:** 5–12 items in Literature section.

Every biography **must** contain:

**Opening paragraph** (200–350 words): Full name, dates (birth–death or fl.), nationality, primary role or profession (`ALCHEMIST`, `CHEMIST`, `SCHOLAR`, `PHYSICIAN`, etc.), era, and substantive significance to alchemy/chemistry. Do NOT begin with "This figure was..." or "This person is..." — begin with the name.

**At least two `<h2>` sections**, each 250–400 words:

*For historical alchemists/chemists:*
- `<h2>Works and Intellectual Context</h2>` — specific texts, their arguments, what sources they drew from, intellectual traditions they engaged with
- `<h2>Alchemical Significance</h2>` — engagement with transmutation theory, practical operations, theoretical innovations. Ground in material reality: what was actually being done in the laboratory? What equipment? What dangers?
- `<h2>Transmission and Reception</h2>` — how were they read and cited by successors? Were they misunderstood? Reinterpreted? Which manuscripts survived? How did translations alter their meaning?
- `<h2>Scholarly Debates</h2>` — what do modern historians disagree about? Name the scholars and their arguments explicitly. If there's disagreement about authentorship, dating, sources, or significance, present the evidence for competing views.

*For modern scholars:*
- `<h2>Central Thesis</h2>` — their most distinctive historiographical argument
- `<h2>Key Works</h2>` — 2–4 major publications with dates
- `<h2>Methodological Approach</h2>` — what theoretical framework?
- `<h2>Scholarly Disputes</h2>` — who influenced them? What do they disagree with?

**`<h2>Literature</h2>`**: 5–12 bibliographic entries in DGWE format (see below).

### Italics Policy

- Titles of texts: *Summa Perfectionis*, *Emerald Tablet*, *Atalanta Fugiens*
- Foreign technical terms on first use: *calcination*, *sublimatio*, *quinta essentia*
- Names of texts when used as titles (not as concepts)

Do NOT italicize proper names of persons, places, or institutions.

### Example Opening Paragraph

> "Jabir ibn Hayyan (c. 722–815), known to Western alchemists as *Geber*, was an Arab polymath and alchemist active in the 8th century whose vast corpus of works on alchemy, medicine, and natural philosophy shaped the development of practical chemistry for over a millennium. Whether Jabir authored all texts attributed to him remains contested among modern scholars (Lawrence Principe argues for multiple authors; William Newman defends substantial Jabir authorship), but the *Corpus Jabirianum* collectively established systematic distillation, acid production, and metal-working as core alchemical operations rooted in reproducible chemical reactions rather than mystical speculation."

---

## Text Descriptions (analysis_html field)

**Length target:** 1,000–1,800 words (excluding Literature section).
**Format:** Valid HTML with `<p>`, `<h2>`, `<i>`, `<b>` tags.
**Bibliographic minimum:** 5–12 items in Literature section.

**Opening paragraph** (200–300 words): Full title in italics, date of composition or earliest attestation, original language, and a substantive sentence on the text's place in the alchemical canon. State immediately whether it is PRIMARY SOURCE, COMMENTARY, SCHOLARSHIP, etc.

**`<h2>Content and Theory</h2>`** (300–500 words): What does the text argue or teach? Key doctrines, operational instructions, theoretical claims? Cite specific sections or chapter titles. Be specific.

**`<h2>Composition and Textual Tradition</h2>`** (200–400 words, required for primary sources): How did this text survive? Through what manuscript traditions, translations, or intermediaries? Who were the key transmitters? Name them.

**`<h2>Modern Scholarship</h2>`** (150–300 words): Which scholars have produced authoritative editions, translations, or interpretations? What are current scholarly debates about authorship, dating, or significance?

**`<h2>Literature</h2>`**: 5–12 bibliographic entries in DGWE format.

---

## Concept Definitions (definition_long field)

**Length target:** 1,500–2,500 words (excluding Literature section).
**Format:** Valid HTML with `<p>`, `<h2>`, `<i>`, `<b>` tags.
**Bibliographic minimum:** 8–15 items in Literature section.

**Critical note on Actor/Analyst Distinction:** Following Wouter J. Hanegraaff's *Dictionary of Gnosis and Western Esotericism*, you MUST distinguish between:
- **ACTOR_TERMs**: Words used by historical practitioners (e.g., *distillatio*, *calcination*, *transmutatio*). These are terms that alchemists themselves employed and would recognize.
- **ANALYST_TERMs**: Modern retrospective scholarly categories (e.g., *alchemy*, *Hermeticism*, *esotericism*). These are frameworks historians impose after the fact.

Never collapse these registers. If scholars argue about whether a term was really used or really meant what we think it means, say so explicitly.

**Required structure:**

**Opening paragraph** (150–250 words): State the term in original language if applicable. Declare explicitly whether it is an ACTOR_TERM (used by historical alchemists) or ANALYST_TERM (modern historiographical category). Give earliest attestation. Establish significance. Do NOT begin with "This term..." or "This concept..." — begin with the term itself.

**Example opening for ACTOR_TERM:** "Distillatio (Latin; also *distillation* in English, *dhiqa* in some Arabic texts) was an operational term used by medieval and early modern alchemists to describe the separation of substances by heating and condensation, producing volatile essences or refined products..."

**Example opening for ANALYST_TERM:** "Hermeticism is a modern scholarly category for a complex of ideas, texts, and practices ostensibly derived from the Hermetic corpus (Corpus Hermeticum), though Wouter J. Hanegraaff has questioned whether historical actors would have recognized themselves under this rubric. The term gained currency in 20th-century esotericism studies to describe a tradition spanning from Late Antiquity through the present, though contemporary usage masks significant historiographical disputes about periodization and boundaries."

**`<h2>Historical Usage</h2>`** (400–600 words): Trace the term's evolution from earliest attestation through Late Antiquity, medieval Islam, medieval Latin, Renaissance, and early modernity. Name specific texts and authors. Show shifts in meaning. **For ACTOR_TERMs especially:** Ground the term in material reality. What was the actual operation or substance? What tools, dangers, or sensory experiences were involved? (E.g., distillation produces vapors that can be condensed; it requires glass or copper equipment; it poses burn and respiratory hazards.) This grounds abstract terminology in the embodied experience of the alchemist. **For transmission:** Show how the term traveled across cultures and languages, how translations altered meaning, and how practitioners in different contexts may have understood it differently.

**`<h2>Scholarly Significance</h2>`** (400–600 words): How have modern scholars debated this term? Name them by name. State their specific arguments. If historians disagree, state the disagreement explicitly and engage with the evidence on both sides. Example structure: "William R. Newman has argued that distillation was primarily an operational technique rooted in reproducible chemistry, citing specific passages from the *Corpus Jabirianum* (e.g., *Summa Perfectionis* II.7) where the apparatus is described with technical precision. However, Lawrence Principe emphasizes that many alchemists also attributed transmutational significance to distillation, suggesting the operation and the transmutational belief were inseparable in practitioners' minds. Pamela Smith's work on artisanal epistemology suggests that this disagreement reflects a false binary: alchemists learned through embodied, practical engagement with the apparatus itself, which produced both observable chemical effects and theoretical speculation about matter's nature."

**`<h2>Transmission and Variant Forms</h2>`** (200–400 words, OPTIONAL): Include for terms with Greek, Arabic, Latin, or Hebrew variants, or for terms whose meaning shifted significantly in translation.

**`<h2>Related Concepts</h2>`** (100–200 words of prose, NOT a bullet list): Link to 3–5 related entries using `<a href>` tags. Write in full sentences explaining relationships.

**`<h2>Literature</h2>`**: 8–15 bibliographic entries in DGWE format.

### Multi-Register Field (registers JSON)

For every concept definition, also populate the `registers` JSON field in the database. This field is a JSON object mapping each of the four registers to a one-sentence description:

```json
{
  "alchemical": "Operational description: what the procedure involved",
  "medical": "Medical application: how it applied to health/humors",
  "spiritual": "Spiritual significance: inner transformation dimension",
  "cosmological": "Cosmic law: role in creation/universal order"
}
```

Each sentence should be concise (15–30 words) and reflect the core content of the corresponding `<h2>` section in your `definition_long`. This enables the front-end to present concept meanings by register and helps readers understand simultaneity across domains.

---

## Bibliography Format (Literature Sections)

All `<h2>Literature</h2>` sections use the following format, modeled on the *Dictionary of Gnosis and Western Esotericism* (Brill, 2006):

**Monograph:**
> Newman, William R. *Atoms and Alchemy: Chymistry and the Transformation of Matter in the Early Modern Period*. Chicago: University of Chicago Press, 2006.

**Article in journal:**
> Principe, Lawrence. "The Alchemies of Robert Boyle and Isaac Newton: Alternate Approaches and Divergent Deployments." *The Mindful Hand: Inquiry and Invention from the Late Renaissance to Early Industrialization*. New York: Routledge, 2007. 181–202.

**Chapter in edited volume:**
> Pereira, Michela. "The Alchemical Corpus Attributed to Ray Lull." In *Occult Sciences and Alchemy in Medieval Europe*, edited by David C. Lindberg and Michael H. Shank. Chicago: University of Chicago Press, 2002. 267–308.

**Rules:**
- Author surname first, comma, first name
- Book/journal titles in `<i>` tags
- Full publication data: place, publisher, year
- Articles: full page range
- Alphabetical by author surname
- No "ibid."

---

## Historiographical Standards: Actor/Analyst Distinction, Material Culture, Transmission

This portal follows the historiographical framework of **Wouter J. Hanegraaff** (*Dictionary of Gnosis and Western Esotericism*, Brill, 2006) and **Pamela H. Smith** (*The Business of Alchemy*, Smith, 2004; Making and Knowing methodology).

### The Actor/Analyst Distinction (MANDATORY)

Every entry must be clear about whose perspective we're adopting:

- **ACTOR perspective**: What did practitioners in their own time call this? What did they think they were doing? What would surprise or offend them about modern interpretation?
- **ANALYST perspective**: What retrospective categories do 21st-century historians use? How did we arrive at terms like "alchemy," "Hermeticism," or "esotericism"?

Collapsing these perspectives creates false unity and hides genuine historical complexity. Example: Medieval alchemists never called themselves "Hermeticists." They may have read Hermetic texts, but they would not have recognized "Hermeticism" as a category. This is a modern analytical frame. State this clearly.

### Material Culture and Embodied Knowledge

Following Pamela Smith's *artisanal epistemology*, ground all discussions in the material reality of the laboratory:

- What equipment was used? (alembics, retorts, furnaces, crucibles)
- What materials? (minerals, metals, plant matter, animal products)
- What dangers? (fumes, burns, explosions, toxins)
- How was knowledge transmitted? (apprenticeship, bodily practice, not just reading)

Avoid floating abstractions like "transmutation belief." Instead: "Alchemists heated mercury and sulfur together in sealed vessels, expecting to transform base metals into gold, based on theoretical frameworks derived from Jabir ibn Hayyan's operational chemistry and Neoplatonic theories of matter."

### Transmission and Reception History

Every person, text, and concept has a *history*. It was created, copied, translated, misread, reused, embedded in new contexts. Show this:

- Which manuscripts survived and which were lost?
- How did translation alter meaning? (Arabic *dhiqa* → Latin *distillatio* → English *distillation*)
- Who read this text and what did they do with it? (Was it corrected? Rejected? Integrated into new frameworks?)
- Was the author understood as they intended? Or misread? (This is often more historically interesting than "accurate" reading.)

Example: The *Emerald Tablet* circulated in multiple versions. Medieval Latin translators read it as a recipe for transmutation. Renaissance Hermeticists read it as a cosmological text. Modern scholars argue about what Hermes Trismegistus "really" meant, but the medieval and Renaissance *misreadings* shaped alchemy's actual history. Show all of this.

### Multi-Register Interpretation (Concept Definitions)

Alchemical concepts are **polyvalent**: a single term carries meaning simultaneously across multiple knowledge registers. Every concept definition for alchemy must express these registers together, rather than choosing one and dismissing others as "mere metaphor."

**Four core registers:**

1. **Alchemical register**: the operational account (furnace work, material transformation, observable effects)
2. **Medical register**: applications to health, healing, humoral theory, pharmaceutical compounds
3. **Spiritual register**: inner transformation, purification, mystical union, ego-annihilation
4. **Cosmological register**: universal laws, creation mythology, celestial influences, cosmic cycles

Practitioners engaged all four simultaneously. Your concept definitions must show this simultaneity. Do NOT write separate sections for "what it really meant" (chemical) versus "what they thought it meant" (spiritual). Instead, show how a single term like *calcination* or *putrefaction* expressed meaning across all four registers at once.

**Structure:** Divide the concept's `definition_long` field into four `<h2>` sections, one per register. Each section should include primary source quotations, technical details, and scholarly context specific to that register. See `docs/MULTIREGISTER_EXAMPLES.md` for a worked example (calcination across four registers).

**In the database:** Populate the `registers` JSON field with one-sentence summaries:
```
{"alchemical": "...", "medical": "...", "spiritual": "...", "cosmological": "..."}
```

This enables the front-end to present concept meanings by register and helps readers understand how a single term unified different domains of knowledge.

---

## Voice and Register

Write in the voice of a senior academic who is simultaneously a clear writer. Avoid jargon where a plain word suffices. When technical terms are necessary (distillation, calcination, transmutation), define them within prose on first use.

The register is formal but not obscure. Assume an intelligent reader with general education but no specialist background in alchemy or chemistry.

---

## Source Attribution

Every substantive claim must be traceable to a named source. Integrate citations organically into prose: "As William Newman argues in *Atoms and Alchemy* (2006)..." Do not use footnote-style citation brackets.

---

## Optional Historiographical Metadata Fields

Three fields on the persons, texts, and concepts tables support deeper historiographical precision:

### transmission_chain (JSON array)

For concepts and texts with multiple versions, translations, or genealogies, populate this field with an ordered array of related slugs showing evolution:

```json
["distillatio-zosimos", "dhiqa-arabic", "distillatio-latin-gerard", "distillation-medieval", "distillation-paracelsian"]
```

This field enables the front-end to show readers how a term or text evolved across languages, periods, and interpretations. Include it especially for:
- Texts with multiple translations or recensions
- Concepts with variant terminology across languages
- Persons with intellectual predecessors/successors

### scholarly_disagreement (plain text)

If there are significant historiographical disputes about this entry, note them briefly:

> "Authorship of the *Summa Perfectionis* disputed between Newman (defends Jabir authorship, 8th century) and Principe (attributes to 13th-century compiler); see *Scholarly Significance* section for details."

This alerts readers to uncertainties and directs them to the main text where the disagreement is discussed.

### material_grounding (plain text, for concepts, texts, and persons)

For concepts and texts, brief notes on real-world apparatus, materials, or dangers:

> "Apparatus: alembic with long copper neck; common to distill wine, rose water, mineral waters; produces flammable vapors; can cause severe burns; requires careful furnace temperature control."

For persons, note their practical context, teaching lineages, or real-world influence:

> "Active as court physician and laboratory director; trained apprentices in distillation; oversaw production of mineral waters and medicinal compounds; evidence of laboratory accidents in correspondence."

---

## Checking Your Work

Before submitting any prose entry, ask:

1. Would this passage appear unedited in a peer-reviewed encyclopedia?
2. Does it contain any prohibited symbols or formatting artifacts?
3. Are all book titles and foreign terms properly italicized?
4. For concepts: is the Actor/Analyst distinction declared explicitly?
5. Are all claims grounded in a named source?
6. Does the entry meet the minimum word count for its type?
7. Does the Literature section have the minimum number of items?
8. Are there at least 3 internal hyperlinks to related entities?
9. For concepts: have I populated the `registers` JSON field?
10. If there are historiographical disputes: have I noted them in `scholarly_disagreement` and discussed them in the main text?
11. If the entry has a genealogy (translations, successors, variants): have I populated `transmission_chain`?
12. If applicable: have I grounded the entry in material reality via `material_grounding`?

If the answer to any is "no," revise before submission.

---

## Quick Reference: Minimum Specifications

| Content Type | Min Words | Max Words | Min Lit Items | Actors Named |
|---|---|---|---|---|
| Timeline event | 100 | 250 | — | ≥1 |
| Person biography | 1,200 | 2,200 | 5 | — |
| Text description | 1,000 | 1,800 | 5 | — |
| Concept definition | 1,500 | 2,500 | 8 | — |

*These are minimums. Longer, more detailed entries are always preferable.*

---

*This style guide is referenced in `CLAUDE.md` and `PROMPTS.md` and must be consulted at the start of any session producing content.*
