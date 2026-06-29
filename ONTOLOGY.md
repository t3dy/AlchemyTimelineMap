# ALCHEMYTIMELINEMAP Database Schema (ONTOLOGY)

**Complete data model for the SQLite database (`alchemy_timeline.db`).**

**Authority:** For machine-readable enum values, `SCHEMA.json` is authoritative. This file provides narrative documentation.

---

## Core Tables

### timeline_events

The primary content unit: a dated, geotagged historical event with scholarly grounding.

```sql
CREATE TABLE timeline_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    date_label TEXT NOT NULL,
    date_start_year INTEGER,
    date_end_year INTEGER,
    location_slug TEXT NOT NULL,
    description TEXT NOT NULL,
    persons_involved TEXT,           -- JSON: ["person1", "person2"]
    texts_involved TEXT,             -- JSON: ["text1", "text2"]
    concepts_involved TEXT,          -- JSON: ["concept1"]
    scholarly_grounding TEXT,        -- Citation: "Scholar Name showed X in *Title* (Year) ch.X pp.XX-YY"
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_slug) REFERENCES locations(slug)
);
```

**Field Documentation:**

- **scholarly_grounding** (TEXT, OPTIONAL): A citation anchoring this event in modern scholarly historiography. Format: `Scholar Name demonstrated/showed/argued X in *Title* (Year) chapter/page references`. Example: `"Lawrence Principe showed Zosimos' operational chemistry prefigured modern chemistry in *Secrets of Alchemy* (2013) ch.2 pp.45-67"`. This field is displayed on the event's index card and detail page to explain *why* this moment matters to the history of science, grounding it in peer-reviewed scholarship rather than speculation.

---

### persons

Alchemists, chemists, scholars, and patrons.

```sql
CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role_primary TEXT NOT NULL CHECK(role_primary IN (
        'ALCHEMIST', 'CHEMIST', 'SCHOLAR', 'PHILOSOPHER', 'PHYSICIAN',
        'TRANSLATOR', 'MATHEMATICIAN', 'POET', 'PATRON', 'CLERICAL'
    )),
    era TEXT NOT NULL CHECK(era IN (
        'ANTIQUITY', 'LATE_ANTIQUE', 'MEDIEVAL', 'RENAISSANCE', 'EARLY_MODERN', 'MODERN'
    )),
    bio_html TEXT NOT NULL,
    transmission_chain TEXT,         -- JSON array of predecessor/successor slugs
    scholarly_disagreement TEXT,     -- plain text note on contested claims
    material_grounding TEXT,         -- plain text on practical context or laboratory work
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### texts

Primary sources, commentaries, compilations, treatises, and scholarship.

```sql
CREATE TABLE texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    text_type TEXT NOT NULL CHECK(text_type IN (
        'PRIMARY_SOURCE', 'COMMENTARY', 'COMPILATION', 'TREATISE', 'SCHOLARSHIP', 'ENCYCLOPEDIA'
    )),
    original_language TEXT,
    composition_date TEXT,
    composition_year_start INTEGER,
    composition_year_end INTEGER,
    analysis_html TEXT NOT NULL,
    transmission_chain TEXT,         -- JSON array
    scholarly_disagreement TEXT,
    material_grounding TEXT,
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### concepts

Chemical operations, alchemical theories, and analytical categories.

