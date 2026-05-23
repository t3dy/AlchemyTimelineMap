# ALCHEMYTIMELINEMAP Documentation Refactor — Implementation Summary

**Date:** 2026-05-22  
**User:** t3dy  
**Task:** Streamline system files for context efficiency and reduced instruction drift

---

## What Was Done

A comprehensive audit of all 27 project documentation files identified:
- **3–4x duplication** of historiographical principles, content standards, and architectural explanations
- **Phase confusion**: CLAUDE.md says Phase 0, but project is actually at Phase 2 (persons/texts/concepts expansion)
- **Context overhead**: New Claude sessions must parse 7,100+ words to understand the project
- **Agent prompt proliferation**: 7 separate agent prompts likely contain 80% identical preamble

---

## Proposed Changes (Deliverables)

### 1. **REFACTOR_AUDIT_REPORT.md** ✅ Created
Complete inventory of all 27 files, duplication analysis, contradiction resolution, and detailed implementation plan.

**Key findings:**
- Boot layer is 3–4x oversized
- PROMPTS.md, STYLEGUIDE.md, CLAUDE.md, README.md each contain overlapping historiographical framework
- PHASESTATUS.md contradicts CLAUDE.md on current phase
- Agent prompts should be <500 words, not full onboarding documents

---

### 2. **CLAUDE_REFACTORED.md** ✅ Created
New boot-layer document: **<1,200 words** (vs. current 2,600 words)

**Content:**
- Mission & core invariants (5 bullets, non-negotiable)
- Current phase pointer (→ PHASESTATUS.md)
- Task routing (8 rows: task → file → action)
- Core architecture (30-second diagram)
- Schema summary (8 tables)
- Vocabulary lock (enum values)
- Scholarly authorities (7 key scholars)
- Checking your work (validation checklist)

**Impact:**
- **Context reduction:** 60% (1,200w boot vs. 2,600w current)
- Agents get orientation in 3 min, then follow task-specific links
- No duplication of historiography or style rules

---

### 3. **README_REFACTORED.md** ✅ Created
Streamlined quick-start: **<400 words** (vs. current 500+ words + repetition)

**Content:**
- Mission (1 sentence)
- Quick start (5 numbered steps with links)
- Project structure (diagram)
- Tech stack (one paragraph)
- Core principles (4 bullets)
- Current status
- Key authorities
- Next steps link

**Impact:**
- Clear navigation for newcomers
- Links to CLAUDE.md, PHASESTATUS.md, PROMPTS.md, STYLEGUIDE.md
- No duplication of full content

---

### 4. **PHASESTATUS_REFACTORED.md** ✅ Created
Elevated to canonical status: **Clear, accurate phase tracking**

**Key updates:**
- **Corrects phase confusion:** Phase 2 (IN PROGRESS) not Phase 0
- **Event count clarity:** 480/480 enriched in Phase 1, 20 pending to reach 500
- **Phase 2 scope detailed:** Expand persons (20→120), texts (14→60), concepts (18→40)
- **Success criteria** for Phase 2 completion
- **Immediate next actions** for Phase 2.1
- **Known issues** to resolve (invalid entity links, word count audit)

**Impact:**
- Single source of truth for project state
- Resolves contradictions between CLAUDE.md, README.md, PROJECT_SUMMARY.md, SESSION_SUMMARY.md
- Task planning becomes straightforward

---

### 5. **STYLEGUIDE_CONSOLIDATION_PLAN.md** ✅ Created
Strategy for merging 3 overlapping style guides into 1 comprehensive guide

**Current state:**
- STYLEGUIDE.md (core)
- STYLE_GUIDE_ALCHEMISTS.md (person detail)
- STYLE_GUIDE_SCHOLARS_AND_TEXTS.md (scholar + text detail)

**Proposed consolidation (Option A—Recommended):**
- Merge all into expanded STYLEGUIDE.md (~3,500–4,000 words)
- Add subsections for historical alchemists vs. modern scholars
- Add subsections for primary sources vs. commentary vs. scholarship
- Move detailed examples to docs/reference/examples/
- Archive original files with explanatory notes

**Benefit:** Single authoritative source; no contradiction risk; cleaner agent orientation.

---

### 6. **REFACTOR_AUDIT_REPORT.md** ✅ Created (as above)

---

## Proposed New File Hierarchy

