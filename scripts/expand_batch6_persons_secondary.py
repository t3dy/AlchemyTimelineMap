#!/usr/bin/env python3
"""expand_batch6_persons_secondary.py — Expand secondary person bios to 1200-word minimum."""
import sqlite3, re
DB = 'db/alchemy_timeline.db'

def wc(h): return len(re.sub('<[^>]+>', ' ', h or '').split())

def app(conn, slug, extra):
    c = conn.cursor()
    c.execute('SELECT bio_html FROM persons WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row: print(f'  [MISS] {slug}'); return
    cur = row[0] or ''
    new = cur + extra
    c.execute('UPDATE persons SET bio_html=? WHERE slug=?', (new, slug))
    print(f'  {slug}: {wc(cur)} -> {wc(new)}')

def setp(conn, slug, bio):
    c = conn.cursor()
    c.execute('SELECT bio_html FROM persons WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row: print(f'  [MISS] {slug}'); return
    cur = row[0] or ''
    c.execute('UPDATE persons SET bio_html=? WHERE slug=?', (bio, slug))
    print(f'  {slug}: {wc(cur)} -> {wc(bio)}')

# ── Robert Fludd ──────────────────────────────────────────────────────────────

FLUDD_EXTRA = (
    '<h2>Macrocosm, Microcosm, and the Rosicrucian Controversy</h2>'
    '<p>Fludd\'s major work, the <i>Utriusque Cosmi Maioris scilicet et Minoris Metaphysica,'
    ' Physica atque Technica Historia</i> (History of the Two Worlds, the Greater and the'
    ' Lesser, 1617–1621), presents an exhaustive account of macrocosm and microcosm illustrated'
    ' with elaborate engravings. The two worlds are the cosmos and the human being, understood'
    ' as reflections of each other within a Neoplatonic-Hermetic framework. Alchemy appears'
    ' within this framework as the art of purifying and perfecting material substances by'
    ' aligning them with their celestial archetypes — the same logic that governed Fludd\'s'
    ' accounts of music, medicine, memory, and divination. The encyclopedic scope of the work'
    ' and the quality of its illustrations (engraved by Johann Theodor de Bry) made it one'
    ' of the most visually impressive philosophical productions of the early seventeenth century.</p>'
    '<p>Fludd\'s defense of the Rosicrucian manifestos — the <i>Fama Fraternitatis</i> (1614),'
    ' <i>Confessio</i> (1615), and <i>Chymical Wedding of Christian Rosencreutz</i> (1616) —'
    ' in his <i>Apologia Compendiaria</i> (1616) and <i>Tractatus Apologeticus</i> (1617)'
    ' positioned him as the most prominent English intellectual defender of the Rosicrucian'
    ' movement. This defense drew the attention of continental critics, including Johannes'
    ' Kepler and Pierre Gassendi, who attacked Fludd\'s Neoplatonic-Hermetic natural philosophy'
    ' as qualitative, obscurantist, and incompatible with the mathematical natural philosophy'
    ' that Kepler was developing. The exchange between Fludd and Kepler has been analyzed'
    ' by historians including Peter Ammann as one of the defining confrontations between the'
    ' Hermetic-qualitative and the mathematical-quantitative approaches to natural philosophy'
    ' in the early seventeenth century — a confrontation whose outcome helped shape the'
    ' character of the Scientific Revolution.</p>'
    '<p>Fludd was a practicing physician who trained at Oxford and obtained his MD from Christ'
    ' Church in 1605. His medical practice, conducted in London after his return from continental'
    ' travels, employed the Paracelsian chemical medicines alongside Galenic treatments. His'
    ' advocacy for the weapon-salve — a sympathetic cure in which the weapon that caused a wound'
    ' was treated rather than the wound itself — became notorious and drew satire; William Foster\'s'
    ' attack on it and Fludd\'s response were part of the broader controversy about whether'
    ' sympathy and action-at-a-distance had a legitimate place in natural philosophy. This'
    ' controversy directly engaged the same questions about occult qualities and hidden causes'
    ' that [LINK:robert-boyle] and others would address in terms of corpuscular mechanisms'
    ' in the following generation.</p>'
    '<p>Joscelyn Godwin\'s study of Fludd and William Huffman\'s monograph provide the major'
    ' modern scholarly treatments. Frances Yates\'s analysis of Fludd in <i>The Rosicrucian'
    ' Enlightenment</i> (1972) placed him within her broader thesis about Hermeticism and the'
    ' Scientific Revolution. Subsequent scholarship has both built on and modified Yates\'s'
    ' interpretation, noting that Fludd\'s natural philosophy was more explicitly antagonistic'
    ' to the mathematical-mechanical approach than Yates\'s thesis of a unified "Hermetic"'
    ' tradition driving scientific reform suggested. His position within early seventeenth-century'
    ' natural philosophy is best understood as representing a genuine alternative program —'
    ' qualitative, holistic, animated — rather than as a precursor to the scientific approach'
    ' that defeated it.</p>'
)

# ── Theosebeia ────────────────────────────────────────────────────────────────

THEOSEBEIA_EXTRA = (
    '<h2>Zosimos\'s Interlocutor and Early Greek Alchemy</h2>'
    '<p>Theosebeia is attested only in the writings of [LINK:zosimos-of-panopolis], the earliest'
    ' Greek alchemical author whose work survives in recognizable form, writing in Roman Egypt'
    ' around 300 CE. Zosimos addresses her directly in several treatises, apparently responding'
    ' to questions she has raised about alchemical theory and practice. The relationship implied'
    ' by the texts is that of a more experienced practitioner to a serious student, but the'
    ' exact nature of their connection — teacher-student, colleague, patron, relative — cannot'
    ' be determined from the surviving evidence. The name Theosebeia means "reverence for the'
    ' divine" and may be a religious name or pseudonym rather than a birth name; this ambiguity'
    ' is characteristic of the evidence problems that beset all study of ancient alchemical figures.</p>'
    '<p>Her importance for the history of alchemy lies partly in what her presence in the texts'
    ' suggests about the social organization of alchemical practice in late antique Egypt.'
    ' Zosimos writes to her as an intellectual equal capable of engaging with complex theoretical'
    ' discussions about the sulphur-mercury theory of metals, about the relationship between'
    ' alchemical operations and spiritual transformation, and about the interpretation of earlier'
    ' alchemical authorities. This implies that women participated in the practice of Greek'
    ' alchemy at a level of serious intellectual engagement from the earliest period of the'
    ' tradition — a finding consistent with the attribution of other early alchemical texts'
    ' to women practitioners, including the legendary Mary the Jewess (Maria Hebraea), to whom'
    ' the invention of important laboratory apparatus (the bain-marie, the tribikos) was attributed.</p>'
    '<p>The identity of Theosebeia has been discussed by scholars of Gnosticism and late antique'
    ' religion as well as historians of alchemy, since some of Zosimos\'s religious and philosophical'
    ' discussions in the texts addressed to her engage with Gnostic concepts and with the relationship'
    ' between material purification and spiritual ascent. If she was a Gnostic practitioner as'
    ' well as an alchemical one, her figure connects the history of alchemy with the broader'
    ' landscape of late antique religious pluralism in which Gnosticism, Hermeticism, Neoplatonism,'
    ' and proto-orthodox Christianity competed and interpenetrated.</p>'
    '<p>Michela Marzano and Kim Veltman have touched on Theosebeia in studies of gender and'
    ' ancient alchemy. Florian Ebeling\'s work on the secret history of Hermes Trismegistus and'
    ' Matteo Martelli\'s scholarship on early Greek alchemical texts provide the scholarly context'
    ' for situating her within the early Greek alchemical tradition. The inaccessibility of most'
    ' early alchemical texts to non-specialist audiences — the primary collection remains Marcel'
    ' Berthelot\'s nineteenth-century edition, which is in Greek and French — means that'
    ' Theosebeia remains largely unknown outside specialist scholarship, but her presence in the'
    ' earliest sustained alchemical writings in the Western tradition makes her historiographically'
    ' significant as evidence for the social breadth of early alchemical inquiry.</p>'
)

# ── George Agricola ────────────────────────────────────────────────────────────

AGRICOLA_EXTRA = (
    '<h2>De Re Metallica and the Science of Mining</h2>'
    '<p>Agricola\'s <i>De Re Metallica</i> (1556, published posthumously) is the most comprehensive'
    ' technical account of mining, smelting, and metallurgical operations produced in the sixteenth'
    ' century. Illustrated with woodcuts showing mine shafts, ventilation systems, pumping machinery,'
    ' ore-processing equipment, and smelting furnaces, it was a genuinely practical manual for the'
    ' mining industry of central Europe as well as a work of humanist natural philosophy. Its'
    ' combination of classical learning — citations from Pliny, Agricola\'s Latin style and'
    ' humanist credentials — with systematic observation of contemporary industrial practice'
    ' reflects the same synthesis of textual authority and empirical inquiry that characterized'
    ' the best natural philosophy of the period.</p>'
    '<p>Agricola (born Georg Bauer; "Agricola" is a Latinization of "Bauer," meaning farmer)'
    ' spent much of his career in Joachimsthal and Chemnitz, in the Erzgebirge (Ore Mountains)'
    ' of Bohemia and Saxony — a region where the silver mining industry was one of the most'
    ' technologically sophisticated in Europe. His proximity to active mining operations allowed'
    ' him to observe and record practices at first hand rather than relying on transmitted'
    ' classical accounts. The result is a text that is unusually concrete and specific about'
    ' actual operations: the different types of ores, their assay and processing, the equipment'
    ' used for different operations, the problems of water in mine shafts and how they were'
    ' addressed.</p>'
    '<p>The relationship of <i>De Re Metallica</i> to alchemy is one of productive tension.'
    ' Agricola\'s earlier work, <i>Bermannus</i> (1530) and <i>De Natura Fossilium</i> (1546),'
    ' engaged with questions about the generation of metals in the earth using the theoretical'
    ' framework of sulphur-mercury theory — the same framework that structured alchemical matter'
    ' theory. His attitude toward transmutational alchemy was skeptical: in <i>De Re Metallica</i>'
    ' he explicitly distinguishes the practical metallurgy he is describing from the claims of'
    ' alchemists who assert they can make gold, which he doubts. But his theoretical framework'
    ' for understanding how metals form naturally drew on the same Aristotelian-Arabic tradition'
    ' of matter theory that alchemical theory used, and his careful attention to the practical'
    ' chemistry of ore processing contributed to the stock of knowledge about metallic substances'
    ' that both practitioners and theorists would draw on.</p>'
    '<p>Pamela O. Long\'s analysis of Agricola in the context of the "openness" tradition in'
    ' technical knowledge — her argument that the sixteenth century saw a significant shift'
    ' toward public disclosure of craft secrets — situates <i>De Re Metallica</i> as part of'
    ' a broader cultural movement toward print publication of technical knowledge that had'
    ' previously been transmitted only through craft apprenticeship. [LINK:pamela-smith]\'s'
    ' complementary work on artisanal epistemology and the body of the artisan engages with'
    ' the same transition. Agricola\'s text is thus important not only for the specific'
    ' metallurgical knowledge it preserves but as evidence for how the relationship between'
    ' written natural philosophy and workshop practice was being renegotiated in sixteenth-century'
    ' central Europe.</p>'
)

# ── Elias Ashmole ──────────────────────────────────────────────────────────────

ASHMOLE_EXTRA = (
    '<h2>Theatrum Chemicum Britannicum and the Royalist Alchemical Tradition</h2>'
    '<p>Ashmole\'s <i>Theatrum Chemicum Britannicum</i> (1652) is the most important compilation'
    ' of English alchemical verse and the principal source for the texts of [LINK:george-ripley]'
    ' and other medieval and early modern English practitioners. Ashmole assembled these texts'
    ' with scholarly annotations, situating them within a tradition of English alchemical practice'
    ' that he understood as continuous from the medieval period through his own time. The collection'
    ' appeared in the same year as the English Commonwealth was consolidating — the execution of'
    ' Charles I had taken place in 1649 — and Ashmole\'s Royalist politics intersected with his'
    ' alchemical interests in a program for restoring traditional learning alongside the traditional'
    ' monarchy.</p>'
    '<p>Ashmole\'s institutional legacy is the Ashmolean Museum at Oxford, which he founded in'
    ' 1677 by donating his collection of natural curiosities, coins, manuscripts, and artifacts'
    ' to the University. It is the oldest public museum in Britain. The alchemical manuscripts'
    ' and books in his collection — the Ashmole collection at the Bodleian Library — represent'
    ' one of the most important repositories of English alchemical materials and have been'
    ' extensively used by subsequent scholars including Jennifer Rampling and other historians'
    ' of English alchemy.</p>'
    '<p>Ashmole was a Freemason, an astrologer, a member of the early Royal Society, and an'
    ' antiquary of considerable learning. His trajectory — from Royalist exile to founding'
    ' Oxonian institutionalist — reflects the complex politics of knowledge in Restoration'
    ' England. His simultaneous interest in alchemy, astrology, Rosicrucianism, and the new'
    ' experimental philosophy of the Royal Society is characteristic of a generation for which'
    ' these pursuits were not yet clearly separated into legitimate science and disreputable'
    ' occultism. The construction of that separation — which Newman and [LINK:lawrence-principe]'
    ' have analyzed as a retrospective distortion — was still in process during Ashmole\'s'
    ' lifetime, and his career illustrates the mixed cultural landscape before the separation'
    ' was complete.</p>'
    '<p>His personal engagement with alchemical practice is attested by his diary and correspondence.'
    ' He received alchemical instruction from William Backhouse, who he credited as his "adopted'
    ' father" in alchemy and who communicated a version of the Philosophers\' Stone secret to him.'
    ' This personal transmission dimension of Ashmole\'s alchemy connects him to the broader'
    ' pattern of master-pupil transmission that structured early modern alchemical culture —'
    ' the same pattern that organized [LINK:george-starkey]\'s relationship to his mentors and'
    ' that [LINK:isaac-newton] sought to access through the published texts of Philalethes.</p>'
)

# ── Heinrich Khunrath ──────────────────────────────────────────────────────────

KHUNRATH_EXTRA = (
    '<h2>The Amphitheatrum and Christian Alchemy</h2>'
    '<p>Khunrath\'s <i>Amphitheatrum Sapientiae Aeternae</i> (Amphitheater of Eternal Wisdom, first'
    ' complete edition 1609) is among the most elaborate productions of Renaissance Christian'
    ' alchemy. Its five large engraved plates — the "oratory-laboratory," the round amphitheater'
    ' image, and three others — combine laboratory imagery with religious symbols, Hebrew'
    ' inscriptions, and geometric figures in a visual language that insists on the inseparability'
    ' of prayer and laboratory practice. The "oratory-laboratory" plate shows a working chemical'
    ' laboratory on one side with an oratory (prayer space) on the other, connected by a'
    ' corridor: the message is that laboratory work is simultaneously religious work, and'
    ' that neither alone is sufficient for the alchemical goal.</p>'
    '<p>Khunrath was a physician and Paracelsian practitioner who trained at Basel and'
    ' practiced in Hamburg, Dresden, and elsewhere. His connection to the Paracelsian tradition'
    ' is visible in his emphasis on the tria prima (sulfur, mercury, salt) and in his'
    ' identification of the Philosophers\' Stone with Christ — a specifically Christian'
    ' appropriation of alchemical symbolism that was part of a broader late sixteenth-century'
    ' Protestant alchemy that sought to integrate laboratory practice with Lutheran piety.'
    ' The identification of the Stone with Christ (lapis-Christus parallel) was not original'
    ' to Khunrath but reached its most elaborate expression in his work.</p>'
    '<p>The <i>Amphitheatrum</i> was influential on the Rosicrucian movement and on subsequent'
    ' German Protestant alchemy. [LINK:robert-fludd] engaged with the same Christian-Hermetic'
    ' synthesis. Johann Valentin Andreae, whose <i>Chymical Wedding of Christian Rosencreutz</i>'
    ' (1616) is the most literary of the Rosicrucian texts, moved in related circles. The'
    ' visual language of the <i>Amphitheatrum</i> plates influenced subsequent alchemical'
    ' emblem books and contributed to the tradition of emblematic alchemy that culminated in'
    ' Michael Maier\'s <i>Atalanta Fugiens</i> (1617). The combination of serious laboratory'
    ' engagement with elaborate religious symbolism in Khunrath\'s work illustrates the'
    ' degree to which alchemy in this period was understood by its practitioners as a unified'
    ' spiritual-material inquiry rather than a purely technical pursuit.</p>'
    '<p>Peter Forshaw\'s scholarship on Khunrath provides the most systematic modern treatment,'
    ' analyzing the <i>Amphitheatrum</i> in detail and situating it within the broader context'
    ' of late sixteenth-century Paracelsian and Hermetic learning. Forshaw\'s work demonstrates'
    ' that Khunrath was a sophisticated reader of multiple traditions — Kabbalah, Hermetic'
    ' philosophy, Paracelsian medicine, Lutheran theology — and that the synthesis he produced'
    ' was not an incoherent juxtaposition but a carefully constructed intellectual position'
    ' with its own internal logic.</p>'
)

# ── Basilius Valentinus ────────────────────────────────────────────────────────

VALENTINUS_EXTRA = (
    '<h2>The Problem of Authorship and the Antimony Texts</h2>'
    '<p>The works attributed to Basil Valentine — including <i>Triumphwagen Antimonii</i>'
    ' (Triumphal Chariot of Antimony, 1604), <i>Die zwölff Schlüssel</i> (Twelve Keys), and'
    ' several other treatises — present a biographical problem similar to that of [LINK:nicholas-flamel]:'
    ' the claimed author (a fifteenth-century Benedictine monk at Erfurt) cannot be documented'
    ' in any historical records, and the texts themselves appear to date from the late sixteenth'
    ' or early seventeenth century. The publisher Johann Tholde, who brought the texts to print,'
    ' is now considered by many scholars including Lawrence Principe to be the actual author'
    ' rather than merely the editor — another case of pseudepigraphal composition attaching'
    ' practical chemical knowledge to an invented ancient adept for purposes of authority and'
    ' marketability.</p>'
    '<p>Regardless of authorship questions, the chemical content of the Valentine texts is'
    ' genuine and significant. <i>Triumphwagen Antimonii</i> provides detailed accounts of the'
    ' preparation and medical use of antimony compounds — the same compounds whose controversial'
    ' use in medicine precipitated one of the major medical controversies of the seventeenth'
    ' century. The dispute over antimony in France, where the Paris Faculty of Medicine tried'
    ' to ban it and the court physicians used it successfully to treat Louis XIV, illustrates'
    ' how directly alchemical chemical knowledge intersected with practical medical politics.'
    ' The Valentine texts were central to this controversy as sources of preparation methods'
    ' and theoretical justifications for antimony medicine.</p>'
    '<p>The sulphur-mercury-salt (tria prima) framework in the Valentine texts reflects'
    ' Paracelsian influence, and the texts have been used to argue for a continuous tradition'
    ' from Paracelsian iatrochemistry through the more experimentally oriented chymistry of'
    ' the mid-seventeenth century. [LINK:george-starkey] engaged with the Valentine tradition,'
    ' and the Valentinian procedures for antimony were part of the stock of practical chemical'
    ' knowledge that practitioners including [LINK:robert-boyle] had access to and worked with.'
    ' The pseudonymous construction of Basil Valentine as an ancient authority thus served'
    ' a real function in authorizing practical chemical procedures for a generation that relied'
    ' on transmitted expert knowledge and the weight of precedent.</p>'
    '<p>Lawrence Principe and William Newman have discussed the Valentine texts in the context'
    ' of their broader analysis of pseudonymity and authority in early modern chymistry.'
    ' Principe\'s laboratory work has included preparation of antimony compounds following'
    ' Valentine procedures, demonstrating that the chemical content is operationally coherent'
    ' and that the procedures produce the compounds described. This laboratory confirmation'
    ' of the texts\' practical reliability — whatever their historical provenance — is'
    ' consistent with the broader finding that early modern chymical texts, even when their'
    ' claimed authorship is false, often preserve genuine chemical knowledge accumulated'
    ' through actual laboratory practice.</p>'
)

# ── Michela Pereira ────────────────────────────────────────────────────────────

PEREIRA_EXTRA = (
    '<h2>Pseudo-Lullian Alchemy and Medieval Transmission</h2>'
    '<p>Pereira\'s scholarship centers on the pseudo-Lullian alchemical corpus — a body of texts'
    ' attributed to Ramon Lull (1232–1316) but written after his death, some as late as the'
    ' fifteenth century — and on its relationship to the genuine Lullian intellectual project'
    ' of philosophical synthesis. The genuine Lull was a Catalan philosopher, missionary, and'
    ' mystic who developed the Ars Magna, a combinatorial system for demonstrating the truths'
    ' of Christianity to Muslims and Jews through logical argument. He explicitly condemned'
    ' alchemy in his authentic writings. The massive pseudo-Lullian alchemical corpus — texts'
    ' including <i>Testamentum</i>, <i>Codicillus</i>, <i>Liber Mercuriorum</i>, and dozens'
    ' of others — was thus attributed to a philosopher who had rejected alchemy, a paradox'
    ' that Pereira has analyzed as evidence for the authority-seeking strategies of late'
    ' medieval alchemical writers.</p>'
    '<p>Her critical edition and study of the pseudo-Lullian <i>Testamentum</i> established'
    ' the documentary foundations for understanding this corpus. The <i>Testamentum</i> is'
    ' the central text of pseudo-Lullian alchemy, presenting a sophisticated account of'
    ' the philosophical mercury (quinta essentia) as the foundation of alchemical process'
    ' and connecting alchemical theory to the Aristotelian account of generation and corruption.'
    ' Pereira\'s analysis of the relationship between this text and [LINK:john-of-rupescissa]\'s'
    ' quintessence concept demonstrates that the pseudo-Lullian corpus appropriated and'
    ' transformed the Rupescissian material rather than simply repeating it — a process of'
    ' intellectual transformation that she has traced in detail.</p>'
    '<p>Her broader contribution to the historiography of medieval alchemy lies in demonstrating'
    ' that the pseudo-Lullian tradition was not a mere collection of borrowed material but a'
    ' sophisticated intellectual tradition with its own distinctive theoretical positions and'
    ' its own strategies for legitimating alchemical practice within the scholastic framework'
    ' of medieval Latin learning. Her work intersects with that of [LINK:william-newman] on'
    ' the <i>Summa Perfectionis</i> tradition and with the broader project of recovering'
    ' the intellectual history of medieval Latin alchemy as a serious component of'
    ' scholastic natural philosophy.</p>'
)

# ── Muhammad al-Razi ───────────────────────────────────────────────────────────

RAZI_FULL = (
    '<p>Muhammad ibn Zakariya al-Razi (854–925 CE), known in the Latin West as Rhazes, was one'
    ' of the most prolific and influential scholars of the medieval Islamic world. A physician'
    ' who directed hospitals in Ray (near modern Tehran) and Baghdad, he was simultaneously a'
    ' major alchemical theorist and practitioner — a combination that reflects the integration'
    ' of medicine and alchemy in the Islamic intellectual tradition that he helped to define.</p>'
    '<h2>Chemical and Alchemical Contributions</h2>'
    '<p>Al-Razi\'s alchemical writings, particularly the <i>Kitab al-Asrar</i> (Book of Secrets)'
    ' and <i>Kitab Sirr al-Asrar</i> (Book of the Secret of Secrets), represent the most'
    ' systematic classification of chemical substances and operations in the early medieval'
    ' period. His classification of substances into animal, vegetable, and mineral categories,'
    ' and his subdivision of minerals into spirits (volatile substances: mercury, sulfur,'
    ' arsenic, sal ammoniac), bodies (metals), stones, vitriols, boraces, and salts, provided'
    ' the most comprehensive chemical taxonomy available before the development of modern'
    ' chemistry. This classification was translated into Latin and influenced European'
    ' alchemical and medical chemistry through the medieval period.</p>'
    '<p>Al-Razi\'s chemical work was distinguished by his emphasis on systematic laboratory'
    ' procedure. He described in unusual detail the equipment used for distillation, sublimation,'
    ' calcination, and other operations; the specific substances and their behavior under'
    ' different treatments; and the sequences of operations required to prepare particular'
    ' products. This operational specificity — combined with systematic classification —'
    ' made his texts valuable practical references for subsequent practitioners in both'
    ' the Islamic world and, through Latin translation, medieval Europe.</p>'
    '<p>His <i>Kitab al-Mansuri</i> (Liber Almansoris) and the encyclopedic <i>Al-Hawi</i>'
    ' (Continens Liber) were translated into Latin in the twelfth and thirteenth centuries'
    ' and became standard medical texts in European universities. The chemical knowledge'
    ' embedded in his medical works — particularly his account of mineral drugs, their'
    ' preparation, and their therapeutic use — was absorbed into the Latin medical tradition'
    ' alongside his clinical and theoretical contributions. His influence on [LINK:avicenna]\'s'
    ' synthesis and on the development of Latin medical-alchemical tradition through'
    ' [LINK:roger-bacon] and others was significant and has been analyzed by Shlomo Pines'
    ' and Martin Levey in studies of medieval Islamic pharmacology and chemistry.</p>'
    '<p>Al-Razi\'s theoretical alchemy differed from the Jabirian tradition in significant ways.'
    ' Where the Jabirian corpus developed an elaborate system of numerical-philosophical'
    ' alchemy involving the "balance" of qualities, al-Razi\'s approach was more directly'
    ' empirical: his theoretical framework (sulphur-mercury theory for metallic generation)'
    ' was relatively simple compared to the elaborate Jabirian system, and his emphasis was'
    ' on careful observation and classification rather than philosophical systematization.'
    ' This empirical orientation — whatever its ultimate explanation — made his texts'
    ' particularly valuable for practitioners seeking specific procedural guidance and'
    ' contributed to his enduring influence in both medical and alchemical traditions.</p>'
)

# ── Geoffrey Chaucer ───────────────────────────────────────────────────────────

CHAUCER_EXTRA = (
    '<h2>The Canon\'s Yeoman\'s Tale and Alchemical Satire</h2>'
    '<p>The Canon\'s Yeoman\'s Tale in <i>The Canterbury Tales</i> (c. 1390s) is the most'
    ' sustained literary engagement with alchemy in Middle English and one of the most'
    ' important literary sources for the social world of practical alchemy in late medieval'
    ' England. The tale presents a con-artist canon who uses alchemical demonstrations to'
    ' defraud a London priest, employing sleight of hand — a hollow coal loaded with silver'
    ' filings, a hollow stirring rod — to fake the production of gold. The Yeoman who tells'
    ' the tale has spent years working for this canon in the hope of learning the Philosophers\'</p>'
    ' Stone, impoverishing himself in the process. The tale\'s critique is double: it attacks'
    ' fraudulent practitioners while acknowledging that genuine inquiry is being corrupted'
    ' by the existence of fraud.</p>'
    '<p>The tale\'s chemical vocabulary is extensive and largely accurate: Chaucer uses the'
    ' technical terminology of practical alchemy — specific substances (cinnabar, arsenic,'
    ' sal ammoniac, vitriol), specific operations (sublimation, distillation, calcination),'
    ' specific equipment — in ways that indicate familiarity with the actual practice rather'
    ' than merely its literary representation. This has led scholars including Edgar Duncan'
    ' and Stanton Linden to argue that Chaucer had some direct acquaintance with alchemical'
    ' practice, possibly through his contact with the royal court and the London merchant'
    ' community in which alchemical patronage and fraud were both common. His Scrivener\'s'
    ' position, his diplomatic travels, and his contact with the educated world of late'
    ' medieval London would have given him ample opportunity to encounter both serious'
    ' practitioners and con artists.</p>'
    '<p>The ambivalent ending of the Canon\'s Yeoman\'s Tale — in which the Yeoman suggests'
    ' that the true Philosophers\' Stone may exist but that God does not want it found by'
    ' ordinary means — reflects the genuine uncertainty in which late medieval educated'
    ' culture held alchemical claims. Chaucer does not simply debunk alchemy; he distinguishes'
    ' between fraudulent practice and the possibility of genuine achievement while leaving'
    ' the outcome of genuine pursuit open. This nuanced position is consistent with the'
    ' mainstream fourteenth-century scholastic assessment, which rejected fraudulent'
    ' alchemy while leaving open the theoretical possibility of genuine transmutation.'
    ' The tale is thus valuable not only as satire but as evidence for how alchemy was'
    ' understood by a sophisticated late medieval lay audience.</p>'
)

# ── Tycho Brahe ────────────────────────────────────────────────────────────────

BRAHE_EXTRA = (
    '<h2>Alchemy and Astronomy at Uraniborg</h2>'
    '<p>Tycho Brahe\'s alchemical laboratory at Uraniborg (built from 1576 on the Danish island'
    ' of Hven, funded by Frederick II of Denmark) was not a peripheral hobby but an integral'
    ' part of his research program. The basement of the observation tower contained furnaces'
    ' and equipment for chemical work; Tycho produced medicines including herbal preparations'
    ' and "theriac" for distribution to local populations. His alchemy was Paracelsian in'
    ' orientation: chemical medicines rather than transmutational gold-making, integrated with'
    ' his astronomical work through the shared framework of cosmic sympathy and planetary'
    ' influence on terrestrial substances.</p>'
    '<p>The relationship between Tycho\'s astronomical observations and his natural philosophy'
    ' — which rejected both Ptolemaic geocentrism and Copernican heliocentrism in favor of'
    ' the Tychonic system (planets orbit the Sun, which orbits the Earth) — reflects a'
    ' consistent commitment to empirical observation over theoretical speculation. His'
    ' insistence on precise observation, which drove the construction of the elaborate'
    ' quadrants and sextants at Uraniborg that were the most accurate pre-telescopic'
    ' instruments in existence, extended to his chemical work: the laboratory notebooks'
    ' that survive suggest careful attention to specific preparations and their results.'
    ' Victor Thoren\'s biography <i>The Lord of Uraniborg</i> (1990) provides the'
    ' scholarly foundation for understanding Tycho\'s integrated research program.'
    ' John Robert Christianson\'s study of Tycho\'s workshop and his students situates'
    ' the alchemy within the broader intellectual economy of Uraniborg.</p>'
    '<p>Tycho\'s alchemical interests connect him to the central European tradition of'
    ' court alchemy that flourished under Rudolf II in Prague, where Tycho moved his'
    ' operations after 1599. The Prague court attracted alchemical practitioners alongside'
    ' astronomers, painters, and humanist scholars; [LINK:michael-sendivogius] was among'
    ' the alchemical figures in Rudolf\'s orbit. The intersection of Tycho\'s astronomical'
    ' authority with alchemical patronage culture illustrates how the pursuit of'
    ' transmutational alchemy was integrated into the most prestigious natural philosophical'
    ' enterprise of the late sixteenth century rather than being a marginal or disreputable'
    ' activity conducted separately from legitimate science.</p>'
)

# ── Johannes Trithemius ────────────────────────────────────────────────────────

TRITHEMIUS_EXTRA = (
    '<h2>Steganography, Magic, and Natural Knowledge</h2>'
    '<p>Trithemius\'s <i>Steganographia</i> (c. 1499, printed 1606) is the foundational text'
    ' of Western cryptography: it presents a system of coded communication using apparent'
    ' magical invocations as its vehicle, the magical language concealing a straightforward'
    ' cipher. The text was long regarded as a genuine work of angel magic — and attacked as'
    ' such — until the cipher was decoded by Thomas Ernst and Jim Reeds in 1999, demonstrating'
    ' that books one and two were cryptographic manuals rather than magical ones. The'
    ' combination of apparent magic with hidden cipher is characteristic of Trithemius\'s'
    ' approach to occult knowledge: the surface conceals a practical technique accessible'
    ' to those with the key, while appearing incomprehensible or supernatural to those without it.</p>'
    '<p>Trithemius\'s relationship to alchemy was primarily as an institutional context-setter'
    ' rather than as a practitioner. As Abbot of Sponheim (from 1483) and then of St. Jakob'
    ' in Würzburg, he built up one of the largest libraries in Germany and corresponded with'
    ' the leading humanist scholars of his era. His <i>Antipalus Maleficiorum</i> attacked'
    ' popular magic and witchcraft while his other works engaged with learned magic and'
    ' natural philosophy in more positive terms — a double position characteristic of'
    ' many sixteenth-century intellectual figures. His influence on [LINK:henry-cornelius-agrippa]'
    ' was direct and acknowledged: Agrippa visited Trithemius at Würzburg in 1509 and'
    ' showed him the early version of <i>De Occulta Philosophia</i>; Trithemius advised'
    ' him to keep the work private and not expose it to the ignorant crowd.</p>'
    '<p>Trithemius\'s historiographical significance for alchemy lies in his position in'
    ' the network of early sixteenth-century learned magic that provided the intellectual'
    ' context for Agrippa\'s synthesis and through Agrippa for the development of the'
    ' tradition that connected to [LINK:john-dee], [LINK:robert-fludd], and the Rosicrucian'
    ' movement. His library at Sponheim represented an institutional resource for the'
    ' transmission of manuscript knowledge, and his correspondence network connected him'
    ' to scholars across Germany and beyond. Noel Brann\'s biography provides the'
    ' scholarly foundation for understanding Trithemius within this context.</p>'
)

# ── Nicholas of Cusa ───────────────────────────────────────────────────────────

CUSA_EXTRA = (
    '<h2>Learned Ignorance and Natural Philosophy</h2>'
    '<p>Cusanus\'s philosophical program, centered on the concept of <i>docta ignorantia</i>'
    ' (learned ignorance) — the recognition that God as infinite is unknowable through finite'
    ' human concepts, which leads to an infinite regress of approximation as our concepts'
    ' approach but never reach divine truth — had indirect but significant connections to'
    ' natural philosophical inquiry. His mathematical approach to infinity, his account of'
    ' the coincidence of opposites (<i>coincidentia oppositorum</i>) in the divine, and his'
    ' vision of the universe as an infinite sphere with no fixed center (anticipating Copernicus'
    ' in some formulations) shaped fifteenth-century natural philosophy in ways that are still'
    ' being assessed.</p>'
    '<p>His relationship to alchemy was peripheral but not absent. His <i>De Staticis'
    ' Experimentis</i> (On Experiments by Weight) proposes a program of quantitative'
    ' natural investigation through systematic weighing of substances — anticipating in a'
    ' philosophical rather than practical way the quantitative orientation that [LINK:joseph-black]'
    ' and ultimately [LINK:antoine-lavoisier] would develop. Whether this text had direct'
    ' influence on the development of quantitative chemistry is debated; what it demonstrates'
    ' is that the value of measurement as a tool of natural inquiry was recognized by fifteenth-century'
    ' philosophers before the systematic use of weighing in chemical research.</p>'
    '<p>Jasper Hopkins\'s translations and studies of Cusanus provide the scholarly foundation'
    ' for his philosophy. Donald Duclow and others have analyzed his relationship to the'
    ' Hermetic and Neoplatonic traditions. His broader significance for the intellectual'
    ' context of early modern alchemy lies in his vision of the universe as an infinite'
    ' and interconnected whole in which human inquiry could progressively approach but'
    ' never reach complete knowledge — a philosophical framework compatible with the'
    ' iterative, approximate, and self-correcting character of laboratory inquiry, and'
    ' one that influenced the Hermetic Neoplatonism of [LINK:marsilio-ficino] and'
    ' through him the broader Renaissance philosophical context in which alchemy'
    ' was understood.</p>'
)

# ── Robert Grosseteste ─────────────────────────────────────────────────────────

GROSSETESTE_EXTRA = (
    '<h2>Light Metaphysics and Oxford Natural Philosophy</h2>'
    '<p>Grosseteste\'s theory of light — his account that light is the first corporeal form,'
    ' the principle through which extension and matter are united in creation, and the medium'
    ' of divine action on the physical world — provided the metaphysical framework for his'
    ' approach to natural philosophy and particularly to optics. His commentaries on Aristotle\'s'
    ' <i>Posterior Analytics</i> established the methodology of experimental science at Oxford:'
    ' observation, inductive generalization, and deductive test. The connection to alchemy'
    ' is indirect but historically significant: the Oxford tradition of natural philosophy'
    ' that Grosseteste inaugurated, carried forward by [LINK:roger-bacon] and later Duns'
    ' Scotus, William of Ockham, and the fourteenth-century Oxford Calculators, provided'
    ' the intellectual context in which English alchemical practice developed.</p>'
    '<p>Grosseteste\'s influence on Roger Bacon was central to the development of Baconian'
    ' ideas about experimentum as a criterion in natural philosophy — ideas that Bacon'
    ' then applied to alchemical texts and practice, as [LINK:william-newman] has analyzed.'
    ' The genealogy Grosseteste → Bacon → English alchemical tradition is one of the'
    ' important transmission routes through which Oxford natural philosophical methodology'
    ' shaped medieval alchemical inquiry, making Grosseteste a background figure for'
    ' understanding the intellectual context of English medieval alchemy even though he'
    ' was not himself an alchemical writer.</p>'
    '<p>James McEvoy\'s study of Grosseteste\'s philosophy and A.C. Crombie\'s classic account'
    ' of the Oxford scientific tradition provide the scholarly framework. The recent critical'
    ' edition of Grosseteste\'s complete works (the Corpus Philosophorum Medii Aevi series)'
    ' has made his writings accessible for detailed study, enabling historians of medieval'
    ' natural philosophy to assess his place in the transmission of experimental methodology'
    ' to the later medieval period and ultimately to the early modern practitioners whose'
    ' work is the main concern of this timeline.</p>'
)

# ── Robert of Chester ──────────────────────────────────────────────────────────

CHESTER_EXTRA = (
    '<h2>First Latin Translation of an Alchemical Text</h2>'
    '<p>Robert of Chester\'s translation of the Arabic text known in Latin as <i>Liber de'
    ' Compositione Alchemiae</i> (Book on the Composition of Alchemy, completed 1144) is'
    ' the first datable Latin translation of an alchemical text and thus marks the formal'
    ' entry of alchemy into medieval European Latin scholarly culture. The translation was'
    ' made at the request of Herman the Dalmatian, Robert\'s colleague in the translation'
    ' movement of twelfth-century Spain and southern France through which Arabic scientific'
    ' and philosophical texts became available to European readers. Robert was working in'
    ' the same milieu as [LINK:gerard-of-cremona] and other translators who were systematically'
    ' converting the Arabic philosophical and scientific corpus into Latin.</p>'
    '<p>The <i>Liber de Compositione Alchemiae</i> is a dialogue attributed to the philosopher'
    ' Morienus with the Umayyad prince Khalid ibn Yazid, a legendary early Islamic patron of'
    ' alchemy who was believed to have arranged for Greek alchemical texts to be translated'
    ' into Arabic. Whether the dialogue is historically genuine or a literary construction'
    ' attributing alchemical knowledge to a prestigious early Islamic figure — the same'
    ' strategy of attributed authorship that characterized medieval alchemical writing in'
    ' all traditions — is uncertain. What is clear is that Robert\'s translation introduced'
    ' Latin readers to an alchemical text that connected the Arabic tradition to legendary'
    ' Greek origins and provided both theoretical framework (four qualities, transmutation'
    ' of metals) and narrative legitimation (royal patronage, ancient wisdom).</p>'
    '<p>Robert\'s broader career as a translator included a translation of al-Khwarizmi\'s'
    ' algebra (the first Latin algebra text) and a translation of the Quran. His alchemical'
    ' translation should therefore be understood not as an isolated act of occult interest'
    ' but as part of a systematic project of making Arabic knowledge available to Latin readers'
    ' — the same project that was transferring Aristotelian natural philosophy, mathematics,'
    ' astronomy, and medicine from Arabic to Latin in the same decades and that transformed'
    ' the intellectual foundations of European learning.</p>'
)

def load_all():
    conn = sqlite3.connect(DB)

    print('=== Robert Fludd ===')
    app(conn, 'robert-fludd', FLUDD_EXTRA)

    print('=== Theosebeia ===')
    app(conn, 'theosebeia', THEOSEBEIA_EXTRA)

    print('=== George Agricola ===')
    app(conn, 'george-agricola', AGRICOLA_EXTRA)

    print('=== Elias Ashmole ===')
    app(conn, 'elias-ashmole', ASHMOLE_EXTRA)

    print('=== Heinrich Khunrath ===')
    app(conn, 'heinrich-khunrath', KHUNRATH_EXTRA)

    print('=== Basilius Valentinus ===')
    app(conn, 'basilius-valentinus', VALENTINUS_EXTRA)

    print('=== Michela Pereira ===')
    app(conn, 'michela-pereira', PEREIRA_EXTRA)

    print('=== Muhammad al-Razi ===')
    setp(conn, 'muhammad-al-razi', RAZI_FULL)

    print('=== Geoffrey Chaucer ===')
    app(conn, 'geoffrey-chaucer', CHAUCER_EXTRA)

    print('=== Tycho Brahe ===')
    app(conn, 'tycho-brahe', BRAHE_EXTRA)

    print('=== Johannes Trithemius ===')
    app(conn, 'johannes-trithemius', TRITHEMIUS_EXTRA)

    print('=== Nicholas of Cusa ===')
    app(conn, 'nicholas-of-cusa', CUSA_EXTRA)

    print('=== Robert Grosseteste ===')
    app(conn, 'robert-grosseteste', GROSSETESTE_EXTRA)

    print('=== Robert of Chester ===')
    app(conn, 'robert-of-chester', CHESTER_EXTRA)

    conn.commit()
    conn.close()
    print('\n=== Done ===')

if __name__ == '__main__':
    load_all()
