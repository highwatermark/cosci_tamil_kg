"""Nilai v4: the 13 chapters, "a walk through the graph". Writes site/nilai/v4/chapters.json.

Run:  python3 -I site/nilai/v4/chapters_curate.py

THE GRAPH IS THE SCRIPT. This file holds only the curator's choices: which three verses, which lines of each to
show, which two sound links join them, the object each verse names, and the one imagined beat. Every Tamil line,
reading, uncertain flag and link text is copied here from the graph at run time, verbatim, so nothing in
chapters.json is retyped. Check the result with validate_chapters.py.

Stdlib only.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
KG = REPO / 'kg'


def jsonl(p):
    with open(p, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


# ---------------------------------------------------------------------------------------------------------
# Graph access
# ---------------------------------------------------------------------------------------------------------
INDEX = json.load(open(KG / 'groups' / 'index.json', encoding='utf-8'))
NODE_FILES = {}
for g, v in INDEX.items():
    if v.get('nodes'):
        NODE_FILES[REPO / v['nodes']] = g
    for b, p in (v.get('kept_graphs') or {}).items():
        NODE_FILES[REPO / p / 'nodes.jsonl'] = g
_nodes = {}


def node(vid):
    if not _nodes:
        for f, g in NODE_FILES.items():
            for d in jsonl(f):
                if d.get('type') == 'Verse' and d['id'] not in _nodes:
                    d = dict(d)
                    d['_group'] = g
                    d['_file'] = str(f.relative_to(REPO))
                    _nodes[d['id']] = d
            for e in jsonl(f.parent / 'edges.jsonl'):
                if e['p'] == 'EXPRESSES' and e['s'] in _nodes and _nodes[e['s']]['_file'] == str(f.relative_to(REPO)):
                    _nodes[e['s']].setdefault('_concepts', []).append(e['o'].replace('concept:', ''))
    return _nodes[vid]


BRIDGES = list(jsonl(KG / 'groups' / 'bridges.jsonl'))
AUDIT = json.load(open(KG / 'groups' / 'all_link_audit.json', encoding='utf-8'))['links']


def group_edge(s, o, typ):
    for f in NODE_FILES:
        for e in jsonl(f.parent / 'edges.jsonl'):
            if e['s'] == s and e['o'] == o and e['p'].lower() == typ:
                return e, str((f.parent / 'edges.jsonl').relative_to(REPO))
    return None, None


def link(a, b):
    """The sound link between verses a and b, in either recorded direction."""
    for x in BRIDGES:
        if {x['s'], x['o']} == {a, b} and x['grade'] == 'sound':
            return {'s': x['s'], 'o': x['o'], 'type': x['type'], 'grade': x['grade'], 'teaches': x.get('teaches'),
                    'teaches_holds': x.get('teaches_holds'), 'note': x.get('note'), 'source_file': 'kg/groups/bridges.jsonl',
                    'marked_by': x.get('source')}
    for x in AUDIT:
        if {x['a'], x['b']} == {a, b} and x['grade'] == 'sound':
            e, ef = group_edge(x['a'], x['b'], x['type'])
            return {'s': x['a'], 'o': x['b'], 'type': x['type'], 'grade': x['grade'], 'teaches': (e or {}).get('teaches'),
                    'teaches_holds': x.get('teaches_holds'), 'note': (e or {}).get('note'),
                    'source_file': 'kg/groups/all_link_audit.json (text: %s)' % ef, 'marked_by': (e or {}).get('source')}
    raise SystemExit('no sound link between %s and %s' % (a, b))


# ---------------------------------------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------------------------------------
BOOK = {  # id -> (Tamil, English)
    'kural': ('திருக்குறள்', 'Tirukkural'), 'naladiyar': ('நாலடியார்', 'Naladiyar'),
    'purananuru': ('புறநானூறு', 'Purananuru'), 'akananuru': ('அகநானூறு', 'Akananuru'),
    'kalittokai': ('கலித்தொகை', 'Kalittokai'), 'paripadal': ('பரிபாடல்', 'Paripadal'),
    'thinaimalai_nootraimpathu': ('திணைமாலை நூற்றைம்பது', 'Thinaimalai Nootraimpathu'),
    'neelakesi': ('நீலகேசி', 'Neelakesi'), 'civaka_cintamani': ('சீவக சிந்தாமணி', 'Civaka Cintamani'),
    'siddhar': ('சித்தர் பாடல்கள்', 'Siddhar songs'), 'thiruppugazh': ('திருப்புகழ்', 'Thiruppugazh'),
    'tirumanthiram': ('திருமந்திரம்', 'Tirumanthiram'), 'manimekalai': ('மணிமேகலை', 'Manimekalai'),
    'silappathikaram': ('சிலப்பதிகாரம்', 'Silappathikaram'), 'sirupanchamoolam': ('சிறுபஞ்சமூலம்', 'Sirupanchamoolam'),
    'pattupattu': ('பத்துப்பாட்டு', 'Pattuppattu'),
}
PATTU = {6: ('மதுரைக்காஞ்சி', 'Maduraikkanchi')}


def core_siddhar(seq):
    for d in jsonl(KG / 'core' / 'siddhar.jsonl'):
        if d.get('seq') == seq:
            return d


def label(vid):
    n = node(vid)
    book = vid.split(':')[0]
    ta, en = BOOK[book]
    if book == 'siddhar':
        c = core_siddhar(int(vid.split(':')[1]))
        return ('%s %s · %s' % (c['work_title'], c['number'], c['siddhar']),
                '%s %s, %s (siddhar:%s)' % (en, c['number'], c['work_title'], vid.split(':')[1]))
    if book == 'pattupattu':
        num = int(vid.split(':')[1])
        pta, pen = PATTU[num]
        return ('%s %d–%d' % (pta, n['start'], n['end']), '%s (Pattuppattu %d), lines %d–%d' % (pen, num, n['start'], n['end']))
    if book in ('manimekalai', 'silappathikaram') or (book == 'paripadal' and n.get('whole') is False):
        sec = n.get('section') or ''
        return ('%s %s · %s %d–%d' % (ta, vid.split(':')[1], sec, n['start'], n['end']),
                '%s %s, lines %d–%d' % (en, vid.split(':')[1], n['start'], n['end']))
    num = vid.split(':')[1]
    return ('%s %s' % (ta, num), '%s %s' % (en, num))


# ---------------------------------------------------------------------------------------------------------
# Image prompts (marble / bronze / stone gallery on flat #00FF00, as the v3 batches after the style change)
# ---------------------------------------------------------------------------------------------------------
STYLE = ('Museum-quality sculptural rendering. Objects rendered in their true materials (bronze, brass, copper, stone, '
         'palm leaf, glass) with sculptural depth and fine detail; any figure is carved luminous white Carrara marble '
         'accented with Chola panchaloha bronze and restrained gold leaf. Soft directional gallery light from the upper '
         'left, deep gentle shadows, physically accurate reflections, a single soft contact shadow. Elegant, timeless, '
         'refined modern minimalism. Single subject, centred, whole and uncropped, filling about 80% of the frame, on a '
         'flat solid pure chroma green #00FF00 background. No scenery, no plinth unless asked, no text, no letters, no '
         'watermark. Neutral, untinted white gallery light: the marble stays pure white and the metals keep their true '
         'warm colour, with no green cast or green reflections from the background. Square 1:1 image with clear flat '
         'green on all four sides.')
NEW = {  # id -> subject line (the full prompt is subject + STYLE)
    'V4-parasol': 'A royal parasol of a Tamil king: a tall domed parasol of white silk stretched over fine ivory ribs, '
                  'a narrow gold-leaf rim and a small lotus-bud finial, on a long carved bronze staff with ring mouldings, '
                  'standing upright and open, seen from slightly below.',
    'V4-raincloud': 'A single rain cloud carved in softly polished white marble, rounded and heavy, with straight thin '
                    'threads of polished bronze falling from its underside as rain, the threads ending in a clean line.',
    'V4-canopy': 'A slender future shade canopy: one tall polished bronze mast carrying a wide, shallow dome of thin '
                 'translucent panels like overlapping leaves of pale glass edged in gold, open, casting a soft round shadow.',
    'V4-bamboo-flute': 'Three tall stalks of bamboo cast in warm bronze, rising from one clump, with a row of round '
                       'holes bored along the middle stalk where the wind plays it like a flute; a faint carved swirl '
                       'of marble wind curling past the holes.',
    'V4-peacock': 'A peacock sculpted in Chola panchaloha bronze with gold-leaf eyes on its feathers, standing and '
                  'dancing, its tail raised and spread in a full half-circle behind it like a hand fan held overhead.',
    'V4-lightyazh': 'A future yazh, the arched Tamil harp: the same long boat-shaped sound box and curved neck, made of '
                    'white marble and brass, its strings replaced by fine taut threads of warm light.',
    'V4-wave': 'One great sea wave sculpted in polished white marble with fine veining, curling over at its crest, '
               'its foam carved as small gilded beads; a freestanding wave, no water around it.',
    'V4-shuttle': "A weaver's boat-shaped wooden shuttle with brass caps, holding a small bobbin wound with very fine "
                  'cotton thread; the thread runs out of it in a loose spiral as if the bobbin is whirling.',
    'V4-raft': 'A small raft (puṇai) of five straight logs lashed side by side with crossed coir rope, the wood dark and '
               'water-polished, seen at a three-quarter angle from above, empty, afloat on nothing.',
    'V4-misthill': 'A small hill sculpted in grey granite, its upper slope wrapped in a thin drifting veil of mist '
                   'carved in translucent white marble that is already thinning and breaking away at one edge.',
    'V4-lock': 'An old Tamil padlock in dark bronze, shaped like a small temple lamp, hanging from a frame of fine taut '
               'strings like a puppet\'s control bar, as if the body were a string-worked contraption shut with a lock.',
    'V4-bionic-hand': 'A future hand: a slim prosthetic hand of white marble and polished bronze, open, its joints '
                      'showing fine gold cables like tendons where the strings of the old contraption have been rewoven.',
    'V4-floating-pot': 'A round unglazed terracotta pot, laterite red, bobbing tilted on a flat disc of rippled clear '
                       'glass that stands for water, a little water spilling from its mouth.',
    'V4-breath': 'The breath: a classical marble head in profile facing right, lips closed, with two thin ribbons of '
                 'polished brass air drawn in at both nostrils and curling back out in a slow loop before the face.',
    'V4-breathing-machine': 'A future breathing machine as a refined object: a small pleated bellows of pale glass and '
                            'bronze between two marble plates, with a single slim tube rising from it, at rest.',
    'V4-rain-basin': 'A future water tank: a terraced basin of pale granite and clear glass that catches rain, still '
                     'dark water inside, a planted earth bund along one side and a small bronze sluice.',
    'V4-bellows': "A village smith's bellows: a leather bag between two carved wooden boards with bronze handles, and "
                  'a short clay nozzle, half breathed out, as at a forge.',
    'V4-cup': 'A small shallow clay cup tilted and pouring a thin stream of pale palm toddy, a twist of strained fibre '
              'resting on its rim, and one long peacock feather lying beside it.',
    'V4-herostone': 'A Tamil hero stone (naṭukal): an upright slab of dark granite set in a low cairn of rough pebbles, '
                    'the warrior\'s name freshly cut across it in a single band of incised marks, crowned with a red '
                    'flower garland bound with split fibre and a fan of peacock feathers.',
    'V4-herostone-worn': 'The same kind of hero stone generations later: an upright slab of dark granite worn smooth and '
                         'leaning, lichen in its cracks, the band of incised letters across it eroded to faint shallow '
                         'marks no one could read, no garland.',
    'V4-staff': 'A long old walking staff of dark polished wood with a bronze ring (toṭi) fitted at its head and a worn '
                'iron ferrule at its foot, standing upright as if leaned on by a trembling hand that is not shown.',
    'V4-seawater': 'A shallow bronze bowl holding sea water rendered as clear rippled glass, a skin of white froth '
                   'carved in marble being skimmed from its surface onto the rim.',
    'V4-exo-brace': 'A future walking aid: a slim exoskeleton brace for one leg in polished bronze and white marble, '
                    'its knee joint a fine gilded hinge, standing upright on its own.',
}
ASSET = {  # existing images in site/nilai/assets/web/<id>.webp, as flow_log.md and the v3 shot list describe them
    '02-T': 'hand-held tharasu, a brass two-pan balance', '02-N': 'laboratory analytical balance',
    '09-U': 'small palm-leaf umbrella on a bamboo stick', '21-T': 'yazh, the ancient Tamil arched harp',
    '26-F': 'solar sail spacecraft of beaten gold foil', '24-T': 'parisal, a round river coracle with a paddle',
    '04-F1': 'empty terracotta pot with one long crack', '31-T': 'kuthuvilakku, the bronze standing oil lamp',
    '31-N': 'early glass light bulb, unlit', '18-T': 'dark granite standing stone with a marigold garland',
    'V4-pillar': 'stone pillar with a guardian goddess in relief', 'V4-shrine': 'small stone shrine',
    'V4-speaker': 'speaker (the voice without a body)', 'V4-hands': 'many raised marble hands',
    '04-F2': 'ēri tank with an earth bund and palmyra palms', '04-F3': 'granite temple tank with steps on four sides',
    '07-E': 'empty banana leaf', '07-F': 'open server-rack frame laid long and low like a dining row',
    '31-F1': 'small sculpted sun, a sphere of polished gold', '01-T': 'palm-leaf manuscript bundle, closed',
    '01-F': 'one long palm leaf, gold-edged and lit from within', '10-H': 'pond heron in profile',
    '26-T': 'sewn-plank trading ship (nāvāy)', '03-N': 'black-glass monolith in a brass bezel, blank face',
}


def img(key):
    if key in ASSET:
        return {'asset': key, 'asset_file': 'site/nilai/assets/web/%s.webp' % key, 'asset_is': ASSET[key]}
    return {'asset': None, 'new_image': key, 'prompt': NEW[key] + ' ' + STYLE}


# ---------------------------------------------------------------------------------------------------------
# The 13 chapters. Each verse: (id, lines to show or None for all, object named, image key, note on the image).
# Each chapter's links are given in walk order as verse-index pairs.
# ---------------------------------------------------------------------------------------------------------
CHAPTERS = [
    {'id': 'aram', 'accent': '#7a2e1d', 'subtitle': 'the balance that levels itself',
     'verses': [
         ('purananuru:6', [8, 9, 10], 'the beam of a balance (தெரிகோல் ஞமன்)', '02-T', None),
         ('pattupattu:6:489-506', [489, 490, 491, 492], 'the beam of a balance (ஞெமன்கோல்), the court likened to it', '02-T', None),
         ('kural:118', None, 'the balance that first levels itself, then weighs (சமன்செய்து சீர்தூக்குங் கோல்)', '02-T', None)],
     'links': [(1, 0), (1, 2)],
     'forward': ('The balance passed from a king’s person to a court, and the Kural asked it to level itself before it weighs. '
                 'In 2526 machines do the weighing; we ask who levels them first.'),
     'then': '02-T', 'future': '02-N', 'transform': 'the brass tharasu becomes the sealed laboratory balance'},
    {'id': 'porul', 'accent': '#6a4e00', 'subtitle': 'the parasol, and who falls outside its shade',
     'verses': [
         ('purananuru:35', [19, 20, 21], 'the king’s tall parasol (வியன்குடை)', 'V4-parasol', None),
         ('kalittokai:99', [8, 9, 10], 'the king’s parasol held as the shade of virtue (ஆய் குடை)', 'V4-parasol', None),
         ('kural:559', None, 'the rain the sky withholds (வானம் பெயல்)', 'V4-raincloud', None)],
     'links': [(0, 1), (1, 2)],
     'forward': ('The parasol was raised to shade those who suffer, and a friend asked who had fallen outside it. '
                 'In 2526 we ask it of every system raised over people: whom does its shade miss?'),
     'then': 'V4-parasol', 'future': 'V4-canopy', 'transform': 'the royal parasol becomes a wide canopy of glass leaves'},
    {'id': 'inbam', 'accent': '#8a1f4e', 'subtitle': 'the hill that played every instrument',
     'verses': [
         ('akananuru:82', [1, 2, 3, 4], 'wind in bored bamboo as the flute (ஆடுஅமைக் குயின்ற அவிர்துளை)', 'V4-bamboo-flute', None),
         ('paripadal:21:30-38', [30, 31, 32, 35], 'the dancing peacock with its tail spread like a fan (மஞ்ஞை, சாந்தாற்றி)', 'V4-peacock', None),
         ('thinaimalai_nootraimpathu:111', None, 'the bees as the yazh (வண்டு யாழாக)', '21-T', None)],
     'links': [(1, 0), (0, 2)],
     'forward': ('The hill played every instrument, and the woman alone could not bear the music. '
                 'In 2526 any sound can be made to order; we ask what still reaches a heart left alone.'),
     'then': '21-T', 'future': 'V4-lightyazh', 'transform': 'the yazh keeps its shape; its strings become threads of light'},
    {'id': 'veedu', 'accent': '#2f4a6b', 'subtitle': 'the raft across the sea of deeds',
     'verses': [
         ('kural:10', None, 'the great sea of births (பிறவிப் பெருங்கடல்)', 'V4-wave', None),
         ('civaka_cintamani:3019', None, 'thread whirling in a weaver’s shuttle (நுண்ணூல் நாழிகை)', 'V4-shuttle', None),
         ('neelakesi:155', None, 'the raft that is hard to find (போதரும் புணை)', 'V4-raft', None)],
     'links': [(1, 0), (2, 0)],
     'forward': ('The sea was made of the swimmer’s own deeds, and the Lord’s part was to build the raft. '
                 'In 2526 we build the craft for a darker sea; we ask whether we still swim, or only ride.'),
     'then': 'V4-raft', 'future': '26-F', 'transform': 'the lashed raft becomes the gold solar sail'},
    {'id': 'udal', 'accent': '#7a3b10', 'subtitle': 'the boat, the mist and the lock',
     'verses': [
         ('siddhar:987', None, 'the boat (ஓடம்) and its pole (கோல்)', '24-T',
          'the verse names a boat (ஓடம்) poled across water; 24-T is a round river coracle, the nearest boat we have'),
         ('naladiyar:28', None, 'mist moving on a hill (மலையாடு மஞ்சு)', 'V4-misthill', None),
         ('thiruppugazh:548', [1, 2, 3], 'a string-worked contraption and a lock (சூத்திரம், பூட்டு)', 'V4-lock', None)],
     'links': [(0, 1), (2, 1)],
     'forward': ('The body was a boat to use while it lasted, a mist on a hill, a string-worked thing shut with a lock. '
                 'In 2526 medicine can mend the boat and rework the strings; we ask what the voyage is for.'),
     'then': 'V4-lock', 'future': 'V4-bionic-hand', 'transform': 'the lock on its strings becomes a hand whose strings are gold tendons'},
    {'id': 'ullam', 'accent': '#4b3b78', 'subtitle': 'from the tossed pot to the lit temple',
     'verses': [
         ('siddhar:1166', None, 'a clay pot bobbing on the water (பொய்க்குடம்)', 'V4-floating-pot', None),
         ('naladiyar:47', None, 'a pot seeping from nine openings (கும்பம்)', '04-F1', None),
         ('tirumanthiram:1823', None, 'the temple, its tower gate, and the bright lamps (கோயில், கோபுரவாசல், மணிவிளக்கு)', '31-T', None)],
     'links': [(0, 1), (2, 1)],
     'forward': ('One body was a pot tossed on water, a pot that seeps, and a temple whose five thieving senses become lamps. '
                 'In 2526 we can light the mind from outside; we ask whether it still learns to light itself.'),
     'then': '31-T', 'future': '31-N', 'transform': 'the bronze lamp becomes the glass bulb lit from elsewhere'},
    {'id': 'irai', 'accent': '#6c4605', 'subtitle': 'the stone that speaks',
     'verses': [
         ('siddhar:1458', None, 'the planted stone (நட்டகல்)', '18-T', None),
         ('manimekalai:21:112-129', [115, 116, 127, 128], 'stone and the painted figure, which do not speak, and the deity that never leaves its place (கல்லும் எழுதிய பாவையும், தெய்வதம்)', 'V4-pillar',
          'the prototype shows 115–116 and 125–128 on wide screens; at most four lines are listed here, the four it shows on a phone'),
         ('civaka_cintamani:2058', None, 'the god in its shrine, whose mouth seemed to speak (தெய்வந் தான்வாய் விட்டுரைத்திட்டது)', 'V4-shrine', None)],
     'links': [(1, 0), (2, 0)],
     'forward': 'The stones learned to speak. In 2526 we ask the epic’s question: who stands behind the voice?',
     'then': '18-T', 'future': 'V4-speaker', 'transform': 'the planted stone becomes the speaker; the many hands rise before it (V4-hands)'},
    {'id': 'yogam', 'accent': '#1f5b57', 'subtitle': 'the breath that kicks Death away',
     'verses': [
         ('tirumanthiram:571', None, 'the breath drawn in and let out through both nostrils (இருகாலும் பூரிக்குங் காற்று)', 'V4-breath', None),
         ('kural:269', None, None, 'V4-breath',
          'COMPROMISE: the couplet names no concrete object, only Death (கூற்றம்) and the leap past it; the breath image carries over from verse 1'),
         ('siddhar:1119', None, 'the one who runs out and runs back, the breath (ஓடிஓடி மீளுவான்)', 'V4-breath', None)],
     'links': [(0, 1), (2, 1)],
     'forward': ('The measured breath was said to kick Death away, and the runner within to settle. '
                 'In 2526 machines can breathe for us; we ask what the held breath still teaches.'),
     'then': 'V4-breath', 'future': 'V4-breathing-machine', 'transform': 'the brass ribbon of breath becomes a glass bellows at rest'},
    {'id': 'iyarkai', 'accent': '#2f5d1f', 'subtitle': 'the tank, the well and the gift of food',
     'verses': [
         ('purananuru:18', [18, 19, 28, 29], 'the water body bound where the land dips (நிலன்நெளி மருங்கின் நீர்நிலை)', '04-F2', None),
         ('sirupanchamoolam:65', None, 'the tank and its bank, and the shared well (குளம், கோடு, கிணறு)', '04-F3', None),
         ('manimekalai:11:76-98', [76, 77, 95, 96], 'the great raft of learning that hunger makes one drop (கல்விப் பெரும் புணை)', 'V4-raft', None)],
     'links': [(1, 0), (2, 0)],
     'forward': ('The tank a king was told to dig became a merit for any man of means, then a renunciant’s gift of food. '
                 'In 2526, with rain less certain, we ask who will bind the water now.'),
     'then': '04-F2', 'future': 'V4-rain-basin', 'transform': 'the earth-bunded ēri becomes a terraced basin of stone and glass'},
    {'id': 'samugam', 'accent': '#6b2c63', 'subtitle': 'the widow’s leaf and the sun',
     'verses': [
         ('purananuru:246', [6, 7, 8, 9], 'the leaf-wrapped rice ball and the bed of pebbles (அடை, பிண்டம், பரற்பெய் பள்ளி)', '07-E',
          'அடை is a leaf; 07-E is an empty banana leaf'),
         ('manimekalai:2:42-57', [42, 43, 44, 45], 'the smith’s bellows (ஊது உலைக் குருகு)', 'V4-bellows', None),
         ('silappathikaram:18:34-53', [50, 51, 52, 53], 'the blazing sun Kannaki questions (காய்கதிர்ச் செல்வன்)', '31-F1', None)],
     'links': [(1, 0), (2, 0)],
     'forward': ('A widow was told what to eat, where to sleep and when to burn, and Kannaki turned and asked the sun. '
                 'In 2526 we ask who still writes the rules for another person’s life.'),
     'then': '07-E', 'future': '07-F', 'transform': 'the leaf in its row becomes the rack where rules now run'},
    {'id': 'aivu', 'accent': '#1d4f7a', 'subtitle': 'the bird that drinks the milk and leaves the water',
     'verses': [
         ('thiruppugazh:70', [5, 6, 7, 8], 'endless crores of books (நூல் அனந்த கோடி)', '01-T', None),
         ('naladiyar:135', None, 'the bird that drinks the milk and leaves the water (நீரொழியப் பாலுண் குருகு)', '10-H',
          'குருகு is a heron or crane; 10-H is a pond heron (no milk bowl in the image)'),
         ('tirumanthiram:2720', None, 'the precious vessel that reaches the farther shore (அங்கரை சேர்ந்த அருங்கலம்)', '26-T', None)],
     'links': [(0, 1), (2, 1)],
     'forward': ('Learning has no shore and our days are few, so the wise drank the milk and left the water. '
                 'In 2526 all learning is on tap; we ask who teaches the choosing.'),
     'then': '01-T', 'future': '01-F', 'transform': 'the bundle of endless leaves becomes the one leaf lit from within'},
    {'id': 'pulamai', 'accent': '#5e4a12', 'subtitle': 'the name cut in stone',
     'verses': [
         ('purananuru:232', [3, 4, 5, 6], 'the hero stone crowned with a peacock feather, toddy poured from a small cup (நடுகல், பீலி, சிறுகலம்)', 'V4-cup', None),
         ('purananuru:264', [1, 2, 3, 4], 'the stone set up with his name carved on it (பெயர்பொறித்து நட்டனரே கல்)', 'V4-herostone', None),
         ('akananuru:297', [7, 8, 9, 10], 'the old hero stone with its worn inscription (பேஎம் முதிர் நடுகல், குயில் எழுத்து)', 'V4-herostone-worn', None)],
     'links': [(1, 0), (2, 1)],
     'forward': ('Names were cut in stone so the bards would know, and a later road walked past the worn letters unread. '
                 'In 2526 everything is written down; we ask who will stop to read it.'),
     'then': 'V4-herostone-worn', 'future': '03-N', 'transform': 'the worn hero stone becomes the blank glass monolith'},
    {'id': 'kaalam', 'accent': '#45484d', 'subtitle': 'the staff that comes to every youth',
     'verses': [
         ('purananuru:243', [11, 12, 13, 14], 'the ringed staff leaned on (தொடித்தலை விழுத்தண்டு)', 'V4-staff', None),
         ('naladiyar:11', None, 'the staff one rises on (கோல்)', 'V4-staff', None),
         ('tirumanthiram:848', None, 'the salt water of the shore, skimmed of its froth (கானல் உவரி, நுரை)', 'V4-seawater', None)],
     'links': [(0, 1), (2, 1)],
     'forward': ('The staff came to every youth, and one verse said a skimmed sea water could turn the grey back. '
                 'In 2526 we can hold the staff off for decades; we ask who gets the long years, and what they are for.'),
     'then': 'V4-staff', 'future': 'V4-exo-brace', 'transform': 'the ringed staff becomes a light bronze brace'},
]

CATS = {c['id']: c for c in json.load(open(KG / 'themes' / 'concept_categories.json', encoding='utf-8'))['categories']}


def lines_of(vid, pick):
    n = node(vid)
    tam = n['tamil']
    start = n.get('start') or 1
    nums = list(range(start, start + len(tam))) if pick is None else pick
    if len(nums) > 4:
        raise SystemExit('%s: more than 4 lines' % vid)
    return [{'n': k, 'ta': tam[k - start]} for k in nums]


def build():
    out = {'about': ('Nilai v4, a walk through the graph: 13 chapters, one per concept category. Each walks three corpus '
                     'verses joined by two graded sound links and ends in one beat labelled imagined. Tamil lines, '
                     'readings, flags and link texts are copied verbatim from kg/ by chapters_curate.py; '
                     'validate_chapters.py checks them.'),
           'chapters': []}
    for ch in CHAPTERS:
        cat = CATS[ch['id']]
        verses = []
        for (vid, pick, obj, key, imgnote) in ch['verses']:
            n = node(vid)
            lta, len_ = label(vid)
            v = {'id': vid, 'book': n.get('book') or vid.split(':')[0], 'group': n['_group'],
                 'label_ta': lta, 'label': len_, 'lines': lines_of(vid, pick),
                 'lines_shown_of': [n.get('start') or 1, (n.get('start') or 1) + len(n['tamil']) - 1],
                 'reading': n['reading'], 'uncertain': bool(n.get('uncertain')),
                 'concepts': n.get('_concepts'), 'object': obj}
            v.update(img(key))
            if imgnote:
                v['image_note'] = imgnote
            verses.append(v)
        links = []
        for (i, j) in ch['links']:
            a, b = verses[i]['id'], verses[j]['id']
            L = link(a, b)
            use_teaches = bool(L['teaches']) and L['teaches_holds'] is True
            sym = L['type'] in ('same_image', 'agrees', 'tension', 'parallel_domain')
            links.append({'from': a, 'to': b, 'type': L['type'], 'grade': L['grade'],
                          'text': L['teaches'] if use_teaches else L['note'],
                          'text_field': 'teaches' if use_teaches else 'note',
                          'teaches_holds': L['teaches_holds'],
                          'true_direction': {'s': L['s'], 'o': L['o'], 'symmetric': sym,
                                             'reads': ('%s %s %s' % (L['s'], 'and' if sym else L['type'], L['o'])) +
                                                      (' (%s; recorded s to o)' % L['type'] if sym else '')},
                          'source_file': L['source_file'], 'marked_by': L['marked_by']})
        out['chapters'].append({
            'id': ch['id'], 'tamil': cat['tamil'], 'name': cat['name'], 'accent': ch['accent'],
            'subtitle': ch['subtitle'], 'verses': verses, 'links': links,
            'forward': {'text': ch['forward'], 'label': 'கற்பனை · imagined',
                        'then': dict(img(ch['then']), object_of=ch['then']),
                        'future': dict(img(ch['future']), object_of=ch['future']),
                        'transformation': ch['transform']}})
    (HERE / 'chapters.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('wrote site/nilai/v4/chapters.json: %d chapters' % len(out['chapters']))


if __name__ == '__main__':
    build()
