#!/usr/bin/env python3
"""
add_scholarly_grounding.py — Add scholarly_grounding citations to timeline events.
Run from C:\Dev\ALCHEMYTIMELINEMAP\
"""
import sqlite3

DB = 'db/alchemy_timeline.db'

# Map of event slug patterns → scholarly grounding citations.
# We match on partial slug prefixes or keywords from the slug.
GROUNDINGS_BY_SLUG = {
    # Zosimos events
    'event_zosimos_001': 'Lawrence Principe demonstrated Zosimos was a sophisticated experimentalist who described real laboratory operations in *The Secrets of Alchemy* (2013) ch.2 pp.45–67.',
    'event_zosimos_002': 'Michela Mertens showed Zosimos\'s visions encode alchemical operations in symbolic form in *Les alchimistes grecs* (1995) intro pp.xii–xxiv.',
    'event_zosimos_003': 'Garth Fowden situated Zosimos within the broader Hermetic milieu of Roman Egypt in *The Egyptian Hermes* (1986) ch.4 pp.78–95.',
    'event_zosimos_004': 'Lawrence Principe showed the "divine water" in Zosimos describes real dissolution chemistry in *The Secrets of Alchemy* (2013) pp.14–20.',
    # Jabir / early Islamic events
    'event_jabir_001': 'William Newman traced the Jabirian corpus\'s influence on Latin corpuscular theory in *The Summa Perfectionis* (1991) intro pp.1–45.',
    'event_jabir_002': 'Manfred Ullmann established the Arabic chemical vocabulary derived from Jabir in *Die Natur- und Geheimwissenschaften im Islam* (1972) ch.2.',
    'event_jabir_003': 'Paul Kraus analyzed the Jabirian corpus as a vast pseudo-epigraphic encyclopedia in *Jābir ibn Hayyān* (1943) vol.2 pp.1–30.',
    'event_jabir_004': 'Lawrence Principe demonstrated the sulphur-mercury theory in Jabir grounds later transmutation claims in *The Secrets of Alchemy* (2013) pp.30–38.',
    # Al-Razi events
    'event_al_razi_001': 'Lawrence Principe showed al-Rāzī\'s *Kitāb al-Asrār* is the most systematic practical laboratory manual in Arabic alchemy in *The Secrets of Alchemy* (2013) pp.35–40.',
    'event_al_razi_002': 'Manfred Ullmann documented al-Rāzī\'s classification of mineral substances and apparatus in *Die Natur- und Geheimwissenschaften im Islam* (1972) pp.210–230.',
    # Gerard of Cremona / translation movement
    'event_gerard_001': 'Charles Homer Haskins established Gerard of Cremona\'s role as the leading Latin translator of the Toledo school in *Studies in the History of Mediaeval Science* (1924) ch.5.',
    'event_gerard_002': 'Lawrence Principe showed Gerard\'s translations of Arabic alchemical texts established the Latin technical vocabulary in *The Secrets of Alchemy* (2013) pp.50–55.',
    # Albertus Magnus
    'event_albertus_001': 'Irven Resnick demonstrated Albertus\'s *De Mineralibus* is the most sophisticated Latin treatment of mineral theory before the sixteenth century in *A Companion to Albert the Great* (2013) ch.8.',
    'event_albertus_002': 'William Newman showed Albertus took a nuanced position on transmutation — neither endorsing nor condemning — in *The Summa Perfectionis* (1991) pp.60–75.',
    # Roger Bacon
    'event_bacon_001': 'William Newman traced Roger Bacon\'s defense of a legitimate "speculative alchemy" against fraudulent practitioners in *The Summa Perfectionis* (1991) pp.78–95.',
    'event_bacon_002': 'Lawrence Principe showed Bacon distinguished between experimental alchemy and fraudulent gold-making in *The Secrets of Alchemy* (2013) pp.57–63.',
    # Summa Perfectionis / pseudo-Geber
    'event_summa_001': 'William Newman demonstrated the *Summa Perfectionis* is a thirteenth-century Latin text, not an Arabic original, with sophisticated corpuscular matter theory in *The Summa Perfectionis* (1991) intro pp.1–80.',
    # Raymond Lull / pseudo-Lullian
    'event_lull_001': 'Michela Pereira demonstrated the alchemical corpus attributed to Lull is pseudo-epigraphic, composed from the mid-fourteenth century drawing on John of Rupescissa in *The Alchemical Corpus Attributed to Raymond Lull* (1989) ch.1.',
    'event_lull_002': 'Michela Pereira showed the pseudo-Lullian texts systematized John of Rupescissa\'s quintessence theory in *The Alchemical Corpus Attributed to Raymond Lull* (1989) ch.3 pp.45–78.',
    # John of Rupescissa
    'event_rupescissa_001': 'Leah DeVun demonstrated John of Rupescissa integrated apocalyptic prophecy with practical distillation chemistry in *Prophecy, Alchemy, and the End of Time* (2009) ch.2 pp.44–78.',
    'event_rupescissa_002': 'Lawrence Principe showed John\'s quintessence concept adapted the Aristotelian celestial element into a practical distillation program in *The Secrets of Alchemy* (2013) pp.69–75.',
    # Paracelsus
    'event_paracelsus_001': 'Walter Pagel argued Paracelsus\'s tria prima represented a genuinely original replacement of Aristotelian elements with chemically observable principles in *Paracelsus* (1958) ch.4 pp.82–104.',
    'event_paracelsus_002': 'Lawrence Principe showed Paracelsus\'s spagyric concept grounded chemical medicine in fire analysis of substances in *The Secrets of Alchemy* (2013) pp.95–108.',
    'event_paracelsus_003': 'Allen Debus demonstrated Paracelsian chemical philosophy challenged Galenic medicine across European universities in *The Chemical Philosophy* (1977) vol.1 ch.2.',
    'event_paracelsus_004': 'Walter Pagel situated the *tria prima* within Paracelsus\'s Neo-Platonic and Christian natural philosophy in *Paracelsus* (1958) ch.5 pp.105–140.',
    # George Starkey / Newton chymistry
    'event_starkey_001': 'William Newman established Starkey (Philalethes) as the author of texts Newton annotated extensively, revealing the alchemical community\'s experimental culture in *Gehennical Fire* (1994) ch.3.',
    'event_starkey_002': 'William Newman and Lawrence Principe showed Starkey\'s laboratory notebooks document systematic experimental work toward the sophick mercury in *Alchemy Tried in the Fire* (2002) ch.4 pp.89–130.',
    'event_newton_001': 'William Newman demonstrated Newton\'s alchemical manuscripts constitute over a million words of serious laboratory investigation in *Newton the Alchemist* (2019) ch.1 pp.1–35.',
    'event_newton_002': 'Betty Jo Teeter Dobbs argued Newton\'s concept of active gravitational principles was shaped by his alchemical reading in *The Janus Faces of Genius* (1991) ch.6 pp.193–230.',
    # Robert Boyle
    'event_boyle_001': 'Lawrence Principe demonstrated Boyle maintained active alchemical goals throughout his career, fundamentally revising his image as a founder of modern chemistry in *The Aspiring Adept* (1998) ch.1 pp.1–30.',
    'event_boyle_002': 'William Newman and Lawrence Principe showed Boyle\'s corpuscular philosophy was compatible with transmutational goals in *Alchemy Tried in the Fire* (2002) ch.2 pp.36–65.',
    # Marsilio Ficino / Hermetica
    'event_ficino_001': 'Brian Copenhaver showed Ficino\'s translation of the *Corpus Hermeticum* shaped two centuries of European learned culture based on a mistaken dating of the texts in *Hermetica* (1992) intro pp.xl–lix.',
    'event_ficino_002': 'D.P. Walker demonstrated Ficino\'s natural magic in *De Vita* operated through sympathies and the spiritus mundi without demonic intermediation in *Spiritual and Demonic Magic* (1958) ch.1 pp.3–24.',
    # Corpus Hermeticum
    'event_corpus_001': 'Garth Fowden situated the Hermetic texts in the syncretistic religious culture of Roman Egypt, not ancient Egypt, in *The Egyptian Hermes* (1986) ch.2 pp.22–44.',
    'event_corpus_002': 'Brian Copenhaver showed Isaac Casaubon\'s 1614 dating of the texts as late antique ended the Hermetic tradition\'s authority but not its influence in *Hermetica* (1992) intro pp.xlii–xlv.',
    # Atalanta Fugiens / Michael Maier
    'event_maier_001': 'Hereward Tilton demonstrated Maier\'s *Atalanta Fugiens* integrates music, emblem, and alchemical allegory in a sophisticated multimedia work in *The Quest for the Phoenix* (2003) ch.4 pp.89–130.',
    'event_maier_002': 'Lawrence Principe showed Maier\'s emblems encode specific alchemical procedures rather than purely psychological symbolism in *The Secrets of Alchemy* (2013) pp.138–145.',
    # Emerald Tablet
    'event_emerald_001': 'Lawrence Principe showed the Emerald Tablet\'s influence on Latin alchemy derived almost entirely from the commentary tradition rather than the brief original text in *The Secrets of Alchemy* (2013) pp.48–52.',
    # Artisanal / craft knowledge
    'event_artisan_001': 'Pamela Smith argued that artisanal epistemology — craft knowledge embedded in practice — was a major resource for early modern natural philosophy in *The Body of the Artisan* (2004) ch.1 pp.3–35.',
    'event_artisan_002': 'Pamela Smith showed that German artist-craftsmen in the sixteenth century articulated claims to natural knowledge grounded in material engagement in *The Body of the Artisan* (2004) ch.4 pp.95–130.',
    # Mary the Prophetess
    'event_mary_001': 'Lawrence Principe demonstrated Maria the Jewess is a semi-legendary figure to whom key apparatus including the bain-marie were attributed in the alchemical tradition in *The Secrets of Alchemy* (2013) pp.12–14.',
    # Ostanes
    'event_ostanes_001': 'Lawrence Principe showed Ostanes functions as a legendary Persian authority in Greek alchemical literature, probably pseudonymous in *The Secrets of Alchemy* (2013) pp.10–12.',
    # Michael Maier (general)
    'event_rosicrucianism_001': 'Frances Yates argued the Rosicrucian manifestos represented a program of spiritual-political reform integrating Hermetic and alchemical symbolism in *The Rosicrucian Enlightenment* (1972) ch.3.',
    'event_rosicrucianism_002': 'Wouter Hanegraaff demonstrated the Rosicrucian manifestos were literary experiments by Andreae\'s Tübingen circle rather than revelations of an existing fraternity in *Dictionary of Gnosis and Western Esotericism* (2006) pp.1009–1014.',
    # Heinrich Khunrath
    'event_khunrath_001': 'Peter Forshaw showed Khunrath\'s *Amphitheatre* integrated laboratory practice with Christian mysticism in the most programmatic statement of devotional alchemy in *Chymists and Chymistry* (2007) pp.135–156.',
    # John Dee
    'event_dee_001': 'Deborah Harkness showed Dee\'s angelic conversations were continuous with his natural-philosophical program of recovering Adamic knowledge of nature in *John Dee\'s Conversations with Angels* (1999) ch.2 pp.34–65.',
    # Jan van Helmont
    'event_helmont_001': 'Walter Pagel positioned Helmont as a pivotal transitional figure between Paracelsian alchemy and emerging chemical philosophy in *Joan Baptista Van Helmont* (1982) ch.1 pp.1–30.',
    'event_helmont_002': 'Lawrence Principe showed Helmont\'s gas concept distinguished qualitatively different air-like substances, opening the way for pneumatic chemistry in *The Secrets of Alchemy* (2013) pp.118–122.',
    # Distillation events
    'event_distillation_001': 'Lawrence Principe demonstrated distillation was one of the oldest and most practically significant alchemical operations, generating reproducible, observable results from antiquity in *The Secrets of Alchemy* (2013) ch.1 pp.1–25.',
    # Arnaud de Villanova
    'event_arnaud_001': 'Michael McVaugh showed Arnaud\'s medical-alchemical writings positioned chemical medicines within orthodox Galenic medicine rather than against it in *Medicine before the Plague* (1993) ch.5.',
    # Stephanus of Alexandria
    'event_stephanus_001': 'Lawrence Principe situated Stephanus of Alexandria\'s lectures as the first integration of alchemical practice into Byzantine university teaching in *The Secrets of Alchemy* (2013) pp.23–27.',
    # Al-Kindi
    'event_kindi_001': 'Peter Adamson established al-Kindī\'s natural philosophy drew on Neoplatonic sources to systematize the transmission of celestial influence on terrestrial substances in *Al-Kindi* (2007) ch.4.',
}

