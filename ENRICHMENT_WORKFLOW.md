# Enrichment Workflow — ALCHEMYTIMELINEMAP

**Purpose:** Convert working notes (extracted from markdown sources) into full, scholarly database entries (timeline events, person biographies, text descriptions, concept definitions).

**Audience:** Content writers, enrichment agents, scholarly editors.

**Updated:** 2026-06-14

---

## PHASE 1: PREPARATION

### Step 1.1: Review Your Batch

You have received a batch of working notes (typically 10–20 sources per batch, grouped by era/region).

**Deliverable for this step:** `[BATCH_NAME]_enrichment_plan.md`

```markdown
# Enrichment Plan: [Region/Era]

**Batch:** [Name, e.g., "Early Islamic Baghdad, 9th century"]
**Working notes:** [List of note_*.md files]
**Sources:** [Original PDF titles]
**Expected output:** [X persons, Y texts, Z events, C concepts]

## Entity Triage

### New Persons (Need full biographies)
- [ ] Person A
- [ ] Person B

### New Texts (Need descriptions/analyses)
- [ ] Text A
- [ ] Text B

### New Concepts (Need definitions)
- [ ] Concept A
- [ ] Concept B

### New Timeline Events (Need 100–250 word descriptions)
- [ ] Event A
- [ ] Event B

## Historiographical Context

[2–3 sentences on the era/region and its significance to alchemy/chemistry history. Reference key scholars in CONCEPTUAL_FRAMEWORK.md]

## Quality Targets

- Persons: 1,200+ words per biography
- Texts: 1,000+ words per analysis
- Concepts: 1,500+ words per definition
- Events: 100–250 words per description
- Confidence: Target HIGH where possible, accept MEDIUM with justification
```

### Step 1.2: Load Your Schema Context

Before writing anything, consult:

1. **CLAUDE.md** (5 min) — Mission, core invariants, vocab lock
2. **PHASESTATUS.md** (2 min) — Current phase, success criteria
3. **CONCEPTUAL_FRAMEWORK.md** (8 min) — Historiographical principles, Actor/Analyst distinction
4. **SCHEMA.json** (3 min) — Valid enum values for era_slug, role, review_status, confidence
5. **STANDARD_[TYPE].md** (10 min) — Specific format for each content type (events, persons, texts, concepts)

---

## PHASE 2: PERSON BIOGRAPHY ENRICHMENT

### Task 2.1: Create Person Entry

**Input:** Working note with person identified  
**Output:** Full biography, 1,200–2,200 words, ready for database insertion

**Format:** See `STANDARD_PERSON_BIOGRAPHIES.md`

**Required sections:**
1. **Biographical summary** (2–3 sentences)
2. **Life and activity** (dates, roles, major work)
3. **Key intellectual contributions** (what did they do? why does it matter?)
4. **Influence and transmission** (who read them? how did their work circulate?)
5. **Scholarly assessment** (modern historiographical context)
6. **Literature** (8–12 references in DGWE format)

**Quality checklist:**
- [ ] All dates are precise or flagged as approximate (c. 1200, fl. 1250, etc.)
- [ ] Actor/Analyst distinction explicit (e.g., "Paracelsus called himself an alchemist; modern scholars classify him as...")
- [ ] No endorsement of transmutation claims (e.g., "He believed he could transmute lead into gold" ≠ "He could transmute...")
- [ ] Material culture included (apparatus, laboratory conditions, dangers)
- [ ] At least 3 named scholars cited
- [ ] All entity links use `[LINK:slug]` format and reference existing entities
- [ ] Word count: 1,200–2,200 (plain text, no HTML)
- [ ] Bibliography: DGWE format (Author LastName, *Title*, Publisher, Year)

**Example structure:**

