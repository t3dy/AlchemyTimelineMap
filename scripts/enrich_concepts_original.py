#!/usr/bin/env python3
"""enrich_concepts_original.py — Expand original 18 concepts to full definition_long."""
import sqlite3

DB = 'db/alchemy_timeline.db'

ENRICHMENTS = {
'calcination': {
'definition_long': """<p>Calcination (Latin: <i>calcinatio</i>; also called the nigredo or "blackening" in alchemical color symbolism) was one of the primary alchemical operations in which a substance was subjected to intense, prolonged heat until it was reduced to ash or a black, charred residue. This is an ACTOR_TERM — historical practitioners explicitly performed and named this operation. The term appears across alchemical literature from the Greek tradition through medieval Latin and early modern practice. Calcination was understood not merely as destruction but as a necessary preliminary to reconstitution: the original form of the substance was broken down, freeing the matter to receive a new, more perfect form. [LINK:george-ripley]'s twelve-gate poem placed Calcination as the first gate, the necessary beginning of the alchemical work.</p>

<h2>Historical Usage and Material Grounding</h2>
<p>The operation was grounded in observable chemical phenomena. When organic materials — wood, plants, animal matter — were burned in fire, they were reduced to ash. When metals or minerals were subjected to intense heat (in furnaces, crucibles, or over open flame), they underwent visible transformations: colors shifted (from bright metal to black oxides to reddish or gray residues), textures changed (from solid to powder or glass), and the material appeared to be destroyed. Practitioners recognized these changes as physically real and experientially meaningful. The sensory dimensions were important: the intense heat, the acrid smell of burning, the visual darkness of the blackened matter, the possibility of dangerous burns or explosive reactions. These sensory and embodied dimensions grounded calcination in material reality rather than pure abstraction.</p>

<p>In the sulphur-mercury theory of metallic composition, calcination was understood as a way to access the underlying components: burning away the metallic form to reveal the sulphur and mercury elements within. The black residue of calcined metal was theoretically closer to prima materia — undifferentiated matter — than the original metal, and therefore more amenable to reconstitution in a new form. Different substances required different intensities and durations of heat: plant matter calcined quickly to ash; minerals required sustained, intense heat; metals demanded specialized furnaces and long periods of exposure.</p>

<h2>Scholarly Significance</h2>
<p>William Newman demonstrated that calcination operations correspond to genuine chemical phenomena — the production of metal oxides, char, and ash through oxidation and thermal decomposition — in *The Summa Perfectionis* (1991) pp.110–135. Lawrence Principe's laboratory replication of alchemical procedures has shown that calcination, when performed as described in historical texts, produces reproducible, observable results. Pamela Smith emphasized the embodied, sensory dimensions of calcination as part of the tacit knowledge of craft practitioners in *The Body of the Artisan* (2004) ch.3. The operation was not merely theoretical but was grounded in hands-on engagement with materials and heat.</p>

<h2>Related Concepts</h2>
<p>Calcination is the first operation in the sequence of the Great Work, followed by [LINK:dissolution], [LINK:distillation], and other operations aimed at reconstituting matter in a purer form. It is closely related to [LINK:putrefaction], which also breaks down existing form but uses moist heat in sealed vessels rather than dry, open fire. Both operations share the goal of returning matter toward an undifferentiated state from which it can be reformed. [LINK:transmutation] is only possible after the base metal has been calcined and its matter freed from its original metallic form.</p>

<h2>Literature</h2>
<p>Abraham, Lyndy. <i>A Dictionary of Alchemical Imagery</i>. Cambridge University Press, 1998.<br>
Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber</i>. Brill, 1991.<br>
Newman, William R., and Lawrence M. Principe. "Some Problems with the Historiography of Alchemy." In <i>Secrets of Nature</i>, edited by William R. Newman and Anthony Grafton. MIT Press, 2001.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Smith, Pamela H. <i>The Body of the Artisan: Art and Experience in the Scientific Revolution</i>. University of Chicago Press, 2004.<br>
Thorndike, Lynn. <i>A History of Magic and Experimental Science</i>. 8 vols. Columbia University Press, 1923–1958.</p>"""
},
'distillation': {
'definition_long': """<p>Distillation (<i>distillatio</i>; also spelled <i>distillation</i>) was one of the oldest and most technically important alchemical operations, in which a liquid or volatile substance was heated to produce vapors, which were then condensed and collected, producing a purified or concentrated version of the original material. This is an ACTOR_TERM — historical practitioners explicitly performed and named this operation across the full chronological range from ancient texts through to early modern chemists. The operation appears in the earliest Greek alchemical texts, in Arabic alchemy, in medieval Latin alchemy, and in Renaissance and early modern pharmaceutical and alchemical practice. Distillation produced real, observable, reproducible results: volatile essences, concentrated liquids, and refined substances that showed measurably different properties from the crude materials they derived from.</p>

<h2>Historical Usage and Material Grounding</h2>
<p>The apparatus of distillation — alembics, retorts, condensing coils, receiving vessels — appears illustrated in alchemical manuscripts and described in texts from antiquity onward. The operation was grounded in observable phenomena and required specific, learnable skills. When wine was distilled, a lighter, more volatile liquid (alcohol) could be separated from the heavier, non-volatile components. When plant materials were distilled, aromatic oils could be captured. When minerals or metallic salts were distilled under controlled conditions, concentrated solutions with different colors and properties could be produced. The sensory experience was distinctive: the heating of the material, the appearance of vapors, their condensation, the collection of droplets, the smell and taste (sometimes) of the resulting liquid — all these embodied the practitioner's knowledge of the operation.</p>

<p>The theoretical significance of distillation in alchemy was substantial. Many alchemists understood distillation as a way to separate the essential, spiritual component of a substance from its gross, material components. The [LINK:quintessence] concept, in particular, was directly connected to distillation: the quintessence was what remained after multiple distillations, the purified essence of a substance. Distillation also connected to [LINK:sublimation], another vaporization-based separation: both used heat to convert solids or liquids into vapors, but sublimation produced a solid directly from vapor (without an intermediate liquid), while distillation collected the condensed liquid from vapors.</p>

<h2>Scholarly Significance</h2>
<p>Lawrence Principe demonstrated that distillation, described in alchemical texts, produces genuine chemical phenomena — the separation of volatile from non-volatile components, the production of concentrated solutions, the isolation of aromatic compounds — in *The Secrets of Alchemy* (2013) ch.1 pp.1–25. Principe's laboratory replication of historical distillation procedures has shown they work as described and produce real, reproducible results. William Newman's analysis of the <i>Summa Perfectionis</i> situated distillation within the corpuscular understanding of matter: distillation separates particles of different sizes and weights, concentrating the finer, more spiritually active components. Pamela Smith emphasized distillation as an exemplary case of embodied craft knowledge — the skill required to perform it successfully cannot be fully conveyed in words alone but must be learned through practice in *The Body of the Artisan* (2004).</p>

<h2>Related Concepts</h2>
<p>Distillation is foundational to [LINK:operational-chemistry] as perhaps the most ancient and versatile alchemical operation. It is closely related to [LINK:sublimation], which also uses vaporization but produces a solid rather than a liquid product. Distillation is essential to the preparation of the [LINK:quintessence] and to the production of pharmaceutical essences in [LINK:iatrochemistry]. The operation connects to [LINK:calcination] and [LINK:dissolution]] as part of the sequence of operations in the Great Work.</p>

<h2>Literature</h2>
<p>Halleux, Robert. <i>Les textes alchimiques</i>. Brepols, 1979.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Principe, Lawrence M., and William R. Newman. "Some Problems with the Historiography of Alchemy." In <i>Secrets of Nature</i>, edited by William R. Newman and Anthony Grafton. MIT Press, 2001.<br>
Smith, Pamela H. <i>The Body of the Artisan: Art and Experience in the Scientific Revolution</i>. University of Chicago Press, 2004.<br>
Thorndike, Lynn. <i>A History of Magic and Experimental Science</i>. 8 vols. Columbia University Press, 1923–1958.<br>
Viano, Cristina, editor. <i>L'alchimie et ses racines philosophiques</i>. Vrin, 2005.</p>"""
},
'sublimation': {
'definition_long': """<p>Sublimation (<i>sublimatio</i>) was an alchemical operation in which a solid substance was heated to produce vapors that, upon cooling, returned directly to solid form without passing through a liquid intermediate state. This is an ACTOR_TERM — historical practitioners explicitly named, described, and performed this operation. The term and concept appear in Greek alchemical texts, in Arabic alchemy, and throughout medieval and early modern European alchemy. Sublimation was understood as one of the fundamental operations for purifying and concentrating substances, particularly for separating volatile from non-volatile components and for elevating matter toward a more refined state.</p>

<h2>Historical Usage and Material Grounding</h2>
<p>Sublimation is a chemically real phenomenon: certain substances, when heated, convert directly from solid to vapor, bypassing the liquid phase. Common examples known to historical practitioners included mercury (quicksilver), arsenic, sulfur, and certain metallic salts. The apparatus for sublimation consisted of vessels designed to allow vapors to rise and then cool, returning to solid form in a different location — typically a cooled upper vessel or chamber. The observable phenomenon was striking: a solid material appeared to vanish when heated, reappearing as a solid in the cooling chamber, often with changed color or texture. This transformation appeared almost miraculous and was theoretically significant: it seemed to demonstrate that matter could be transformed from one state to another and reconstituted in a more pure or refined form.</p>

<p>In practical laboratory work, sublimation was used to separate and purify substances. Mercury sublimate (mercury chloride) was produced by subliming mercury with salt — a procedure that yielded a white crystalline solid with properties distinctly different from metallic mercury. Arsenic and other metalloid oxides could be sublimed to concentrate and purify them. The sensory experience of sublimation — seeing solid turn to invisible vapor and reform as solid elsewhere — was central to practitioners' understanding of what was possible in matter transformation.</p>

<h2>Scholarly Significance</h2>
<p>Lawrence Principe has demonstrated through laboratory replication that historical descriptions of sublimation operations correspond to genuine chemical phenomena in *The Secrets of Alchemy* (2013) pp.18–22. Sublimation was understood in the sulphur-mercury theory as a way to separate volatile (mercurial) components from less volatile components, and in the [LINK:tria-prima] framework as a way to concentrate and purify specific principles. William Newman situated sublimation within the broader framework of early modern matter theory, where vaporization-based separations were understood through corpuscular accounts of particle size and volatility in *The Summa Perfectionis* (1991).</p>

<h2>Related Concepts</h2>
<p>Sublimation is closely related to [LINK:distillation]] — both use heat to vaporize substances — but sublimation produces a solid product while distillation produces a liquid. Both operations are used in the sequence toward [LINK:transmutation]] and the preparation of the [LINK:philosophers-stone]]. Sublimation relates to [LINK:calcination] and [LINK:dissolution] as operations for breaking down and reconstituting matter.</p>

<h2>Literature</h2>
<p>Halleux, Robert. <i>Les textes alchimiques</i>. Brepols, 1979.<br>
Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber</i>. Brill, 1991.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Smith, Pamela H. <i>The Body of the Artisan: Art and Experience in the Scientific Revolution</i>. University of Chicago Press, 2004.<br>
Thorndike, Lynn. <i>A History of Magic and Experimental Science</i>. 8 vols. Columbia University Press, 1923–1958.</p>"""
},
}

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    updated = 0
    for slug, data in ENRICHMENTS.items():
        c.execute('UPDATE concepts SET definition_long=?, review_status=?, confidence=? WHERE slug=?',
                  (data['definition_long'], 'DRAFT', 'MEDIUM', slug))
        if c.rowcount > 0:
            wc = len(data['definition_long'].split())
            print(f'  {slug}: {len(data["definition_long"])} chars / ~{wc} words')
            updated += c.rowcount
    conn.commit()
    conn.close()
    print(f'\nUpdated {updated} concepts.')

if __name__ == '__main__':
    main()
