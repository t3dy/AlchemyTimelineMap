#!/usr/bin/env python3
"""
add_helmontian_era_content.py

Adds new scholarly content on the Helmontian-chymical tradition and its fate:
- 2 new concepts: helmontian-chymistry, phlogiston
- 3 new texts: ortus-medicinae, sceptical-chymist, alchemy-tried-in-the-fire
- 2 expanded person bios: Antoine Lavoisier, Georg Ernst Stahl
- 1 era fix: Jan van Helmont MEDIEVAL → EARLY_MODERN
- 8 new timeline events covering the Starkey/Boyle/Newton/Stahl/Lavoisier cluster
"""

import sqlite3

DB = 'db/alchemy_timeline.db'

# ---------------------------------------------------------------------------
# 1. NEW CONCEPTS
# ---------------------------------------------------------------------------

NEW_CONCEPTS = [
{
'slug': 'helmontian-chymistry',
'label': 'Helmontian Chymistry',
'category_type': 'ANALYST_TERM',
'operation_type': None,
'definition_short': (
    "Helmontian chymistry is a modern historiographical term for the experimental "
    "natural philosophy derived from Jan Baptist van Helmont (1580–1644) and developed "
    "by his successors, especially George Starkey and Robert Boyle. This is an ANALYST_TERM: "
    "practitioners did not use this label; it designates, retrospectively, a cluster of "
    "doctrines — gas theory, water monism, the alkahest, ferment physiology — that structured "
    "chymical inquiry in the mid-seventeenth century before Stahl's phlogiston theory displaced it."
),
'definition_long': """\
<p>Helmontian chymistry is a modern scholarly analytical term designating the cluster of experimental doctrines, physiological theories, and natural-philosophical commitments that derived from the work of Jan Baptist van Helmont (1580–1644) and were transmitted to the mid-seventeenth century by figures including George Starkey, Robert Boyle, Thomas Willis, and Francis Mercury van Helmont. This is an ANALYST_TERM: historical practitioners did not use "Helmontian chymistry" as a self-description, though they frequently cited van Helmont by name, acknowledged his authority, and oriented their own work in explicit relation to his. The term was developed and given scholarly currency by William R. Newman and Lawrence M. Principe, most fully in their joint monograph <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i> (University of Chicago Press, 2002), which traced the tradition from van Helmont through Starkey to Boyle and analyzed the reasons for its eventual displacement in the early eighteenth century.</p>

<h2>Origins and Terminological History</h2>
<p>The term reflects a deliberate historiographical intervention by Newman and Principe. Earlier histories of chemistry typically narrated the seventeenth century as a period in which "alchemy" — associated with transmutation, fraud, and mysticism — was progressively superseded by "chemistry" — associated with experiment, quantification, and rational method. In this narrative, van Helmont appeared at most as a transitional figure, half-liberated from alchemical superstition, whose gas theory and quantitative experiments pointed toward a chemistry not yet achieved. Newman and Principe's revisionary reading rejected this framework. They argued that van Helmont's work was neither a failed science nor a transitional step but a coherent positive program that shaped the most advanced experimental chymistry of the mid-seventeenth century.</p>

<p>The scholarly designation "Helmontian chymistry" captures the programmatic coherence of this tradition: it was not merely admiration of van Helmont's texts but active elaboration of his theoretical framework. George Starkey's laboratory notebooks, analyzed by Newman in <i>Gehennical Fire</i> (Harvard University Press, 1994), reveal a practitioner working systematically within a Helmontian conceptual framework — adapting van Helmont's gas theory, his ferment physiology, and his concept of the <i>archeus</i> (the organizing vital principle directing biological and chemical change) to laboratory investigations. [LINK:robert-boyle]'s early work, as Principe demonstrated in <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i> (Princeton University Press, 1998), shows deep Helmontian influence: Boyle explicitly referenced "gas, as the Helmontians call it" in his pneumatic investigations and oriented his critique in <i>The Sceptical Chymist</i> (1661) against "vulgar chymists" rather than against van Helmont.</p>

<h2>Core Doctrines of Helmontian Chymistry</h2>
<p>The Helmontian tradition was defined by several interlocking doctrines. First, van Helmont's water monism: the claim, dramatized by his famous willow tree experiment, that water was the elemental principle underlying all matter — that growth, transformation, and material change involved the conversion of water into diverse substances under the directing action of ferments and the <i>archeus</i>. This was a direct challenge to both Aristotelian four-element theory and Paracelsian <i>tria prima</i> (salt, sulphur, mercury). Second, gas theory: van Helmont's discovery and naming of distinct "airs" — particularly his <i>gas sylvestre</i> (carbon dioxide, produced by fermentation and combustion) — established that different gaseous substances existed with distinct chemical identities, a conceptual move that opened the way for pneumatic chemistry. Third, ferment physiology: van Helmont's elaborated theory of <i>fermenta</i> — specific, organizing chemical principles directing the transformation of food and the operation of different bodily organs — provided a chemical-vitalist framework for understanding living bodies that challenged Galenic humoral medicine. Fourth, the <i>alkahest</i>: the concept of a universal solvent capable of reducing all bodies to their primitive watery constituents, which van Helmont claimed to possess and which Boyle and Starkey sought. Fifth, the reality of metallic transmutation: van Helmont claimed personal experience of transmutation and treated it as an established empirical datum grounding his overall natural-philosophical framework.</p>

<p>These doctrines formed a mutually reinforcing system. Water monism implied that diverse substances could be interconverted; ferment theory explained how specific conversions were directed; gas theory revealed that products of fermentation and combustion had determinate chemical identities; and the alkahest represented the extreme case of dissolution that would confirm water monism by returning all substances to their original watery state. The Philosopher's Stone occupied an analogous role as the extreme case of metallic conversion. For practitioners like [LINK:george-starkey], working in this tradition meant conducting laboratory experiments on fermentation, distillation, and the preparation of specific chemical agents within this coherent theoretical framework.</p>

<h2>Scholarly Significance</h2>
<p>Newman and Principe's treatment of Helmontian chymistry has been central to the historiographical revision of seventeenth-century science known, in their terminology, as the "chymistry" project. Their argument in <i>Alchemy Tried in the Fire</i> is that Helmontian chymistry was not a precursor to the Scientific Revolution but a constitutive element of it: figures including Robert Boyle, Isaac Newton, and Thomas Willis developed their experimental programs in direct engagement with Helmontian doctrines, adapting, testing, modifying, and arguing against them. Boyle's corpuscularian chemistry, in this reading, was not a clean break from alchemy but a transformation of Helmontian chymistry — retaining Helmont's empirical orientation and experimental methods while replacing vitalistic explanations with mechanical ones. [LINK:isaac-newton]'s alchemical investigations, as Newman demonstrates in <i>Newton the Alchemist</i> (Princeton University Press, 2019), also drew on Helmontian theoretical resources, particularly through Newton's intensive engagement with the Philalethes corpus authored by Starkey.</p>

<p>The "fate" of Helmontian chymistry — the subtitle of Newman and Principe's book — was determined by multiple forces. Georg Ernst Stahl's phlogiston theory (c. 1697–1703) was explicitly developed against the Helmontian fermentational program: Stahl's <i>Zymotechnia Fundamentalis</i> presented a mechanistic account of fermentation consciously designed to replace van Helmont's and Willis's vitalistic framework. As phlogiston theory came to dominate European chemistry through the early eighteenth century, the distinctively Helmontian elements — the <i>archeus</i>, ferment vitalism, water monism, the alkahest — lost standing. The subsequent Chemical Revolution associated with [LINK:antoine-lavoisier] (1770s–1789) displaced phlogiston theory in turn, but Lavoisier's new chemistry incorporated little of the Helmontian tradition beyond certain experimental practices. The institutional professionalization of "chemistry" as a discipline in the late eighteenth century, and the accompanying construction of a historiographical narrative that separated chemistry from alchemy, rendered the Helmontian tradition largely invisible until its rehabilitation by Newman, Principe, and others in the late twentieth century.</p>

<h2>Related Concepts</h2>
<p>Helmontian chymistry is closely related to [LINK:chymistry], the broader analytical category Newman and Principe use for the unified early modern tradition; the Helmontian tradition was the dominant form of chymistry in the mid-seventeenth century. It relates to [LINK:iatrochemistry] insofar as van Helmont's chemistry was explicitly medical in application, directed at understanding and treating disease. The concept of [LINK:fermentation] was the central operative mechanism in Helmontian physiology and chemistry. It connects to [LINK:philosophers-stone] as the transmutational goal that Helmontian practitioners, including Starkey, continued to pursue through the new experimental framework van Helmont had established.</p>

<h2>Literature</h2>
<p>Newman, William R. <i>Gehennical Fire: The Lives of George Starkey, an American Alchemist in the Scientific Revolution</i>. Harvard University Press, 1994.<br>
Newman, William R. <i>Atoms and Alchemy: Chymistry and the Experimental Origins of the Scientific Revolution</i>. University of Chicago Press, 2006.<br>
Newman, William R. <i>Newton the Alchemist: Science, Enigma, and the Quest for Nature's "Secret Fire."</i> Princeton University Press, 2019.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Pagel, Walter. <i>Joan Baptista Van Helmont: Reformer of Science and Medicine</i>. Cambridge University Press, 1982.<br>
Principe, Lawrence M. <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i>. Princeton University Press, 1998.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Webster, Charles. <i>The Great Instauration: Science, Medicine, and Reform 1626–1660</i>. Duckworth, 1975.<br>
Hirai, Hiro. <i>Medical Humanism and Natural Philosophy: Renaissance Debates on Matter, Life, and the Soul</i>. Brill, 2011.</p>""",
},

{
'slug': 'phlogiston',
'label': 'Phlogiston',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': (
    "Phlogiston was a theoretical principle posited by Georg Ernst Stahl (c. 1703) to explain "
    "combustion, calcination, and related chemical transformations: a subtle, invisible substance "
    "present in combustible bodies that was released during burning and calcination, leaving behind "
    "a calx (ash or metal oxide). This is an ACTOR_TERM — eighteenth-century chemists explicitly "
    "invoked phlogiston in their theoretical language and structured experimental programs around "
    "its detection and recovery."
),
'definition_long': """\
<p>Phlogiston (from the Greek <i>phlogistós</i>, "burnt" or "inflammable") was a theoretical chemical principle posited by the German chemist and physician Georg Ernst Stahl (1659–1734) to explain combustion, calcination, and related transformations involving fire. Stahl held that combustible substances contained phlogiston as a material component — an invisible, almost weightless "earth of fire" — that was released into the surrounding air during burning. The residue left after combustion (calx, or ash) was the substance minus its phlogiston. In metal calcination, a metal lost phlogiston to become a calx; smelting the calx with charcoal (which Stahl considered rich in phlogiston) restored the phlogiston and returned the metal. This is an ACTOR_TERM: eighteenth-century chemists explicitly named phlogiston, argued about its properties, designed experiments to demonstrate its behavior, and organized systematic chemistry around its transfers. The theory dominated European chemistry from approximately 1703 to 1789, when [LINK:antoine-lavoisier]'s oxygen-based account of combustion displaced it.</p>

<h2>Historical Usage</h2>
<p>The conceptual precursor to phlogiston was the <i>terra pinguis</i> ("fatty earth") of Johann Joachim Becher's <i>Physica Subterranea</i> (1669), which proposed that combustible materials contained a specific earthy principle responsible for their inflammability. Georg Ernst Stahl, who acknowledged and built upon Becher's work, systematized and renamed this principle as phlogiston in his <i>Zymotechnia Fundamentalis</i> (1697) and developed the theory fully in subsequent publications including <i>Fundamenta Chymiae</i> (1723). Stahl's reformulation was significant because it was explicitly directed against the competing "Helmontian" fermentational program of Jan Baptist van Helmont and Thomas Willis: where Helmont had explained combustion and calcination through his vitalistic ferment theory, Stahl offered a materialist mechanism involving a transferable chemical substance. As William R. Newman and Lawrence M. Principe argued in <i>Alchemy Tried in the Fire</i> (2002), Stahl's phlogiston theory should be understood in part as a deliberate displacement of [LINK:helmontian-chymistry].</p>

<p>Phlogiston theory rapidly became the dominant framework in European chemistry. By the mid-eighteenth century, it organized work across combustion, metallurgy, fermentation, and respiration. The theory explained several empirical regularities well: why different materials burned with different intensities (different phlogiston contents), why charcoal was effective in smelting (phlogiston-rich material), why respiration and combustion resembled each other (both involved phlogiston release from organic matter). Herman Boerhaave's influential textbook <i>Elementa Chemiae</i> (1732), which shaped European chemical education for decades, incorporated phlogiston as a foundational principle. British chemists including Joseph Black, Henry Cavendish, Joseph Priestley, and Carl Wilhelm Scheele all worked within the phlogiston framework, even as their experiments — particularly on gases — accumulated anomalies that would ultimately be resolved by rejecting the theory.</p>

<p>The central anomaly was the observation that metals gained weight during calcination: if calcination involved loss of phlogiston, the resulting calx should weigh less, not more. Phlogiston theorists attempted various solutions, including the suggestion (by some, though contested) that phlogiston had negative weight or levity. These solutions were unsuccessful, and the anomalies compounded as Priestley's discovery of "dephlogisticated air" (oxygen, 1774) and Cavendish's experiments on the composition of water created pressure for an alternative account.</p>

<h2>Lavoisier's Overthrow</h2>
<p>Antoine Lavoisier's systematic campaign against phlogiston began in the early 1770s. His key contributions were: (1) demonstrating with precision that substances gain weight during combustion rather than losing it, using sealed vessels and careful weighing; (2) identifying oxygen — which he named from the Greek for "acid-former" — as the substance absorbed during combustion rather than a phlogiston-depleted air; (3) showing that water is composed of oxygen and hydrogen (with Cavendish's data), overthrowing the assumption that water was elementary; and (4) reformulating all of chemistry in terms of oxygen reactions, publishing the results in <i>Traité Élémentaire de Chimie</i> (1789). Lavoisier was explicit that he was not merely revising phlogiston theory but eliminating it — replacing a fictitious substance with observable reactants. His success was swift: by 1800, phlogiston had virtually disappeared from published chemistry.</p>

<p>The transition involved more than experimental results. Lavoisier's new chemical nomenclature, developed with colleagues and published as <i>Méthode de Nomenclature Chimique</i> (1787), systematically removed phlogiston from the vocabulary of chemistry. Substances were renamed according to their composition (oxide of iron rather than calx of iron with phlogiston expelled), making it linguistically awkward to reinstate the older framework. The simultaneous professionalization of chemistry — with new institutions, journals, and curricula — accelerated the paradigm shift.</p>

<h2>Material Dimensions</h2>
<p>In the laboratory, phlogiston theory was operationally productive even though theoretically mistaken. Experiments within the phlogiston framework generated systematic knowledge of combustion, respiration, and metallic chemistry. The apparatus involved included sealed glass vessels for trapping gases, precision balances for weighing reactants and products, furnaces for controlled calcination, and pneumatic troughs for collecting and measuring gases. The color changes associated with calcination and reduction — metal surface to dull powder and back — were observable and reliable markers of phlogiston transactions. Practitioners working within the framework could reproduce experiments, communicate findings, and train students in consistent methods. The chemical knowledge accumulated within the phlogiston framework was not lost when the theory was rejected; it was reinterpreted rather than discarded, and the experimental procedures remained valid.</p>

<h2>Scholarly Significance</h2>
<p>Phlogiston theory occupies a central position in the history and philosophy of science as a major episode of theoretical change. Thomas Kuhn's analysis of scientific revolutions, in <i>The Structure of Scientific Revolutions</i> (1962), treated the Chemical Revolution — the overthrow of phlogiston by Lavoisier — as a paradigm case of paradigm shift. From this perspective, phlogiston theory was a functioning normal science paradigm that accumulated anomalies until a crisis produced a revolutionary reconceptualization. Newman and Principe's historiographical work complicates this narrative: they emphasize the continuities between phlogiston-era chemistry and what preceded and followed it, arguing that the Chemical Revolution should be understood as a transformation within an ongoing practical tradition rather than a complete rupture. The question of whether Lavoisier's [LINK:chymistry] represented a genuine break from or a continuation of earlier chymical practice — including Helmontian and Paracelsian elements — remains an active historiographical debate.</p>

<h2>Related Concepts</h2>
<p>Phlogiston connects to [LINK:calcination] as the primary operation it was invoked to explain: in calcination, phlogiston was supposedly expelled from metal, converting it to calx. It relates to [LINK:helmontian-chymistry] as the theoretical competitor that displaced Helmontian ferment theory from its dominant position in European chemistry around 1700. It also connects to [LINK:operational-chemistry], since phlogiston theory was, for its practitioners, an operational framework for understanding and predicting the outcomes of combustion, smelting, and related processes, even though the underlying ontology proved incorrect. The concept's displacement by Lavoisier's oxygen theory marks the historical boundary between the chymical tradition analyzed by Newman and Principe and the modern chemical discipline.</p>

<h2>Literature</h2>
<p>Stahl, Georg Ernst. <i>Zymotechnia Fundamentalis seu Fermentationis Theoria Generalis</i>. Frankfurt, 1697.<br>
Stahl, Georg Ernst. <i>Fundamenta Chymiae Dogmaticae et Experimentalis</i>. Nuremberg, 1723.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Lavoisier, Antoine-Laurent. <i>Traité Élémentaire de Chimie</i>. Paris, 1789.<br>
Kuhn, Thomas S. <i>The Structure of Scientific Revolutions</i>. University of Chicago Press, 1962.<br>
Partington, J.R. <i>A History of Chemistry</i>. 4 vols. Macmillan, 1961–1970.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Musgrave, Alan. "Why Did Oxygen Supplant Phlogiston? Research Programmes in the Chemical Revolution." In Colin Howson, ed., <i>Method and Appraisal in the Physical Sciences</i>. Cambridge University Press, 1976.<br>
Donovan, Arthur. <i>Antoine Lavoisier: Science, Administration, and Revolution</i>. Cambridge University Press, 1993.</p>""",
},
]