```markdown
# [Person Name]

**Era:** [Medieval / Renaissance / Early Modern]
**Role:** [Alchemist, Physician, Polymath, etc.]
**Lifespan:** [Birth–Death, if known; otherwise "fl. 1250" for flourished]

## Biographical Summary

[2–3 sentences introducing the person and their historical significance]

## Life and Activity

[Organized by phase or decade. Specific dates. Key events.]

## Intellectual Contributions

[What did they discover, invent, write? Why does it matter to alchemy/chemistry history?]

## Influence and Transmission

[Who read their work? How did it circulate? Translations? Commentaries? Misreadings?]

## Scholarly Assessment

[Modern historiographical context. Which scholars write about this person? What's debated?]

## Literature

- Smith, Pamela (Year). *The Business of Alchemy*. Princeton University Press, pp. XX–YY.
- [8–12 more references]
```

### Task 2.2: Validate Person Entry

Before saving to staging/:

```python
# Check word count
word_count = len(bio_html.split())
assert 1200 <= word_count <= 2200, f"Word count {word_count} out of range"

# Check links
import re
links = re.findall(r'\[LINK:(\w+)\]', bio_html)
for slug in links:
    assert slug_exists_in_db(slug), f"Link [LINK:{slug}] references non-existent entity"

# Check bibliography
bib_count = len(re.findall(r'^- [A-Z][a-z]+', bio_html, re.MULTILINE))
assert bib_count >= 8, f"Bibliography has only {bib_count} items (minimum 8)"

# Check for markdown artifacts
assert not re.search(r'(?:^|\s)#+\s|(?:^|\s)\*+|(?:^|\s)-\s\[', bio_html), "Markdown artifacts detected"
```

---

## PHASE 3: TEXT DESCRIPTION ENRICHMENT

### Task 3.1: Create Text Entry

**Input:** Working note with text identified  
**Output:** Full analysis/description, 1,000–1,800 words

**Format:** See `STANDARD_TEXT_DESCRIPTIONS.md`

**Required sections:**
1. **Bibliographic data** (Title, author, date, format)
2. **Content and scope** (What does the text contain? Major sections?)
3. **Historical context** (Why was it written? For whom?)
4. **Scholarly significance** (Why do modern scholars care about this text?)
5. **Transmission history** (Manuscripts, translations, editions, misreadings)
6. **Literature** (6–10 scholarly references)

**Quality checklist:**
- [ ] All dates are precise or flagged as approximate
- [ ] Transmission history accounts for translations and commentary layers
- [ ] Links to key persons, concepts, and related texts
- [ ] Distinguishes primary content from later interpretations
- [ ] At least 2 named modern scholars cited
- [ ] Word count: 1,000–1,800 (plain text, no HTML)
- [ ] Bibliography: DGWE format

---

## PHASE 4: CONCEPT DEFINITION ENRICHMENT

### Task 4.1: Create Concept Entry

**Input:** Working note with concept identified  
**Output:** Full definition, 1,500–2,500 words, with explicit Actor/Analyst distinction

**Format:** See `STANDARD_CONCEPT_DEFINITIONS.md`

**Required sections:**
1. **Actor/Analyst declaration** (Is this a term practitioners used, or a modern analytical category?)
2. **Historical definition** (How did practitioners define/use this term?)
3. **Material grounding** (What equipment, materials, observable results?)
4. **Transmission** (How did understanding of this concept evolve over time?)
5. **Scholarly significance** (Modern historiographical disputes about this concept)
6. **Related concepts** (Links to 3–5 other concepts)
7. **Literature** (8–15 scholarly references)

**Quality checklist:**
- [ ] ACTOR_TERM vs. ANALYST_TERM is explicit in opening
- [ ] If ACTOR_TERM: material grounding included (equipment, temperatures, visible results)
- [ ] If ANALYST_TERM: historiographical debate explained
- [ ] Etymology provided (Latin, Greek, Arabic, etc. if relevant)
- [ ] At least 3 named scholars cited
- [ ] Links to at least 3 other concepts using `[LINK:slug]`
- [ ] Word count: 1,500–2,500 (plain text, no HTML)
- [ ] Bibliography: DGWE format

**Example structure:**

