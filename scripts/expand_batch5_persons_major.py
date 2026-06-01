#!/usr/bin/env python3
"""expand_batch5_persons_major.py — Expand remaining major person bios to minimum 1200 words."""
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

# ── Quick top-ups for items just below 1200 ──────────────────────────────────

ALBERTUS_EXTRA = (
    '<p>Albertus Magnus served as Provincial of the Dominican Order for Germany (1254–1257) and briefly as'
    ' Bishop of Regensburg (1260–1262), positions he relinquished to return to teaching and writing. His'
    ' institutional authority lent credibility to natural philosophical inquiry within the Dominican order'
    ' and within Latin Christendom more broadly. His reputation as a practical investigator of natural'
    ' phenomena was exceptional for his era: contemporaries called him "the Great" and attributed to him'
    ' knowledge that sometimes shaded into legend. The texts attributed to him thus carried enormous'
    ' prestige, which is precisely why the debate over whether he actually wrote the alchemical works'
    ' attributed to him matters: if he did, Dominican scholastic authority endorsed practical alchemy; if'
    ' he did not, the texts are pseudepigraphal compositions designed to borrow that authority.</p>'
)

AVICENNA_EXTRA = (
    '<p>The influence of Avicenna on Latin European natural philosophy extended far beyond alchemy and'
    ' medicine. His <i>Kitab al-Shifa</i> (Book of Healing) was translated in parts and became a'
    ' standard university text in natural philosophy alongside Aristotle. His psychology, his theory of'
    ' the soul, and his commentary on Aristotelian metaphysics shaped Latin scholastic thought from the'
    ' twelfth century forward. This means that when Latin alchemical writers invoked Avicenna, they were'
    ' not citing a marginal authority but one of the most widely read and argued-about philosophers in'
    ' European academic culture. The <i>Sciant artifices</i> passage thus entered a tradition already'
    ' primed to take its author seriously.</p>'
)

# ── Marsilio Ficino ───────────────────────────────────────────────────────────

FICINO_EXTRA = (
    '<h2>Alchemy, Natural Magic, and the Prisca Theologia</h2>'
    '<p>Ficino\'s relationship to alchemy was indirect but structurally important. His translation of the'
    ' <i>Corpus Hermeticum</i> in 1463 — which he interrupted his work on Plato to complete, at Cosimo de\'Medici\'s'
    ' urgent request — established the Hermetic texts as authoritative ancient wisdom for Renaissance'
    ' European readers. The <i>Corpus Hermeticum</i> contains accounts of cosmological creation, the'
    ' descent of the soul, and the purification of matter that alchemical writers from [LINK:marsilio-ficino]\'s'
    ' era onward would read as philosophical confirmation of transmutational practice. Ficino did not simply'
    ' translate these texts: he interpreted them within his Neoplatonic framework and assigned them an'
    ' antiquity — predating Plato, descending from the "first Mercury" — that subsequent scholarship'
    ' has comprehensively revised but that was accepted without serious challenge until Isaac Casaubon\'s'
    ' dating work in 1614.</p>'
    '<p>The concept of <i>prisca theologia</i> — a primordial unified theology handed down from Hermes'
    ' Trismegistus through Orpheus, Pythagoras, and Plato — provided the philosophical legitimacy for'
    ' treating the Hermetic corpus as ancient wisdom. Alchemical writers regularly situated their practice'
    ' within this lineage: if Hermes Trismegistus had transmitted both the <i>Tabula Smaragdina</i> and'
    ' the Hermetic dialogues, then alchemy was part of the most ancient wisdom tradition available. Ficino\'s'
    ' Florentine translations made this claim available in polished Latin to the educated European public'
    ' rather than only to specialists with access to manuscript copies.</p>'
    '<p>Ficino\'s <i>De vita libri tres</i> (Three Books on Life, 1489) is the text most directly relevant'
    ' to alchemical and natural magical practice. The third book, <i>De vita coelitus comparanda</i> (On'
    ' Obtaining Life from the Heavens), develops a systematic account of how stellar and planetary'
    ' influences can be captured in material objects — stones, metals, plants, incenses, images — to'
    ' produce therapeutic and protective effects. This celestial magic drew on the same doctrine of'
    ' sympathies and correspondences between macrocosm and microcosm that structured alchemical'
    ' understanding of metallic generation under planetary influence. The metals of alchemy — gold under'
    ' the Sun, silver under the Moon, iron under Mars, copper under Venus, quicksilver under Mercury,'
    ' tin under Jupiter, lead under Saturn — were not ornamental symbolism but an explanatory framework'
    ' grounded in the same natural philosophy Ficino was articulating.</p>'
    '<p>The Florentine context of Ficino\'s work is important for understanding its reception. Cosimo and'
    ' later Lorenzo de\' Medici\'s patronage of the Platonic Academy created an environment in which'
    ' philosophical inquiry, literary production, and civic life were intertwined. [LINK:pico-della-mirandola],'
    ' fifteen years younger than Ficino, absorbed the Hermetic and Neoplatonic synthesis and pushed it toward'
    ' the Kabbalah and an even more ambitious program of prisca theologia. The intersection of Ficinian'
    ' Neoplatonism, Hermetic texts, and Kabbalah produced the "Christian Kabbalah" synthesis that'
    ' [LINK:henry-cornelius-agrippa] would systematize in <i>De Occulta Philosophia</i>. The line from'
    ' Ficino\'s translations to Agrippa\'s synthesis is one of the most important intellectual genealogies'
    ' in the history of early modern learned magic and its relationship to alchemical practice.</p>'
    '<p>Frances Yates\'s <i>Giordano Bruno and the Hermetic Tradition</i> (1964) placed Ficino at the'
    ' center of a "Hermetic Tradition" that she argued was causally important for the Scientific Revolution.'
    ' Subsequent scholarship has substantially qualified this thesis. Brian Vickers, D.P. Walker, and'
    ' others established that the Hermetic tradition was more internally diverse and less uniformly'
    ' progressive than Yates\'s account suggested. Newman and Principe\'s framework distinguishes between'
    ' the philosophical Hermeticism that Ficino transmitted — which provided a legitimating framework but'
    ' was not itself a program of laboratory research — and the operational chymistry that engaged with'
    ' the laboratory through direct experiment. Ficino\'s significance for the history of alchemy is'
    ' therefore primarily as an intellectual context-setter rather than as a practitioner: his translations'
    ' and syntheses made Hermetic philosophical legitimation available to practitioners who were already'
    ' pursuing laboratory-grounded research through quite different methods.</p>'
)

# ── George Ripley ─────────────────────────────────────────────────────────────

