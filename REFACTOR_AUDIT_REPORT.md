# ALCHEMYTIMELINEMAP Documentation Refactor — Audit Report

**Date:** 2026-05-22  
**Task:** Streamline system files for context efficiency while preserving scholarly authority

---

## Executive Summary

The ALCHEMYTIMELINEMAP project has grown to **27 top-level and docs/ markdown files** with significant duplication across three layers:

1. **Canonical documents** (PROMPTS.md, STYLEGUIDE.md) are being re-stated in routing/entry documents (CLAUDE.md, README.md)
2. **Phase status contradictions** exist between CLAUDE.md (Phase 0), PHASESTATUS.md (Phase 2 ready), and README.md (Phase 0)
3. **Session/project summaries** (PROJECT_SUMMARY.md, SESSION_SUMMARY.md) duplicate each other and PHASESTATUS.md
4. **Agent prompts** (7 files) likely contain overlapping onboarding content instead of task-specific routing
5. **Historiographical profiles** (SCHOLARLYPROFILE.md, SONNETSCHOLARLYPROFILE.md) are not referenced in the boot sequence

**Cost:** New sessions must read 5–8 files (15,000+ words) to understand the project. Context overhead is unsustainable at scale.

---

## File Inventory & Analysis

### Current Boot-Layer Files (Always Loaded)

| File | Size | Redundancy | Issues |
|------|------|-----------|--------|
| CLAUDE.md | 2,600w | HIGH | Contains full PROMPTS content (vision, historiography, authorities, vocabulary lock), full STYLEGUIDE summary, full PIPELINE, full ONTOLOGY, full SYSTEM. Duplicates README and PROMPTS wholesale. |
| README.md | 500w | HIGH | Duplicates PROMPTS (vision, historiography, authorities), STYLEGUIDE (content model), CLAUDE (quick start routing), PROJECT_SUMMARY (status). Points to 8 different files. |
| PROMPTS.md | 4,000+w | BASELINE | Canonical vision — should be read once, not summarized in CLAUDE/README |

**Assessment:** Boot layer is 3–4x larger than necessary. Every new Claude session must parse all three files + decide what to read next. **Trim to <1,200 words for CLAUDE.md.**

---

### Historiographical/Profile Files

| File | Purpose | Status | Recommendations |
|------|---------|--------|------------------|
| SCHOLARLYPROFILE.md | Ted Hand's scholarly values, methods, authorities | COMPLETE | Move to `docs/reference/SCHOLARLY_PROFILE.md`. Not needed for agent boot. Read only when understanding user intent. |
| SONNETSCHOLARLYPROFILE.md | Similar (generated for Sonnet model) | COMPLETE | Archive in `docs/archive/` or delete. Superseded by SCHOLARLYPROFILE.md. |

---

### Standards & Style Files

| File | Purpose | Completeness | Deduplication Status |
|------|---------|--------------|---------------------|
| STYLEGUIDE.md | Comprehensive prose standards (word counts, required sections, bibliography, Actor/Analyst) | 100% COMPLETE | **KEEP as canonical.** Consolidate STYLE_GUIDE_ALCHEMISTS.md and STYLE_GUIDE_SCHOLARS_AND_TEXTS.md into STYLEGUIDE.md if they add value, else archive. |
| STYLE_GUIDE_ALCHEMISTS.md | (not yet read) | ? | Likely predecessor. Check if it contains unique content or is subsumed by STYLEGUIDE.md. |
| STYLE_GUIDE_SCHOLARS_AND_TEXTS.md | (not yet read) | ? | Likely predecessor. Check if it contains unique content or is subsumed by STYLEGUIDE.md. |

**Recommendation:** Read both and consolidate into single STYLEGUIDE.md with clear section headers. Archive originals.

---

### Architecture & Technical Documentation

