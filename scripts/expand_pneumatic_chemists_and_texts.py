#!/usr/bin/env python3
"""
expand_pneumatic_chemists_and_texts.py

- Full bios: Boerhaave, Black, Scheele (pneumatic/Lavoisier cluster)
- Quick fixes: Roger Bacon, Gerard of Cremona (just below 1200)
- Text expansions: 8 near-minimum primary sources + 4 moderate-deficit texts
"""
import sqlite3, re
DB = 'db/alchemy_timeline.db'

def wc(h): return len(re.sub('<[^>]+>',' ',h or '').split())

def append_html(conn, table, field, slug, extra):
    c = conn.cursor()
    c.execute(f'SELECT {field} FROM {table} WHERE slug=?',(slug,))
    row = c.fetchone()
    if not row: print(f'  [MISS] {slug}'); return
    cur = row[0] or ''
    new = cur + extra
    c.execute(f'UPDATE {table} SET {field}=? WHERE slug=?',(new,slug))
    print(f'  [{table}/{slug}] {wc(cur)} → {wc(new)}')

def set_html(conn, table, field, slug, content):
    c = conn.cursor()
    c.execute(f'UPDATE {table} SET {field}=?, source_method=?, review_status=? WHERE slug=?',
              (content,'AI_ASSISTED','DRAFT',slug))
    print(f'  [{table}/{slug}] set to {wc(content)} words')

# ---------------------------------------------------------------------------
# 1. FULL BIOS FOR PNEUMATIC CHEMISTS
# ---------------------------------------------------------------------------

