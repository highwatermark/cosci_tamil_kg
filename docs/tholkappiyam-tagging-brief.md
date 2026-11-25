# Brief: tagging verses with Tholkappiyam's theory of meaning

This is a pilot. It asks whether the categories of the பொருளதிகாரம், the third book of the
Tholkappiyam, make a better tagging frame for our five books (Kural, Naladiyar, Tirumanthiram,
Thiruppugazh, Siddhar songs) than the free concept list in `kg/themes/concepts.json`. The
Tholkappiyam was written for Sangam poetry: love poems set in a landscape (akam) and poems of war,
praise and death (puram). None of our five books is that kind of poetry. So the frame will fit some
verses natively, some by extension, and some not at all, and the tags must say which.

The source text is `kg/core/tholkappiyam.jsonl` (Project Madurai pmuni0100, sutras only, no
commentary). Citations below are `porul I.N` for `tholkappiyam:porul:I:N` (iyal I, nurpa N in that
edition's numbering) and `eluttu I.N` for the letters book. Numbering in other editions differs by a
few nurpas; always cite by this file's ids.

Read the Tamil first. For the Tirumanthiram, Thiruppugazh and Siddhar songs the marked `reading`
and `nuance` were written by Claude agents and are claims, not evidence. Tag what the Tamil does.
Never copy a modern commentary.

## The fields

One JSON object per verse. Every field is required; use `null` or `[]` when a category does not
apply, and say why in `note` when the reason is not obvious.

### 1. `akam_puram`: inner or outer

`akam`, `puram`, `mixed` or `neither`.

- `akam`: the verse is about love between a man and a woman, spoken by or for one of the people of
  the love situation (porul 1.1, 1.16, 1.57). The Kural's third book is the obvious case. A
  devotional song in which a girl pines for the god and a friend or mother speaks for her is also
  akam in form: porul 2.23 says the love theme is not barred even for gods (காமப் பகுதி கடவுளும்
  வரையார்).
- `puram`: everything the seven outer thinais cover (porul 2.1 to 2.30): raid, invasion, siege,
  battle, excellence in one's calling, impermanence, praise. Most didactic and devotional verse
  lands here, by extension (see `frame_fit`).
- `mixed`: the verse uses akam's apparatus (landscape, the woman, union, the address to the hill
  lord) for a puram or devotional subject, or the reverse.
- `neither`: technical exposition (cosmology, tattva counts, breath rules, signs of death) that no
  thinai describes. Use it honestly; do not force a thinai on a verse about the thirty-six tattvas.

### 2. `frame_fit`

`native` (the verse is the kind of poem the iyal describes), `extended` (the category applies by
analogy, e.g. an aphorism read as admonition) or `none`.

### 3. `thinai` and `thurai`

`thinai`: for akam, one of `kurinji`, `mullai`, `marutham`, `neythal`, `paalai` (porul 1.5, 1.6 to
1.12), `kaikkilai`, `perunthinai` (porul 1.1, 1.53, 1.54). For puram, one of `vetchi`, `vanji`,
`uzhinai`, `thumbai`, `vaakai`, `kaanchi`, `paadaan` (porul 2.1, 2.6, 2.8, 2.12, 2.15, 2.18,
2.20). `null` for `neither`.

Assign the akam thinai by its `uri` when there is no landscape (porul 1.14 allows thinais to mix, and
1.15 says everything except uri may mix, so uri decides). The puram thinais that matter for our books:

- `vaakai` (porul 2.15, 2.16): excelling in one's own calling; 2.16 lists the brahmin's, the king's
  and others' parts, the sage (அறிவன்) and the ascetic (தாபதப் பக்கம்). Verses praising a type of
  person (the well-born, the patient, the ascetic, the good king) go here.
- `kaanchi` (porul 2.18, 2.19): நில்லா உலகம், the world that does not stay. 2.19 names
  inescapable death (மாற்ற அருங் கூற்றம்) and the old age shown to the living. Impermanence,
  funerals, the body's end.
- `paadaan` (porul 2.20 to 2.30): praise. It includes கடவுள் வாழ்த்து (2.27), praise and
  supplication (பரவலும் புகழ்ச்சியும், 2.22), and, importantly, வாயுறை வாழ்த்து and
  செவியறிவுறூஉ (2.29): wholesome counsel and admonition addressed to a hearer. Most of the
  Kural's and Naladiyar's plain instruction is செவியறிவுறூஉ. Every Thiruppugazh song is paadaan.
- `uzhinai` (porul 2.8: besieging and holding the fort) and `thumbai` (2.12: battle) for the
  Kural's verses on forts and war.