```
ALCHEMYTIMELINEMAP/
├── CLAUDE.md [NEW]           (boot: <1,200 words)
├── README.md [UPDATED]       (quick start: <400 words)
├── PHASESTATUS.md [UPDATED]  (source of truth: current phase, what's next)
├── PROMPTS.md [EXISTING]     (canonical vision: historiography, content standards)
├── STYLEGUIDE.md [UPDATED]   (consolidated prose standards for all content types)
│
├── docs/
│   ├── SYSTEM.md             (architecture: read before modifying pipeline)
│   ├── ONTOLOGY.md           (schema: read before adding/changing tables)
│   ├── PIPELINE.md           (script order: read before running deploy)
│   ├── CONTEXT_ENGINEERING.md (batch strategy: read before Phase 1 enrichment)
│   │
│   ├── agents/
│   │   ├── TASK_ROUTING.md   [NEW] (maps tasks → prompts → prerequisites)
│   │   ├── PROMPT_EVENT_ENRICHER.md      [NEW] (<500 words, task-specific)
│   │   ├── PROMPT_BIOGRAPHY_ENRICHER.md  [NEW]
│   │   ├── PROMPT_TEXT_ENRICHER.md       [NEW]
│   │   └── PROMPT_CONCEPT_ENRICHER.md    [NEW]
│   │
│   ├── reference/            [NEW DIRECTORY]
│   │   ├── SCHOLARLY_PROFILE.md (Ted Hand's values: context only)
│   │   ├── ARCHAEOLOGY_AND_MATERIAL_CULTURE.md
│   │   ├── ARCHAEOLOGY_RESEARCH_SUMMARY.md
│   │   ├── INTEGRATION_GUIDE_ARCHAEOLOGY.md
│   │   └── examples/         [NEW SUBDIRECTORY]
│   │       └── WILLIAM_NEWMAN_EXAMPLE.md (full person biography example)
│   │
│   └── archive/              [NEW DIRECTORY]
│       ├── SONNETSCHOLARLYPROFILE.md (superseded)
│       ├── PROJECT_SUMMARY.md (superseded by PHASESTATUS)
│       ├── SESSION_SUMMARY.md (session notes, not canonical)
│       ├── STYLE_GUIDE_ALCHEMISTS.md (consolidated into STYLEGUIDE.md)
│       └── STYLE_GUIDE_SCHOLARS_AND_TEXTS.md (consolidated)
│
└── [other existing files unchanged]
```

---

## Context Reduction (Quantified)

### Current State
- **Boot load:** CLAUDE.md + README.md + PROMPTS.md = ~7,100 words
- **Typical agent task read:** boot + STYLEGUIDE.md + task prompt = ~9,100 words
- **Percentage of context:** ~25% of a typical session

### After Refactor
- **Boot load:** New CLAUDE.md alone = <1,200 words
- **Typical agent task read:**
  - CLAUDE.md (<1,200w) [boot]
  - STYLEGUIDE.md (2,000w) [before writing prose]
  - Task prompt (300–500w) [role-specific]
  - Subtotal: **3,500 words** (vs. 9,100 current)
- **Savings: 62% reduction in mandatory reading**
- **Optional reads** (PROMPTS.md, PHASESTATUS.md) consulted as needed, not pre-loaded

---

## Implementation Plan (4 Phases)

### Phase A: Decision & Approval (30 min)
1. User reviews:
   - REFACTOR_AUDIT_REPORT.md (understand the problem)
   - This REFACTOR_SUMMARY.md (understand the solution)
   - STYLEGUIDE_CONSOLIDATION_PLAN.md (decide on guide consolidation)
2. User confirms or adjusts proposed approach
3. **Open questions from audit:**
   - ✅ Phase contradiction: Is Phase 2 the current correct status?
   - ✅ Event count: Is 480 current, 20 pending for 500 target?
   - ⏳ Style guide consolidation: Approve Option A (merge all into STYLEGUIDE.md)?
   - ⏳ Agent prompts: Which 7 prompts are actively used vs. templates?

### Phase B: File Restructuring (60 min)
1. Create `docs/agents/`, `docs/reference/`, `docs/archive/` directories
2. Copy/move files:
   - CLAUDE_REFACTORED.md → CLAUDE.md (replace original)
   - README_REFACTORED.md → README.md (replace original)
   - PHASESTATUS_REFACTORED.md → PHASESTATUS.md (replace original)
   - SCHOLARLYPROFILE.md → docs/reference/
   - ARCHAEOLOGY_*.md → docs/reference/
   - STYLE_GUIDE_*.md → docs/archive/
   - SONNETSCHOLARLYPROFILE.md → docs/archive/
   - PROJECT_SUMMARY.md, SESSION_SUMMARY.md → docs/archive/
3. Archive this audit report and consolidation plan in docs/archive/

### Phase C: STYLEGUIDE Consolidation (90 min)
1. Expand STYLEGUIDE.md with subsections for person & text types
2. Integrate unique content from STYLE_GUIDE_ALCHEMISTS.md and STYLE_GUIDE_SCHOLARS_AND_TEXTS.md
3. Move example entries to docs/reference/examples/
4. Test with sample agent prompt

### Phase D: Agent Prompt Refactoring (90 min)
1. Create `docs/agents/TASK_ROUTING.md` with task matrix
2. Refactor existing 7 agent prompts to <500 words each
3. Each prompt states: "Read STYLEGUIDE.md § X, PROMPTS.md § Y, then complete task Z"
4. Test with Phase 2 enrichment task

