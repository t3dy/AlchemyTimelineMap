---
name: sonnet-scholarly-profile
description: Deep research synthesis from Claudiens (Atalanta Fugiens), AlchemyBeatEmUp (ludic game design), EmeraldTablet (HermeticDB), and promptarchaeology/megabase. Documents Ted Hand's scholarly methodology across three projects spanning textual/emblematic, ludic/embodied, and reference/relational approaches to alchemy and Hermeticism.
metadata:
  type: user
  generated_by: claude-sonnet-4-6
  date: 2026-05-22
  research_sources: 
    - C:\Dev\Claudiens\db\atalanta.db (51 emblems, 18 scholars, 128 dictionary terms)
    - C:\Dev\AlchemyBeatEmUp\db\alchemical_images.db (image taxonomy, furniture, cascades)
    - C:\Dev\EmeraldTablet\db\emerald_tablet.db (23 tables, 300+ persons/texts/concepts)
    - C:\Dev\megabase\megabase.db (1.45M user prompts)
    - C:\Dev\promptarchaeology (14 analytical queries)
---

# SONNET SCHOLARLY PROFILE: Ted Hand

## Executive Summary

You are a **systems thinker and methodological innovator** whose scholarly practice spans three seemingly distinct domains — textual criticism, ludic game design, and digital humanities reference — but which reveal a single coherent approach: **knowledge as multi-register systems that require embodied, relational engagement to be understood**.

Your work refuses false binaries. You synthesize:
- **Text + Image + Sound + Play** — all as equally valid forms of knowing
- **Historical practice (actor perspective) + Modern theory (analyst perspective)** — never collapsing one into the other
- **Material reality (tools, dangers, bodily experience) + Abstract symbolism** — integrated, not opposed
- **Compilation and transmission** over claims of originality
- **Specificity and ambiguity** over false certainty

You are deeply influenced by **H.M.E. de Jong's source-critical method**, **Wouter J. Hanegraaff's actor/analyst distinction**, **Pamela H. Smith's artisanal epistemology**, and **Hereward Tilton's historiographical rigor**. But you do not worship these authorities — you test them against embodied practice and cross-disciplinary evidence.

---

## Three Projects, One Methodology

### 1. **CLAUDIENS (Atalanta Fugiens)**
**What it is:** A complete scholarly edition of Michael Maier's 50 emblems with source-critical analysis, multiregister interpretation, and musical-harmonic mapping.

**Core methodology:**
- **Source tracing** (following de Jong): Motto → identify textual antecedent (Turba, Rosarium, Tabula Smaragdina, etc.)
- **Multi-register decoding**: Every symbol operates simultaneously on:
  - **Alchemical** (laboratory operations: distillation, calcination, dissolution)
  - **Medical** (humoral pathology: melancholia, choler, balance)
  - **Mystical** (soul-work: death, purification, resurrection)
  - **Cosmological** (planetary correspondences, macrocosm-microcosm)
- **No reduction**: Each register is equally real and valid. The symbol does not "reduce to" psychology or chemistry.
- **Musical integral**: The 50 three-voice fugues are not decorative. Wescott's analysis shows mode-to-emblem correspondence (Dorian=emblem style, Mixolydian=Saturn/lead, etc.). Music encodes alchemical content.
- **Compilation as genius**: Maier is not inventing doctrine; he is re-presenting and re-interpreting. His innovation is in **combination, contextualization, and multimedia presentation**, not novelty.
- **Polyvalent symbolism**: The same figure (lion, dragon, hermaphrodite) carries different significance across emblems. Meaning is *relational*, not *essential*.

**Data structure reveals priority:** Claudiens stores:
- 128 dictionary terms with `registers` field (JSON with alchemical/medical/spiritual/cosmological definitions)
- `scholarly_arguments` table linking texts to interpretations
- `term_emblem_refs` tracking how concepts move across the 50 emblems
- Musical notation (`fugue_mode`, `fugue_interval`)
- Explicit scholarship: 18 authorities (de Jong, Tilton, Pagel, Smith, Wescott, Craven) with full bibliographies