RIPLEY_EXTRA = (
    '<h2>The Twelve Gates and English Alchemical Tradition</h2>'
    '<p>Ripley\'s <i>Compound of Alchymy</i> (1471) structures the alchemical process through twelve'
    ' sequential operations, each named as a "gate": calcination, dissolution, separation, conjunction,'
    ' putrefaction, congelation, cibation, sublimation, fermentation, exaltation, multiplication, and'
    ' projection. This systematic framework — presenting alchemy as a sequence of distinct, learnable'
    ' operations — became highly influential in English alchemical tradition. The text circulated'
    ' in manuscript before its first printed edition and was reprinted multiple times in the sixteenth'
    ' and seventeenth centuries, appearing in Elias Ashmole\'s <i>Theatrum Chemicum Britannicum</i>'
    ' (1652), the major compilation of English alchemical verse.</p>'
    '<p>Lawrence Principe\'s laboratory replication program has engaged with Ripley\'s procedures.'
    ' The "Ripley Scrolls" — a series of large illustrated scrolls combining pictorial imagery with'
    ' verse instructions, attributed to or based on Ripley\'s tradition — have been analyzed for their'
    ' operational content. Principe and others have argued that the symbolic imagery (figures of dragons,'
    ' pelicans, kings, queens, figures undergoing various transformations) encodes specific laboratory'
    ' procedures involving mercury, sulfur, antimony, and mineral acids. The scrolls were luxury objects'
    ' produced for wealthy patrons and preserved in multiple versions, suggesting that the combination'
    ' of expensive illustration and encoded chemical instruction was commercially and culturally viable'
    ' in late-medieval and early modern England.</p>'
    '<p>Ripley\'s relationship to continental alchemy is significant. The <i>Compound</i> shows familiarity'
    ' with [LINK:pseudo-geber]\'s sulphur-mercury theory and with the Lullian alchemical tradition, suggesting'
    ' that English alchemy in the fifteenth century was well-connected with continental developments.'
    ' His Latin works, including <i>Medulla Alchimiae</i> (Marrow of Alchemy) and <i>Liber Duodecim'
    ' Portarum</i> (Book of Twelve Gates), circulated on the continent as well as in England. The'
    ' prestige of the Ripley attribution meant that later texts, including the scrolls, were often'
    ' associated with his name regardless of their actual authorship — the same dynamics of pseudonymity'
    ' and attributed authority that Newman identifies in the Starkey/Philalethes case operated in the'
    ' Ripley tradition as well.</p>'
    '<p>Ripley\'s intellectual biography connects alchemy to English ecclesiastical culture and continental'
    ' learning. His travels in Italy and possible residence in Rome indicate access to Italian humanist'
    ' circles; his dedication of the <i>Compound</i> to Edward IV signals royal-adjacent patronage'
    ' ambitions that would become standard for English alchemical practitioners into the Stuart period.'
    ' [LINK:elias-ashmole]\'s later editorial championing of Ripley\'s verse in <i>Theatrum Chemicum'
    ' Britannicum</i> placed him at the head of a national alchemical tradition at precisely the moment'
    ' when the new experimental philosophy was establishing itself at the Royal Society — a juxtaposition'
    ' that Ashmole\'s editorial choices seem designed to negotiate.</p>'
    '<p>Stanton Linden\'s study of alchemical literature in England and Lyndy Abraham\'s dictionary of'
    ' alchemical imagery provide scholarly frameworks for situating Ripley within English literary'
    ' history. Jennifer Rampling\'s recent scholarship on English alchemy from Ripley through Newton'
    ' has substantially enriched the picture, demonstrating that the English alchemical tradition was'
    ' more continuous and coherent than earlier accounts suggested and connecting the experimental'
    ' culture of Restoration chymistry to the verse tradition of the fifteenth century through'
    ' transmission routes that can now be partially traced.</p>'
)

# ── Nicholas Flamel ───────────────────────────────────────────────────────────

FLAMEL_EXTRA = (
    '<h2>The Legend and Its Making</h2>'
    '<p>The core claim of the Flamel legend — that a fourteenth-century Parisian scribe decoded an'
    ' ancient alchemical manuscript, the "Book of Abraham the Jew," with assistance from a Spanish'
    ' rabbi, and thereby achieved both the Philosophers\' Stone and the projection of gold — rests'
    ' entirely on a text that was not published until 1612: the <i>Livre des figures hiéroglyphiques</i>'
    ' (Book of Hieroglyphic Figures), attributed to Flamel and purporting to describe the decorative'
    ' program of a charity archway he funded at the cemetery of the Innocents in Paris. The archway itself'
    ' was real; the attribution of the text to Flamel is almost certainly false; and no evidence that'
    ' Flamel practiced alchemy appears in the historical documents that attest his existence as a'
    ' prosperous Parisian scribe, property owner, and charitable donor.</p>'
    '<p>The scholarly demolition of the Flamel legend is associated particularly with the work of'
    ' Didier Kahn, whose research on French alchemy establishes that the "Flamel" texts are'
    ' seventeenth-century compositions attaching a legendary practitioner\'s name to alchemical'
    ' doctrines current at the time of composition. The actual Nicholas Flamel (d. 1418) appears in'
    ' Parisian notarial records as a book merchant and scribe who accumulated substantial property'
    ' over a long career — wealth consistent with successful commerce and careful financial management'
    ' rather than with any extraordinary transmutational event. His charitable bequests (hospitals,'
    ' churches, the cemetery archway) were significant but not inexplicable for a prosperous Parisian'
    ' bourgeois of the period.</p>'
    '<p>The 1612 publication of the <i>Figures hiéroglyphiques</i> launched the Flamel legend into'
    ' European alchemical culture at precisely the moment of maximum enthusiasm for Paracelsian and'
    ' Rosicrucian alchemy. [LINK:isaac-newton] copied passages from Flamel texts into his alchemical'
    ' notebooks, treating them as potentially genuine transmissions of practical knowledge. [LINK:elias-ashmole]'
    ' collected Flamel-attributed texts. The legend\'s longevity reflects the structure of alchemical'
    ' authority: claims of achieved transmutation, attributed to named figures who could be'
    ' independently documented as having lived, carried persuasive force in a tradition organized'
    ' around master-pupil transmission of secret knowledge.</p>'
    '<p>The Flamel case is instructive for the historiographical methodology Newman and Principe advocate.'
    ' The legend demonstrates how pseudepigraphal compositions created false genealogies of alchemical'
    ' achievement, and how these false genealogies shaped the reading and practice of serious'
    ' practitioners including Newton. Untangling the real history from the legendary accretion requires'
    ' exactly the archival and manuscript-critical methods that Newman applied to the Starkey/Philalethes'
    ' identification and that Principe applied to the Boyle manuscripts — the same toolkit, applied'
    ' to a case where the conclusion is debunking rather than rehabilitation. The modern popularity'
    ' of Flamel in fantasy literature and occult culture (he appears in J.K. Rowling\'s <i>Harry'
    ' Potter and the Philosopher\'s Stone</i> and in numerous subsequent works) represents the'
    ' continuation of the legendary tradition by other means, now thoroughly detached from any claim'
    ' to historical accuracy.</p>'
)

# ── Hildegard of Bingen ───────────────────────────────────────────────────────