```sql
CREATE TABLE concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    label TEXT NOT NULL,
    category_type TEXT NOT NULL CHECK(category_type IN ('ACTOR_TERM', 'ANALYST_TERM')),
    definition_short TEXT NOT NULL,   -- 60–120 words
    definition_long TEXT NOT NULL,    -- 1,500–2,500 words HTML
    operation_type TEXT CHECK(operation_type IN (
        'DISTILLATION', 'SUBLIMATION', 'CALCINATION', 'FERMENTATION', 'CRYSTALLIZATION',
        'DISSOLUTION', 'COAGULATION', 'PUTREFACTION', 'CIRCULATION'
    )),
    scholarly_disagreement TEXT,
    transmission_chain TEXT,
    material_grounding TEXT,
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### processes

The "Twelve Alchemical Processes" (mapped to the zodiac in the early-modern correspondence tradition) plus other major operations. Each process is presented as an index card and a long-form essay page. A process may link to an existing `concepts` row via `concept_slug`; the process page carries the narrative essay and bibliography, while the concept page carries the analytical definition.

```sql
CREATE TABLE processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    sequence_order INTEGER,              -- display order: 1-12 canonical (zodiac order), then extras
    is_canonical_twelve INTEGER NOT NULL DEFAULT 0,  -- 1 = one of the twelve zodiac-mapped processes
    zodiac_sign TEXT CHECK(zodiac_sign IN (
        'ARIES','TAURUS','GEMINI','CANCER','LEO','VIRGO',
        'LIBRA','SCORPIO','SAGITTARIUS','CAPRICORN','AQUARIUS','PISCES'
    )),
    zodiac_glyph TEXT,                   -- Unicode glyph, e.g. U+2648 Aries; NULL for non-canonical
    short_description TEXT NOT NULL,     -- 3-6 sentences (index card)
    essay_html TEXT,                     -- long-form essay (Historical Development / Textual Tradition / Modern Scholarship)
    references_html TEXT,                -- DGWE bibliography
    concept_slug TEXT,                   -- optional FK to concepts(slug)
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (concept_slug) REFERENCES concepts(slug)
);
```

**Provenance note:** the zodiac–process correspondence is an attested early-modern *cryptographic* scheme (Dom Antoine-Joseph Pernety, *Dictionnaire mytho-hermétique*, 1758). Pernety's twelve operations are **related to but distinct from** George Ripley's twelve "gates" in the *Compound of Alchemy* (1471): Ripley's gates are Calcination, Solution, Separation, Conjunction, Putrefaction, Congelation, Cibation, Sublimation, Fermentation, Exaltation, Multiplication, Projection, whereas Pernety substitutes Fixation, Digestion and Distillation and drops Conjunction, Putrefaction, Cibation and Exaltation (the four Ripley gates carried here as non-canonical "other major processes"). The scheme is **not** universal alchemical doctrine — different authors gave different sequences. Pages must attribute the scheme to its source and never imply transmutation was real.

---

### locations

Cities and regions with geographic coordinates for map display.

```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    place_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    region TEXT NOT NULL,
    modern_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Reference Tables

```sql
CREATE TABLE person_event_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_slug TEXT NOT NULL,
    event_slug TEXT NOT NULL,
    FOREIGN KEY (person_slug) REFERENCES persons(slug),
    FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
    UNIQUE(person_slug, event_slug)
);

CREATE TABLE text_event_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_slug TEXT NOT NULL,
    event_slug TEXT NOT NULL,
    FOREIGN KEY (text_slug) REFERENCES texts(slug),
    FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
    UNIQUE(text_slug, event_slug)
);

CREATE TABLE concept_event_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_slug TEXT NOT NULL,
    event_slug TEXT NOT NULL,
    FOREIGN KEY (concept_slug) REFERENCES concepts(slug),
    FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
    UNIQUE(concept_slug, event_slug)
);
```

---

## Enum Values (Vocabulary Lock)

See `SCHEMA.json` for machine-readable authority. All CHECK constraints enforce these values — do not invent new values without updating the schema and `init_db.py` first.

```
era: ANTIQUITY | LATE_ANTIQUE | MEDIEVAL | RENAISSANCE | EARLY_MODERN | MODERN
zodiac_sign: ARIES | TAURUS | GEMINI | CANCER | LEO | VIRGO | LIBRA | SCORPIO | SAGITTARIUS | CAPRICORN | AQUARIUS | PISCES
role_primary: ALCHEMIST | CHEMIST | SCHOLAR | PHILOSOPHER | PHYSICIAN | TRANSLATOR | MATHEMATICIAN | POET | PATRON | CLERICAL
text_type: PRIMARY_SOURCE | COMMENTARY | COMPILATION | TREATISE | SCHOLARSHIP | ENCYCLOPEDIA
category_type: ACTOR_TERM | ANALYST_TERM
operation_type: DISTILLATION | SUBLIMATION | CALCINATION | FERMENTATION | CRYSTALLIZATION | DISSOLUTION | COAGULATION | PUTREFACTION | CIRCULATION
confidence: HIGH | MEDIUM | LOW
review_status: DRAFT | REVIEWED | VERIFIED
source_method: MANUAL | AI_ASSISTED | SCHOLARSHIP_BASED
```

---

## Expected Row Counts

| Table | Rows | Notes |
|-------|------|-------|
| `timeline_events` | 500+ | Primary content unit |
| `persons` | 100+ | Alchemists, chemists, scholars |
| `texts` | 50+ | Treatises, scholarship, compilations |
| `concepts` | 30+ | Chemical operations, theories |
| `processes` | 17 | Twelve zodiac-mapped processes + major extras |
| `locations` | 20+ | Cities, regions with coordinates |

---

*For script execution order see `PIPELINE.md`. For batch enrichment strategy see `CONTEXT_ENGINEERING.md`. For machine-readable schema see `SCHEMA.json`.*
