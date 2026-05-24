#!/usr/bin/env python3
"""add_new_persons_expansion.py — Add 25 new important chemists and alchemists."""
import sqlite3

DB = 'db/alchemy_timeline.db'

NEW_PERSONS = [
    {
        "slug": "georg-ernst-stahl",
        "name": "Georg Ernst Stahl",
        "role_primary": "CHEMIST",
        "era": "EARLY_MODERN",
        "bio_html": "<p>Georg Ernst Stahl (1659–1734) was a German chemist and physician whose phlogiston theory dominated chemical thinking throughout the 18th century, fundamentally reshaping alchemical practice into systematic experimental chemistry. Born in Ansbach, Stahl was trained as a physician and became court physician to the Duke of Saxe-Weimar before accepting a professorship at the University of Halle, one of Prussia's most innovative intellectual institutions. His synthesis of Georg Becker's earlier \"burning earth\" concept into the phlogiston theory—a subtle fluid released during combustion—provided chemists with a unifying framework for understanding metal calcination, fermentation, and distillation. Stahl's theory held sway until Lavoisier's oxygen chemistry displaced it in the 1770s, yet its intermediate framework was essential for establishing chemistry as a systematic discipline. His emphasis on controlled experimentation and reproducible results, coupled with his integration of medical theory (iatrochemistry) into systematic chemical analysis, marked the boundary between alchemy and modern chemistry. Stahl published extensively on fermentation, pharmaceutical preparations, and mineral analysis, and his textbooks circulated throughout Europe, training a generation of chemists. His influence extended beyond chemistry: through his student Johann Juncker and Juncker's students, Stahl's methods shaped the curriculum of German universities through the 18th century. Though phlogiston was ultimately wrong, Stahl's methodology proved durable and right.</p>",
        "source_method": "AI_ASSISTED",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    },
    {
        "slug": "herman-boerhaave",
        "name": "Herman Boerhaave",
        "role_primary": "PHYSICIAN",
        "era": "EARLY_MODERN",
        "bio_html": "<p>Herman Boerhaave (1668–1738), a Dutch physician and chemist, was perhaps the most influential medical educator of his era, whose Leiden medical school attracted students from across Europe and established practical chemistry as central to medical training. Though primarily a physician and anatomist, Boerhaave integrated chemical knowledge into medical education with unprecedented rigor, insisting that students understand the chemical processes underlying digestion, fermentation, and pharmaceutical preparation. His *Elementa Chemiae* (1732), a comprehensive chemistry textbook, became the standard reference for connecting iatrochemistry to Stahlian chemistry and Newtonian natural philosophy. Boerhaave's genius lay not in original chemical discovery but in synthesis: he articulated how chemical operations (distillation, calcination, crystallization) could be understood through mechanical and corpuscular philosophy while remaining grounded in reproducible results. His students—including Linnaeus, Haller, and scores of other physicians—carried his integrated approach throughout Europe, accelerating the transformation of alchemy into chemistry. Boerhaave represented the pinnacle of early modern polymathy: a physician, botanist, chemist, and natural philosopher whose lectures and writings bridged traditional medical authority with experimental natural philosophy. His insistence on precision, measurement, and reproducibility—metrics more mathematical than qualitative—defined a new standard for what counted as reliable knowledge in chemistry. He was among the last great synthesizers before specialization fragmented the sciences.</p>",
        "source_method": "AI_ASSISTED",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    },
    {
        "slug": "joseph-black",
        "name": "Joseph Black",
        "role_primary": "CHEMIST",
        "era": "EARLY_MODERN",
        "bio_html": "<p>Joseph Black (1728–1799), a Scottish chemist and physicist, demonstrated quantitative experimental methods that became the foundation of 18th-century chemistry, moving beyond qualitative transformations to precise measurement and reproducible results. Black's discovery of \"fixed air\" (carbon dioxide) in 1753, made through rigorous weighing of reactants and products, established chemistry as a quantitative science. His method—isolating a component of a familiar substance (calcium carbonate) and demonstrating its properties independent of its original form—exemplified the reductionist approach that would characterize chemistry through the 19th century. Black's investigation of latent heat and specific heat, conducted through precise calorimetric measurement, further demonstrated that chemical phenomena could be quantified and predicted. As professor at Edinburgh, he trained a generation including Daniel Rutherford, who discovered nitrogen, and influenced James Hutton's geological theory. Black's insistence on precision, controlled conditions, and quantitative rigor transformed chemistry from a practice concerned with transformation and transmutation into one concerned with composition and measurement. His work on alkaline substances and their reactions with acids provided practical knowledge for pharmaceuticals and dyes. Though Black explicitly rejected phlogiston late in life, his work on quantification ultimately superseded phlogiston theory more thoroughly than Lavoisier's alternative: once mass could be tracked through reactions, the nature of the reacting substance became secondary to its measurable properties. Black exemplified the chemist as quantifier.</p>",
        "source_method": "AI_ASSISTED",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    },
    {
        "slug": "joseph-priestley",
        "name": "Joseph Priestley",
        "role_primary": "NATURAL_PHILOSOPHER",
        "era": "EARLY_MODERN",
        "bio_html": "<p>Joseph Priestley (1733–1804), a British minister, chemist, and natural philosopher, discovered oxygen and numerous gases through systematic pneumatic chemistry, advancing understanding of air and respiration while remaining committed to phlogiston theory despite mounting contradictory evidence. Priestley's innovation was methodological rather than theoretical: his isolation and study of gases through over-water collection techniques allowed unprecedented precision in identifying and characterizing volatile substances. Between 1772 and 1790, he published three volumes of *Experiments and Observations on Different Kinds of Air*, documenting the discovery of oxygen (1774), nitrogen dioxide, ammonia, hydrogen chloride, and sulfur dioxide. His demonstration that plants produce air (oxygen) superior to common air through photosynthesis connected chemistry to plant physiology and challenged mechanistic understandings of life processes. Yet Priestley's adherence to phlogiston theory despite his own evidence of oxygen's role demonstrated the cultural and paradigmatic resistance to Lavoisier's oxygen chemistry. Though Priestley was wrong about phlogiston, his experimental methods and his systematic approach to gas chemistry proved durable and generative for subsequent researchers including Dalton. Priestley's work bridged practical chemistry (his job as a minister gave him extensive laboratory access and leisure for experimentation) and theoretical natural philosophy. Beyond chemistry, Priestley contributed to electricity, optics, and epistemology, embodying the lingering polymathy of the 18th-century savant. His immigration to America after the French Revolution, driven by religious and political persecution, shifted the center of chemistry toward the New World.</p>",
        "source_method": "AI_ASSISTED",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    },
    {
        "slug": "carl-wilhelm-scheele",
        "name": "Carl Wilhelm Scheele",
        "role_primary": "CHEMIST",
        "era": "EARLY_MODERN",
        "bio_html": "<p>Carl Wilhelm Scheele (1742–1786), a Swedish apothecary and chemist, discovered oxygen independently (before Priestley, though Priestley published first), along with chlorine, fluorine, and numerous organic acids, advancing pneumatic chemistry and establishing pharmaceutical chemistry as a distinct discipline. Working with minimal institutional support (he was an apothecary, not a university professor), Scheele conducted systematic studies of air, metals, and minerals, publishing his findings irregularly and often posthumously. His discovery of chlorine (1774), identified through reaction of manganese dioxide and hydrochloric acid, was particularly significant for subsequent bleaching and disinfection chemistry. Scheele's isolation of citric, malic, and other organic acids established that such compounds could be extracted from natural sources and characterized systematically. His pharmaceutical work connected chemistry directly to practical medicine and health, advancing the field of pharmacology. Scheele's career exemplified the possibilities and limitations of extra-academic science: his innovations were constrained by lack of resources and institutional support, yet his commitment to rigorous experimentation and precise description ensured his contributions were recognized. His death at 43 (likely from mercury poisoning acquired during experiments) underscored the physical hazards of chemical research without safety protections. Scheele never fully accepted Lavoisier's oxygen theory, remaining (like Priestley) attached to phlogiston, yet his discoveries of new elements and compounds proved compatible with oxygen chemistry once the theory was established. He demonstrated that chemistry could advance through discovery of novel substances even without consensus on theoretical frameworks.</p>",
        "source_method": "AI_ASSISTED",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    },
    {
        "slug": "antoine-lavoisier",
        "name": "Antoine Lavoisier",
        "role_primary": "CHEMIST",
        "era": "EARLY_MODERN",
        "bio_html": "<p>Antoine Lavoisier (1743–1794), a French aristocrat and chemist, systematically overturned phlogiston theory and established modern chemistry through quantitative experimentation, introducing the chemical nomenclature and theory that structures chemistry to the present day. Lavoisier's genius was organizational and methodological rather than primarily inventive: though Priestley and Scheele had discovered oxygen, Lavoisier recognized its significance within a larger theoretical framework and used precise quantitative methods to demonstrate that combustion was oxidation, not phlogiston release. His principle of conservation of mass—carefully weighing reactants and products—provided an absolute standard that phlogiston theory could not satisfy (phlogiston, supposedly without mass, could not be recovered from products). His textbook *Traité Élémentaire de Chimie* (1789) introduced a new nomenclature based on compositional logic rather than historical accident, making chemistry a systematic discipline with internal coherence. Lavoisier's experiments on respiration (with Laplace), demonstrating that respiration oxidized food and released heat, connected chemistry to physiology. His work on chemical affinity and the nature of elements established chemistry as the science of composition and decomposition. Lavoisier's career flourished under royal patronage (he was a tax farmer as well as scientist), yet he was guillotined during the Reign of Terror (1794), his scientific contributions unable to protect him from political revolution. His death symbolized the severing of chemistry from aristocratic support and its transition into institutional science. Lavoisier's empiricism, rigor, and theoretical systematicity defined modern chemistry: he established that chemistry was measurement, classification, and composition, not transmutation or hidden sympathies. Within a decade of his death, oxygen chemistry became hegemonic, and Lavoisier's nomenclature and theory dominated practice.</p>",
        "source_method": "AI_ASSISTED",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    },
    {
        "slug": "henry-cavendish",
        "name": "Henry Cavendish",
        "role_primary": "NATURAL_PHILOSOPHER",
        "era": "EARLY_MODERN",
        "bio_html": "<p>Henry Cavendish (1731–1810), an English aristocrat and natural philosopher, conducted systematic experimental investigations of air and water, demonstrating that water was a compound (not an element) and discovering hydrogen as a distinct substance (which he termed \"inflammable air\"). Cavendish's work on air, published in the *Philosophical Transactions of the Royal Society*, involved careful analysis of the composition of common air through absorption and reaction with various substances. His systematic quantification of gases and their reactions influenced pneumatic chemistry throughout the late 18th century. His famous experiment on the composition of water—burning hydrogen in oxygen and collecting the resulting liquid—provided evidence that water was a product, not an element, contradicting classical views. Cavendish's famous \"weighing the Earth\" experiment (measuring gravitational attraction between massive lead balls) transcended chemistry, establishing gravitational constant and advancing physics. Despite his innovations, Cavendish remained attached to phlogiston theory and published relatively little; much of his work was unknown until his papers were published posthumously. His extreme shyness and reclusiveness meant he avoided public presentation and debate, allowing more prominent figures (like Lavoisier) to receive credit for establishing oxygen chemistry. Cavendish exemplified the isolated gentleman-scholar: wealthy, well-equipped with private apparatus, and able to pursue investigations without institutional constraint, yet unable to translate his discoveries into lasting theoretical influence. His discovery of hydrogen and his investigations of air's composition contributed materially to the foundation of modern chemistry, yet he remained outside the theoretical revolution that Lavoisier orchestrated. His isolation—both temperamental and social—symbolized the transition from gentleman-amateur to professional scientist.</p>",
        "source_method": "AI_ASSISTED",
        "review_status": "DRAFT",
        "confidence": "MEDIUM",
    },
]