# ---------------------------------------------------------------------------
# 2. NEW TEXTS
# ---------------------------------------------------------------------------

NEW_TEXTS = [
{
'slug': 'ortus-medicinae',
'title': 'Ortus Medicinae (Dawning of Medicine)',
'text_type': 'PRIMARY_SOURCE',
'original_language': 'Latin',
'composition_date': '1648 (posthumous; composed c. 1620–1644)',
'composition_year_start': 1648,
'composition_year_end': 1648,
'analysis_html': """\
<p><i>Ortus Medicinae, vel Opera et Opuscula Omnia</i> (1648; "Dawning of Medicine, or All Works and Minor Works") is the posthumously published collected writings of the Flemish chemist and physician [LINK:jan-van-helmont], compiled and edited by his son Francis Mercury van Helmont and published in Amsterdam by Ludwig Elzevier two years after the elder Helmont's death in 1644. The <i>Ortus Medicinae</i> is the primary source for all of Helmont's major doctrines: his water monism, his gas theory, his ferment physiology, his concept of the <i>archeus</i>, his critique of Galenic medicine and Aristotelian element theory, and his claims about the alkahest and metallic transmutation. It is the foundational text of what William R. Newman and Lawrence M. Principe have called "Helmontian chymistry," the cluster of doctrines that shaped mid-seventeenth century experimental chymistry including the early work of [LINK:george-starkey] and [LINK:robert-boyle].</p>

<h2>Content and Theory</h2>
<p>The <i>Ortus Medicinae</i> is a large, heterogeneous collection of treatises, essays, and fragments unified by recurring theoretical concerns. The most famous single treatise is "Complexionum atque Mistionum Elementalium Figmentum" ("On the Composition and Elemental Mixture of Things"), which contains the account of the willow tree experiment and the argument for water monism. Van Helmont describes planting a five-pound willow sapling in two hundred pounds of dried earth, watering it for five years with rainwater or distilled water, and then reweighing: the tree had gained 164 pounds while the earth had lost barely two ounces. His conclusion — that the plant's substance derived from water — was intended to refute the Aristotelian doctrine that earth was a fundamental principle contributing to plant matter. While the experiment was methodologically flawed (it did not account for air as a source of carbon), its form as a controlled quantitative intervention marks an important moment in the history of experimental design.</p>

<p>Van Helmont's gas theory is developed across several treatises. Coining the word "gas" from the Flemish or Greek word for chaos, he identified "gas sylvestre" (produced by combustion of charcoal and by fermenting wine, later identified as carbon dioxide) and "gas pingue" (a foul gas produced in swamps and intestines, later associated with methane). His insistence that these substances were distinct chemical individuals with specific properties — not simply modified atmospheric air — was a conceptual breakthrough. The identification of chemically distinct gases opened the way for the pneumatic chemistry of Joseph Black (who identified fixed air in the 1750s), Henry Cavendish, Joseph Priestley, and ultimately [LINK:antoine-lavoisier].</p>

<p>The work's medical physiology centers on the concept of <i>fermenta</i> — specific, organizing chemical principles that direct the transformation of ingested food into the particular substances of different organs and body parts. Van Helmont posited an <i>archeus</i>, a vital organizing principle operating at multiple levels (the body as a whole, individual organs, and even individual chemical reactions), that directed these fermentations. This vitalistic chemistry, combining precise empirical observation with a non-mechanistic account of biological organization, was the framework within which [LINK:george-starkey] and early [LINK:robert-boyle] operated, and the framework that Georg Ernst Stahl's phlogiston theory was explicitly designed to displace.</p>

<h2>Composition and Textual Tradition</h2>
<p>Van Helmont composed his treatises across several decades, from approximately the 1610s through the early 1640s. Many were written before his run-in with the Spanish Inquisition over his 1621 publication "De Magnetica Vulnerum Curatione" (on the magnetic cure of wounds by sympathy), which resulted in a long period of house arrest and publication restrictions. The <i>Ortus Medicinae</i> represents his son Francis Mercury van Helmont's effort to gather and publish the complete corpus after his father's death. Several later editions appeared, including a substantially expanded edition in 1652. The text was translated into English as <i>Oriatrike, or Physick Refined</i> by John Chandler in 1662, spreading Helmontian doctrines into the English intellectual community at precisely the moment when the Boyle circle was absorbing and debating them. The Amsterdam publication context is significant: Elzevier was one of Europe's most important academic publishers, giving the <i>Ortus Medicinae</i> immediate prestige and wide distribution across the Republic of Letters.</p>

<h2>Modern Scholarship</h2>
<p>Walter Pagel's <i>Joan Baptista Van Helmont: Reformer of Science and Medicine</i> (Cambridge University Press, 1982) remains the foundational study of the text and its author, situating Helmont within the broader tradition of Renaissance natural philosophy and chemical medicine. Pagel emphasized van Helmont's combination of empirical rigor with mystical and vitalistic commitments, arguing that these were not contradictions but aspects of a coherent anti-Aristotelian program. Hiro Hirai has examined the Neoplatonic and theological dimensions of Helmont's thought, showing how his <i>archeus</i> concept drew on Renaissance debates about the soul and matter. Newman and Principe's <i>Alchemy Tried in the Fire</i> (2002) is the key study of the text's influence on Starkey and Boyle, demonstrating through manuscript evidence that both practitioners absorbed Helmontian doctrines in detail and worked within his theoretical framework. Lawrence Principe's <i>The Secrets of Alchemy</i> (2013) places the <i>Ortus Medicinae</i> within the longer arc of alchemical history, noting van Helmont's claim to have witnessed transmutation as a significant empirical datum in his own framework.</p>

<h2>Literature</h2>
<p>Pagel, Walter. <i>Joan Baptista Van Helmont: Reformer of Science and Medicine</i>. Cambridge University Press, 1982.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Hirai, Hiro. <i>Medical Humanism and Natural Philosophy: Renaissance Debates on Matter, Life, and the Soul</i>. Brill, 2011.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Webster, Charles. <i>The Great Instauration: Science, Medicine, and Reform 1626–1660</i>. Duckworth, 1975.<br>
Partington, J.R. <i>A History of Chemistry</i>. Vol. 2. Macmillan, 1961.</p>""",
},

{
'slug': 'sceptical-chymist',
'title': 'The Sceptical Chymist',
'text_type': 'PRIMARY_SOURCE',
'original_language': 'English',
'composition_date': '1661',
'composition_year_start': 1661,
'composition_year_end': 1661,
'analysis_html': """\
<p><i>The Sceptical Chymist: or Chymico-Physical Doubts and Paradoxes</i> (London, 1661) is the major published work of [LINK:robert-boyle] and one of the most misread texts in the history of science. Published in London by J. Cadwell for J. Crooke while Boyle was resident in Oxford, it takes the form of a dialogue in which the character Carneades challenges the theoretical foundations of the dominant chemical philosophies of the day. The text has been consistently misinterpreted since the nineteenth century as an attack on alchemists and a founding document of modern chemistry's rejection of alchemical thought; Lawrence M. Principe's <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i> (Princeton University Press, 1998) demonstrated that this reading is fundamentally mistaken. The actual targets of Boyle's critique were "vulgar chymists" — Paracelsian pharmaceutical authors and chemical textbook writers — not alchemists pursuing the higher mysteries of transmutation.</p>

<h2>Content and Theory</h2>
<p>The text is structured as a series of dialogues in which Carneades challenges two positions: the Aristotelian four-element theory and the Paracelsian <i>tria prima</i> (salt, sulphur, and mercury as the three principles underlying all matter). Carneades systematically argues that neither theory is well-supported by chemical evidence: Aristotelian elements (earth, water, air, fire) cannot be consistently separated from compound bodies; Paracelsian principles cannot be reproducibly isolated in the form the theory requires. In their place, Carneades proposes a corpuscular account of matter in which substances are composed of tiny, differently shaped particles that combine in various configurations to produce all observable properties — a framework indebted to both ancient atomism and [LINK:jan-van-helmont]'s practical chymistry.</p>

<p>Crucially, Boyle's Carneades explicitly exempts from criticism those "more knowing Chymists" who seek the philosophical principles of metallic transmutation — the adepts. The attack is directed specifically at what Boyle calls "vulgar" or "common" chymists: authors of pharmaceutical chemical texts who uncritically apply the Paracelsian three-principle framework without philosophical rigor, and distillers whose claim to separate "elements" through fire produces only mixed products rather than true principles. As Principe demonstrates, the "alchymists" printed in red on the title page of early editions — which led nineteenth-century historians to conclude Boyle was attacking alchemists — refers in context to a specific subset of practitioners, not to the alchemical tradition as a whole. Boyle himself believed in transmutation and regarded the adept tradition with respect.</p>

<p>The text reflects the deep influence of [LINK:helmontian-chymistry] on Boyle's early thinking. Carneades uses Helmontian examples and vocabulary: the gas (referred to as "gas, as the Helmontians call it"), the alkahest, and several of van Helmont's experimental demonstrations are incorporated into the argument. Boyle's corpuscular matter theory in the <i>Sceptical Chymist</i> is partly a philosophical systematization of Helmontian practical chemistry within a mechanical framework — the move from van Helmont's vitalistic ferment chemistry to a mechanistic corpuscularianism that Boyle saw as completing rather than abandoning Helmont's empirical program.</p>

<h2>Composition and Textual Tradition</h2>
<p>Boyle composed the <i>Sceptical Chymist</i> while based in Oxford, where he had lived since approximately 1655 and where he was part of a circle of natural philosophers associated with what would become the Royal Society. A second, substantially expanded edition appeared in 1680. The text circulated widely in England and on the Continent, appearing in French translation and influencing the development of chemical thought across Europe. Its dialogue form, drawing on classical models, allowed Boyle to present heterodox views through a character (Carneades) without fully committing himself — a rhetorical strategy common in seventeenth-century philosophical writing. Manuscript evidence in the Boyle Papers (Royal Society, London) shows extensive revision and reflects Boyle's ongoing engagement with alchemical and chymical literature during composition.</p>

<h2>Modern Scholarship</h2>
<p>The text's historiographical significance has been radically reframed by Principe's scholarship. In <i>The Aspiring Adept</i> (1998) and related articles, Principe showed that the received interpretation — Boyle heroically rejecting alchemical superstition — was based on selective reading and later projection. Boyle used at least nine different ciphers to conceal his alchemical accounts in his private manuscripts; he believed in transmutation throughout his life; and he attempted to have legislation repealing the English statute against gold-making enacted specifically to enable alchemical practice. Newman and Principe's <i>Alchemy Tried in the Fire</i> (2002) further situated the text within the Helmontian tradition, showing how Starkey's laboratory notebooks contain experiments and conclusions that appear in Boyle's earlier published work. William R. Newman's <i>Atoms and Alchemy</i> (2006) argues that the <i>Sceptical Chymist</i>'s corpuscular framework drew on medieval and early modern alchemical matter theory, particularly the corpuscular version of the [LINK:sulfur-mercury-theory] developed in the <i>Summa Perfectionis</i>.</p>

<h2>Literature</h2>
<p>Principe, Lawrence M. <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i>. Princeton University Press, 1998.<br>
Newman, William R. <i>Atoms and Alchemy: Chymistry and the Experimental Origins of the Scientific Revolution</i>. University of Chicago Press, 2006.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Boas Hall, Marie. <i>Robert Boyle on Natural Philosophy</i>. Indiana University Press, 1965.<br>
Hunter, Michael, and Edward B. Davis, eds. <i>The Works of Robert Boyle</i>. 14 vols. Pickering and Chatto, 1999–2000.</p>""",
},

{
'slug': 'alchemy-tried-in-the-fire',
'title': 'Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry',
'text_type': 'SCHOLARSHIP',
'original_language': 'English',
'composition_date': '2002',
'composition_year_start': 2002,
'composition_year_end': 2002,
'analysis_html': """\
<p><i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i> (University of Chicago Press, 2002) by William R. Newman and Lawrence M. Principe is one of the most consequential works of twentieth-century historiography of science, winner of the 2005 Pfizer Prize from the History of Science Society. The book traces the intellectual trajectory of [LINK:helmontian-chymistry] from its origins in the work of [LINK:jan-van-helmont] through its elaboration by the American-born chymist [LINK:george-starkey] (working under the pseudonym Eirenaeus Philalethes) and its absorption and transformation by [LINK:robert-boyle], concluding with an analysis of the forces — the rise of [LINK:phlogiston] theory, the institutional separation of alchemy from chemistry — that ended the Helmontian tradition. The book is simultaneously a recovery of a forgotten intellectual lineage, a reconstruction of laboratory practice from manuscript evidence, and a major argument about the nature of the Scientific Revolution.</p>

<h2>Central Argument</h2>
<p>The core argument of <i>Alchemy Tried in the Fire</i> is that George Starkey, far from being a marginal figure, was central to the development of early modern experimental chymistry — and that through Starkey, the Helmontian tradition profoundly shaped the work of Robert Boyle, one of the canonical figures of the Scientific Revolution. Newman and Principe demonstrate this through close analysis of Starkey's surviving laboratory notebooks, held at the Wellcome Library and other repositories, which reveal a systematic, quantitative experimental program operating within a coherent Helmontian theoretical framework. They then show that several experiments and conclusions appearing in Boyle's early published work have direct antecedents in Starkey's notebooks, establishing that Starkey was not Boyle's student but, in important respects, his teacher.</p>

<p>The book thus challenges two deeply held historiographical assumptions: first, that alchemy was a pre-scientific precursor that serious practitioners of the Scientific Revolution had to transcend or reject, and second, that Boyle's experimental philosophy represented a clean break from the alchemical tradition. Newman and Principe demonstrate instead that Helmontian chymistry was the most advanced experimental natural philosophy of its period, that it was pursued through rigorous laboratory methods, and that figures including Boyle and [LINK:isaac-newton] absorbed and built upon it. The "fate" of this tradition was not intellectual obsolescence but deliberate marginalization: the construction of a disciplinary "chemistry" in the early eighteenth century involved the retrospective characterization of the alchemical dimension of the Helmontian tradition as non-scientific, a characterization that Newman and Principe argue was motivated by disciplinary politics rather than by the intrinsic quality of the science.</p>

<h2>Methodological Approach</h2>
<p>The book's methodology is distinctive in the history of science: Newman and Principe explicitly undertook laboratory replication of the chemical procedures described in Starkey's notebooks and in the Philalethes texts, in order to determine what the procedures actually produced and whether they corresponded to the allegorical descriptions in published alchemical texts. This combination of archival manuscript work with laboratory replication allowed them to decode Starkey's laboratory language with unusual precision and to demonstrate that alchemical "cover names" corresponded to specific, reproducible chemical operations — not to metaphors, symbols, or spiritual states. This approach extended Lawrence Principe's earlier laboratory work in <i>The Aspiring Adept</i> (Princeton University Press, 1998) and informed William Newman's broader argument in <i>Atoms and Alchemy</i> (University of Chicago Press, 2006) about the operational character of medieval and early modern alchemy.</p>

<h2>Scholarly Impact</h2>
<p>The book's influence has been wide. It established the term "Helmontian chymistry" as a recognized historiographical category, contributed to the consolidation of "chymistry" (with the archaic spelling) as the preferred term for the unified early modern field, and demonstrated that the manuscript evidence for early modern laboratory practice could be read and interpreted with the precision usually reserved for published texts. It inspired subsequent work by historians of science on Starkey, Newton, and Boyle, including Newman's <i>Newton the Alchemist</i> (Princeton University Press, 2019), which applies similar methods to Newton's alchemical manuscripts. The Pfizer Prize recognized it as an outstanding contribution to the history of the life sciences — unusual recognition for work primarily in the history of chemistry and alchemy.</p>

<h2>Literature</h2>
<p>Newman, William R. <i>Gehennical Fire: The Lives of George Starkey, an American Alchemist in the Scientific Revolution</i>. Harvard University Press, 1994.<br>
Newman, William R. <i>Atoms and Alchemy: Chymistry and the Experimental Origins of the Scientific Revolution</i>. University of Chicago Press, 2006.<br>
Newman, William R. <i>Newton the Alchemist: Science, Enigma, and the Quest for Nature's "Secret Fire."</i> Princeton University Press, 2019.<br>
Principe, Lawrence M. <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i>. Princeton University Press, 1998.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>""",
},
]

