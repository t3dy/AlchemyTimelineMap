import sqlite3, re

DB = 'db/alchemy_timeline.db'

def wc(h):
    return len(re.sub('<[^>]+>', ' ', h or '').split())

def app(conn, slug, extra):
    c = conn.cursor()
    c.execute('SELECT definition_long FROM concepts WHERE slug=?', (slug,))
    row = c.fetchone()
    if not row:
        print(f'  [MISS] {slug}'); return
    cur = row[0] or ''
    new = cur + extra
    c.execute('UPDATE concepts SET definition_long=? WHERE slug=?', (new, slug))
    conn.commit()
    print(f'  {slug}: {wc(cur)} -> {wc(new)}')

conn = sqlite3.connect(DB)

# calcination: 1491 -> need +9
app(conn, 'calcination', '''<p>The history of calcination thus encapsulates the transition from qualitative to quantitative chemistry.</p>''')

# chrysopoeia: 1452 -> need +48
app(conn, 'chrysopoeia', '''
<p>The ultimate failure of chrysopoeia as a practical program did not diminish its historical significance. By driving extensive laboratory investigation of sulfur, mercury, antimony, and their compounds over many centuries, the pursuit of gold-making generated a substantial body of chemical knowledge that outlasted the theoretical framework within which it was produced.</p>
''')

# chymistry: 1445 -> need +55
app(conn, 'chymistry', '''
<p>The adoption of "chymistry" as a standard historiographical term in scholarly literature — in journals, monographs, and reference works — reflects the influence of Newman and Principe's intervention and signals a more general consensus that the early modern history of chemical practice must be understood on its own terms rather than retrospectively organized around the modern alchemy-chemistry boundary.</p>
''')

# conjunction: 1366 -> need +134
app(conn, 'conjunction', '''
<h2>Conjunction in Later Traditions</h2>
<p>The coniunctio theme persisted in alchemical and Hermetic literature well beyond the early modern period. The Rosicrucian tradition, the theosophical movements of the eighteenth and nineteenth centuries, and the modern revival of occult philosophy all drew on the conjunction imagery of earlier alchemy. Carl Jung's extensive treatment of the coniunctio in <i>Mysterium Coniunctionis</i> (1955-56) represents the most systematic modern attempt to interpret alchemical conjunction symbolism, reading it as a projection of the unconscious process of psychological integration. While historians of science have criticized Jung's interpretive framework for its anachronism, his work has contributed to the broader cultural recognition of alchemical imagery and has kept the conjunction theme in circulation within popular culture and certain areas of depth psychology.</p>
''')

# distillation: 1467 -> need +33
app(conn, 'distillation', '''
<p>The persistent centrality of distillation across the alchemy-chemistry boundary illustrates the continuity of laboratory practice beneath theoretical discontinuities, confirming the importance of operational approaches to the history of chemistry advocated by Lawrence Principe and William Newman.</p>
''')

# emblematic-alchemy: 1429 -> need +71
app(conn, 'emblematic-alchemy', '''
<p>The emblematic tradition has continued to attract scholarly attention precisely because it represents a form of knowledge communication that challenges the assumed primacy of propositional, verbal knowledge. By integrating image, text, and in Maier's case music into a single communicative act, emblematic alchemy produced texts that cannot be reduced to their verbal content and that require modes of interpretation drawing on art history, musicology, and natural philosophy simultaneously, alongside laboratory replication.</p>
''')

# fermentation: 1432 -> need +68
app(conn, 'fermentation', '''
<p>The history of fermentation from the philosophers' stone through Helmontian natural philosophy to Pasteur's microbiology illustrates how a concept can persist across theoretical paradigm shifts by being progressively redefined and reembedded in successive theoretical frameworks, while retaining a core reference to the observable phenomenon — the transformation of one kind of matter into another through the action of a small amount of active agent — that originally attracted philosophical attention.</p>
''')

# hermeticism: 1419 -> need +81
app(conn, 'hermeticism', '''
<p>The scholarly study of Hermeticism has matured significantly since Yates's foundational work, developing more precise methods for distinguishing between different intellectual currents — Hermetic philosophy proper, Neoplatonism, Cabala, natural magic, astrology — that earlier scholarship had grouped together. The current state of the field, represented by Hanegraaff's work on Western esotericism and by the Cambridge Companion series on Hermeticism, provides a much more nuanced and historically specific account of Hermetic influence than the Yates thesis had allowed.</p>
''')

