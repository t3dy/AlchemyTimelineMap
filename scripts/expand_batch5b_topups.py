#!/usr/bin/env python3
"""expand_batch5b_topups.py — Top-up persons still below 1200 words after batch 5."""
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

RIPLEY_TOP = (
    '<p>The survival of Ripley\'s works in multiple manuscript traditions and in Ashmole\'s printed'
    ' compilation demonstrates the durability of the English verse alchemy tradition. His <i>Compound</i>'
    ' was cited by Samuel Norton, by Elias Ashmole, and by other practitioners through the seventeenth'
    ' century as an authoritative English statement of alchemical process. The twelve-gate structure'
    ' influenced subsequent systematic treatments of alchemy as a sequence of operations, contributing'
    ' to the development of the systematic experimental program that Newman identifies in Starkey\'s work.</p>'
)

FLAMEL_TOP = (
    '<p>The Flamel case is one of the clearest illustrations of how the construction of legendary'
    ' alchemical authority worked in practice. A real historical figure — documented, well-attested,'
    ' prosperous — became the anchor for a pseudepigraphal tradition because the combination of'
    ' documented existence and undocumented wealth made the legend plausible to those who wanted to'
    ' believe it. The lesson for the historiography of alchemy is methodological: the presence of a'
    ' real person in the historical record does not guarantee that texts attributed to that person'
    ' are genuine, and the most persuasive legends are those attached to figures about whom some'
    ' true things can be independently confirmed.</p>'
)

HILDEGARD_TOP = (
    '<p>The modern revival of interest in Hildegard — through recordings of her music, through'
    ' the "alternative medicine" appropriation of her herbalism and dietary recommendations, and'
    ' through her beatification and canonization by Pope Benedict XVI in 2012 — has sometimes'
    ' distorted the historical picture by projecting contemporary concerns onto a twelfth-century'
    ' abbess. The scholarly Hildegard, whose visionary claims were grounded in the specific'
    ' institutional context of Benedictine religious life and the theological controversies of'
    ' her era, is a more complex and more interesting figure than the "medieval health guru"'
    ' of popular appropriation. Her <i>Physica</i> reflects genuine observation of the natural'
    ' world, but within a framework of symbolic correspondences and theological meaning that is'
    ' inseparable from her medical recommendations and cannot be extracted from them without'
    ' misrepresenting what she was doing.</p>'
)

PRINCIPE_TOP = (
    '<p>The collaborative framework Principe has built at Johns Hopkins — combining his laboratory'
    ' replication work with [LINK:william-newman]\'s manuscript-critical scholarship — represents'
    ' a model for how the history of alchemy should be pursued: lab work and archival work'
    ' together, each informing and constraining the other. His <i>The Secrets of Alchemy</i>'
    ' (University of Chicago Press, 2013) consolidates this approach for a general audience,'
    ' demonstrating that rigorous scholarship and accessible communication are compatible goals.'
    ' His influence on students and on the field more broadly positions him as one of the'
    ' defining figures in the scholarly rehabilitation of alchemy as a legitimate subject of'
    ' historical inquiry.</p>'
)

AGRIPPA_TOP = (
    '<p>The reception of <i>De Occulta Philosophia</i> demonstrates the complex relationship'
    ' between print culture and the transmission of learned magic. Available in print from 1531,'
    ' it circulated to audiences that included both serious philosophical practitioners and readers'
    ' seeking popular magical knowledge — a combination that created interpretive problems for'
    ' authorities and for subsequent scholars trying to assess its influence on the development'
    ' of natural philosophy.</p>'
)