HILDEGARD_EXTRA = (
    '<h2>Natural Philosophy and the Hildegardian Tradition</h2>'
    '<p>Hildegard\'s medical and natural philosophical writings stand apart from the mainstream of'
    ' twelfth-century Latin learning in their explicit grounding in visionary experience rather than'
    ' scholastic commentary on authoritative texts. Where [LINK:albertus-magnus] and his contemporaries'
    ' worked within Aristotelian frameworks imported through Arabic and earlier Latin translation,'
    ' Hildegard developed her understanding of the natural world through a different authority:'
    ' direct divine illumination, which she described as the "living light" revealing the hidden'
    ' correspondences of creation. This alternative epistemological claim gave her work both a'
    ' distinctive character and a particular kind of authority: not the authority of Aristotle or'
    ' Avicenna, but the authority of prophetic vision grounded in the institutional context of'
    ' the Benedictine order and confirmed by Bernard of Clairvaux and, eventually, Pope Eugenius III.</p>'
    '<p>The <i>Physica</i> — also known as the <i>Liber Subtilitatum</i> (Book of Subtleties) —'
    ' covers minerals, plants, animals, and the elements. Its sections on metals and stones describe'
    ' their curative properties, their spiritual correspondences, and their generation within the earth'
    ' — a topic that connects to alchemical matter theory in later medieval Latin writers even if'
    ' Hildegard herself does not engage with alchemical texts or procedures. Her four-element cosmology,'
    ' her concern with the balance of qualities (hot, cold, wet, dry) as the foundation of health, and'
    ' her interest in the hidden powers of created things (<i>viriditas</i>, the greening power of'
    ' living nature) overlap with alchemical natural philosophy without being derived from it.</p>'
    '<p>The <i>Causae et Curae</i> addresses the physiology and pathology of the human body within a'
    ' framework that combines Galenic humoral medicine with Hildegard\'s distinctive cosmological vision.'
    ' Her account of sexuality, conception, and the formation of the fetus draws on humoral physiology'
    ' but also on a vision of how the elements and the stars contribute to human temperament. The gender'
    ' categories in her physiology — her account of different humoral constitutions in men and women —'
    ' have attracted attention from historians of medicine and gender interested in medieval understandings'
    ' of bodily difference.</p>'
    '<p>Within the historiography of alchemy and learned magic, Hildegard matters primarily as evidence'
    ' for the breadth of natural philosophical inquiry in the twelfth century before the full impact of'
    ' Aristotelian natural philosophy arrived through translation. She represents a different current'
    ' of medieval learning — one that was not displaced but rather supplemented by the scholastic'
    ' tradition, and that retained influence in practical contexts (herbalism, medicine, music, theology)'
    ' that scholastic philosophy addressed less directly. Barbara Newman\'s scholarship (no relation to'
    ' William Newman) on Hildegard\'s visionary theology and Sabina Flanagan\'s biography provide the'
    ' scholarly foundations for situating her within the history of medieval learning. Her <i>Physica</i>'
    ' and <i>Causae et Curae</i> have been edited critically and translated, making her natural'
    ' philosophical work accessible for comparative study with contemporaneous alchemical and medical'
    ' traditions.</p>'
)

# ── William Newman ────────────────────────────────────────────────────────────

NEWMAN_EXTRA = (
    '<h2>Methodology and Impact</h2>'
    '<p>Newman\'s methodology combines conventional historical scholarship — archival research, manuscript'
    ' analysis, the recovery of manuscript transmission networks — with a distinctive analytical framework'
    ' derived from careful reading of primary sources on their own terms. His insistence on the'
    ' "chymistry" label, shared with [LINK:lawrence-principe], is partly terminological and partly'
    ' substantive: it signals a refusal to import retrospective categories that separate "real chemistry"'
    ' from "mere alchemy" into a period in which practitioners themselves made no such distinction.'
    ' This methodological commitment has been productive precisely because it forces the analyst to'
    ' ask what the practitioners were actually trying to do and what evidence they were actually'
    ' working with, rather than filtering the record through anachronistic categories.</p>'
    '<p>The Chymistry of Isaac Newton project (chymistry.indiana.edu) represents Newman\'s most significant'
    ' institutional contribution to the field: a digital edition of Newton\'s alchemical manuscripts'
    ' that makes approximately one million words of previously difficult-to-access material freely'
    ' available in transcription and facsimile. The project involved scholarly collaboration with'
    ' multiple investigators and technical development of editorial tools. Its effect on Newton'
    ' scholarship has been substantial: arguments about Newton\'s alchemy that previously depended'
    ' on partial quotation from manuscripts accessible only to specialists can now be evaluated'
    ' by any scholar who can read early modern English and Latin.</p>'
    '<p>Newman\'s broader contribution to the historiography of early modern science lies in his'
    ' sustained argument that the boundary between alchemy and chemistry was constructed retrospectively'
    ' — particularly by eighteenth-century chemists who needed to distinguish their new scientific'
    ' discipline from its disreputable past — and that the construction of this boundary has'
    ' distorted historical understanding of how early modern natural philosophy actually worked.'
    ' His collaborative work with [LINK:lawrence-principe], including the jointly edited <i>Alchemy'
    ' Tried in the Fire</i> (2002) and the theoretical article "Alchemy vs. Chemistry: The Etymological'
    ' Origins of a Historiographic Mistake" (1998), has been widely cited across the history of'
    ' science and has influenced scholars working on periods and topics well beyond early modern alchemy.</p>'
)

# ── Lawrence Principe ─────────────────────────────────────────────────────────

PRINCIPE_EXTRA = (
    '<h2>Laboratory Replication and Historiographical Impact</h2>'
    '<p>Principe\'s laboratory replication program is distinctive within the history of science for'
    ' its method: he actually performs historical chemical procedures to understand what early modern'
    ' practitioners were doing and what they were observing. This approach has produced results not'
    ' available through text-based analysis alone. For the Ripley Scrolls and related mercury-sulfur'
    ' procedures, laboratory work demonstrated that the distinctive color sequence described in'
    ' alchemical texts — black, white, citrine, red — corresponds to observable changes in specific'
    ' sulfur-mercury-antimony preparations under controlled heating. For Starkey\'s procedures,'
    ' following the laboratory notebook to its operational conclusions revealed techniques for'
    ' preparing amalgams and specific mineral compounds that were genuinely sophisticated for their era.</p>'
    '<p>His revision of Boyle\'s historical image — from founder of modern chemistry to aspiring'
    ' adept whose experimental program was entangled with alchemical goals — has been one of the'
    ' most consequential historiographical interventions in the study of the Scientific Revolution.'
    ' Principe documented this through the Boyle Papers at the Royal Society, particularly the'
    ' coded notebooks and the correspondence with Starkey. The argument that Boyle\'s corpuscular'
    ' chemistry and his pursuit of the Philosophers\' Stone were not separable — that the same'
    ' theoretical framework motivated both — required showing that Boyle\'s private papers told'
    ' a different story than his published works, a classic problem in intellectual history that'
    ' Principe resolved through sustained archival research.</p>'
    '<p>Principe\'s broader teaching and public communication work includes <i>The Secrets of'
    ' Alchemy</i> (2013), an accessible introduction for non-specialist audiences that presents'
    ' the scholarly consensus on alchemy as a laboratory-grounded practice without endorsing'
    ' its transmutational claims. His Great Courses lecture series on the history of science'
    ' has reached audiences far beyond academic readership. Within the discipline, his influence'
    ' extends through students trained at Johns Hopkins, through collaborative publications with'
    ' [LINK:william-newman] and others, and through the example of a methodological approach'
    ' that takes laboratory evidence seriously as a source of historical understanding.</p>'
)