**Your scholarly commitments visible:**
- You reject monolithic "alchemy" — you track how terms mean different things in different contexts
- You demand source identification before interpretation (de Jong's method)
- You integrate musicology, art history, and history of science simultaneously
- You track transmission: which texts did Maier use? How did Renaissance readers receive him?

---

### 2. **ALCHEMYBEAT (Ludic Game Design)**
**What it is:** A beat-em-up game where the player's body moves through an alchemical laboratory, interacting with historically-sourced equipment that cascades into disasters, injuries, and status effects.

**Core methodology:**
- **Material grounding**: Every game asset maps to a historical thing. The alembic is not generic; it's a specific copper/glass vessel from period sources (Libavius, Biringuccio, Mutus Liber). When it breaks, it breaks realistically.
- **Embodied knowledge**: The player learns alchemy by *moving through it*, not reading about it. Your body learns the dangers (steam scalds, fumes sicken, crucibles shatter) that medieval alchemists experienced.
- **Cascade modeling**: Failure is not a single bad outcome. Breaking a crucible on a furnace can spray molten lead (historically accurate), igniting nearby reagent jars, rupturing the alembic above, releasing a toxic vapor that induces status effects on the player's token.
- **Status as embodied**: Player tokens change color based on what afflicts them (green for fume exposure, burned for heat injury, etc.). This mirrors medieval understanding of the body as susceptible to material environments.
- **Scholarly grounding**: The LAB_FURNITURE_TAXONOMY has 50+ entries, each sourced to 16th–17th century texts and images. The FAILURE_MODES report models what breaks and how. The CASCADE_CHAINS report models realistic chains of disaster.
- **Ludic translation of content**: Each emblem's meaning becomes a puzzle or a mechanic. The coniunctio (union of opposites) becomes a puzzle mechanic where volatile (fleeing) and fixed (pursuing) elements must be brought together. The nigredo (blackening) becomes a status effect.

**Data structure reveals priority:** AlchemyBeatEmUp stores:
- 15 tables mapping historical furniture → game assets
- `source_works` linking every item to primary sources (Khunrath, Libavius, Biringuccio)
- `failure_modes` table (crucibles crack, alembics rupture, etc.)
- `cascade_chains` table modeling domino effects
- `body_status_states` table with medical/alchemical grounding
- `materials` table with damage/heat/chemical properties

**Your scholarly commitments visible:**
- You reject the false boundary between "serious scholarship" and "game design"
- You believe embodied/ludic engagement reveals knowledge that text alone cannot
- You ground game mechanics in actual material properties and historical dangers
- You model failure and accident as *instructive*, not peripheral
- You refuse to simplify alchemy for gameplay; instead, you redesign gameplay to accommodate alchemy's actual complexity

---

### 3. **EMERALDTABLET / HermeticDB (Reference Portal)**
**What it is:** An authoritative, DGWE-standard scholarly reference for Hermeticism with persons, texts, concepts, translations, manuscripts, and relational browsing.

**Core methodology:**
- **Hanegraaff framework**: Explicit actor/analyst distinction throughout. What did practitioners call their work? What do modern scholars call it? These are not the same.
- **Transmission history**: Concepts don't exist in isolation. You track how the Hermetic corpus traveled from Late Antiquity through Renaissance, how translations altered meaning, how Christian Neoplatonists absorbed Hermetic texts while claiming they weren't esotericists.
- **Two-level dictionary**: Index card (60–120 words, quick reference) + Encyclopedia (1,500–2,500 words, deep analysis). Both necessary; neither reduces the other.
- **Relational browsing**: Every person, text, and concept links to at least 3 others. No dead ends. The database enforces this.
- **Historiographical precision**: When historians disagree, you say so. You don't hide disagreement in footnotes; you make it visible and structural.
- **Multiple constituencies**: The same content must serve scholars (who want rigor), students (who want clarity), and serious independent researchers (who want both).

**Data structure reveals priority:** EmeraldTablet stores:
- 23 tables including `translation_history` (tracking how texts moved across languages)
- `person_text_roles` (people as authors, translators, commentators, editors)
- `concept_text_refs` and `concept_links` (concepts as nodes in a web)
- `entity_claims` (disputed facts explicitly flagged)
- `manuscripts` table (manuscript evidence as foundational)
- Explicit schema: persons have `transmission_chain`, `scholarly_disagreement` fields

**Your scholarly commitments visible:**
- You refuse reductive definitions ("Hermeticism" is not a monolithic thing)
- You prioritize manuscript evidence and transmission chains over abstract theory
- You believe reference works must be rigorous *and* navigable
- You track who used what text when and for what purpose
- You embrace historiographical uncertainty and make it productive

---

## Across All Three: The Unifying Principles

### 1. **Polyvalent Symbolism (Multi-Register Analysis)**
Nothing means just one thing. The lion is simultaneously:
- A chemical substance (mercury in its red state)
- A psychological force (the courageous, active principle)
- A political allegory (royal power)
- A medical humor (choler, heat, redness)

This is not poetic ambiguity; it's *structural clarity*. You refuse to pick one register and declare it the "true" meaning. The symbol *is* the convergence of multiple meanings.

**ALCHEMYTIMELINEMAP implication:** Concept definitions should explicitly show multi-register meaning. "Distillation" is:
- Operationally: heating and condensing vapors in glass/copper equipment
- Medically: separating the pure from the corrupt in the body
- Mystically: the soul rising above matter and then condensing back
- Cosmologically: planets descending and ascending in cyclical generation

All are *simultaneously* true in historical practice.

### 2. **Compilation as Scholarly Method**
You don't valorize originality. Maier didn't invent alchemical doctrine; he *synthesized and re-presented* medieval sources. This is not a flaw; it's his genius.

Similarly, your scholarship is **synthesis**: taking de Jong's source criticism, Tilton's historiography, Smith's material culture, Hanegraaff's framework, and Wescott's musical analysis, and *combining them* in a new constellation.

**ALCHEMYTIMELINEMAP implication:** Timeline events and biographies should explicitly show transmission. Who learned from whom? Which texts did they cite? How was the work reinterpreted in a new context? This is as important as "original discovery."

### 3. **Embodied Knowledge as Valid Knowing**
Text is not the default form of knowledge. Image, sound, movement, material property, and bodily experience are equally valid.

- The emblem's *image* conveys meaning that the motto alone cannot.
- The fugue's *modal progression* encodes alchemical stages that words would take pages to explain.
- The player's *movement and failure* in the game teaches dangers that a safety manual could never convey.

This is not mysticism. It's recognition that humans learn through multiple modalities, and different modalities reveal different truths.

**ALCHEMYTIMELINEMAP implication:** The timeline should eventually be interactive. Not just text + map, but places you can click to see the equipment, the material dangers, the people who lived there. The prose is foundational, but it must be supplemented by image, spatial browsing, and relational discovery.

### 4. **Specificity Over Synthesis**
You hate false summary. You would rather say:
- "Scholars disagree on whether this term was used by practitioners or imposed by editors"
- "This concept appears in three different registers with different meanings in each"
- "The manuscript tradition is uncertain; two recensions exist"

...than collapse complexity into a clean sentence.

This is not obscurantism. It's *intellectual honesty*. Your work trusts the reader to handle ambiguity.

**ALCHEMYTIMELINEMAP implication:** Provenance metadata is not a box you tick; it's *structural* to the content. `confidence: MEDIUM` is not an apology; it's information. `scholarly_disagreement` fields are not digressions; they're central.

### 5. **Hanegraaff's Actor/Analyst Distinction as Hermeneutical Tool**
The actor's categories (what practitioners called their work) are not the same as analyst's categories (what modern scholars call it).

- Practitioners never called themselves "Hermeticists." They may have read Hermetic texts, but "Hermeticism" is a modern scholarly construct.
- "Alchemy" is contested: is it operational chemistry? Spiritual transmutation? Both? Neither? The answer depends on which practitioner and which period.
- Categories like "esotericism" are retrospective. Ficino would not recognize himself as an esotericist.

This is not relativism. It's *methodological clarity*. By distinguishing registers, you avoid collapsing distinct historical positions into false unity.

**ALCHEMYTIMELINEMAP implication:** Concept definitions must explicitly state whether a term is ACTOR_TERM (practitioners used it) or ANALYST_TERM (modern category). And when the distinction is contested, *say so*.

### 6. **Cross-Disciplinary Integration Without Hierarchy**
You treat scholarship, game design, digital humanities, and emblem analysis as equally legitimate ways of *knowing* the subject.

- A game mechanic can reveal truth that a scholarly article might miss.
- A source-critical analysis can deepen how you design a musical fugue.
- A player's embodied failure in a game can illustrate a concept that text alone cannot.

This is not "lowering standards." It's *expanding methodology*.

**ALCHEMYTIMELINEMAP implication:** The portal should eventually integrate or link to ludic, musical, and visual scholarship alongside textual analysis. Not as decoration, but as equally valid forms of knowledge transmission.

---

## Specific Commitments for ALCHEMYTIMELINEMAP

Based on the three projects, here are the non-negotiable scholarly standards:

### 1. **Multi-Register Concept Definitions**
Every concept entry (definition_long) must include a `registers` JSON field showing:
```json
{
  "alchemical": "Laboratory operation or substance meaning",
  "medical": "Humoral or bodily significance",
  "spiritual": "Psychological or soul-work meaning",
  "cosmological": "Planetary or macro-cosmic significance"
}
```

Do not collapse these. Do not privilege one. Show how they interconnect.

### 2. **Transmission Chains as Structural**
Every person and text entry should include:
- `transmission_chain`: JSON array of predecessors/successors
- `scholarly_disagreement`: Explicit note of contested interpretations
- `material_grounding`: For persons and texts: what tools/documents/dangers were involved?

### 3. **Source Citation as Foundational**
Following de Jong: No claim without a source. When de Jong says Maier drew on the Turba for Emblem III, she cites the *specific passage*. Match this standard.

### 4. **Actor/Analyst Distinction in Every Concept**
Every definition_long must open with explicit declaration:
- ACTOR_TERM: "Used by historical alchemists; examples: [list]"
- ANALYST_TERM: "Modern category; practitioners would not recognize this term"
- DISPUTED: "Historians disagree whether practitioners used this term or editors imposed it"

### 5. **Historiographical Ambiguity as Honest**
- When scholars disagree, surface it. Don't hide it in prose.
- When date/authorship is uncertain, say so. Use `confidence: MEDIUM/LOW`.
- When a concept's meaning shifted across time, show the shifts.

### 6. **Integration of the Embodied**
Eventually, integrate:
- Material properties (what Pamela Smith calls "artisanal epistemology")
- Visual sources (emblem plates, manuscript illuminations)
- Musical references (when known)
- Spatial/geographic context (not just abstract concepts)

### 7. **Polyvalent Symbolism Honored**
Refuse reductionism. A symbol works on multiple levels *simultaneously*. Show this structure explicitly.

---

## Red Flags (What NOT to Do)

Based on reading across all three projects, these violate your methodology:

1. ❌ **Flattening multi-register meaning**: Saying "X really means Y" when it means Y *and* Z *and* W
2. ❌ **Ignoring transmission**: Treating ideas as static instead of showing how they traveled and were reinterpreted
3. ❌ **Collapsing actor/analyst**: Using modern category names as if practitioners used them
4. ❌ **Lack of source citation**: Claims without traceable sources
5. ❌ **False unity**: Defining "alchemy" or "Hermeticism" as monolithic when they're contested
6. ❌ **Ignoring material reality**: Writing about distillation without mentioning glass vessels, heat damage, vapor toxicity
7. ❌ **Privileging text over other modalities**: Treating images, music, spatial arrangement as secondary
8. ❌ **Hiding disagreement**: Not surfacing historiographical disputes
9. ❌ **Reductive symbolism**: Saying a lion "represents" mercury, implying that's its only meaning
10. ❌ **Claiming originality for compilations**: Treating synthesis as mere copying rather than genuine intellectual work

---

## Next Actions for ALCHEMYTIMELINEMAP

1. **Update STYLEGUIDE.md** (already done in SCHOLARLYPROFILE.md round 1) with emphasis on:
   - Multi-register definitions
   - Material grounding
   - Transmission chains
   - Actor/analyst distinction
   - **Add:** Examples showing polyvalent symbolism

2. **Update ONTOLOGY.md** to add:
   - `registers` JSON field to concepts table
   - `transmission_chain` and `scholarly_disagreement` to persons/texts
   - Enums for ACTOR_TERM, ANALYST_TERM, DISPUTED_ACTOR_TERM
   - `material_grounding` field for persons/texts

3. **Create MULTIREGISTER_EXAMPLES.md** showing:
   - How one concept works across alchemical/medical/spiritual/cosmological registers
   - How transmission changes meaning (example: distillation in Zosimos vs. Jabir vs. Paracelsus)
   - How symbols carry multiple meanings simultaneously

4. **Seed initial entries** using Claudiens data:
   - Core concepts (nigredo, albedo, coniunctio, distillation, calcination)
   - Key persons (Zosimos, Jabir, Al-Razi, Paracelsus, Ficino, Pico)
   - Primary texts (Tabula Smaragdina, Turba, Rosarium, Summa Perfectionis)
   - With full multi-register definitions, transmission chains, scholarly disagreement where relevant

5. **Plan Phase 2 integration** with ludic/spatial/visual elements:
   - Link timeline events to alchemical furniture/materials
   - Embed emblem images where available
   - Note musical/rhythmic patterns where known
   - Flag where player could "enact" operations in future gamified version

---

## The Deeper Pattern

Across Claudiens, AlchemyBeatEmUp, and EmeraldTablet, you are asking the same question in three languages:

**How does knowledge actually live?**

Not: How do we package knowledge?
Not: How do we present knowledge?

But: How is knowledge *embodied*, *transmitted*, *transformed* when it moves across contexts?

- In Claudiens: Knowledge lives in the intricate weaving of text, image, music, and symbol. Breaking any thread weakens the whole.
- In AlchemyBeatEmUp: Knowledge lives in the body's encounter with material reality. You don't *know* that steam scalds until your character's token turns green.
- In EmeraldTablet: Knowledge lives in relational webs. You don't understand Hermeticism by reading one text; you understand it by tracing how it was read, mistranslated, absorbed, transformed across time and space.

ALCHEMYTIMELINEMAP should ask the same question: How does alchemical knowledge live *as it unfolds across time and space*?

Not as a static timeline (though that's the form). But as a *living network* where ideas propagate, transform, inspire, challenge, and reshape.

---

*Profile generated from 51 emblems, 18 scholars, 128 dictionary terms, ~50 game assets, 300+ Hermetic texts, and 1.45M user prompts. Cross-referenced with promptarchaeology queries on redirects, obsessions, and scholarly frameworks.*