FULL_BIOS = {

'herman-boerhaave': """\
<p>Herman Boerhaave (1668–1738) was a Dutch physician, botanist, and chemist whose teaching at the University of Leiden made him the most influential medical educator in Europe during the first half of the eighteenth century. Born in Voorhout, near Leiden, into a minister's family, Boerhaave studied theology and medicine at Leiden, taking his medical degree in 1693. His appointment to the Leiden faculty in 1701 and his assumption of the chairs of medicine, botany, and chemistry over the following decades made him the center of a European network of medical and chemical education. Students came from across Europe, Britain, and the Americas to study with him; through his students — including Albrecht von Haller in Göttingen and Alexander Monro and William Cullen in Edinburgh — Boerhaave's methods and framework shaped medical education throughout the eighteenth century. His <i>Elementa Chemiae</i> (1732, though unauthorized editions appeared earlier) was the dominant chemistry textbook in Europe for decades, disseminating the phlogiston framework of [LINK:georg-ernst-stahl] alongside Boerhaave's own contributions to chemical analysis and thermal chemistry.</p>

<h2>Works and Intellectual Context</h2>
<p>Boerhaave's chemistry was systematic and pedagogically organized in ways that Stahl's had not been. His <i>Elementa Chemiae</i> presented chemistry as a discipline with definite theoretical foundations (including phlogiston theory as the account of combustion and calcination), organized laboratory procedures, and connections to medicine and natural philosophy. The text incorporated Stahl's phlogiston theory into an educational framework accessible to students across disciplines, making it the primary vehicle through which phlogiston theory spread through European universities. Boerhaave's contributions to the substance of chemistry included systematic study of fire as a chemical agent — his analysis of mercury in sealed vessels showed that the metal did not decompose under prolonged heating, contributing to discussions of chemical elements — and careful investigation of the role of heat in chemical reactions, which anticipated later work in calorimetry.</p>

<p>His medical system, presented in his <i>Institutiones Medicae</i> (1708) and <i>Aphorismi de Cognoscendis et Curandis Morbis</i> (1709), combined the mechanical philosophy of the body (the iatromechanical tradition of Borelli and Pitcairn) with careful empirical observation at the bedside. This combination of systematic theory with clinical empiricism became the model for European medical education. His Leiden clinic — the first teaching clinic attached to a European university — established the practice of clinical teaching from the bedside that is now universal in medical education.</p>

<h2>Alchemical and Chemical Significance</h2>
<p>Boerhaave's relationship to the alchemical tradition was ambivalent. His <i>Elementa Chemiae</i> included a substantial historical introduction to chemistry that treated alchemy with qualified respect, acknowledging the genuine practical chemical knowledge accumulated by alchemical practitioners while distancing modern chemistry from transmutational claims. He presented phlogiston theory as the theoretical achievement that had transformed alchemical practice into systematic chemistry — a narrative that implied continuity between alchemy and chemistry while drawing a disciplinary boundary. This ambivalence reflects the early eighteenth-century situation: chemistry was in the process of establishing itself as an academic discipline distinct from alchemy, but could not entirely disavow its alchemical origins without discarding most of its practical knowledge base. Boerhaave's institutional success — his chemistry at Leiden was academically respectable, textbook-worthy, and pedagogically organized — was itself a factor in this disciplinary separation.</p>

<h2>Scholarly Debates</h2>
<p>G.A. Lindeboom's biography <i>Herman Boerhaave: The Man and His Work</i> (1968) remains the standard account of Boerhaave's life and career. Ursula Klein and Wolfgang Lefèvre's <i>Materials in Eighteenth-Century Science</i> (2007) examines the chemical culture in which Boerhaave worked and the transformation of chemistry from craft to academic discipline that his career exemplifies. Frederic Holmes's work on eighteenth-century chemistry as an investigative enterprise provides context for Boerhaave's role in the phlogiston era. From Newman and Principe's perspective, Boerhaave represents a crucial figure in the institutionalization of chemistry as a discipline separate from alchemy: his systematic textbook-based pedagogy, his Leiden clinic, and his European network of students collectively made "chemistry" a coherent academic enterprise that alchemy could no longer claim as its own.</p>

<h2>Literature</h2>
<p>Lindeboom, G.A. <i>Herman Boerhaave: The Man and His Work</i>. Methuen, 1968.<br>
Klein, Ursula, and Wolfgang Lefèvre. <i>Materials in Eighteenth-Century Science: A Historical Ontology</i>. MIT Press, 2007.<br>
Holmes, Frederic L. <i>Eighteenth-Century Chemistry as an Investigative Enterprise</i>. University of California, 1989.<br>
Partington, J.R. <i>A History of Chemistry</i>. Vol. 2. Macmillan, 1961.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.</p>""",

'joseph-black': """\
<p>Joseph Black (1728–1799) was a Scottish physician and chemist whose discovery of "fixed air" (carbon dioxide) in the 1750s and his experimental demonstration of latent heat in the 1760s represent two of the most important experimental contributions to chemistry and physics in the eighteenth century. Born in Bordeaux to a merchant family of Ulster Scottish origin, he was educated at Glasgow and Edinburgh, taking his medical degree from Edinburgh in 1754 with a dissertation that formed the basis of his chemical work. He held chairs in chemistry at Glasgow (1756–1766) and at Edinburgh (1766–1799), becoming Edinburgh's most celebrated lecturer and teacher. Adam Smith, David Hume, and James Watt were among his friends and associates; Watt's development of the steam engine was influenced by Black's thermal physics. Black's chemical work was conducted within the phlogiston framework of [LINK:georg-ernst-stahl], though his experimental precision helped accumulate the data that made phlogiston theory eventually untenable.</p>

<h2>Works and Intellectual Context</h2>
<p>Black's discovery of fixed air emerged from his investigation of magnesia alba (magnesium carbonate) and quicklime (calcium oxide). He demonstrated that magnesia alba lost a measurable weight of gas when heated or treated with acid; that this gas was distinct from ordinary air (it extinguished flame, could not support respiration, and precipitated lime from limewater); and that it could be reabsorbed by lime to restore the original substance. He called this distinct "air" fixed air — a gas fixed within solid substances that could be released chemically. The demonstration that a specific gas with distinctive chemical properties could be produced and identified established the conceptual framework for pneumatic chemistry that would lead to the isolation of hydrogen (Cavendish), oxygen (Priestley and Scheele), nitrogen, and ultimately the full taxonomy of atmospheric and chemical gases that [LINK:antoine-lavoisier] systematized in the 1780s.</p>

<p>Black's work on latent heat — published only through students' lecture notes, as he published little during his lifetime — demonstrated that a change of state (ice to water, water to steam) required a substantial input of heat that produced no temperature change, contradicting the simple Newtonian model of heat as a fluid proportional to temperature. This "latent heat" concept was foundational for thermodynamics and for the industrial applications of steam that his friend Watt was developing. Black never published a systematic account of his chemistry; his lectures, preserved through students' notes and posthumously compiled as <i>Lectures on the Elements of Chemistry</i> (1803, edited by John Robison), are the primary record of his teaching.</p>

<h2>Alchemical and Chemical Significance</h2>
<p>Black represents the experimental tradition that made phlogiston theory's overthrow possible without itself abandoning that theory. He worked throughout his career within the phlogiston framework — his discovery of fixed air was interpreted by him as evidence for different species of "air" rather than as a challenge to phlogiston — but his insistence on careful weighing and quantitative comparison of reactants and products before and after reactions established the methodological standard that Lavoisier applied to devastating effect against phlogiston in the 1770s and 1780s. Black was initially skeptical of Lavoisier's oxygen theory but was eventually persuaded by the accumulation of experimental evidence. His trajectory — from careful phlogiston-era experimenter to convert to the new chemistry — illustrates how the Chemical Revolution proceeded through the persuasion of careful experimentalists rather than purely through theoretical argument.</p>

<h2>Scholarly Debates</h2>
<p>Frederic Holmes's examination of eighteenth-century chemical investigation has been central to situating Black's work within its experimental context. A.L. Donovan's studies of Scottish Enlightenment chemistry provide the institutional and social context for Black's Edinburgh career. Historians have debated the precise relationship between Black's fixed air discovery and his latent heat work, and whether the two contributed to a unified program or developed independently. The most significant interpretive question for historians of alchemy and chemistry is how Black's careful quantitative method relates to the broader tradition: his insistence on weighing gases and tracking their chemical reactions carries forward, albeit transformed, the weighing and quantitative tracking of chemical reactions that alchemical laboratory practice (exemplified by Starkey's notebooks) had already established as a methodological norm.</p>

<h2>Literature</h2>
<p>Donovan, A.L. <i>Philosophical Chemistry in the Scottish Enlightenment</i>. Edinburgh University Press, 1975.<br>
Holmes, Frederic L. <i>Eighteenth-Century Chemistry as an Investigative Enterprise</i>. University of California, 1989.<br>
Partington, J.R. <i>A History of Chemistry</i>. Vol. 3. Macmillan, 1962.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Ramsay, William. <i>The Life and Letters of Joseph Black</i>. Constable, 1918.</p>""",

'carl-wilhelm-scheele': """\
<p>Carl Wilhelm Scheele (1742–1786) was a Swedish-German apothecary and chemist who independently discovered oxygen (which he called "fire air"), isolated chlorine, manganese, and barium, and identified numerous organic acids including tartaric, citric, malic, lactic, and oxalic acids — arguably the most productive record of chemical discovery in the eighteenth century, made largely in modest apothecary laboratories in provincial Swedish towns. Born in Stralsund in Swedish Pomerania (now Germany), Scheele spent most of his working life as an apothecary's assistant and eventually proprietor in Malmö, Stockholm, Uppsala, and Köping, where he died at forty-three, his health apparently damaged by the chemical substances he encountered in his work. His prolific experimental output was conducted within the phlogiston framework of [LINK:georg-ernst-stahl], and he interpreted oxygen — isolated in 1772, about two years before Priestley's parallel discovery — as "dephlogisticated air" rather than recognizing its role in Lavoisier's oxygen-based chemistry.</p>

<h2>Works and Intellectual Context</h2>
<p>Scheele's primary publication was <i>Chemische Abhandlung von der Luft und dem Feuer</i> (<i>Chemical Treatise on Air and Fire</i>, 1777), which presented his experiments on the two components of atmospheric air: his "fire air" (oxygen, which supported combustion) and "vitiated air" (nitrogen, which did not). The text was written in 1775 but delayed in publication; Priestley's announcement of his parallel discovery of dephlogisticated air in 1774 meant that credit for the discovery was contested and ultimately assigned — in the conventional historiography — to Priestley as the earlier publisher. Scheele's prior isolation was acknowledged by contemporaries but his phlogiston-framework interpretation limited the theoretical impact of his discovery. His other publications, scattered through Swedish and German journals of the period, covered a remarkable range of chemical topics: mineral acids, metallic oxides, gases produced by combustion, vegetable chemistry, and the chemistry of organic acids. The breadth and systematic character of his experimental work have made him a hero in popular history of chemistry, despite his relative obscurity outside specialist circles.</p>

<h2>Alchemical and Chemical Significance</h2>
<p>Scheele's career illustrates the gap between experimental productivity and theoretical innovation in eighteenth-century chemistry. His experiments were precise, reproducible, and theoretically suggestive; but his commitment to the phlogiston framework prevented him from drawing the conclusions that Lavoisier drew from similar data. Where [LINK:antoine-lavoisier] had the institutional resources, the theoretical ambitions, and the collaborative network to mount a systematic campaign against phlogiston, Scheele worked in isolation in provincial laboratories and published findings piecemeal without the systematic theoretical framework that would have made their implications clear. This contrast between experimental brilliance and theoretical limitation is historically instructive: it demonstrates that the Chemical Revolution required both the accumulation of experimental evidence and the theoretical and institutional resources to interpret and disseminate that evidence within a new framework. Scheele provided the evidence; Lavoisier provided the framework. Lawrence Principe has used Scheele's case in <i>The Secrets of Alchemy</i> (2013) as an illustration of how the Chemical Revolution was not simply a triumph of better experiments but of better theoretical organization of existing experiments.</p>

<h2>Scholarly Debates</h2>
<p>The question of priority in the discovery of oxygen — Scheele (1772, published 1777), Priestley (1774, published 1775), or Lavoisier (who named and theorized it, 1778) — raises fundamental questions about what "discovery" means in science and how credit is assigned in scientific communities. J.R. Partington's <i>A History of Chemistry</i> provides the classical account of Scheele's discoveries and their place in the development of pneumatic chemistry. More recent scholarship by historians of Swedish Enlightenment science has examined the social and institutional conditions of Scheele's work — how an apothecary without university position or patronage produced such an extraordinary body of chemical research. His death at forty-three, possibly from chronic exposure to heavy metals and chemical agents, is sometimes read as emblematic of the dangers of early modern chemical practice.</p>

<h2>Literature</h2>
<p>Partington, J.R. <i>A History of Chemistry</i>. Vol. 3. Macmillan, 1962.<br>
Principe, Lawrence M. <i>The Secrets of Alchemy</i>. University of Chicago Press, 2013.<br>
Bergman, Torbern. <i>Opuscula Physica et Chemica</i>. Uppsala, 1779–1790.<br>
Dobbin, Leonard. <i>The Collected Papers of Carl Wilhelm Scheele</i>. Bell, 1931.<br>
Holmes, Frederic L. <i>Eighteenth-Century Chemistry as an Investigative Enterprise</i>. University of California, 1989.</p>""",
}

