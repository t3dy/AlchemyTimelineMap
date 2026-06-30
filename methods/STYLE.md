# STYLE — the consolidated style authority (entry point)

Style is split across many files; this is the map. For prose, the binding specs are the
`STANDARD_*.md` files. For visual/cartographic style, see the map framework.

## Prose & content
| Content type | Binding spec |
|--------------|--------------|
| Person biography | `STANDARD_PERSON_BIOGRAPHIES.md` |
| Timeline event | `STANDARD_TIMELINE_EVENTS.md` |
| Text description | `STANDARD_TEXT_DESCRIPTIONS.md` |
| Concept definition | `STANDARD_CONCEPT_DEFINITIONS.md` |
| General prose principles | `STYLEGUIDE_CONSOLIDATED.md` (comprehensive source) |

Core prose rules: provenance in-line; actor/analyst marked; no transmutation
endorsement; no markdown artifacts in HTML; DGWE bibliography format.

## Provenance & metadata style (applies everywhere)
- `source` = "Author, *Work* (Year)" or a URL + access date for tertiary facts.
- `confidence` ∈ {HIGH, MEDIUM, LOW}; `review_status` defaults to `DRAFT` for new data.
- Evidence vocabulary (itinerary/relations): `attested` | `approximate` | `inferred`;
  relations also carry `survives` (does documentary evidence exist).

## Visual / cartographic style
For maps, journeys, and networks, the binding style guide is
`../MAPRESEARCH/research/MAPTYPES_FRAMEWORK.md`. Key conventions:
- **line style = evidence** (solid attested / dashed inferred); **opacity = confidence**;
  **colour = category, never confidence**.
- Theme-to-type pairing: noir → journey · copperplate → network/lineage ·
  illuminated → patronage · atlas → neutral default.
- Every node/edge/stop carries a hoverable source; show a "what this map does NOT show"
  note.

## Known style-file sprawl (see FILE_AUTHORITY_MAP.md for the full audit)
`STYLEGUIDE.md`, `STYLEGUIDE_CONSOLIDATED.md`, `STYLE_GUIDE_ALCHEMISTS.md`,
`STYLE_GUIDE_SCHOLARS_AND_TEXTS.md` overlap. Canonical = `STYLEGUIDE_CONSOLIDATED.md`
+ the `STANDARD_*.md` set; the rest are superseded and slated for `archive/`.