# ── John Dee ──────────────────────────────────────────────────────────────────

DEE_EXTRA = (
    '<h2>Natural Philosophy, Angel Magic, and Alchemy</h2>'
    '<p>Dee\'s intellectual program was organized around a vision of universal reform through mastery'
    ' of the mathematical arts — arithmetic, geometry, astronomy, music, and their applications in'
    ' navigation, cartography, optics, and the practical arts. His <i>Mathematical Preface</i> to'
    ' the first English Euclid (1570) remains one of the most important statements of the case for'
    ' mathematics as the foundation of all human knowledge, with applications ranging from surveying'
    ' to military engineering to navigation. This program was not separate from his occult interests'
    ' but integrated with them: for Dee, number was the bridge between material and spiritual'
    ' reality, and mastery of number in both its practical and its Neoplatonic dimensions was a'
    ' unified pursuit.</p>'
    '<p>The angel conversations conducted with Edward Kelley between 1582 and 1589 — documented in'
    ' Dee\'s diaries and in the transcripts he compiled — occupy the center of most popular accounts'
    ' of Dee but have been somewhat sidelined by historians interested in his contributions to'
    ' mathematics and navigation. The conversations were conducted through a scrying stone (a'
    ' polished obsidian mirror, now in the British Museum) and produced extensive records of'
    ' angelic speech in the "Enochian" language that Kelley claimed to receive. Historians debate'
    ' the extent to which Dee believed the conversations were genuinely angelic and the extent'
    ' to which he understood them as a performance organized by Kelley; the diary evidence is'
    ' ambiguous but suggests a complex negotiated belief rather than simple credulity.</p>'
    '<p>Dee\'s library at Mortlake — destroyed by a mob in 1583 in his absence — was one of the'
    ' largest private libraries in Elizabethan England, containing several thousand volumes including'
    ' substantial holdings in alchemy, mathematics, and natural philosophy. The loss was catastrophic'
    ' for Dee personally and symbolically: it represented the destruction of a significant intellectual'
    ' resource for English natural philosophy at the moment of its greatest development. The'
    ' relationship between Dee\'s library, his mathematical work, his contacts with continental'
    ' humanist scholars, and his alchemical and magical interests illustrates the unrealized potential'
    ' of a synthetic English natural philosophy in the late sixteenth century.</p>'
    '<p>William Sherman\'s <i>John Dee: The Politics of Reading and Writing in the English Renaissance</i>'
    ' (1995) and Deborah Harkness\'s <i>John Dee\'s Conversations with Angels</i> (1999) represent'
    ' the major modern scholarly treatments. Nicholas Clulee\'s <i>John Dee\'s Natural Philosophy'
    ' Between Science and Religion</i> (1988) provides a comprehensive analysis of his intellectual'
    ' program. The relationship between Dee\'s Monas Hieroglyphica and the alchemical tradition —'
    ' his claim that the monas symbol united all the planetary symbols through a mathematical'
    ' construction — connects his work to the emblematic tradition in alchemy and has been analyzed'
    ' in the context of Renaissance magical philosophy. Dee\'s influence on English alchemy extended'
    ' to [LINK:elias-ashmole] and through him to the Royalist alchemical culture of the mid-seventeenth'
    ' century.</p>'
)

# ── Henry Cornelius Agrippa ───────────────────────────────────────────────────

AGRIPPA_EXTRA = (
    '<h2>De Occulta Philosophia and Its Influence</h2>'
    '<p>The three-book structure of <i>De Occulta Philosophia</i> — natural magic (based on the'
    ' properties of elemental things), celestial magic (based on the influences of stars and spirits),'
    ' and ceremonial magic (based on divine names and ritual) — provided the most systematic'
    ' philosophical framework for learned magic available in print in the sixteenth century.'
    ' Natural magic in book one encompasses the doctrine of sympathies and antipathies between'
    ' substances, the hidden properties of stones, plants, and metals, and the principles governing'
    ' how these properties could be exploited for practical ends. This is the domain most directly'
    ' relevant to alchemy: the same doctrine of elemental qualities and planetary correspondences'
    ' that structured Agrippa\'s natural magic structured alchemical theories of metallic generation'
    ' and transformation.</p>'
    '<p>Agrippa\'s relationship to practical alchemy was skeptical in his published work: in'
    ' <i>De Incertitudine et Vanitate Scientiarum</i> (On the Uncertainty and Vanity of the Sciences,'
    ' 1530), he attacked virtually every form of human learning including alchemy, astrology, and'
    ' philosophy — a rhetorical exercise in radical skepticism that has been read as sincere, as'
    ' ironic, and as tactical depending on the interpreter. The tension between the systematic'
    ' validation of occult knowledge in <i>De Occulta Philosophia</i> and the global skepticism'
    ' of <i>De Vanitate</i> has occupied scholars since the sixteenth century. Charles Nauert\'s'
    ' biography and Christopher Lehrich\'s study of Agrippa\'s language and magic are the major'
    ' modern scholarly treatments.</p>'
    '<p>The influence of Agrippa\'s synthesis on subsequent alchemical and magical writing was'
    ' extensive. [LINK:john-dee]\'s <i>Monas Hieroglyphica</i> engages with the same tradition'
    ' of mathematical-magical symbolism. [LINK:heinrich-khunrath]\'s <i>Amphitheatrum Sapientiae'
    ' Aeternae</i> combines Agrippa\'s Neoplatonic-Hermetic framework with Protestant theology'
    ' and alchemical imagery. [LINK:marsilio-ficino]\'s Neoplatonism was the philosophical'
    ' foundation for the celestial magic of book two; Pico della Mirandola\'s Christian Kabbalah'
    ' informed book three. The synthesis was available to every literate European from the 1531'
    ' edition forward and shaped the vocabulary in which alchemy, magic, and natural philosophy'
    ' were discussed for the next century.</p>'
    '<p>Agrippa\'s life was marked by the institutional tensions his program created. His defense'
    ' of a woman accused of witchcraft early in his career, his service to various German, French,'
    ' and Netherlands patrons, his theological unorthodoxy, and his eventual service as imperial'
    ' historiographer to Charles V all reflect a career negotiating between intellectual ambition,'
    ' patronage dependence, and religious controversy. His experience illustrates the conditions'
    ' under which natural magic and its relationship to alchemy were pursued in early sixteenth-century'
    ' Europe: not quietly, but under continuous pressure from theological and academic authorities'
    ' who found the synthesis of Hermeticism, Kabbalah, and natural philosophy troubling.</p>'
)