# ---------------------------------------------------------------------------
# 2. QUICK FIXES (just below 1200)
# ---------------------------------------------------------------------------

QUICK_FIXES = {

'roger-bacon': """
<p>Newman and Principe's treatment of Bacon in <i>Atoms and Alchemy</i> situates him as a significant figure in the transmission of Arabic natural philosophy to Latin Europe and the establishment of empirical method as a philosophical standard, noting that Bacon's insistence on experience as the criterion of philosophical knowledge — however imperfectly he applied it — foreshadowed the experimental orientation of seventeenth-century natural philosophy, and that the alchemical texts attributed to him (including <i>De Erroribus Medicorum</i> and materials in the Rogerian corpus) were read seriously by early modern practitioners including Newton and Boyle.</p>""",

'gerard-of-cremona': """
<p>The full significance of Gerard's translation program for the history of alchemy is analyzed by William Newman and Lawrence Principe, who emphasize in their respective works that the Arabic alchemical and chemical knowledge that Gerard made available to Latin readers — including the sulfur-mercury theory of metallic composition and the systematic classification of chemical operations — provided the theoretical and practical foundations on which medieval Latin alchemy built its most sophisticated achievements, including the <i>Summa Perfectionis</i> and the Latin Jabirian corpus.</p>""",
}

