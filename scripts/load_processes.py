#!/usr/bin/env python3
"""
Idempotent loader for the `processes` table.

Loads the "Twelve Alchemical Processes" (mapped to the zodiac in the early-modern
correspondence tradition codified by Pernety, 1758) plus other major operations.

Each process carries:
  - a complete 3-6 sentence index-card description,
  - a full essay (Historical Development / Textual Tradition / Modern Scholarship),
  - a DGWE bibliography,
  - an optional link to an existing concepts row (concept_slug).

Provenance & accuracy notes (invariants #1-#3):
  * The zodiac-process correspondence is an attested early-modern cryptographic
    scheme: Dom Antoine-Joseph Pernety, *Dictionnaire mytho-hermetique* (1758),
    maps twelve operations to the twelve signs (Calcination-Aries ... Projection-
    Pisces).
  * Pernety's twelve are RELATED TO BUT DISTINCT FROM George Ripley's twelve
    "gates" in the *Compound of Alchemy* (1471). Ripley's gates are Calcination,
    Solution, Separation, Conjunction, Putrefaction, Congelation, Cibation,
    Sublimation, Fermentation, Exaltation, Multiplication, Projection. Pernety
    substitutes Fixation, Digestion and Distillation and drops Conjunction,
    Putrefaction, Cibation and Exaltation. The four Ripley gates Pernety omits
    are included here as non-canonical "other major processes."
  * Transmutation is reported only as historical belief; never endorsed.

Usage:
    python scripts/load_processes.py

Idempotent on `slug` (INSERT ... ON CONFLICT(slug) DO UPDATE).

Author: Claude
Date: 2026-06-29
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "alchemy_timeline.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    sequence_order INTEGER,
    is_canonical_twelve INTEGER NOT NULL DEFAULT 0,
    zodiac_sign TEXT CHECK(zodiac_sign IN (
        'ARIES','TAURUS','GEMINI','CANCER','LEO','VIRGO',
        'LIBRA','SCORPIO','SAGITTARIUS','CAPRICORN','AQUARIUS','PISCES'
    )),
    zodiac_glyph TEXT,
    short_description TEXT NOT NULL,
    essay_html TEXT,
    references_html TEXT,
    concept_slug TEXT,
    source_method TEXT NOT NULL CHECK(source_method IN ('MANUAL', 'AI_ASSISTED', 'SCHOLARSHIP_BASED')),
    review_status TEXT NOT NULL CHECK(review_status IN ('DRAFT', 'REVIEWED', 'VERIFIED')),
    confidence TEXT NOT NULL CHECK(confidence IN ('HIGH', 'MEDIUM', 'LOW')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (concept_slug) REFERENCES concepts(slug)
);
"""

ZODIAC_GLYPHS = {
    "ARIES": "♈", "TAURUS": "♉", "GEMINI": "♊", "CANCER": "♋",
    "LEO": "♌", "VIRGO": "♍", "LIBRA": "♎", "SCORPIO": "♏",
    "SAGITTARIUS": "♐", "CAPRICORN": "♑", "AQUARIUS": "♒", "PISCES": "♓",
}

# ── Shared bibliography building blocks (DGWE format) ──────────────────────────
REF_PERNETY = "Pernety, Antoine-Joseph. <i>Dictionnaire mytho-hermetique</i>. Bauche, 1758."
REF_RIPLEY = "Ripley, George. <i>The Compound of Alchymy, or The Twelve Gates</i>. 1471."
REF_PRINCIPE = "Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013."
REF_NEWMAN_ATOMS = "Newman, William R. <i>Atoms and Alchemy: Chymistry and the Transformation of Matter</i>. University of Chicago Press, 2006."
REF_NEWMAN_SUMMA = "Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber: A Critical Edition, Translation and Study</i>. Brill, 1991."
REF_NP_FIRE = "Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002."
REF_RAMPLING = "Rampling, Jennifer M. <i>The Experimental Fire: Inventing English Alchemy, 1300-1700</i>. University of Chicago Press, 2020."
REF_ABRAHAM = "Abraham, Lyndy. <i>A Dictionary of Alchemical Imagery</i>. Cambridge University Press, 1998."
REF_LINDEN = "Linden, Stanton J. <i>The Alchemy Reader: From Hermes Trismegistus to Isaac Newton</i>. Cambridge University Press, 2003."
REF_HOLMYARD = "Holmyard, Eric John. <i>Alchemy</i>. Penguin, 1957."
REF_MULTHAUF = "Multhauf, Robert P. <i>The Origins of Chemistry</i>. Oldbourne, 1966."
REF_MORAN = "Moran, Bruce T. <i>Distilling Knowledge: Alchemy, Chemistry, and the Scientific Revolution</i>. Harvard University Press, 2005."
REF_HANEGRAAFF = "Hanegraaff, Wouter J. <i>Esotericism and the Academy: Rejected Knowledge in Western Culture</i>. Cambridge University Press, 2012."
REF_NUMMEDAL = "Nummedal, Tara. <i>Alchemy and Authority in the Holy Roman Empire</i>. University of Chicago Press, 2007."
REF_PRINCIPE_ADEPT = "Principe, Lawrence M. <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i>. Princeton University Press, 1998."


def essay(historical, textual, modern):
    """Assemble a full essay from three section blocks (each a string of <p>...)."""
    return (
        "<h3>Historical Development</h3>" + historical +
        "<h3>Textual Tradition</h3>" + textual +
        "<h3>Modern Scholarship</h3>" + modern
    )


def refs(*items):
    return "<ul>" + "".join(f"<li>{r}</li>" for r in items) + "</ul>"