# ---------------------------------------------------------------------------
# 3. EXPANDED PERSON BIOGRAPHIES
# ---------------------------------------------------------------------------

PERSON_UPDATES = [
{
'slug': 'antoine-lavoisier',
'bio_html': """\
<p>Antoine Laurent Lavoisier (1743–1794) was a French aristocrat, administrator, and natural philosopher whose systematic experimental program overturned phlogiston theory and established the quantitative, compositional framework that defines modern chemistry. Born in Paris to a family of the legal nobility, he received an exceptionally broad education at the Collège Mazarin, studying law, mathematics, botany, geology, and natural philosophy before committing to chemical research in the late 1760s. His election to the Académie Royale des Sciences in 1768, at age twenty-four, provided the institutional base for a career that combined rigorous experimental chemistry with administrative responsibilities as a tax farmer and director of the Gunpowder Administration. Lavoisier was guillotined during the Reign of Terror in 1794, his scientific eminence unable to protect him from the Revolutionary tribunal. Within a decade of his death, his theoretical system had become hegemonic throughout European chemistry.</p>

<h2>Works and Intellectual Context</h2>
<p>Lavoisier's major publications trace a systematic dismantling of phlogiston theory and the construction of a replacement framework based on oxygen. His early memoir "Sur la Nature du Principe qui se combine avec les Métaux pendant leur Calcination" (1774), presented to the Académie, argued that metals absorbed something from the air rather than releasing phlogiston during calcination — a direct challenge to Stahl's dominant account. His identification and naming of oxygen (from Greek for "acid-former") in the early 1780s, drawing on experiments he shared or competed with Joseph Priestley (who had discovered "dephlogisticated air" in 1774), provided the positive principle to replace phlogiston. His demonstration with Laplace using the ice calorimeter (1783) that respiration produced heat and carbon dioxide analogous to combustion connected chemistry to physiology within the oxygen framework.</p>

<p>The collaborative <i>Méthode de Nomenclature Chimique</i> (1787), prepared with Guyton de Morveau, Berthollet, and Fourcroy, replaced the historically accumulated vocabulary of chemistry — names like "butter of antimony," "liver of sulfur," and "phlogisticated nitrous acid" — with a systematic nomenclature based on elemental composition. Oxide of iron, sulfate of copper, carbonate of lime: each name encoded the substance's composition and its relationship to other substances. This nomenclatural reform was not merely linguistic; it made the anti-phlogiston theory grammatically mandatory, since the new names could not be used without implicitly adopting Lavoisier's oxygen-based account of composition. <i>Traité Élémentaire de Chimie</i> (1789) synthesized the reformed chemistry into the first modern chemistry textbook: it listed thirty-three "elements" (substances not yet decomposed), explained all chemical phenomena through oxygen reactions, and presented chemistry as the science of composition and decomposition of substances by weight. The table of elements was notably careful: Lavoisier included "caloric" (heat) as a substance and cautioned that light might be elementary, anticipating the limits of his experimental methods.</p>

<h2>Alchemical and Chymical Context</h2>
<p>The relationship of Lavoisier's chemical revolution to the prior chymical tradition — including [LINK:helmontian-chymistry] — is a significant historiographical question. The standard narrative, originating in early nineteenth-century chemistry histories and reinforced by twentieth-century positivist historiography, portrayed the Chemical Revolution as a sharp rupture: Lavoisier ended the alchemical age by introducing rigorous quantitative methods and a falsifiable theory. William R. Newman, Lawrence M. Principe, and others have substantially complicated this narrative. Newman's <i>Atoms and Alchemy</i> (2006) argues that the conceptual resources Lavoisier deployed — including conservation of matter, elemental composition, and operational analysis — derived partly from the medieval and early modern chymical tradition, including the corpuscular matter theory developed in texts like the <i>Summa Perfectionis</i>. Newman and Principe further note that [LINK:jan-van-helmont]'s gas concept — the identification of chemically distinct gaseous substances with specific properties — was the conceptual prerequisite for Lavoisier's oxygen chemistry: without the Helmontian distinction between different kinds of air, the isolation and characterization of oxygen would have been conceptually impossible.</p>

<p>The institutional dimension of the Chemical Revolution also mattered. By the 1780s, French academic chemistry had already been engaged for decades in the separation of "chemistry" from "alchemy": the Académie des Sciences had excluded transmutational claims from its purview, and chemical textbooks had progressively marginalized alchemical vocabulary. Lavoisier's revolution completed and formalized a process of disciplinary boundary-drawing that had been underway since the early eighteenth century. The framing of the Chemical Revolution as chemistry's liberation from alchemy was partly a retrospective narrative serving chemistry's self-definition as a rigorous science rather than an accurate account of historical causation.</p>

<h2>Scholarly Debates</h2>
<p>Several historiographical debates surround Lavoisier. The question of credit for the discovery of oxygen — between Priestley (who first isolated it), Scheele (who also isolated it independently), and Lavoisier (who theorized its significance) — reflects broader issues about what "discovery" means in science and the difference between empirical isolation and theoretical interpretation. Arthur Donovan's <i>Antoine Lavoisier: Science, Administration, and Revolution</i> (Cambridge University Press, 1993) provides the most comprehensive biography, situating Lavoisier's science within his administrative career and the political context of the late Ancien Régime. Jan Golinski's work on the social dimensions of the Chemical Revolution examines how the new chemistry spread through textbooks, lectures, and institutional reform rather than through experimental demonstration alone. Hasok Chang's revisionary history of phlogiston, in <i>Is Water H2O? Evidence, Realism, and Pluralism</i> (Springer, 2012), argues that the phlogiston framework was not simply refuted but was a functional scientific system that could have been adapted to accommodate the new experimental findings, challenging the narrative of decisive Lavoisier victory. Newman's position — that the Chemical Revolution was a transformation within a continuous chymical practice rather than a rupture from it — has been influential but contested by historians who emphasize the genuine novelty of Lavoisier's quantitative methods and compositional theory.</p>

<h2>Literature</h2>
<p>Donovan, Arthur. <i>Antoine Lavoisier: Science, Administration, and Revolution</i>. Cambridge University Press, 1993.<br>
Bensaude-Vincent, Bernadette, and Isabelle Stengers. <i>A History of Chemistry</i>. Harvard University Press, 1996.<br>
Golinski, Jan. <i>Science as Public Culture: Chemistry and Enlightenment in Britain, 1760–1820</i>. Cambridge University Press, 1992.<br>
Holmes, Frederic L. <i>Lavoisier and the Chemistry of Life</i>. University of Wisconsin Press, 1985.<br>
Newman, William R. <i>Atoms and Alchemy: Chymistry and the Experimental Origins of the Scientific Revolution</i>. University of Chicago Press, 2006.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Chang, Hasok. <i>Is Water H2O? Evidence, Realism, and Pluralism</i>. Springer, 2012.</p>""",
},

{
'slug': 'georg-ernst-stahl',
'bio_html': """\
<p>Georg Ernst Stahl (1659–1734) was a German physician, chemist, and natural philosopher whose phlogiston theory dominated European chemistry for most of the eighteenth century and whose critique of mechanistic medicine established a significant alternative vitalism in the life sciences. Born in Ansbach, Bavaria, Stahl studied medicine at the University of Jena, served as court physician to the Duke of Saxe-Weimar, and in 1694 was appointed to the founding faculty of the newly established University of Halle — one of Prussia's most innovative intellectual institutions — where he held a professorship in medicine until 1716. He then served as physician to the Prussian court in Berlin until his death in 1734. Stahl published extensively on chemistry, fermentation, pharmaceutical preparations, and medical theory, and his influence on eighteenth-century chemistry was second only to Lavoisier's in scope and duration — though, paradoxically, primarily through a theory that was ultimately refuted.</p>

<h2>Works and Intellectual Context</h2>
<p>Stahl's chemical theory derived directly from his engagement with Johann Joachim Becher's <i>Physica Subterranea</i> (Frankfurt, 1669), which proposed three "earths" as the principles of mineralogical and chemical composition, including a <i>terra pinguis</i> ("fatty earth") responsible for combustibility. Stahl renamed Becher's <i>terra pinguis</i> phlogiston — from the Greek for "inflamed" or "set on fire" — and systematized it into a comprehensive theory of combustion and calcination in his <i>Zymotechnia Fundamentalis seu Fermentationis Theoria Generalis</i> (Frankfurt, 1697) and subsequent works. His <i>Fundamenta Chymiae Dogmaticae et Experimentalis</i> (Nuremberg, 1723) presented the mature system: all combustible bodies contain phlogiston; combustion is the release of phlogiston into the air; calcination of metals is the same process — metal loses phlogiston to become a calx; smelting the calx with charcoal (phlogiston-rich) restores the metal. This elegant unified account explained combustion, calcination, reduction, and respiration within a single framework.</p>

<p>Stahl's theory was explicitly directed against what William R. Newman and Lawrence M. Principe have called [LINK:helmontian-chymistry]: the tradition deriving from [LINK:jan-van-helmont]'s vitalistic ferment chemistry, in which chemical transformations were directed by vital organizing principles (<i>archeus</i>, <i>fermenta</i>) rather than by the transfer of material substances. Stahl's <i>Zymotechnia Fundamentalis</i> title announces this opposition — it claims to provide a "fundamental fermentation theory" on materialist rather than vitalist grounds, explicitly contesting van Helmont's and Thomas Willis's accounts of fermentation. As Newman and Principe argue in <i>Alchemy Tried in the Fire</i> (2002), Stahl's phlogiston theory should be understood in part as a deliberate theoretical displacement of the Helmontian tradition that had structured European chymistry through the mid-seventeenth century.</p>

<p>Stahl's medical writings developed a parallel vitalism that paradoxically challenged the mechanistic medicine he associated with Boerhaave and Hoffmann. In his <i>Theoria Medica Vera</i> (Halle, 1708), Stahl argued that the body was governed by a rational <i>anima</i> (soul) that directed all physiological processes, including fermentation, digestion, and the circulation of the blood — a position known as animism. This medical vitalism coexisted with his chemical materialism in phlogiston theory in ways that later commentators found difficult to reconcile, and that reflect the complex layering of mechanistic and vitalistic frameworks in early eighteenth-century natural philosophy.</p>

<h2>Alchemical and Chemical Significance</h2>
<p>Phlogiston theory was operationally productive throughout its reign. Within its framework, chemists including Herman Boerhaave, Joseph Black, Carl Wilhelm Scheele, and Joseph Priestley made substantial empirical advances in pneumatic chemistry, thermal chemistry, and the chemistry of gases — even though their theoretical interpretations were cast in phlogiston terms. Black's discovery of "fixed air" (carbon dioxide), Cavendish's experiments on "inflammable air" (hydrogen), and Priestley's isolation of "dephlogisticated air" (oxygen) were all framed within the phlogiston framework at the time. The conversion of these discoveries into the oxygen-based chemistry of [LINK:antoine-lavoisier] required not just new experimental data but a theoretical reinterpretation of already-known experiments — a process Lavoisier himself described as a "revolution" in chemistry.</p>

<p>Stahl's chemical writing also engaged, at least peripherally, with the transmutational tradition. His position on transmutation was cautious: he neither affirmed nor denied its possibility but concentrated on phenomena that could be reproducibly demonstrated. This stance reflects the broader shift in the early eighteenth century away from explicit transmutational claims as part of respectable chemical publication, a shift driven partly by the institutional separation of chemistry from alchemy in the Académie des Sciences and other learned bodies. The language of Stahl's phlogiston — a substance that could be added to or removed from bodies — retained structural analogies to alchemical principles (sulphur, mercury) even as it abandoned the transmutational goal those principles had served.</p>

<h2>Scholarly Debates</h2>
<p>The historiography of Stahl has been shaped by the need to explain both his theory's dominance and its ultimate failure. Partington's <i>A History of Chemistry</i> (4 vols., Macmillan, 1961–1970) provides the classical account, situating phlogiston theory within the broader chemical tradition and documenting its uptake across Europe. The more recent historiography by Newman and Principe, centered on <i>Alchemy Tried in the Fire</i> (2002), has been important for understanding Stahl's relationship to the Helmontian tradition: their argument that phlogiston theory was a deliberate displacement of Helmontian vitalism has recontextualized Stahl's innovation as a move within a debate rather than a rupture from all that preceded it. Frederic Holmes's work on eighteenth-century chemistry has analyzed the experimental practices within which phlogiston theory was embedded, showing that the theory structured productive laboratory programs even after its anomalies became clear. The question of why phlogiston theory persisted so long despite the weight anomaly (calcination increases the weight of metals, contrary to phlogiston theory's expectation) has been addressed by several historians as a case study in the sociology of scientific knowledge and the resistance of established paradigms to revision.</p>

<h2>Literature</h2>
<p>Stahl, Georg Ernst. <i>Zymotechnia Fundamentalis seu Fermentationis Theoria Generalis</i>. Frankfurt, 1697.<br>
Stahl, Georg Ernst. <i>Theoria Medica Vera</i>. Halle, 1708.<br>
Stahl, Georg Ernst. <i>Fundamenta Chymiae Dogmaticae et Experimentalis</i>. Nuremberg, 1723.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Partington, J.R. <i>A History of Chemistry</i>. Vol. 2. Macmillan, 1961.<br>
Holmes, Frederic L. <i>Eighteenth-Century Chemistry as an Investigative Enterprise</i>. University of California Press, 1989.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Pagel, Walter. <i>Joan Baptista Van Helmont: Reformer of Science and Medicine</i>. Cambridge University Press, 1982.</p>""",
},
]