```markdown
# [Concept Name]

**Type:** ACTOR_TERM / ANALYST_TERM  
**Etymology:** [Latin/Greek/Arabic term, if applicable]  
**First attestation:** [Date or text where term first appears]

## Canonical Definition

[How practitioners defined this; how modern scholars understand it]

## Historical Usage

[Evolution of the concept over time; regional variations; name changes]

## Material Grounding [for ACTOR_TERM]

[Equipment: What apparatus was used?]
[Procedure: What steps?]
[Results: What were the observable, reproducible outcomes?]
[Dangers: What hazards did practitioners face?]

## Historiographical Significance

[Why do modern scholars care about this concept? What debates exist?]
[Which scholars argue what positions?]

## Related Concepts

- [LINK:related-concept-1]
- [LINK:related-concept-2]
- [LINK:related-concept-3]

## Literature

[8–15 references]
```

---

## PHASE 5: TIMELINE EVENT ENRICHMENT

### Task 5.1: Create Event Entry

**Input:** Event candidate from working note (date, location, actors)  
**Output:** Full description, 100–250 words, with scholarly grounding

**Format:** See `STANDARD_TIMELINE_EVENTS.md`

**Required fields:**
- `date_label` (e.g., "c. 825", "1200–1210")
- `date_sort` (numeric year for sorting)
- `location_slug` (reference to existing location in database)
- `era_slug` (reference to existing era: medieval, renaissance, early-modern)
- `title` (brief event title, 5–10 words)
- `description` (100–250 words)
- `scholarly_grounding` (citation to named modern scholar)
- `persons_involved` (list of `[LINK:slug]`)
- `texts_involved` (list of `[LINK:slug]`)
- `concepts_involved` (list of `[LINK:slug]`)

**Description structure:**

```
[Date/location]: [Main narrative - what happened, who did it, what was discovered].

[Significance - why this matters to alchemy/chemistry history].
[Connection to broader developments or transmission].
```

**Quality checklist:**
- [ ] Date is precise or reasonably approximate
- [ ] Location is a city (or region if city unknown)
- [ ] At least 1 person, 1 text, or 1 concept linked
- [ ] Word count: 100–250 (plain text, no HTML tags)
- [ ] Scholarly grounding present: "Scholar LastName [demonstrated/showed/argued] X in *Title* (Year) ch.X pp.XX-YY"
- [ ] All `[LINK:slug]` references exist in database
- [ ] No markdown artifacts in prose

**Example:**

```json
{
  "date_label": "c. 825",
  "date_sort": 825,
  "era_slug": "early-medieval",
  "location_slug": "baghdad",
  "title": "Jabir ibn Hayyan's Distillation Experiments",
  "description": "c. 825, Baghdad: The Persian alchemist [LINK:jabir-ibn-hayyan] conducted systematic distillation experiments, producing concentrated essences and volatile liquids from plant and mineral sources. Working in the context of the Abbasid intellectual flourishing, Jabir documented his operations with unprecedented precision, distinguishing between [LINK:distillation] and [LINK:sublimation], and emphasizing the importance of controlled heat and sealed apparatus. His work represented a major advance in the material understanding of chemical transformation, moving beyond allegorical descriptions to precise, reproducible laboratory operations.\n\nWilliam Newman demonstrated Jabir's sophisticated experimentalism in *The Summa Perfectionis of Pseudo-Geber* (2016), ch. 3, pp. 89–124, establishing him as a genuine pioneer of operational chemistry rather than a mystical fantasist.",
  "scholarly_grounding": "William Newman demonstrated Jabir ibn Hayyan's sophisticated experimentalism in *The Summa Perfectionis of Pseudo-Geber* (2016) ch. 3 pp. 89–124",
  "review_status": "DRAFT",
  "confidence": "HIGH"
}
```

---

## PHASE 6: VALIDATION & STAGING

### Task 6.1: Prepare Staging JSON

Before submitting to main session, prepare JSON file in `staging/`:

**File:** `staging/[BATCH_NAME]_enriched_entities.json`