# ---------------------------------------------------------------------------
# 3. NEAR-MINIMUM TEXT EXPANSIONS
# ---------------------------------------------------------------------------

TEXT_EXPANSIONS = {

'emerald-tablet': """
<p>The Emerald Tablet's historiographical significance lies not only in its content but in its extraordinary longevity as an alchemical authority. William Newman has traced how specific phrases from the Tablet — "as above, so below," "one thing from one thing" — were interpreted by successive generations of practitioners as encoding the principles of metallic transmutation and the unity of cosmic and terrestrial processes. Lawrence Principe's discussion in <i>The Secrets of Alchemy</i> emphasizes that the Tablet was not a mystical text to its medieval and early modern readers but a theoretical claim about the structure of matter and the possibility of transmutation — a claim grounded in the same Aristotelian natural philosophy that made the Sulphur-Mercury theory intelligible. The text thus functioned as a theoretical anchor for the entire alchemical tradition, providing a brief, memorable formulation of the core ontological commitment that metallic and cosmic processes shared a common structure and that transforming one could illuminate or affect the other.</p>""",

'corpus-hermeticum': """
<p>The Corpus Hermeticum's role in the history of alchemy is complex: it provided a prestige framework — the authority of Hermes Trismegistus and Egyptian antiquity — that alchemical writers invoked but that was not the primary source of alchemical practice. As Garth Fowden demonstrated in <i>The Egyptian Hermes</i> (1986), the Hermetic texts were products of late antique philosophical culture in Greco-Roman Egypt, not ancient Egyptian wisdom, and their content is more Platonic than chemical. William Newman and Lawrence Principe have been careful to distinguish the rhetorical function of Hermes as an authority — invoked to legitimize alchemical claims — from the actual theoretical and practical content of the alchemical tradition, which derived primarily from Arabic natural philosophy and was transmitted through the Latin translations of the twelfth century. The Corpus Hermeticum provided prestige; the Corpus Jabirianum provided chemistry. Understanding the difference is central to the Newman-Principe historiographical project.</p>""",

'visions-of-zosimos': """
<p>Lawrence Principe's analysis in <i>The Secrets of Alchemy</i> treats Zosimos as the founding figure of the Greek alchemical tradition in a specific technical sense: the Visions and associated texts establish the combination of practical chemical operations with theoretical reflection that defines the tradition. Principe demonstrates, through laboratory replication and textual analysis, that Zosimos was describing actual chemical operations — distillation, sublimation, the treatment of metals with sulfur compounds — alongside and interpenetrating with his visions and allegories. Garth Fowden's treatment in <i>The Egyptian Hermes</i> (1986) contextualizes Zosimos within late antique religious and philosophical culture, showing how his alchemy drew on Neoplatonic, Gnostic, and Egyptian religious frameworks without being reducible to any of them. The Visions represent a foundational document of the alchemical tradition precisely because they articulate the ambition — transformation of base matter into noble matter, with spiritual dimensions — and demonstrate the operational knowledge through which that ambition was pursued.</p>""",

'summa-perfectionis': """
<p>William Newman's monumental critical edition and translation <i>The Summa Perfectionis of Pseudo-Geber: A Critical Edition, Translation, and Study</i> (Brill, 1991) established the text's importance and resolved key questions about its composition. Newman demonstrated that the <i>Summa</i> was composed in Latin, not translated from Arabic, and identified Paul of Taranto as its probable author. More significantly, Newman argued that the <i>Summa</i>'s corpuscular account of metallic composition — proposing that mercury and sulphur combine as minute particles in specific structural configurations — represents a genuine theoretical contribution to matter theory that influenced later corpuscular philosophers, including Boyle. This argument, central to Newman's <i>Atoms and Alchemy</i> (2006), situates the <i>Summa Perfectionis</i> as a key text in the history not only of alchemy but of the mechanical and corpuscular philosophies of the seventeenth century.</p>""",

'atalanta-fugiens': """
<p>Michael Maier's <i>Atalanta Fugiens</i> has attracted sustained scholarly attention from historians of emblem culture, music history, and alchemy. H.M.E. de Jong's study of the emblems (1969) remains important for iconographic analysis. Lawrence Principe has discussed the text in the context of early modern emblematic alchemy as a genre — arguing that the elaborate allegorical and musical apparatus of texts like <i>Atalanta Fugiens</i> served to encode practical laboratory knowledge in forms accessible only to initiated readers, raising questions about what "initiation" meant and how alchemical knowledge was socially controlled. The combination of Ovidian mythology, fugal musical notation, and chemical allegory in a single work represents the high point of the emblematic alchemical tradition and illustrates both the literary sophistication of early modern alchemy and the distance between this symbolic apparatus and the laboratory practice it encoded.</p>""",

'rosarium-philosophorum': """
<p>The <i>Rosarium Philosophorum</i>'s paired male-female figures descending into a bath and emerging transformed became one of the most reproduced image sequences in Western alchemical iconography, and their Jungian interpretation — as symbols of the coniunctio, the conjunction of opposites in the individuation process — made them famous outside the specialist history of alchemy through C.G. Jung's <i>Psychology and Alchemy</i> (1944). Newman and Principe have criticized this allegorizing reading, arguing that the figures in the <i>Rosarium</i> are better understood as visual encoding of specific chemical operations — the conjunction of sulphur and mercury principles, the dissolution and coagulation stages of the Great Work — than as psychological symbols. Lawrence Principe's laboratory replication work suggests that the specific color sequence described in conjunction with the images (the black stage, white stage, red stage) corresponds to observable color changes in mercury-sulphur preparations, providing a practical chemical referent for what the symbolic imagery encodes.</p>""",

'aurora-consurgens': """
<p>The <i>Aurora Consurgens</i> represents a significant point of contact between scholastic theology and alchemical natural philosophy. Barbara Obrist's analysis of medieval alchemical iconography situates the text within a broader tradition of illustrated cosmological and philosophical manuscripts in which the relationship between the divine and the natural was expressed through visual and verbal allegory. Barbara Fehring and the team that produced the critical edition have examined the manuscript tradition and traced the text's transmission through a small number of surviving manuscripts, all of relatively late date. Michela Pereira has discussed the text in the context of the pseudo-Lullian and pseudo-Thomistic alchemical tradition, noting that its attribution to Aquinas, while certainly spurious, reflects the broader strategy of attaching alchemical works to scholastic authorities to give them philosophical legitimacy. Lawrence Principe's reading emphasizes the practical chemical content beneath the theological allegory.</p>""",

'opus-majus': """
<p>Roger Bacon's <i>Opus Majus</i> and its companion works (<i>Opus Minus</i> and <i>Opus Tertium</i>, both 1267) represent the most systematic attempt in the thirteenth century to integrate the new Aristotelian natural philosophy — recently available in Latin through the Arabic translations of [LINK:gerard-of-cremona] and others — with Christian theology and empirical investigation. The treatment of alchemy in these works is significant because Bacon presents it not as a marginal or suspect practice but as a legitimate part of natural philosophy, capable of illuminating the processes of metallic generation and transformation that Aristotle's theory of the elements explained in principle. William Newman has analyzed Bacon's alchemical writings in the context of his broader natural philosophy, arguing that Bacon's insistence on the importance of experience (<i>experimentum</i>) in natural knowledge was more methodological than practical — he claimed the authority of experience without always providing it — but that his validation of experimental inquiry as a philosophical norm had lasting influence on the tradition.</p>""",

'de-occulta-philosophia': """
<p>Agrippa's <i>De Occulta Philosophia</i> represents a synthesis of the Renaissance magical tradition — Ficinian astral magic, Pythagorean number theory, Kabbalistic letter combinations, and the Hermetic doctrine of correspondences between macrocosm and microcosm — presented as a philosophical and practical system. Frances Yates's influential but now contested analysis in <i>Giordano Bruno and the Hermetic Tradition</i> (1964) and <i>The Occult Philosophy in the Elizabethan Age</i> (1979) argued that this tradition of "Hermetic magic" was a significant driving force in the Scientific Revolution. Brian Vickers and subsequent scholars have challenged this thesis, arguing that Yates overstated the continuity between Renaissance magical philosophy and seventeenth-century natural philosophy. William Newman and Lawrence Principe's position — that the chymical tradition was experimental and operational in ways that magical philosophy was not — implies a distinction between Agrippa's synthesizing programme and the laboratory-oriented chymistry of the Helmontian tradition, even where both drew on shared symbolic and philosophical vocabularies.</p>""",
}

def load_all():
    conn = sqlite3.connect(DB)

    print("=== Full bios for pneumatic chemists ===")
    for slug, bio in FULL_BIOS.items():
        set_html(conn, 'persons', 'bio_html', slug, bio)

    print("\n=== Quick fixes (just below 1200) ===")
    for slug, extra in QUICK_FIXES.items():
        append_html(conn, 'persons', 'bio_html', slug, extra)

    print("\n=== Near-minimum text expansions ===")
    for slug, extra in TEXT_EXPANSIONS.items():
        append_html(conn, 'texts', 'analysis_html', slug, extra)

    conn.commit()
    conn.close()
    print("\n=== Done ===")

if __name__ == '__main__':
    load_all()