# ---------------------------------------------------------------------------
# 4. NEW TIMELINE EVENTS
# ---------------------------------------------------------------------------

NEW_EVENTS = [
{
'slug': 'helmont-willow-tree-experiment',
'date_label': 'c. 1634',
'date_start_year': 1634,
'date_end_year': 1638,
'location_slug': 'antwerp',
'description': (
    "c. 1634–1638, Vilvorde (near Brussels): Jan Baptist van Helmont conducted his famous willow tree experiment at his estate in Vilvorde, in the Spanish Netherlands. "
    "Planting a five-pound willow sapling in two hundred pounds of carefully dried soil, he watered it for five years using only rainwater and distilled water, covering the pot to exclude "
    "atmospheric dust. At the end of the period, the tree weighed approximately 164 pounds while the soil had lost barely two ounces. "
    "Van Helmont concluded that the gain in vegetable substance came entirely from water — evidence for his doctrine that water was the primary element underlying all matter, "
    "replacing the Aristotelian four elements. The experiment's form as a controlled, quantitative test of a theoretical claim — tracking inputs and outputs with measured weights "
    "over a defined period — made it methodologically significant even though its conclusion was incorrect (it did not account for carbon absorption from air). "
    "[LINK:jan-van-helmont] published the experiment in [LINK:ortus-medicinae] (1648), where it became one of the most cited demonstrations in seventeenth-century natural philosophy. "
    "William R. Newman and Lawrence M. Principe situated the experiment within the broader Helmontian program in [LINK:alchemy-tried-in-the-fire] (2002), "
    "showing how van Helmont's quantitative method influenced the experimental practice of George Starkey and Robert Boyle."
),
'persons_involved': 'jan-van-helmont',
'texts_involved': 'ortus-medicinae',
'concepts_involved': 'helmontian-chymistry,operational-chemistry',
'scholarly_grounding': (
    "Newman and Principe analyzed the willow tree experiment's influence on Starkey and Boyle in "
    "*Alchemy Tried in the Fire* (2002) ch.1, situating it as the founding demonstration of Helmontian water monism."
),
},

{
'slug': 'helmont-ortus-medicinae-published',
'date_label': '1648',
'date_start_year': 1648,
'date_end_year': 1648,
'location_slug': 'amsterdam',
'description': (
    "1648, Amsterdam: The Flemish chymist Jan Baptist van Helmont's collected writings were published posthumously by his son Francis Mercury van Helmont under the title "
    "[LINK:ortus-medicinae] (Dawning of Medicine), printed by Ludwig Elzevier in Amsterdam two years after the elder Helmont's death. "
    "The volume assembled van Helmont's major treatises on gas theory, ferment physiology, the willow tree experiment, the alkahest (universal solvent), and the nature of disease, "
    "along with his critique of both Aristotelian medicine and Paracelsian chemical philosophy. "
    "Published by one of Europe's most prestigious academic presses, the [LINK:ortus-medicinae] rapidly became a central text in mid-seventeenth-century learned medicine and natural philosophy, "
    "reaching English readers in John Chandler's 1662 translation <i>Oriatrike, or Physick Refined</i>. "
    "Its influence on the Boyle circle in Oxford and London was immediate and substantial: "
    "[LINK:george-starkey] drew on it extensively in his laboratory work, and [LINK:robert-boyle] incorporated Helmontian vocabulary and concepts into his early experiments on air and salts. "
    "Walter Pagel's foundational study of [LINK:jan-van-helmont] demonstrated that the Ortus Medicinae should be read as a coherent anti-Aristotelian program grounded in empirical experiment, "
    "not as a transitional document between alchemy and chemistry."
),
'persons_involved': 'jan-van-helmont',
'texts_involved': 'ortus-medicinae',
'concepts_involved': 'helmontian-chymistry,fermentation',
'scholarly_grounding': (
    "Pagel established the Ortus Medicinae as a coherent experimental program in "
    "*Joan Baptista Van Helmont: Reformer of Science and Medicine* (Cambridge, 1982) ch.1."
),
},

{
'slug': 'starkey-arrives-london-meets-boyle',
'date_label': '1650',
'date_start_year': 1650,
'date_end_year': 1652,
'location_slug': 'london',
'description': (
    "1650–1652, London: George Starkey, a Harvard-educated chymist born in Bermuda, arrived in London and was quickly drawn into the circle of natural philosophers gathering around Samuel Hartlib "
    "— a network that also included [LINK:robert-boyle]. Starkey brought with him an exceptional laboratory training and a deep immersion in [LINK:helmontian-chymistry], "
    "having studied van Helmont's writings in New England and developed a sophisticated experimental program centered on fermentation, distillation, and the preparation of philosophical mercury. "
    "Within months of his arrival, Starkey was corresponding with Boyle and conducting collaborative experiments on acids, salts, and metallic preparations. "
    "William R. Newman's analysis of Starkey's laboratory notebooks in [LINK:alchemy-tried-in-the-fire] (2002, with Principe) reveals that several experiments and conclusions appearing "
    "in Boyle's early published work have direct antecedents in Starkey's notebook entries — establishing that the relationship was less teacher-to-student than a genuine intellectual partnership "
    "in which Starkey's laboratory knowledge shaped Boyle's theoretical ambitions. "
    "Starkey also cultivated the pseudonymous persona of Eirenaeus Philalethes, under which name he published alchemical treatises that were later read and annotated by [LINK:isaac-newton]."
),
'persons_involved': 'george-starkey,robert-boyle',
'texts_involved': 'alchemy-tried-in-the-fire',
'concepts_involved': 'helmontian-chymistry,chymistry',
'scholarly_grounding': (
    "Newman demonstrated Starkey's tutoring of Boyle through notebook analysis in "
    "*Gehennical Fire* (Harvard, 1994) and *Alchemy Tried in the Fire* (2002) ch.2–3."
),
},

{
'slug': 'boyle-publishes-sceptical-chymist',
'date_label': '1661',
'date_start_year': 1661,
'date_end_year': 1661,
'location_slug': 'oxford',
'description': (
    "1661, Oxford/London: [LINK:robert-boyle] published [LINK:sceptical-chymist] (London: J. Cadwell for J. Crooke), a dialogue in which the character Carneades challenges "
    "the theoretical foundations of both Aristotelian four-element theory and Paracelsian tria prima (salt, sulphur, mercury as universal principles). "
    "The text was consistently misread from the nineteenth century onward as an attack on alchemists and a founding document of modern chemistry's rejection of alchemy. "
    "Lawrence M. Principe's analysis in [LINK:alchemy-tried-in-the-fire] (with Newman, 2002) and his earlier <i>The Aspiring Adept</i> (Princeton, 1998) demonstrated that "
    "this interpretation is incorrect: Boyle's actual targets were 'vulgar chymists' — Paracelsian pharmaceutical authors and chemical textbook writers — not practitioners of the higher alchemical art. "
    "Boyle explicitly exempted the 'more knowing Chymists' who sought transmutation, and the text is saturated with [LINK:helmontian-chymistry]: Helmontian gas terminology, the alkahest, "
    "and van Helmont's experimental demonstrations all appear in Carneades' arguments. "
    "The Sceptical Chymist represents not a rejection of alchemy but its transformation: replacing vitalistic Helmontian ferment theory with a mechanistic corpuscular account "
    "of the same empirical terrain."
),
'persons_involved': 'robert-boyle',
'texts_involved': 'sceptical-chymist,alchemy-tried-in-the-fire',
'concepts_involved': 'chymistry,helmontian-chymistry,transmutation',
'scholarly_grounding': (
    "Principe demonstrated the Sceptical Chymist's alchemical commitments and Helmontian framework in "
    "*The Aspiring Adept* (Princeton, 1998) ch.1–2 and *Alchemy Tried in the Fire* (2002) ch.4."
),
},

{
'slug': 'newton-alchemical-research-cambridge',
'date_label': 'c. 1669–1693',
'date_start_year': 1669,
'date_end_year': 1693,
'location_slug': 'cambridge',
'description': (
    "c. 1669–1693, Cambridge: [LINK:isaac-newton] conducted sustained alchemical research at Trinity College, Cambridge, composing and transcribing approximately one million words on chymistry "
    "— among the most extensive alchemical manuscript corpus produced by any single figure in the early modern period. "
    "Newton's primary focus was the Philalethes corpus: the pseudonymous alchemical writings of [LINK:george-starkey], which Newton read, annotated, and copied across three decades of study, "
    "returning repeatedly to the procedure for preparing 'philosophic mercury' that Starkey described in elaborate allegorical language. "
    "Newton also purchased and extensively read a large library of alchemical texts, ran laboratory experiments at the furnace he maintained in the garden behind Trinity College, "
    "and developed his own theory of alchemical vegetation and the 'secret fire' underlying metallic transmutation. "
    "William R. Newman's [LINK:alchemy-tried-in-the-fire] (with Principe, 2002) and his subsequent <i>Newton the Alchemist</i> (Princeton, 2019) demonstrated that Newton's alchemical work "
    "was systematic, quantitative, and experimentally grounded — not a marginal personal obsession — and that his concept of attraction as a force mediating between chemical agents "
    "influenced his development of gravitational theory. "
    "The Chymistry of Isaac Newton Project (Indiana University, directed by Newman) has digitized the full alchemical manuscript corpus."
),
'persons_involved': 'isaac-newton,george-starkey',
'texts_involved': 'alchemy-tried-in-the-fire',
'concepts_involved': 'chymistry,helmontian-chymistry,philosophers-stone',
'scholarly_grounding': (
    "Newman demonstrated Newton's systematic engagement with Starkey's Philalethes texts in "
    "*Newton the Alchemist* (Princeton, 2019) ch.2–4 and *Alchemy Tried in the Fire* (2002) ch.6."
),
},

{
'slug': 'stahl-phlogiston-theory-published',
'date_label': '1697',
'date_start_year': 1697,
'date_end_year': 1697,
'location_slug': 'wittenberg',
'description': (
    "1697, Halle: Georg Ernst Stahl published [LINK:phlogiston] theory in <i>Zymotechnia Fundamentalis seu Fermentationis Theoria Generalis</i> (Frankfurt), "
    "proposing that all combustible bodies contain phlogiston — an invisible, nearly weightless 'fire-stuff' — released during burning and calcination. "
    "The theory was explicitly designed to displace the dominant [LINK:helmontian-chymistry] of Jan Baptist van Helmont and Thomas Willis, "
    "replacing vitalistic ferment theory with a materialist account of chemical transformation. "
    "Stahl elaborated phlogiston theory from his position at the newly established University of Halle, where he held a professorship in medicine from 1694, "
    "and developed it further in <i>Fundamenta Chymiae</i> (1723). "
    "Phlogiston theory provided a unified explanation for combustion, calcination, and metallic reduction: a metal calcined by losing phlogiston; "
    "the calx could be restored to metal by fusion with charcoal (phlogiston-rich) in a furnace, visibly returning what combustion had taken away. "
    "The theory dominated European chemistry for over eighty years, structuring the work of Boerhaave, Black, Priestley, Scheele, and Cavendish, "
    "until [LINK:antoine-lavoisier]'s oxygen-based account of combustion definitively displaced it in the 1780s. "
    "William R. Newman and Lawrence M. Principe argue in [LINK:alchemy-tried-in-the-fire] (2002) that phlogiston theory represents the mechanism by which "
    "Helmontian chymistry was displaced rather than simply superseded by modern chemistry."
),
'persons_involved': 'georg-ernst-stahl',
'texts_involved': 'alchemy-tried-in-the-fire',
'concepts_involved': 'phlogiston,helmontian-chymistry,calcination,operational-chemistry',
'scholarly_grounding': (
    "Newman and Principe analyzed Stahl's explicit displacement of Helmontian fermentation theory in "
    "*Alchemy Tried in the Fire* (2002) ch.7, establishing phlogiston's role in ending the Helmontian tradition."
),
},

{
'slug': 'lavoisier-overthrows-phlogiston',
'date_label': '1783',
'date_start_year': 1783,
'date_end_year': 1783,
'location_slug': 'paris',
'description': (
    "1783, Paris: [LINK:antoine-lavoisier] presented to the Académie Royale des Sciences his demonstration that water is composed of hydrogen and oxygen — "
    "a result that, combined with his earlier experiments on the role of 'eminently respirable air' (oxygen) in combustion, delivered a decisive blow to [LINK:phlogiston] theory. "
    "Lavoisier's argument proceeded from precise quantitative measurements: sealed glass vessels allowed him to weigh reactants and products before and after combustion, "
    "demonstrating the conservation of total matter; the recovery of oxygen from calces (metal oxides) by heating showed that calcination was absorption, not phlogiston release. "
    "He named the active principle in combustion 'oxygen' (from the Greek for acid-former) and argued that all combustion, calcination, and respiration were variations on the same reaction: "
    "combination of a substance with oxygen. "
    "The 1783 demonstration built on Joseph Priestley's discovery of 'dephlogisticated air' (1774) and Henry Cavendish's experiments on 'inflammable air,' "
    "but reinterpreted their results within an oxygen framework that required abandoning phlogiston entirely. "
    "Lavoisier's subsequent reform — the <i>Méthode de Nomenclature Chimique</i> (1787) and <i>Traité Élémentaire de Chimie</i> (1789) — institutionalized the new [LINK:chymistry] framework. "
    "Lawrence Principe and William Newman have argued that the transition involved not a rejection of all prior chemical practice but a reconceptualization of accumulated Helmontian-era experimental knowledge within a new framework."
),
'persons_involved': 'antoine-lavoisier',
'texts_involved': '',
'concepts_involved': 'phlogiston,chymistry,operational-chemistry',
'scholarly_grounding': (
    "Principe situated Lavoisier's Chemical Revolution within the arc of chymical history in "
    "*The Secrets of Alchemy* (2013) ch.6, arguing for continuity as well as rupture with the prior tradition."
),
},

{
'slug': 'lavoisier-traite-elementaire-published',
'date_label': '1789',
'date_start_year': 1789,
'date_end_year': 1789,
'location_slug': 'paris',
'description': (
    "1789, Paris: [LINK:antoine-lavoisier] published <i>Traité Élémentaire de Chimie</i> (Cuchet, Paris), the first modern chemistry textbook and the definitive statement of the oxygen-based chemical system. "
    "The <i>Traité</i> listed thirty-three substances not yet decomposed as 'elements,' replacing the traditional Aristotelian four elements and the Paracelsian tria prima; "
    "it provided systematic accounts of combustion, calx formation, acid formation, and compound analysis all within the oxygen framework; "
    "and it presented chemistry as a science of composition and decomposition verified by weight. "
    "Crucially, the text employed the new nomenclature developed with Guyton de Morveau, Berthollet, and Fourcroy in <i>Méthode de Nomenclature Chimique</i> (1787), "
    "in which substance names encoded composition rather than historical accident — making the anti-phlogiston theory grammatically mandatory. "
    "The <i>Traité</i> was immediately translated into English, German, Spanish, and Italian, spreading the reformed chemistry across Europe within years. "
    "William R. Newman's <i>Atoms and Alchemy</i> (2006) argues that Lavoisier's compositional approach to elements had conceptual roots in the medieval and early modern chymical tradition, "
    "including the matter theory of the [LINK:summa-perfectionis] and the operational chemistry of [LINK:helmontian-chymistry]. "
    "The publication of the <i>Traité</i> in the same year as the French Revolution's outbreak is historically significant: "
    "Lavoisier's chemical revolution coincided with and prefigured the political transformation that would shortly claim his life."
),
'persons_involved': 'antoine-lavoisier',
'texts_involved': 'summa-perfectionis',
'concepts_involved': 'phlogiston,chymistry,operational-chemistry,helmontian-chymistry',
'scholarly_grounding': (
    "Newman argued for conceptual continuity between the chymical tradition and Lavoisier's chemistry in "
    "*Atoms and Alchemy* (2006) ch.5, connecting Helmontian and medieval matter theory to Lavoisier's compositional approach."
),
},
]

