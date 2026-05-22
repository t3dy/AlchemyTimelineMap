# ALCHEMYTIMELINEMAP: Canonical Vision and Prompts

**This file is the single document AI agents read before beginning any content or architecture work on ALCHEMYTIMELINEMAP. It compiles the user's expressed vision and the historiographical framework governing the project.**

---

## Part I: Project Vision

ALCHEMYTIMELINEMAP is an authoritative, interactive portal for the history of alchemy and the chemical sciences from Late Antiquity through the early modern period. It combines a **500-event interactive timeline** with a **geo-pinned map** covering Europe, North Africa, and the Middle East, allowing scholars, students, and independent researchers to explore the chemical discoveries, alchemical theories, key texts, and pivotal figures that shaped the tradition.

The portal is **not** esoteric or mystical. It is a rigorous, provenance-aware historical resource structured for academic browsing and discovery, built to the historiographical standards of **William R. Newman** (*Atoms and Alchemy*, Yale), **Michela Pereira** (medieval alchemy), and the *Dictionary of Gnosis and Western Esotericism* (Hanegraaff, Brill, 2006).

**The model for every entry is the DGWE itself:** scholarly precision, chronological depth, named sources, and transparent attention to historiographical disputes.

**What this portal is NOT:**
- An esoteric or New Age resource
- A guide to alchemical practice or transmutation claims
- A Wikipedia mirror
- A collection of AI-generated summaries without scholarly grounding

**The tone is always:** critical, reportorial, provenance-aware. Disagreements between scholars are named explicitly.

---

## Part II: Three Constituencies

Every page and event must serve all three simultaneously:

1. **Scholars**: Need precision, historiographical nuance, named sources, complete bibliography, relational links to primary texts and secondary literature. They will tolerate no vagueness.

2. **Students**: Need accessible prose, definitions on first use of technical terms (distillation, calcination, transmutation, etc.), clear chronological frameworks, and visual scaffolding (the map and timeline themselves serve this purpose). They will be lost without context.

3. **Serious independent researchers**: Need depth, the ability to follow a thread from one event to a related figure to a text to a concept, and delightful browsing. A user should be able to start at a European city's 14th-century alchemical circle, jump to a specific figure (Roger Bacon), follow a link to texts they wrote, and discover which concepts they engaged with.

**Design principle for constituency 3:** Every event must link to at least one person, one text, and ideally one concept or location. The map and timeline must both be full of outbound links. The user should never reach a dead end.

---

## Part III: Historiographical Framework (Bake These In)

The following principles are not stylistic preferences — they are the intellectual foundation of this project. Every agent and contributor must internalize them:

### 3.1 Alchemy Is Not (Just) Chemistry

Modern historiography distinguishes between:
- **Alchemy**: A tradition of texts, practices, and ideas about transformation, spiritual perfection, and the manipulation of matter through secret operations. Practitioners believed they were working toward transmutation of base metals into gold (and spiritual perfection). Whether this was literally possible is irrelevant to understanding why they pursued it.
- **Chemistry**: The modern discipline that emerged from alchemy but abandoned transmutational claims, grounding itself in empirical experimentation and eventually atomic theory.

**Do not collapse these registers.** Historical actors called themselves *alchemists*, not chemists. When discussing their work, use their own language. When discussing modern understanding, signal clearly that we are using retrospective analytical categories.

### 3.2 Medieval Continuity in Arabic and Latin

