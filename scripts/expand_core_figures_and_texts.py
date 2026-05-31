#!/usr/bin/env python3
"""
expand_core_figures_and_texts.py

Batch 2 of Helmontian-era content:
- Expand Starkey, Boyle, Newton, van Helmont bios to 1200+ words
- Add 3 new scholarship texts: Gehennical Fire, The Aspiring Adept, Newton the Alchemist
- Add alkahest concept (ACTOR_TERM)
- Bring 9 existing scholarship/compilation texts above their word-count minimums
"""

import sqlite3, re

DB = 'db/alchemy_timeline.db'

def wc(html):
    return len(re.sub('<[^>]+>', ' ', html or '').split())

def append_html(conn, table, field, slug, extra):
    c = conn.cursor()
    c.execute(f'SELECT {field} FROM {table} WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row:
        print(f'  [MISS] {slug}')
        return
    current = row[0] or ''
    new_val = current + extra
    c.execute(f'UPDATE {table} SET {field}=? WHERE slug=?', (new_val, slug))
    print(f'  [{table}/{slug}] {wc(current)} → {wc(new_val)} words')

# ---------------------------------------------------------------------------
# 1. PERSON BIO EXPANSIONS
# ---------------------------------------------------------------------------

PERSON_EXPANSIONS = {

'george-starkey': """
<h2>Life in London and the Philalethes Persona</h2>
<p>The strategic construction of the Philalethes persona is among the most intriguing episodes in the history of alchemical literature. Starkey presented Eirenaeus Philalethes as a mysterious American adept who had achieved the Philosophers' Stone in New England and then vanished — an anonymous master whose identit was known to no one. The mythology he attached to this persona included claims of miraculous feats: restoring hair and teeth to an aged woman, reviving a withered peach tree to fruit. The pseudonym itself — "peaceful lover of truth" — signaled a practitioner beyond worldly concern. In constructing this figure, Starkey was doing more than concealing his identity; he was creating a form of alchemical authority that his own biography as a Harvard graduate and immigrant physician could not provide. The texts attributed to Philalethes attracted readers including Leibniz, who corresponded about them, and the German Pietist movement, which found their spiritual vocabulary congenial.</p>

<p>In London, Starkey operated at the intersection of multiple social worlds: the natural-philosophical network of the Hartlib circle, the commercial market for chymical medicines, and the clandestine world of alchemical adepts and aspirants. His medical practice depended on the sale of iatrochemical preparations — antimony-based remedies, metallic salts, mineral acids applied to disease in the Paracelsian tradition — that were both commercially necessary and experimentally informative. The same operations that produced his materia medica produced the intermediate compounds in his pursuit of philosophic mercury. This integration of economic activity with experimental research is characteristic of the early modern chymist as described by Pamela Smith: a practitioner whose knowledge was simultaneously practical, commercial, and theoretical, embedded in material production rather than purely theoretical contemplation.</p>

<p>Starkey contracted plague and died in August 1665 during the Great Plague of London, at thirty-seven, before completing the work he had spent fifteen years pursuing. The Philalethes texts continued to circulate for decades after his death, increasingly attributed — by Newton and others — to a real adept who had achieved transmutation. Newman's recovery of Starkey's authorship dissolved this attribution, but it also revealed something more important: that the texts' intellectual content was the product of systematic experimental labor by a historically traceable individual, not the inheritance of a legendary master. This transformation of the Philalethes corpus from legendary wisdom to documented experimental practice is central to Newman's contribution to the historiography of seventeenth-century science.</p>""",

'robert-boyle': """
<h2>Alchemical Quest and Secrecy</h2>
<p>Lawrence Principe's archival research has established details of Boyle's alchemical practice that fundamentally revise the conventional portrait. Boyle used at least nine distinct ciphers and code systems in his private alchemical notebooks, suggesting unusual caution even by the standards of a tradition that routinely concealed its procedures. He actively sought contact with practicing adepts, corresponding with intermediaries and receiving reports of transmutations performed by mysterious figures. On at least one occasion he appears to have believed himself within reach of the Stone: a 1677 letter describes an anonymous American who "communicated to me a considerable arcanum," and his subsequent inquiries suggest he was attempting to reproduce or extend what he had been shown. He also made a serious effort to have the English statutory prohibition on gold-making (the 1404 Act of Multipliers) repealed — not out of commercial interest but specifically to remove legal obstacles to alchemical practice. This effort, analyzed by Principe, shows that Boyle's alchemy was not a private fantasy but a practical program that engaged with the legal and social infrastructure of his day.</p>

<p>Boyle's alchemical interests were inseparable from his theological concerns. His persistent anxiety about atheism — he endowed the Boyle Lectures after his death specifically to refute it — was addressed partly through his natural philosophy and partly through his alchemy. If the Philosophers' Stone existed, it demonstrated the reality of forces beyond mechanical matter in motion; if spiritual adepts genuinely possessed extraordinary powers over nature, this was evidence against a purely materialist universe. Principe argues that Boyle's corpuscular philosophy and his alchemical quest were not contradictory but complementary: both were strategies for demonstrating that nature contained active principles beyond the merely mechanical, and that God was operatively present in the material world. The reconstruction of Boyle's "lost" <i>Dialogue on the Transmutation and Melioration of Metals</i> from scattered manuscript fragments in the Royal Society archive provides direct evidence of this integration: the dialogue's argument moves fluidly between corpuscular theory, experimental results, and the possibility of transmutation, treating them as parts of a single investigation.</p>""",

'isaac-newton': """
<h2>The Laboratory at Trinity</h2>
<p>Newton's most intensive period of laboratory work ran from approximately 1678 to 1696, when he was simultaneously writing the <i>Principia</i> (1687) and conducting experiments in the garden shed behind his rooms at Trinity College, Cambridge. His laboratory records from this period, analyzed in the Chymistry of Isaac Newton project, show sustained attention to specific operations: the amalgamation of metals with mercury, the preparation of antimony compounds, the study of colored precipitates and color changes under heating, and the behavior of gold and silver in various mineral acid preparations. These were not random experiments but part of a systematic program aimed at preparing the "sophick mercury" described in the [LINK:george-starkey] Philalethes texts. Newton's annotation of specific Philalethes procedures, preserved in his manuscript "Index Chemicus," cross-references dozens of alchemical authors to extract converging claims about the first matter of the Stone.</p>

<p>The connection between Newton's alchemy and his natural philosophy is one of the most debated questions in Newton scholarship. Newton believed in what he called a "vegetative principle" — an active force in nature responsible for biological growth, metallic vegetation (the growth-like formations produced when metals crystallize from solution), and chemical transmutation — that was distinct from and superior to the mechanical forces of collision and pressure. This vegetative spirit appears in his early alchemical manuscripts as the animating principle of the Stone; it reappears, in philosophical guise, in his later discussions of active principles in the <i>Opticks</i> (Query 31, 1706), where Newton asks whether "Nature does nothing in vain" and describes subtle active forces operating within and between particles of matter. Richard Westfall argued that these active principles derived from Newton's alchemical thought; William Newman has been more cautious but concedes that the continuity is real. Whatever the precise causal connection, Newton's alchemy and his natural philosophy inhabited a single conceptual world.</p>""",

'jan-van-helmont': """
<h2>Inquisition, Mysticism, and Empiricism</h2>
<p>Van Helmont's career was not the smooth progression of an experimental philosopher but a fraught negotiation between empirical ambition and institutional constraint. His 1621 pamphlet "De Magnetica Vulnerum Curatione" ("On the Magnetic Cure of Wounds"), which discussed the fashionable topic of sympathetic cure by means of an ointment applied to the weapon that inflicted the wound rather than to the wound itself, attracted denunciation from Spanish theologians and eventually from the Spanish Inquisition. He was placed under house arrest and prohibited from publishing for more than fifteen years, a restriction that paradoxically concentrated his energies on the unpublished laboratory and theoretical work that would become the <i>Ortus Medicinae</i>. The tensions between his devout Catholicism, his mystical experiences (he reports a vision of his own soul as a geometrical luminosity), and his anti-scholastic empiricism are characteristic of the devout natural philosophers of the late sixteenth and early seventeenth centuries — figures for whom empirical investigation and spiritual commitment were not in conflict but mutually reinforcing.</p>

<p>Van Helmont's influence on the generation that followed him operated primarily through the <i>Ortus Medicinae</i> as a practical and theoretical resource. Practitioners working through the text found in it an anti-Aristotelian, anti-Galenic program grounded in chemical experiment: a framework for medicine in which disease had specific chemical causes and required specific chemical remedies, in which the body was governed by vital organizing principles (fermenta, archeus) rather than by the balance of humors, and in which matter at its most fundamental was water capable of infinite transformation under the action of those principles. [LINK:george-starkey] absorbed this framework so thoroughly that his laboratory notebooks read as Helmontian research programs. [LINK:robert-boyle]'s early work on air, salts, and acids is intelligible as Helmontian chymistry applied to mechanical philosophy. Even after Georg Ernst Stahl displaced Helmontian vitalism with phlogiston theory, van Helmont's gas concept — the discovery that distinct gaseous substances existed with specific chemical properties — remained foundational to the pneumatic chemistry of Joseph Black, Henry Cavendish, and ultimately [LINK:antoine-lavoisier].</p>""",
}

# ---------------------------------------------------------------------------
# 2. NEW SCHOLARSHIP TEXTS
# ---------------------------------------------------------------------------

NEW_TEXTS = [
{
'slug': 'gehennical-fire',
'title': "Gehennical Fire: The Lives of George Starkey, an American Alchemist in the Scientific Revolution",
'text_type': 'SCHOLARSHIP',
'original_language': 'English',
'composition_date': '1994',
'composition_year_start': 1994,
'composition_year_end': 1994,
'analysis_html': """\
<p><i>Gehennical Fire: The Lives of George Starkey, an American Alchemist in the Scientific Revolution</i> (Harvard University Press, 1994) by William R. Newman is the foundational monograph establishing [LINK:george-starkey] as a major figure in seventeenth-century natural philosophy and identifying him as the author of the pseudonymous Eirenaeus Philalethes corpus. The book's title refers to the "secret fire" described in alchemical texts as the active agent of metallic transformation — and to the destructive fire of social circumstance that consumed Starkey in the Great Plague of 1665. The "lives" of the subtitle are plural: Starkey the historically traceable Harvard graduate and London physician, and Philalethes the legendary American adept whose texts circulated as authentic transmissionary wisdom for decades after Starkey's death.</p>

<h2>Content and Argument</h2>
<p>Newman's central contribution is archival: the identification of Starkey as Philalethes through manuscript evidence, including letters in the Hartlib Papers at Sheffield University that connect Starkey's laboratory work directly to passages in the published Philalethes texts, and Starkey's laboratory notebooks (held at the Wellcome Library and other repositories), which reveal the experimental foundations of the allegorical texts. The demonstration that the "mysterious American adept" was a historically specific Harvard graduate who conducted quantitative laboratory experiments in London — and that the Philalethes texts were not received wisdom but worked-out laboratory knowledge — is among the most significant archival discoveries in the history of alchemy scholarship.</p>

<p>Beyond the archival identification, Newman argues for a positive evaluation of Starkey's experimental practice. Reading the laboratory notebooks against the published texts, he shows that Starkey translated the figurative, allegorical language of alchemical tradition into specific, reproducible laboratory procedures — a translation process that Newman characterizes as genuinely scientific in method, even if the goals remained alchemical. The procedures involved systematic weighing and measurement, control of temperature, close observation of color changes and material behaviors, and correlation of results with theoretical expectations derived from reading. This was experimental inquiry in a meaningful sense, and Newman's argument that it represents a genuine form of early experimental science — continuous with, rather than opposed to, the emerging scientific revolution — has been influential in reshaping historiography of both alchemy and seventeenth-century science.</p>

<h2>Scholarly Significance</h2>
<p>The book launched Newman's sustained project of recovering the experimental character of early modern alchemy and situating it within the history of chemistry rather than the history of religion or psychology. It established the methodological approach — combining manuscript analysis with laboratory replication — that Newman and Lawrence Principe extended in their joint work, most fully in [LINK:alchemy-tried-in-the-fire] (2002). The book also inaugurated the rehabilitation of Starkey as a figure worthy of serious historical attention, a rehabilitation continued by the Chymistry of Isaac Newton project (Indiana University), which has digitized the alchemical manuscripts that Starkey's Philalethes texts inspired Newton to annotate.</p>

<h2>Literature</h2>
<p>Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Newman, William R. <i>Newton the Alchemist: Science, Enigma, and the Quest for Nature's "Secret Fire."</i> Princeton University Press, 2019.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Webster, Charles. <i>The Great Instauration: Science, Medicine, and Reform 1626–1660</i>. Duckworth, 1975.</p>""",
},

{
'slug': 'the-aspiring-adept',
'title': "The Aspiring Adept: Robert Boyle and His Alchemical Quest",
'text_type': 'SCHOLARSHIP',
'original_language': 'English',
'composition_date': '1998',
'composition_year_start': 1998,
'composition_year_end': 1998,
'analysis_html': """\
<p><i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i> (Princeton University Press, 1998) by Lawrence M. Principe is the monograph that fundamentally revised the received image of [LINK:robert-boyle] as a founder of "modern chemistry" who decisively rejected alchemical tradition. Drawing on extensive manuscript research in the Boyle Papers at the Royal Society and other archives, Principe demonstrates that Boyle pursued alchemical goals — including the preparation of the Philosophers' Stone and metallic transmutation — throughout his life with the same seriousness he brought to his pneumatic experiments and corpuscular theory. The book is simultaneously a major archival contribution, a methodological argument for reading alchemical manuscripts on their own terms, and a revision of what the "Scientific Revolution" looked like to those living through it.</p>

<h2>Content and Argument</h2>
<p>Principe's central archival discoveries include the identification of nine distinct ciphers that Boyle used to protect his alchemical records — evidence that the sensitivity around his alchemical practice was real and deliberate, not the occasional privacy of a minor hobby. More dramatically, he reconstructed Boyle's "lost" <i>Dialogue on the Transmutation and Melioration of Metals</i> from scattered manuscript fragments, presenting for the first time a direct record of Boyle arguing for the possibility of transmutation within his corpuscular theoretical framework. This dialogue demonstrates that Boyle's alchemy and his natural philosophy were not compartmentalized but integrated: his corpuscular theory provided a mechanistic rationale for transmutation (altering the texture of metallic particles), and his alchemical aspirations motivated his attention to the "active principles" that his mechanical philosophy required.</p>

<p>Principe's reinterpretation of [LINK:sceptical-chymist] is among the book's most influential contributions. Where earlier historians had read the text as an attack on alchemists, Principe showed that the actual targets were "vulgar chymists" — Paracelsian pharmaceutical authors and textbook writers — and that Boyle explicitly exempted practitioners of the higher alchemical art from his criticism. The misreading originated in the nineteenth century, when chemists seeking disciplinary ancestors encountered the word "alchymists" in the text and assumed it referred to the alchemical tradition as a whole. Principe's careful contextual analysis of the text's argument, vocabulary, and manuscript evidence corrected this misreading and demonstrated its historiographical consequences.</p>

<h2>Scholarly Significance</h2>
<p>The book has been central to the broader revision of seventeenth-century chemical historiography undertaken by Principe and William Newman. Together with Newman's work on [LINK:george-starkey] and Newton, and their joint monograph [LINK:alchemy-tried-in-the-fire] (2002), <i>The Aspiring Adept</i> established that the distinction between "alchemy" and "chemistry" was not made by seventeenth-century practitioners in the way that later histories assumed. Boyle represents the clearest case: a figure canonical in the history of modern chemistry who simultaneously held the transmutational ambitions of an alchemist and structured his philosophical thinking partly around their realization. The book's impact has been wide, influencing scholarship on Boyle's theology, his social network, his laboratory practice, and his role in the formation of the Royal Society.</p>

<h2>Literature</h2>
<p>Hunter, Michael. <i>Boyle: Between God and Science</i>. Yale University Press, 2009.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Shapin, Steven. <i>A Social History of Truth: Civility and Science in Seventeenth-Century England</i>. University of Chicago Press, 1994.</p>""",
},

{
'slug': 'newton-the-alchemist',
'title': "Newton the Alchemist: Science, Enigma, and the Quest for Nature's 'Secret Fire'",
'text_type': 'SCHOLARSHIP',
'original_language': 'English',
'composition_date': '2019',
'composition_year_start': 2019,
'composition_year_end': 2019,
'analysis_html': """\
<p><i>Newton the Alchemist: Science, Enigma, and the Quest for Nature's "Secret Fire"</i> (Princeton University Press, 2019) by William R. Newman is the culminating volume in Newman's decades-long project of recovering the experimental character of early modern alchemy. The book applies to [LINK:isaac-newton]'s alchemical manuscripts the same combination of archival analysis and laboratory replication that Newman and Lawrence Principe used in earlier work on [LINK:george-starkey] and [LINK:robert-boyle]. Drawing on the full digital corpus of Newton's alchemical manuscripts, now accessible through the Chymistry of Isaac Newton project at Indiana University (directed by Newman), the book provides the first comprehensive account of what Newton was actually doing in his alchemical laboratory — and argues that his alchemy was a systematic, quantitative experimental program rather than a mystical digression from his scientific work.</p>

<h2>Content and Argument</h2>
<p>Newman's central argument has two parts. First, he demonstrates that Newton's primary alchemical interest was in preparing "sophick mercury" — a specially processed form of mercury, first described in the Philalethes corpus authored by Starkey, that was supposed to serve as the "first matter" or primary reagent in producing the Philosophers' Stone. Newton copied, annotated, and attempted to reproduce the Philalethes procedures for preparing this mercury over more than thirty years, and his laboratory records show careful, quantitative tracking of his experiments. This was not casual reading but sustained laboratory research with specific operational goals. Second, Newman examines the connection between Newton's alchemy and his natural philosophy, arguing that Newton's concept of "active principles" — forces operating within matter that were distinct from mechanical collision — derived partly from his alchemical thinking about "vegetative" and "multiplicative" forces that made metallic growth and transmutation possible.</p>

<p>Newman also provides a thorough critique of earlier interpretations of Newton's alchemy. B.J.T. Dobbs's influential thesis — that Newton's alchemy was primarily driven by his heterodox theology and his search for a "vegetative spirit" that proved God's activity in nature — is examined and partially revised: Newman agrees that theological and natural-philosophical motivations were present but argues that Dobbs underemphasized the practical, laboratory-experimental dimension of Newton's work and overstated the mystical character of his alchemical interests. Richard Westfall's assessment is similarly nuanced: the connection between alchemy and gravitational theory is acknowledged but treated with more caution than Westfall's formulation allowed.</p>

<h2>Scholarly Significance</h2>
<p>The book represents the most complete account of Newton's alchemy yet written and is likely to be the reference work on the subject for decades. Its methodological contribution — demonstrating that historical alchemy can be studied through laboratory replication alongside manuscript analysis — extends Newman's earlier work and provides a model for future historians of science working in this area. The book also contributes to the wider project of the "chymistry" paradigm advanced by Newman and Principe: understanding early modern natural philosophy requires taking seriously the experimental programs that pursued transmutational goals, because those programs were structurally connected to the observational and theoretical advances that historians of science study under the name of the Scientific Revolution.</p>

<h2>Literature</h2>
<p>Dobbs, Betty Jo Teeter. <i>The Foundations of Newton's Alchemy</i>. Cambridge University Press, 1975.<br>
Dobbs, Betty Jo Teeter. <i>The Janus Faces of Genius: The Role of Alchemy in Newton's Thought</i>. Cambridge University Press, 1991.<br>
Newman, William R. <i>Gehennical Fire: The Lives of George Starkey, an American Alchemist in the Scientific Revolution</i>. Harvard University Press, 1994.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Westfall, Richard S. <i>Never at Rest: A Biography of Isaac Newton</i>. Cambridge University Press, 1980.</p>""",
},
]

# ---------------------------------------------------------------------------
# 3. NEW CONCEPT: ALKAHEST
# ---------------------------------------------------------------------------

ALKAHEST_CONCEPT = {
'slug': 'alkahest',
'label': 'Alkahest (Universal Solvent)',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': (
    "The alkahest (also alcahest) was a hypothetical universal solvent posited by Jan Baptist van Helmont "
    "(1580–1644) as the most powerful agent of chemical dissolution: a substance capable of reducing any body "
    "to its ultimate, primitive constituents. This is an ACTOR_TERM — van Helmont coined the term and "
    "practitioners including George Starkey and Robert Boyle explicitly sought it in their laboratory work. "
    "The alkahest occupied a structural position in Helmontian chemistry analogous to the Philosopher's Stone "
    "in transmutational alchemy: the supreme solvent as the Stone was the supreme transformative agent."
),
'definition_long': """\
<p>The alkahest (also spelled alcahest or alcahest; etymology uncertain, possibly from the Arabic, possibly a Paracelsian coinage that van Helmont adopted or invented) was a hypothetical universal solvent posited by Jan Baptist van Helmont (1580–1644) as the most powerful agent of dissolution conceivable: a liquid capable of reducing any compound body — metals, stones, bones, organic tissue — to its original, primitive elemental constituents without itself being consumed or altered in the process. This is an ACTOR_TERM: van Helmont introduced and defined the concept, claimed to possess the alkahest, and practitioners including [LINK:george-starkey] and [LINK:robert-boyle] explicitly sought it as an experimental goal. The alkahest occupied a structural position in [LINK:helmontian-chymistry] analogous to the [LINK:philosophers-stone] in the transmutational tradition: as the Stone was the supreme agent of metallic transformation, the alkahest was the supreme agent of dissolution, and together they represented the outer limits of what chymical operation could in principle achieve.</p>

<h2>Historical Usage</h2>
<p>Van Helmont described the alkahest in several treatises collected in the <i>Ortus Medicinae</i> (1648). He claimed to have prepared and used it, describing its properties: it dissolved gold and other metals without corrosion, leaving the dissolved substance in an elemental or primitive state from which it could not be reconstituted to its original form. The alkahest itself emerged unchanged from each dissolution, available for further use. This indestructibility distinguished it from ordinary acids, which were consumed in their reactions, and made it theoretically significant as a substance that acted on matter without itself undergoing change — a kind of chemical catalyst avant la lettre, though operating at a more fundamental level than catalysts as understood in modern chemistry.</p>

<p>Van Helmont's claim to possess the alkahest was part of his broader argument for water monism — his doctrine that water was the ultimate element underlying all material substance. If a universal solvent could reduce any substance to its primitive constituents, and if van Helmont was correct that all matter ultimately derived from water, then the alkahest would reduce all bodies to water. The willow tree experiment, which he interpreted as demonstrating that plant matter derived from water, and the alkahest, which would confirm that reduction, were complementary demonstrations of the same underlying doctrine. This theoretical coherence gave the alkahest conceptual weight beyond being merely a laboratory aspiration.</p>

<p>[LINK:robert-boyle] referred to the alkahest in <i>The Sceptical Chymist</i> (1661), adopting Helmontian vocabulary to challenge Paracelsian element theory: if a universal solvent could dissolve any substance to its primitive constituents, then the products of distillation and combustion could not be the "elements" and "principles" that Paracelsians claimed to separate through fire. Boyle's use of the alkahest concept was both critical (he questioned whether any substance could truly be a universal solvent) and constructive (the concept supported his argument against fire-based analysis as a route to elemental knowledge). [LINK:george-starkey] treated the alkahest as an active experimental goal, and his laboratory notebooks show attempts to identify substances that might constitute or serve as precursors to the alkahest, alongside his work on philosophic mercury and the Philosophers' Stone. Lawrence Principe, in <i>The Aspiring Adept</i> (1998), documented Boyle's ongoing engagement with the alkahest as part of his broader alchemical program.</p>

<h2>Scholarly Significance</h2>
<p>The alkahest illustrates the methodological challenges in interpreting Helmontian chymistry. If van Helmont genuinely believed he possessed it, his claim was an empirical report subject to the same standards he applied to his gas experiments and physiological observations — not a metaphor or a spiritual symbol. Walter Pagel, whose foundational study of van Helmont (<i>Joan Baptista Van Helmont: Reformer of Science and Medicine</i>, 1982) remains essential, treated van Helmont's claims about the alkahest with careful attention to context, noting that the combination of empirical rigor and extraordinary claim is characteristic of van Helmont throughout the <i>Ortus Medicinae</i>. Lawrence Principe's approach to such claims — taking them seriously as empirical reports that can be evaluated against the practical chemistry of the period — provides a productive framework: the question is not whether the alkahest "really" existed but what specific chemical operations van Helmont was conducting when he believed he had prepared it, and whether those operations correspond to any known chemistry.</p>

<p>Newman and Principe's treatment of the alkahest in [LINK:alchemy-tried-in-the-fire] (2002) situates it within the Helmontian program as transmitted to Starkey and Boyle, showing how the concept structured experimental inquiry in the mid-seventeenth century. The alkahest functioned as a regulative ideal in Helmontian laboratory practice: a goal that organized experimental programs toward dissolution and analysis of matter even when the specific operations undertaken were preliminary steps rather than achievements of the goal itself. This regulative function — comparable to the role of the Philosophers' Stone in the broader alchemical tradition — is what makes the concept historically significant regardless of whether any practitioner ever produced what they described.</p>

<h2>Related Concepts</h2>
<p>The alkahest is closely related to [LINK:helmontian-chymistry] as one of its defining aspirational goals, alongside the gas theory and the archeus. It connects to [LINK:philosophers-stone] as a structural parallel: supreme agent of dissolution as the Stone is supreme agent of transformation. The concept of [LINK:prima-materia] — the prime matter underlying all substance — is the theoretical terminus of what the alkahest would reveal: if every substance could be dissolved to its primitive constituents, those constituents would constitute the prima materia of ancient and medieval speculation. The alkahest also relates to [LINK:distillation] as the sophisticated end of the dissolution operations that distillation represented at a more modest scale.</p>

<h2>Literature</h2>
<p>Pagel, Walter. <i>Joan Baptista Van Helmont: Reformer of Science and Medicine</i>. Cambridge University Press, 1982.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Principe, Lawrence M. <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i>. Princeton University Press, 1998.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Newman, William R. <i>Gehennical Fire: The Lives of George Starkey, an American Alchemist in the Scientific Revolution</i>. Harvard University Press, 1994.<br>
Moran, Bruce T. <i>Distilling Knowledge: Alchemy, Chemistry, and the Scientific Revolution</i>. Harvard University Press, 2005.<br>
Hirai, Hiro. <i>Medical Humanism and Natural Philosophy: Renaissance Debates on Matter, Life, and the Soul</i>. Brill, 2011.<br>
Partington, J.R. <i>A History of Chemistry</i>. Vol. 2. Macmillan, 1961.</p>""",
}