| File | Purpose | Status | Deduplication |
|------|---------|--------|----------------|
| docs/SYSTEM.md | Tech stack, data flow diagram, design principles | COMPLETE | Referenced in CLAUDE.md and README.md but not duplicated in content. **KEEP.** Remove from boot layer. Task-specific. |
| docs/ONTOLOGY.md | Database schema (8 tables, enums, constraints) | COMPLETE | Referenced but not duplicated. **KEEP.** Remove from boot. Task-specific. |
| docs/PIPELINE.md | Script execution order (6 phases) | COMPLETE | Duplicated in CLAUDE.md (§Pipeline Rules). **Move to Tier 2** (read before running scripts). |
| docs/CONTEXT_ENGINEERING.md | Batch strategy for 500-event scale | COMPLETE | Referenced but not duplicated. **KEEP.** Task-specific for Phase 1 (event enrichment). |

**Recommendation:** None of these belong in boot layer. SYSTEM.md, ONTOLOGY.md, PIPELINE.md should be read only when executing their specific tasks.

---

### Phase Tracking & Status Files

| File | Content | Issues | Recommendation |
|------|---------|--------|-----------------|
| PHASESTATUS.md | Current phase, completed tasks, next steps, success criteria | PRIMARY SOURCE | **PROMOTE to canonical status.** Currently says Phase 1 complete, Phase 2 ready. But CLAUDE.md says Phase 0. Resolve contradiction. Make this the single source of truth for project state. |
| PROJECT_SUMMARY.md | Reiterates what has been created (system files, scripts, database) | DUPLICATE | Summarizes what PHASESTATUS already tracks. **Archive in docs/archive/.** Links to it from PHASESTATUS if needed. |
| SESSION_SUMMARY.md | Completed work, current state, database row counts | DUPLICATE | Nearly identical to PROJECT_SUMMARY. **Delete or archive both.** Use PHASESTATUS.md only. |

**Contradiction to resolve:** CLAUDE.md says "PHASE 0: SYSTEM ARCHITECTURE + SEED DATA" but PHASESTATUS.md clearly shows:
- Phase 0 ✅ COMPLETE
- Phase 1 ✅ COMPLETE (480/480 events enriched)
- Phase 2 🔄 READY (Persons, texts, concepts expansion)

**Action:** Update CLAUDE.md to point to PHASESTATUS.md for current phase. Accept PHASESTATUS as source of truth.

---

### Agent Prompt Files

| File | Purpose | Likely Content |
|------|---------|-----------------|
| AGENT_PROMPT_EVENT_ENRICHER.md | Task prompt for enriching timeline events | Probably contains: task description, historiographical principles, style rules, vocabulary lock, example |
| AGENT_PROMPT_BIOGRAPHY_ENRICHER.md | Task prompt for expanding person biographies | Similar full onboarding |
| AGENT_PROMPT_TEXT_ENRICHER.md | Task prompt for expanding text analyses | Similar full onboarding |
| AGENT_PROMPT_ARCHIVE_ENTITY_EXTRACTOR.md | Task prompt for extracting entities from archive sources | Similar full onboarding |
| AGENT_PROMPT_COMPLETE_PERSON_BIOGRAPHIES.md | Task prompt for complete person biographies | Similar |
| AGENT_PROMPT_COMPLETE_TEXT_ANALYSES.md | Task prompt for complete text analyses | Similar |
| AGENT_PROMPT_COMPLETE_CONCEPT_DEFINITIONS.md | Task prompt for complete concept definitions | Similar |

**Assessment:** These likely contain 80% identical preamble (historiography, actor/analyst, style rules) + 20% task-specific content.

**Recommendation:** Refactor to:
1. Create `docs/agents/TASK_ROUTING.md` that maps tasks to their prompts and prerequisite reads
2. Each agent prompt should be <500 words and contain:
   - Task summary (1 para)
   - Prerequisites to read: "Read STYLEGUIDE.md § [section], PROMPTS.md § [section], PHASESTATUS.md"
   - Task-specific constraints
   - Example input/output
   - Link to Tier 1 & 2 docs