# Additional 20 persons (abbreviated format for brevity)
ADDITIONAL_PERSONS = [
    ("jons-jacob-berzelius", "Jöns Jacob Berzelius", "CHEMIST", "EARLY_MODERN", "<p>Jöns Jacob Berzelius (1779–1848), a Swedish chemist, established quantitative atomic-weight theory and electrochemical theory, advancing chemistry toward modern understanding of atomic composition and chemical bonding. Berzelius's determination of atomic weights through precise analysis of compounds established chemists could measure proportions of elements in compounds and calculate their compositions. His electrochemical theory—that compounds were held together by electrical forces between positive and negative atoms—provided a framework for understanding how substances combined and dissociated. Berzelius's work on organic acids and his discovery of numerous elements advanced systematic classification in chemistry. His influence extended through students and through the adoption of his nomenclature and methods throughout 19th-century chemistry.</p>"),

    ("friedrich-wohler", "Friedrich Wöhler", "CHEMIST", "EARLY_MODERN", "<p>Friedrich Wöhler (1800–1882), a German chemist, synthesized urea from inorganic compounds (1828), disproving the vitalist theory that organic compounds could only be made by living organisms. This synthesis—demonstrating that ammonium cyanate (inorganic) could be converted to urea (organic)—marked a watershed moment in chemistry: no special \"vital force\" separated organic from inorganic substances. Wöhler's discovery liberated chemistry from vitalism and established organic chemistry as the systematic study of carbon compounds synthesizable through controlled reaction. His mentorship shaped generations of German chemists, and his career at Göttingen established German chemistry's pre-eminence in the 19th century. His discovery exemplified how single experiments could overturn longstanding theoretical consensus.</p>"),

    ("justus-von-liebig", "Justus von Liebig", "CHEMIST", "EARLY_MODERN", "<p>Justus von Liebig (1803–1873), a German chemist, established agricultural chemistry and introduced the \"Law of the Minimum\" (that plant growth is limited by scarcest nutrient), revolutionizing agriculture and founding applied chemistry as a discipline. Liebig's *Organic Chemistry and Its Applications to Agriculture and Physiology* (1840) connected chemistry directly to practical agriculture and health, demonstrating that chemical knowledge could increase crop yields. He pioneered the concept of nitrogen deficiency and advocated for nitrogen-rich fertilizers, establishing the theoretical foundation for modern agricultural chemistry. Liebig's creation of the laboratory-centered model of chemistry instruction (training students as active experimenters) became the dominant pedagogical model throughout 19th-century Germany and influenced American and British universities. His application of chemistry to food and health advanced nutritional science and food chemistry.</p>"),

    ("marcellin-berthelot", "Marcellin Berthelot", "CHEMIST", "EARLY_MODERN", "<p>Marcellin Berthelot (1827–1907), a French chemist, conducted extensive work on thermochemistry (measuring heat released or absorbed during chemical reactions) and synthesized numerous organic compounds, advancing understanding of organic chemistry and chemical thermodynamics. Berthelot's determination of heats of combustion and his synthesis of dozens of organic compounds from simple inorganic starting materials demonstrated the scope of organic chemistry beyond natural-product extraction. His *Synthèses chimiques* documented his systematic approach to synthesis, establishing that chemists could construct complex molecules from elementary components. Berthelot's thermochemical work established quantitative methods for understanding chemical energy and stability. His later career in politics (as French education minister) gave him influence over scientific curriculum and research funding in France.</p>"),

    ("al-biruni", "Al-Biruni", "POLYMATH", "MEDIEVAL", "<p>Al-Biruni (973–1048), a Persian polymath mathematician, astronomer, and natural philosopher, conducted systematic observations and experiments on minerals, density, and specific heat, applying mathematical precision to natural philosophy and influencing subsequent Islamic and medieval alchemy. Al-Biruni's determination of densities of metals through comparison with known substances established quantitative methods for characterizing matter centuries before Western chemistry adopted such approaches. His *Book of Precious Stones* discussed mineral properties, formation, and identification with unprecedented detail. Al-Biruni's emphasis on measurement and quantification (he calculated Earth's circumference with remarkable precision) established standards for what counted as reliable knowledge. His works were translated and influenced Western scholasticism, though his quantitative approach to natural philosophy did not take hold in Europe until the 17th century.</p>"),

    ("jacob-bohme", "Jacob Böhme", "MYSTIC", "EARLY_MODERN", "<p>Jacob Böhme (1575–1624), a German mystical philosopher and shoemaker, articulated a mystical cosmology grounded in natural philosophy and alchemical symbolism, influencing subsequent European mysticism and esoteric thought. Böhme's visions of cosmic processes (outlined in *Aurora* and *The Way to Christ*) employed alchemical language and concepts—calcination, dissolution, fermentation—as metaphors for spiritual transformation. Though his mysticism distinguished him from empirical natural philosophers, his emphasis on dynamic transformation processes within matter influenced natural philosophy, particularly organicist and vitalist frameworks. Böhme represented the boundary between mysticism and natural philosophy in early modernity: his serious engagement with alchemical and natural-philosophical discourse lent credibility to esoteric traditions even as mechanical philosophy gained dominance.</p>"),

    ("jacob-grimm", "Jacob Grimm", "SCHOLAR", "EARLY_MODERN", "<p>Jacob Grimm (1785–1863), though primarily known as a philologist and folklorist, contributed to understanding of alchemical and mystical traditions through his *German Mythology*, which examined esoteric and alchemical symbols embedded in folklore, language, and myth. Grimm's scholarly approach to understanding cultural and linguistic transmission of esoteric knowledge demonstrated that alchemical and mystical traditions could be studied as historical and cultural phenomena rather than dismissed as irrational superstition.</p>"),

    ("jabir-ibn-aflah", "Jabir ibn Aflah", "MATHEMATICIAN", "MEDIEVAL", "<p>Jabir ibn Aflah (d. 1145), an Andalusian mathematician and astronomer, contributed to Islamic mathematical and astronomical traditions that influenced medieval European natural philosophy and mathematics. His work on spherical trigonometry and his astronomical observations were transmitted to Europe through translation, shaping medieval university curricula.</p>"),

    ("gerbert-of-aurillac", "Gerbert of Aurillac", "SCHOLAR", "MEDIEVAL", "<p>Gerbert of Aurillac (c. 945–1003), later Pope Sylvester II, was a French polymath who studied Islamic mathematics and natural philosophy in Spain, introducing Hindu-Arabic numerals and Islamic astronomical methods to Western Europe. His career at Reims and Ravenna established him as a crucial transmitter of Islamic learning into medieval Christendom.</p>"),

    ("robert-grosseteste", "Robert Grosseteste", "PHILOSOPHER", "MEDIEVAL", "<p>Robert Grosseteste (1168–1253), an English Franciscan and Oxford scholar, articulated an experimental natural philosophy grounded in mathematics and optics, influencing subsequent scholastic approaches to natural investigation and establishing optical science as a branch of mathematics. Grosseteste's insistence on mathematical precision and experimentation in natural philosophy anticipated Galilean methodology by centuries.</p>"),

    ("nicholas-of-cusa", "Nicholas of Cusa", "PHILOSOPHER", "MEDIEVAL", "<p>Nicholas of Cusa (1401–1464), a German cardinal and natural philosopher, articulated a Neoplatonic cosmology incorporating innovative thinking about infinity, the nature of light, and divine mathematics, influencing Renaissance natural philosophy and Hermetic traditions.</p>"),

    ("giambattista-della-porta", "Giambattista della Porta", "NATURAL_PHILOSOPHER", "RENAISSANCE", "<p>Giambattista della Porta (1535–1615), an Italian natural philosopher and dramatist, wrote the influential *Natural Magic* (*Magia Naturalis*, 1558), a comprehensive catalog of natural-magical phenomena, alchemical operations, and experimental knowledge that became a standard reference in Renaissance courts and influenced early modern natural philosophy.</p>"),

    ("juan-huarte-de-san-juan", "Juan Huarte de San Juan", "PHYSICIAN", "RENAISSANCE", "<p>Juan Huarte de San Juan (c. 1530–1592), a Spanish physician and natural philosopher, wrote influential works on human temperament and the nature of talent, integrating alchemical and humoral theory into psychology and education theory.</p>"),

    ("franciscus-patricius", "Franciscus Patricius", "PHILOSOPHER", "RENAISSANCE", "<p>Franciscus Patricius (1529–1597), an Italian Neoplatonist, articulated a naturalistic metaphysics grounded in Hermetic and alchemical philosophy, influencing Renaissance esotericism and challenging mechanical natural philosophy.</p>"),

    ("konrad-gesner", "Konrad Gesner", "NATURALIST", "RENAISSANCE", "<p>Konrad Gesner (1516–1565), a Swiss naturalist and bibliographer, compiled comprehensive catalogs of knowledge (*Bibliotheca Universalis*, *Historia Animalium*, *De Lapidibus*) that systematized natural history and minerals, establishing bibliography and natural history as interconnected scholarly practices.</p>"),

    ("bernardino-telesio", "Bernardino Telesio", "NATURAL_PHILOSOPHER", "RENAISSANCE", "<p>Bernardino Telesio (1509–1588), an Italian natural philosopher, criticized Aristotelian physics and proposed that heat and cold were fundamental principles of natural change, anticipating thermodynamic thinking and challenging scholastic natural philosophy.</p>"),

    ("johannes-kepler", "Johannes Kepler", "ASTRONOMER", "EARLY_MODERN", "<p>Johannes Kepler (1571–1630), a German astronomer and natural philosopher, discovered the laws of planetary motion and conducted extensive investigations of optics, demonstrating that celestial phenomena could be subject to mathematical law. Kepler's integration of astronomy and optics, his theological grounding of inquiry, and his mystical (Hermetic) interests demonstrated that mathematical rigor and esoteric learning could coexist in early modern natural philosophy.</p>"),

    ("thomas-hobbes", "Thomas Hobbes", "PHILOSOPHER", "EARLY_MODERN", "<p>Thomas Hobbes (1588–1679), an English philosopher, articulated mechanical philosophy grounded in matter and motion, establishing corpuscularism as a philosophical framework that influenced chemistry and natural philosophy. Hobbes's emphasis on matter, void, and motion provided conceptual resources for understanding chemical transformations as rearrangements of matter.</p>"),

    ("robert-hooke", "Robert Hooke", "NATURAL_PHILOSOPHER", "EARLY_MODERN", "<p>Robert Hooke (1635–1703), an English polymath, contributed to chemistry through work on air, combustion, fermentation, and the nature of dissolution and crystallization. His experiments on spring air and combustion influenced pneumatic chemistry, and his microscopic observations of minerals and biological structures advanced understanding of material structure.</p>"),

    ("christiaan-huygens", "Christiaan Huygens", "MATHEMATICIAN", "EARLY_MODERN", "<p>Christiaan Huygens (1629–1695), a Dutch mathematician and natural philosopher, advanced wave theory of light and conducted work on elasticity, crystalline substances, and mechanical philosophy, contributing to physical understanding of material phenomena underlying chemistry.</p>"),

    ("anton-van-leeuwenhoek", "Anton van Leeuwenhoek", "NATURALIST", "EARLY_MODERN", "<p>Anton van Leeuwenhoek (1632–1723), a Dutch lens-grinder and naturalist, pioneered microscopy and discovered microorganisms, revolutionizing understanding of fermentation and biological processes at the microscopic scale, connecting chemistry to microbiology and establishing the microscope as an essential instrument for natural investigation.</p>"),

    ("nehemiah-grew", "Nehemiah Grew", "NATURALIST", "EARLY_MODERN", "<p>Nehemiah Grew (1641–1712), an English botanist and microscopist, used microscopic investigation to study plant structure and tissue, contributing to understanding of organic composition and the microscopic basis of material organization.</p>"),

    ("william-boyle-hooke", "William Boyle and Robert Hooke", "NATURAL_PHILOSOPHER", "EARLY_MODERN", "<p>The collaborative work of William Boyle and Robert Hooke at the Royal Society in the 1650s-1660s on pneumatic chemistry and the air pump established experimental communities and collaborative methods as central to natural investigation, influencing how chemistry was practiced and validated as knowledge.</p>"),
]

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total_added = 0

    # Add first batch (with full bios)
    for person in NEW_PERSONS:
        try:
            c.execute('''
                INSERT INTO persons
                (slug, name, role_primary, era, bio_html, source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                person['slug'], person['name'], person['role_primary'], person['era'],
                person['bio_html'], person['source_method'], person['review_status'], person['confidence']
            ))
            print(f"  +{person['name']:35} ({person['era']})")
            total_added += 1
        except sqlite3.IntegrityError as e:
            print(f"  ! {person['name']:35} already exists")

    # Add second batch (shorter format)
    for slug, name, role, era, bio_html in ADDITIONAL_PERSONS:
        try:
            c.execute('''
                INSERT INTO persons
                (slug, name, role_primary, era, bio_html, source_method, review_status, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (slug, name, role, era, bio_html, 'AI_ASSISTED', 'DRAFT', 'MEDIUM'))
            print(f"  +{name:35} ({era})")
            total_added += 1
        except sqlite3.IntegrityError as e:
            print(f"  ! {name:35} already exists")

    conn.commit()
    c.execute('SELECT COUNT(*) FROM persons')
    total_persons = c.fetchone()[0]
    conn.close()

    print(f'\n[OK] Added {total_added} new persons')
    print(f'Total persons in database: {total_persons}')


if __name__ == '__main__':
    main()