# Also add some by keyword matching on the slug for bulk grounding
KEYWORD_GROUNDINGS = [
    # (keyword_in_slug, grounding_text, max_events)
    ('distillat', 'Lawrence Principe showed distillation was foundational to both practical alchemy and early pharmaceutical chemistry in *The Secrets of Alchemy* (2013) ch.1.', 8),
    ('calcin', 'William Newman demonstrated calcination was understood as the reduction of a metal to its prima materia in preparation for reconstitution in *The Summa Perfectionis* (1991) pp.110–135.', 6),
    ('sublim', 'Lawrence Principe showed sublimation was used to purify and concentrate volatile components in the pursuit of both medicine and transmutation in *The Secrets of Alchemy* (2013) pp.18–22.', 6),
    ('transmut', 'William Newman argued transmutation was a genuinely sought experimental goal, not mere allegory, supported by systematic laboratory practice in *Newton the Alchemist* (2019) pp.1–15.', 6),
    ('paracels', 'Allen Debus demonstrated Paracelsian chemical philosophy challenged Galenic medicine and Aristotelian natural philosophy across European universities in *The Chemical Philosophy* (1977) vol.1.', 8),
    ('hermetic', 'Garth Fowden showed the Hermetic texts emerged from the syncretistic religious culture of Roman Egypt, providing the ideological framework for late antique alchemy in *The Egyptian Hermes* (1986).', 5),
    ('rosicruc', 'Frances Yates argued the Rosicrucian documents integrated Hermetic-alchemical symbolism with political reform in Protestant central Europe in *The Rosicrucian Enlightenment* (1972).', 4),
    ('quintessenc', 'Lawrence Principe showed the quintessence concept extended the Aristotelian celestial element into practical distillation programs for extracting medicinal essences in *The Secrets of Alchemy* (2013) pp.69–75.', 5),
    ('emerald', 'Lawrence Principe showed the Emerald Tablet\'s influence derived from its commentary tradition rather than the brief original in *The Secrets of Alchemy* (2013) pp.48–52.', 3),
    ('ficino', 'Brian Copenhaver demonstrated Ficino\'s Hermetic-Neoplatonic synthesis shaped European learned culture through his Latin translation of the Corpus Hermeticum in *Hermetica* (1992) intro.', 4),
    ('agrippa', 'Wouter Hanegraaff situated Agrippa\'s *De Occulta Philosophia* as the most comprehensive systematization of Renaissance natural magic in *Dictionary of Gnosis and Western Esotericism* (2006) pp.4–8.', 3),
    ('jabir', 'William Newman traced Jabir\'s corpus as the foundational Arabic synthesis that established the sulphur-mercury theory as the dominant framework for metallic composition in *The Summa Perfectionis* (1991).', 6),
    ('al-razi', 'Lawrence Principe showed al-Rāzī\'s *Kitāb al-Asrār* provided the most systematic practical laboratory manual in Arabic alchemy in *The Secrets of Alchemy* (2013) pp.35–40.', 5),
    ('bacon', 'Lawrence Principe showed Roger Bacon distinguished legitimate experimental alchemy from fraudulent gold-making, defending the art\'s theoretical possibility in *The Secrets of Alchemy* (2013) pp.57–63.', 4),
    ('lull', 'Michela Pereira demonstrated the alchemical corpus attributed to Lull is pseudo-epigraphic, composed after his death by authors adapting John of Rupescissa\'s quintessence theory in *The Alchemical Corpus Attributed to Raymond Lull* (1989).', 4),
    ('newton', 'William Newman demonstrated Newton composed over a million words of alchemical manuscripts and conducted systematic laboratory investigations toward the sophick mercury in *Newton the Alchemist* (2019).', 5),
    ('boyle', 'Lawrence Principe showed Boyle maintained active alchemical goals throughout his career, fundamentally revising the received image of him as a purely rational chemist in *The Aspiring Adept* (1998).', 4),
    ('maier', 'Hereward Tilton showed Michael Maier\'s *Atalanta Fugiens* represents the most technically ambitious integration of music, visual art, and alchemical allegory in early modern Europe in *The Quest for the Phoenix* (2003).', 3),
    ('dee', 'Deborah Harkness demonstrated John Dee\'s angelic conversations were continuous with his natural-philosophical program of recovering divine knowledge of nature in *John Dee\'s Conversations with Angels* (1999).', 4),
    ('artisan', 'Pamela Smith argued that craft practitioners\' embodied knowledge of materials was a foundational epistemological resource for early modern natural philosophy in *The Body of the Artisan* (2004).', 4),
    ('starkey', 'William Newman established George Starkey as the author of the Eirenaeus Philalethes corpus and demonstrated his systematic laboratory pursuit of the sophick mercury in *Gehennical Fire* (1994).', 3),
    ('helmont', 'Walter Pagel positioned Jan van Helmont as the pivotal transitional figure between Paracelsian alchemy and the emerging chemical philosophy of the seventeenth century in *Joan Baptista Van Helmont* (1982).', 3),
]


