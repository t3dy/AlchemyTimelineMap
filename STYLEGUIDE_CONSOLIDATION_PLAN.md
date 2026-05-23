# STYLEGUIDE Consolidation Plan

**Date:** 2026-05-22

---

## Current Style Guide Files

1. **STYLEGUIDE.md** (comprehensive, ~2,000 words)
   - Core prose standards (no markdown, no bullets, no hashtags)
   - Timeline events (100–250 words)
   - Person biographies (1,200–2,200 words)
   - Text descriptions (1,000–1,800 words)
   - Concept definitions (1,500–2,500 words)
   - Bibliography format (DGWE)
   - Checklist

2. **STYLE_GUIDE_ALCHEMISTS.md** (~1,000 words)
   - Focused on person biographies
   - Target lengths (index card vs. encyclopedia)
   - Structure for full entries (opening, main sections for historical alchemists vs. modern scholars)
   - Literature section
   - Example opening paragraphs

3. **STYLE_GUIDE_SCHOLARS_AND_TEXTS.md** (~1,500 words)
   - Part 1: Modern scholars (structure, example: William R. Newman)
   - Part 2: Alchemical texts (structure, example content)

---

## Content Overlap Analysis

### Unique content in STYLE_GUIDE_ALCHEMISTS.md
- More detailed breakdown of person sections (Works, Alchemical Significance, Transmission, Scholarly Debates)
- Distinction between historical alchemists and modern scholars
- Concrete example opening paragraph (Jabir ibn Hayyan)
- **Recommendation:** Integrate as §2.2 "Detailed Section Breakdown" in STYLEGUIDE.md

### Unique content in STYLE_GUIDE_SCHOLARS_AND_TEXTS.md
- Part 1: Detailed structure for modern scholars (Central Thesis, Key Works, Historiographical Position)
  - **Recommendation:** Integrate into STYLEGUIDE.md §2 "Person Biographies" as subsection
- Part 2: Detailed structure for alchemical texts (Content and Theory, Composition, Reception, Literature)
  - **Recommendation:** Merge into STYLEGUIDE.md §3 "Text Descriptions" as expanded detail section
- Full example: William R. Newman biography (900+ words)
  - **Recommendation:** Move to docs/reference/examples/ as WILLIAM_NEWMAN_EXAMPLE.md

---

## Consolidation Strategy

### Option A (Recommended): Merge into STYLEGUIDE.md

1. Keep STYLEGUIDE.md as comprehensive master guide (~3,500–4,000 words)
2. Expand §2 (Person Biographies) with subsections:
   - §2.1: General requirements (all persons)
   - §2.2: Historical alchemists (Works, Alchemical Significance, Transmission, Scholarly Debates)
   - §2.3: Modern scholars (Central Thesis, Key Works, Historiographical Position)
   - §2.4: Example opening paragraphs (both types)
3. Expand §3 (Text Descriptions) with subsections:
   - §3.1: Primary sources (Content, Composition, Reception)
   - §3.2: Commentary & scholarship
   - §3.3: Example structure
4. Move detailed examples (William R. Newman) to docs/reference/examples/
5. Archive STYLE_GUIDE_ALCHEMISTS.md and STYLE_GUIDE_SCHOLARS_AND_TEXTS.md

**Benefit:** Single authoritative source for all prose standards. Agents read STYLEGUIDE.md once and know everything.

### Option B (Alternative): Keep Specialized Guides

1. Rename STYLEGUIDE.md → STYLEGUIDE_CORE.md (core standards only, ~1,500 words)
2. Keep STYLE_GUIDE_ALCHEMISTS.md and STYLE_GUIDE_SCHOLARS_AND_TEXTS.md as task-specific references
3. Cross-reference from STYLEGUIDE_CORE.md: "For person biographies, also see STYLE_GUIDE_ALCHEMISTS.md and STYLE_GUIDE_SCHOLARS_AND_TEXTS.md Part 1"

**Benefit:** Task-specific guides may be easier to reference during active writing.  
**Drawback:** Doubles reading overhead; risk of contradiction between guides.

---

## Recommendation: Option A (Merge)

**Rationale:**
- Agents should read one comprehensive guide, not three
- Eliminates contradiction risk
- Context efficiency (fewer files to load per task)
- Examples can be preserved in reference/ for case studies

---

## Implementation Steps

1. **Read both STYLE_GUIDE files carefully** (already done)
2. **Identify unique content** in each (done above)
3. **Structure expanded STYLEGUIDE.md** with new sections
4. **Copy detailed examples** to docs/reference/examples/
5. **Test with an agent prompt:** "Write a person biography for [figure]. Read STYLEGUIDE.md § 2.2 first."
6. **Archive original files** (move to docs/archive/ with explanatory note)

---

## Updated STYLEGUIDE.md Structure (Proposed)

```
# ALCHEMYTIMELINEMAP Content Style Guide

## § 1: The Core Standard
- Encyclopedia prose standard
- Absolute prohibitions (no markdown, no bullets, etc.)

## § 2: Person Biographies (bio_html)
- General requirements (1,200–2,200 words)
- Opening paragraph template
- § 2.1: For historical alchemists/chemists
  - Required sections: Works, Alchemical Significance, Transmission, Scholarly Debates
  - Material grounding in laboratory practice
- § 2.2: For modern scholars
  - Required sections: Central Thesis, Key Works, Methodological Approach, Scholarly Disputes
- § 2.3: Literature section format
- § 2.4: Complete example (Jabir ibn Hayyan or William R. Newman)
- Checklist

## § 3: Text Descriptions (analysis_html)
- General requirements (1,000–1,800 words)
- Opening paragraph template
- § 3.1: For primary sources
  - Required sections: Content and Theory, Composition and Textual Tradition, Modern Scholarship
  - Material and textual grounding
- § 3.2: For commentary and scholarship
- § 3.3: Literature section format
- § 3.4: Complete example
- Checklist

## § 4: Timeline Events
- [existing content]
- Checklist

## § 5: Concept Definitions
- [existing content + expanded]
- Actor/Analyst distinction with detailed examples
- Historical Usage section with material grounding
- Scholarly Significance section with named scholars
- Checklist

## § 6: Bibliography Format (DGWE Model)
- Format specification
- Examples across types

## Appendix A: Example Opening Paragraphs
- Historical alchemist (Jabir ibn Hayyan)
- Modern scholar (William R. Newman)
- Primary source (Summa Perfectionis)
- Concept ACTOR_TERM (Distillation)
- Concept ANALYST_TERM (Hermeticism)

## Appendix B: Complete Example Entries
- Full person biography (William R. Newman, 900 words)
- Full text description (Summa Perfectionis, 1,200 words)
```

---

## Estimated Time

- Consolidation: 90 minutes
- Testing with agent: 30 minutes
- Archiving & documentation: 20 minutes
- **Total: ~2.5 hours**

---

## Next Steps

1. Confirm this consolidation strategy with user
2. Execute consolidation
3. Test with Phase 2 agent task
4. Update CLAUDE.md and agent prompts to reference new STYLEGUIDE.md structure

---

*This plan is subject to user approval.*
