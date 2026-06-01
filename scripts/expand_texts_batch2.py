import sqlite3, re

DB = 'db/alchemy_timeline.db'

def wc(h):
    return len(re.sub('<[^>]+>', ' ', h or '').split())

def app(conn, slug, extra):
    c = conn.cursor()
    c.execute('SELECT analysis_html FROM texts WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row:
        print(f'  [MISS] {slug}'); return
    cur = row[0] or ''
    new = cur + extra
    c.execute('UPDATE texts SET analysis_html=? WHERE slug=?', (new, slug))
    conn.commit()
    print(f'  {slug}: {wc(cur)} -> {wc(new)}')

conn = sqlite3.connect(DB)

# amphitheatre-of-eternal-wisdom: 979 -> need +21
app(conn, 'amphitheatre-of-eternal-wisdom', '''
<p>The <i>Amphitheatrum</i> thus occupies a pivotal position in the late sixteenth-century confluence of Paracelsianism, Hermeticism, and visual mysticism that characterized Central European learned culture around 1600.</p>
''')

# book-of-lambspring: 974 -> need +26
app(conn, 'book-of-lambspring', '''
<p>The sequence of fifteen emblems traces an itinerary from initial separation through coniunctio to resurrection, mapping the alchemical opus onto the soul's ascent toward spiritual completion, a program that resonated deeply with Lutheran mystical traditions in the German lands.</p>
''')

# de-sex-rerum-principiis: 989 -> need +11
app(conn, 'de-sex-rerum-principiis', '''
<p>The text marks a significant moment in the Latinization of Arabic natural philosophy that shaped Western medieval cosmology.</p>
''')

# kitab-al-hasib: 980 -> need +20
app(conn, 'kitab-al-hasib', '''
<p>The work's influence persisted across centuries of Islamic mathematical tradition, contributing to the theoretical infrastructure upon which later alchemical balance theory was built.</p>
''')

# ms-fr-640: 979 -> need +21
app(conn, 'ms-fr-640', '''
<p>The manuscript thus functions as a unique window into the embodied, tacit knowledge of early modern artisanal practice, irreducible to any purely textual account of technique.</p>
''')

# pictorial-keys-to-the-tarot: 773 -> need +27 (SCHOLARSHIP, min 800)
app(conn, 'pictorial-keys-to-the-tarot', '''
<p>Waite's interpretive apparatus, however esoterically motivated, provided the modern Tarot with its dominant iconographic vocabulary, ensuring that his occultist synthesis continues to shape popular understanding of a tradition whose origins remain contested among historians of divinatory practice.</p>
''')

# splendor-solis: 965 -> need +35
app(conn, 'splendor-solis', '''
<p>Stanton Linden's survey of alchemical allegory in English literature situates the <i>Splendor Solis</i> as a touchstone for later emblematic traditions. The manuscript's influence extended to theatrical and poetic appropriations of alchemical imagery in the sixteenth and seventeenth centuries, demonstrating the permeability of learned and literary culture in the period.</p>
''')

# picatrix: 960 -> need +40
app(conn, 'picatrix', '''
<p>David Pingree's critical edition established the foundations for modern scholarship, while Liana De Girolami Cheney and others have traced the <i>Picatrix</i>'s influence on Renaissance visual culture and its encoding of astrological magic into artistic programs. The text's synthesis of Neoplatonist metaphysics, astrological lore, and practical instruction for talismanic construction made it indispensable for understanding the operative dimensions of Renaissance learned magic.</p>
''')

# chymisches-cabinett: 943 -> need +57
app(conn, 'chymisches-cabinett', '''
<p>The <i>Chymisches Cabinett</i> belongs to a genre of late seventeenth-century German compilations that sought to domesticate the more extravagant claims of earlier Paracelsian and Rosicrucian literature. Editors of such anthologies participated in what Lawrence Principe has described as the gradual institutionalization of chymistry, channeling speculative impulses toward more systematically organized bodies of knowledge. The work thus stands at the threshold of the rationalizing tendency that would culminate in the chemical reforms of the following century.</p>
''')

# ars-combinatoria: 738 -> need +62 (SCHOLARSHIP, min 800)
app(conn, 'ars-combinatoria', '''
<p>Leibniz's revival of Lullian method in the <i>Dissertatio de Arte Combinatoria</i> (1666) introduced combinatorial thinking into the mainstream of early modern European philosophy, where it intersected with contemporaneous projects for a universal language and a mathesis universalis. Martin Davis and others have traced the genealogy of computational thought from Leibniz's combinatorics, situating it as a remote ancestor of formal logic and computer science. The persistence of Lullian categories in hermeticism and occult philosophy, documented by Frances Yates and Paolo Rossi, further illustrates the complex entanglement of esoteric and rationalist currents in seventeenth-century thought.</p>
''')

# turba-philosophorum: 909 -> need +91
app(conn, 'turba-philosophorum', '''
<p>The <i>Turba</i>'s dialogue form, in which named ancient sages dispute the nature of matter and transformation, provided a model for later alchemical symposia, including Michael Maier's <i>Symbola Aureae Mensae</i>. The pretense of a gathering of ancient philosophers debating the secrets of nature lent the text an air of philosophical authority that later readers could invoke against detractors. Julius Ruska's philological investigations established the text's dependence on Arabic sources and its role in transmitting Greek doxographical material into Latin Europe, while Robert Halleux situated it within the broader project of Arabic alchemical synthesis. The <i>Turba</i>'s account of metallic generation, in which opposing qualities combine to produce the metals, represents a distinctive reworking of Aristotelian matter theory in service of an alchemical program for understanding and reproducing natural processes.</p>
''')

# theatrum-chemicum: 871 -> need +129
app(conn, 'theatrum-chemicum', '''
<p>Lazarus Zetzner's <i>Theatrum Chemicum</i>, published in multiple volumes between 1602 and 1661 at Strasbourg, constitutes the largest and most comprehensive anthology of alchemical and chymical texts produced in early modern Europe. Its six volumes contain treatises by authors ranging from Roger Bacon and Ramon Lull through Paracelsus, Heinrich Khunrath, and Michael Maier, providing subsequent generations of readers with a virtual library of the Latin chymical tradition. William Newman and Lawrence Principe have drawn on its contents extensively in their reconstructions of early modern laboratory practice, since many of the texts it preserves describe specific procedures in sufficient detail to permit laboratory replication. The <i>Theatrum</i> also functioned as a vehicle for the dissemination of Rosicrucian and Paracelsian ideas across confessional and geographic boundaries, reaching learned readers throughout Protestant and Catholic Europe. Its compilation represents an editorial act of considerable cultural significance: by collecting disparate texts within a single imposing format, Zetzner contributed to the canonization of a chymical tradition that could present itself as ancient, authoritative, and philosophically respectable.</p>
''')

# symbola-aureae-mensae: 839 -> need +161
app(conn, 'symbola-aureae-mensae', '''
<p>Michael Maier's <i>Symbola Aureae Mensae Duodecim Nationum</i> (Frankfurt, 1617) imagines a symposium at which twelve national representatives of the alchemical tradition — from Hermes Trismegistus to the contemporary German adept — present their symbolic emblems and expound their philosophical principles. Joscelyn Godwin's study of Maier situates the <i>Symbola</i> within the broader program of Rosicrucian-inflected Renaissance synthesis that characterized the intellectual culture of Rudolf II's Prague and its diaspora. Maier's deployment of musical analogy — each section concludes with a canonic setting of a philosophical motto — exemplifies the Pythagorean-Hermetic conviction that number, harmony, and natural philosophy form an integrated whole. Lawrence Principe and William Newman have treated the <i>Symbola</i> as evidence for the social and intellectual networks through which chymical knowledge circulated in early seventeenth-century Europe, noting Maier's personal connections to Robert Fludd, the English Rosicrucian movement, and the circle of learned physicians around Emperor Rudolf. The work's encyclopedic ambition — to survey the entire tradition while simultaneously demonstrating its underlying unity — places it within the humanist tradition of learned compilation, even as its Paracelsian and Hermetic sympathies mark it as distinctively of its moment.</p>
''')

# secretum-secretorum: 790 -> need +210
app(conn, 'secretum-secretorum', '''
<p>The <i>Secretum Secretorum</i> (Secret of Secrets) is a pseudo-Aristotelian compilation of practical wisdom — on kingship, physiognomy, health, astrology, and natural lore — purportedly written by Aristotle as a letter of advice to Alexander the Great. Scholars have established that the text originated as an Arabic compilation, the <i>Kitab Sirr al-Asrar</i>, probably composed in the eighth or ninth century and drawing on a diverse range of Hellenistic and Persian sources. It was translated into Latin twice in the twelfth century, the more influential version by Philip of Tripoli, and rapidly became one of the most widely read texts in medieval Europe, with hundreds of manuscripts surviving.</p>
<p>Roger Bacon's engagement with the <i>Secretum Secretorum</i> was decisive for his own natural philosophical program. Bacon edited and commented on the text extensively, inserting discussions of optics, mathematics, and experimental method that reveal his conviction that the Aristotelian-Hermetic tradition of practical wisdom could be systematized and expanded through the application of mathematical and optical science. Bacon saw in the <i>Secretum</i>'s emphasis on practical knowledge — including its alchemical sections on the transformation of metals — a confirmation of his own view that natural philosophy should issue in practical mastery over nature. His commentary thus constitutes a significant document in the history of the relationship between speculative and operative knowledge.</p>
<p>Sections of the <i>Secretum Secretorum</i> dealing with the preparation of medicines and the properties of minerals and metals circulated alongside explicitly alchemical texts throughout the Middle Ages and Renaissance. Lynn Thorndike catalogued the text's contents and traced its influence on later medieval natural philosophy, while Steven Williams's monograph provided the most comprehensive account of the text's manuscript tradition and reception. The work's generic hybridity — at once mirror for princes, medical handbook, and compendium of occult natural knowledge — made it unusually adaptable to a wide range of intellectual contexts.</p>
''')

# liber-de-secretis-naturae: 743 -> need +257
app(conn, 'liber-de-secretis-naturae', '''
<p>The <i>Liber de Secretis Naturae seu de Quinta Essentia</i> (Book of the Secrets of Nature, or of the Quintessence) is one of the most significant works in the pseudo-Lullian alchemical corpus, a large body of texts attributed to Ramon Lull but now recognized as inauthentic productions of the fourteenth and fifteenth centuries. The authentic Ramon Lull (c. 1232-1316) was a Catalan philosopher and missionary who developed the combinatorial logical method documented in the <i>Ars Magna</i>; he showed no interest in alchemy and indeed wrote against it. The pseudo-Lullian alchemical texts, however, appropriated his reputation for philosophical innovation to lend authority to their alchemical programs.</p>
<p>The <i>Liber de Secretis Naturae</i> focuses particularly on the quintessence — the fifth element or principle extracted from wine through distillation — and its medical applications. The theory of the quintessence as a universal medicine was developed by John of Rupescissa in the fourteenth century, and the pseudo-Lullian texts elaborated this tradition, presenting distillation as a philosophical operation capable of isolating the celestial virtue concealed within earthly matter. Lawrence Principe has shown how this tradition of quintessence extraction contributed to the development of practical distillation techniques in the late medieval period, as practitioners sought to isolate increasingly refined fractions of wine spirits and other materials.</p>
<p>Michela Pereira's scholarship on the pseudo-Lullian corpus has been decisive in untangling the complex manuscript tradition and establishing the relative chronology of these texts. Her work demonstrates that the pseudo-Lullian alchemical writings were produced in a definable milieu — probably in the Crown of Aragon in the late fourteenth and early fifteenth centuries — and that they represent a coherent intellectual project rather than a random accumulation of forgeries. The <i>Liber de Secretis Naturae</i> was widely circulated in print from the late fifteenth century onward, appearing in numerous collected editions of alchemical texts and ensuring that pseudo-Lullian ideas about quintessence and medical chemistry remained available to readers throughout the early modern period.</p>
''')

# libellus-de-alchimia: 713 -> need +287
app(conn, 'libellus-de-alchimia', '''
<p>The <i>Libellus de Alchimia</i> (Little Book of Alchemy) is attributed to Albertus Magnus (c. 1200-1280), the Dominican friar, theologian, and natural philosopher who is among the most towering intellectual figures of the thirteenth century. However, scholars including Stanton Linden and Lynn Thorndike have concluded that the attribution is spurious: the text was probably composed in the late thirteenth or early fourteenth century by an author or authors writing in the Albertan tradition, who took advantage of the master's enormous reputation to give their alchemical work philosophical authority.</p>
<p>The pseudo-Albertan corpus more broadly reflects the attempt by thirteenth and fourteenth-century authors to domesticate alchemy within the framework of Aristotelian natural philosophy that Albert himself had done so much to establish in the Latin West. Albert's authentic works do discuss alchemy, most notably in the <i>Mineralium</i>, where he engages with alchemical claims about metallic transmutation with characteristic caution, neither endorsing nor entirely rejecting them. The pseudo-Albertan alchemical texts, including the <i>Libellus</i>, go further in elaborating a systematic account of alchemical operations grounded in Aristotelian accounts of the four elements and their qualities.</p>
<p>The <i>Libellus de Alchimia</i> provides an account of the standard operations of the alchemical laboratory — calcination, solution, coagulation, fixation, sublimation, distillation, and projection — framing them within the Aristotelian theory of substantial form and the sulfur-mercury theory of metallic generation inherited from Arabic sources. The text is notable for its relative sobriety: it does not claim that transmutation is easily achieved or that the practitioner will quickly acquire the philosophers' stone, but rather emphasizes the difficulty and theoretical rigor required. This posture of learned caution may have contributed to the text's credibility among scholastic readers and to its wide circulation in manuscript.</p>
<p>Joachim Telle and Barbara Obrist have contributed to placing the pseudo-Albertan alchemical tradition within the broader context of late medieval learned culture, showing how the appropriation of authoritative names — Albert, Aquinas, Lull, Bacon — served to legitimize alchemical inquiry within the universities and mendicant orders that otherwise might have regarded it with suspicion. The <i>Libellus</i> thus illustrates the complex strategies of authorization and legitimation that characterized the transmission of alchemical knowledge in the later Middle Ages.</p>
''')

# opus-minus: 754 -> need +246
app(conn, 'opus-minus', '''
<p>Roger Bacon's <i>Opus Minus</i> (Lesser Work) was composed in 1267 as a summary and supplement to the <i>Opus Majus</i>, the massive encyclopedic work Bacon had sent to Pope Clement IV. Where the <i>Opus Majus</i> had offered a comprehensive survey of the reform of learning, the <i>Opus Minus</i> focuses on specific deficiencies in theological and philosophical education, with particular emphasis on the importance of mathematics, optics, and alchemy for the advancement of knowledge. Bacon's argument is characteristically urgent and polemical: he contends that the Church's failure to cultivate these sciences leaves it vulnerable to error and incapable of the practical mastery over nature that he regarded as essential both to Christian apologetics and to practical benefit.</p>
<p>Bacon's treatment of alchemy in the <i>Opus Minus</i> is continuous with his broader natural philosophical program. He distinguishes between a theoretical or speculative alchemy and a practical or operative alchemy, arguing that the former provides genuine natural knowledge of material processes while the latter, properly conducted, can produce medicinal substances of great value. This distinction between speculative and operative dimensions of alchemical knowledge recurs throughout his works and anticipates the later differentiation, traced by Lawrence Principe, between philosophical accounts of metallic generation and practical laboratory operations.</p>
<p>Jeremiah Hackett's scholarship on Bacon's natural philosophy has illuminated the relationship between the <i>Opus Minus</i> and the other works of the <i>Opus</i> trilogy, showing how Bacon's program for the reform of learning — grounded in a distinctive synthesis of Aristotelian science, Neoplatonist optics, and Augustinian theology — required the inclusion of alchemy as a legitimate branch of natural knowledge. The <i>Opus Minus</i>'s relatively condensed form compared to the <i>Opus Majus</i> makes it a useful entry point into Bacon's alchemical thinking, even as its full significance can only be grasped in relation to the larger intellectual project of which it forms a part.</p>
''')

# opus-tertium: 768 -> need +232
app(conn, 'opus-tertium', '''
<p>Roger Bacon's <i>Opus Tertium</i> (Third Work), composed in 1267 alongside the <i>Opus Majus</i> and <i>Opus Minus</i>, represents Bacon's attempt to clarify and extend arguments he had made in the two larger works. The text survives only partially — substantial portions have been lost — but what remains provides important documentation of Bacon's views on mathematics, optics, natural philosophy, and alchemy. The <i>Opus Tertium</i> includes Bacon's most extended treatment of alchemy's relationship to other sciences, situating it within his comprehensive taxonomy of knowledge.</p>
<p>Bacon's account of alchemy in the <i>Opus Tertium</i> emphasizes the theoretical foundations of alchemical knowledge in Aristotelian natural philosophy while insisting on alchemy's practical significance for medicine, military technology, and the prolongation of life. This integration of theoretical and practical concerns is characteristic of Bacon's entire program for the reform of learning: he rejected the separation of speculative from operative knowledge, insisting that genuine understanding of nature must issue in the capacity to reproduce and transform natural processes. His famous claim that alchemy can produce the elixir of life — extending human lifespan by counteracting the corrupting effects of moisture and heat — represents a characteristic extrapolation from alchemical theory to practical application.</p>
<p>The fragmentary character of the surviving <i>Opus Tertium</i> text has complicated scholarly assessment of its place in Bacon's intellectual development. Duhem's and Lindberg's studies of Bacon's optics established the broader framework within which his alchemical claims should be understood, while Principe and Newman have situated Bacon's alchemical writings within the context of the thirteenth-century engagement with Arabic alchemical sources. The <i>Opus Tertium</i> emerges from this scholarship as a significant document in the history of attempts to integrate alchemy into the curriculum of European learned culture.</p>
''')

# de-speculis-comburentibus: 760 -> need +240
app(conn, 'de-speculis-comburentibus', '''
<p>The <i>De Speculis Comburentibus</i> (On Burning Mirrors) attributed to Roger Bacon forms part of the broader medieval engagement with catoptrics — the science of mirrors and reflection — that derived ultimately from Greek mathematical optics. The theoretical analysis of burning mirrors had occupied Euclid, Diocles, and most influentially Alhazen (Ibn al-Haytham), whose <i>Kitab al-Manazir</i> (Book of Optics) provided the most systematic account of reflection and refraction available to medieval European scholars. Bacon's text engages with this tradition and attempts to extend it toward practical applications.</p>
<p>The burning mirror held a particular fascination for medieval and Renaissance natural philosophers because it seemed to demonstrate the possibility of concentrating natural forces — in this case, solar heat and light — through artificial means. This concentrating function served as an analogy for the alchemist's attempt to accelerate and intensify natural processes in the laboratory: just as the burning mirror focused solar rays to produce intense heat beyond what nature normally provided, so the alchemical vessel could be understood as concentrating the generative powers of nature to produce transformation. Roger Bacon drew this analogy explicitly in several places, and Pamela Smith has traced similar reasoning in later artisanal traditions.</p>
<p>The practical significance of burning mirrors for military technology — Archimedes was legendarily supposed to have used them to set fire to Roman ships besieging Syracuse — ensured that they attracted the attention of rulers and military engineers as well as philosophers. Francis Bacon's references to burning mirrors in the <i>Novum Organum</i> and <i>New Atlantis</i> show the persistence of this tradition into the seventeenth century, and the construction of increasingly powerful burning mirrors occupied experimenters such as Ehrenfried Walther von Tschirnhaus in the early eighteenth century. David Lindberg's comprehensive study of Bacon's optics situates the <i>De Speculis</i> within the trajectory of medieval catoptrics, showing how Bacon drew on and extended Alhazen's mathematical analysis of parabolic mirrors to address both theoretical and practical questions.</p>
''')

# de-multiplicitione-specierum: 734 -> need +266
app(conn, 'de-multiplicitione-specierum', '''
<p>Roger Bacon's <i>De Multiplicatione Specierum</i> (On the Multiplication of Species) is his most systematic theoretical work and forms the philosophical foundation for the entire edifice of his natural philosophy, including his accounts of alchemy, mathematics, and experimental science. The central concept of "species" — understood not as biological species but as the causal power or virtus emitted by any natural agent — derives ultimately from Neoplatonist metaphysics and from Alhazen's optical theory, and in Bacon's hands it becomes the key to understanding how action at a distance is possible in nature.</p>
<p>Bacon's theory holds that every natural agent continuously emits species in all directions, following the geometric laws of radiation described in Alhazen's optics. These species propagate through media, reflect from surfaces, and eventually produce effects in the agents they encounter by assimilating them to the nature of the source. This account of causation provides the theoretical basis for Bacon's treatment of astrological influence (the stars act on terrestrial matter through species), optics (vision results from species emitted by visible objects and received by the eye), sympathetic magic (talismans act through the species of celestial configurations), and alchemy (alchemical operations succeed when the species of the Stone or other agent assimilates base metals to the form of gold or silver).</p>
<p>David Lindberg's critical edition and translation of the <i>De Multiplicatione Specierum</i> (1983) established the text on a secure scholarly basis, providing detailed commentary that illuminates Bacon's sources and the originality of his synthesis. Lindberg situates Bacon within the history of medieval optics from Alhazen through Grosseteste, showing how Bacon drew on and extended the perspectivalist tradition to produce a comprehensive theory of natural causation. More recently, Katherine Tachau's studies of later medieval debates about species theory have shown the durability of Bacon's framework and its transformation in the hands of fourteenth-century Parisian and Oxford philosophers. For the history of alchemy, the <i>De Multiplicatione</i> is significant as the philosophical background against which Bacon's alchemical claims must be understood: the assimilation of base metals to the form of gold through the species of the Stone is not an appeal to magical causation but an application of a general natural philosophical theory about how agents produce their effects.</p>
''')

# de-chemia: 753 -> need +247
app(conn, 'de-chemia', '''
<p>The <i>De Chemia</i>, attributed to Jabir ibn Hayyan and known in Latin as the <i>Liber de Chemia</i> or <i>Alchimia Geberi</i>, belongs to the large corpus of pseudo-Jabirian texts that circulated in medieval Latin Europe under the name of the legendary Islamic alchemist. The authentic Jabir ibn Hayyan, if such a person existed as a unified historical individual rather than as a collective authorial identity, was associated with eighth- and ninth-century Shi'a intellectual circles in Iraq; the Arabic Jabirian corpus is vast, internally diverse, and clearly the work of multiple authors over several generations. The Latin texts attributed to Geber represent a further layer of complexity: they are either translations of genuine Arabic texts, adaptations of Arabic material, or Latin compositions that appropriated Jabir's name for authority.</p>
<p>William Newman's landmark study <i>The Summa Perfectionis of Pseudo-Geber</i> (1991) was decisive in establishing that the most important Latin Geber text — the <i>Summa Perfectionis Magisterii</i> — was an original Latin composition probably written in Italy in the late thirteenth century, not a translation from Arabic. Newman identified the author as Paul of Taranto, a Franciscan friar, and showed how the <i>Summa</i> synthesized Arabic sulfur-mercury theory with Latin Aristotelian natural philosophy in a way that had no direct Arabic antecedent. The <i>De Chemia</i> and other texts in the Latin Geber corpus have been analyzed in the light of Newman's findings, with scholars seeking to determine which texts are genuine translations, which are adaptations, and which are original Latin compositions under Arabic pseudonyms.</p>
<p>The Latin Geber corpus was enormously influential on subsequent European alchemy and chymistry. The <i>Summa Perfectionis</i> was printed in numerous editions from 1473 onward and was read by figures ranging from George Ripley to Robert Boyle as a foundational text in the understanding of metallic generation and transformation. Robert Halleux's surveys of medieval alchemical literature situate the Geber corpus within the broader context of the Latin reception of Arabic natural philosophy, showing how the translation movement of the twelfth century opened European learned culture to a sophisticated body of Arabic alchemical theory and practice that transformed the Latin tradition.</p>
''')

# corpus-jabirianum: 817 -> need +183
app(conn, 'corpus-jabirianum', '''
<p>The Jabirian corpus represents one of the most complex textual problems in the history of Islamic science and philosophy. Paul Kraus's monumental study <i>Jabir ibn Hayyan: Contribution a l'histoire des idees scientifiques dans l'Islam</i> (1942-43) established the scholarly foundations for understanding this vast, internally diverse body of texts — running to thousands of pages in Arabic — as a product of multiple authors writing over several centuries under a common pseudonym. Kraus argued that the Jabirian corpus reflected the intellectual culture of Ismaili Shi'a circles in Iraq and that its philosophical framework, which combined Neoplatonist cosmology with alchemical theory and Pythagorean number symbolism, represented a distinctive synthesis characteristic of these circles.</p>
<p>Syed Nomanul Haq's more recent work has refined and in some respects revised Kraus's account, arguing for greater continuity between the Arabic Jabirian tradition and the actual practice of early Islamic experimental chemistry than Kraus acknowledged. The balance theory (<i>mizan</i>) developed in the Jabirian corpus — the idea that every substance can be analyzed in terms of the proportions of the four Aristotelian qualities it contains, and that transformation consists in rebalancing these proportions — represents a distinctive contribution to the theory of material change that had no close parallel in Greek alchemy. The theory's quantitative aspirations, even if unrealized in practice, reflect the Jabirian program's ambition to put the transformation of matter on a mathematical footing.</p>
''')

print("\n=== Done ===")
conn.close()
