# ALCHEMYTIMELINEMAP Database Schema (ONTOLOGY)

**Complete data model for the SQLite database (`alchemy_timeline.db`).**

---

## Core Tables

### timeline_events

The primary content unit: a dated, geotagged historical event in the history of alchemy and chemistry.

```sql
CREATE TABLE timeline_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,  -- e.g. "event_000001"
    date_label TEXT NOT NULL,   -- e.g. "c. 1320" or "1250–1300"
    date_start_year INTEGER,    -- for sorting/filtering
    date_end_year INTEGER,      -- for sorting/filtering
    location_slug TEXT NOT NULL,
    description TEXT NOT NULL,  -- 100–250 words (the core content)
    
    -- JSON arrays of slugs (denormalized for query efficiency)
    persons_involved TEXT,      -- JSON: ["person1", "person2"]
    texts_involved TEXT,        -- JSON: ["text1", "text2"]
    concepts_involved TEXT,     -- JSON: ["concept1"]
    
    -- Provenance
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (location_slug) REFERENCES locations(slug)
);
```

**Fields:**
- `slug`: unique identifier (lowercase, hyphens, no special chars)
- `date_label`: human-readable date ("c. 1320", "1250–1300")
- `date_start_year`, `date_end_year`: numeric years for sorting/filtering on timeline
- `location_slug`: FK to locations table
- `description`: 100–250 word plain text (or HTML with `<a href>` tags) describing the event
- `persons_involved`, `texts_involved`, `concepts_involved`: JSON arrays of entity slugs
- Provenance: `source_method`, `review_status`, `confidence`

**Indexing:**
- `CREATE INDEX idx_timeline_date ON timeline_events(date_start_year, date_end_year);`
- `CREATE INDEX idx_timeline_location ON timeline_events(location_slug);`

---

### persons

Alchemists, chemists, scholars, and patrons.

```sql
CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,  -- e.g. "jabir-ibn-hayyan"
    name TEXT NOT NULL,         -- full name
    role_primary TEXT NOT NULL CHECK(role_primary IN (
        'ALCHEMIST', 'CHEMIST', 'SCHOLAR', 'PHILOSOPHER', 'PHYSICIAN',
        'TRANSLATOR', 'MATHEMATICIAN', 'POET', 'PATRON', 'CLERICAL'
    )),
    era TEXT NOT NULL CHECK(era IN (
        'ANTIQUITY', 'LATE_ANTIQUE', 'MEDIEVAL', 'RENAISSANCE', 'EARLY_MODERN', 'MODERN'
    )),
    
    -- Full biography (1,200–2,200 words)
    bio_html TEXT NOT NULL,
    
    -- Provenance
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(name, era)  -- prevent duplicate entries for different eras
);
```

**Fields:**
- `slug`: unique identifier (e.g., "jabir-ibn-hayyan")
- `name`: full name (e.g., "Jabir ibn Hayyan")
- `role_primary`: ALCHEMIST, CHEMIST, SCHOLAR, etc.
- `era`: ANTIQUITY, LATE_ANTIQUE, MEDIEVAL, RENAISSANCE, EARLY_MODERN, MODERN
- `bio_html`: Full HTML biography (1,200–2,200 words, with `<h2>` sections and `<a href>` links)
- Provenance metadata

**Indexing:**
- `CREATE INDEX idx_persons_era ON persons(era);`
- `CREATE INDEX idx_persons_role ON persons(role_primary);`

---

### texts

Primary sources (alchemical treatises, translations), commentaries, scholarship, encyclopedias.

```sql
CREATE TABLE texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,  -- e.g. "corpus-hermeticum"
    title TEXT NOT NULL,        -- full title (italicized in display)
    text_type TEXT NOT NULL CHECK(text_type IN (
        'PRIMARY_SOURCE', 'COMMENTARY', 'COMPILATION', 'TREATISE', 'SCHOLARSHIP', 'ENCYCLOPEDIA'
    )),
    original_language TEXT,     -- Latin, Arabic, Greek, Hebrew, English, etc.
    composition_date TEXT,      -- e.g. "c. 1320" or "1250–1300"
    composition_year_start INTEGER,  -- for sorting/filtering
    composition_year_end INTEGER,
    
    -- Full text description/analysis (1,000–1,800 words)
    analysis_html TEXT NOT NULL,
    
    -- Provenance
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(title, text_type)
);
```

