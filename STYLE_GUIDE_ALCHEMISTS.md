# Style Guide: Historical Alchemists & Chemists

## Purpose

This guide establishes standards for encyclopedia-length entries documenting historical alchemists, chemists, and natural philosophers who contributed to alchemical theory and practice from Late Antiquity through the early modern period.

## Target Length

- **Index card (short bio)**: 60–120 words
- **Encyclopedia page (full bio_html)**: 1,200–2,200 words

## Structure for Full Entries

### Opening Paragraph (200–350 words)

Begin with the person's full name, dates (birth–death or *fl.* for flourished), geographic origin, and primary role(s).

**Essential information:**
- Full name (with alternate names/transliterations)
- Birth–death dates or floruit period (e.g., "fl. c. 1290")
- Geographic origin and primary location(s)
- Primary role(s): ALCHEMIST, CHEMIST, PHILOSOPHER, PHYSICIAN, TRANSLATOR, MATHEMATICIAN, SCHOLAR, CLERICAL, PATRON
- Era: ANTIQUITY, LATE_ANTIQUE, MEDIEVAL, RENAISSANCE, EARLY_MODERN, MODERN
- One sentence establishing historical significance

**Example opening:**

> Jabir ibn Hayyan (c. 722–815), known to Western alchemists as *Geber*, was an Arab polymath whose vast corpus of alchemical and chemical texts shaped the development of practical chemistry for over a millennium. Born in Khorasan (northeastern Persia), Jabir was active in the intellectual courts of Baghdad and Ray during the height of the Abbasid caliphate. Whether Jabir authored all texts attributed to him remains contested—Lawrence Principe argues for multiple authorial layers; William Newman defends substantial Jabir authorship—but the *Corpus Jabirianum* collectively established systematic distillation, acid production, and metal-working as core alchemical operations rooted in reproducible chemical reactions rather than mystical speculation.

---

### Main Sections (250–400 words each)

#### For Historical Alchemists:

**1. Works and Intellectual Context**
- Specific treatises authored or major compilations
- Arguments and doctrines presented
- Sources and influences (what did this person draw from?)
- Institutional context (court, university, monastery, workshop)
- Integration with contemporary philosophy, medicine, natural history

**2. Alchemical Significance**
- Specific contributions to operational chemistry (distillation, sublimation, etc.)
- Transmutation theory and claims
- Laboratory apparatus and methods
- Innovations or refinements to technique
- Relationship between practical operations and theoretical claims

**3. Transmission and Reception**
- How were this person's texts transmitted (manuscript, print, translation)?
- Key medieval or Renaissance interpreters
- Citation history (who quoted them and why?)
- Influence on successors
- Modern editions and translations

**4. Scholarly Debates**
- Historiographical disagreements about authorship, dating, significance
- Modern reassessments vs. traditional narratives
- Contested claims (transmutation, etc.)
- Contemporary scholarship positions (Newman vs. Principe, for example)

---

#### For Modern Scholars:

**1. Central Thesis**
- What is this scholar's distinctive argument about alchemy/chemistry history?
- How does it challenge or refine earlier interpretations?
- What is their methodology?

**2. Key Works**
- 2–4 major publications with dates
- Brief description of each work's contribution

**3. Scholarly Approach**
- Theoretical framework (actor/analyst distinction, etc.)
- Primary vs. secondary sources used
- Geographic or temporal focus
- Interdisciplinary methods (textual, experimental, social history, etc.)

**4. Reception and Impact**
- How has scholarship responded?
- Which arguments have been accepted/contested?
- Ongoing influence in the field

---

### Literature Section (5–12 entries)

Format: **Author Last Name. *Full Title of Work*. Publisher, Year.**

Example:

> Newman, William R. *Atoms and Alchemy: Chymistry and the Transformation of Matter in the Early Modern World*. University of Chicago Press, 2006.
>
> Principe, Lawrence M. *The Secrets of Alchemy*. University of Chicago Press, 2013.
>
> Smith, Pamela H. *The Business of Alchemy: Science and Culture in the Holy Roman Empire*. University of Chicago Press, 1994.

---

## Historiographical Standards

### 1. Ground All Claims in Named Sources

Do NOT write: "Alchemists believed transmutation was possible."

DO write: "As William Newman argues in *Atoms and Alchemy* (2006), medieval alchemists pursued transmutation through rigorous laboratory operations based on their understanding of matter's mutability."

### 2. Distinguish Historical Actors from Later Interpretations

**Actor terminology:** Use "alchemist" when discussing historical self-identification; use "chemist" only for post-18th-century figures or when discussing modern reinterpretations of their work.

Example: "Jabir ibn Hayyan was an alchemist whose operational methods—distillation, sublimation, acid production—were genuine chemical advances, though he pursued the impossible goal of transmutation."

### 3. Medieval Continuity, Not Gap

Never treat the Middle Ages as a period of decline or abandonment of alchemy. Instead, trace transmission chains:

