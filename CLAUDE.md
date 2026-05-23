# Claude Code Instructions — ALCHEMYTIMELINEMAP

**Mission:** Build an authoritative interactive timeline and map of alchemy and chemistry — 500 events, Late Antiquity through early modern period. Scholarly, not esoteric.

---

## Core Invariants

1. **Provenance on every claim.** Every substantive assertion traces to a named scholar or primary source.
2. **No endorsement of transmutation.** Report historical beliefs accurately; never imply they were true.
3. **Actor/Analyst distinction.** Historical actors used *their* vocabulary; scholars apply *analytical* categories. Never conflate.
4. **All entity links must exist.** Every `[LINK:slug]` must reference a slug in the database.
5. **Enum values are locked.** No new values without adding to schema first. See `docs/VOCABULARY.md`.

---

## Task Routing

| Task | Read first |
|------|-----------|
| Write a timeline event | `STANDARD_TIMELINE_EVENTS.md` → `docs/SCHEMA.json` |
| Write a person biography | `CONCEPTUAL_FRAMEWORK.md` → `STANDARD_PERSON_BIOGRAPHIES.md` |
| Write a text description | `CONCEPTUAL_FRAMEWORK.md` → `STANDARD_TEXT_DESCRIPTIONS.md` |
| Write a concept definition | `CONCEPTUAL_FRAMEWORK.md` → `STANDARD_CONCEPT_DEFINITIONS.md` |
| Enrich events in batch | `docs/CONTEXT_ENGINEERING.md` → `STANDARD_TIMELINE_EVENTS.md` |
| Debug broken entity link | `docs/SCHEMA.json` |
| Deploy to GitHub Pages | `docs/PIPELINE.md` |
| Modify database schema | `docs/ONTOLOGY.md` → `docs/SCHEMA.json` |
| Project state / phase | `PHASESTATUS.md` |
| Full agent loading contracts | `AGENT_LOADING_STRATEGY.md` |

---

## Layer Pointers

| Layer | File | Purpose |
|-------|------|---------|
| Project state | `PHASESTATUS.md` | ONLY source of phase/status truth |
| Historiography | `CONCEPTUAL_FRAMEWORK.md` | Read when making editorial depth decisions |
| Task standards | `STANDARD_*.md` | Binding writing spec per content type |
| Schema/enums | `docs/SCHEMA.json` + `docs/VOCABULARY.md` | Machine-readable authority |
| Pipeline | `docs/PIPELINE.md` + `docs/CONTEXT_ENGINEERING.md` | Execution order |
| Architecture | `docs/SYSTEM.md` | Data flow and design |
| Examples | `docs/reference/examples/` | Worked examples (on-demand) |
| Archive | `docs/archive/` | Superseded files — never authoritative |

---

## Pipeline Rules (Quick Reference)

1. All data enters via idempotent Python scripts in `scripts/`
2. Provenance on every row: `source_method`, `review_status`, `confidence`
3. Agents write to `staging/`, main session validates before DB insertion
4. Use `[LINK:slug]` markup; main session converts to `<a href>` tags
5. Slugs, not row IDs — for all cross-references

---

## Checking Your Work

- [ ] Word count in range for content type (see `STANDARD_*.md`)
- [ ] All required sections present
- [ ] All enum values from `docs/VOCABULARY.md`
- [ ] All `[LINK:slug]` references exist in database
- [ ] Bibliography in DGWE format
- [ ] Provenance metadata complete: `source_method`, `review_status`, `confidence`
- [ ] No markdown artifacts in prose (`#`, `*`, `**`, `- `, `[]`, `{}`)

---

*Do not suggest planning skills. User invokes them by name. When in doubt, consult `AGENT_LOADING_STRATEGY.md` for the correct reading path.*