```json
{
  "batch_name": "[Region/Era]",
  "created": "2026-06-14T14:30:00",
  "persons": [
    {
      "slug": "jabir-ibn-hayyan",
      "name": "Jabir ibn Hayyan",
      "name_alternate": ["Geber", "Geberus"],
      "era": "Early Medieval",
      "role": "Alchemist",
      "bio_html": "[Full biography text...]",
      "source_method": "PDF_INGESTION:source_file.md",
      "review_status": "DRAFT",
      "confidence": "HIGH",
      "literature": [
        "Newman, William R. (Year). *Title*. Publisher, pp. XX–YY."
      ]
    }
  ],
  "texts": [
    {
      "slug": "summa-perfectionis",
      "title": "Summa Perfectionis",
      "author_slug": "pseudo-geber",
      "date_label": "c. 1300",
      "analysis": "[Full text analysis...]",
      "source_method": "PDF_INGESTION:source_file.md",
      "review_status": "DRAFT",
      "confidence": "MEDIUM"
    }
  ],
  "concepts": [
    {
      "slug": "distillation",
      "term": "Distillation",
      "type": "ACTOR_TERM",
      "definition_long": "[Full definition...]",
      "source_method": "PDF_INGESTION:source_file.md",
      "review_status": "DRAFT",
      "confidence": "HIGH"
    }
  ],
  "events": [
    {
      "date_label": "c. 825",
      "date_sort": 825,
      "era_slug": "early-medieval",
      "location_slug": "baghdad",
      "title": "Jabir ibn Hayyan's Distillation Experiments",
      "description": "[100–250 word description with [LINK:slug] markup...]",
      "scholarly_grounding": "Scholar LastName demonstrated X in *Title* (Year) ch.X pp.XX-YY",
      "persons_involved": ["jabir-ibn-hayyan"],
      "texts_involved": [],
      "concepts_involved": ["distillation"],
      "source_method": "PDF_INGESTION:source_file.md",
      "review_status": "DRAFT",
      "confidence": "HIGH"
    }
  ]
}
```

### Task 6.2: Validation Checklist

Run these checks before marking batch as "READY FOR MAIN SESSION":

```markdown
# [BATCH_NAME] Validation Checklist

## Persons (N total)
- [ ] All [X] persons have biographies 1,200–2,200 words
- [ ] All biographies include Literature section with 8+ references
- [ ] All biographies include Actor/Analyst distinction where relevant
- [ ] All dates are precise or marked as approximate (c., fl., etc.)
- [ ] All person links are validated against SCHEMA.json
- [ ] Word counts: MIN [X], MAX [Y], AVERAGE [Z]

## Texts (N total)
- [ ] All [X] texts have analyses 1,000–1,800 words
- [ ] All analyses include Transmission History section
- [ ] All analyses include Literature section with 6+ references
- [ ] All text links are validated against SCHEMA.json
- [ ] Word counts: MIN [X], MAX [Y], AVERAGE [Z]

## Concepts (N total)
- [ ] All [X] concepts have definitions 1,500–2,500 words
- [ ] All definitions declare ACTOR_TERM or ANALYST_TERM explicitly
- [ ] All ACTOR_TERM concepts include Material Grounding section
- [ ] All ANALYST_TERM concepts include Historiographical Significance section
- [ ] All concepts include Related Concepts links (3+ each)
- [ ] All concepts include Literature section with 8+ references
- [ ] Word counts: MIN [X], MAX [Y], AVERAGE [Z]

## Timeline Events (N total)
- [ ] All [X] events have descriptions 100–250 words
- [ ] All events have scholarly_grounding citations
- [ ] All events link to at least 1 person/text/concept
- [ ] All [LINK:slug] references validated against SCHEMA.json
- [ ] All dates are valid and sortable
- [ ] All locations are valid location_slugs
- [ ] All eras are valid era_slugs
- [ ] No markdown artifacts detected
- [ ] Word counts: MIN [X], MAX [Y], AVERAGE [Z]

## Cross-references
- [ ] No broken [LINK:slug] references
- [ ] All person slugs unique
- [ ] All text slugs unique
- [ ] All concept slugs unique
- [ ] All event titles unique (within reasonable bounds)

## Quality Metrics
- [ ] Confidence distribution: HIGH [X]%, MEDIUM [Y]%, LOW [Z]%
- [ ] Review status: DRAFT [X], READY_FOR_REVIEW [Y], REVIEWED [Z]
- [ ] Source attribution complete (source_method on every row)
- [ ] Bibliography consistency: All DGWE format, proper citations

## Ready for Main Session?
**Date:** _______________  
**Validator:** _______________  
**Status:** ☐ PASS / ☐ CONDITIONAL (Flagged for: ___) / ☐ NEEDS WORK

---
```