# ── The twelve zodiac-mapped operations (Pernety's order) + major extras ───────
PROCESSES = [
    {
        "slug": "calcination",
        "name": "Calcination",
        "sequence_order": 1,
        "is_canonical_twelve": 1,
        "zodiac_sign": "ARIES",
        "concept_slug": "calcination",
        "confidence": "HIGH",
        "short_description": (
            "Calcination is the reduction of a substance to a dry, friable powder or 'ash' by intense, "
            "sustained heat, driving off moisture and volatile matter and leaving a <i>calx</i> (typically a "
            "metal oxide). Practitioners treated it as the opening operation that breaks down the gross body of a "
            "metal so that its purer principles may be released. In the early-modern correspondence scheme of "
            "Pernety (1758) it stands first and is keyed to Aries, the fiery sign that opens the zodiacal year. The "
            "operation has firm laboratory reality: roasting ores and metals to oxides was a routine metallurgical "
            "and assaying technique long before it became an alchemical 'gate.'"
        ),
        "essay": essay(
            "<p>Calcination by fire is among the oldest recorded chemical operations, rooted in the metallurgical "
            "roasting of ores and the production of lime and metal oxides. Greco-Egyptian and Arabic practitioners "
            "described reducing metals to a powdery <i>calx</i>, and Latin authors made calcination the first of the "
            "staged operations of the <i>magnum opus</i>. Its placement at the head of nearly every sequence reflects "
            "a craft logic shared by metalworkers and alchemists alike: the body must be broken and opened before it "
            "can be purified and recombined.</p>"
            "<p>The pairing of calcination with Aries belongs to a later, specifically cryptographic tradition. In "
            "his <i>Dictionnaire mytho-hermetique</i> (1758) Dom Antoine-Joseph Pernety keyed each of twelve "
            "operations to a zodiac sign, beginning with Calcination under Aries. This correspondence is a system of "
            "concealment and mnemonics, not a claim that the operation was governed by the stars.</p>",
            "<p>Calcination appears throughout the corpus, from the Jabirian writings and the Latin Pseudo-Geber's "
            "<i>Summa perfectionis</i> to George Ripley's <i>Compound of Alchemy</i> (1471), where it is the first of "
            "the twelve gates, and onward into early-modern chymistry. Robert Boyle and others treated calcination "
            "as a standard laboratory procedure whose products (calces) could be weighed and compared, a practice "
            "central to debates about whether matter gained or lost substance in the fire.</p>",
            "<p>Historians including Lawrence Principe and William Newman treat calcination as a clear case where "
            "alchemical terminology maps onto reproducible laboratory practice (oxidation and decomposition by heat), "
            "supporting an operational reading of the tradition rather than a purely spiritual one. The later weighing "
            "of calces fed directly into the eighteenth-century chemistry of combustion and the eventual overthrow of "
            "the phlogiston theory, making calcination a thread connecting alchemical craft to modern chemistry.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_NEWMAN_SUMMA, REF_NEWMAN_ATOMS, REF_PRINCIPE, REF_ABRAHAM),
    },
    {
        "slug": "congelation",
        "name": "Congelation (Coagulation)",
        "sequence_order": 2,
        "is_canonical_twelve": 1,
        "zodiac_sign": "TAURUS",
        "concept_slug": "coagulation",
        "confidence": "MEDIUM",
        "short_description": (
            "Congelation, often used interchangeably with coagulation, is the fixing of a fluid or volatile "
            "substance into a solid, stable body. It is the complementary counterpart to dissolution, embodying the "
            "alchemical rhythm of <i>solve et coagula</i> ('dissolve and coagulate'). Pernety's scheme assigns it to "
            "Taurus, an earthy sign suited to consolidation, and Ripley made 'albificative freezing' his sixth gate. "
            "In the laboratory the term covered crystallization, freezing, precipitation, and the setting of amalgams "
            "and salts."
        ),
        "essay": essay(
            "<p>Congelation names the passage from a liquid or vapour to a settled solid, the act of giving matter a "
            "durable body. Paired with solution, it forms one half of the maxim <i>solve et coagula</i> that "
            "structured much alchemical thinking about the rhythmic alternation of dissolution and fixation. The two "
            "operations were understood as a cycle that could be repeated to refine a substance step by step.</p>"
            "<p>Pernety assigns congelation to Taurus; Ripley, working in a different but overlapping scheme, made "
            "'albificative congelation' the sixth of his twelve gates. The two lists agree on this operation even "
            "where they diverge elsewhere, a reminder that the staged schemes drew on a shared pool of operations "
            "while ordering and naming them differently.</p>",
            "<p>The operation is treated across the Latin and vernacular corpus and is folded into the staged works "
            "of Ripley and his many readers. Lyndy Abraham's survey of alchemical imagery documents how congelation "
            "carried symbolic weight (the binding of spirit into body) alongside its concrete laboratory sense.</p>",
            "<p>Modern scholarship reads congelation/coagulation as spanning several distinct laboratory phenomena "
            "(crystallization, precipitation, amalgamation, solidification on cooling), a good illustration of how a "
            "single actor's term can map onto multiple modern chemical categories. Historians caution against "
            "collapsing the period vocabulary into any one modern process.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_ABRAHAM, REF_PRINCIPE, REF_NEWMAN_ATOMS),
    },
    {
        "slug": "fixation",
        "name": "Fixation",
        "sequence_order": 3,
        "is_canonical_twelve": 1,
        "zodiac_sign": "GEMINI",
        "concept_slug": None,
        "confidence": "MEDIUM",
        "short_description": (
            "Fixation is the operation that renders a volatile substance stable, so that it withstands fire without "
            "subliming or evaporating away. To 'fix the volatile' was a central aim, since a fixed body was thought "
            "able to endure transformation and to fix other substances in turn. Pernety assigns the operation to "
            "Gemini. Practically it described converting fugitive materials (volatile salts, mercury preparations, "
            "arsenical 'spirits') into heat-stable solids."
        ),
        "essay": essay(
            "<p>Fixation addresses one of the defining problems of premodern chemistry: making volatile matter endure "
            "fire. A 'fixed' body was prized because it resisted destruction and was held capable of imparting "
            "stability to other substances, a decisive step on the path to a perfected medicine or Stone. The "
            "language of 'fixing the volatile' and 'volatilizing the fixed' became a shorthand for the whole "
            "transformative project.</p>"
            "<p>Pernety places fixation under Gemini. Notably, fixation is not one of Ripley's twelve gates: it is "
            "among the operations Pernety's zodiacal scheme adds where Ripley had instead listed conjunction, "
            "putrefaction, cibation and exaltation. This divergence is a concrete sign that the two famous "
            "'twelve-operation' lists are related traditions rather than a single canon.</p>",
            "<p>The vocabulary of fixation pervades the corpus from the Arabic tradition through the Latin "
            "Pseudo-Geber, whose <i>Summa perfectionis</i> theorizes the stability of substances in corpuscular "
            "terms, and into early-modern chymistry. William Newman's edition and study of the <i>Summa</i> shows how "
            "carefully such operations were defined.</p>",
            "<p>Scholars note that 'fixation' maps onto real, observable changes in volatility and thermal stability, "
            "again revealing the operational substrate beneath alchemical vocabulary. They simultaneously caution "
            "against reading the eighteenth-century zodiacal scheme back into the practice of earlier centuries, where "
            "the operation existed without any fixed astrological key.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_NEWMAN_SUMMA, REF_NEWMAN_ATOMS, REF_PRINCIPE, REF_ABRAHAM),
    },
    {
        "slug": "solution",
        "name": "Solution (Dissolution)",
        "sequence_order": 4,
        "is_canonical_twelve": 1,
        "zodiac_sign": "CANCER",
        "concept_slug": "dissolution",
        "confidence": "HIGH",
        "short_description": (
            "Solution, or dissolution, is the reduction of a solid into a liquid, whether by water, acid, or a "
            "'philosophical' solvent. It is the complement of congelation in the <i>solve et coagula</i> cycle and "
            "was thought to return a body toward its first matter. Pernety assigns it to Cancer, a watery sign, and "
            "Ripley made 'secret dissolution' his second gate. The operation embraced everything from dissolving "
            "salts and metals in the strong mineral acids to the slow liquefaction of substances in gentle heat or "
            "corrosive waters."
        ),
        "essay": essay(
            "<p>Solution names the breaking-down of a solid body into a liquid state, conceptually returning matter "
            "toward an undifferentiated first matter from which it could be reformed. With congelation it expresses "
            "the foundational alternation of dissolving and fixing that organizes much alchemical theory and "
            "practice.</p>"
            "<p>The medieval Latin discovery and refinement of the strong mineral acids (nitric, hydrochloric, "
            "sulphuric, and the gold-dissolving <i>aqua regia</i>) gave dissolution dramatic new power. Pernety keys "
            "the operation to Cancer; Ripley had already made it his second gate, 'secret dissolution.' Here the two "
            "schemes coincide, both treating dissolution as an early and essential step.</p>",
            "<p>Dissolution is ubiquitous across the corpus, from the Arabic tradition through Pseudo-Geber and the "
            "vernacular treatises. The discovery of the mineral acids is documented in the works analyzed by Robert "
            "Multhauf and is central to the practical chymistry that William Newman and Lawrence Principe have "
            "reconstructed.</p>",
            "<p>Historians of chemistry highlight the medieval mineral acids as a turning point that made dissolution "
            "a precise and powerful analytical tool, central to assaying and to the eventual emergence of analytical "
            "chemistry. The capacity to dissolve and then recover metals quantitatively underwrote both alchemical "
            "ambition and sober metallurgical testing.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_MULTHAUF, REF_NEWMAN_ATOMS, REF_NP_FIRE, REF_ABRAHAM),
    },
    {
        "slug": "digestion",
        "name": "Digestion",
        "sequence_order": 5,
        "is_canonical_twelve": 1,
        "zodiac_sign": "LEO",
        "concept_slug": None,
        "confidence": "MEDIUM",
        "short_description": (
            "Digestion is the prolonged, gentle heating of a substance, often in a sealed vessel, to mature, soften, "
            "or 'concoct' it, by analogy with the body's digestion of food. It is an operation of nurture rather than "
            "violence, frequently carried out in a warm bath (<i>balneum mariae</i>), a dung-bed, or the steady-heat "
            "furnace called the athanor. Pernety assigns it to Leo, a sign of constant solar heat. The technique "
            "underlies many extractions, infusions, and the slow ripening of alchemical mixtures."
        ),
        "essay": essay(
            "<p>Digestion borrows its name and logic from physiology: as the stomach concocts food by gentle warmth, "
            "so the alchemist matures matter by patient, regulated heat. It is the operation of slow nurture, often "
            "lasting weeks or months, and it placed a premium on the control and maintenance of low, steady "
            "temperatures, one of the genuinely demanding skills of the premodern laboratory.</p>"
            "<p>Pernety assigns digestion to Leo. Like fixation and distillation, digestion is one of the operations "
            "Pernety's zodiacal list includes but Ripley's gates do not, underscoring that the two twelve-fold "
            "schemes are related yet distinct selections from a larger repertoire of operations.</p>",
            "<p>Steady-heat techniques (the <i>balneum mariae</i> named for Maria the Jewess, the dung-bed, and the "
            "self-feeding athanor furnace) are described from the Greco-Egyptian corpus onward and are essential to "
            "the staged works of the Latin and early-modern traditions. Treatises on distillation and on the "
            "quintessence give detailed instructions for maintaining digestive heat.</p>",
            "<p>Scholars emphasize the sophistication of premodern heat control, which projects such as Making and "
            "Knowing and historians like Bruce Moran have reconstructed and analyzed. Their work shows that "
            "'digestion' denoted genuine, repeatable thermal practice rather than vague metaphor, and that mastery of "
            "fire was itself a prized form of artisanal knowledge.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_MORAN, REF_PRINCIPE, REF_ABRAHAM, REF_HOLMYARD),
    },
    {
        "slug": "distillation",
        "name": "Distillation",
        "sequence_order": 6,
        "is_canonical_twelve": 1,
        "zodiac_sign": "VIRGO",
        "concept_slug": "distillation",
        "confidence": "HIGH",
        "short_description": (
            "Distillation is the separation and purification of a substance by vaporizing a liquid and condensing the "
            "vapour, drawing off the 'spirit' or essence from the gross residue. It was among the most prized and "
            "technically demanding operations, requiring the alembic and, later, increasingly elaborate glassware. "
            "Pernety assigns it to Virgo. Distillation produced alcohol (<i>aqua vitae</i>), the mineral acids, and "
            "essential oils, and was a genuine engine of chemical discovery from antiquity through the Scientific "
            "Revolution."
        ),
        "essay": essay(
            "<p>Distillation, the vaporization of a liquid and condensation of its vapour, let practitioners separate "
            "the volatile 'spirit' of a substance from its body. The refinement of distillation apparatus, from the "
            "simple alembic to multi-stage and continuous (circulatory) setups, drove much practical chemistry and "
            "made distillation the showcase operation of the alchemical laboratory.</p>"
            "<p>Pernety keys distillation to Virgo. It is one of the operations distinctive to his zodiacal list "
            "rather than to Ripley's gates, where the closely related work of subtilizing is gathered under "
            "sublimation. The prestige of distillation in early-modern Europe, fuelled by the medical and commercial "
            "value of distilled waters and spirits, helps explain its prominence in the later scheme.</p>",
            "<p>Distillation is central to the Greco-Egyptian corpus, where apparatus is attributed to Maria the "
            "Jewess, to the Arabic tradition, and to the medieval Latin production of <i>aqua vitae</i> and the "
            "mineral acids. Vernacular printed books such as Hieronymus Brunschwig's distillation manuals (1500, "
            "1512) carried the technique to a wide audience.</p>",
            "<p>Historians treat distillation as a paradigmatic case of cumulative chemical know-how: the isolation "
            "of alcohol and the mineral acids reshaped medicine and assaying, as Robert Multhauf and Bruce Moran "
            "document. Moran in particular uses distillation to trace the continuity between alchemy, chemistry, and "
            "the Scientific Revolution.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_MULTHAUF, REF_MORAN, REF_PRINCIPE, REF_HOLMYARD, REF_ABRAHAM),
    },
    {
        "slug": "sublimation",
        "name": "Sublimation",
        "sequence_order": 7,
        "is_canonical_twelve": 1,
        "zodiac_sign": "LIBRA",
        "concept_slug": "sublimation",
        "confidence": "HIGH",
        "short_description": (
            "Sublimation is the conversion of a solid directly into a vapour by heat, which then resolidifies on a "
            "cooler surface, leaving impurities behind. It was valued for purifying volatile solids such as sal "
            "ammoniac, sulphur, and mercuric compounds. Pernety assigns the operation to Libra, and Ripley made it "
            "his eighth gate. As a means of purification and of raising the 'subtle' part of a substance, sublimation "
            "was both an exact laboratory technique and a rich emblem of spiritual elevation."
        ),
        "essay": essay(
            "<p>Sublimation raises a solid directly into vapour and recondenses it as a purified solid, separating the "
            "subtle from the gross. It was a standard purification for substances such as sal ammoniac, sulphur, and "
            "mercuric compounds, and it doubled as a favourite emblem of refinement and ascent. Few operations so "
            "neatly joined a concrete procedure to a vivid symbolic meaning.</p>"
            "<p>Pernety assigns sublimation to Libra; Ripley made it the eighth of his twelve gates, 'the secret of "
            "subtlety.' Here, as with calcination, congelation, solution, separation, fermentation, multiplication "
            "and projection, the two schemes agree, marking sublimation as part of the shared operational core that "
            "both lists draw upon.</p>",
            "<p>The operation is described in detail in the Arabic and Pseudo-Geberian corpus, where the sublimation "
            "of salts and 'spirits' is fundamental to preparing reagents. William Newman's edition of the <i>Summa "
            "perfectionis</i> shows how precisely sublimation was specified, including the design of the vessels and "
            "the regulation of heat.</p>",
            "<p>Newman's broader work on Pseudo-Geber and corpuscular matter theory uses such operations to argue "
            "that medieval alchemy rested on exact, repeatable laboratory procedure and a sophisticated theory of "
            "matter, countering older views that dismissed it as mere mysticism.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_NEWMAN_SUMMA, REF_NEWMAN_ATOMS, REF_PRINCIPE, REF_ABRAHAM),
    },
    {
        "slug": "separation",
        "name": "Separation",
        "sequence_order": 8,
        "is_canonical_twelve": 1,
        "zodiac_sign": "SCORPIO",
        "concept_slug": None,
        "confidence": "MEDIUM",
        "short_description": (
            "Separation is the dividing of a mixed substance into its distinct components, parting the pure from the "
            "impure and the subtle from the gross. It underlies many other operations and is closely tied to the "
            "spagyric motto 'separate, and join together again.' Pernety assigns it to Scorpio, and Ripley made "
            "'elemental separation' his third gate. In practice it embraced filtration, decantation, the collecting "
            "of distilled fractions, and the parting of metals in assaying."
        ),
        "essay": essay(
            "<p>Separation is the operation of division: parting a body into its constituents so that the pure may be "
            "retained and the impure discarded. It is foundational to the spagyric program associated with "
            "Paracelsian medicine, whose very name was glossed from Greek roots meaning to separate and to recombine. "
            "Separation thus sat at the heart of an analytical impulse that ran through alchemy.</p>"
            "<p>Pernety keys separation to Scorpio; Ripley had made 'our elemental separation' his third gate. In "
            "assaying, separation corresponds to the parting of gold and silver by acids or cementation, a precise "
            "and economically vital procedure that connected alchemical theory to the work of mints and "
            "metallurgists.</p>",
            "<p>Separation pervades the corpus and is treated by the Paracelsians as the key to isolating the active "
            "virtues of substances for medicine. Stanton Linden's anthology gathers many texts in which separation "
            "carries both technical and allegorical meaning.</p>",
            "<p>Scholars of Paracelsian and spagyric medicine, including Wouter Hanegraaff and William Newman, situate "
            "separation within the broader analytical project that later informed chemical analysis proper. They "
            "stress that the operation's spiritual readings coexisted with, rather than replaced, its hands-on "
            "laboratory use.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_HANEGRAAFF, REF_LINDEN, REF_PRINCIPE, REF_ABRAHAM),
    },
    {
        "slug": "ceration",
        "name": "Ceration",
        "sequence_order": 9,
        "is_canonical_twelve": 1,
        "zodiac_sign": "SAGITTARIUS",
        "concept_slug": None,
        "confidence": "MEDIUM",
        "short_description": (
            "Ceration is the softening of a hard, dry substance into a waxy, fusible consistency, typically by "
            "repeatedly moistening (imbibing) and gently heating it; the name derives from <i>cera</i>, wax. It "
            "prepares a matter to melt and flow rather than burn or crumble. Pernety assigns the operation to "
            "Sagittarius. Ripley treats ceration together with exaltation in his tenth gate, a small but telling "
            "difference between the two twelve-fold schemes."
        ),
        "essay": essay(
            "<p>Ceration brings a dry, refractory substance to a soft, waxy state in which it can fuse and flow. The "
            "alchemist achieves it by alternately imbibing the matter with a liquid and gently heating it until it "
            "becomes malleable, like wax, hence the name from Latin <i>cera</i>. The operation expresses the close "
            "attention premodern practitioners paid to the consistency and workability of matter.</p>"
            "<p>Pernety's 1758 table assigns ceration to Sagittarius. In Ripley's <i>Compound</i> ceration is not an "
            "independent gate but is joined with exaltation in the tenth gate; some later lists substitute a fiery "
            "operation here. These variations show that the sequences were never fully standardized, even among the "
            "most influential authors.</p>",
            "<p>Ceration appears among the staged operations in the Latin tradition and in the gate-schemes of the "
            "fifteenth century. Lyndy Abraham's dictionary records its technical sense and its symbolic associations "
            "with softening and union.</p>",
            "<p>Modern commentators use ceration to illustrate how finely premodern practitioners distinguished "
            "consistencies and states of matter, a vocabulary that does not map neatly onto any single modern "
            "process and that rewards careful, non-anachronistic reading.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_ABRAHAM, REF_PRINCIPE, REF_HOLMYARD),
    },
    {
        "slug": "fermentation",
        "name": "Fermentation",
        "sequence_order": 10,
        "is_canonical_twelve": 1,
        "zodiac_sign": "CAPRICORN",
        "concept_slug": "fermentation",
        "confidence": "MEDIUM",
        "short_description": (
            "Fermentation is the enlivening or transformation of a substance by the addition of a 'ferment,' on the "
            "model of leaven raising bread or yeast working in must. In the work of the Stone it often denoted the "
            "imparting of a new quality or 'tincture' to the matured matter, frequently by joining it with gold or "
            "silver. Pernety assigns it to Capricorn, and Ripley made it his ninth gate. The term drew directly on "
            "the visible, reproducible phenomena of brewing and bread-making."
        ),
        "essay": essay(
            "<p>Fermentation names transformation worked from within by a small added agent, the ferment or leaven, by "
            "analogy with bread and wine. In the alchemical work it frequently signified the stage at which the "
            "matured matter received its specific virtue or tincture, often through union with a noble metal that was "
            "said to 'ferment' the whole.</p>"
            "<p>Pernety keys fermentation to Capricorn; Ripley made it the ninth of his twelve gates. The two schemes "
            "agree on this operation, and both treat it as a late, qualifying step rather than an early breaking-down, "
            "reflecting a shared sense of where in the work the imparting of virtue belonged.</p>",
            "<p>The metaphor of leaven is ancient and recurs throughout the corpus; fermentation is one of Ripley's "
            "gates and a staple of the English tradition that grew from him, traced in detail by Jennifer Rampling. "
            "Lyndy Abraham documents the term's double life as craft practice and alchemical symbol.</p>",
            "<p>Historians note the productive ambiguity of the term, which bridged everyday craft (brewing, baking) "
            "and alchemical theory and was only much later reconceived in biological and chemical terms. Its history "
            "is a case study in how a single word can migrate across kitchen, laboratory, and philosophy.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_RAMPLING, REF_PRINCIPE, REF_ABRAHAM),
    },
    {
        "slug": "multiplication",
        "name": "Multiplication",
        "sequence_order": 11,
        "is_canonical_twelve": 1,
        "zodiac_sign": "AQUARIUS",
        "concept_slug": None,
        "confidence": "MEDIUM",
        "short_description": (
            "Multiplication is the operation by which the perfected medicine or Stone was supposedly increased in "
            "quantity and potency, each repetition augmenting its transformative power. It is a late stage in the "
            "work, presupposing that the Stone has already been achieved. Pernety assigns it to Aquarius, and Ripley "
            "made it his eleventh gate. This site reports multiplication as a historical belief about the Stone; it "
            "makes no claim that any such augmentation occurred."
        ),
        "essay": essay(
            "<p>Multiplication is the augmentation of the finished Stone, both in mass and in strength, by repeating "
            "earlier operations upon it. It is among the final stages, presupposing a completed <i>magnum opus</i>, "
            "and it expresses the striking claim that a perfected agent could propagate its own virtue, transmuting "
            "ever larger quantities of base metal with each cycle.</p>"
            "<p>Pernety keys multiplication to Aquarius; Ripley made it the eleventh of his twelve gates, 'our "
            "marvellous multiplication.' Both schemes place it just before projection, reflecting a shared narrative "
            "in which the adept first perfects, then increases, and only finally projects the Stone.</p>",
            "<p>Multiplication figures prominently in Ripley's gates and in the English alchemical tradition that "
            "followed. Jennifer Rampling's research shows how such claims circulated in manuscripts and shaped "
            "patronage relationships, while Tara Nummedal documents how promises of multiplication featured in courtly "
            "contracts and, sometimes, in fraud trials.</p>",
            "<p>Historians report multiplication as a period belief and a rhetorical-economic argument rather than an "
            "achieved fact. This portal follows that approach: the doctrine is documented as history, with no "
            "endorsement of the underlying claim that base metal can be transmuted or a medicine endlessly "
            "augmented.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_RAMPLING, REF_NUMMEDAL, REF_ABRAHAM),
    },
    {
        "slug": "projection",
        "name": "Projection",
        "sequence_order": 12,
        "is_canonical_twelve": 1,
        "zodiac_sign": "PISCES",
        "concept_slug": "projection",
        "confidence": "MEDIUM",
        "short_description": (
            "Projection is the culminating operation in which a small quantity of the finished Stone or 'powder of "
            "projection' was cast upon a molten base metal in order, it was claimed, to transmute it into gold or "
            "silver. It is the final gate, the moment toward which the entire work was directed. Pernety assigns it to "
            "Pisces, the last sign of the zodiac, and Ripley made it his twelfth gate. This site reports projection as "
            "the historical goal claimed by practitioners; it endorses no claim that transmutation ever succeeded."
        ),
        "essay": essay(
            "<p>Projection is the climactic act of the work: casting a minute portion of the Stone onto a large mass "
            "of molten base metal in the expectation of transmuting it. Its position as the twelfth and final stage "
            "mirrors Pisces as the final sign, the completion of the cycle, and gives the whole sequence a satisfying "
            "narrative shape from first calcination to final projection.</p>"
            "<p>Pernety keys projection to Pisces; Ripley made it the twelfth and last of his gates. The two schemes "
            "agree on the endpoint even though they differ in the middle, suggesting that the broad arc of the work "
            "(open the body, purify, unite, perfect, increase, project) was more stable than the exact list of "
            "operations.</p>",
            "<p>Accounts of projection recur across the late-medieval and early-modern corpus and in the many "
            "transmutation narratives of the period, including the widely reported demonstrations that circulated in "
            "print and at court. Such narratives are gathered and contextualized in Stanton Linden's anthology.</p>",
            "<p>Historians such as Lawrence Principe analyze transmutation narratives critically, as period testimony "
            "shaped by patronage, credibility and rhetoric, while Tara Nummedal situates them within the economic and "
            "legal world of the courts. Following that scholarship, this portal documents projection as a historical "
            "claim and goal, never as an achieved fact.</p>",
        ),
        "refs": refs(REF_PERNETY, REF_RIPLEY, REF_PRINCIPE, REF_NUMMEDAL, REF_LINDEN),
    },
    # ── Other major processes (Ripley gates outside Pernety's zodiacal twelve, plus circulation) ──
    {
        "slug": "putrefaction",
        "name": "Putrefaction",
        "sequence_order": 13,
        "is_canonical_twelve": 0,
        "zodiac_sign": None,
        "concept_slug": "putrefaction",
        "confidence": "MEDIUM",
        "short_description": (
            "Putrefaction is the rotting or decomposition of matter, classically signalled by a blackening (the "
            "<i>nigredo</i>), regarded as a necessary death before regeneration. It is among the most emblematically "
            "charged operations, expressing the principle that nothing is reborn unless it first decays. It is the "
            "fifth of Ripley's twelve gates but is absent from Pernety's strict zodiacal list, which is why it appears "
            "here among the major non-canonical processes. In practice it covered controlled decay, maceration, and "
            "slow corruption in gentle heat."
        ),
        "essay": essay(
            "<p>Putrefaction is the operation of decay: the deliberate corruption of matter, frequently marked by the "
            "blackening called the <i>nigredo</i> and understood as the death that must precede regeneration. It "
            "carried exceptional symbolic weight as the turning point of the work, the low point from which the "
            "whitening and reddening would follow.</p>"
            "<p>Putrefaction is the fifth of Ripley's twelve gates, yet it is one of the four Ripley operations "
            "(with conjunction, cibation and exaltation) that Pernety's zodiacal twelve drops in favour of fixation, "
            "digestion and distillation. Its prominence in Ripley but absence from Pernety's signs is a clear example "
            "of how the two famous schemes diverge.</p>",
            "<p>Putrefaction is treated throughout the corpus and is central to the colour-sequence (black, white, "
            "red) of the <i>magnum opus</i>. Stanton Linden's anthology and Lyndy Abraham's dictionary document its "
            "dense imagery, from graves and ravens to dissolving kings.</p>",
            "<p>Scholars of alchemical imagery emphasize the symbolic richness of putrefaction, while operational "
            "historians connect it to genuine practices of controlled decomposition and maceration. The two readings "
            "are complementary: the same blackening that carried allegorical meaning was also a real, observed "
            "laboratory phenomenon.</p>",
        ),
        "refs": refs(REF_RIPLEY, REF_ABRAHAM, REF_LINDEN, REF_PRINCIPE),
    },
    {
        "slug": "conjunction",
        "name": "Conjunction",
        "sequence_order": 14,
        "is_canonical_twelve": 0,
        "zodiac_sign": None,
        "concept_slug": "conjunction",
        "confidence": "MEDIUM",
        "short_description": (
            "Conjunction is the union of opposed principles, classically the 'chymical wedding' of a masculine sulphur "
            "and a feminine mercury, or of fixed and volatile, into a single body. It typically follows separation "
            "and purification, joining what has been refined. It is the fourth of Ripley's twelve gates ('matrimonial "
            "conjunction') but does not appear in Pernety's zodiacal twelve. Practically it denoted the combining and "
            "amalgamation of prepared substances."
        ),
        "essay": essay(
            "<p>Conjunction is the operation of union, the joining of contraries (sulphur and mercury, fixed and "
            "volatile, male and female, sun and moon) into one body. It typically follows separation, recombining "
            "what has been purified, and it is among the most richly allegorized of all the operations, the "
            "centrepiece of the 'chymical wedding' imagery.</p>"
            "<p>Conjunction is the fourth of Ripley's twelve gates, his 'matrimonial conjunction.' It is one of the "
            "Ripley operations Pernety's zodiacal scheme omits, and so it sits here among the major extra processes "
            "rather than under a zodiac sign, another marker of the difference between the two twelve-fold lists.</p>",
            "<p>Conjunction is depicted vividly in emblem books such as the <i>Rosarium philosophorum</i> and Michael "
            "Maier's <i>Atalanta fugiens</i> (1617), whose images of royal marriage encode both laboratory operation "
            "and philosophical meaning. Stanton Linden and Lyndy Abraham trace this imagery across the tradition.</p>",
            "<p>Scholars of emblematic alchemy read the chymical wedding both as coded laboratory instruction and as a "
            "vehicle for philosophical, psychological and theological meaning. Negotiating that duality, without "
            "collapsing the operation into either pure chemistry or pure symbol, is central to current "
            "historiography.</p>",
        ),
        "refs": refs(REF_RIPLEY, REF_ABRAHAM, REF_LINDEN, REF_PRINCIPE),
    },
    {
        "slug": "circulation",
        "name": "Circulation",
        "sequence_order": 15,
        "is_canonical_twelve": 0,
        "zodiac_sign": None,
        "concept_slug": "circulation",
        "confidence": "MEDIUM",
        "short_description": (
            "Circulation is the repeated, continuous distillation of a liquid within a closed vessel, so that vapour "
            "rises and condensate falls back again in an endless cycle, refining the substance with each pass. It was "
            "carried out in a special double vessel, the pelican, whose side-arms return the condensate to the body. "
            "It belongs to neither Pernety's zodiacal twelve nor Ripley's gates, but it was a standard and important "
            "laboratory operation. It aimed to exalt and subtilize the matter through unceasing motion."
        ),
        "essay": essay(
            "<p>Circulation is continuous internal distillation: in a sealed vessel, vapour rises, condenses, and "
            "returns to the body to rise again, refining the substance through endless repetition. The pelican, with "
            "its returning side-arms, was the apparatus emblematic of the operation, and the closed cycle it enabled "
            "was prized for producing especially pure and 'exalted' substances.</p>"
            "<p>Unlike the operations in the two twelve-fold schemes, circulation is not a numbered gate or zodiacal "
            "station; it is a general technique that supports many of them. It is included here as a major additional "
            "process because of its central role in the preparation of quintessences and spirits.</p>",
            "<p>Circulation is described across the medieval and early-modern technical literature on distillation, "
            "from the treatises on the quintessence to the printed distillation manuals. Its apparatus is documented "
            "by historians of laboratory practice and figures in the work of Bruce Moran on distilling knowledge.</p>",
            "<p>Historians of apparatus and technique treat circulation as evidence of sophisticated closed-system "
            "design, an important step toward controlled, reproducible chemical processing and toward the reflux "
            "methods of later chemistry.</p>",
        ),
        "refs": refs(REF_ABRAHAM, REF_MORAN, REF_PRINCIPE, REF_HOLMYARD),
    },
    {
        "slug": "cibation",
        "name": "Cibation",
        "sequence_order": 16,
        "is_canonical_twelve": 0,
        "zodiac_sign": None,
        "concept_slug": None,
        "confidence": "MEDIUM",
        "short_description": (
            "Cibation is the 'feeding' of the work: the measured addition of fresh matter or moisture to the "
            "developing substance, as one feeds an infant, to sustain and nourish it through the operation. The name "
            "comes from Latin <i>cibus</i> (food). It is the seventh of Ripley's twelve gates and is distinctive to "
            "the English alchemical tradition; it does not appear in Pernety's zodiacal list."
        ),
        "essay": essay(
            "<p>Cibation is the careful feeding of the work, replenishing the matter with new material or liquid in "
            "measured portions, on the nurturing analogy of feeding a child. The aim is to sustain the process "
            "without drowning or starving it, a matter of judgement and timing as much as of recipe.</p>"
            "<p>Cibation is best known as the seventh of the twelve gates in George Ripley's <i>Compound of "
            "Alchemy</i> (1471) and is characteristic of the English tradition that grew from it. It is one of the "
            "Ripley gates absent from Pernety's zodiacal twelve, and so it appears here among the major extra "
            "operations.</p>",
            "<p>The term and its imagery are documented in Lyndy Abraham's dictionary, and the gate itself is traced "
            "through its many English readers and adaptors. Ripley's scheme, including cibation, was copied, glossed "
            "and reworked in manuscript for more than two centuries.</p>",
            "<p>Jennifer Rampling's study of English alchemy reconstructs how Ripley's gate-scheme was read and "
            "practised across three centuries, making cibation a useful case in the historiography of vernacular "
            "alchemy and of how practitioners turned cryptic verse into bench procedure.</p>",
        ),
        "refs": refs(REF_RIPLEY, REF_RAMPLING, REF_ABRAHAM),
    },
    {
        "slug": "exaltation",
        "name": "Exaltation",
        "sequence_order": 17,
        "is_canonical_twelve": 0,
        "zodiac_sign": None,
        "concept_slug": None,
        "confidence": "MEDIUM",
        "short_description": (
            "Exaltation is the raising of a substance to a higher degree of purity, power, or perfection, an "
            "intensification of its virtues beyond its ordinary state. The term carries both a chemical sense "
            "(heightened potency) and a spiritual resonance (elevation). It is the tenth of Ripley's twelve gates, "
            "where it is paired with ceration, but it does not feature in Pernety's strict zodiacal list."
        ),
        "essay": essay(
            "<p>Exaltation denotes elevation: bringing a substance to a higher state of purity and potency than it "
            "naturally possesses. The word fuses a chemical meaning (concentration of virtue) with a spiritual one "
            "(raising up), and so sits at the meeting point of practice and allegory that characterizes much "
            "alchemical language.</p>"
            "<p>Exaltation is the tenth of Ripley's twelve gates, where it is joined with ceration. Like conjunction, "
            "putrefaction and cibation, it is a Ripley operation that Pernety's zodiacal twelve omits, and it is "
            "therefore presented here among the major additional processes rather than under a zodiac sign.</p>",
            "<p>Exaltation recurs in the English and Continental traditions that drew on Ripley, and its imagery of "
            "ascent and heightening is catalogued in Lyndy Abraham's dictionary and illustrated in Stanton Linden's "
            "anthology of sources.</p>",
            "<p>Studies of alchemical language emphasize how terms like exaltation operated on multiple registers at "
            "once, a feature modern scholarship is careful to parse rather than flatten into a single meaning. "
            "Reading such words demands attention to context, since the same term could name a bench operation or a "
            "philosophical aspiration.</p>",
        ),
        "refs": refs(REF_RIPLEY, REF_RAMPLING, REF_ABRAHAM, REF_LINDEN),
    },
]


def load():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)

    # Validate concept_slug references exist (invariant: all entity links must exist).
    existing_concepts = {r[0] for r in cur.execute("SELECT slug FROM concepts")}
    missing = [p["concept_slug"] for p in PROCESSES
               if p["concept_slug"] and p["concept_slug"] not in existing_concepts]
    if missing:
        raise SystemExit(f"[ERROR] concept_slug references not found in concepts table: {missing}")

    upsert = """
    INSERT INTO processes (
        slug, name, sequence_order, is_canonical_twelve, zodiac_sign, zodiac_glyph,
        short_description, essay_html, references_html, concept_slug,
        source_method, review_status, confidence
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(slug) DO UPDATE SET
        name=excluded.name,
        sequence_order=excluded.sequence_order,
        is_canonical_twelve=excluded.is_canonical_twelve,
        zodiac_sign=excluded.zodiac_sign,
        zodiac_glyph=excluded.zodiac_glyph,
        short_description=excluded.short_description,
        essay_html=excluded.essay_html,
        references_html=excluded.references_html,
        concept_slug=excluded.concept_slug,
        source_method=excluded.source_method,
        review_status=excluded.review_status,
        confidence=excluded.confidence
    """

    for p in PROCESSES:
        zsign = p["zodiac_sign"]
        glyph = ZODIAC_GLYPHS.get(zsign) if zsign else None
        cur.execute(upsert, (
            p["slug"], p["name"], p["sequence_order"], p["is_canonical_twelve"],
            zsign, glyph, p["short_description"], p["essay"], p["refs"], p["concept_slug"],
            "AI_ASSISTED", "REVIEWED", p.get("confidence", "MEDIUM"),
        ))

    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM processes").fetchone()[0]
    canonical = cur.execute("SELECT COUNT(*) FROM processes WHERE is_canonical_twelve=1").fetchone()[0]
    conn.close()
    print(f"[OK] processes table loaded: {count} rows ({canonical} canonical twelve, {count - canonical} extras)")


if __name__ == "__main__":
    load()