The tradition of alchemy is **not** an invention of the European Renaissance. It has continuous roots in:
- **Late Antique and Byzantine alchemical texts** (Zosimos of Panopolis, 3rd century)
- **Arabic alchemical tradition** (Jabir ibn Hayyan / Geber, 8th–9th century; Abu Ma'shar; al-Razi; the *Emerald Tablet* and its Arabic recensions)
- **Latin medieval tradition** (Gerard of Cremona translations, 12th century; Roger Bacon, 13th century; alchemical encyclopedias)

The Renaissance "discovery" of classical alchemy was built on this continuous, unbroken medieval transmission. Never treat the medieval period as a gap or dark age.

### 3.3 Chemical Operations Are Real

When an alchemist describes distillation, sublimation, fermentation, or crystallization, they are describing **actual chemical operations** that produce measurable, observable results. These operations were genuine advances in practical chemistry — what they *believed* about transmutation was separate from what they could *actually do* with matter.

Separate the operational knowledge (valuable) from the transmutational theory (historically contingent). Both deserve serious treatment, but they are different things.

### 3.4 Provenance on Every Claim

Every substantive assertion must be traceable to a named source. Integrate citations organically: "As William Newman argues in *Atoms and Alchemy* (2006)..." Do not use footnote brackets — write citations into prose. Every event description must conclude with a single-sentence historiographical significance statement.

### 3.5 Geographic Specificity

Every event must have a specific location (city, ideally; region at minimum) with coordinates. The map is not decoration — it is a primary research tool. Clustering of events in certain regions (Baghdad, 9th century; medieval Iberia; Renaissance Italy; early modern Antwerp) reveals the geography of alchemical knowledge.

### 3.6 Chemical Taxonomy

Chemical operations and theoretical categories (distillation, fermentation, transmutation, quintessence, etc.) are **first-class concepts** in this portal. They are not buried in text — they appear as filterable categories on the timeline and as browsable concept pages.

---

## Part IV: Content Standards

The following are the **minimum** requirements for each content type. Read `STYLEGUIDE.md` for full specifications.

### Timeline Event (the primary content unit)
- **100–250 words**, plain text
- **Exact date or date range** (CE/BCE), location with coordinates, named actors
- **One sentence of historiographical significance**: Why does this matter to the history of alchemy and chemistry specifically?
- At least one link to a person, text, or concept

**Example:**
> "c. 1320, Bologna: Attended scholars from the *Stadium* of Bologna's natural philosophy faculty gathered in private to discuss alchemical texts recently translated from Arabic, including the *Summa Perfectionis* (attributed to Jabir ibn Hayyan). This event represents the infiltration of alchemical thought into a major European university center where natural philosophy was already institutionalized, marking a shift from alchemy's previous isolation in monastic scriptoria and solitary practitioners' laboratories."

### Person Biography (bio_html field)
- 1,200–2,200 words total
- Opening paragraph: 200–350 words
- 2–4 `<h2>` sections: 250–400 words each
- Literature section: 5–12 references
- Must specify: role (ALCHEMIST, CHEMIST, SCHOLAR, PHILOSOPHER, PHYSICIAN, etc.)
- Must specify: era (ANTIQUITY, MEDIEVAL, EARLY_MODERN, MODERN)

### Text Description (analysis_html field)
- 1,000–1,800 words total
- Opening paragraph: 200–300 words
- Sections: Composition and Textual Tradition / Content and Theory / Modern Scholarship
- Literature section: 5–12 references
- Must distinguish: PRIMARY SOURCE vs. COMMENTARY vs. SCHOLARSHIP

### Concept Definition (definition_long field)
- 1,500–2,500 words
- Required sections: Historical Usage → Scholarly Significance → Related Concepts → Literature
- Must specify: ACTOR_TERM (used by historical alchemists) vs. ANALYST_TERM (modern historiographical category)
- At least 3 hyperlinks to related entities

---

## Part V: Architecture Principles

### 5.1 Timeline as Primary Navigation

Unlike the EmeraldTablet (dictionary-first), ALCHEMYTIMELINEMAP is **timeline-first**:
- `/timeline/` — the home view: chronological slider showing 500 events
- `/map/` — geographic view: Leaflet map with clustered pins, filterable by era/region/figure
- `/persons/[slug].html` — biography pages (secondary)
- `/texts/[slug].html` — text description pages (secondary)
- `/concepts/[slug].html` — concept pages (secondary)

Events are the atoms; persons, texts, concepts are the links between them.

### 5.2 Geo-Pinning and Clustering

Every event has (latitude, longitude, place_name). The map is **not** decorative—it shows:
- Event density by region (Baghdad 9th century, Iberia 12th century, Italy 15th century, etc.)
- Geographic transmission of knowledge
- Regional variations in alchemical practice

Clusters are calculated in JavaScript; the backend exports a JSON data file with coordinates.

### 5.3 Relational Browsing (No Dead Ends)

Every entity page must link to at least 3 other entities. The timeline event description must mention at least one person, text, or concept by name (these are rendered as hyperlinks in the final HTML).

### 5.4 Pipeline Rules
- All data enters via idempotent Python scripts in `scripts/`
- No hardcoded database row IDs — use slugs
- All agent output goes to `staging/` first, validated before DB insertion
- Staging files are JSON with `[LINK:slug]` placeholders for the main session to convert to `<a href>` tags
- Clear stale HTML before regenerating pages
- Export `data.json` for JavaScript timeline/map consumers

---

## Part VI: Key Scholarly Authorities

These are the primary scholarly authorities whose frameworks govern this portal:

| Scholar | Key Work | Relevance |
|---------|----------|-----------|
| William R. Newman | *Atoms and Alchemy* (Yale, 2006); *The Summa Perfectionis* (2016) | Master of alchemical texts; operational chemistry vs. transmutational theory distinction |
| Michela Pereira | *The Alchemical Corpus Attributed to Ray Lull* (2007) | Medieval alchemy, especially Catalan tradition |
| Eric John Holmyard | *Alchemy* (1957, Dover reissue 2005) | Classic historiographical overview |
| Stanton J. Loomis | *The Chemistry in Western History* | History of chemistry's emergence from alchemy |
| Garth Fowden | *The Egyptian Hermes* (1986) | Late Antique roots of alchemical thought |
| Wouter J. Hanegraaff | *Dictionary of Gnosis and Western Esotericism* (2006) | Methodological framework; historiographical principles |
| Lawrence Principe | Works on practical alchemy and transmutation claims | Modern reassessment of alchemical operations |
| Pamela Smith | *The Business of Alchemy* (2005) | Early modern alchemy and craft knowledge |

---

## Part VII: Vocabulary Lock

All enum values are defined in `scripts/init_db.py` CHECK constraints. Do not invent new values without adding them to the schema first.

```
era:           ANTIQUITY | LATE_ANTIQUE | MEDIEVAL | RENAISSANCE | EARLY_MODERN | MODERN
role_primary:  ALCHEMIST | CHEMIST | SCHOLAR | PHILOSOPHER | PHYSICIAN | TRANSLATOR | MATHEMATICIAN | POET | PATRON | CLERICAL
text_type:     PRIMARY_SOURCE | COMMENTARY | COMPILATION | TREATISE | SCHOLARSHIP | ENCYCLOPEDIA
category_type: ACTOR_TERM | ANALYST_TERM
operation:     DISTILLATION | SUBLIMATION | CALCINATION | FERMENTATION | CRYSTALLIZATION | DISSOLUTION | COAGULATION | PUTREFACTION | CIRCULATION
confidence:    HIGH | MEDIUM | LOW
review_status: DRAFT | REVIEWED | VERIFIED
```

---

## Part VIII: Agent Operating Rules

### 8.1 Three Standard Agent Types

**Agent Type A — Timeline Event Enricher**
- Given: A batch of 20–50 event stubs (date, location, involved persons/texts/concepts)
- Pre-queried context: Full entity list (persons, texts, concepts) as JSON
- Task: Write event descriptions (100–250 words each) with historiographical significance
- Output: `staging/timeline_events_batch_[era]_[region].json` with descriptions
- Constraints: Must reach 100–250 words; must declare historiographical significance explicitly; must mention ≥1 named person/text/concept; all entity names must be wrapped in `[LINK:slug]` markup

**Agent Type B — Biography Enricher**
- Given: Person slug, role, era, brief notes on their contributions
- Pre-queried context: All texts they authored/translated, all events involving them
- Task: Write complete biography (1,200–2,200 words)
- Output: `staging/persons/[slug].json`
- Constraints: Must reach 1,200–2,200 words; must name ≥2 specific texts; must cite ≥2 named scholars

**Agent Type C — Relational Auditor**
- Given: Full entity list (persons, texts, concepts) as JSON
- Task: Audit for dead ends, ensure every entity links to ≥3 others
- Output: `staging/audit_relational.json` with recommended cross-links
- No database access needed

### 8.2 Context-Efficient Querying for 500 Events

To avoid context explosion with 500 timeline events, the pipeline uses **pre-loaded entity batches**:

1. **Main session pre-queries**: For each batch of 20–50 events, fetch all involved persons, texts, concepts as JSON
2. **Agent receives**: Batch of event stubs + compact JSON context
3. **Agent writes**: Event descriptions (using `[LINK:slug]` markup)
4. **Main session converts**: `[LINK:slug]` → `<a href=../persons/[slug].html>[name]</a>`

See `CONTEXT_ENGINEERING.md` for detailed query patterns.

### 8.3 Staging File Pattern

All agent output goes to `staging/` before validation and DB insertion. Staging files use this schema:

```json
{
  "entities": [
    {
      "type": "timeline_event",
      "date": "c. 1460",
      "location_slug": "florence",
      "description": "Event description with [LINK:person_slug] and [LINK:text_slug]...",
      "persons_involved": ["person1", "person2"],
      "texts_involved": ["text1"],
      "concepts_involved": ["concept1"]
    }
  ],
  "metadata": {
    "batch_id": "era_region",
    "agent_type": "A",
    "timestamp": "2026-05-21T10:00:00Z",
    "confidence": "MEDIUM",
    "review_status": "DRAFT"
  }
}
```

---

## Part IX: Project Phases

| Phase | Goal | Status |
|-------|------|--------|
| **1** | Database schema + seed data | Planned |
| **2** | Timeline event skeleton (500 stubs) | Planned |
| **3** | Enrich events via agent swarm (batched) | Planned |
| **4** | Map + timeline UI + relational browsing | Planned |
| **5** | Deploy + refinement | Planned |

---

*This document is referenced in `CLAUDE.md` and must be consulted at the start of any session that will produce content or architecture work on ALCHEMYTIMELINEMAP.*