AQUINAS_TOP = (
    '<p>The genuine Thomist engagement with alchemical questions, traceable in the authentic'
    ' commentaries on Aristotle, illustrates that medieval scholastic philosophy could not'
    ' avoid alchemy entirely: alchemical claims about metallic transformation were natural'
    ' philosophical claims that any systematic account of matter and change had to address.'
    ' Aquinas\'s careful response — neither endorsing nor absolutely rejecting the possibility'
    ' of artificial metallic generation — reflects the limits of thirteenth-century theoretical'
    ' resources for deciding the question, and demonstrates that the relationship between'
    ' scholastic philosophy and alchemy was one of serious intellectual engagement rather than'
    ' simple dismissal.</p>'
)

BACON_F_TOP = (
    '<p>Francis Bacon\'s influence on English natural philosophy was as much institutional as'
    ' intellectual: the program for collaborative, organized, state-supported natural inquiry'
    ' that he outlined in <i>New Atlantis</i> (1627) became the model invoked by the founders'
    ' of the Royal Society in 1660. The actual research practices of Royal Society members —'
    ' including [LINK:robert-boyle]\'s chymical inquiries — were not straightforwardly Baconian,'
    ' but the Baconian rhetoric of useful, practical, systematic knowledge legitimized the'
    ' experimental program and distinguished it from the speculative natural philosophy that'
    ' the new institution was designed to replace.</p>'
)

PICO_TOP = (
    '<p>Pico\'s death at thirty-one cut short what might have been a longer program of'
    ' philosophical synthesis. His influence on the generation of [LINK:henry-cornelius-agrippa]'
    ' and on sixteenth-century Neoplatonic and Hermetic thought was exercised primarily through'
    ' the <i>Oration</i> and through the <i>Conclusiones</i> (Nine Hundred Theses, 1486)'
    ' — the ambitious compilation that Pope Innocent VIII found theologically suspect. The'
    ' theological controversy that attached to Pico\'s program of universal synthesis illustrates'
    ' the institutional pressures that shaped how natural magic and its alchemical applications'
    ' were pursued in the early sixteenth century.</p>'
)

BRUNO_TOP = (
    '<p>Bruno\'s memory arts — his series of treatises on artificial memory systems, including'
    ' <i>De Umbris Idearum</i> (On the Shadows of Ideas, 1582) — drew on the classical tradition'
    ' of the art of memory but combined it with Lullian combinatorics and Hermetic symbolism to'
    ' produce systems of extraordinary complexity. Frances Yates analyzed these in <i>The Art'
    ' of Memory</i> (1966) as expressions of a Hermetic magical worldview in which mastering the'
    ' images of the memory palace meant mastering the fundamental structures of a divinely ordered'
    ' cosmos. Whether or not this interpretation is fully accepted, the memory arts intersected'
    ' with alchemical emblematic practice in the shared use of symbolic imagery as a vehicle for'
    ' encoded knowledge about nature.</p>'
)

SENDIVOGIUS_TOP = (
    '<h2>Influence on Newton and Later Pneumatic Chemistry</h2>'
    '<p>The specific influence of Sendivogius on [LINK:isaac-newton]\'s concept of the"aerial niter"'
    ' has been traced by Karin Figala and others. Newton\'s query about whether a nitrous spirit in'
    ' the air might serve as the universal active principle — sustaining life, enabling combustion,'
    ' mediating gravitational attraction — reflects the Sendivogian language of the spirit of niter'
    ' translated into Newton\'s own natural philosophical framework. This line of influence represents'
    ' one of the specific channels through which early modern alchemical concepts contributed to'
    ' the formation of Newtonian natural philosophy, a contribution that becomes visible only when'
    ' Newton\'s alchemical reading is taken seriously rather than dismissed as an eccentric private'
    ' obsession.</p>'
    '<p>The relationship between Sendivogius\'s spirit of niter and the eighteenth-century pneumatic'
    ' revolution is indirect but real. The concept of a chemically specific atmospheric component'
    ' essential to combustion and respiration anticipated the experimental program that would lead'
    ' [LINK:carl-wilhelm-scheele] and Joseph Priestley to isolate oxygen. They worked within the'
    ' phlogiston framework rather than the Sendivogian one, but the underlying question — what is'
    ' the active component of air that sustains fire and life? — connects the traditions across'
    ' the intervening century of chemical development.</p>'
)