# ---------------------------------------------------------------------------
# 4. EXISTING TEXT EXPANSIONS (near-minimum; need 25-150 words each)
# ---------------------------------------------------------------------------

TEXT_EXPANSIONS = {

'atoms-and-alchemy': """
<p>The book also contains an important methodological contribution: Newman demonstrates that laboratory replication of historical alchemical procedures can function as a scholarly tool. By conducting actual chemical experiments replicating procedures described in the <i>Summa Perfectionis</i> and other texts, Newman showed that the operations described were real and reproducible — not metaphors, not spiritual exercises, but actual chemistry that produced specific, describable results. This combination of archival scholarship with laboratory practice provides a model for the historiography of early chemistry that has been widely followed. Newman's Indiana University "Chymistry of Isaac Newton" project extends this method to Newton's alchemical manuscripts, digitizing and contextualizing a corpus of over a million words.</p>""",

'the-business-of-alchemy': """
<p>Smith's methodological contribution extends beyond alchemy to the historiography of the scientific revolution generally: her argument that "knowing how" preceded and enabled "knowing that" — that practical, embodied craft knowledge was a source of theoretical insight rather than merely applied science — challenges narratives that treat the Scientific Revolution as a purely intellectual event. This approach influenced the broader "material turn" in history of science, and <i>The Business of Alchemy</i> is widely cited in scholarship on artisanal knowledge, laboratory practice, and the social organization of early modern science. Lawrence Principe's laboratory replication work and Newman's archival analysis of practitioners' notebooks both draw on Smith's framework for understanding what it meant to know chemistry in the sixteenth and seventeenth centuries.</p>""",

'the-egyptian-hermes': """
<p>Fowden's work has been influential beyond the specialist study of Hermetism. His argument that Hermetic literature must be understood as a product of specific late antique social and religious conditions — rather than as a timeless wisdom tradition or a collection of pseudo-antique forgeries — provided the historiographical foundation for subsequent work on the relationship between Hermetism and early alchemy. Lawrence Principe and William Newman have drawn on Fowden's contextualization of the Hermetic corpus in arguing for a non-mystical, experimentally grounded reading of early alchemical texts: if even the Hermetic literature that alchemists cited as authority was a product of specific historical conditions rather than revealed wisdom, the practical and theoretical content of alchemical texts becomes primary, and their spiritual and symbolic dimensions become secondary. Fowden's influence on the historiography of late antique religion, philosophy, and proto-science remains foundational.</p>""",

'the-body-of-the-artisan': """
<p>Smith's broader argument is that the "Scientific Revolution" cannot be understood purely as an intellectual event driven by university-educated natural philosophers. The practical knowledge embodied in workshop production — how materials behave, what happens to metals in fire, how pigments mix, how glass flows — was a constitutive input to the theoretical developments of the period, not merely an application of prior theory. This argument connects to William Newman's demonstration that alchemical laboratory notebooks (especially Starkey's) show a form of experimental inquiry that preceded and informed more publicly recognized natural philosophy. For historians of chemistry and alchemy specifically, Smith's work situates the laboratory practitioner — the apothecary, the assayer, the metalworker, the alchemist — as an epistemologically significant figure rather than a craftsman awaiting theoretical guidance from above.</p>""",

'collection-of-the-ancient-greek-alchemists': """
<p>The importance of Berthelot's collection for later scholarship cannot be overstated, despite the limitations of his approach. Every subsequent study of Greek alchemy — from the early twentieth-century work of F. Sherwood Taylor to Garth Fowden's contextual analysis in <i>The Egyptian Hermes</i> (1986) and the ongoing critical editions of individual texts — depends on or responds to Berthelot's foundational compilation. Lawrence Principe has used the collection in his broader history of alchemy (<i>The Secrets of Alchemy</i>, 2013), while acknowledging that Berthelot's nineteenth-century positivist framework imposed anachronistic categories on texts that require more careful contextual treatment. The <i>Collection</i> remains essential as a repository even where its editorial judgments have been superseded.</p>""",

'theatrum-chemicum': """
<p>The <i>Theatrum Chemicum</i>'s editorial and commercial success illustrates the significance of the early modern print market for the transmission of alchemical knowledge. Zetzner's publisher venture made obscure manuscripts available to readers across Europe who would otherwise have had no access to them, standardizing variant texts and creating a reference library that practitioners could purchase, annotate, and cite. Lawrence Principe and William Newman have examined the <i>Theatrum Chemicum</i> as a transmission vehicle in their studies of Starkey, Boyle, and Newton: all three read and annotated texts from Zetzner's compilation, and its standardization of certain versions of key texts (rather than others) shaped the alchemical tradition into which they entered.</p>""",

'turba-philosophorum': """
<p>Scholarly attention to the <i>Turba Philosophorum</i> has focused on its function as a vehicle for transmitting Arabic alchemical theory into Latin Europe and on the historical significance of its dialogue form — the dramatic staging of philosophical debate between ancient sages — as a rhetoric of authority. William Newman has examined the <i>Turba</i>'s relationship to the Latin alchemical corpus of the twelfth through fourteenth centuries, tracing how its theoretical framework for understanding metallic composition and transformation was absorbed into and modified by later Latin texts including the <i>Summa Perfectionis</i>. The text is also significant as evidence for the process of Arabization of Greek natural philosophy: many of the "philosophers" depicted in the dialogue bear versions of names of ancient Greek thinkers, but their arguments are mediated through Arabic translation and reinterpretation.</p>""",

'corpus-jabirianum': """
<p>The question of Jabir's authorship remains unresolved, and the debate itself is historically instructive. Jabir ibn Hayyan was a real figure at the Abbasid court; whether he wrote any of the texts attributed to him is disputed. Paul Kraus's foundational study (1942–1943) argued for a ninth-century Ismaili compilation with multiple authors; William Newman's reanalysis of Kraus's argument, in <i>Atoms and Alchemy</i> (2006), challenged aspects of Kraus's reconstruction while accepting that the corpus accumulated over time. The Jabir question illustrates a pervasive feature of early chemical literature: authority was constructed through attribution, and texts accumulated authorship through association with prestigious names. What matters for the history of chemistry is not whether Jabir wrote these texts but that the corpus collectively systematized practical chemistry into a theoretical framework that shaped the tradition for centuries. The sulfur-mercury theory, the classification of substances, and the systematic approach to laboratory procedure that the Jabirian corpus established were transmitted to Latin Europe through twelfth-century translations and remained influential through the early modern period.</p>""",
}