### Phase E: Verification & Finalization (30 min)
1. New Claude session test: Start with new CLAUDE.md, follow links, verify all accessible
2. Generate CHANGELOG entry (see below)
3. Create backup branch or note changeset
4. Commit with message referencing this audit

**Total time: ~4–5 hours**

---

## CHANGELOG Entry (Proposed)

```markdown
## [2026-05-22] Documentation Refactor — Streamline Boot Layer

**Major change:** Restructured all system documentation into three-tier hierarchy 
to reduce context overhead and eliminate duplication.

**Boot layer reduction:** 7,100 words → <1,200 words (62% context savings)

### Changed Files
- CLAUDE.md: Rewritten as <1,200-word boot-only guide (from 2,600 words)
  - Removes full PROMPTS/STYLEGUIDE/PIPELINE summaries
  - Adds task routing table linking to specific files
  - Corrects phase status (Phase 2, not Phase 0)
  
- README.md: Streamlined to <400-word quick start (from 500+ words with duplication)
  - Clear navigation to CLAUDE.md, PHASESTATUS.md, PROMPTS.md, STYLEGUIDE.md
  - Removes duplicated content from other files
  
- PHASESTATUS.md: Elevated to canonical source of truth
  - Clarifies current phase (Phase 2 IN PROGRESS, not Phase 0)
  - Details Phase 2 scope: persons (20→120), texts (14→60), concepts (18→40)
  - Resolves event count contradiction (480 current, 20 pending for 500)
  - Lists immediate Phase 2.1 actions

### New Files
- REFACTOR_AUDIT_REPORT.md: Complete inventory of 27 files, duplication analysis, 
  contradictions, and implementation plan
- STYLEGUIDE_CONSOLIDATION_PLAN.md: Strategy for merging 3 style guides into 1
- REFACTOR_SUMMARY.md: This summary of changes and implementation

### Reorganized Files
- docs/reference/: Ted Hand's scholarly profile, archaeology research
- docs/archive/: Superseded guides (STYLE_GUIDE_ALCHEMISTS.md, SESSION_SUMMARY.md, etc.)
- docs/agents/: (Placeholder for refactored task-specific prompts)

### Deduplication Summary
- Historiographical framework: Now in PROMPTS.md only (not repeated in CLAUDE.md, README.md)
- Content standards: Now in STYLEGUIDE.md only (consolidated from 3 guides)
- Phase status: Now in PHASESTATUS.md only (source of truth)
- Architecture: Now in docs/SYSTEM.md only (not duplicated in CLAUDE.md)

### Benefits
- **62% context reduction** in typical agent task startup (9,100 words → 3,500 words)
- **Single source of truth** for each concept (no contradiction risk)
- **Task-specific reading**: Agents follow links based on their task, not pre-loaded with everything
- **Clearer phase tracking**: PHASESTATUS.md is now canonical

### Testing
- Verify CLAUDE.md → PHASESTATUS.md links work
- Verify CLAUDE.md → STYLEGUIDE.md task routing is accurate
- Verify docs/ directory structure
- Test with Phase 2 agent prompt (biography enrichment)

### Next Steps
- (Phase B-E above) Implement directory restructuring and guide consolidation
- Update agent prompts to reference consolidated STYLEGUIDE.md
- Archive old files with explanatory notes
```

---

## Open Approval Checkpoints

Before implementing Phase B onwards:

- [ ] **Confirm phase status:** Is Phase 2 (PERSONS/TEXTS/CONCEPTS EXPANSION) current?
- [ ] **Confirm event count:** 480 enriched in Phase 1, 20 more needed to reach 500 target?
- [ ] **Approve style guide consolidation:** Merge STYLE_GUIDE_ALCHEMISTS + SCHOLARS_AND_TEXTS into STYLEGUIDE.md (Option A)?
- [ ] **Clarify agent prompts:** Which 7 agent prompt files are actively used? (Helps Phase D planning)
- [ ] **Approve new file hierarchy:** Accept proposed docs/agents/, docs/reference/, docs/archive/ structure?

---

## Files Ready for Review

✅ **REFACTOR_AUDIT_REPORT.md** — Complete inventory and analysis  
✅ **CLAUDE_REFACTORED.md** — New boot file (ready to replace CLAUDE.md)  
✅ **README_REFACTORED.md** — New quick-start (ready to replace README.md)  
✅ **PHASESTATUS_REFACTORED.md** — Corrected phase status (ready to replace PHASESTATUS.md)  
✅ **STYLEGUIDE_CONSOLIDATION_PLAN.md** — Consolidation strategy (ready for approval)  
✅ **REFACTOR_SUMMARY.md** — This document

---

## Next Steps for User

1. **Review** the audit report and this summary
2. **Answer** the 5 open approval checkpoints above
3. **Decide** on timing (implement now, or defer to later session?)
4. **Approve** the implementation plan (Phases A–E)
5. **Initiate** Phase B (file restructuring) or ask for adjustments

**Estimated total refactor time: 4–5 hours**

---

*End of Summary. Questions? See REFACTOR_AUDIT_REPORT.md for details.*
