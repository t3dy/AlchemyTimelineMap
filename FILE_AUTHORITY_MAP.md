# FILE AUTHORITY MAP — ALCHEMYTIMELINEMAP

**Purpose:** Define the ONE canonical responsibility of each file. Identify duplication, contradictions, merges, deprecations.

---

## SYSTEM AUDIT TABLE

For every active file, identify its authority class and canonical responsibility.

| File | Current Size | Type | Canonical Responsibility | Should Contain | Should NOT Contain | Authority Status | Action |
|------|------|------|------|------|------|------|------|
| **BOOT/ROUTING (Layer 0)** |
| CLAUDE.md | 2,600w | Canonical | Boot + task routing | Mission, invariants, routing decision tree | Historiography, standards, architecture summary, vocabulary, authorities | **STALE** (contradicts PHASESTATUS) | **REPLACE with 400w version** |
| CLAUDE_NEW.md | 500w | Canonical (candidate) | Boot + task routing | Mission, invariants, routing | (correct) | **VALID** | Rename to CLAUDE.md; delete old |
| CLAUDE_REFACTORED.md | 500w | Derived | Boot + task routing | (same as CLAUDE_NEW.md) | (correct) | **DUPLICATE of CLAUDE_NEW.md** | Delete |
| README.md | 500w | Onboarding | Project overview for GitHub | 1-sentence pitch, tech stack, links to CLAUDE/TASK_ROUTING | Duplicated routing, duplicated historiography, full architecture | **PARTIAL** (overlaps CLAUDE.md) | **Shrink to <200w** |
| **PROJECT STATE (Layer 1)** |
| PHASESTATUS.md | 1,200w | Canonical | Single source of truth for phase, status, next steps | Current phase, completed tasks, known issues, event counts, immediate next actions | Session notes, project history, historiography | **CORRECT** | Keep as-is (ONLY status file) |
| PROJECT_SUMMARY.md | 500w | Archival | Session snapshot from Phase 0/1 | (historical record) | Current operations | **SUPERSEDED by PHASESTATUS.md** | Move to docs/archive/; do not read |
| SESSION_SUMMARY.md | 500w | Archival | Session working notes | (historical record) | Current operations | **ARCHIVAL (decay risk)** | Move to docs/archive/; do not read |
| **CONCEPTUAL FRAMEWORK (Layer 2)** |
| PROMPTS.md | 4,000w | Canonical (bloated) | Historiographical framework + scholarly authorities | Vision, historiography, authorities, methodological commitments | Word count rules, prose standards, agent operating rules, vocabulary lock | **AUTHORITATIVE but BLOATED** | **TRIM to 2,000w** (remove standards, rules, vocabulary) |
| PROMPTS_REFACTORED.md | 2,500w | Derived | Historiographical framework | (correct subset of PROMPTS.md) | (correct) | **VALID TRIMMED VERSION** | Rename to CONCEPTUAL_FRAMEWORK.md; delete PROMPTS.md |
| SCHOLARLYPROFILE.md | 1,500w | Reference | Ted Hand's scholarly values and methodological commitments | User's scholarly values, preferences, why these choices matter | Operational rules | **OPTIONAL CONTEXT** | Move to docs/reference/ (on-demand, not boot) |
| SONNETSCHOLARLYPROFILE.md | 1,200w | Archival | Duplicate for Sonnet model | (historical) | Current operations | **SUPERSEDED** | Move to docs/archive/; delete |
| **OPERATIONAL STANDARDS (Layer 3)** |
| STYLEGUIDE.md | 2,000w | Canonical (fragmented) | Prose standards for all content types | General prose principles, per-type word counts, required sections, checklist | Entity linking instructions (→ Layer 4), enum usage (→ Layer 4) | **AUTHORITATIVE but SPLIT across files** | Keep as reference; CREATE task-specific standard files |
| STYLEGUIDE_CONSOLIDATED.md | 3,500w | Derived | Prose standards (expanded) | § 1–6: all content types, examples, checklist | (correct as comprehensive) | **VALID but TOO LARGE** | Use as source for task-specific files; archive original |
| STYLE_GUIDE_ALCHEMISTS.md | 1,000w | Archival | Person biography standards (historical predecessor) | (historical) | Current operations | **CONSOLIDATED into STYLEGUIDE.md** | Move to docs/archive/ |
| STYLE_GUIDE_SCHOLARS_AND_TEXTS.md | 1,500w | Archival | Text + scholar biography standards (historical) | (historical) | Current operations | **CONSOLIDATED into STYLEGUIDE.md** | Move to docs/archive/ |
| STANDARD_TIMELINE_EVENTS.md | 400w | Canonical (NEW) | Timeline event writing specification | Word count, required fields, validation checklist, example | Historiography, entity linking details | **NEW FILE** | Create (pull from STYLEGUIDE § 4) |
| STANDARD_PERSON_BIOGRAPHIES.md | 500w | Canonical (NEW) | Person biography writing specification | Word count, required sections, validation checklist, example | Historiography (optional context via link only) | **NEW FILE** | Create (pull from STYLEGUIDE § 2) |
| STANDARD_TEXT_DESCRIPTIONS.md | 450w | Canonical (NEW) | Text description writing specification | Word count, required sections, validation checklist, example | Historiography | **NEW FILE** | Create (pull from STYLEGUIDE § 3) |
| STANDARD_CONCEPT_DEFINITIONS.md | 550w | Canonical (NEW) | Concept definition writing specification | Word count, required sections, ACTOR_TERM/ANALYST_TERM rules, validation checklist, example | General historiography (link to PROMPTS instead) | **NEW FILE** | Create (pull from STYLEGUIDE § 5) |
| **TECHNICAL CONTRACTS & SCHEMA (Layer 4)** |
| docs/VOCABULARY.md | 500w | Canonical (mixed) | Enum definitions + explanations | Enum values with descriptions | Prose philosophy | **AUTHORITATIVE but PROSE-ONLY** | Keep for reference; CREATE JSON schema version |
| docs/ONTOLOGY.md | 1,400w | Canonical (mixed) | Database schema (prose + SQL) | Table definitions, field types, constraints | Architecture philosophy (→ SYSTEM.md) | **AUTHORITATIVE but PROSE-HEAVY** | Keep for reference; CREATE JSON schema version |
| docs/SYSTEM.md | 900w | Canonical | Data flow diagram + design principles | Architecture diagram, design philosophy, typical workflow | Enum definitions (→ VOCABULARY), schema (→ ONTOLOGY) | **CORRECT** | Keep as-is |
| docs/PIPELINE.md | 900w | Canonical | Script execution order | Script names, dependencies, execution order | Architecture explanation (→ SYSTEM.md), implementation details (→ code) | **CORRECT** | Keep as-is |
| docs/CONTEXT_ENGINEERING.md | 1,200w | Canonical | Batch strategy for 500-event scale | Problem, solution (batch + pre-query pattern), 5-step workflow | General architecture (→ SYSTEM.md) | **CORRECT** | Keep as-is |
| SCHEMA.json | 0 | Canonical (NEW) | Machine-readable schema authority | All content type specs, enum definitions, field definitions | Prose | **NEW FILE (executable authority)** | Create from docs/VOCABULARY.md + docs/ONTOLOGY.md |
| CONTRACTS.json | 0 | Canonical (NEW) | Pipeline execution contracts | Staging manifest format, validation gates, error codes | Prose philosophy | **NEW FILE (executable authority)** | Create for staging workflow |
| **AGENT ROUTING & EXECUTION (Layer 3)** |
| docs/agents/TASK_ROUTING.md | 600w | Canonical | Task → prerequisites → prompt router | Decision matrix for 11 common tasks | Detailed task instructions (→ PROMPT_*.md) | **CORRECT** | Keep as-is; link from CLAUDE.md |
| docs/agents/PROMPT_BIOGRAPHY_ENRICHER.md | 400w | Canonical (NEW) | Person biography execution contract | Word count, required sections, validation checklist, example | Prose historiography preamble (reference PROMPTS instead) | **EXECUTABLE CONTRACT** | Create (trim from existing agent prompt) |
| docs/agents/PROMPT_EVENT_ENRICHER.md | 380w | Canonical (NEW) | Timeline event execution contract | Word count, required fields, validation checklist, example | Historiography preamble | **EXECUTABLE CONTRACT** | Create |
| docs/agents/PROMPT_CONCEPT_ENRICHER.md | 450w | Canonical (NEW) | Concept definition execution contract | Word count, ACTOR_TERM/ANALYST_TERM rules, validation checklist, example | Historiography preamble | **EXECUTABLE CONTRACT** | Create |
| docs/agents/PROMPT_TEXT_ENRICHER.md | 400w | Canonical (NEW) | Text description execution contract | Word count, required sections, validation checklist, example | Historiography preamble | **EXECUTABLE CONTRACT** | Create |
| AGENT_PROMPT_EVENT_ENRICHER.md | 400w | Archival | Old version of task prompt | (historical) | Current operations | **SUPERSEDED by docs/agents/PROMPT_EVENT_ENRICHER.md** | Move to docs/archive/ |
| AGENT_PROMPT_BIOGRAPHY_ENRICHER.md | 400w | Archival | Old version of task prompt | (historical) | Current operations | **SUPERSEDED** | Move to docs/archive/ |
| AGENT_PROMPT_TEXT_ENRICHER.md | 400w | Archival | Old version of task prompt | (historical) | Current operations | **SUPERSEDED** | Move to docs/archive/ |
| AGENT_PROMPT_COMPLETE_PERSON_BIOGRAPHIES.md | 400w | Archival | Old version of task prompt | (historical) | Current operations | **SUPERSEDED** | Move to docs/archive/ |
| AGENT_PROMPT_COMPLETE_TEXT_ANALYSES.md | 400w | Archival | Old version of task prompt | (historical) | Current operations | **SUPERSEDED** | Move to docs/archive/ |
| AGENT_PROMPT_COMPLETE_CONCEPT_DEFINITIONS.md | 400w | Archival | Old version of task prompt | (historical) | Current operations | **SUPERSEDED** | Move to docs/archive/ |
| AGENT_PROMPT_ARCHIVE_ENTITY_EXTRACTOR.md | 400w | Archival | Old version of task prompt | (historical) | Current operations | **UNCLEAR IF USED** | Move to docs/archive/ or delete |
| **EXAMPLES & REFERENCE (Layer 6)** |
| docs/reference/examples/ | — | Reference | Worked examples | Complete timeline event, person bio, text description, concept definitions (ACTOR_TERM, ANALYST_TERM) | Operational rules | **ON-DEMAND** | Create from STYLEGUIDE.md examples |
| docs/reference/SCHOLARLY_PROFILE.md | 1,500w | Reference | Ted Hand's scholarly context | Scholarly values, methodological commitments, preferred frameworks | Operational instructions | **CONTEXT** | Move from root; keep as optional read |
| docs/reference/ARCHAEOLOGY_AND_MATERIAL_CULTURE.md | — | Reference | Domain-specific research | Material evidence, Pamela Smith framework, archaeological examples | Operational standards | **DOMAIN CONTEXT** | Move from root; keep as reference |
| docs/reference/ARCHAEOLOGY_RESEARCH_SUMMARY.md | — | Reference | Archaeology research synthesis | Complete research summary with sources | Operational standards | **DOMAIN CONTEXT** | Move from root; keep as reference |
| docs/reference/ACTOR_ANALYST_EXAMPLES.md | — | Reference (NEW) | Worked examples of ACTOR_TERM vs. ANALYST_TERM distinction | Multiple examples per type | Prose explanation (→ PROMPTS) | **CLARITY REFERENCE** | Create from PROMPTS § 5 examples |
| **ARCHIVE & HISTORY (Layer 7)** |
| docs/archive/ | — | Archival | All superseded files with deprecation notes | Reason file was archived, what replaced it | Current operations | **HISTORICAL RECORD** | Use for all deprecated files |
| CHANGELOG.md | 1,000w | Documentation | What changed in refactoring | Version history, refactor dates, files moved | Current operational rules | **PROCESS DOCUMENTATION** | Keep as historical record |
| IMPLEMENTATION_COMPLETE.md | 1,600w | Documentation | Refactoring implementation guide | Steps taken, verification checklist | Current operational rules | **PROCESS DOCUMENTATION** | Keep as historical record |
| ARCHITECTURE_AUDIT_CRITICAL.md | 3,000w | Documentation | Critical audit findings | Problem analysis, layer bleed examples, contradiction risks | Current operational rules | **DIAGNOSTIC** | Keep as reference for why redesign happened |
| SEPARATION_OF_CONCERNS_ARCHITECTURE.md | 2,000w | Documentation | Previous separation-of-concerns design (pre-Layer redesign) | Historical approach | Current layered design | **SUPERSEDED by LAYERED_ARCHITECTURE_DESIGN.md** | Move to docs/archive/ |
| REFACTOR_AUDIT_REPORT.md | 3,000w | Documentation | Previous refactor audit | Historical findings | Current design | **SUPERSEDED** | Move to docs/archive/ |

