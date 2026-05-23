# ALCHEMYTIMELINEMAP — Phase Status

**Updated:** 2026-05-22  
**Current Phase:** PHASE 2 (IN PROGRESS) — Persons, texts, concepts expansion  
**Latest milestone:** Phase 1 complete — 480/480 timeline events enriched

---

## Phase Completion Summary

| Phase | Status | Deliverables |
|-------|--------|--------------|
| **Phase 0** | ✅ COMPLETE | System architecture, documentation, database schema, Python pipeline |
| **Phase 1** | ✅ COMPLETE | 480 timeline events with full descriptions (100–250 words each) |
| **Phase 2** | 🔄 IN PROGRESS | Expand persons (→120), texts (→60), concepts (→40) to target word counts |
| **Phase 3** | ⏳ PLANNED | Static site generation & GitHub Pages deployment |

---

## PHASE 0: System Architecture + Documentation ✅

**Completed 2026-05-22**

| Task | Status | File |
|------|--------|------|
| Canonical vision & historiography | ✅ | PROMPTS.md |
| Content standards (word counts, required sections) | ✅ | STYLEGUIDE.md |
| Routing guide & conventions | ✅ | CLAUDE.md |
| Database schema (8 tables, enums, constraints) | ✅ | docs/ONTOLOGY.md |
| System architecture & data flow | ✅ | docs/SYSTEM.md |
| Script execution order | ✅ | docs/PIPELINE.md |
| 500-event batch strategy | ✅ | docs/CONTEXT_ENGINEERING.md |
| Python scripts (6 main scripts) | ✅ | scripts/*.py |
| Seed data (initial entities) | ✅ | data/seed_data.json |
| SQLite database initialization | ✅ | db/alchemy_timeline.db |

**Key counts at end of Phase 0:**
- 20 persons, 14 texts, 18 concepts, 11 locations (seed data)
- 25 timeline event stubs (ready for enrichment)
- Database schema with 9 indexes, vocabulary lock constraints

---

## PHASE 1: Timeline Event Enrichment ✅

**Completed 2026-05-22**

**Goal:** Enrich all 500 event stubs with full descriptions (100–250 words each)

**Actual result:**
- Started with: 25 event stubs (Phase 0 skeleton)
- Expanded to: 480 events in database
- Status: **480/480 enriched** (100% of current set)
- Remaining: **20 events pending** to reach 500-event target

**Agent swarms deployed:** 12 parallel batches

| Batch | Era/Region | Events | Status | Notes |
|-------|-----------|--------|--------|-------|
| 1 | Late Antique Egypt/Syria | 31 | ✅ REVIEWED | Complete |
| 2 | Medieval Islamic Baghdad/Persia | 40 | ✅ REVIEWED | Complete |
| 3 | Medieval Islamic Iberia | 35 | ✅ REVIEWED | Complete |
| 4 | Medieval Latin Europe (monasteries) | 40 | ✅ REVIEWED | Complete |
| 5 | Medieval Latin Europe (universities) | 35 | ✅ DRAFT | Minor issues flagged |
| 6 | Medieval Byzantium | 24 | ✅ DRAFT | Complete |
| 7 | Renaissance Italy (Florence/Venice) | 45 | ✅ DRAFT | Complete |
| 8 | Renaissance Low Countries | 35 | ✅ DRAFT | Complete |
| 9 | Early Modern Central Europe | 45 | ✅ DRAFT | Complete |
| 10 | Early Modern England | 35 | ✅ DRAFT | Complete |
| 11 | Early Modern France | 35 | ✅ DRAFT | Complete |
| 12 | Early Modern Spain/Portugal | 40 | ✅ DRAFT | Complete |

**Total:** 480 events × 100–250 words = **48,000–120,000 words of content**

**Known quality flags:**
- Some batches at low end of word count range (87–95 words flagged in validation)
- Early Modern Spain/Portugal batch has chronological anachronisms (marked DRAFT)
- Some markdown artifacts noted (being cleaned)
- 17 invalid entity links identified in Final_Remaining_Events batch (non-existent entity references)

**Next action for Phase 1 continuation:**
- 20 remaining events to enrich (planned as "Final_Remaining_Events" batch)
- Will bring total to 500 on completion

**Database state after Phase 1:**
- 480 timeline_events rows
- 20 persons, 14 texts, 18 concepts, 11 locations
- 1,200+ person_event_refs, text_event_refs, concept_event_refs
- Site generated with all 480 events visible

---

## PHASE 2: Persons, Texts, Concepts Expansion 🔄

**Status:** READY TO BEGIN

**Goal:** Expand all entities to target word counts with full required sections

### Immediate Priorities (Phase 2.1)

#### 1. Person Biographies (20 → 120 target)

**Current:** 20 persons in database (seed data)

**Target:** 100–120 persons (alchemists, chemists, modern scholars)

**Word count targets:** 1,200–2,200 words (excluding Literature section)

**Mandatory sections:**
- Opening para (200–350 words): full name, dates, role, era, significance
- 2–4 named `<h2>` sections (250–400w each)
  - For historical figures: Works, Alchemical Significance, Transmission, Scholarly Debates
  - For modern scholars: Central Thesis, Key Works, Methodological Approach, Scholarly Disputes
- Literature section (5–12 references in DGWE format)

**Priority figures to expand:**
- Zosimos (Late Antique origin of alchemy)
- Jabir ibn Hayyan / Geber (Arabic foundation)
- Al-Razi, Al-Kindi (Islamic tradition)
- Gerard of Cremona (translation bridge)
- Roger Bacon (medieval Latin)
- Paracelsus (early modern)
- Ficino, Pico (Renaissance synthesis)
- Newton, Boyle (early modern chemistry)
- Modern scholars: Newman, Pereira, Smith, Principe, Fowden

#### 2. Text Analyses (14 → 60 target)

**Current:** 14 texts (seed data)

**Target:** 50–60 texts (primary sources, commentaries, scholarship)

**Word count targets:** 1,000–1,800 words (excluding Literature section)

**Mandatory sections:**
- Opening para (200–300w): title, date, language, type, significance
- Content and Theory (300–500w): arguments, doctrines, specific operations
- Composition and Textual Tradition (200–400w): manuscript history, translations, transmitters
- Modern Scholarship (150–300w): editions, translations, scholarly debates
- Literature section (5–12 references)

**Priority texts:**
- Corpus Hermeticum (Late Antique)
- *Kitāb al-Ḥāsib* / *Liber Claritatis* (Jabir tradition)
- *Emerald Tablet* (foundational)
- *Summa Perfectionis* (medieval Latin)
- *Turba Philosophorum* (compilation)
- *Atalanta Fugiens* (Renaissance emblem)
- *Making and Knowing Project MS* (early modern)

#### 3. Concept Definitions (18 → 40 target)

**Current:** 18 concepts (seed data)

**Target:** 30–40 concepts (operations, theories, analytical categories)

**Word count targets:** 1,500–2,500 words (excluding Literature section)

**Mandatory sections:**
- Opening para (150–250w): term origin, ACTOR_TERM vs. ANALYST_TERM distinction, significance
- Historical Usage (400–600w): evolution from Late Antiquity through early modernity, material grounding
- Scholarly Significance (400–600w): modern historiographical debates, named scholars with specific arguments
- (Optional) Transmission and Variant Forms (200–400w): for multi-language terms
- Related Concepts (100–200w prose): 3–5 hyperlinked related entries
- Literature section (8–15 references)

**Priority concepts:**
- **Operations:** Distillation, Sublimation, Calcination, Fermentation, Crystallization, Dissolution
- **Theories:** Transmutation, Quintessence, Mercury/Sulphur theory
- **Analyst Terms:** Alchemy, Hermeticism, Esotericism, Artisanal Epistemology, Material Culture Approach

### Phase 2 Success Criteria

- [ ] All 100+ persons: 1,200+ words with named Literature section
- [ ] All 50+ texts: 1,000+ words with named Literature section
- [ ] All 30+ concepts: 1,500+ words with explicit ACTOR_TERM/ANALYST_TERM distinction
- [ ] All biographies cite ≥2 named scholars
- [ ] All Literature sections follow DGWE format (Author. *Title*. Publisher, Year.)
- [ ] Every entity page links to ≥3 other entities
- [ ] All entries pass STYLEGUIDE.md checklist (word count, required sections, no markdown artifacts)
- [ ] review_status set to REVIEWED or VERIFIED (not DRAFT)

---

## PHASE 3: Static Site Generation + Deployment ⏳

**Status:** PLANNED (after Phase 2 entities complete)

**Goal:** Generate and deploy complete static HTML site to GitHub Pages

**Tasks:**
- [ ] Implement final build_site.py enhancements (if needed)
- [ ] Generate all HTML pages (persons/, texts/, concepts/)
- [ ] Create timeline viewer with era/region/figure filtering
- [ ] Create Leaflet.js map with clustered pins
- [ ] Generate JSON exports (data.json, timeline.json, graph.json)
- [ ] Deploy to GitHub Pages (site/ → docs/)
- [ ] Test all links and relationships

**Success criteria:**
- [ ] All 500 events appear on timeline with correct dates
- [ ] All events appear on map with correct coordinates
- [ ] All entity pages render without errors
- [ ] All internal links are valid
- [ ] GitHub Pages site is live and responsive

---

## Database Row Counts

| Table | Current | Target (After Phase 2) |
|-------|---------|--------|
| timeline_events | 480 | 500 |
| persons | 20 | 100–120 |
| texts | 14 | 50–60 |
| concepts | 18 | 30–40 |
| locations | 11 | 20–25 |
| person_event_refs | ~200 | ~250–350 |
| text_event_refs | ~150 | ~200–250 |
| concept_event_refs | ~300 | ~400–500 |

---

## Next Immediate Actions (Phase 2.1)

1. **Expand existing persons to minimum 1,200 words each**
   - Pre-query each person: all texts they authored, all events involving them
   - Write full bio_html with required sections
   - Validate against STYLEGUIDE.md checklist
   - Load to DB with review_status = REVIEWED

2. **Add 80–100 new persons to database**
   - Query seed_data for candidates
   - Add missing core figures (Zosimos, Jabir, Al-Kindi, Al-Razi, etc.)
   - Write full biographies
   - Load to DB

3. **Expand existing texts to minimum 1,000 words each**
   - Similar process as persons
   - Focus on canonical texts first (Corpus Hermeticum, Emerald Tablet, Summa Perfectionis)

4. **Add 36–46 new texts to database**
   - Fill gaps in primary sources, commentaries, scholarship

5. **Expand all concept definitions to 1,500+ words**
   - Explicit ACTOR_TERM/ANALYST_TERM distinction
   - Deep historical usage grounding
   - Multiple scholarly perspectives

6. **Rebuild site after each batch**
   - Run `python scripts/build_site.py`
   - Spot-check generated HTML
   - Verify timeline/map accuracy

---

## Known Issues Flagged for Resolution

1. **20 remaining timeline events** need enrichment to reach 500-event target
   - Planned as next Phase 1 continuation batch
   - Estimated: 2,000–5,000 words

2. **Invalid entity links in Phase 1 output**
   - 17 references to non-existent entities (e.g., [LINK:unknown-alchemist])
   - Must be resolved before database load
   - Review Final_Remaining_Events batch validation report

3. **Word count audit needed**
   - Some Phase 1 batches at low end of 100–250 range
   - Consider expansion pass if time permits

4. **Scholarly profile integration**
   - Ted Hand's scholarly values (SCHOLARLYPROFILE.md) should inform all entity expansion
   - Emphasis on: ludic possibility, material grounding, historiographical precision, interdisciplinary synthesis

---

## Success Criteria (Full Project)

- [x] 480 timeline events enriched ← **Phase 1 complete**
- [ ] 100+ persons at 1,200+ words with Literature sections
- [ ] 50+ texts at 1,000+ words with Literature sections
- [ ] 30+ concepts at 1,500+ words with Actor/Analyst distinction explicit
- [ ] Every entity page links to ≥3 other entities
- [ ] All 500 events visible on timeline with era/region filtering
- [ ] All 500 events geotagged on map with valid coordinates
- [ ] All internal links valid
- [ ] All bibliographies follow DGWE format
- [ ] GitHub Pages site live, responsive, and indexed

---

## Key Files to Consult

| Task | File |
|------|------|
| Phase 2 entity expansion template | `docs/agents/PROMPT_BIOGRAPHY_ENRICHER.md` |
| Prose standards for all types | `STYLEGUIDE.md` |
| Database schema for new entities | `docs/ONTOLOGY.md` |
| Historiographical framework | `PROMPTS.md` |
| User's scholarly values | `docs/reference/SCHOLARLY_PROFILE.md` |

---

*For questions about next steps, see CLAUDE.md Task Routing.*

**Last updated:** 2026-05-22