# ── Hermes Trismegistus ───────────────────────────────────────────────────────

HERMES_EXTRA = (
    '<h2>The Scholarly Reassessment</h2>'
    '<p>The figure of Hermes Trismegistus is a construction of ancient religious syncretism:'
    ' the identification of the Greek messenger-god Hermes with the Egyptian god Thoth, patron of'
    ' writing and wisdom, produced a composite figure credited with the authorship of texts that'
    ' were actually written across several centuries by multiple authors working in Greek in Roman'
    ' Egypt. Garth Fowden\'s <i>The Egyptian Hermes: A Historical Approach to the Late Pagan Mind</i>'
    ' (1986) is the standard scholarly treatment of this literary tradition and its religious context.'
    ' Fowden situates the <i>Corpus Hermeticum</i> within the broader landscape of Greco-Egyptian'
    ' religious texts — Gnostic gospels, magical papyri, astrological manuals — that were produced'
    ' in the same period and by similar cultural processes of syncretism between Egyptian, Greek,'
    ' and Jewish traditions.</p>'
    '<p>Isaac Casaubon\'s <i>De Rebus Sacris et Ecclesiasticis Exercitationes</i> (1614) demonstrated'
    ' on linguistic and historical grounds that the <i>Corpus Hermeticum</i> could not be as ancient'
    ' as claimed: the Greek was post-classical, the philosophical concepts were post-Platonic, and'
    ' the historical context presupposed by the texts was Roman imperial rather than Egyptian'
    ' pharaonic. Casaubon\'s dating was a decisive intervention in the Renaissance prisca theologia'
    ' tradition, removing the Hermetic texts from their position as pre-Platonic Egyptian wisdom.'
    ' The impact was significant for the intellectual standing of Hermeticism as an authoritative'
    ' tradition, though it did not immediately end the use of Hermetic texts in alchemical and'
    ' magical contexts — texts that had been culturally and intellectually productive continued to'
    ' circulate even when their claimed historical provenance was disproved.</p>'
    '<p>Wouter Hanegraaff\'s <i>Hermetic Spirituality and the Historical Imagination</i> (2022)'
    ' represents the most recent major scholarly treatment, arguing for a distinction between the'
    ' ancient Hermetica (the texts themselves), the Renaissance reception of those texts through'
    ' [LINK:marsilio-ficino]\'s translations, and the modern occultist tradition that treats'
    ' "Hermeticism" as a living practice. Hanegraaff\'s genealogical approach traces how the'
    ' figure of Hermes Trismegistus has been constructed and reconstructed across these different'
    ' cultural contexts, each serving different intellectual and religious purposes.</p>'
)

# ── Thomas Aquinas ────────────────────────────────────────────────────────────

AQUINAS_EXTRA = (
    '<h2>Alchemy, Natural Philosophy, and the Thomist Tradition</h2>'
    '<p>The texts attributed to Thomas Aquinas in the alchemical tradition — including <i>De'
    ' Alchimia</i> and the extensive <i>Aurora Consurgens</i> — are now understood by scholars'
    ' to be pseudepigraphal. Aquinas himself wrote no alchemical treatises. The attributions'
    ' reflect the same strategy operative throughout the medieval alchemical corpus: attaching'
    ' texts to the most authoritative available philosophical name to give them intellectual'
    ' legitimacy. That strategy was applied to Aquinas because his synthesis of Aristotelian'
    ' natural philosophy with Christian theology was the most prestigious intellectual achievement'
    ' of thirteenth-century Latin learning, and because Thomist natural philosophy — with its'
    ' distinction between primary and secondary causation, its affirmation that art can imitate'
    ' and complete nature, and its account of matter and form — provided a philosophical framework'
    ' within which alchemical practice could be legitimated.</p>'
    '<p>The genuine Thomist position on alchemy is recoverable from authentic texts. In his'
    ' commentary on Aristotle\'s <i>Meteorologica</i>, Aquinas addresses the question of whether'
    ' art can produce real metals or only superficial resemblances. His position, following'
    ' Aristotle\'s account of generation and corruption, is careful: art may be able to produce'
    ' the material forms of metals if it can replicate the natural processes of metallic generation,'
    ' but it is unlikely that current alchemical practice actually achieves this. This is a'
    ' measured skepticism rather than a flat denial — which is precisely why the attribution'
    ' of alchemical texts to Aquinas was plausible to later readers who knew his work on'
    ' natural philosophy and saw him as someone who had engaged with the question.</p>'
    '<p>The <i>Aurora Consurgens</i>, attributed to Aquinas by its manuscript tradition and'
    ' analyzed by Marie-Louise von Franz in a study that treated it as an expression of'
    ' psychological integration in Jungian terms, has been reassessed by Michela Pereira'
    ' and others as a text that belongs to the Lullian pseudo-alchemical tradition of the'
    ' late thirteenth or early fourteenth century. The attribution to Aquinas in the manuscript'
    ' tradition is not historical testimony but the construction of philosophical authority for'
    ' a text that used Christian mystical and alchemical symbolism in ways that required the'
    ' support of a recognized orthodox theologian. The historiographical significance of the'
    ' Aquinas attributions is as evidence for how medieval alchemical writers understood their'
    ' relationship to scholastic philosophy: not as opponents of the academic tradition but as'
    ' participants seeking its authorization.</p>'
)

# ── Francis Bacon ─────────────────────────────────────────────────────────────

BACON_EXTRA = (
    '<h2>Alchemy, Experiment, and the Reform of Learning</h2>'
    '<p>Bacon\'s relationship to alchemy was consistently ambivalent in his published work.'
    ' In <i>The Advancement of Learning</i> (1605) and <i>De Augmentis Scientiarum</i> (1623),'
    ' he criticizes alchemists for excessive secrecy, for using figurative and equivocal language,'
    ' and for pursuing impractical and unfounded transmutational goals — while acknowledging that'
    ' alchemical practice had produced genuinely useful chemical knowledge incidentally, as a'
    ' byproduct of the pursuit of gold that the alchemists had not intended but that a properly'
    ' reformed natural philosophy should harvest and systematize. This stance — respectful of'
    ' alchemical practice, dismissive of alchemical goals — became influential in eighteenth-century'
    ' accounts of chemistry\'s relationship to its alchemical past, including [LINK:herman-boerhaave]\'s'
    ' treatment in <i>Elementa Chemiae</i>.</p>'
    '<p>Bacon\'s <i>Novum Organum</i> (1620) is primarily a work of logical methodology — a'
    ' replacement of Aristotelian syllogistic with inductive method for the investigation of'
    ' nature. Its relevance to alchemy lies in its account of what proper experimental inquiry'
    ' looks like: systematic observation, tabulation of instances, identification of forms,'
    ' and gradual ascent to axioms. This is recognizably different from both scholastic'
    ' philosophical commentary and from the laboratory practice of alchemical adepts who worked'
    ' from transmitted procedures rather than systematic inductive inquiry. Newman has analyzed'
    ' the degree to which the actual laboratory practices of seventeenth-century chymists —'
    ' particularly [LINK:george-starkey] and [LINK:robert-boyle] — conformed to Baconian ideals'
    ' versus operating through quite different experimental logics, concluding that the Baconian'
    ' framework had rhetorical influence on how practitioners described their work but was not'
    ' the actual method by which chymical knowledge was produced.</p>'
    '<p>Bacon\'s death, traditionally attributed to a chill contracted while stuffing a chicken'
    ' with snow to test theories of refrigeration, is itself a kind of legend about experimental'
    ' inquiry taken too far — the natural philosopher undone by his own methodology. Whether true'
    ' in detail or not, the story captures something of Bacon\'s intellectual culture: a man'
    ' sufficiently committed to experimental test that he would expose himself to winter'
    ' conditions to get data. His intellectual legacy — the organization of the Royal Society,'
    ' the development of collaborative research programs, the idea of a "natural history" as'
    ' foundation for theoretical philosophy — was formative for the same English chymical'
    ' tradition that produced [LINK:robert-boyle] and ultimately [LINK:isaac-newton]\'s'
    ' laboratory practice, even when the actual research methods differed substantially'
    ' from what Bacon had prescribed.</p>'
)