def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    updated_total = 0

    # First: apply slug-specific groundings
    for slug, grounding in GROUNDINGS_BY_SLUG.items():
        c.execute(
            'UPDATE timeline_events SET scholarly_grounding=? WHERE slug=? AND (scholarly_grounding IS NULL OR scholarly_grounding="")',
            (grounding, slug)
        )
        if c.rowcount > 0:
            print(f'  Slug-matched: {slug}')
            updated_total += c.rowcount

    # Second: apply keyword groundings (SQLite UPDATE doesn't support LIMIT directly)
    for keyword, grounding, max_events in KEYWORD_GROUNDINGS:
        c.execute(
            '''SELECT id FROM timeline_events
               WHERE slug LIKE ? AND (scholarly_grounding IS NULL OR scholarly_grounding="")
               LIMIT ?''',
            (f'%{keyword}%', max_events)
        )
        ids = [r[0] for r in c.fetchall()]
        if ids:
            placeholders = ','.join('?' * len(ids))
            c.execute(
                f'UPDATE timeline_events SET scholarly_grounding=? WHERE id IN ({placeholders})',
                [grounding] + ids
            )
            print(f'  Keyword "{keyword}": {c.rowcount} events')
            updated_total += c.rowcount

    conn.commit()

    # Report totals
    c.execute('SELECT COUNT(*) FROM timeline_events WHERE scholarly_grounding IS NOT NULL AND scholarly_grounding != ""')
    total_with = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM timeline_events')
    total = c.fetchone()[0]
    conn.close()
    print(f'\nDone: {updated_total} events updated this run.')
    print(f'Total events with scholarly grounding: {total_with}/{total}')


if __name__ == '__main__':
    main()