---

## CONTRADICTION RISKS (Current System)

| Conflict | Source A | Source B | Risk | Resolution |
|----------|----------|----------|------|-----------|
| **Current phase** | CLAUDE.md: "Phase 0" | PHASESTATUS.md: "Phase 2" | **HIGH** | Delete CLAUDE.md; point to PHASESTATUS.md only |
| **Historiography** | PROMPTS.md § 3 | Agent prompt preambles | **MEDIUM** | Remove preambles; link to PROMPTS instead |
| **Prose standards** | STYLEGUIDE.md | STANDARD_*.md (when created) | **WILL APPEAR** | STANDARD_*.md is task-specific; STYLEGUIDE.md is reference |
| **Enum values** | docs/VOCABULARY.md (prose) | SCHEMA.json (when created) | **WILL APPEAR** | SCHEMA.json is authoritative; VOCABULARY.md is reference |
| **ACTOR_TERM definition** | PROMPTS.md § 5 | docs/VOCABULARY.md | **LOW** | Both can coexist; PROMPTS is conceptual, VOCABULARY is definition |

---

## MERGE RECOMMENDATIONS

| Files | Should Merge Into | Reason |
|-------|------|-------|
| PROMPTS.md + PROMPTS_REFACTORED.md | CONCEPTUAL_FRAMEWORK.md (2,000w) | Remove duplication; keep only historiography |
| STYLEGUIDE.md + STYLEGUIDE_CONSOLIDATED.md | Reference layer; split by task | One reference file + 4 task-specific standard files |
| STYLE_GUIDE_ALCHEMISTS.md + STYLE_GUIDE_SCHOLARS_AND_TEXTS.md | docs/archive/ | Consolidated into STYLEGUIDE.md |
| CLAUDE.md + CLAUDE_NEW.md + CLAUDE_REFACTORED.md | New CLAUDE.md (400w) | Keep one canonical boot file |
| docs/VOCABULARY.md + SCHEMA.json | Keep separate (prose reference + executable schema) | Different audiences |
| docs/ONTOLOGY.md + SCHEMA.json | Keep separate (prose reference + executable schema) | Different audiences |