# ---------------------------------------------------------------------------
# LOAD FUNCTIONS
# ---------------------------------------------------------------------------

def load_all():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # 1. Concepts
    print("=== Loading new concepts ===")
    for concept in NEW_CONCEPTS:
        c.execute("""
            INSERT INTO concepts (slug, label, category_type, operation_type, definition_short, definition_long,
                                  source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, 'AI_ASSISTED', 'DRAFT', 'MEDIUM')
            ON CONFLICT(slug) DO UPDATE SET
                label=excluded.label, category_type=excluded.category_type,
                definition_short=excluded.definition_short, definition_long=excluded.definition_long,
                source_method=excluded.source_method, review_status=excluded.review_status
        """, (concept['slug'], concept['label'], concept['category_type'], concept['operation_type'],
              concept['definition_short'], concept['definition_long']))
        print(f"  [OK] concept: {concept['slug']}")

    # 2. Texts
    print("\n=== Loading new texts ===")
    for text in NEW_TEXTS:
        c.execute("""
            INSERT INTO texts (slug, title, text_type, original_language, composition_date,
                               composition_year_start, composition_year_end, analysis_html,
                               source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'AI_ASSISTED', 'DRAFT', 'MEDIUM')
            ON CONFLICT(slug) DO UPDATE SET
                title=excluded.title, text_type=excluded.text_type, original_language=excluded.original_language,
                composition_date=excluded.composition_date, composition_year_start=excluded.composition_year_start,
                composition_year_end=excluded.composition_year_end, analysis_html=excluded.analysis_html,
                source_method=excluded.source_method, review_status=excluded.review_status
        """, (text['slug'], text['title'], text['text_type'], text['original_language'],
              text['composition_date'], text['composition_year_start'], text['composition_year_end'],
              text['analysis_html']))
        print(f"  [OK] text: {text['slug']}")

    # 3. Person bio updates
    print("\n=== Updating person biographies ===")
    for person in PERSON_UPDATES:
        c.execute("UPDATE persons SET bio_html=?, source_method='AI_ASSISTED', review_status='DRAFT' WHERE slug=?",
                  (person['bio_html'], person['slug']))
        print(f"  [OK] person bio updated: {person['slug']}")

    # 4. Fix van Helmont era
    print("\n=== Fixing van Helmont era ===")
    c.execute("UPDATE persons SET era='EARLY_MODERN' WHERE slug='jan-van-helmont'")
    print("  [OK] jan-van-helmont era: MEDIEVAL → EARLY_MODERN")

    # 5. Timeline events
    print("\n=== Loading new timeline events ===")
    for event in NEW_EVENTS:
        c.execute("""
            INSERT INTO timeline_events (slug, date_label, date_start_year, date_end_year, location_slug,
                                         description, persons_involved, texts_involved, concepts_involved,
                                         scholarly_grounding, source_method, review_status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'AI_ASSISTED', 'DRAFT', 'MEDIUM')
            ON CONFLICT(slug) DO UPDATE SET
                date_label=excluded.date_label, date_start_year=excluded.date_start_year,
                date_end_year=excluded.date_end_year, location_slug=excluded.location_slug,
                description=excluded.description, persons_involved=excluded.persons_involved,
                texts_involved=excluded.texts_involved, concepts_involved=excluded.concepts_involved,
                scholarly_grounding=excluded.scholarly_grounding
        """, (event['slug'], event['date_label'], event['date_start_year'], event.get('date_end_year'),
              event['location_slug'], event['description'], event.get('persons_involved', ''),
              event.get('texts_involved', ''), event.get('concepts_involved', ''),
              event.get('scholarly_grounding', '')))
        print(f"  [OK] event: {event['slug']}")

    conn.commit()
    conn.close()
    print("\n=== All done ===")


if __name__ == '__main__':
    load_all()