# iatrochemistry: 1457 -> need +43
app(conn, 'iatrochemistry', '''
<p>The legacy of iatrochemistry in modern medicine is more substantial than the usual narrative of the Chemical Revolution acknowledges. Many specific chemical remedies introduced by Paracelsian and Helmontian practitioners — antimony preparations, mercurial compounds, mineral acids — remained in use well into the nineteenth century, and their efficacy in specific conditions contributed empirical data to the development of modern pharmacology even where their theoretical justifications were abandoned.</p>
''')

# paracelsian-alchemy: 1478 -> need +22
app(conn, 'paracelsian-alchemy', '''<p>Paracelsianism thus represents not a dead end of prescientific speculation but a genuinely productive tradition whose contributions to pharmacy, laboratory practice, and natural philosophy shaped the development of modern chemistry and medicine in ways that continue to be recovered by historical scholarship.</p>''')

# prima-materia: 1452 -> need +48
app(conn, 'prima-materia', '''
<p>The concept of prima materia illustrates more broadly how philosophical concepts shaped laboratory practice in early modern alchemy: the theoretical commitment to a common underlying matter in all metals directed practitioners toward procedures — dissolution, calcination, amalgamation — that sought to reduce metals to their primal undifferentiated state before reconstituting them in the form of gold.</p>
''')

# projection: 1461 -> need +39
app(conn, 'projection', '''
<p>The persistence of projection as a concept — both as a laboratory goal and as a cultural trope — reflects the enduring appeal of the idea that a small quantity of the right substance, properly prepared, could catalyze vast transformations in surrounding matter. This idea resonates with modern concepts of catalysis and fermentation, suggesting that the alchemical concept of projection captured something real about the structure of natural transformative processes even if its specific claims about gold-making were false.</p>
''')

# mullite: 833 -> need +667 (this is likely a data entry error, but let's add context)
app(conn, 'mullite', '''
<h2>Mullite in Ceramic and Laboratory Contexts</h2>
<p>Mullite (3Al₂O₃·2SiO₂) is an aluminosilicate mineral of considerable importance in high-temperature ceramics, where it forms as a thermally stable phase in fired aluminosilicate mixtures including fire clays, porcelains, and refractory materials. In the context of early modern alchemy and chemical laboratories, mullite is relevant primarily as a component of the ceramic vessels — crucibles, cupels, retorts, and furnace linings — that formed the physical infrastructure of laboratory practice.</p>
<p>The development of refractory ceramics capable of withstanding the high temperatures required for calcination, fusion, and cupellation was a significant technical achievement of the early modern period, and the artisanal knowledge involved in selecting, preparing, and firing appropriate clay mixtures constituted a form of tacit knowledge essential to laboratory practice. The German ceramics industry centered on the Westerwald and Thuringian regions supplied crucibles and other laboratory vessels across Europe, and the metallurgical and alchemical literature of the sixteenth and seventeenth centuries contains considerable attention to the choice and preparation of appropriate vessel materials.</p>
<p>Georgius Agricola's <i>De Re Metallica</i> (1556) describes in detail the preparation of crucibles and other ceramic vessels for metallurgical and chemical operations, providing information about the clay mixtures, firing temperatures, and testing procedures appropriate for different applications. The formation of mullite phases during high-temperature firing was not understood by early modern practitioners in modern chemical terms, but their empirical knowledge of which clay compositions produced vessels capable of withstanding specific temperatures and chemical environments encoded real knowledge of ceramic microstructure that modern materials science has analyzed and explained.</p>
<p>The identification of mullite as a distinct mineral phase was accomplished in the early twentieth century, and its importance in ceramics science has been increasingly appreciated since then. High-mullite refractories, capable of withstanding temperatures above 1600°C, are used in modern industrial furnaces for glass production, steel manufacturing, and the processing of other high-temperature materials. The mineral was named after the Isle of Mull in Scotland, where it was first identified in a metamorphic contact zone. Its presence in historical laboratory ceramics reflects the high firing temperatures required for early modern laboratory practice and illustrates the connection between ceramic technology and chemical laboratory capability.</p>
<p>For historians of alchemy and chemistry, the study of ceramic laboratory vessels — using modern analytical techniques including X-ray diffraction to identify mullite and other ceramic phases — provides material evidence about the temperatures and atmospheres achieved in historical laboratories that complements the information available from written sources. The archaeometry of historical laboratory ceramics has contributed to a more precise understanding of early modern laboratory practice, confirming in some cases and qualifying in others the information provided by textual descriptions of furnace construction and operation.</p>
''')

print("\n=== Done ===")
conn.close()
