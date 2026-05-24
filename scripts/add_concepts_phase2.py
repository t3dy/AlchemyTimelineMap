#!/usr/bin/env python3
"""add_concepts_phase2.py — Add new concept definitions to reach 30+ concepts"""
import sqlite3

DB = 'db/alchemy_timeline.db'

NEW_CONCEPTS = [
{
'slug': 'philosophers-stone',
'label': "Philosopher's Stone",
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "The Philosopher's Stone (Latin: <i>lapis philosophorum</i>) was the central goal of Western alchemy: a substance believed capable of transmuting base metals into gold or silver, curing all diseases, and conferring longevity or immortality. This is an ACTOR_TERM — historical practitioners explicitly sought this substance and would recognize the concept under this name.",
'definition_long': """<p>The Philosopher's Stone (Latin: <i>lapis philosophorum</i>; Arabic: <i>al-iksīr</i>, whence "elixir") was the supreme goal of Western alchemical practice: a substance, variously conceived as a powder, a tincture, a liquid, or a solid, believed to be capable of transmuting base metals into gold or silver, healing all diseases, and conferring extended life or immortality on its possessor. This is an ACTOR_TERM — historical practitioners explicitly used this term and regarded the pursuit of the Stone as the central and legitimating goal of the alchemical art. The term appears across the full chronological and geographical range of the alchemical tradition, from early Greek texts attributed to pseudo-Democritus through Arabic alchemy, medieval Latin alchemy, Renaissance emblem books, and early modern laboratory practice. Lawrence Principe has argued that the Stone should be understood as a genuinely sought experimental goal rather than as pure metaphor or psychological symbol, and that laboratory practitioners attempted to prepare it according to specific, reproducible procedures.</p>

<h2>Historical Usage</h2>
<p>The concept of a transformative substance capable of converting base metals into noble ones appears in the earliest Greek alchemical texts, associated with the figure of the "divine water" or "universal solvent" that could dissolve and recombine material substances. In Arabic alchemy, the concept was systematized: <i>al-iksīr</i> (elixir) was a specific preparation — sometimes identified with the Red Elixir (for gold transmutation) and the White Elixir (for silver transmutation) — produced through elaborate sequences of operations including calcination, sublimation, dissolution, and congelation. [LINK:jabir-ibn-hayyan]'s corpus devoted extensive attention to the theory and preparation of the elixir, grounding its possibility in the sulphur-mercury theory of metallic composition: if metals differed only in the ratio and purity of their sulphur and mercury components, a prepared elixir capable of correcting these ratios could convert any metal to gold.</p>

<p>In Latin medieval alchemy, the Stone was conceptualized in multiple registers simultaneously. As a practical chemical goal, it was a specific preparation of mercury and sulphur (or, in later accounts, of a sophic mercury prepared through elaborate processing) that would function as a catalyst for metallic transmutation when projected onto molten base metal. As a theoretical object, it was the endpoint of the alchemical process — the most perfect form of matter, embodying the pure formal principle of gold in concentrated form. As a theological allegory, it was associated by many medieval writers with Christ as the cornerstone of creation, with the Holy Spirit as the animating principle of transformation, and with the process of spiritual redemption paralleling the material purification of base metal. [LINK:george-ripley]'s twelve-gate allegorical poem structured the process of making the Stone across twelve stages corresponding to alchemical operations and spiritual states.</p>

<p>In the early modern period, the Stone remained an active experimental goal. [LINK:george-starkey] devoted his career to preparing a "sophick mercury" that he identified as the first stage toward the Stone, following procedures derived from the pseudonymous Eirenaeus Philalethes corpus. [LINK:isaac-newton] read and annotated Starkey's Philalethes texts extensively and conducted his own laboratory investigations aimed at preparing similar materials. [LINK:robert-boyle] claimed to have witnessed transmutation performed with the Stone on at least one occasion and treated the possibility of the Stone's existence as an open empirical question consistent with his corpuscular theory of matter.</p>

<h2>Scholarly Significance</h2>
<p>The Philosopher's Stone presents distinctive historiographical challenges. William R. Newman has argued forcefully that the Stone should be treated as a genuine experimental goal — that practitioners were attempting real chemical preparations and were using specific, describable procedures — rather than as pure allegory or delusion. Newman's laboratory-historical work, particularly on Starkey's notebooks, demonstrates that alchemical laboratory practice aimed at the Stone was systematic and experimental in a meaningful sense. Lawrence Principe's laboratory replication work has confirmed that several procedures described in alchemical texts for preparing precursors to the Stone correspond to genuine, reproducible chemical reactions. This "practical" interpretation stands against older historiographies that treated the Stone either as a transparent fraud or as exclusively a spiritual or psychological symbol (the Jungian interpretation).</p>

<p>Michela Pereira has examined the Stone in the context of medieval natural philosophy, showing how alchemical theorists integrated the concept into Aristotelian frameworks of substantial form and material change: if the Stone embodied the pure form of gold, its "projection" onto base metal would induce the formal change from lead-form or iron-form to gold-form, a process theoretically coherent within scholastic natural philosophy. The pseudo-Lullian corpus, analyzed by Pereira, developed an elaborate theory of the Stone as a medicine for metals parallel to the universal medicine (elixir of life) for human bodies.</p>

<h2>Related Concepts</h2>
<p>The Philosopher's Stone is closely connected to [LINK:transmutation] as its practical application: the Stone is the agent; transmutation is the result. It relates to [LINK:sublimation], [LINK:calcination], and [LINK:distillation] as the primary operations through which the Stone was prepared. The concept of [LINK:quintessence] shares the Stone's character as a distilled or purified essence representing the highest form of a class of substances. The [LINK:sulfur-mercury-theory] provided the theoretical foundation for why a prepared Stone could transmute metals.</p>

<h2>Literature</h2>
<p>Newman, William R. <i>Gehennical Fire: The Lives of George Starkey, an American Alchemist in the Scientific Revolution</i>. Harvard University Press, 1994.<br>
Newman, William R. <i>Newton the Alchemist</i>. Princeton University Press, 2019.<br>
Pereira, Michela. <i>The Alchemical Corpus Attributed to Raymond Lull</i>. Warburg Institute, 1989.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Principe, Lawrence M. <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i>. Princeton University Press, 1998.<br>
Thorndike, Lynn. <i>A History of Magic and Experimental Science</i>. 8 vols. Columbia University Press, 1923–1958.</p>"""
},

{
'slug': 'sulfur-mercury-theory',
'label': 'Sulfur-Mercury Theory',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "The sulfur-mercury theory held that all metals are composed of two elemental principles — sulphur (responsible for combustibility, color, and quality) and mercury (responsible for fusibility, luster, and metallic character) — in varying ratios and degrees of purity. This is an ACTOR_TERM — historical practitioners invoked these principles to explain metallic differences and the possibility of transmutation.",
'definition_long': """<p>The sulfur-mercury theory held that all metals are composed of two elemental principles — philosophical sulphur (responsible for combustibility, color, and specific quality) and philosophical mercury (responsible for fusibility, luster, and the metallic character common to all metals) — combined in varying proportions and with varying degrees of purity. This is an ACTOR_TERM: the theory was explicitly articulated and deployed by historical practitioners as the dominant explanatory framework for metallic composition and transformation in Arabic and Latin medieval alchemy. The "sulfur" and "mercury" of the theory were not necessarily the physical substances of those names — though they were related to them — but rather ideal principles or essences of which the physical materials were impure embodiments. As Lawrence Principe has emphasized, practitioners recognized this distinction clearly and argued that it made the theory more, not less, explanatorily powerful.</p>

<h2>Historical Usage</h2>
<p>The theory originated in Arabic alchemy, probably developed from earlier Greek theories of metallic generation involving dry and moist exhalations (following Aristotle's <i>Meteorologica</i>), and was systematized in texts attributed to [LINK:jabir-ibn-hayyan] and definitively formulated in [LINK:avicenna]'s mineralogical writings (the <i>De Mineralibus</i>). In Avicenna's version — which became the standard scholastic account in Latin Europe through the translation of [LINK:gerard-of-cremona] — all metals form underground through the interaction of dry, sulphurous exhalations and moist, mercurial vapors; the specific ratio and purity of these exhalations determines which metal forms. Gold forms when the ratio and purity are perfect; the other metals are imperfect approximations of gold's ideal combination. This account simultaneously explained why metals resemble one another (shared mercury component), differ from one another (different sulphur ratios), and why gold excels all others (perfect composition).</p>

<p>The sulphur-mercury theory immediately suggested the theoretical possibility of transmutation: if base metals differed from gold only in the ratio and purity of their sulphur and mercury components, then correcting these ratios — by purifying and adjusting the components — could convert base metal to gold. This inference, drawn explicitly in the Arabic alchemical tradition, provided the theoretical foundation for the alchemical goal of transmutation and for the concept of the [LINK:philosophers-stone] as an agent capable of performing this correction. The theory thus made the alchemical project theoretically coherent within the dominant natural philosophy of the medieval period.</p>

<p>In Latin medieval alchemy, the sulphur-mercury theory was transmitted through multiple channels, including the [LINK:emerald-tablet] commentary tradition, the [LINK:summa-perfectionis] (attributed to pseudo-Geber), and numerous shorter texts. The <i>Summa Perfectionis</i>, analyzed by William Newman, presented a sophisticated development of the theory that proposed a corpuscular account of metallic composition: sulphur and mercury components exist as tiny particles that combine in specific configurations to produce metallic textures. This corpuscular version of the theory, Newman argues, represents a genuine predecessor of the corpuscular matter theory of the Scientific Revolution.</p>

<h2>Scholarly Significance</h2>
<p>William Newman has argued that the sulphur-mercury theory, particularly in its corpuscular form as developed in the <i>Summa Perfectionis</i>, represents a significant theoretical contribution to the history of matter theory, providing a sophisticated account of material constitution that influenced Robert Boyle's corpuscular philosophy. Lawrence Principe has situated the theory within the laboratory practice of alchemical practitioners, showing how it structured experimental work: practitioners attempted to identify and isolate the sulphur and mercury components of metals, purify them, and recombine them in the proportions required for gold. The theory was not merely speculative but operationally generative — it suggested specific experimental programs.</p>

<h2>Related Concepts</h2>
<p>The sulfur-mercury theory is the theoretical framework within which [LINK:transmutation] was understood as possible. It connects directly to [LINK:calcination] and [LINK:sublimation] as operations for separating and purifying the sulphur and mercury components of metals. The Paracelsian <i>tria prima</i> — sulfur, mercury, salt — extended the binary theory by adding salt as a third principle associated with bodily stability. This concept also relates to [LINK:operational-chemistry] as the primary theoretical framework guiding laboratory operations.</p>

<h2>Literature</h2>
<p>Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber</i>. Brill, 1991.<br>
Newman, William R. <i>Atoms and Alchemy: Chymistry and the Transformation of Matter</i>. University of Chicago Press, 2006.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Ullmann, Manfred. <i>Die Natur- und Geheimwissenschaften im Islam</i>. Brill, 1972.</p>"""
},

{
'slug': 'putrefaction',
'label': 'Putrefaction',
'category_type': 'ACTOR_TERM',
'operation_type': 'PUTREFACTION',
'definition_short': "Putrefaction (<i>putrefactio</i>) was an alchemical operation in which a substance was subjected to slow decomposition under controlled conditions — typically moist heat in a sealed vessel — to break down its current form and prepare it for reconstitution in a purer or more elevated state. This is an ACTOR_TERM: historical practitioners recognized and named this operation explicitly.",
'definition_long': """<p>Putrefaction (<i>putrefactio</i>; also called <i>nigredo</i>, "blackening," in the color-stage symbolism of later alchemy) was an alchemical operation in which a substance — typically a metallic amalgam, a mineral preparation, or a plant material — was subjected to prolonged slow decomposition under controlled conditions, usually involving gentle moist heat in a sealed vessel, producing a dark, malodorous mass that was understood as the necessary preliminary to reconstitution and elevation into a purer form. This is an ACTOR_TERM: historical practitioners explicitly named, described, and performed this operation, and they recognized it as a distinct stage in alchemical processes. The operation was grounded in analogy with natural processes of decomposition and regeneration — seeds rotting before germinating, winter preceding spring — and these agricultural analogies were central to the theoretical justification for putrefaction as necessary for alchemical regeneration.</p>

<h2>Historical Usage</h2>
<p>Putrefaction appears in the earliest Greek alchemical texts as one of the fundamental operations of the art. The pseudo-Democritean tradition described the blackening of materials subjected to "melanosis" (blackening) as the first stage of the dyeing and transmutation process. [LINK:zosimos-of-panopolis]'s visions, with their imagery of priests being consumed, boiled, and reconstituted, can be read as allegorical representations of putrefaction and resurrection as stages in alchemical transformation. In Arabic alchemy, putrefaction was integrated into systematic accounts of the alchemical process, and [LINK:jabir-ibn-hayyan]'s corpus described the controlled decomposition of sulphur-mercury mixtures as a necessary preliminary to their reconstitution in a more perfect form.</p>

<p>In medieval Latin alchemy, putrefaction became one of the canonical stages of the Great Work, typically placed after the initial combination of materials and before the stages of whitening (<i>albedo</i>) and reddening (<i>rubedo</i>). [LINK:george-ripley]'s twelve-gate allegorical poem positioned "Putrefaction" as the fifth gate, following Calcination, Dissolution, Separation, and Conjunction, and preceding Congelation, Cibation, and Sublimation. The laboratory correlate of putrefaction in this tradition was the production of a dark, decomposed mixture in a sealed vessel maintained at low, steady heat — what later practitioners called the "philosophical egg" kept at "horse-dung heat" (the gentle warmth of fermenting manure). The production of a uniformly black, moist mass was the observable sign that putrefaction had been achieved and the next stage could begin.</p>

<p>In Paracelsian alchemy, putrefaction retained its importance but was reframed: the decomposition of materials was understood as the dissolution of their individual form to reveal the universal matter underlying all substances, which could then be directed by the alchemist's art toward new, more perfect formations. [LINK:jan-van-helmont]'s concept of the <i>archeus</i> — an organizing vital principle directing biological processes — made putrefaction the stage at which the old organizing principle was dissolved, leaving the matter free to receive a new one.</p>

<h2>Scholarly Significance</h2>
<p>Lawrence Principe's laboratory-historical work has shown that the "putrefaction" described in alchemical texts often corresponds to genuine chemical phenomena: the production of dark sulfide or organic decomposition products under moist heat, the formation of amorphous black masses from metallic salts, and the slow reactions of sulfur with metals. These processes are chemically real and observable; alchemical descriptions of them are not mere fantasy. William Newman has situated putrefaction within the broader context of alchemical matter theory, showing how it was understood as the dissolution of a specific metallic form in preparation for reconstitution — a process theoretically coherent within the sulphur-mercury framework.</p>

<h2>Related Concepts</h2>
<p>Putrefaction is closely related to [LINK:calcination] as both are operations that break down the current structure of a substance, though calcination uses dry heat while putrefaction uses moist heat in a sealed vessel. It is a necessary precursor to subsequent operations of purification and reconstitution including [LINK:sublimation] and [LINK:distillation]. The concept of [LINK:transmutation] as the final goal of the Great Work requires putrefaction as one of its preparatory stages. In the color-stage symbolism of later alchemy, putrefaction corresponds to the <i>nigredo</i>, which precedes the <i>albedo</i> and <i>rubedo</i>.</p>

<h2>Literature</h2>
<p>Abraham, Lyndy. <i>A Dictionary of Alchemical Imagery</i>. Cambridge University Press, 1998.<br>
Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber</i>. Brill, 1991.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Principe, Lawrence M., and William R. Newman. "Some Problems with the Historiography of Alchemy." In <i>Secrets of Nature</i>, edited by William R. Newman and Anthony Grafton. MIT Press, 2001.</p>"""
},

{
'slug': 'projection',
'label': 'Projection',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "Projection was the final stage of alchemical transmutation, in which a small quantity of the Philosopher's Stone or prepared tincture was cast onto molten base metal to convert it into gold or silver. This is an ACTOR_TERM: practitioners specifically named this act of casting or projecting the Stone as the culminating act of the Great Work.",
'definition_long': """<p>Projection was the culminating operation of the alchemical Great Work: the act of casting or projecting a small quantity of the prepared [LINK:philosophers-stone] or "tincture" onto a quantity of molten base metal to convert it into gold or silver. This is an ACTOR_TERM — historical practitioners explicitly used this term for the act of applying the finished Stone to effect transmutation, and the term appears across the alchemical literature from the Arabic tradition through medieval Latin and early modern European alchemy. The extraordinary efficiency of the Stone, as claimed in the tradition, was expressed through the concept of "multiplication": a small quantity of Stone could project its form onto a much larger quantity of metal, and could itself be multiplied further before use. Claims of successful projection — witnessed events of transmutation, sometimes reported by credible observers — were a recurring feature of alchemical discourse and a significant element in debates about the art's legitimacy.</p>

<h2>Historical Usage</h2>
<p>The concept of projection appears in Arabic alchemical texts as the application of the prepared elixir (<i>al-iksīr</i>) to metallic substrates. The sulphur-mercury theory of metallic composition provided the theoretical framework: the Stone, embodying the perfect formal principle of gold in concentrated form, could induce the formal change from base metal to gold when brought into contact with the molten base metal, in the same way that a small quantity of leaven raises a large mass of dough. [LINK:jabir-ibn-hayyan]'s corpus described the projection of prepared tinctures onto metallic substrates, and Arabic texts regularly distinguished between the "medicine for metals" (producing transmutation) and the "medicine for bodies" (the elixir of life for healing).</p>

<p>In medieval Latin alchemy, projection was the final stage after the lengthy preparatory work of producing the Stone. [LINK:george-ripley]'s twelve-gate poem placed "Projection" as the twelfth and final gate, following Calcination, Dissolution, Separation, Conjunction, Putrefaction, Congelation, Cibation, Sublimation, Fermentation, Exaltation, and Multiplication. The expectation was that a successful projection would be dramatic and observable: molten lead or mercury in a crucible would be transformed visibly when the Stone was cast upon it, producing a mass of gold that could be tested by assay. Reports of successful projection — from [LINK:nicholas-flamel] to [LINK:jan-van-helmont] to various early modern court alchemists — were significant claims that drove continued interest and patronage.</p>

<h2>Scholarly Significance</h2>
<p>Lawrence Principe has examined historical accounts of projection with careful historical skepticism: not dismissing all claims as deliberate fraud, but analyzing the epistemological framework within which claims of witnessed transmutation were made and evaluated. In a period before reliable analytical chemistry, distinguishing between a genuine transmutation and a well-executed fraud (using gold-containing alloys, selective analysis, or prepared apparatus) was genuinely difficult; even sophisticated observers could be deceived. William Newman's work on [LINK:george-starkey] has shown that at least some alchemists approaching projection were engaged in genuine experimental inquiry aimed at producing the Stone, rather than performing deliberate deception — though their experimental goals were ultimately unachievable within the laws of chemistry as we now understand them.</p>

<h2>Related Concepts</h2>
<p>Projection is the culminating application of the [LINK:philosophers-stone] and the practical realization of [LINK:transmutation]. It follows the "multiplication" of the Stone (increasing its quantity and power through further operations) and requires the prior successful completion of the entire sequence of alchemical operations. The concept of "fermentation" in some alchemical traditions refers to a preliminary stage of activation of the Stone before projection.</p>

<h2>Literature</h2>
<p>Newman, William R. <i>Gehennical Fire</i>. Harvard University Press, 1994.<br>
Principe, Lawrence M. <i>The Aspiring Adept: Robert Boyle and His Alchemical Quest</i>. Princeton University Press, 1998.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>"""
},

{
'slug': 'chymistry',
'label': 'Chymistry',
'category_type': 'ANALYST_TERM',
'operation_type': None,
'definition_short': "Chymistry is a modern historiographical term introduced by William R. Newman and Lawrence M. Principe to refer to the unified practical and theoretical tradition of laboratory chemical investigation in the early modern period (roughly 1400–1750) before the disciplinary separation of alchemy and chemistry. This is an ANALYST_TERM: historical practitioners did not use this label; it is a retrospective scholarly category.",
'definition_long': """<p>Chymistry (also spelled "chymistry" to distinguish it from "chemistry" with its retrospective disciplinary connotations) is a modern scholarly analytical term introduced by William R. Newman and Lawrence M. Principe to designate the unified practical and theoretical tradition of laboratory chemical investigation in the early modern period, roughly from the fifteenth through the mid-eighteenth century, before the disciplinary boundaries between alchemy and chemistry were established in the late eighteenth century. This is an ANALYST_TERM: historical practitioners in this period did not use "chymistry" as a term to distinguish their work from "alchemy" in the way modern historians might; the term is a retrospective scholarly category designed to overcome the anachronistic projection of the alchemy/chemistry distinction back onto a period in which that distinction did not yet exist.</p>

<h2>Origins and Terminological History</h2>
<p>The term reflects a deliberate historiographical intervention. Earlier histories of chemistry — from the 1780s through much of the twentieth century — typically narrated the history of the field as a progressive emergence of "true chemistry" from the fog of alchemical superstition, culminating in Antoine Lavoisier's "Chemical Revolution" of the 1780s. This narrative projected a sharp distinction between alchemy (associated with transmutation, secrecy, fraud, and mysticism) and chemistry (associated with experiment, publication, and rational method) back into the early modern period, where it distorted the actual historical record. In practice, practitioners in the sixteenth and seventeenth centuries who performed laboratory operations on metals, minerals, plants, and gases did not regard themselves as doing two different things — "alchemy" and "chemistry" — but as participating in a single learned tradition of chemical investigation that encompassed transmutation, medicine, metallurgy, and natural philosophy.</p>

<p>Newman and Principe's collaborative work — most fully articulated in <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i> (2002) and in their separate monographs — demonstrated through archival and laboratory-historical research that figures like [LINK:robert-boyle] and [LINK:george-starkey] did not regard their work as divided between alchemical and chemical components. Boyle's corpuscular philosophy was used to justify transmutational goals; Starkey's laboratory notebooks show the same experimental methods applied to transmutational and pharmaceutical goals. The introduction of "chymistry" as a term for their unified practice is intended to restore the historical integrity of this tradition.</p>

<h2>Scholarly Significance</h2>
<p>The chymistry concept has been broadly influential in the history of science. It has licensed a reassessment of the relationship between early modern alchemy and the Scientific Revolution: rather than treating alchemy as an obstacle to the development of modern science that had to be overcome, historians now recognize the practical laboratory culture of alchemical chymistry as a major source of the experimental methods, instrumentation, and conceptual vocabulary that early modern natural philosophy drew on. Pamela Smith's work on artisanal epistemology complements the chymistry argument by showing that the practical knowledge of workshop practitioners — metallurgists, assayers, distillers — was a major resource for the new natural philosophy, not merely background noise.</p>

<p>The term has occasionally attracted criticism for potentially obscuring real differences between different kinds of practice in the early modern period. Some historians argue that distinctions between transmutational alchemy and analytical or pharmaceutical chemistry were meaningful to some practitioners, even if not universal; the chymistry concept risks flattening these distinctions. Newman and Principe have acknowledged this tension while maintaining that the unified term is historiographically more accurate than imposing the alchemy/chemistry distinction anachronistically.</p>

<h2>Related Concepts</h2>
<p>[LINK:operational-chemistry] is the broader category within which chymistry fits — the tradition of practical laboratory investigation of material change. The [LINK:yates-paradigm] represents the older historiographical approach that chymistry historiography was partly designed to correct. [LINK:artisanal-epistemology] provides the social-historical context for understanding why chymistry as unified practice made sense in early modern culture. [LINK:paracelsian-alchemy] represents one major strand within the chymical tradition.</p>

<h2>Literature</h2>
<p>Newman, William R. <i>Atoms and Alchemy: Chymistry and the Transformation of Matter</i>. University of Chicago Press, 2006.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire: Starkey, Boyle, and the Fate of Helmontian Chymistry</i>. University of Chicago Press, 2002.<br>
Newman, William R., and Lawrence M. Principe. "Alchemy vs. Chemistry: The Etymological Origins of a Historiographic Mistake." <i>Early Science and Medicine</i> 3 (1998): 32–65.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Smith, Pamela H. <i>The Body of the Artisan: Art and Experience in the Scientific Revolution</i>. University of Chicago Press, 2004.</p>"""
},

{
'slug': 'prima-materia',
'label': 'Prima Materia (First Matter)',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "Prima materia (Latin: first matter; also called hyle or the philosophical chaos) was the undifferentiated primordial matter from which all substances derived, and which alchemists sought to return metals to in order to reconstitute them in a purer form. This is an ACTOR_TERM — historical practitioners explicitly invoked this concept as the theoretical ground for understanding material transformation.",
'definition_long': """<p>Prima materia (Latin: first matter; also called <i>hyle</i>, from the Greek, or the "philosophical chaos") was the undifferentiated, qualityless primordial matter that Aristotelian natural philosophy posited as the substratum underlying all physical substances, receiving various forms to produce the specific bodies of the natural world. In alchemical theory, prima materia played a crucial role: it was the material foundation to which metals could theoretically be returned through alchemical dissolution or putrefaction, freeing them from their current specific form and making them available for reconstitution in a purer or more perfect form. This is an ACTOR_TERM — historical practitioners explicitly invoked this Aristotelian concept and argued that their operations engaged with prima materia as a real, laboratory-accessible substrate, not merely a philosophical abstraction.</p>

<h2>Historical Usage</h2>
<p>The concept derives from Aristotle's hylomorphism: all material substances consist of matter and form; matter (hyle, prima materia) is in itself qualityless, the pure potentiality for receiving any form. In his natural philosophy, prima materia never actually exists without some form — it is always already the matter of some specific substance — but it is the conceptual ground underlying all material change. Medieval Aristotelian natural philosophy transmitted this concept to Latin Europe, and alchemists integrated it into their theoretical frameworks. If a metal like lead consists of prima materia informed by the specific form of lead, then alchemical treatment could in principle strip away the form of lead, returning the material to a state more closely approaching undifferentiated matter, which could then receive the form of gold through the action of the [LINK:philosophers-stone].</p>

<p>The practical identification of prima materia was one of the persistent theoretical problems in alchemical literature. Different traditions proposed different candidates: some identified prima materia with common mercury (quicksilver), arguing that its liquid, metallic character and ability to amalgamate with other metals made it the closest physical approach to undifferentiated metallic matter; others proposed that it was sulphur, chaos, or a specific material preparation (sophic mercury, philosophical salt) accessible only to the initiated practitioner. [LINK:jabir-ibn-hayyan]'s corpus engaged extensively with the problem of identifying and purifying the prima materia of metals as a preliminary to their transformation. [LINK:george-starkey]'s laboratory work, analyzed by William Newman, centered on preparing a "sophick mercury" that he understood as a prepared form of mercury approximating the prima materia of metals.</p>

<h2>Scholarly Significance</h2>
<p>William Newman has shown that the concept of prima materia was operationally generative for alchemical practitioners: it provided theoretical justification for specific laboratory procedures aimed at "reducing" metals to their prima materia as a preparatory stage for transmutation. The theoretical coherence of the concept within Aristotelian natural philosophy gave it legitimacy within university natural philosophy, and defended alchemical transmutation claims against the objection that metals had fixed, unchangeable natures. Lawrence Principe has noted that the practical identification of prima materia — which material in the laboratory corresponded to this theoretical concept — drove substantial experimental investigation, as practitioners attempted to identify through experiment which materials and procedures could reduce metals to a sufficiently undifferentiated state.</p>

<h2>Related Concepts</h2>
<p>Prima materia is the theoretical complement of [LINK:transmutation]: if transmutation is possible, it requires that the matter of a base metal can be returned to or approximated to prima materia and then informed with the form of gold. It connects to [LINK:putrefaction] and [LINK:calcination] as the operations through which existing metallic form is dissolved or destroyed. The [LINK:sulfur-mercury-theory] provided a more specific account of metallic composition that refined the general prima materia concept.</p>

<h2>Literature</h2>
<p>Holmyard, E.J. <i>Alchemy</i>. Penguin Books, 1957.<br>
Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber</i>. Brill, 1991.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>"""
},

{
'slug': 'chrysopoeia',
'label': 'Chrysopoeia (Gold-Making)',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "Chrysopoeia (Greek: gold-making; also argyropoeia, silver-making) was the practical goal of producing gold or silver from base metals through alchemical operations. This is an ACTOR_TERM used in Greek alchemical literature to designate the art of metallic transformation, distinct from the spiritual or philosophical dimensions that later accretions added.",
'definition_long': """<p>Chrysopoeia (Greek: χρυσοποιία, "gold-making"; also <i>argyropoeia</i>, "silver-making") was the practical goal of producing gold or silver from base metals through alchemical operations, and the term used in the earliest Greek alchemical literature to designate the art of metallic transformation. This is an ACTOR_TERM — the word was used by Greek-language practitioners in the early centuries of the common era to describe what they understood themselves to be doing: making gold-like or silver-like materials through laboratory procedures. Lawrence Principe has argued that chrysopoeia, in the earliest Greek texts, referred to genuinely practical goals achievable through the chemical manipulation of metallic alloys, surface treatments, and colorings — producing materials that looked like gold and might pass superficial tests — before the concept acquired the more ambitious sense of actual elemental transmutation that it would carry in the later Arabic and Latin traditions.</p>

<h2>Historical Usage</h2>
<p>The earliest surviving Greek alchemical texts — attributed to figures like pseudo-Democritus ([LINK:democritus]) and compiled in the collection of [LINK:zosimos-of-panopolis] — describe chrysopoeia in terms of practical recipes for producing gold-colored materials: alloys of gold with copper or zinc, surface gilding through mercury amalgamation, and colorings of silver and other metals using plant and mineral dyes. The Leiden and Stockholm papyri (both dating from the third or fourth century CE) contain collections of recipes for dyeing textiles, tinting metals, and producing imitation gems that represent the practical tradition from which alchemical chrysopoeia emerged. Whether these recipes were intended as fraudulent counterfeiting of the precious metals or as genuinely believed transformations is debated; Principe argues that the distinction was not always sharp in the minds of practitioners.</p>

<p>As the Greek alchemical tradition developed through [LINK:zosimos-of-panopolis] and subsequent writers, chrysopoeia acquired a more theoretical character: it was not merely practical gold-making but the production of true gold through the application of a universal transformative agent (the divine water, the sulphurous spirit) to base metallic substrates. This escalation of claims — from gold-colored materials to true gold — was accompanied by increasing theoretical elaboration about the nature of metallic forms and the possibility of formal change. The transmission of Greek chrysopoeia into Arabic alchemy, where it was integrated with the sulphur-mercury theory and the concept of the elixir, transformed it further: Arabic alchemy aimed not at gold-colored imitations but at gold indistinguishable from the natural product by any test.</p>

<h2>Scholarly Significance</h2>
<p>Principe's laboratory-historical analysis of the Leiden and Stockholm papyri has shown that many of the earliest chrysopoeia recipes describe genuine chemical procedures with reproducible results: they produce materials that have the color and some of the surface properties of gold or silver, through processes that modern chemistry recognizes as alloy formation, cementation, and surface plating. This does not mean the practitioners achieved genuine elemental transmutation, but it means they were engaged with real chemical phenomena — not pure fantasy — and that their practices reflected genuine experimental knowledge of the behavior of metals and their compounds.</p>

<h2>Related Concepts</h2>
<p>Chrysopoeia is the earliest practical form of the goal that was later systematized as [LINK:transmutation] and conceptualized through the [LINK:philosophers-stone]. It connects to [LINK:operational-chemistry] as the practical laboratory tradition from which alchemical theory developed. The [LINK:sulfur-mercury-theory] provided the theoretical framework within which later forms of chrysopoeia were understood.</p>

<h2>Literature</h2>
<p>Caley, Earle R. "The Leyden Papyrus X." <i>Journal of Chemical Education</i> 3 (1926): 1149–1166.<br>
Halleux, Robert. <i>Les textes alchimiques</i>. Brepols, 1979.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Viano, Cristina, editor. <i>L'alchimie et ses racines philosophiques</i>. Vrin, 2005.</p>"""
},

{
'slug': 'iatrochemistry',
'label': 'Iatrochemistry',
'category_type': 'ANALYST_TERM',
'operation_type': None,
'definition_short': "Iatrochemistry (from Greek <i>iatros</i>, physician) is a modern scholarly term for the integration of chemical-alchemical practice with medicine, especially in the Paracelsian tradition of the sixteenth and seventeenth centuries, in which chemical preparations of minerals and metals were advocated as remedies for disease. This is an ANALYST_TERM; practitioners themselves spoke of 'chemical medicine' or 'spagyric art.'",
'definition_long': """<p>Iatrochemistry (from Greek <i>iatros</i>, physician, + <i>chemia</i>, chemistry/alchemy) is a modern scholarly term designating the integration of chemical-alchemical practice with medicine, particularly the tradition associated with [LINK:paracelsian-alchemy] that advocated the preparation and use of mineral and metallic substances — preparations of antimony, mercury, arsenic, sulfur, and vitriol — as pharmaceutical remedies superior to the plant-based remedies of Galenic medicine. This is an ANALYST_TERM: historical practitioners did not typically call themselves "iatrochemists" but spoke of chemical medicine (<i>medicina chymica</i>), the spagyric art (<i>ars spagyrica</i>, from Paracelsus's coinage), or the Paracelsian philosophy. The term "iatrochemistry" is a retrospective scholarly category for identifying a coherent tradition of medically oriented alchemy in the sixteenth and seventeenth centuries.</p>

<h2>Historical Usage</h2>
<p>The integration of alchemical-chemical practice with medicine predates Paracelsus: [LINK:john-of-rupescissa]'s fourteenth-century quintessence theory was explicitly medical, and Arabic alchemists including [LINK:al-razi] described elaborate mineral pharmaceutical preparations. What Paracelsus contributed was a radical theoretical reorientation: rather than treating Galenic medicine (with its plant remedies and humoral theory) as the baseline and chemical preparations as additions, he proposed replacing the entire Galenic system with a chemical medicine grounded in the <i>tria prima</i> (sulfur, mercury, salt) as the three principles of all bodies, and in the idea that diseases had specific chemical causes requiring specific chemical remedies. This theoretical aggression provoked intense controversy and positioned iatrochemistry as a competing medical system rather than a supplement.</p>

<p>The major figures of iatrochemistry included [LINK:jan-van-helmont], who accepted Paracelsian rejection of Galenic medicine while developing his own gas-based chemistry; [LINK:george-starkey], whose iatrochemical remedies were a source of income alongside his transmutational laboratory work; and figures like Jan Baptist van Helmont's son Francis Mercury van Helmont. The debate between Galenic and Paracelsian medicine was one of the most significant intellectual controversies of the sixteenth and seventeenth centuries, involving university faculties (particularly the Paris medical faculty), courts, and professional medical organizations across Europe.</p>

<h2>Scholarly Significance</h2>
<p>Allen G. Debus's work on the "chemical philosophy" — particularly <i>The Chemical Philosophy: Paracelsian Science and Medicine in the Sixteenth and Seventeenth Centuries</i> (1977) — established the intellectual context of iatrochemistry and its relationship to natural philosophy more broadly. William Newman and Lawrence Principe's work has integrated iatrochemistry into the broader "chymistry" framework, treating pharmaceutical and transmutational goals as aspects of the same unified laboratory practice rather than separate endeavors. Pamela Smith's work on artisanal and court patronage of chemical medicine has illuminated the social and economic contexts of iatrochemical practice.</p>

<h2>Related Concepts</h2>
<p>Iatrochemistry is directly continuous with [LINK:paracelsian-alchemy] as its major institutional expression. It connects to [LINK:distillation] and [LINK:calcination] as the central operations of pharmaceutical preparation. The [LINK:medicamenta-tria] (three medicines: sulfur, mercury, salt) is the Paracelsian framework within which iatrochemical remedies were theorized. The broader category of [LINK:operational-chemistry] encompasses iatrochemistry as one of its major strands.</p>

<h2>Literature</h2>
<p>Debus, Allen G. <i>The Chemical Philosophy: Paracelsian Science and Medicine in the Sixteenth and Seventeenth Centuries</i>. 2 vols. Science History Publications, 1977.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire</i>. University of Chicago Press, 2002.<br>
Pagel, Walter. <i>Paracelsus: An Introduction to Philosophical Medicine in the Era of the Renaissance</i>. Karger, 1958.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>"""
},

{
'slug': 'conjunction',
'label': 'Conjunction',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "Conjunction (<i>coniunctio</i>) was an alchemical operation in which two purified substances — typically philosophical sulfur and philosophical mercury, or the 'red king' and 'white queen' in allegorical terms — were combined to produce the unified matter from which the Philosopher's Stone would be elaborated. This is an ACTOR_TERM: historical practitioners named and performed this operation explicitly.",
'definition_long': """<p>Conjunction (<i>coniunctio</i>; also called "marriage" or "coitus" in the symbolic vocabulary of alchemical allegory) was an alchemical operation in which two previously separated, purified substances were combined to produce the unified material from which the Philosopher's Stone would be elaborated through subsequent operations. In the sulphur-mercury theory of metallic composition, conjunction brought together the purified philosophical sulphur (associated with the masculine, solar, red principle) and the purified philosophical mercury (associated with the feminine, lunar, white principle) in the correct proportions and form. This is an ACTOR_TERM — the operation was explicitly named and performed in laboratory practice, and the allegorical vocabulary of the "royal wedding" of king and queen was understood as symbolic encoding of this laboratory procedure. Lawrence Principe's laboratory replication work has helped clarify which specific chemical operations correspond to the "conjunction" described in various texts.</p>

<h2>Historical Usage</h2>
<p>Conjunction appears in the alchemical literature from the Arabic tradition through medieval Latin and early modern practice. [LINK:jabir-ibn-hayyan]'s corpus described the combination of purified sulphur and mercury as the central procedure of the Great Work. In [LINK:george-ripley]'s twelve-gate poem, Conjunction appears as the fourth gate, following Calcination, Dissolution, and Separation, and preceding Putrefaction — placing it as the first synthetic operation after the analytical dissolution stages. The [LINK:rosarium-philosophorum] (<i>Rosarium Philosophorum</i>), a major illustrated alchemical text of the fifteenth century, depicted conjunction through the image of a king and queen bathing together, then embracing and merging — images that Carl Jung later interpreted psychologically but which Principe and Newman treat as encoded representations of laboratory procedures for combining specific preparations of sulfur-mercury materials.</p>

<h2>Scholarly Significance</h2>
<p>The scholarly debate over conjunction centers on the relationship between the allegorical representation and the laboratory practice. Jungian interpreters treated the king-queen conjunction image as a projection of psychological archetypes (the union of animus and anima) and the entire alchemical symbolism as unconscious psychological symbolism. Newman and Principe's laboratory-historical approach treats the allegorical language as a deliberate encoding of laboratory procedures for a specifically initiated audience, arguing that practitioners were using allegory as a form of technical language rather than as unconscious psychological expression. This interpretive disagreement is fundamental to understanding how alchemical texts should be read.</p>

<h2>Related Concepts</h2>
<p>Conjunction is one stage within the full sequence of alchemical operations leading to the [LINK:philosophers-stone]. It follows the analytical operations of [LINK:calcination], [LINK:sublimation], and dissolution, and is followed by [LINK:putrefaction] and the later synthetic stages. The [LINK:sulfur-mercury-theory] provides the theoretical framework within which conjunction is understood as combining the two principles of metallic composition.</p>

<h2>Literature</h2>
<p>Abraham, Lyndy. <i>A Dictionary of Alchemical Imagery</i>. Cambridge University Press, 1998.<br>
Newman, William R. <i>The Summa Perfectionis of Pseudo-Geber</i>. Brill, 1991.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>"""
},

{
'slug': 'tria-prima',
'label': 'Tria Prima (Three Principles)',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "Tria prima (Latin: three first things) was Paracelsus's revision of elemental theory: all material substances consist of three principles — sulfur (combustibility and soul), mercury (volatility and spirit), and salt (solidity and body). This is an ACTOR_TERM; Paracelsus and his followers explicitly used this framework to explain health, disease, and material transformation.",
'definition_long': """<p>Tria prima (Latin: "three first things" or "three principles") was the theoretical innovation introduced by [LINK:paracelsian-alchemy]'s founder Paracelsus (Theophrastus Bombastus von Hohenheim, 1493–1541) as a replacement for both the Aristotelian four elements (earth, water, air, fire) and the Arabic alchemical [LINK:sulfur-mercury-theory]. Paracelsus proposed that all material substances — metals, plants, human bodies, minerals — consist of three philosophical principles: sulphur (responsible for combustibility, color, and soul), mercury (responsible for volatility, fluidity, and spirit), and salt (responsible for solidity, fixity, and body). This is an ACTOR_TERM — Paracelsus and his followers explicitly used this framework and would recognize the concept under this name. The tria prima provided a chemical-medical theory of disease (as an imbalance of the three principles in specific organs) and of remedy (as the use of chemically prepared substances to restore balance).</p>

<h2>Historical Usage</h2>
<p>Paracelsus developed the tria prima across his extensive body of writings, including the <i>Opus Paramirum</i>, the <i>Paragranum</i>, and his medical-philosophical treatises. He presented the three principles as observable through fire analysis: when any substance is burned, the volatile component (mercury) escapes as smoke or vapor, the combustible component (sulfur) burns, and the incombustible solid residue (salt) remains. This simple analytical observation grounded the tria prima in actual laboratory experience, giving it a practical authority that the Aristotelian four elements, which were not directly observable as discrete components of combustion, lacked. Paracelsus applied the framework medically: each organ of the body has its specific form of the three principles, and disease occurs when the sulphur, mercury, or salt of a specific organ is corrupted or imbalanced; the remedy must address this specific chemical imbalance using chemically prepared medicines.</p>

<p>The tria prima framework was widely adopted by Paracelsian followers in the later sixteenth century, including [LINK:jan-van-helmont] (who critiqued it while inheriting its medical-chemical orientation), figures of the English Paracelsian movement like Robert Bostocke, and the broader tradition of chemical medicine that opposed Galenism. [LINK:robert-boyle]'s <i>Sceptical Chymist</i> directly engaged with and criticized the tria prima as an inadequate account of elemental composition, arguing from chemical experiments that the three supposed principles could not be consistently separated from all substances.</p>

<h2>Scholarly Significance</h2>
<p>Walter Pagel's scholarship on Paracelsus provided the foundational scholarly account of the tria prima within Paracelsian natural philosophy, situating it within the context of Renaissance Neoplatonism and Hermetic thought as well as practical medicine. Allen G. Debus examined the reception and controversy of the tria prima within the broader "Chemical Philosophy" movement of the sixteenth and seventeenth centuries. Lawrence Principe has situated the tria prima within the laboratory practice of early modern chymistry, noting that despite its theoretical inadequacy by later chemical standards, it was operationally useful as an organizing framework for pharmaceutical chemistry.</p>

<h2>Related Concepts</h2>
<p>The tria prima is the distinctive theoretical contribution of [LINK:paracelsian-alchemy] to alchemical theory, replacing the [LINK:sulfur-mercury-theory] with a triadic framework. It directly informs [LINK:iatrochemistry] as the theoretical basis for chemical medicine. The concept of [LINK:distillation] was central to identifying the three principles through fire analysis. The broader [LINK:medicamenta-tria] concept in which three chemical medicines correspond to the three principles extends the framework into pharmaceutical practice.</p>

<h2>Literature</h2>
<p>Debus, Allen G. <i>The Chemical Philosophy: Paracelsian Science and Medicine in the Sixteenth and Seventeenth Centuries</i>. Science History Publications, 1977.<br>
Pagel, Walter. <i>Paracelsus: An Introduction to Philosophical Medicine in the Era of the Renaissance</i>. Karger, 1958.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Webster, Charles. <i>Paracelsus: Medicine, Magic and Mission at the End of Time</i>. Yale University Press, 2008.</p>"""
},

{
'slug': 'emblematic-alchemy',
'label': 'Emblematic Alchemy',
'category_type': 'ANALYST_TERM',
'operation_type': None,
'definition_short': "Emblematic alchemy is a modern scholarly term for the tradition of alchemical emblem books and illustrated texts — including the Rosarium Philosophorum, Splendor Solis, and Atalanta Fugiens — that communicated alchemical knowledge through sequences of visual images accompanied by explanatory text. This is an ANALYST_TERM for a category of alchemical literature defined by its use of emblematic form.",
'definition_long': """<p>Emblematic alchemy is a modern scholarly term for the tradition of alchemical emblem books and illustrated manuscripts or printed texts — including the [LINK:rosarium-philosophorum], the [LINK:splendor-solis], and [LINK:atalanta-fugiens] — that communicated alchemical knowledge through sequences of visual images (woodcuts, copperplates, miniatures) accompanied by explanatory prose or verse. This is an ANALYST_TERM: historical practitioners did not call their work "emblematic alchemy" but produced emblem books, illustrated treatises, and pictorial sequences as recognized genres of learned communication; the scholarly category "emblematic alchemy" groups these productions as a coherent tradition. Emblematic alchemy sits at the intersection of the emblem book tradition (derived from Andrea Alciato's <i>Emblemata</i>, 1531, and its successors), learned humanist visual culture, and the specifically alchemical need to communicate encoded knowledge through symbolic imagery.</p>

<h2>Historical Usage</h2>
<p>Illustrated alchemical manuscripts predate the printed emblem tradition: the Greek alchemical manuscripts compiled in Byzantine collections contain sequences of images — the Ouroboros serpent, the dragon devouring its tail, the king in the bath — that functioned as allegorical representations of alchemical processes. The [LINK:book-of-pictures] (<i>Mushaf al-Suwar</i>) of Muhammad ibn Umail is an Arabic illustrated alchemical text. The Rosarium Philosophorum (first printed 1550) is perhaps the most influential medieval illustrated alchemical text, presenting a twenty-image sequence depicting the "royal wedding" of king and queen through bathing, death, and resurrection as allegory for the alchemical conjunction and subsequent operations.</p>

<p>The high Renaissance and early modern period saw the florescence of emblematic alchemy as a printed genre. The <i>Splendor Solis</i> (c. 1532–1535), attributed to Salomon Trismosin and surviving in several sumptuous illustrated manuscript copies, presents a twenty-two panel sequence of extraordinary visual richness, combining solar and cosmic imagery with alchemical allegory in a format that blended artistic ambition with alchemical content. Michael Maier's <i>Atalanta Fugiens</i> (1617) is the most technically elaborate emblematic alchemical work: fifty emblems each accompanied by an epigram, a prose "discourse," and a musical canon, integrating music, poetry, visual art, and alchemical allegory in an unprecedented multimedia synthesis.</p>

<h2>Scholarly Significance</h2>
<p>The scholarly analysis of emblematic alchemy has been pursued from several directions. Art historians have examined the visual programs of emblematic texts within the context of Renaissance and Baroque visual culture; Barbara Obrist's work on medieval alchemical images and the scholarship of Lyndy Abraham have been important. Historians of alchemy like Lawrence Principe have approached emblematic texts primarily as encrypted technical communications, arguing that the visual imagery encodes specific laboratory procedures rather than psychological archetypes (against the Jungian reading). Hereward Tilton's study of Michael Maier has combined musical analysis with alchemical history. The question of the audience for emblematic alchemical texts — whether they were primarily designed for initiated practitioners who could "decode" the imagery, for aristocratic patrons who appreciated their visual-symbolic richness, or for a broader literate public — remains debated.</p>

<h2>Related Concepts</h2>
<p>Emblematic alchemy is closely related to [LINK:hermeticism] as the broader intellectual tradition within which it operated. The concept of [LINK:prisca-theologia] — ancient wisdom encoded and transmitted through symbolic forms — provided the ideological framework for emblematic communication. [LINK:conjunction] and [LINK:putrefaction] are among the alchemical operations most frequently represented in emblematic sequences.</p>

<h2>Literature</h2>
<p>Abraham, Lyndy. <i>A Dictionary of Alchemical Imagery</i>. Cambridge University Press, 1998.<br>
Obrist, Barbara. <i>Les débuts de l'imagerie alchimique (XIVe–XVe siècles)</i>. Le Sycomore, 1982.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Tilton, Hereward. <i>The Quest for the Phoenix: Spiritual Alchemy and Rosicrucianism in the Work of Count Michael Maier</i>. de Gruyter, 2003.</p>"""
},

{
'slug': 'spagyrics',
'label': 'Spagyrics',
'category_type': 'ACTOR_TERM',
'operation_type': None,
'definition_short': "Spagyrics (from Greek <i>spao</i>, to separate, and <i>ageiro</i>, to gather) was Paracelsus's term for his reformed chemical medicine: the art of separating the three principles (sulfur, mercury, salt) of a substance, purifying each, and recombining them in improved form to produce a superior medicine. This is an ACTOR_TERM coined by Paracelsus.",
'definition_long': """<p>Spagyrics (from Greek <i>spao</i>, to separate, and <i>ageiro</i>, to gather; also <i>spagyricus</i> in Latin) was the term coined by [LINK:paracelsian-alchemy]'s founder Paracelsus to designate his reformed chemical medicine: the art of separating the three principles ([LINK:tria-prima]: sulfur, mercury, and salt) of a plant, mineral, or metallic substance, purifying each principle individually, and then recombining them in a more perfect form to produce a potent medicine. This is an ACTOR_TERM — Paracelsus himself coined and used this word, and his followers adopted it as the technical designation for chemical pharmaceutical preparation within the Paracelsian system. The concept distinguished Paracelsian chemical medicine from both Galenic plant medicine (which used simple extracts without theoretical analysis into principles) and from transmutational alchemy (which aimed at metallic transmutation rather than therapeutic application).</p>

<h2>Historical Usage</h2>
<p>The spagyric process followed the logic of the tria prima: to prepare a medicine from a plant, for example, one would first extract the sulphur component (through distillation of the volatile oils), then separate the mercury component (the aqueous essence), then calcine the residue to obtain the salt (mineral salts from the ash). Each component was purified and then recombined in the correct proportions. The resulting medicine was understood as a purified, concentrated form of the original substance's healing virtues — more potent than the crude plant material because the three principles had been individually purified before recombination. This process of separation, purification, and recombination gave practical content to the spagyric concept and connected it to actual laboratory operations.</p>

<p>Spagyric preparations of minerals and metals — particularly antimony, mercury, vitriol, and sulfur — were the most controversial aspect of Paracelsian medicine, as these substances were known to be toxic in large doses and their therapeutic use required careful preparation. [LINK:george-starkey]'s career was partly devoted to the preparation and sale of spagyric mineral remedies, including preparations of antimony, and he understood his laboratory work as continuous between the pharmaceutical and the transmutational goals. The antimony controversy in seventeenth-century France — centering on whether antimony preparations were safe and effective medicines — was partly a debate about the validity of the spagyric framework.</p>

<h2>Scholarly Significance</h2>
<p>Allen G. Debus examined spagyrics as part of the broader "chemical philosophy" and its opposition to Galenic medicine. Lawrence Principe and William Newman have situated spagyrics within the unified "chymistry" tradition, noting that the same practitioners pursued spagyric pharmaceutical preparations and transmutational alchemy as aspects of the same laboratory culture. The practical continuity between spagyrics and subsequent pharmaceutical chemistry — many spagyric preparations of plant and mineral substances correspond to genuine chemical extractions with real physiological effects — has been noted by historians of pharmacy as well as historians of alchemy.</p>

<h2>Related Concepts</h2>
<p>Spagyrics is the pharmaceutical application of [LINK:paracelsian-alchemy] and of the [LINK:tria-prima] framework. It connects to [LINK:distillation] and [LINK:calcination] as its primary operations. The broader tradition of [LINK:iatrochemistry] encompasses spagyrics as one of its central practical expressions. The concept of [LINK:operational-chemistry] situates spagyrics within the practical laboratory tradition.</p>

<h2>Literature</h2>
<p>Debus, Allen G. <i>The Chemical Philosophy: Paracelsian Science and Medicine in the Sixteenth and Seventeenth Centuries</i>. Science History Publications, 1977.<br>
Newman, William R., and Lawrence M. Principe. <i>Alchemy Tried in the Fire</i>. University of Chicago Press, 2002.<br>
Pagel, Walter. <i>Paracelsus: An Introduction to Philosophical Medicine in the Era of the Renaissance</i>. Karger, 1958.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>"""
},
]


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    added = 0
    updated = 0
    for concept in NEW_CONCEPTS:
        c.execute('SELECT id FROM concepts WHERE slug=?', (concept['slug'],))
        row = c.fetchone()
        if row:
            c.execute('''UPDATE concepts SET label=?, category_type=?, definition_short=?,
                         definition_long=?, operation_type=?, review_status=?, confidence=?
                         WHERE slug=?''',
                      (concept['label'], concept['category_type'], concept['definition_short'],
                       concept['definition_long'], concept.get('operation_type'),
                       'DRAFT', 'MEDIUM', concept['slug']))
            print(f'  Updated concept: {concept["slug"]}')
            updated += 1
        else:
            c.execute('''INSERT INTO concepts
                         (slug, label, category_type, definition_short, definition_long,
                          operation_type, source_method, review_status, confidence)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (concept['slug'], concept['label'], concept['category_type'],
                       concept['definition_short'], concept['definition_long'],
                       concept.get('operation_type'), 'AI_ASSISTED', 'DRAFT', 'MEDIUM'))
            print(f'  Added concept: {concept["slug"]}')
            added += 1
    conn.commit()
    conn.close()
    print(f'\nDone: {added} added, {updated} updated.')


if __name__ == '__main__':
    main()