# ── Pico della Mirandola ──────────────────────────────────────────────────────

PICO_EXTRA = (
    '<h2>Kabbalah, Hermeticism, and the Dignity of Man</h2>'
    '<p>Pico\'s <i>Oration on the Dignity of Man</i> (c. 1486, published posthumously 1496) is the'
    ' canonical text of Renaissance humanism not because it represents the mainstream of Quattrocento'
    ' Florentine thought but because it articulates a vision — of humanity as uniquely unfixed in'
    ' the hierarchy of being, capable of ascending to the divine or descending to the bestial through'
    ' the exercise of free will — that became programmatic for humanist self-understanding. Within'
    ' the intellectual history of alchemy, the Oration is significant for what it implies about'
    ' human capacity for natural-philosophical inquiry: if humanity\'s unique dignity lies in the'
    ' ability to occupy any position in the created order, then the alchemist\'s aspiration to'
    ' complete and perfect natural processes through art participates in this distinctively human'
    ' calling.</p>'
    '<p>Pico\'s Christian Kabbalah — his argument that the Hebrew Kabbalah, properly interpreted,'
    ' confirmed the truth of Christianity and provided a deeper understanding of divine names and'
    ' their power — represented a significant extension of [LINK:marsilio-ficino]\'s Neoplatonic-Hermetic'
    ' synthesis. Where Ficino had drawn on the Greek Hermetic and Platonic traditions, Pico added'
    ' Hebrew kabbalistic texts as a third stream of prisca theologia, arguing that Moses had received'
    ' an oral tradition alongside the written Torah that encoded Neoplatonic philosophical truths.'
    ' This synthesis was taken up by [LINK:henry-cornelius-agrippa] in book three of <i>De Occulta'
    ' Philosophia</i> and became part of the standard equipment of learned magical and alchemical'
    ' writers in the sixteenth century who needed theological legitimation for operations involving'
    ' the invocation of divine names and angelic powers.</p>'
    '<p>The relationship between Pico\'s Kabbalah and alchemical practice was indirect: Pico himself'
    ' was not an alchemical practitioner, and his intellectual interests were primarily philosophical'
    ' and theological. But his validation of the Kabbalah as a legitimate source of natural and'
    ' divine knowledge, combined with the kabbalistic tradition\'s account of how divine power'
    ' was distributed through the Sephiroth into the material world, provided a framework within'
    ' which alchemical operations could be understood as manipulating the same divine-material'
    ' channels that the Kabbalah described. This connection between kabbalistic theory and'
    ' alchemical practice is visible in [LINK:heinrich-khunrath]\'s work, in the theosophy of'
    ' Jakob Böhme, and in the later development of laboratory alchemy in the tradition'
    ' that connects to [LINK:george-starkey] and [LINK:robert-boyle].</p>'
)

# ── Giordano Bruno ────────────────────────────────────────────────────────────

BRUNO_EXTRA = (
    '<h2>Hermeticism, Cosmology, and the Memory Arts</h2>'
    '<p>Bruno\'s relationship to alchemy was peripheral compared to his engagement with Hermetic'
    ' philosophy and the memory arts, but the shared intellectual context is significant. His'
    ' Hermetic Copernicism — the argument that the heliocentric cosmos confirmed the Hermetic'
    ' vision of an infinitely alive and ensouled universe, with the Sun at its center as the'
    ' visible manifestation of divine light — drew on exactly the same corpus of texts that'
    ' alchemical natural philosophy found philosophically authoritative. His cosmological writings,'
    ' particularly <i>De la Causa, Principio e Uno</i> (On Cause, Principle and One, 1584) and'
    ' <i>De l\'Infinito, Universo e Mondi</i> (On the Infinite, the Universe, and Worlds, 1584),'
    ' develop an account of the universe as an infinite animated whole that resonated with'
    ' the Paracelsian and Helmontian vision of nature as a living system in which human'
    ' practice could participate.</p>'
    '<p>Frances Yates\'s argument in <i>Giordano Bruno and the Hermetic Tradition</i> (1964)'
    ' that Bruno\'s Hermeticism was causally important for the Scientific Revolution — through'
    ' its influence on the development of heliocentrism and the experimental philosophy — has'
    ' been substantially qualified by subsequent scholarship. The main lines of critique are:'
    ' Bruno\'s Hermeticism led him toward an animated, qualitative vision of the cosmos that'
    ' is not obviously proto-scientific; the actual mechanisms of influence are hard to document;'
    ' and the figures who developed mathematical natural philosophy (Galileo, Descartes, Newton)'
    ' did not show significant Brunian influence. Brian Vickers, Stephen Pumfrey, and others'
    ' have detailed these objections. The "Yates thesis" remains historically important as a'
    ' formative intervention in the history of science, even if its substantive claims have'
    ' been largely rejected.</p>'
    '<p>Bruno\'s execution by the Roman Inquisition in 1600, after eight years of imprisonment,'
    ' made him a martyr figure for nineteenth- and twentieth-century secularist historiography:'
    ' a free-thinker burned by religious reaction for advancing scientific ideas. The scholarly'
    ' consensus now is that the charges against Bruno were primarily religious (denial of the'
    ' Trinity, denial of transubstantiation, magical practices, heretical cosmology) rather'
    ' than specifically scientific, and that his cosmological ideas were not the primary focus'
    ' of the trial. His case illustrates the difficulty of distinguishing "science" from'
    ' "religion" and "magic" in late-sixteenth-century contexts — a difficulty that is precisely'
    ' the point of the "chymistry" framework Newman and Principe have developed.</p>'
)

# ── Michael Sendivogius ───────────────────────────────────────────────────────