RUPESCISSA_TOP = (
    '<h2>Institutional Context and Transmission</h2>'
    '<p>Rupescissa wrote in Franciscan captivity, confined by his order for prophetic and reforming'
    ' activities that the institutional church found disruptive. His laboratory work and his'
    ' prophetic writings were produced under the same conditions of constraint and opposition,'
    ' and it is not possible to separate the pharmaceutical program from the apocalyptic framework'
    ' that motivated it: he expected the quintessence medicines would be needed because he expected'
    ' apocalyptic tribulation to make normal Galenic medicine insufficient. This integration of'
    ' laboratory practice with theological urgency is characteristic of a specifically Franciscan'
    ' tradition of practical engagement with the material world in service of spiritual and social'
    ' reform — a tradition that influenced [LINK:paracelsus] and the broader Paracelsian movement'
    ' of the sixteenth century even when direct textual connections are difficult to trace.</p>'
    '<p>The transmission of Rupescissa\'s quintessence concept through pseudo-Lullian alchemical'
    ' texts and eventually into the Paracelsian tradition represents an important case study in'
    ' how medieval alchemical innovations were transmitted and transformed. The concept was'
    ' detached from its Franciscan apocalyptic context, reinterpreted within different theoretical'
    ' frameworks, and eventually became a standard element of early modern chemical medicine —'
    ' a trajectory that demonstrates both the productivity and the instability of alchemical'
    ' conceptual innovations as they moved through different intellectual environments.</p>'
)

SMITH_TOP = (
    '<h2>Material Culture and the Senses</h2>'
    '<p>Smith\'s contribution to the history of alchemy lies in her insistence that the material'
    ' culture of the workshop — the specific tools, materials, and physical environments in which'
    ' early modern artisans worked — was a form of knowledge, not merely a context for knowledge.'
    ' Her concept of "artisanal epistemology" (distinct from but related to Pamela O. Long\'s'
    ' "openness, secrecy, authorship" framework) argues that what artisans knew was embodied in'
    ' their skilled practice and their sensory attunement to materials, not merely in the recipes'
    ' and formulas they could articulate. This creates interpretive challenges for historians'
    ' working from texts alone: the most important knowledge may be precisely what was not written'
    ' down because it could not be adequately expressed in words.</p>'
    '<p>The Making and Knowing project (the Ms. Fr. 640 reconstruction) has demonstrated how much'
    ' can be recovered through reconstructive experiment even when written records are incomplete.'
    ' The project\'s multi-disciplinary approach — bringing together historians of science,'
    ' archaeologists, materials scientists, and practicing artisans — models a collaborative'
    ' methodology that parallels [LINK:lawrence-principe]\'s laboratory history of alchemy.'
    ' The convergence of these two programs — both emphasizing material practice as the site'
    ' of historical knowledge production — represents a significant reorientation of the'
    ' history of early modern science toward embodied, sensory, workshop-based inquiry.</p>'
)