---

### Content Integration & Archaeology Files

| File | Purpose | Status | Recommendation |
|------|---------|--------|-----------------|
| docs/ARCHAEOLOGY_AND_MATERIAL_CULTURE.md | Material evidence research, Hessian crucibles, Tycho Brahe, Making and Knowing | COMPLETE | Task-specific for Phase 2 entity enrichment. Move to `docs/reference/` or archive. Not needed for boot. |
| ARCHAEOLOGY_RESEARCH_SUMMARY.md | Complete research synthesis | COMPLETE | Archive. Useful for future enrichment but not boot. |
| INTEGRATION_GUIDE_ARCHAEOLOGY.md | How to incorporate archaeology into timeline/entities | COMPLETE | Archive. Needed only for Phase 2. Reference from task prompt. |
| CONTENT_EXPANSION_SUMMARY.md | Content expansion work | COMPLETE | Archive. Session note, not canonical. |

**Recommendation:** Move to `docs/reference/` or `docs/archive/` depending on whether it's active research.

---

### Miscellaneous

| File | Purpose | Recommendation |
|------|---------|-----------------|
| docs/MULTIREGISTER_EXAMPLES.md | Examples of actor/analyst distinction | Move to `docs/reference/examples/` or include as appendix in STYLEGUIDE.md. |

---

## Contradiction Resolution

### 1. Current Phase (CRITICAL)

**Contradiction:**
- CLAUDE.md: "PHASE 0: SYSTEM ARCHITECTURE + SEED DATA"
- PHASESTATUS.md: "Phase 1 Complete — All 480/480 events enriched. Current Phase: PHASE 2 (READY)"
- README.md: "Phase 0 (System Architecture + Documentation)"

**Evidence:** PHASESTATUS.md is correct. Phase 0 is complete. Phase 1 (event enrichment) produced 480 enriched events. Phase 2 (persons/texts/concepts expansion) is ready to begin.

**Action:** Update CLAUDE.md to point to PHASESTATUS.md as the source of truth. Remove Phase description from CLAUDE.md.

---

### 2. Event Count

**Contradiction:**
- "500-event target" vs. "480/480 events enriched"

**Evidence:** Timeline skeleton started at 25, expanded to 480 during Phase 1. Target is 500 but not yet reached. Additional 20 events to be added in continuation.

**Action:** PHASESTATUS.md should clarify: "Phase 1 complete at 480 events. 20 remaining events (planned for Phase 1 continuation) pending enrichment. 500-event target on track."

---

## Proposed New File Hierarchy

