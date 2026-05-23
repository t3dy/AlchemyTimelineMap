# archive/ — Superseded Files

These files were deprecated during the May 2026 architectural refactoring. Each was merged, split, or replaced by more focused alternatives.

**Do not reference these files for new work.** Use the layer system instead — see `LAYERED_ARCHITECTURE_DESIGN.md`.

---

## What Was Superseded and Why

| File | Reason deprecated | Replaced by |
|------|------------------|-------------|
| `CLAUDE_NEW.md` | Duplicate version during refactoring | `CLAUDE.md` (canonical boot file) |
| `CLAUDE_REFACTORED.md` | Draft version during refactoring | `CLAUDE.md` (canonical boot file) |
| `PROMPTS_REFACTORED.md` | Merged into CONCEPTUAL_FRAMEWORK.md | `CONCEPTUAL_FRAMEWORK.md` |
| `STYLEGUIDE_CONSOLIDATED.md` | Split into 4 task-specific files | `STANDARD_*.md` files |
| `STYLE_GUIDE_ALCHEMISTS.md` | Superseded by task-specific files | `STANDARD_PERSON_BIOGRAPHIES.md` |
| `STYLE_GUIDE_SCHOLARS_AND_TEXTS.md` | Superseded by task-specific files | `STANDARD_TEXT_DESCRIPTIONS.md` |
| `PHASESTATUS_REFACTORED.md` | Draft version during refactoring | `PHASESTATUS.md` (canonical) |
| `README_REFACTORED.md` | Draft version during refactoring | `README.md` |

---

## Deprecated Root-Level AGENT_PROMPT_*.md Files

The root-level `AGENT_PROMPT_*.md` files were superseded by the more focused agent prompts. The current canonical agent prompts are `AGENT_PROMPT_BIOGRAPHY_ENRICHER.md`, `AGENT_PROMPT_EVENT_ENRICHER.md`, `AGENT_PROMPT_TEXT_ENRICHER.md`, and `AGENT_PROMPT_ARCHIVE_ENTITY_EXTRACTOR.md`.

The `AGENT_PROMPT_COMPLETE_*.md` files (PERSON_BIOGRAPHIES, TEXT_ANALYSES, CONCEPT_DEFINITIONS) were one-shot prompts for bulk expansion runs and are no longer needed now that bulk expansion is complete.

---

*Created: 2026-05-23. For current documentation, start with `CLAUDE.md`.*