`thurai`: free text naming the sub-situation when one is clear (`செவியறிவுறூஉ`, `கடவுள் வாழ்த்து`,
`மாற்ற அருங் கூற்றம்`, `தாபதப் பக்கம்`, `நெஞ்சொடு கிளத்தல்`), else `null`.

### 4. `mutal`, `karu`, `uri`: setting, native things, human feeling

Porul 1.3 says poems are built of three: முதல், கரு, உரிப்பொருள்.

- `mutal` (porul 1.4, 1.19): land and time. `{"nilam": [words], "pozhudu": [words],
  "negated": bool}`. Land is the four landscapes of porul 1.5 (forest, mountain, watered fields,
  sand shore); the middle thinai, paalai, has no land of its own (1.2) and is fixed by midday and
  summer (1.11). Time is season and hour (porul 1.6 to 1.12, e.g. யாமம், midnight, for kurinji,
  1.7). Put the Tamil words that fix it. Set `negated: true` when the verse explicitly
  denies land or time (பாரில்லை நீரில்லை; இரவும் பகலும் இலாத இடம்): that is a real and telling
  move in mystical verse, not an absence. `null` when the verse has no setting.
- `karu` (porul 1.20, 1.21): the native things: god, food, beast, tree, bird, drum, occupation,
  lute, and the like (தெய்வம் உணாவே மா மரம் புள் பறை செய்தி யாழின் பகுதி). List the Tamil words.
  A temple town's fields, fish and areca palms in a Thiruppugazh praise section are karu; the millet
  field and kura grove of the Valli story are kurinji karu.
- `uri` (porul 1.16): one of `punarthal` (union), `pirithal` (parting), `irutthal` (waiting),
  `irangal` (lament), `oodal` (lovers' quarrel), or `null`. Uri is defined only for akam. Do not
  give a didactic verse an uri because it mentions sorrow.

### 5. `meyppadu`: the eight feelings

Porul 6.3 names eight: நகை `nakai` (laughter), அழுகை `azhugai` (weeping), இளிவரல் `ilivaral`
(disgust, abjection), மருட்கை `marutkai` (wonder), அச்சம் `accham` (fear), பெருமிதம் `perumitham`
(pride), வெகுளி `vekuli` (anger), உவகை `uvagai` (delight). Tag **at most two**: the feelings the
verse makes visible (மெய்ப்படு, brought out in the body) in its speaker, or, in a plain
instruction, the feeling its image is built to raise. An empty list is a correct answer for flat
instruction and exposition.

Porul 6.4 to 6.11 give four causes for each, and the causes are often more telling than the
feeling. Record them in `meyppadu_cause` (Tamil words from those nurpas):

| feeling | causes | nurpa |
|---|---|---|
| nakai | எள்ளல் இளமை பேதைமை மடன் | porul 6.4 |
| azhugai | இளிவு இழவு அசைவு வறுமை | 6.5 |
| ilivaral | மூப்பு பிணி வருத்தம் மென்மை | 6.6 |
| marutkai | புதுமை பெருமை சிறுமை ஆக்கம் | 6.7 |
| accham | அணங்கு விலங்கு கள்வர் தம் இறை | 6.8 |
| perumitham | கல்வி தறுகண் புகழ்மை கொடை | 6.9 |
| vekuli | உறுப்பறை குடிகோள் அலை கொலை | 6.10 |
| uvagai | செல்வம் புலன் புணர்வு விளையாட்டு | 6.11 |

Note what follows from the table: self-abasement (இளிவு) is a cause of azhugai, not of ilivaral;
ilivaral is the feeling raised by old age, disease, suffering and weakness. A Thiruppugazh catalogue
of the body's decay is ilivaral; a poet calling himself a dog is azhugai.

`other_states`: porul 6.12 lists thirty-two further states that are "also there" (இவையும் உளவே):
உடைமை இன்புறல் நடுவுநிலை அருளல் தன்மை அடக்கம் வரைதல் அன்பு கைம்மிகல் நலிதல் சூழ்ச்சி
வாழ்த்தல் நாணுதல் துஞ்சல் அரற்று கனவு முனிதல் நினைதல் வெரூஉதல் மடிமை கருதல் ஆராய்ச்சி
விரைவு உயிர்ப்பு கையாறு இடுக்கண் பொச்சாப்பு பொறாமை வியர்த்தல் ஐயம் மிகை நடுக்கு. Use these (in
Tamil) when the verse's real tone is one of them: equanimity (நடுவுநிலை), restraint (அடக்கம்),
love (அன்பு), grace (அருளல்), reproach (முனிதல்). This is where devotional and renunciant verse
usually lives, because the eight have no slot for calm. Say so rather than forcing one of the eight.

### 6. Meaning layers

`layers` has four keys.

- `stated`: one short English sentence of what the words say.
- `iraicchi`: a meaning that arises from a native thing in the verse without being compared to
  anything (porul 5.33: இறைச்சிதானே உரிப் புறத்ததுவே; 5.34: இறைச்சியின் பிறக்கும் பொருளும்).
  `{"words": [Tamil], "sense": "..."}` or `null`. Strictly this is an akam device; mark it on a
  non-akam verse only when a thing in the verse plainly carries an unstated sense (the funeral
  drum beaten for the bearers too).
- `kurippu`: meaning outside the words themselves, carried by a word's double sense or by what is
  pointedly left out (porul 8.172: பொருட்புறத்ததுவே குறிப்பு மொழியே). `{"words", "sense"}` or
  `null`. The Siddhars' cipher belongs here when the coded sense rests on one word (மெய் as body and
  truth; the horse; the snake), and in `ullurai` when it rests on a whole image.