```
ALCHEMYTIMELINEMAP/
├── CLAUDE.md (NEW — <1,200 words, boot only)
│   ├─ Mission & core invariants
│   ├─ Current phase pointer (→ PHASESTATUS.md)
│   ├─ Task routing (3 rows)
│   └─ "Read next" instruction set
│
├── PHASESTATUS.md (PROMOTED to canonical)
│   ├─ Current phase & completion status
│   ├─ Completed tasks (all phases)
│   ├─ Next immediate steps
│   └─ Success criteria
│
├── PROMPTS.md (TIER 2 — read before new agent tasks)
│   ├─ Canonical vision
│   ├─ Three constituencies
│   ├─ Historiographical framework
│   ├─ Content standards
│   ├─ Key authorities
│   └─ Vocabulary lock
│
├── STYLEGUIDE.md (TIER 2 — read before writing prose)
│   ├─ Core prose standards
│   ├─ Timeline events
│   ├─ Person biographies
│   ├─ Text descriptions
│   ├─ Concept definitions
│   ├─ Bibliography format
│   ├─ Actor/Analyst examples
│   └─ Comprehensive checklist
│
├── README.md (UPDATED — quick start only, <400 words)
│   ├─ Project summary
│   └─ Links to CLAUDE.md, PHASESTATUS.md, PROMPTS.md, STYLEGUIDE.md
│
├── docs/
│   ├─ SYSTEM.md (Architecture — read before modifying pipeline)
│   ├─ ONTOLOGY.md (Schema — read before adding/changing tables)
│   ├─ PIPELINE.md (Script order — read before running deploy)
│   ├─ CONTEXT_ENGINEERING.md (Batch strategy — read before Phase 1)
│   │
│   ├─ agents/
│   │   ├─ TASK_ROUTING.md (Maps tasks → prompts → prerequisites)
│   │   ├─ PROMPT_EVENT_ENRICHER.md (NEW — <500 words, task-specific)
│   │   ├─ PROMPT_BIOGRAPHY_ENRICHER.md
│   │   ├─ PROMPT_TEXT_ENRICHER.md
│   │   ├─ PROMPT_CONCEPT_ENRICHER.md (NEW or rename)
│   │   └─ PROMPT_ARCHIVE_EXTRACTOR.md
│   │
│   ├─ reference/
│   │   ├─ SCHOLARLY_PROFILE.md (Ted Hand's values — context, not boot)
│   │   ├─ ARCHAEOLOGY_AND_MATERIAL_CULTURE.md (Research — reference only)
│   │   ├─ ARCHAEOLOGY_RESEARCH_SUMMARY.md
│   │   ├─ examples/
│   │   │   └─ MULTIREGISTER_EXAMPLES.md (Actor/analyst distinction)
│   │   └─ INTEGRATION_GUIDE_ARCHAEOLOGY.md
│   │
│   └─ archive/
│       ├─ SONNETSCHOLARLYPROFILE.md (Superseded)
│       ├─ PROJECT_SUMMARY.md (Superseded by PHASESTATUS)
│       ├─ SESSION_SUMMARY.md (Session notes, not canonical)
│       ├─ STYLE_GUIDE_ALCHEMISTS.md (Consolidated into STYLEGUIDE.md)
│       └─ STYLE_GUIDE_SCHOLARS_AND_TEXTS.md (Consolidated into STYLEGUIDE.md)
│
└── scripts/ (no changes)
```

---

## Deduplication Summary

| Content | Currently Appears In | After Refactor |
|---------|---------------------|-----------------|
| **Canonical vision** | PROMPTS.md, CLAUDE.md (§ Project Mission), README.md | PROMPTS.md only |
| **Historiographical framework** | PROMPTS.md, CLAUDE.md (implied), README.md (§ Historiographical Framework) | PROMPTS.md only |
| **Content standards (word counts, sections)** | STYLEGUIDE.md (full), PROMPTS.md (§ Part IV), CLAUDE.md (§ Data Ontology), README.md (§ Content Model) | STYLEGUIDE.md only |
| **Key authorities** | PROMPTS.md (§ Part VI), CLAUDE.md (§ Key Scholarly Authorities), README.md (§ Key Authorities), SCHOLARLYPROFILE.md | PROMPTS.md only; SCHOLARLYPROFILE.md in reference/ for user context |
| **Vocabulary lock (enums)** | PROMPTS.md (§ Part VII), CLAUDE.md (§ Vocabulary Lock), docs/ONTOLOGY.md (CHECK constraints) | docs/ONTOLOGY.md (schema source); STYLEGUIDE.md (enforcement rule) |
| **Architecture diagram** | docs/SYSTEM.md, CLAUDE.md (§ Architecture at a Glance) | docs/SYSTEM.md only |
| **Data flow pipeline** | docs/PIPELINE.md, CLAUDE.md (§ Data Flow & Pipeline Rules), docs/SYSTEM.md (§ Data Flow Diagram) | docs/PIPELINE.md only |
| **Phase status** | PHASESTATUS.md, PROJECT_SUMMARY.md, SESSION_SUMMARY.md, CLAUDE.md (§ Current Phase) | PHASESTATUS.md only |

---

## Context Reduction (Quantified)