> Greek alchemy (Zosimos) → Islamic elaboration (Jabir ibn Hayyan, Al-Razi) → Latin translation (Gerard of Cremona, 12th c.) → European integration (Roger Bacon, medieval universities) → Renaissance expansion (Paracelsus, emblem books) → Early modern refinement (Boyle, Newton, Starkey)

### 4. Chemical Operations Are Real

Describe distillation, sublimation, calcination, dissolution as genuine chemical processes with measurable results. These were not metaphorical or mystical—they are reproducible chemistry.

### 5. Proper Attribution

Distinguish between authorial attribution (what the text claims) and scholarly consensus (what historians believe). Example:

> *Summa Perfectionis* is attributed to Jabir ibn Hayyan, but modern scholars (Newman, 1991) treat it as a 13th-century Latin compilation possibly authored by a European alchemist familiar with Jaber tradition.

---

## HTML and Formatting

**Valid tags only:**
- `<p>` for paragraphs
- `<h2>` for section headers
- `<i>` for italics (text titles, foreign terms, scholarly emphasis)
- `<b>` for bold (sparingly, only for true emphasis)

**NO markdown, NO bullet points, NO hashtags.**

### Entity Linking

Wrap person, text, and concept names in `[LINK:slug]` markup:

- `[LINK:jabir-ibn-hayyan]` for persons
- `[LINK:summa-perfectionis]` for texts
- `[LINK:distillation]` for concepts

Do NOT link generic terms ("an alchemist", "a text") or proper nouns not in the entity list.

---

## Index Card Format (60–120 words)

**Lead with name + era + significance:**

> **Jabir ibn Hayyan** (c. 722–815), Arab alchemist and polymath. Known to Europeans as *Geber*. Established systematic distillation, sublimation, and acid production as reproducible chemical operations. *Corpus Jabirianum* became the canonical authority in medieval and Renaissance European alchemy. Whether Jabir personally authored all attributed works remains debated; modern scholarship (Newman, Principe) treats the corpus as a sophisticated synthesis of Islamic and Hellenistic alchemical traditions. Influence: immense; virtually every European alchemist from the 13th century onward quoted Jabir.

---

## Checklist Before Finalizing

- [ ] Full name with alternate names and transliterations?
- [ ] Birth/death or floruit dates clearly stated?
- [ ] Era and role(s) correctly assigned?
- [ ] Opening paragraph 200–350 words?
- [ ] 2–4 main sections, each 250–400 words?
- [ ] All claims grounded in named sources?
- [ ] Historiographical significance explained?
- [ ] Literature section 5–12 entries in DGWE format?
- [ ] All titles italicized?
- [ ] Entity links in `[LINK:slug]` format?
- [ ] No markdown, bullets, or hashtags?
- [ ] Total word count 1,200–2,200?

---

## Example: Expanded Entry

**Paracelsus (1493/94–1541)**

*Opening (300 words):*
Paracelsus, born Theophrastus Bombastus von Hohenheim in Switzerland, was a revolutionary physician, alchemist, and natural philosopher whose integration of alchemy with medicine fundamentally altered both disciplines. Active across Switzerland, Germany, and Austria, Paracelsus rejected traditional Galenic medicine and alchemical convention alike, arguing that alchemy's true purpose was to produce medicines, not transmute metals. His rejection of classical authority—he famously burned the works of Galen and Avicenna—and his insistence on empirical observation and experimentation anticipated early modern scientific method. Though his medical theories were often wrong (his chemical explanations of disease), his emphasis on laboratory practice, precise dosing, and chemical preparation of remedies represented a genuine advance. Paracelsus's work bridged alchemy and pharmacy, establishing the legitimacy of chemical medicine alongside traditional herbalism.

*Alchemical Significance:*
For Paracelsus, alchemy was not the pursuit of transmutation but the art of extraction and preparation—the "alchemy" of pulling virtue from matter through heat, dissolution, and distillation. He pioneered the use of mineral medicines (mercury, arsenic, antimony, sulphur) and chemical operations to treat disease. His doctrine of *Iatrochemistry* (medical chemistry) made alchemy an essential component of pharmacy, elevating it from marginal craft to legitimate medical practice. This reorientation—from transmutation to pharmaceutical preparation—proved historically consequential: it allowed alchemy to survive the Scientific Revolution by transforming into early modern chemistry and iatrochemistry.

*Reception:*
Paracelsus was celebrated and vilified in equal measure. His followers (Paracelsians) dominated 16th- and 17th-century medical controversy. Opponents attacked his mysticism and his chemical doctrines. By the 18th century, however, his emphasis on empirical chemistry and pharmaceutical preparation had become mainstream, and his most radical claims (transmutation, universal remedies) had been superseded. Modern scholarship (Moran, 2005) emphasizes Paracelsus as a transitional figure bridging medieval alchemy and early modern chemistry.

---

This style guide establishes scholarly rigor while maintaining accessibility. Apply it consistently across all alchemist, scholar, and text entries.