# ---------------------------------------------------------------------------
# LOAD FUNCTIONS
# ---------------------------------------------------------------------------

def load_all():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    print("=== Expanding person bios ===")
    for slug, extra in PERSON_EXPANSIONS.items():
        append_html(conn, 'persons', 'bio_html', slug, extra)

    print("\n=== Adding new scholarship texts ===")
    for text in NEW_TEXTS:
        c.execute("""
            INSERT INTO texts (slug, title, text_type, original_language, composition_date,
                               composition_year_start, composition_year_end, analysis_html,
                               source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'AI_ASSISTED', 'DRAFT', 'MEDIUM')
            ON CONFLICT(slug) DO UPDATE SET
                title=excluded.title, text_type=excluded.text_type, analysis_html=excluded.analysis_html
        """, (text['slug'], text['title'], text['text_type'], text['original_language'],
              text['composition_date'], text['composition_year_start'], text['composition_year_end'],
              text['analysis_html']))
        c.execute('SELECT analysis_html FROM texts WHERE slug=?', (text['slug'],))
        print(f"  [texts/{text['slug']}] {wc(c.fetchone()[0])} words")

    print("\n=== Adding alkahest concept ===")
    a = ALKAHEST_CONCEPT
    c.execute("""
        INSERT INTO concepts (slug, label, category_type, operation_type, definition_short, definition_long,
                              source_method, review_status, confidence)
        VALUES (?, ?, ?, ?, ?, ?, 'AI_ASSISTED', 'DRAFT', 'MEDIUM')
        ON CONFLICT(slug) DO UPDATE SET
            label=excluded.label, definition_short=excluded.definition_short,
            definition_long=excluded.definition_long
    """, (a['slug'], a['label'], a['category_type'], a['operation_type'],
          a['definition_short'], a['definition_long']))
    c.execute('SELECT definition_long FROM concepts WHERE slug=?', (a['slug'],))
    print(f"  [concepts/{a['slug']}] {wc(c.fetchone()[0])} words")

    print("\n=== Expanding existing texts ===")
    for slug, extra in TEXT_EXPANSIONS.items():
        append_html(conn, 'texts', 'analysis_html', slug, extra)

    conn.commit()
    conn.close()
    print("\n=== Done ===")

if __name__ == '__main__':
    load_all()