### Current State
- **Boot load:** CLAUDE.md + README.md + PROMPTS.md = ~7,100 words
- **Typical agent task:** Reads boot + STYLEGUIDE.md + task prompt = ~9,100 words (25% of context)

### After Refactor
- **Boot load:** New CLAUDE.md (<1,200 words) = MINIMAL
- **Typical agent task:** 
  - Reads new CLAUDE.md (<1,200w) 
  - Follows link to PROMPTS.md (4,000w) [only if new content domain]
  - Reads STYLEGUIDE.md (2,000w) [before writing]
  - Task prompt (300–500w) [role-specific]
  - **Total: 1,200 + 2,000 + 400 = 3,600w** (vs. 9,100w currently)
  - **Savings: 60% context reduction**

---

## Remaining Open Questions

1. **STYLE_GUIDE_ALCHEMISTS.md & STYLE_GUIDE_SCHOLARS_AND_TEXTS.md:** Have these been read yet? Do they contain unique content not in STYLEGUIDE.md? (Need to read both before consolidation decision.)

2. **INTEGRATION_GUIDE_ARCHAEOLOGY.md:** Is this still actively used in Phase 2? Or superseded by PHASESTATUS.md Phase 2 instructions?

3. **Incomplete agent prompts:** Do the 7 AGENT_PROMPT_*.md files currently exist and contain working content, or are they templates to be filled?

4. **SONNETSCHOLARLYPROFILE.md:** Can this be safely deleted, or does it serve a different model/version?

5. **Event count accuracy:** Confirm: 480 events currently enriched, 20 more planned to reach 500, not 440 + 60?

---

## Implementation Plan

### Phase 1: Audit & Consolidation (30 mins)
1. Read STYLE_GUIDE_ALCHEMISTS.md and STYLE_GUIDE_SCHOLARS_AND_TEXTS.md
2. Consolidate unique content into STYLEGUIDE.md (if any)
3. Answer open questions above

### Phase 2: File Restructuring (45 mins)
1. Create `docs/agents/` directory
2. Create `docs/reference/` and `docs/archive/` directories
3. Move/copy files according to new hierarchy
4. Archive obsolete files with explanatory notes

### Phase 3: Rewrite Boot Layer (60 mins)
1. Rewrite CLAUDE.md (<1,200 words)
2. Rewrite README.md (<400 words, quick-start only)
3. Update PHASESTATUS.md to clarify phase status and event count
4. Ensure links from new CLAUDE.md are accurate

### Phase 4: Agent Prompt Refactor (90 mins)
1. Create `docs/agents/TASK_ROUTING.md` with matrix
2. Refactor existing agent prompts to <500 words each (or create new ones)
3. Each prompt states: "Read STYLEGUIDE.md § X, PROMPTS.md § Y, then complete task Z"

### Phase 5: Verification (30 mins)
1. New Claude session: Start with new CLAUDE.md
2. Follow links sequentially; verify all files accessible
3. Check that agent prompts link correctly
4. Generate CHANGELOG entry

---

## Success Criteria

- [x] All 27 files inventoried and categorized
- [x] Duplications identified and mapped
- [x] Phase contradiction flagged
- [ ] STYLE_GUIDE files reviewed (pending)
- [ ] New file hierarchy diagram created
- [ ] CLAUDE.md rewritten to <1,200 words
- [ ] README.md rewritten to <400 words
- [ ] PHASESTATUS.md clarified
- [ ] Agent prompts refactored to <500 words each
- [ ] CHANGELOG entry written
- [ ] New session verification test passed

---

## Approval Checkpoints

**Before Phase 2 (Restructuring):**
- [ ] User confirms contradiction resolution (current phase is Phase 2, not Phase 0)
- [ ] User confirms event count (480 current, 20 pending for 500 target)
- [ ] User confirms STYLE_GUIDE consolidation strategy

**Before Phase 4 (Agent Prompts):**
- [ ] User confirms agent prompt refactoring approach
- [ ] User clarifies which agent prompts are actively used

---

*End of Audit Report*