---

## PHASE 7: HANDOFF TO MAIN SESSION

When batch is complete and validated:

1. **Copy staging JSON to staging/ directory**
2. **Update `staging/BATCH_STATUS.md`** with completion date and metrics
3. **Notify main session** (output summary below)

**Handoff summary:**

```markdown
# Enrichment Batch Complete: [BATCH_NAME]

**Completed:** [ISO date]
**Enriched by:** [Name/Agent ID]

## Deliverables

### Persons
- Count: [X]
- Word count range: [MIN]–[MAX] (average [AVG])
- Confidence: [HIGH/MEDIUM/LOW distribution]
- Staging file: `staging/[BATCH]_persons.json`

### Texts
- Count: [X]
- Word count range: [MIN]–[MAX] (average [AVG])
- Confidence: [HIGH/MEDIUM/LOW distribution]
- Staging file: `staging/[BATCH]_texts.json`

### Concepts
- Count: [X]
- Word count range: [MIN]–[MAX] (average [AVG])
- Confidence: [HIGH/MEDIUM/LOW distribution]
- Staging file: `staging/[BATCH]_concepts.json`

### Events
- Count: [X]
- Word count range: [MIN]–[MAX] (average [AVG])
- Confidence: [HIGH/MEDIUM/LOW distribution]
- Scholarly grounding: [X]% coverage
- Staging file: `staging/[BATCH]_events.json`

## Quality Metrics

- Validation: ✅ PASS
- Broken links: 0
- Markdown artifacts: 0
- Missing bibliographies: 0

## Notes

[Any historiographical insights, patterns, or recommendations for next batch]
```

---

## APPENDIX A: QUICK REFERENCE — REQUIRED FIELDS

### Person
- slug, name, era, role, bio_html (1,200+ words), source_method, review_status, confidence, literature

### Text
- slug, title, author_slug, date_label, analysis (1,000+ words), source_method, review_status, confidence

### Concept
- slug, term, type (ACTOR_TERM/ANALYST_TERM), definition_long (1,500+ words), source_method, review_status, confidence

### Event
- date_label, date_sort, era_slug, location_slug, title, description (100–250 words), scholarly_grounding, persons_involved, texts_involved, concepts_involved, source_method, review_status, confidence

---

## APPENDIX B: BIBLIOGRAPHY FORMAT (DGWE)

```
Author LastName. *Title of Work*. Publisher, Year, pp. XX–YY.

-- With chapter:
Author LastName. *Title of Work*. Publisher, Year, ch. X, pp. XX–YY.

-- With translator:
Original Author. *Title*. trans. Translator Name. Publisher, Year.

-- Journal article:
Author LastName. "Article Title." *Journal Name*, vol. X, no. Y, Year, pp. XX–YY.

-- Edited volume:
Editor LastName (ed.). *Title of Collection*. Publisher, Year.
```

---

## APPENDIX C: ENTITY SLUG CONVENTIONS

- **Person:** `firstname-lastname` (lowercase, hyphens) — `jabir-ibn-hayyan`, `paracelsus`, `al-razi`
- **Text:** `short-title-slug` (lowercase, hyphens) — `summa-perfectionis`, `emerald-tablet`, `the-book-of-zosimos`
- **Concept:** `term-slug` (lowercase, hyphens) — `distillation`, `transmutation`, `philosophers-stone`
- **Location:** `city-slug` (lowercase, hyphens) — `baghdad`, `florence`, `prague`

---

*For questions about enrichment standards, consult STANDARD_[TYPE].md. For historiographical guidance, see CONCEPTUAL_FRAMEWORK.md.*