**Fields:**
- `slug`: unique identifier (e.g., "summa-perfectionis")
- `title`: full title of the work
- `text_type`: PRIMARY_SOURCE, COMMENTARY, COMPILATION, TREATISE, SCHOLARSHIP, ENCYCLOPEDIA
- `original_language`: original language of composition
- `composition_date`: human-readable (e.g., "c. 1300")
- `composition_year_start`, `composition_year_end`: numeric years for sorting
- `analysis_html`: HTML description (1,000–1,800 words with sections and citations)
- Provenance metadata

**Indexing:**
- `CREATE INDEX idx_texts_type ON texts(text_type);`
- `CREATE INDEX idx_texts_language ON texts(original_language);`

---

### concepts

Chemical operations, alchemical theories, and analytical categories.

```sql
CREATE TABLE concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,  -- e.g. "distillation"
    label TEXT NOT NULL,        -- term name (e.g., "Distillation")
    category_type TEXT NOT NULL CHECK(category_type IN ('ACTOR_TERM', 'ANALYST_TERM')),
    
    -- Index card (60–120 words)
    definition_short TEXT NOT NULL,
    
    -- Full encyclopedia page (1,500–2,500 words)
    definition_long TEXT NOT NULL,
    
    -- Chemical operation type (if applicable)
    operation_type TEXT CHECK(operation_type IN (
        'DISTILLATION', 'SUBLIMATION', 'CALCINATION', 'FERMENTATION', 'CRYSTALLIZATION',
        'DISSOLUTION', 'COAGULATION', 'PUTREFACTION', 'CIRCULATION'
    )),
    
    -- Provenance
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(label, category_type)
);
```

**Fields:**
- `slug`: unique identifier (e.g., "calcination")
- `label`: term name (e.g., "Calcination")
- `category_type`: ACTOR_TERM (used by historical actors) or ANALYST_TERM (retrospective scholarly category)
- `definition_short`: 60–120 word index card
- `definition_long`: 1,500–2,500 word encyclopedia page (HTML with sections and citations)
- `operation_type`: if this concept is a chemical operation, which one?
- Provenance metadata

**Indexing:**
- `CREATE INDEX idx_concepts_category ON concepts(category_type);`
- `CREATE INDEX idx_concepts_operation ON concepts(operation_type);`

---

### locations

Cities and regions with geographic coordinates for map display.

```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,  -- e.g. "baghdad"
    place_name TEXT NOT NULL,   -- "Baghdad" or "Andalusia"
    latitude REAL NOT NULL,     -- decimal degrees
    longitude REAL NOT NULL,    -- decimal degrees
    region TEXT NOT NULL,       -- broader area ("Iraq", "Iberia", "Italy", etc.)
    modern_name TEXT,           -- modern country/region name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(place_name, latitude, longitude)
);
```

**Fields:**
- `slug`: unique identifier (e.g., "baghdad")
- `place_name`: display name ("Baghdad")
- `latitude`, `longitude`: decimal coordinates for map clustering
- `region`: broader region ("Iraq", "Islamic World", "Europe", etc.)
- `modern_name`: modern country name (e.g., "Iraq", "Spain", "Italy")

**Indexing:**
- `CREATE INDEX idx_locations_region ON locations(region);`

---

## Reference Tables

These tables track relationships between entities for efficient querying and relational browsing.

### person_event_refs

Links persons to timeline events (for easy lookup of "all events involving this person").

```sql
CREATE TABLE person_event_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_slug TEXT NOT NULL,
    event_slug TEXT NOT NULL,
    FOREIGN KEY (person_slug) REFERENCES persons(slug),
    FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
    UNIQUE(person_slug, event_slug)
);
```

---

### text_event_refs

Links texts to timeline events.

```sql
CREATE TABLE text_event_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_slug TEXT NOT NULL,
    event_slug TEXT NOT NULL,
    FOREIGN KEY (text_slug) REFERENCES texts(slug),
    FOREIGN KEY (event_slug) REFERENCES timeline_events(slug),
    UNIQUE(text_slug, event_slug)
);
```

