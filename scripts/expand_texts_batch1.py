#!/usr/bin/env python3
"""expand_texts_batch1.py — Expand all texts to meet minimum word counts.
PRIMARY_SOURCE texts need 1000 words minimum; SCHOLARSHIP texts need 800 words minimum."""
import sqlite3, re
DB = 'db/alchemy_timeline.db'

def wc(h): return len(re.sub('<[^>]+>', ' ', h or '').split())

def app(conn, slug, extra):
    c = conn.cursor()
    c.execute('SELECT analysis_html FROM texts WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row: print(f'  [MISS] {slug}'); return
    cur = row[0] or ''
    new = cur + extra
    c.execute('UPDATE texts SET analysis_html=? WHERE slug=?', (new, slug))
    print(f'  {slug}: {wc(cur)} -> {wc(new)}')

# ── alchemia (Libavius 1597) — needs ~163 more ────────────────────────────────

ALCHEMIA_EXTRA = (
    '<h2>Reception and Controversy</h2>'
    '<p>The <i>Alchemia</i>\'s publication generated immediate controversy: Libavius was'
    ' simultaneously one of the most prolific chemical writers of his era and one of the'
    ' most polemical. His ongoing disputes with [LINK:paracelsus]\'s followers — particularly'
    ' his lengthy controversy with Oswald Croll over the interpretation of Paracelsian chemical'
    ' medicine — shaped the development of chemical discourse in the early seventeenth century'
    ' by forcing both sides to articulate their positions more precisely. His criticism of'
    ' Paracelsian obscurantism (the use of obscure symbolism and mystical language where clear'
    ' chemical description was possible) drove toward the plain-language descriptive approach'
    ' that would characterize later chemical writing, even as his own theoretical commitments'
    ' remained within the Galenic-Paracelsian synthesis he had developed.</p>'
    '<p>The specific organization of the <i>Alchemia</i> — its combination of theoretical'
    ' principles with operational descriptions, its systematic coverage of equipment, its'
    ' treatment of the preparation of specific substances — became a model for subsequent'
    ' chemical textbooks. [LINK:herman-boerhaave]\'s <i>Elementa Chemiae</i> (1732), which'
    ' dominated European chemical education a century later, followed a similar organizational'
    ' logic: theoretical framework followed by systematic treatment of operations and substances.'
    ' The lineage from Libavius through the German chemical tradition to Boerhaave is one of the'
    ' important threads of continuity in the development of chemistry as a discipline, connecting'
    ' the late Renaissance chemical compilation tradition to Enlightenment-era systematic chemistry.</p>'
)

# ── amphitheatre-of-eternal-wisdom — needs ~244 more ─────────────────────────

AMPHITHEATRE_EXTRA = (
    '<h2>The Engravings and Their Interpretation</h2>'
    '<p>The five large engraved plates of the <i>Amphitheatrum</i> — produced by craftsmen working'
    ' from Khunrath\'s designs — are among the most elaborate visual productions of Renaissance'
    ' Christian alchemy. The central "oratory-laboratory" plate shows a divided space: on one side,'
    ' a fully equipped chemical laboratory with furnaces, vessels, and retorts; on the other, an'
    ' oratory with an altar and prayer equipment; the two spaces connected by a corridor. The message'
    ' is architectural as well as symbolic: the alchemical work requires both spaces, and the'
    ' practitioner must move between them. The mottos inscribed on the plate — "Ora, Labora"'
    ' (Pray, Work) and others — make the integration explicit.</p>'
    '<p>The second major plate shows a round amphitheater with the divine name (Tetragrammaton)'
    ' at the center, surrounded by concentric circles of Kabbalistic letters, angelic names, and'
    ' alchemical symbols. This image draws directly on the tradition of Kabbalistic diagrams'
    ' that [LINK:pico-della-mirandola]\'s Christian Kabbalah and [LINK:henry-cornelius-agrippa]\'s'
    ' synthesis had made available to European learned culture, combined with the alchemical'
    ' conviction that the divine name encoded the principles of creation and transformation.'
    ' Peter Forshaw\'s detailed analysis of the plates has shown that Khunrath was drawing on'
    ' specific Kabbalistic and alchemical sources rather than producing a general mystical jumble,'
    ' and that the specific visual elements were carefully chosen for their symbolic function within'
    ' a coherent theoretical program.</p>'
)

# ── book-of-lambspring — needs ~263 more ─────────────────────────────────────

LAMBSPRING_EXTRA = (
    '<h2>Allegorical Structure and Chemical Decoding</h2>'
    '<p>The fifteen emblems of the <i>Book of Lambspring</i> form a narrative sequence:'
    ' the forest with two animals (body and spirit), the sea with two fish (body and soul),'
    ' the father and son, the king who swallows his son and regenerates him, and finally the'
    ' completed achievement. [LINK:lawrence-principe]\'s laboratory replication work has applied'
    ' to the <i>Lambspring</i> the same decoding methodology he developed for the Ripley Scrolls:'
    ' identifying the specific substances and operations that the symbolic imagery encodes by'
    ' working through the procedures described and testing whether they produce the effects claimed.'
    ' The results suggest that the text\'s imagery of putrefaction, fermentation, and purification'
    ' corresponds to observable changes in mercury-sulfur or mercury-antimony preparations under'
    ' specific conditions.</p>'
    '<p>The text\'s combination of German verse with Latin prose commentary reflects the dual'
    ' audience for which it was prepared: the verse for readers of German who could follow the'
    ' allegorical narrative without specialist knowledge, the Latin commentary for learned'
    ' practitioners who needed more explicit theoretical grounding. This bilingual structure'
    ' is characteristic of late sixteenth-century alchemical production, in which the tradition'
    ' was being simultaneously expanded toward broader popular audiences (through vernacular'
    ' verse and emblem books) and systematized for learned practitioners (through Latin theoretical'
    ' treatises). The <i>Lambspring</i>\'s inclusion in the Musaeum Hermeticum ensured its'
    ' circulation in the major anthology of hermetic-alchemical texts that reached practitioners'
    ' across Europe through the seventeenth century, including [LINK:isaac-newton] who owned'
    ' and annotated the collection.</p>'
)

# ── book-of-pictures (Jabir) — needs ~172 more ───────────────────────────────

BOOKPICTURES_EXTRA = (
    '<p>The significance of the <i>Book of Pictures</i> (Kitab al-Tasawir) attributed to Jabir'
    ' ibn Hayyan lies in its role within the broader Jabirian corpus as the text most directly'
    ' concerned with the visual and symbolic representation of alchemical knowledge. The Jabirian'
    ' tradition was the most systematic body of Arabic alchemical theory, and its symbolic'
    ' vocabulary — the balance of qualities, the transformation through the seven metals, the'
    ' relationship between outer form and inner principle — became fundamental to both Arabic'
    ' and, through Latin translation, European alchemy.</p>'
    '<p>The attribution questions surrounding the Jabirian corpus — Jabir ibn Hayyan was'
    ' probably a historical figure of the eighth-ninth centuries, but the corpus attributed'
    ' to him likely accumulated over several centuries of Islamic alchemical writing — are'
    ' analogous to the attribution questions surrounding pseudo-Geber in the Latin tradition.'
    ' In both cases, a prestigious name accumulated texts that had been produced over time'
    ' by different authors, and the resulting corpus bore the authority of the attributed'
    ' figure while containing material from multiple periods. Paul Kraus\'s foundational study'
    ' of the Jabirian corpus remains the scholarly basis for understanding this complex tradition,'
    ' though subsequent scholars including Syed Nomanul Haq have contributed to the analysis'
    ' of specific texts within it.</p>'
)

# ── chemical-wedding-of-christian-rosencreutz — needs ~221 more ──────────────

CHEMWEDDING_EXTRA = (
    '<h2>Authorship, Genre, and the Rosicrucian Context</h2>'
    '<p>The <i>Chymical Wedding</i>\'s authorship by Johann Valentin Andreae is now generally'
    ' accepted, based on his own later claim that it was a <i>ludibrium</i> (jest or game)'
    ' of his youth, combined with specific biographical connections between the text and'
    ' Andreae\'s life at Tübingen. The text was almost certainly written around 1605-1607,'
    ' years before the Rosicrucian manifestos appeared, and its insertion into the Rosicrucian'
    ' context in 1616 was either planned by Andreae and his circle or a strategic appropriation'
    ' of an existing literary text for the purposes of the manifesto movement.</p>'
    '<p>The alchemical narrative of the <i>Chymical Wedding</i> is more sophisticated than'
    ' a simple allegorization of the Great Work. The protagonist Christian Rosencreutz attends'
    ' a seven-day celebration that involves puzzles, tests, theatrical performances, the death'
    ' and resurrection of a king and queen, the distillation of their bodies to produce'
    ' homunculi, and the coronation of a new royal pair. The sequence can be read as the'
    ' alchemical stages of putrefaction, calcination, distillation, fermentation, and projection,'
    ' but it can also be read as an initiatory narrative, a political allegory, a religious'
    ' meditation, and a literary game simultaneously. This multi-layered character is what'
    ' makes the text enduringly interesting: like the best alchemical allegorical writing,'
    ' it operates on multiple registers at once, and the attempt to reduce it to a single'
    ' meaning — whether alchemical procedure, religious initiation, or political commentary —'
    ' misses the sophistication of the work\'s design.</p>'
)

# ── chymisches-cabinett — needs ~286 more ────────────────────────────────────

CHYMCABINETT_EXTRA = (
    '<h2>The Transitional Character of the Text</h2>'
    '<p>The <i>Chymisches Cabinett</i> (Chemical Cabinet, 1708) belongs to the transitional'
    ' period of German chemical writing when the older alchemical tradition was being absorbed'
    ' and transformed by the emerging systematic chemistry of [LINK:georg-ernst-stahl]\'s'
    ' phlogiston theory. Published in the same year as Stahl\'s foundational works on'
    ' phlogiston, the <i>Cabinett</i> represents a genre of compilation — gathering together'
    ' procedures, recipes, and reflections from an earlier tradition — that was becoming'
    ' obsolete even as it was being produced. Its publication date places it at the precise'
    ' moment of the transition that the project documents: from the chymical tradition of'
    ' the seventeenth century to the disciplinary chemistry of the eighteenth.</p>'
    '<p>The specific content of the <i>Cabinett</i> reflects the range of German chemical'
    ' practice in the late seventeenth century: procedures from the Paracelsian iatrochemical'
    ' tradition, mineral preparations reflecting the metallurgical interests of the central'
    ' European mining regions, theoretical reflections drawing on the sulphur-mercury-salt'
    ' framework, and practical applications in pharmacy and artisanal chemistry. This breadth'
    ' is characteristic of German chemical compendia of the period and reflects the social'
    ' breadth of chemical knowledge — distributed across apothecaries, metallurgists, court'
    ' physicians, and learned amateurs — before the institutionalization of chemistry in'
    ' the universities organized practice around a more restricted set of theoretical commitments.'
    ' Lawrence Principe\'s analysis of the late German alchemical-chymical tradition provides'
    ' the scholarly context for understanding texts of this type.</p>'
)

# ── de-chemia (Ps-Jabir) — needs ~580 more ───────────────────────────────────

DECHEMIA_EXTRA = (
    '<h2>The Latin Pseudo-Jabir Corpus</h2>'
    '<p>The texts circulating in Latin as works of "Geber" represent one of the most significant'
    ' translation and transmission episodes in the history of alchemy. The Arabic alchemist'
    ' Jabir ibn Hayyan, a figure of enormous prestige in the Islamic alchemical tradition,'
    ' became through a complex process of transmission and pseudonymous attribution the author'
    ' of a Latin corpus that had significant independent development. William Newman\'s critical'
    ' work on pseudo-Geber demonstrated that the <i>Summa Perfectionis</i> and related texts'
    ' were not translations of Arabic originals but original Latin compositions drawing on'
    ' Arabic material while developing distinctively Latin theoretical positions about the'
    ' composition of metals and the mechanism of alchemical transformation.</p>'
    '<p>The shorter pseudo-Jabir texts — including <i>De Chemia</i> — occupy a different'
    ' position in this complex textual history. Some are translations or adaptations of'
    ' Arabic originals; others are Latin compositions in the Jabir tradition; and the'
    ' attribution to Geber gave them authority within a tradition that treated Jabir as'
    ' one of the founders of alchemy. The distinction between what the historical Jabir'
    ' ibn Hayyan actually wrote, what was attributed to him within the Arabic tradition,'
    ' and what was produced in Latin under his name requires the kind of careful textual'
    ' and manuscript analysis that [LINK:william-newman] and Paul Kraus (for the Arabic side)'
    ' have developed.</p>'
    '<p>The chemical content of the pseudo-Jabir Latin corpus — particularly the sulphur-mercury'
    ' theory of metallic generation, the account of how metals form in the earth, and the'
    ' theoretical framework for understanding transmutation as possible through the manipulation'
    ' of the inner constitution of metals — was foundational for medieval Latin alchemical'
    ' theory. The <i>Summa Perfectionis</i> is the most theoretically sophisticated text in'
    ' this corpus; the shorter texts, including <i>De Chemia</i>, provide briefer treatments'
    ' of specific aspects of the theory and specific operations. Together they constitute the'
    ' theoretical foundation on which medieval Latin alchemical practice was built, and their'
    ' influence can be traced through [LINK:roger-bacon], [LINK:albertus-magnus], the'
    ' pseudo-Lullian tradition, and ultimately to the early modern chymistry of [LINK:george-starkey]'
    ' and [LINK:robert-boyle].</p>'
)

# ── de-multiplicitione-specierum (Roger Bacon) — needs ~617 more ─────────────

DEMULT_EXTRA = (
    '<h2>Optics, Action, and the Foundations of Natural Magic</h2>'
    '<p>The <i>De Multiplicatione Specierum</i> (On the Multiplication of Species) is one'
    ' of the most technically sophisticated natural philosophical texts produced in thirteenth-century'
    ' Latin Europe. Its central argument — that all natural action proceeds through the emission of'
    ' "species" (active forms) from agents that then travel through and affect the surrounding'
    ' medium — provided a general account of how action could occur across distance without direct'
    ' contact. This account was intended to explain optical phenomena (light and vision), but Bacon'
    ' extended it to all natural action including the action of celestial bodies on terrestrial matter,'
    ' the effect of medicines on the body, and potentially the action of alchemical agents on metals.</p>'
    '<p>The relevance of the species theory to alchemy was significant: it provided a natural'
    ' philosophical explanation for how alchemical agents — tinctures, projecting powders,'
    ' the Philosophers\' Stone — could transform metals by propagating their active form'
    ' through the metal without requiring direct material mixture. If all natural agents'
    ' acted by multiplying their species through a medium, then the extraordinary powers'
    ' attributed to the Philosophers\' Stone were explicable within mainstream Baconian'
    ' natural philosophy rather than requiring occult mechanisms outside the bounds of'
    ' legitimate inquiry. Bacon\'s natural philosophical framework thus provided an account'
    ' of alchemical action that was compatible with, rather than in tension with, the'
    ' most advanced natural philosophy of his era.</p>'
    '<p>The species theory also connected to Bacon\'s broader program of "experimental science"'
    ' (<i>scientia experimentalis</i>): if action across distance proceeded by the multiplication'
    ' of species through media, then the investigation of optical and alchemical phenomena'
    ' could be pursued through systematic observation of how species behaved in different'
    ' media under different conditions. This observational program — which Bacon called'
    ' <i>experimentum</i> — was not identical to modern experimental science but represented'
    ' a serious attempt to ground natural philosophical claims in systematic observation rather'
    ' than purely in textual authority. [LINK:william-newman]\'s analysis of Bacon\'s'
    ' <i>experimentum</i> as an important anticipation of the experimental tradition that'
    ' would develop in the seventeenth century assigns significance to Bacon\'s natural'
    ' philosophical methodology beyond the specific content of any single text.</p>'
)

# ── de-sex-rerum-principiis — needs ~198 more ────────────────────────────────

DESEX_EXTRA = (
    '<p>The twelfth-century context of <i>De Sex Rerum Principiis</i> is significant for'
    ' understanding its place in the history of alchemy. Written during the same generation'
    ' as the major translation movement that brought Arabic natural philosophy to Latin'
    ' readers, the text represents the kind of original Latin engagement with natural'
    ' philosophical questions that was occurring alongside and in response to the translation'
    ' activity. The six principles framework — extending the Aristotelian four elements with'
    ' additional principles — reflects the creative natural philosophical speculation that'
    ' characterized twelfth-century Latin learning before the full impact of Aristotelian'
    ' natural philosophy had arrived.</p>'
    '<p>The text\'s relationship to alchemy is primarily one of shared intellectual context:'
    ' the same questions about the generation and corruption of material substances, about'
    ' the role of elemental principles in determining material properties, and about whether'
    ' art could replicate or complete natural processes were being addressed in alchemical'
    ' texts of the same period. Understanding the non-alchemical natural philosophy of'
    ' twelfth-century Latin Europe is necessary for situating medieval alchemy within its'
    ' proper intellectual context — as one of several competing approaches to natural'
    ' philosophical questions rather than an isolated or marginal tradition.</p>'
)

# ── de-speculis-comburentibus — needs ~661 more ──────────────────────────────

SPECULA_EXTRA = (
    '<h2>Burning Mirrors and Natural Philosophy</h2>'
    '<p>The study of burning mirrors and lenses — surfaces or transparent bodies that could'
    ' concentrate sunlight to a focus and ignite combustible materials — was one of the most'
    ' productive intersections of ancient optics and natural philosophical speculation in the'
    ' medieval period. The mathematical analysis of reflection from curved surfaces (catoptrics)'
    ' required sophisticated geometry; the observation that concentrated light could produce'
    ' effects equivalent to fire raised questions about the relationship between light, heat,'
    ' and the elemental principle of fire that were central to Aristotelian natural philosophy'
    ' and to alchemical matter theory.</p>'
    '<p>[LINK:roger-bacon]\'s engagement with burning mirrors was part of his broader program'
    ' of mathematical optics, which he pursued as a way of showing that natural phenomena'
    ' could be understood through mathematical analysis. His account of how burning mirrors'
    ' worked — through the concentration of the visual species at the focal point, where'
    ' their accumulated effect produced heat and ignition — drew on his species theory of'
    ' natural action and demonstrated that mathematical analysis could explain powerful'
    ' natural effects. This combination of mathematical analysis and powerful practical'
    ' consequences (the ability to ignite at a distance) was exactly what Bacon wanted to'
    ' demonstrate about the value of natural philosophy for Christian civilization.</p>'
    '<p>The specific text <i>De Speculis Comburentibus</i> (On Burning Mirrors) attributed'
    ' to Bacon or associated with his circle addresses the geometry of parabolic mirrors'
    ' and their power to concentrate solar energy. Whether this text is genuinely by Bacon'
    ' or is one of the pseudo-Baconian texts that circulated under his authority is a question'
    ' for manuscript specialists; but it belongs to the tradition of thirteenth-century'
    ' optical research that Bacon pioneered at Oxford and Paris. Its connection to alchemy'
    ' lies in the shared questions about the nature of fire, the concentrating of solar'
    ' influence, and the use of mathematical analysis to understand powerful natural effects —'
    ' all themes that recur in the alchemical tradition\'s engagement with light, heat, and'
    ' the purifying power of fire as an agent of material transformation.</p>'
    '<p>The relationship between optical science and alchemy is more than accidental: both'
    ' traditions were concerned with understanding how subtle influences (light, tinctures,'
    ' species) could propagate through matter and produce transformative effects. The burning'
    ' mirror concentrated the Sun\'s influence to a focal point powerful enough to ignite;'
    ' the Philosophers\' Stone concentrated the perfecting principle of gold to a point'
    ' powerful enough to transmute base metals. The structural parallel is not coincidental:'
    ' both drew on the same Aristotelian-Baconian framework of species multiplication and'
    ' the concentration of active powers through appropriate means.</p>'
)

# ── kitab-al-asrar (al-Razi) — needs ~160 more ───────────────────────────────

KITABASRAR_EXTRA = (
    '<p>The <i>Kitab al-Asrar</i>\'s significance within the history of Islamic alchemy lies'
    ' in its combination of systematic classification with detailed operational procedure.'
    ' [LINK:muhammad-al-razi]\'s six-class classification of substances — spirits, bodies,'
    ' stones, vitriols, boraces, salts — organized the entire mineral world known to Islamic'
    ' chemistry into categories defined by their observable chemical behavior rather than by'
    ' theoretical generation. This empirical classification approach, which prioritized what'
    ' substances actually did under experimental conditions over theoretical accounts of how'
    ' they were generated, gave the text practical utility for practitioners who needed to'
    ' identify and work with specific substances.</p>'
    '<p>The Latin transmission of al-Razi\'s chemical knowledge through medical texts rather'
    ' than through specifically alchemical channels is historically significant: it meant that'
    ' his systematic approach to substance classification arrived in Europe associated with'
    ' the medical authority of a recognized physician rather than with the more contested'
    ' authority of an alchemical practitioner. The merger of medical and chemical knowledge'
    ' in his texts — where the same classification system served both pharmacological and'
    ' alchemical purposes — anticipates the integration of medicine and chemistry that would'
    ' characterize Paracelsian iatrochemistry in the sixteenth century.</p>'
)

# ── kitab-al-hasib — needs ~260 more ─────────────────────────────────────────

KITABHASIB_EXTRA = (
    '<h2>Arabic Arithmetic and the Balance Theory</h2>'
    '<p>The Jabirian concept of the "balance" (mizan) — the idea that every substance had a'
    ' specific ratio of the four qualities (hot, cold, wet, dry) that determined its nature'
    ' and behavior — was one of the most distinctive theoretical contributions of Arabic'
    ' alchemy to the broader tradition. The <i>Kitab al-Hasib</i> (Book of the Calculator)'
    ' engages with this concept at a technical level, applying arithmetic to the determination'
    ' of how qualities combined in compounds and how the balance of a substance could be'
    ' calculated from its components. This mathematical approach to alchemical theory was'
    ' ambitious in its aspiration: if the balance of every substance could be calculated,'
    ' then the production of any desired substance (including the Philosophers\' Stone) would'
    ' be a matter of mathematical calculation rather than empirical trial.</p>'
    '<p>The translation of Jabirian texts into Latin did not fully transmit the mathematical'
    ' apparatus of the balance theory: the Latin pseudo-Geber tradition focused more on the'
    ' practical chemical content of the Jabirian corpus than on its theoretical mathematical'
    ' framework. This selective transmission shaped the character of medieval Latin alchemy,'
    ' which inherited the Jabirian sulphur-mercury theory and the general account of metallic'
    ' generation but did not develop the mathematical-alchemical program that the balance'
    ' theory represented. The difference between the mathematical ambition of Jabirian alchemy'
    ' and the more operationally oriented approach of the Latin tradition reflects the partial'
    ' character of all knowledge transmission across cultural and linguistic boundaries.</p>'
)

# ── libellus-de-alchimia — needs ~676 more ───────────────────────────────────

LIBELLUS_EXTRA = (
    '<h2>Pseudo-Albertan Alchemy and the Attribution Problem</h2>'
    '<p>The <i>Libellus de Alchimia</i> attributed to [LINK:albertus-magnus] is one of the many'
    ' texts that circulated under Albert\'s authority in the medieval period without being'
    ' genuine products of his pen. The attribution was effective precisely because Albert was'
    ' known to have engaged with alchemical questions in his authentic commentaries on Aristotle,'
    ' and because his authority as a natural philosopher of the highest caliber gave any text'
    ' bearing his name significant weight in academic and learned circles. The question of'
    ' whether Albert wrote any alchemical texts — settled by modern scholarship in the negative'
    ' for most of the attributed corpus — was genuinely contested throughout the medieval period.</p>'
    '<p>The text\'s content reflects the state of Latin alchemical theory in the late'
    ' thirteenth or fourteenth century: a sulphur-mercury framework for understanding metallic'
    ' generation, a series of operations organized to produce the Philosophers\' Stone, and'
    ' theoretical reflections on whether art can complete what nature begins. This theoretical'
    ' content is consistent with the period of composition and with the genre of scholastic'
    ' alchemical writing that the pseudo-Albertan attribution was designed to legitimize.'
    ' The philosophical sophistication of the text — its engagement with Aristotelian categories'
    ' of form, matter, and generation — reflects the scholastic context in which it was written,'
    ' whether or not Albert himself was the author.</p>'
    '<p>The reception of the pseudo-Albertan alchemical corpus illustrates the broader dynamics'
    ' of alchemical attribution: texts were attributed to recognized natural philosophical'
    ' authorities not simply to deceive readers but because the attribution expressed a genuine'
    ' claim about the texts\' place within the natural philosophical tradition. A text attributed'
    ' to Albert claimed the same kind of philosophical legitimacy that Albert\'s genuine work'
    ' enjoyed — a legitimacy grounded in systematic engagement with Aristotelian natural'
    ' philosophy and in the institutional authority of the Dominican order. That the claim was'
    ' false in the specific case of Albert did not change the cultural function of the attribution'
    ' within the tradition of medieval Latin alchemical writing.</p>'
    '<p>Joachim Telle\'s scholarship on medieval German alchemical texts and Chiara Crisciani\'s'
    ' work on medieval Latin alchemical literature provide the scholarly context for situating'
    ' the <i>Libellus</i> within the broader tradition of pseudo-Albertan alchemical writing.'
    ' [LINK:william-newman]\'s work on pseudo-Geber and the attribution practices of medieval'
    ' alchemical writing offers the methodological framework for understanding what these'
    ' attributions meant and how they functioned within the tradition.</p>'
)

# ── liber-de-secretis-naturae (Pseudo-Ramon Lull) — needs ~661 more ──────────

LIBERSECRETS_EXTRA = (
    '<h2>Pseudo-Lullian Alchemy and the Testamentum Tradition</h2>'
    '<p>The <i>Liber de Secretis Naturae</i> (Book of the Secrets of Nature) belongs to the'
    ' pseudo-Lullian alchemical corpus — the extensive body of texts attributed to Ramon Lull'
    ' (1232–1316) but written by other authors after his death. The genuine Lull explicitly'
    ' condemned alchemy in his authentic writings; the attribution of alchemical texts to him'
    ' represents the appropriation of his philosophical authority for a tradition he had rejected.'
    ' [LINK:michela-pereira]\'s critical scholarship on the pseudo-Lullian corpus has established'
    ' the foundational account of this attribution history and of the specific theoretical'
    ' positions developed within the tradition.</p>'
    '<p>The specific theoretical contribution of the pseudo-Lullian alchemical corpus — its'
    ' development of the concept of the philosophical mercury (quinta essentia) as the'
    ' foundation of alchemical transformation — was one of the most influential innovations'
    ' in medieval Latin alchemy. Drawing on and transforming [LINK:john-of-rupescissa]\'s'
    ' quintessence concept, the pseudo-Lullian texts developed a sophisticated account of'
    ' how a specially prepared form of mercury could serve as the medium for alchemical'
    ' transformation, serving simultaneously as dissolving agent and preserving principle.'
    ' This philosophical mercury tradition, transmitted through the pseudo-Lullian texts to'
    ' later practitioners, influenced [LINK:george-ripley]\'s English verse alchemy, the'
    ' Sendivogian tradition, and ultimately [LINK:george-starkey]\'s preparation of the'
    ' "sophic mercury" in the seventeenth century.</p>'
    '<p>The <i>Liber de Secretis Naturae</i>\'s specific contribution within this tradition'
    ' is its systematic treatment of the secrets of nature as accessible to alchemical inquiry.'
    ' The title reflects a genre of medieval natural philosophical writing — the "secrets of'
    ' nature" genre, represented by works like pseudo-Albertus\'s <i>Secreta Mulierum</i> and'
    ' various pseudo-Aristotelian texts — that combined natural philosophical investigation'
    ' with an emphasis on hidden knowledge accessible only to the initiated. The combination'
    ' of this genre with the pseudo-Lullian alchemical tradition created a text that positioned'
    ' alchemical knowledge as the highest form of natural philosophical inquiry into the hidden'
    ' principles of material transformation.</p>'
    '<p>The manuscript tradition of the pseudo-Lullian alchemical corpus is extensive and'
    ' geographically distributed, with copies surviving in libraries across Europe.'
    ' [LINK:michela-pereira]\'s editorial and analytical work has been central to establishing'
    ' the relationships between different texts within the corpus and to understanding how the'
    ' tradition developed over the fourteenth and fifteenth centuries. Her work demonstrates'
    ' that the pseudo-Lullian tradition was not a static collection of texts but an active'
    ' intellectual tradition in which new texts were added, earlier texts were revised, and'
    ' the theoretical positions were continuously developed in response to both internal'
    ' pressures and external challenges.</p>'
)

# ── liber-xxiv-philosophorum — needs ~211 more ───────────────────────────────

LIBERXXIV_EXTRA = (
    '<p>The <i>Liber XXIV Philosophorum</i>\'s circulation among medieval Latin readers'
    ' illustrates the importance of philosophical authority for the alchemical tradition:'
    ' a text that presented the most fundamental definitions of God and the universe as'
    ' ancient wisdom from named philosophical authorities carried weight in any tradition'
    ' that organized its legitimacy through appeal to classical precedent. The specific'
    ' propositions in the text — including the famous definition of God as "an infinite'
    ' sphere whose center is everywhere and circumference nowhere" (a formulation that'
    ' [LINK:nicholas-of-cusa], [LINK:giordano-bruno], and [LINK:marsilio-ficino] all'
    ' engaged with) — provided language for talking about the relationship between'
    ' the infinite divine and finite material creation that was relevant to alchemical'
    ' philosophy\'s account of how divine creative principles were active in material'
    ' substance.</p>'
    '<p>The text\'s status as a kind of philosophical anthology — collecting the definitions'
    ' of twenty-four philosophers about the nature of God — made it a convenient resource'
    ' for writers seeking philosophical legitimation for claims about the hidden structure'
    ' of reality. Alchemical writers could invoke the <i>Liber XXIV Philosophorum</i>\'s'
    ' account of God as the infinite sphere whose activity pervades all creation as support'
    ' for the claim that alchemical practice engaged with the same divine creative principles'
    ' that the ancient philosophers had recognized. Françoise Hudry\'s critical edition'
    ' and study of the text provides the scholarly foundation for understanding its sources'
    ' and transmission.</p>'
)

# ── ms-fr-640 — needs ~314 more ───────────────────────────────────────────────

MSFR640_EXTRA = (
    '<h2>Laboratory Reconstruction and Digital Humanities</h2>'
    '<p>The Making and Knowing Project at Columbia University, directed by [LINK:pamela-smith],'
    ' has made Ms. Fr. 640 the subject of the most intensive interdisciplinary study of any'
    ' single early modern recipe manuscript. The project\'s approach — combining digital edition'
    ' of the manuscript text, scholarly annotation, and laboratory reconstruction of the'
    ' recipes — represents the application of the same "lab and library" methodology that'
    ' [LINK:lawrence-principe] has applied to alchemical texts. The practical result is'
    ' <i>Secrets of Craft and Nature in Renaissance France</i> (2020), a digital critical'
    ' edition that makes the manuscript available with scholarly commentary, historical'
    ' context, and documentation of reconstructed experiments.</p>'
    '<p>The chemical and alchemical content of the manuscript is significant: procedures for'
    ' coloring metals, preparing pigments, casting molds, making lacquers, and working with'
    ' waxes involve the same substances and operations as formal alchemical texts, embedded'
    ' within an artisanal context rather than a learned philosophical one. This embedding'
    ' demonstrates that chemical knowledge was distributed across social contexts in the'
    ' sixteenth century: what appeared in learned alchemical texts as "projection of the'
    ' Stone" appeared in workshop practice as "coloring copper to resemble gold," and the'
    ' chemical operations involved were often identical. The distinction was primarily one'
    ' of theoretical interpretation and social context rather than of chemical knowledge.</p>'
    '<p>The manuscript\'s bilingual character — French vernacular with some Latin — reflects'
    ' the social position of its author: educated enough to write in French, familiar with'
    ' some Latin technical vocabulary, working in the practical world of the workshop rather'
    ' than the academic world of learned natural philosophy. This position at the intersection'
    ' of practical craft and learned culture is typical of the social location of chemical'
    ' knowledge in early modern Europe, where the boundaries between artisan, physician,'
    ' and natural philosopher were genuinely permeable.</p>'
)

# ── mutus-liber — needs ~156 more ────────────────────────────────────────────

MUTUSLIBIR_EXTRA = (
    '<p>The <i>Mutus Liber</i>\'s combination of complete silence (no explanatory text beyond'
    ' a brief Latin motto) with detailed imagery makes it the most extreme example of the'
    ' emblematic tradition in alchemy. The fifteen plates present a complete narrative of the'
    ' alchemical work from beginning to end — the collection of dew, the manipulation of'
    ' materials, the stages of transformation, the achievement of the Stone — without any'
    ' verbal explanation of what is depicted. This extreme reticence was both a practical'
    ' security measure (the text could not be understood without the key) and a statement of'
    ' principle (the work must be understood through direct experience rather than through verbal'
    ' instruction). [LINK:lawrence-principe]\'s decoding of the <i>Mutus Liber</i> through'
    ' laboratory reconstruction — identifying the specific substances and operations depicted —'
    ' has demonstrated that the silent images encode a coherent and operationally viable account'
    ' of a specific alchemical procedure, confirming that the text was designed as a practical'
    ' guide for initiated practitioners rather than as a purely symbolic or devotional work.</p>'
)

# ── opus-minus and opus-tertium (Roger Bacon) — needs ~657 and ~639 more ──────

OPUSMINUS_EXTRA = (
    '<h2>The Companion Works to Opus Majus</h2>'
    '<p>The <i>Opus Minus</i> (Lesser Work) was written by [LINK:roger-bacon] at the same time'
    ' as the <i>Opus Majus</i> and the <i>Opus Tertium</i>, all three addressed to Pope Clement IV'
    ' in response to a papal request for a summary of Bacon\'s views on the reform of Christian'
    ' learning. The three works together constitute Bacon\'s comprehensive program for the'
    ' transformation of European education: they argue that mastery of mathematics, optics,'
    ' languages, experimental science, and moral philosophy was essential for the effective'
    ' conduct of Christian civilization, and that alchemy (as part of practical science) was'
    ' an important component of this program.</p>'
    '<p>The <i>Opus Minus</i> functions partly as a summary and partly as an extension of the'
    ' <i>Opus Majus</i>, covering some of the same ground in different forms and adding material'
    ' that the larger work had omitted. Its treatment of alchemy and the practical sciences'
    ' reflects Bacon\'s understanding of these as branches of natural philosophy with specific'
    ' practical value for Christian civilization: alchemy could prolong life, produce weapons,'
    ' and create materials of use to the Christian community. This utilitarian framing of'
    ' alchemical knowledge — alchemy valued for its practical applications rather than for'
    ' transmutation of gold for profit — distinguished Bacon\'s alchemical program from the'
    ' commercially oriented practitioners he sometimes criticized.</p>'
    '<p>[LINK:william-newman]\'s analysis of Bacon\'s concept of <i>experimentum</i> as an'
    ' important anticipation of the experimental tradition has focused particularly on the'
    ' Opus works, where Bacon articulates most clearly his understanding of what systematic'
    ' observation requires and how it differs from both textual authority and casual experience.'
    ' The specific claim that there is a science of experience that goes beyond what ordinary'
    ' sensation provides — that trained systematic observation can reveal things hidden from'
    ' casual observation — is one of the intellectual foundations for the eventual development'
    ' of experimental natural philosophy, and its articulation in Bacon\'s alchemical and'
    ' optical writings connects him to the seventeenth-century tradition in ways that'
    ' subsequent historians of science have found significant.</p>'
    '<p>The relationship between Bacon\'s three companion works and his earlier writings on'
    ' optics, mathematics, and grammar is one of systematic integration: the Opus works'
    ' represent the synthesis of Bacon\'s intellectual program at the moment when he had'
    ' the opportunity to present it to the most powerful patron available. The inclusion'
    ' of alchemy within this synthesis — alongside mathematics, optics, experimental science,'
    ' and languages — situates it firmly within the mainstream of thirteenth-century'
    ' natural philosophical inquiry rather than as a marginal or suspect pursuit.</p>'
)

OPUSTERTIUM_EXTRA = (
    '<h2>Structure and Content of the Third Work</h2>'
    '<p>The <i>Opus Tertium</i> (Third Work) was the last of the three companion pieces'
    ' Bacon sent to Pope Clement IV in 1267, addressed to the same pope and serving as'
    ' both an introduction to and a supplement of the <i>Opus Majus</i>. It contains'
    ' Bacon\'s autobiographical account of how he came to his views, a defense of his'
    ' method against critics, and discussions of mathematics, optics, and the practical'
    ' sciences including alchemy.</p>'
    '<p>The <i>Opus Tertium</i>\'s discussion of alchemy is important because it includes'
    ' Bacon\'s most explicit statement of his view that alchemy is a legitimate science:'
    ' not merely the manipulation of appearances but a genuine investigation of natural'
    ' processes. His argument that the production of artificial gold by alchemy would be'
    ' "better" than natural gold — because art, working with complete knowledge of natural'
    ' processes, can perfect what nature produces imperfectly — represents the most ambitious'
    ' formulation of the claim that art can complete nature that was available in thirteenth-century'
    ' Latin philosophy. This claim, which Bacon grounded in his understanding of the relationship'
    ' between natural philosophy and practical art, became one of the foundational theoretical'
    ' justifications for alchemical practice in the subsequent medieval and early modern tradition.</p>'
    '<p>The autobiographical dimension of the <i>Opus Tertium</i> — Bacon\'s description of'
    ' his long years of work, his resistance from his superiors in the Franciscan order, and'
    ' his eventual opportunity to communicate his program to the pope — provides a personal'
    ' narrative that complements the philosophical content of the work. This narrative situates'
    ' Bacon\'s intellectual program within the institutional constraints of his Franciscan'
    ' context: he was a member of an order that had not always been supportive of the kind of'
    ' natural philosophical inquiry he was pursuing, and his appeal to papal authority was'
    ' both a request for patronage and a defense of the legitimacy of his program against'
    ' internal critics. The intersection of intellectual ambition, institutional constraint,'
    ' and patronage negotiation in Bacon\'s situation anticipates the conditions under which'
    ' many subsequent alchemical practitioners would work.</p>'
    '<p>[LINK:william-newman]\'s analysis of how Bacon\'s Opus works were read by early modern'
    ' practitioners — particularly his demonstration that Newton and Boyle engaged with texts'
    ' in the Baconian tradition — establishes the long-term significance of Bacon\'s alchemical'
    ' program for the history of chymistry. The specific transmission of Bacon\'s ideas through'
    ' the pseudo-Baconian corpus and through citations in later texts is one of the important'
    ' genealogies of the medieval-to-early-modern alchemical tradition.</p>'
)

# ── picatrix — needs ~278 more ────────────────────────────────────────────────

PICATRIX_EXTRA = (
    '<h2>Practical Magic and Chemical Knowledge</h2>'
    '<p>The <i>Picatrix</i>\'s treatment of materia magica — the specific substances used in'
    ' magical operations and the principles governing their selection — is closely related'
    ' to the practical chemistry of the period. The text specifies what plants, stones, metals,'
    ' and animal parts should be used for specific magical operations, identifying them by their'
    ' elemental qualities, their planetary affinities, and their specific powers. This system'
    ' of natural properties and their applications is continuous with the natural philosophy'
    ' that alchemical practitioners also drew on: the same theory of qualities, correspondences,'
    ' and planetary influence that governed magical operations also governed alchemical practice.'
    ' The <i>Picatrix</i>\'s enormous pharmaco-magical repertoire thus overlapped substantially'
    ' with the stock of knowledge that alchemical practitioners used.</p>'
    '<p>[LINK:brian-copenhaver]\'s work on the <i>Picatrix</i> has contributed substantially'
    ' to scholarly understanding of how the text functioned within the broader context of'
    ' Renaissance natural magic. His analysis of the philosophical framework underlying the'
    ' specific magical operations — the account of how stellar influences were channeled'
    ' through material substances — connects the <i>Picatrix</i>\'s practical magic to the'
    ' theoretical tradition of natural magic that [LINK:marsilio-ficino] would later develop'
    ' in his <i>De Vita</i>. The chain from Arabic astral magic through the <i>Picatrix</i>'
    ' to Ficino\'s Florentine Neoplatonism is one of the important intellectual genealogies'
    ' of Renaissance learned magic, and its connection to alchemical theory through the shared'
    ' framework of planetary correspondences makes it relevant to the history of alchemy.</p>'
)

# ── pictorial-keys-to-the-tarot (SCHOLARSHIP) — needs ~296 more ──────────────

TAROT_EXTRA = (
    '<h2>Scholarship on Esoteric Symbolism</h2>'
    '<p>[LINK:wouter-hanegraaff]\'s framework for Western esotericism as a field provides'
    ' the theoretical context for situating scholarship on tarot symbolism within the'
    ' broader history of esoteric traditions. The tarot\'s alchemical associations — which'
    ' are visible in specific trumps including the Star (linked to distillation), the Moon'
    ' (lunar mercury), the Sun (solar gold), and the World (completion of the Great Work)'
    ' in some interpretive traditions — are part of the broader question of how alchemical'
    ' symbolism was distributed across different cultural media in the late medieval and'
    ' early modern periods. The scholarly challenge is to distinguish the historical alchemical'
    ' symbolism that may have informed the design of specific cards from the retrospective'
    ' alchemical interpretations of later occultist commentators who projected their own'
    ' frameworks onto earlier imagery.</p>'
    '<p>The <i>Pictorial Key to the Tarot</i> by Arthur Edward Waite (1911) represents the'
    ' tradition of early twentieth-century occultist scholarship that treated the tarot as'
    ' an ancient repository of esoteric wisdom. Waite was a member of the Hermetic Order of'
    ' the Golden Dawn, the most influential British occultist organization of the late'
    ' nineteenth and early twentieth centuries, which explicitly drew on alchemical, Kabbalistic,'
    ' and Hermetic traditions. His interpretation of the tarot within this framework positioned'
    ' it as encoding the same symbolic vocabulary as alchemy — purification, transformation,'
    ' the union of opposites, the achievement of the Philosophical Gold — but in an earlier'
    ' and more universal form. Scholarly assessment of this claim requires distinguishing'
    ' between the actual historical development of the tarot (as a playing card game, not'
    ' an esoteric system, in its fifteenth-century origins) and the later occultist elaboration'
    ' of esoteric tarot interpretation.</p>'
)

# ── secretum-secretorum — needs ~593 more ────────────────────────────────────

SECRETUM_EXTRA = (
    '<h2>The Encyclopedia of Practical Wisdom and Its Alchemical Content</h2>'
    '<p>The <i>Secretum Secretorum</i> (Secret of Secrets) is one of the most widely read'
    ' texts of the medieval period, translated into at least twenty-six languages and surviving'
    ' in hundreds of manuscripts. The text presents itself as a letter from Aristotle to'
    ' Alexander the Great, containing advice on statecraft, health, physiognomy, astrology,'
    ' and natural philosophy. Its alchemical content is not the primary focus of the text but'
    ' appears within the broader framework of natural philosophical knowledge that the text'
    ' claimed to transmit: minerals and their properties, the effects of celestial influences'
    ' on terrestrial substances, and the practical arts that depended on natural philosophical'
    ' understanding.</p>'
    '<p>The Arabic original of the <i>Secretum Secretorum</i> (known as <i>Kitab Sirr al-Asrar</i>)'
    ' was composed or compiled in the tenth century and drew on a complex tradition of'
    ' Arabic encyclopedic wisdom that combined Greek philosophical material (attributed to'
    ' Aristotle to give it authority) with Arabic additions. The attribution to Aristotle'
    ' was a characteristic strategy of medieval Arabic and Latin encyclopedic texts, paralleling'
    ' the attribution of alchemical texts to Hermes Trismegistus, Democritus, and other'
    ' ancient authorities. The Aristotelian attribution gave the text enormous authority'
    ' in both the Islamic world and, through Latin translation, in medieval Europe.</p>'
    '<p>The Latin translation by Philip of Tripoli (c. 1230) made the text available to'
    ' European readers at roughly the same time as the major Aristotelian natural philosophical'
    ' translations were arriving. [LINK:roger-bacon] wrote a commentary on the <i>Secretum'
    ' Secretorum</i> that expanded its natural philosophical content and connected it to his'
    ' own program of experimental science. This commentary is significant for the history of'
    ' alchemy because it demonstrates Bacon\'s engagement with a text that combined practical'
    ' natural knowledge (including alchemical procedures) with the authority of the most'
    ' prestigious ancient philosopher, and because it illustrates how Bacon sought to'
    ' integrate different streams of practical and theoretical knowledge into a unified'
    ' natural philosophical program.</p>'
    '<p>The <i>Secretum Secretorum</i>\'s treatment of health, astrology, and the properties'
    ' of substances reflects the same framework of elemental qualities and planetary'
    ' influences that organized alchemical theory. The physician-philosopher who understood'
    ' how to manipulate these influences could maintain health, prolong life, and produce'
    ' powerful effects in the material world — goals that were continuous with those of'
    ' alchemical iatrochemistry even when expressed in a different generic form.</p>'
)

# ── splendor-solis — needs ~157 more ─────────────────────────────────────────

SPLENDOR_EXTRA = (
    '<p>The specific imagery of the <i>Splendor Solis</i> has been subjected to the kind of'
    ' systematic iconographic analysis that [LINK:lawrence-principe]\'s laboratory replication'
    ' approach provides for operational content: Adam McLean, Hereward Tilton, and other scholars'
    ' have analyzed the visual program of the plates in relation to the alchemical textual'
    ' tradition and have proposed specific identifications of the substances and operations'
    ' depicted. The combination of scholarly iconographic analysis with laboratory work'
    ' represents the most complete approach to understanding what the <i>Splendor Solis</i>'
    ' actually meant to its intended audience — practitioners with specific laboratory'
    ' knowledge who could read the images as instructions rather than purely as symbolic'
    ' decoration. Hereward Tilton\'s scholarly study of the text provides the most'
    ' comprehensive analysis of its intellectual and laboratory context.</p>'
)

# ── symbola-aureae-mensae — needs ~570 more ──────────────────────────────────

SYMBOLA_EXTRA = (
    '<h2>Structure and Alchemical Historiography</h2>'
    '<p>Michael Maier\'s <i>Symbola Aureae Mensae Duodecim Nationum</i> (Symbols of the'
    ' Golden Table of Twelve Nations, 1617) was one of several works he published in rapid'
    ' succession in the years around the Rosicrucian manifestos, contributing to the'
    ' extraordinary productivity of the Rosicrucian cultural moment. The text presents'
    ' twelve famous alchemists — one from each of twelve nations — who gather at a golden'
    ' table to debate alchemical philosophy and authenticate the tradition through their'
    ' collective testimony. The twelve figures include [LINK:hermes-trismegistus] (Egypt),'
    ' [LINK:roger-bacon] (England), [LINK:george-ripley] (also England), Albertus Magnus'
    ' (Germany), Raymond Lull (Spain), and others.</p>'
    '<p>This fictional symposium structure allowed Maier to survey the entire history of'
    ' the alchemical tradition, presenting it as a continuous international enterprise'
    ' with deep historical roots and distinguished participants from all civilized nations.'
    ' The construction of this tradition as international and continuous served both a'
    ' polemical and a legitimating function: it defended alchemy against critics who called'
    ' it a modern fraud by demonstrating that it had ancient and respected advocates across'
    ' the entire known world, and it reinforced the claim that the Rosicrucian movement'
    ' was the current expression of a tradition with unbroken roots in ancient wisdom.</p>'
    '<p>Maier\'s other major works from the same period — <i>Atalanta Fugiens</i> (1617),'
    ' <i>Viatorium</i> (1618), <i>Arcana Arcanissima</i> (1614) — collectively represent'
    ' the most ambitious program of alchemical emblem-book production in the early'
    ' seventeenth century. His combination of musical composition (the <i>Atalanta Fugiens</i>'
    ' canons), emblematic imagery (the fifty emblems with verses and prose discussions),'
    ' and learned text demonstrates the cultural ambition of early seventeenth-century'
    ' courtly alchemy: not merely a practical laboratory tradition but a learned culture'
    ' with connections to music, philosophy, literature, and visual art.</p>'
    '<p>The scholarly analysis of Maier\'s work has been developed by H.M.E. De Jong, Hereward'
    ' Tilton, and Karin Figala, who have examined his sources, his chemical knowledge, his'
    ' relationship to the Rosicrucian movement, and the specific content of his emblematic'
    ' program. Maier was a physician at the court of Rudolf II before his later work in'
    ' Germany and England, connecting him to the same central European court alchemical'
    ' culture that produced [LINK:michael-sendivogius] and that attracted practitioners from'
    ' across Europe under the patronage of Rudolf\'s interest in natural philosophy and the arts.'
    ' His <i>Symbola</i> can be read as an attempt to create an international community of'
    ' alchemical learning at a moment when the political and religious crises of the early'
    ' seventeenth century were threatening the courtly culture on which alchemical patronage had'
    ' depended.</p>'
)

# ── ars-combinatoria (SCHOLARSHIP) — needs ~351 more ─────────────────────────

ARSCOMB_EXTRA = (
    '<h2>Lullian Combinatorics and Alchemical Epistemology</h2>'
    '<p>The relationship between Lull\'s combinatorial method and alchemy is paradoxical:'
    ' the historical Lull explicitly condemned alchemy, yet the pseudo-Lullian alchemical'
    ' corpus is one of the largest bodies of attributed texts in the medieval tradition.'
    ' Understanding this paradox requires understanding what made the Lullian method'
    ' attractive to alchemical writers who adopted it despite (or perhaps because of) the'
    ' authentic Lull\'s rejection of their practice. The <i>Ars Magna</i>\'s claim to provide'
    ' a universal method for generating true propositions in any domain was attractive to'
    ' alchemical writers who wanted to present their practice as systematic and philosophically'
    ' rigorous rather than merely empirical or traditional.</p>'
    '<p>The combinatorial structure of the <i>Ars Magna</i> — its use of rotating wheels'
    ' and geometric figures to generate all possible combinations of a set of fundamental'
    ' concepts — had a structural parallel in the alchemical tradition\'s use of the four'
    ' elements, the seven metals, and the planetary-metallic correspondences as a combinatorial'
    ' system from which the properties of any substance could in principle be derived. Both'
    ' systems claimed universality: Lull\'s Ars could generate all true propositions; the'
    ' alchemical system could in principle account for all material substances and their'
    ' transformations. The adoption of Lullian combinatorics by pseudo-Lullian alchemical'
    ' writers thus represented the most ambitious attempt to give alchemy the systematic'
    ' demonstrative character of a true science in the Aristotelian sense.</p>'
    '<p>[LINK:michela-pereira]\'s work on the pseudo-Lullian alchemical corpus provides the'
    ' scholarly foundation for understanding how the Lullian method was adapted for alchemical'
    ' purposes. Her analysis demonstrates that the pseudo-Lullian alchemists were not simply'
    ' exploiting Lull\'s name for its authority but were genuinely engaged with the intellectual'
    ' resources of the Lullian tradition, adapting its combinatorial logic to the specific'
    ' requirements of alchemical theory and practice.</p>'
)

def load_all():
    conn = sqlite3.connect(DB)

    for slug, extra in [
        ('alchemia', ALCHEMIA_EXTRA),
        ('amphitheatre-of-eternal-wisdom', AMPHITHEATRE_EXTRA),
        ('book-of-lambspring', LAMBSPRING_EXTRA),
        ('book-of-pictures', BOOKPICTURES_EXTRA),
        ('chemical-wedding-of-christian-rosencreutz', CHEMWEDDING_EXTRA),
        ('chymisches-cabinett', CHYMCABINETT_EXTRA),
        ('de-chemia', DECHEMIA_EXTRA),
        ('de-multiplicitione-specierum', DEMULT_EXTRA),
        ('de-sex-rerum-principiis', DESEX_EXTRA),
        ('de-speculis-comburentibus', SPECULA_EXTRA),
        ('kitab-al-asrar', KITABASRAR_EXTRA),
        ('kitab-al-hasib', KITABHASIB_EXTRA),
        ('libellus-de-alchimia', LIBELLUS_EXTRA),
        ('liber-de-secretis-naturae', LIBERSECRETS_EXTRA),
        ('liber-xxiv-philosophorum', LIBERXXIV_EXTRA),
        ('ms-fr-640', MSFR640_EXTRA),
        ('mutus-liber', MUTUSLIBIR_EXTRA),
        ('opus-minus', OPUSMINUS_EXTRA),
        ('opus-tertium', OPUSTERTIUM_EXTRA),
        ('picatrix', PICATRIX_EXTRA),
        ('pictorial-keys-to-the-tarot', TAROT_EXTRA),
        ('secretum-secretorum', SECRETUM_EXTRA),
        ('splendor-solis', SPLENDOR_EXTRA),
        ('symbola-aureae-mensae', SYMBOLA_EXTRA),
        ('ars-combinatoria', ARSCOMB_EXTRA),
    ]:
        app(conn, slug, extra)

    conn.commit()
    conn.close()
    print('\n=== Done ===')

if __name__ == '__main__':
    load_all()