HANEGRAAFF_TOP = (
    '<h2>Alchemy within Western Esotericism</h2>'
    '<p>Hanegraaff\'s treatment of alchemy within the Western esoteric tradition distinguishes'
    ' between the historical phenomenon — practitioners in specific times and places pursuing'
    ' specific laboratory and spiritual goals — and the later esotericist reconstruction of'
    ' alchemy as a timeless tradition of spiritual wisdom. The distinction matters because'
    ' the esotericist tradition has influenced how alchemy has been studied: Carl Gustav Jung\'s'
    ' interpretation of alchemical symbolism as the projection of unconscious psychological'
    ' processes onto material substances, for instance, treats the historical practitioners as'
    ' primarily interesting for what they revealed about the structure of the human psyche rather'
    ' than for what they were actually trying to do in their laboratories. Hanegraaff\'s approach,'
    ' like [LINK:william-newman] and [LINK:lawrence-principe]\'s, requires recovering the'
    ' historical actors on their own terms before evaluating modern interpretive traditions.'
    ' His genealogical method provides the historical-critical tools for this recovery in the'
    ' domain of religious and esoteric history.</p>'
    '<p>Within the institutional history of the field, Hanegraaff has been a primary organizer'
    ' of the academic study of Western esotericism as a recognized area of inquiry. His'
    ' association with the European Society for the Study of Western Esotericism, his'
    ' editorial work on journals and reference volumes, and his Amsterdam professorship in'
    ' the History of Hermetic Philosophy and Related Currents (the first such chair anywhere)'
    ' have created institutional infrastructure for scholarship that was previously conducted'
    ' in fragmented ways across different disciplines. The result is a field that can now'
    ' engage with alchemical history alongside Hermeticism, Kabbalah, Rosicrucianism, and'
    ' other traditions in a way that acknowledges their historical interconnections without'
    ' collapsing their differences.</p>'
)

FOWDEN_TOP = (
    '<h2>Impact on Alchemy Historiography</h2>'
    '<p>Fowden\'s work has been important for the historiography of alchemy primarily through'
    ' its effect on how scholars understand the Hermetic texts that alchemical practitioners'
    ' cited as authoritative. By establishing the actual historical context of these texts —'
    ' Roman Egypt, the second through fourth centuries CE, Greco-Egyptian religious syncretism'
    ' — Fowden made it possible to ask what the texts meant in their original context rather'
    ' than only in the Renaissance reception that [LINK:marsilio-ficino]\'s translations shaped.'
    ' This distinction between original meaning and reception meaning is methodologically'
    ' important for the history of alchemy: the alchemical tradition used the Hermetic texts'
    ' in ways that were not governed by their original meaning, and understanding what was'
    ' projected onto them by later readers requires first understanding what they actually said.'
    ' Fowden\'s historical scholarship provides that baseline.</p>'
    '<p>His subsequent work on <i>Empire to Commonwealth: Consequences of Monotheism in Late'
    ' Antiquity</i> (1993) broadened his analysis to the political and religious transformations'
    ' of the late Roman world, situating the Hermetic tradition within the larger story of'
    ' how Mediterranean religious culture was reorganized by the rise of Christianity and Islam.'
    ' For the history of alchemy, this broader context matters because it explains how the'
    ' Hermetic texts survived into medieval Christian Europe and Islamic culture in forms'
    ' available for later appropriation: through the same processes of religious synthesis'
    ' and cultural translation that Fowden analyzed in his earlier work.</p>'
)

def load_all():
    conn = sqlite3.connect(DB)

    print('=== Near-minimum top-ups ===')
    app(conn, 'george-ripley', RIPLEY_TOP)
    app(conn, 'nicholas-flamel', FLAMEL_TOP)
    app(conn, 'hildegard-of-bingen', HILDEGARD_TOP)
    app(conn, 'lawrence-principe', PRINCIPE_TOP)
    app(conn, 'henry-cornelius-agrippa', AGRIPPA_TOP)
    app(conn, 'thomas-aquinas', AQUINAS_TOP)
    app(conn, 'francis-bacon', BACON_F_TOP)
    app(conn, 'pico-della-mirandola', PICO_TOP)
    app(conn, 'giordano-bruno', BRUNO_TOP)

    print('\n=== Deeper expansions ===')
    app(conn, 'michael-sendivogius', SENDIVOGIUS_TOP)
    app(conn, 'john-of-rupescissa', RUPESCISSA_TOP)
    app(conn, 'pamela-smith', SMITH_TOP)
    app(conn, 'wouter-hanegraaff', HANEGRAAFF_TOP)
    app(conn, 'garth-fowden', FOWDEN_TOP)

    conn.commit()
    conn.close()
    print('\n=== Done ===')

if __name__ == '__main__':
    load_all()