SENDIVOGIUS_EXTRA = (
    '<h2>The Philosophical Treatise on Niter and Its Influence</h2>'
    '<p>Sendivogius\'s <i>Novum Lumen Chymicum</i> (New Chemical Light, 1604) argued that the'
    ' "spirit of niter" — a nitrous aerial substance — was the active vital principle that nourished'
    ' both combustion and life, present in air but distinct from ordinary air. This identification'
    ' of a distinct vital-chemical component of air was an important step toward the pneumatic'
    ' chemistry that [LINK:joseph-black], Henry Cavendish, [LINK:carl-wilhelm-scheele], and'
    ' Joseph Priestley would develop in the eighteenth century. The spirit of niter concept was'
    ' taken seriously by serious natural philosophers in the seventeenth century: [LINK:robert-boyle]'
    ' engaged with it, and there are scholars who have argued that [LINK:isaac-newton]\'s concept'
    ' of the aerial niter — a universal active principle distributed through the atmosphere —'
    ' was influenced by Sendivogius.</p>'
    '<p>The circumstances of Sendivogius\'s life were dramatic even by the standards of early'
    ' modern alchemical practitioners. His relationship to the Scottish alchemist Alexander'
    ' Seton — from whom he allegedly obtained alchemical knowledge after rescuing him from'
    ' captivity in Germany — is the subject of contested historical accounts. The claim that'
    ' Sendivogius performed successful transmutations before witnesses, including the Emperor'
    ' Rudolf II in Prague, was not unusual in the alchemical culture of Rudolf\'s court, which'
    ' attracted practitioners from across Europe. Vladimír Karpenko and John Norris have provided'
    ' the scholarly analysis of Sendivogius\'s chemical contributions within this court context.</p>'
    '<p>The <i>Novum Lumen Chymicum</i> was widely translated and reprinted: into English, German,'
    ' French, and other languages, with multiple editions across the seventeenth century.'
    ' [LINK:isaac-newton] read Sendivogius and made annotations. The text circulated within the'
    ' same network of chymical literature that included [LINK:george-ripley], the Lullian texts,'
    ' and the Philalethes works of [LINK:george-starkey]. Lawrence Principe has analyzed'
    ' Sendivogius within the broader tradition of "philosophical mercury" texts — a corpus'
    ' concerned with the identification and preparation of the specific form of mercury that'
    ' served as the foundation for the alchemical process — and has identified the spirit of'
    ' niter as Sendivogius\'s distinctive contribution to this tradition.</p>'
)

# ── John of Rupescissa ────────────────────────────────────────────────────────

RUPESCISSA_EXTRA = (
    '<h2>Quintessence and the Reform of Medicine</h2>'
    '<p>John of Rupescissa\'s <i>De consideratione quintae essentiae rerum omnium</i> (c. 1351–1352)'
    ' argued that the distillation of wine produced not merely a concentrated form of wine but a'
    ' fundamentally different substance — the "fifth essence" or quintessence — that was the'
    ' celestial element that Aristotle had described as the substance of the heavens, now obtainable'
    ' in the laboratory through distillation. This quintessence, wine alcohol, was incorruptible,'
    ' preserved against putrefaction anything dissolved in it, and could be used to extract the'
    ' quintessences of medicinal plants and substances. The resulting medicines, freed from their'
    ' gross material components, were theoretically more powerful and stable than conventional'
    ' Galenic preparations.</p>'
    '<p>The historical context of Rupescissa\'s work is important. Writing from Franciscan imprisonment'
    ' and informed by apocalyptic Franciscan prophecy, he situated his pharmaceutical alchemy within'
    ' a millenarian framework: the quintessence medicines would be needed to sustain and heal humanity'
    ' during the tribulations preceding the Last Days. This combination of laboratory chemistry with'
    ' apocalyptic prophecy reflects the specific intersection of Franciscan spirituality, Joachite'
    ' eschatology, and natural philosophical inquiry that characterized certain fourteenth-century'
    ' Franciscan intellectuals.</p>'
    '<p>Barbara Obrist and DeVun Leah have studied Rupescissa within the broader context of medieval'
    ' apocalypticism and natural philosophy. Michela Pereira has analyzed the transmission of the'
    ' quintessence concept through the pseudo-Lullian tradition that rapidly appropriated it.'
    ' The concept of quintessence as purified alcohol becomes fundamental to [LINK:paracelsus]\'s'
    ' iatrochemistry — spagyrics, the extraction of arcana from medicinal substances — and thus'
    ' to the entire tradition of chemical medicine through the seventeenth century. Rupescissa\'s'
    ' contribution was less the specific medicines he proposed than the conceptual framework of'
    ' distillation as a process of purification and spiritualization that could be applied'
    ' systematically across the materia medica.</p>'
)

# ── Pamela Smith ──────────────────────────────────────────────────────────────

SMITH_EXTRA = (
    '<h2>Artisanal Knowledge and the Body of the Artisan</h2>'
    '<p>Smith\'s <i>The Body of the Artisan: Art and Experience in the Scientific Revolution</i>'
    ' (2004) develops an argument about how practical craft knowledge — the knowledge of metalworkers,'
    ' apothecaries, painters, potters, printers — contributed to the development of early modern'
    ' natural philosophy. The "body of the artisan" in her title refers both to the artisan\'s'
    ' physical body as the primary instrument of craft inquiry (skilled hands, calibrated senses,'
    ' embodied judgment) and to the corpus of practical knowledge accumulated through'
    ' generations of workshop practice. Smith\'s argument is that this knowledge was not'
    ' simply absorbed passively by natural philosophers but actively challenged them: the'
    ' recalcitrance of matter in the workshop — the way gold refused to be extracted from ore'
    ' exactly as theory predicted, the way colors shifted in the kiln in unexpected ways —'
    ' forced investigators to revise theoretical accounts of material properties.</p>'
    '<p>Her research on Ms. Fr. 640, a sixteenth-century French manuscript of workshop recipes'
    ' and craft techniques (the "Book of Secrets from the Workshop of a French Artist"), has'
    ' been developed into a major collaborative digital humanities project at Harvard and MIT:'
    ' <i>Secrets of Craft and Nature in Renaissance France</i>. The project combines scholarly'
    ' transcription, translation, and annotation with laboratory reconstruction of the'
    ' manuscript\'s recipes — the same kind of "lab and library" methodology that [LINK:lawrence-principe]'
    ' has applied to alchemical texts. The results demonstrate that the manuscript\'s recipes'
    ' are operationally coherent — they actually work — and that the author was a sophisticated'
    ' observer of material processes who had developed systematic knowledge of pigments, molds,'
    ' metalworking, and natural history through direct experimental inquiry.</p>'
    '<p>Smith\'s broader contribution to the historiography of early modern science lies in her'
    ' insistence that the boundary between "science" and "craft" — between theoretical natural'
    ' philosophy and practical workshop knowledge — was permeable and contested in the sixteenth'
    ' and seventeenth centuries in ways that standard accounts of the Scientific Revolution'
    ' have obscured. Her approach converges with [LINK:william-newman] and Principe\'s revision'
    ' of the alchemy-chemistry boundary: both arguments locate early modern natural knowledge'
    ' production in laboratory and workshop settings where theory and practice were inseparable,'
    ' and both require attending to sources (laboratory notebooks, recipe manuscripts, workshop'
    ' records) that fall outside the canonical texts of the Scientific Revolution narrative.</p>'
)