---

## DEPRECATION PLAN

Files to move to docs/archive/ (with explanatory README):

1. CLAUDE.md (superseded by 400w version)
2. PROMPTS.md (superseded by CONCEPTUAL_FRAMEWORK.md)
3. PROMPTS_REFACTORED.md (merged into CONCEPTUAL_FRAMEWORK.md)
4. STYLEGUIDE.md (split into reference + task-specific files)
5. STYLEGUIDE_CONSOLIDATED.md (replaced by split files)
6. STYLE_GUIDE_ALCHEMISTS.md
7. STYLE_GUIDE_SCHOLARS_AND_TEXTS.md
8. CLAUDE_NEW.md (merged into new CLAUDE.md)
9. CLAUDE_REFACTORED.md (merged into new CLAUDE.md)
10. All AGENT_PROMPT_*.md (root level; superseded by docs/agents/PROMPT_*.md)
11. PROJECT_SUMMARY.md
12. SESSION_SUMMARY.md
13. ARCHAEOLOGY_RESEARCH_SUMMARY.md (move to docs/reference/)
14. ARCHAEOLOGY_AND_MATERIAL_CULTURE.md (move to docs/reference/)
15. INTEGRATION_GUIDE_ARCHAEOLOGY.md (move to docs/reference/)
16. SCHOLARLYPROFILE.md (move to docs/reference/)
17. SONNETSCHOLARLYPROFILE.md (delete or archive)