---

### concept_event_refs

Links concepts to timeline events.

```sql
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

### concept_person_refs

Links concepts to persons (for "which concepts did this alchemist engage with?").

```sql
CREATE TABLE concept_person_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_slug TEXT NOT NULL,
    person_slug TEXT NOT NULL,
    FOREIGN KEY (concept_slug) REFERENCES concepts(slug),
    FOREIGN KEY (person_slug) REFERENCES persons(slug),
    UNIQUE(concept_slug, person_slug)
);
```

---

### concept_text_refs

Links concepts to texts (for "which concepts are discussed in this treatise?").

```sql
CREATE TABLE concept_text_refs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_slug TEXT NOT NULL,
    text_slug TEXT NOT NULL,
    FOREIGN KEY (concept_slug) REFERENCES concepts(slug),
    FOREIGN KEY (text_slug) REFERENCES texts(slug),
    UNIQUE(concept_slug, text_slug)
);
```

---

## Aggregate Views (Optional)

For efficient reporting and site generation, consider creating materialized views:

```sql
-- Events with all related entities joined (for JSON export)
CREATE VIEW event_with_entities AS
SELECT 
    te.slug, te.date_label, te.date_start_year, te.date_end_year,
    te.location_slug, l.place_name, l.latitude, l.longitude, l.region,
    te.description,
    GROUP_CONCAT(DISTINCT p.slug) as person_slugs,
    GROUP_CONCAT(DISTINCT t.slug) as text_slugs,
    GROUP_CONCAT(DISTINCT c.slug) as concept_slugs
FROM timeline_events te
LEFT JOIN locations l ON te.location_slug = l.slug
LEFT JOIN person_event_refs per ON te.slug = per.event_slug
LEFT JOIN persons p ON per.person_slug = p.slug
LEFT JOIN text_event_refs ter ON te.slug = ter.event_slug
LEFT JOIN texts t ON ter.text_slug = t.slug
LEFT JOIN concept_event_refs cer ON te.slug = cer.event_slug
LEFT JOIN concepts c ON cer.concept_slug = c.slug
GROUP BY te.slug;
```

---

## Enum Values (Vocabulary Lock)

All CHECK constraints enforce these values. Do not invent new values without updating the schema first.

```
era: ANTIQUITY | LATE_ANTIQUE | MEDIEVAL | RENAISSANCE | EARLY_MODERN | MODERN

role_primary: ALCHEMIST | CHEMIST | SCHOLAR | PHILOSOPHER | PHYSICIAN | TRANSLATOR | MATHEMATICIAN | POET | PATRON | CLERICAL

text_type: PRIMARY_SOURCE | COMMENTARY | COMPILATION | TREATISE | SCHOLARSHIP | ENCYCLOPEDIA

category_type: ACTOR_TERM | ANALYST_TERM

operation_type: DISTILLATION | SUBLIMATION | CALCINATION | FERMENTATION | CRYSTALLIZATION | DISSOLUTION | COAGULATION | PUTREFACTION | CIRCULATION

confidence: HIGH | MEDIUM | LOW

review_status: DRAFT | REVIEWED | VERIFIED

source_method: MANUAL | AI_ASSISTED | SCHOLARSHIP_BASED
```

---

## Expected Row Counts (Phase 0 Target)

| Table | Rows | Notes |
|-------|------|-------|
| `timeline_events` | 500 | Primary content unit |
| `persons` | 100–120 | Alchemists, chemists, scholars |
| `texts` | 50–60 | Treatises, scholarship, compilations |
| `concepts` | 30–40 | Chemical operations, theories |
| `locations` | 20–25 | Cities, regions with coordinates |
| `person_event_refs` | 200–300 | Each person in ~2–3 events |
| `text_event_refs` | 150–200 | Each text in ~2–4 events |
| `concept_event_refs` | 300–400 | Each event ~0.7 concepts avg |
| `concept_person_refs` | 150–200 | Historians, practitioners engaging with concepts |
| `concept_text_refs` | 100–150 | Concepts discussed in texts |

---

*See `PIPELINE.md` for script execution order. See `CONTEXT_ENGINEERING.md` for efficient querying of timeline events.*