# ── Wouter Hanegraaff ─────────────────────────────────────────────────────────

HANEGRAAFF_EXTRA = (
    '<h2>Western Esotericism as an Academic Field</h2>'
    '<p>Hanegraaff\'s major theoretical contribution is his argument, developed most fully in'
    ' <i>Esotericism and the Academy: Rejected Knowledge in Western Culture</i> (2012), that'
    ' "Western esotericism" is not a unified tradition of secret wisdom but a category of'
    ' rejection: bodies of knowledge that have been excluded from the normative canons of'
    ' academic rationality since the Enlightenment, and which therefore share the negative'
    ' characteristic of having been classified as irrational, superstitious, or merely'
    ' "religious" (in the pejorative sense) rather than the positive characteristic of'
    ' sharing common doctrines or practices. This negative definition is historically motivated:'
    ' before the Enlightenment construction of these exclusions, many of the practices and'
    ' texts now classified as "esoteric" were part of mainstream learned culture.</p>'
    '<p>Applied to alchemy, Hanegraaff\'s framework complements the [LINK:william-newman]/'
    '[LINK:lawrence-principe] revision. Both arguments require taking seriously knowledge'
    ' traditions that later historiography dismissed, and both require analyzing the mechanisms'
    ' by which dismissal occurred. Where Newman and Principe focus on the specific laboratory'
    ' practices and their displacement by eighteenth-century chemistry, Hanegraaff focuses'
    ' on the broader epistemological politics through which Hermetic, Neoplatonic, and'
    ' alchemical knowledge was reclassified as "occult" — a category that functions not'
    ' as a neutral description but as a marker of epistemological illegitimacy.</p>'
    '<p>His <i>Hermetic Spirituality and the Historical Imagination</i> (2022) traces the'
    ' construction and reconstruction of "Hermeticism" as a category from antiquity through'
    ' the present, demonstrating that each historical moment has remade the figure of'
    ' [LINK:hermes-trismegistus] in its own image. The ancient Hermetica, the Ficinian'
    ' Renaissance reception, the nineteenth-century Theosophical appropriation, and the'
    ' modern New Age deployment of "Hermetic" ideas are related but distinct traditions,'
    ' each serving different cultural and religious functions. This genealogical approach'
    ' provides tools for distinguishing between the historical alchemy of the early modern'
    ' laboratory and the modern occultist tradition that claims to continue it, a distinction'
    ' that is practically important for maintaining the scholarly standards that'
    ' [LINK:william-newman] and [LINK:lawrence-principe] have established.</p>'
)

# ── Garth Fowden ──────────────────────────────────────────────────────────────

FOWDEN_EXTRA = (
    '<h2>The Egyptian Hermes and Late Antique Religion</h2>'
    '<p>Fowden\'s <i>The Egyptian Hermes: A Historical Approach to the Late Pagan Mind</i> (1986)'
    ' provides the scholarly foundation for understanding the historical context from which'
    ' the Hermetic texts emerged. His central argument is that the philosophical Hermetica —'
    ' the dialogues of the <i>Corpus Hermeticum</i> and related texts — were produced in a'
    ' specific religious and intellectual milieu in Roman Egypt, where Greek philosophical'
    ' traditions (Platonism, Stoicism, Aristotelianism), Egyptian religious practice, and'
    ' Jewish thought were undergoing complex processes of synthesis. The Hermes Trismegistus'
    ' figure is the product of this synthesis: the Greek Hermes identified with the Egyptian'
    ' Thoth to produce an ideal author for texts that were themselves syntheses of Greek'
    ' philosophy and Egyptian religious wisdom.</p>'
    '<p>Fowden\'s account of the social context of Hermetic production — his argument that'
    ' the texts were produced within communities of philosophical piety concerned with'
    ' spiritual ascent through the planetary spheres — has been influential in situating'
    ' the Hermetica within the broader landscape of late antique religion. His work'
    ' connects to the scholarship of A.D. Nock and A.-J. Festugière, whose earlier'
    ' critical edition of the Hermetica established the documentary foundations,'
    ' and to the broader field of late antique religious history represented by'
    ' scholars like Peter Brown.</p>'
    '<p>For the history of alchemy, Fowden\'s significance is primarily as the scholar who'
    ' provided the most rigorous account of where the Hermetic texts actually came from —'
    ' and therefore why the Renaissance claim that they represented pre-Platonic Egyptian'
    ' wisdom was wrong. The alchemical tradition\'s appropriation of Hermetic authority'
    ' rested on an incorrect historical claim about the texts\' origins; Fowden\'s'
    ' scholarship, building on Casaubon and the subsequent critical tradition, demonstrates'
    ' that the actual Hermetica were products of late antique religious synthesis rather'
    ' than ancient Egyptian wisdom. This does not diminish their intellectual interest or'
    ' historical importance, but it does require recalibrating the claims made on their behalf'
    ' by Renaissance and early modern natural philosophers who treated them as pristine'
    ' ancient witnesses.</p>'
)

def load_all():
    conn = sqlite3.connect(DB)

    print('=== Quick top-ups ===')
    app(conn, 'albertus-magnus', ALBERTUS_EXTRA)
    app(conn, 'avicenna', AVICENNA_EXTRA)

    print('\n=== Major expansions ===')
    app(conn, 'marsilio-ficino', FICINO_EXTRA)
    app(conn, 'george-ripley', RIPLEY_EXTRA)
    app(conn, 'nicholas-flamel', FLAMEL_EXTRA)
    app(conn, 'hildegard-of-bingen', HILDEGARD_EXTRA)
    app(conn, 'william-newman', NEWMAN_EXTRA)
    app(conn, 'lawrence-principe', PRINCIPE_EXTRA)
    app(conn, 'john-dee', DEE_EXTRA)
    app(conn, 'henry-cornelius-agrippa', AGRIPPA_EXTRA)
    app(conn, 'hermes-trismegistus', HERMES_EXTRA)
    app(conn, 'thomas-aquinas', AQUINAS_EXTRA)
    app(conn, 'francis-bacon', BACON_EXTRA)
    app(conn, 'pico-della-mirandola', PICO_EXTRA)
    app(conn, 'giordano-bruno', BRUNO_EXTRA)
    app(conn, 'michael-sendivogius', SENDIVOGIUS_EXTRA)
    app(conn, 'john-of-rupescissa', RUPESCISSA_EXTRA)
    app(conn, 'pamela-smith', SMITH_EXTRA)
    app(conn, 'wouter-hanegraaff', HANEGRAAFF_EXTRA)
    app(conn, 'garth-fowden', FOWDEN_EXTRA)

    conn.commit()
    conn.close()
    print('\n=== Done ===')

if __name__ == '__main__':
    load_all()