- `ullurai`: the hidden comparison (porul 1.49 to 1.51): an image lodged inside the poem whose
  meaning is completed by matching it with an unstated subject (உள்ளுறுத்து இதனொடு ஒத்துப் பொருள்
  முடிக). `{"words", "tenor"}` or `null`. **Only when the tenor is not stated.** If the verse
  states both halves (the bees leave the spent branch; the poor have no kin), it is an open
  comparison and goes in `comparisons` with `type: "juxtaposition"`. Porul 5.46 names five kinds of
  ullurai; we do not tag the kind.

### 7. `comparisons`: the basis of each comparison (உவமவியல்)

Porul 7.1: comparison arises in four kinds, வினை பயன் மெய் உரு: action, result, body (shape and
size), colour-form. Porul 7.2: they may combine. List every comparison:

`{"vehicle": Tamil words, "tenor": what is compared, "marker": the comparison word or "none",
"basis": "vinai"|"payan"|"mey"|"uru", "type": "explicit"|"metaphor"|"juxtaposition"|"ullurai"}`

- `explicit`: with a marker (porul 7.11 lists thirty-six: அன்ன ஏய்ப்ப உறழ ஒப்ப என்ன மான ...
  போல ...).
- `metaphor`: the subject is named as the image itself (porul 7.9: பொருளே உவமம் செய்தனர் மொழியினும்
  ... அஃது உவமம் ஆகும்): வினைக்கடல், the body as a skin bag.
- `juxtaposition`: image and subject set side by side with no marker, both stated.
- `ullurai`: repeat the ullurai here with its basis.

Choose the basis by what is shared, not by the marker. Porul 7.12 to 7.16 assign markers to bases
(அன்ன, என்ன, ஆங்க to action; போல, ஒப்ப to colour-form; ஏய்ப்ப, புரைய to body; எள்ள, வெல்ல to
result). The scoring script records the marker's class separately so the pilot can test whether
markers predict basis in our books. Size comparisons (தினைத்துணை, a millet's worth; இமைக்கும் அளவு)
are `mey` (porul 7.10: பெருமையும் சிறுமையும்). Taste and benefit go to `payan`.

### 8. `uyir_mey`: the letters analogy

The letters book defines the twelve vowels as உயிர் (life) and the eighteen consonants as மெய்
(body) (eluttu 1.8, 1.9). A vowel joined to a consonant keeps its nature (eluttu 1.10: மெய்யொடு
இயையினும் உயிர் இயல் திரியா); the consonant is half a measure (1.11); in the joined letter the
vowel sounds after the consonant (1.18); a bare consonant moves with அ (2.13). This is a grammar,
not a philosophy, but the words are the same ones the Siddhars and Tirumular use for soul and body,
so the pilot tags how each verse relates them:

- `dualist`: life leaves, the body is a husk (the dancer leaves the skin bag).
- `union`: life and body work only together, or the Lord is in the soul as life is in flesh.
- `identity`: the verse says they are not two.
- `transcended`: the body's reckoning is to be ended or its sheaths shed.
- `absent`: the verse does not relate them. Most verses.

### 9. `note`

One or two sentences: why a category was stretched or refused, text doubts, and anything the frame
misses. Do not restate the reading.

## Output

`kg/themes/tholkappiyam_pilot/tags_A.json` (or `tags_B.json`): a JSON array of 100 objects in
packet order, each with `id`, `book` and the fields above. Score with
`python3 -I scripts/tholkappiyam_agreement.py`.