Files to create (NEW):

1. CLAUDE.md (400w, boot only)
2. CONCEPTUAL_FRAMEWORK.md (2,000w, historiography)
3. STANDARD_TIMELINE_EVENTS.md (400w, task-specific)
4. STANDARD_PERSON_BIOGRAPHIES.md (500w, task-specific)
5. STANDARD_TEXT_DESCRIPTIONS.md (450w, task-specific)
6. STANDARD_CONCEPT_DEFINITIONS.md (550w, task-specific)
7. SCHEMA.json (executable, authority source)
8. CONTRACTS.json (executable, staging contracts)
9. docs/agents/PROMPT_BIOGRAPHY_ENRICHER.md (refactored, <500w)
10. docs/agents/PROMPT_EVENT_ENRICHER.md (refactored, <500w)
11. docs/agents/PROMPT_CONCEPT_ENRICHER.md (refactored, <500w)
12. docs/agents/PROMPT_TEXT_ENRICHER.md (refactored, <500w)
13. docs/reference/examples/ (worked examples, on-demand)
14. docs/reference/ACTOR_ANALYST_EXAMPLES.md (clarity reference)

Files to keep (unchanged):

1. PHASESTATUS.md (project state, canonical)
2. README.md (update to <200w)
3. docs/SYSTEM.md
4. docs/ONTOLOGY.md (as reference)
5. docs/PIPELINE.md
6. docs/CONTEXT_ENGINEERING.md
7. docs/agents/TASK_ROUTING.md
8. docs/VOCABULARY.md (as reference, with link to SCHEMA.json)
9. CHANGELOG.md (historical record)

---

## AUTHORITY PRECEDENCE RULES

**If two files conflict, follow this hierarchy:**

1. **Executable schema (SCHEMA.json, CONTRACTS.json, SQL constraints)** ← AUTHORITATIVE
2. **Task-specific standards (STANDARD_*.md)** ← BINDING for that task
3. **Reference documentation (STYLEGUIDE.md, docs/ONTOLOGY.md, docs/VOCABULARY.md)** ← DESCRIPTIVE
4. **Conceptual framework (CONCEPTUAL_FRAMEWORK.md)** ← INTERPRETIVE
5. **Examples & reference (Layer 6)** ← ILLUSTRATIVE
6. **Archive (Layer 7)** ← HISTORICAL ONLY (never authoritative)

---

*Next document: AGENT LOADING STRATEGY*
