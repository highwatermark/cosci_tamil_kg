# Brief: marking the Sangam books

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph builds a knowledge graph of the
meanings, themes and threads of Tamil literature. Five books are marked and linked: the Thirukkural,
the Naladiyar, the Tirumanthiram, the Thiruppugazh and the Siddhar songs. You are marking chapters of
one of three Sangam books:

| Book | Core file | Unit | Verse key |
|---|---|---|---|
| Purananuru | `kg/core/purananuru.jsonl` | 398 poems (267 and 268 are lost) | poem number |
| Akananuru | `kg/core/akananuru.jsonl` | the invocation (poem 0) and 400 poems | poem number |
| Pattupattu | `kg/core/pattupattu_units.jsonl` | 217 reading units of the ten idylls | unit id, `pattupattu:<poem>:<start>-<end>` |

This is the oldest Tamil poetry we hold and the poetry the Tholkappiyam was written for. So besides
our usual marks (reading, nuance, concepts, uncertain, links) every verse gets the Tholkappiyam fields
that two blind taggers agreed on in the pilot, plus the native-thing and colophon fields recommended
by the review of sangamtamil.com. Two fields that the taggers did not agree on, ullurai and
iraicchi, are kept as **experimental**, with a sharper rule below.

## Read first

- `kg/themes/SCHEMA.md`: the house marking rules. Follow them, with the changes below.
- `docs/tholkappiyam-tagging-brief.md`: the definitions of thinai, uri, mutal, karu, meyppadu and
  the comparison fields. This brief narrows them; where the two differ, this one wins.
- `kg/themes/tholkappiyam_pilot/findings.md`, the agreement section at the end: why some fields are
  in and some are out.
- `docs/sangamtamil-review.md`, sections 3 to 6: the colophon errors already found, the Purananuru
  line differences, and the checks `scripts/sangam_validate.py` will run on your marks.
- `kg/themes/concepts.json`: the shared concept list. Reuse ids (aram, eegai, pugazh, maram, padai,
  arasu, vendhan, sengol, nilaiyaamai, saakkaadu, kootru, kaamam, punarchi, kalaviyal, karpu, pirivu,
  oodal, udanpokku, madal, alar, parathai, nenju, ninaivu, pasalai, iravu, inmai and the rest). Add a
  concept only when none fits, and name what the text names (likely: பரிசில், நடுகல், ஆற்றுப்படை,
  கையறுநிலை, வரைவு, குறி). Tag a new concept only on your own verses.

## Commands (from the repository root)

- Chapters and their verses: `python3 -I scripts/book_marks.py akananuru chapters`
- Your chapters' verses: `python3 -I scripts/book_marks.py akananuru show 3 4`
- Validate your files: `python3 -I scripts/book_marks.py akananuru check 3 4`
- Any verse of the marked books: `python3 -I scripts/verse.py kural:1061 naladiyar:47 tirumanthiram:668`
- `show` prints every line with its number. **Line numbers are the ones `show` prints**: the
  position in the poem for Akananuru and Purananuru (a dotted gap line counts as a line), the
  idyll's own line number for the Pattupattu. It also prints the colophon (thinai, thurai, poet,
  patron) and any text flag from `kg/core/sangam_text_flags.jsonl`.

Chapters: Akananuru and Purananuru chapters are runs of 20 poem numbers (chapter 1 of the
Akananuru also holds the invocation, poem 0). Pattupattu chapters are runs of up to 24 units of one
idyll (13 chapters: the long idylls have two).

## Copyright

No modern translation or commentary text anywhere in your files, in Tamil or English.

- The Purananuru core file carries a modern heading (`title`), a modern note (`note`) and Duraisamy
  Pillai's commentary (`duraisamy_pillai.commentary`), all marked `modern` in `rights`. `show` does
  not print them. Do not open them for wording. `check` fails a reading or nuance that repeats a
  run of six words from that commentary.
- sangamtamil.com's English translations and the turai renderings are Vaidehi Herbert's modern work.
  Do not use them. `kg/sangam/facts.jsonl` holds only facts (codes, words, line numbers); you may use
  it to check that you have not missed a native thing.
- The Tamil verse and the colophon facts are public domain. Readings are your own words.

## What a chapter file looks like

`kg/themes/<book>/chNNN.json`, with the house fields `chapter_no`, `chapter_theme`, `verses`,
`links`, `new_concepts`, `source_issues`. There is no commentary in the corpus, so there are no
`positions` and no `contested` (check rejects both).

### House fields (every verse)

| Field | Required | Meaning |
|---|---|---|
| `reading` | yes | one sentence on what the poem says, in your own words |
| `concepts` | yes | 1 to 4 concept ids, most central first |
| `nuance` | no | what a quick reader would miss; omit unless there is something real to say |
| `uncertain` | no | `true` when the sense turns on a corrupt line, a rare word, or a reading you cannot fix |

### Tholkappiyam fields (every verse)

| Field | Required | Agreement in the pilot | What goes in it |
|---|---|---|---|
| `akam_puram` | yes | kappa 0.97 | `akam`, `puram` or `mixed` |
| `colophon` | yes | (a sourced fact) | `{"thinai", "thurai"}` copied exactly from the core record |
| `thinai` | yes | 82% | your inferred thinai (romanized id); `null` only with `uncertain` |
| `thinai_evidence` | with thinai | | `{"basis", "words", "note"}` |
| `mixed` | yes | | `true` when native things of another land are in the poem |
| `uri` | akam | kappa 0.93 | `punarthal`, `pirithal`, `irutthal`, `irangal`, `oodal`; `null` for puram |
| `mutal` | yes | | `{"land", "season", "hour", "negated"}` or `null` |
| `karu` | yes | (recast; see below) | every native thing, with stem, form, line, kind and role |
| `comparisons` | yes | 0.84; basis and type about 0.9 | every comparison, with basis and type; `[]` if none |
| `meyppadu` | yes | Jaccard 0.75 | at most two `{"feeling", "cause"}`; `[]` is a correct answer |
| `thurai_akam` | akam | | speaker, addressee, overhearer, occasion, from the Tamil colophon |
| `puram_thurai` | puram | | the colophon's thurai names, normalised, with the form they came from |
| `entities` | when present | | kings, patrons, battles, towns, rivers, hills, hero-stones named in the poem |
| `ullurai` | experimental | kappa 0.48 | `null` or an object; see the rule |
| `iraicchi` | experimental | kappa 0.49 | `null` or an object; see the rule |

Left out on purpose: `kurippu` (0.45), the porul 6.12 states, `frame_fit` and `uyir_mey` (they were
made for the later books; every Sangam poem is native to the frame).

## The fields in detail

### `akam_puram`

`akam` for love poems spoken by or for a person of the love situation (porul 1.1, 1.3); `puram` for
war, praise, giving, death and counsel (porul 2.1 to 2.30); `mixed` when a poem uses one frame for
the other's matter. Every Akananuru poem is akam by its place in the anthology, but a few carry long
puram matter (a king's battle, a hero-stone on the path): they stay `akam` unless the puram matter
is what the poem is about. The invocations (Akananuru 0, Purananuru 1, Thirumurugatruppadai) are
puram: கடவுள் வாழ்த்து sits under paadaan (porul 2.27).

### `colophon`, `thinai`, `thinai_evidence`, `mixed`

Two thinais, never merged:

- `colophon` is the source's fact. Copy `thinai` and `thurai` exactly as `show` prints them, errors
  included, and `null` where the record has none. Do not correct it here: put the correction in
  `source_issues` (for example Purananuru 5's வெவியறிவுறூஉ for செவியறிவுறூஉ). For a Pattupattu
  unit it is the whole idyll's colophon.
- `thinai` is your inference from this poem (or unit) alone, as a romanized id. Akam: `kurinji`,
  `mullai`, `marutham`, `neythal`, `paalai`, `kaikkilai`, `perunthinai`. Puram: `vetchi`,
  `karanthai`, `vanji`, `kaanchi`, `uzhinai`, `nochchi`, `thumbai`, `vaakai`, `paadaan`,
  `pothuviyal`, `kaikkilai`, `perunthinai` (the colophons use the later twelve-thinai scheme, so
  karanthai, nochchi and pothuviyal are allowed). Decide it before you look at the colophon if you
  can, and do not copy the colophon when the poem points elsewhere: a disagreement is data.
- `thinai_evidence`: `basis` is what decided it: `uri` (the human situation: porul 1.15 says only
  uri may not mix, so it decides when the things are mixed), `karu`, `mutal`, `content` (for puram:
  what the deed is), or `thurai` (only when the poem itself gives no evidence and you fell back on
  the colophon). `words` are Tamil words from the poem (check finds each one), and `note` is one
  clause.
- `mixed`: `true` when a native thing of another landscape appears (திணை மயக்கம், porul 1.14,
  1.21). Mark that thing's `land` in `karu`; check requires at least one karu item with a `land`
  other than your thinai. Paalai has no land of its own (porul 1.2, 1.11), so a paalai poem full
  of kurinji or mullai things is normal; mark it mixed and do not change the thinai.

### `uri`

As in the Tholkappiyam brief (porul 1.16). Required for akam, `null` for puram. For `mixed` give
one when the poem has a love situation.

### `mutal`: land, season and hour, apart from the native things

`{"land": [words], "season": [words], "hour": [words], "negated": bool}` or `null`. Tamil words
from the poem that fix the land (porul 1.5: forest, hill, watered fields, sea shore) and the time
(porul 1.6 to 1.12). For reference: mullai, the rains and evening (1.6); kurinji, the cold season
and midnight (1.7, 1.8); marutham, dawn (1.9); neythal, sunset (1.10); paalai, midday and summer
(1.11, 1.12). `negated: true` when the poem says the land or season is ruined or absent (the
dried spring, the rains that failed). A place name is not mutal; it goes in `entities`.

### `karu`: every native thing, with what it does in the poem

The pilot's karu field (present or not) was the least reliable of all (kappa 0.37). The review
recommends recording each thing as it stands in the line instead, which can be checked against the
8,082 located mentions of sangamtamil.com (`kg/sangam/facts.jsonl`). One object per thing:

    {"form": "காரான்", "stem": "கார் ஆன்", "line": 1, "kind": "maa", "role": "ullurai", "land": null, "sense": "buffalo"}

- `form`: the word exactly as written in that line, sandhi and case ending included; check finds it
  on that line. Do not lemmatise the form.
- `stem`: the base word, your own normalisation.
- `kind`: one of the nine of porul 1.20 (தெய்வம் உணாவே மா மரம் புள் பறை செய்தி யாழின் பகுதியொடு
  ... அவ் வகை பிறவும்): `deyvam` (god), `unavu` (food), `maa` (beast), `maram` (tree and plant,
  flowers included), `pul` (bird), `parai` (drum), `seythi` (occupation and the people who follow
  it), `yaazh` (lute and music), `pira` (the like: water, fish, insects, salt, the rest).
- `role`, what the thing DOES in this poem:
  - `scene`: it sets the place or the moment and carries nothing further.
  - `ullurai`: it is the vehicle of a hidden comparison (rule below).
  - `iraicchi`: it carries an implied sense of its own (rule below).
  - `simile`: it is the vehicle (or tenor) of an explicit comparison listed in `comparisons`.
  - `ornament`: it is worn or carried (a garland, a flower in the hair, a bangle of conch).
  - `gift_food`: it is given, eaten or drunk (the bard's gift, the toddy, the rice of the feast).
  - `absent`: the poem names it as missing, dead or withered.
- `land`: the landscape it is native to, when it is out of place (needed for `mixed`), else `null`.
- `sense`: one or two English words, required for a word with two common senses (மா beast, horse
  or mango; ஏறு bull or thunder; கலை stag or art; அன்ன is a particle, not the swan; இல is "not",
  not the silk-cotton tree). The sense is chosen per verse.

Leave out place names, kings and heroes (they go in `entities`) and abstract words. List a thing
once per role; list it again if the same word plays a second role in another line.

### `comparisons`

As in the Tholkappiyam brief, section 7: `{"vehicle", "tenor", "marker", "basis", "type"}`. `basis`
is one of `vinai`, `payan`, `mey`, `uru` (porul 7.1), or a list of two when they combine (porul 7.2).
`type` is `explicit` (with a marker in its base form, அன்ன or போல; check finds it in the verse,
allowing a vowel-initial marker to lose its vowel in sandhi, as in இயன்றன்ன), `metaphor`, `juxtaposition`
(both halves stated, no marker) or `ullurai`. `marker` is `null` or `"none"` for the last three.
`vehicle` is Tamil words from the poem. Choose the basis by what is shared, not by the marker. Sangam
similes are dense (a town, a king's army, a jewel as vehicle); list each one.

### `meyppadu`

At most two, each `{"feeling", "cause"}`. Feelings: `nakai`, `azhugai`, `ilivaral`, `marutkai`,
`accham`, `perumitham`, `vekuli`, `uvagai` (porul 6.3). The cause must be one of that feeling's four
Tamil words in porul 6.4 to 6.11 (the table in the Tholkappiyam brief); check enforces the pairing.
The feeling is the one the poem makes visible in its speaker or raises in its hearer. Puram poems
are where perumitham (from தறுகண் or கொடை) and azhugai (from இழவு) live; most akam poems of
separation show azhugai or accham, but an empty list is right for a calm description.

### `thurai_akam`: the speech situation

Akananuru colophons give, in Tamil, who speaks, to whom, who overhears and on what occasion. Record
it as a list, one object per numbered alternative in the colophon ((1), (2), (3)), and in colophon
order:

    {"alt": 1, "speaker": "thozhi", "addressee": "thalaivan", "overhearer": null,
     "occasion": {"stage": "karpu", "words": "வாயின் மறுத்தது"}}

Person codes (porul 8.181 and 8.182 name who may speak in களவு and in கற்பு; 4.52 names the
go-betweens): `thalaivan` (கிழவன், தலைமகன்), `thalaivi` (கிழத்தி, தலைமகள்), `thozhi`, `sevili`
(the foster mother), `nartaay` (the mother), `paarppaan`, `paangan` (the hero's companion),
`paanan`, `koothan`, `virali`, `parathai`, `arivar`, `kandor` (onlookers), `ilaiyar`, `virunthinar`,
`ur` (the town, the gossips), `nenju` (the speaker's own heart, as addressee), `pira` (anyone else;
say who in the note). `overhearer` is the person the colophon says is standing by (சிறைப்புறம்,
porul 4.38), else `null`. `occasion.stage` is `kalavu`, `karpu` or `null`; `occasion.words` is a
phrase copied from the colophon thurai (check finds it there). Required for akam verses of the
Akananuru; for the Pattupattu, give it when a unit has its own speaker.

### `puram_thurai` and `entities`

`puram_thurai` is required for puram and mixed verses: a list, `[]` when the colophon has no thurai.
Each item is `{"name": the thurai in its usual spelling, "colophon_form": the same words exactly as
the colophon has them}`. A colophon with two thurais (`...: பொருண் மொழிக் காஞ்சியும் ஆம்`) gives
two items. Correct a misprint in `name` and record it in `source_issues`; `colophon_form` keeps
the misprint.

`entities` (any verse, akam too): every named person and place of these seven types, as
`{"type", "name", "line"}`, with `name` exactly as written on that line: `king`, `patron` (the one
addressed or praised, when not a crowned king), `battle` (a named battlefield or war), `town`,
`river`, `hill`, `herostone` (a நடுகல், named or not; put the word for the stone in `name`).
The poet and the colophon's patron are facts in the core file; list a patron here only where the
poem names him.

## Ullurai and iraicchi (experimental)

The two blind taggers of the pilot disagreed on both (kappa 0.48 and 0.49): one found nine hidden
comparisons, the other three. The rules below are meant to be tested: each condition is something a
second reader can check. Mark every object `"experimental": true`. If a candidate fails a
condition, give the thing `role: "scene"` (or `simile`), not ullurai or iraicchi; you may mention
the traditional reading in `nuance`.

### Ullurai: the hidden comparison

What the Tholkappiyam says: ullurai and the open comparison are the two ways a thinai is known
(porul 1.49); ullurai takes any native thing except the god as its vehicle (porul 1.50: உள்ளுறை
தெய்வம் ஒழிந்ததை நிலம் எனக் கொள்ளும்); it is the image lodged in the poem whose sense is completed
by matching it with something else (porul 1.51: உள்ளுறுத்து இதனொடு ஒத்துப் பொருள் முடிக). Who may
use it is limited: the heroine only with things she knows (porul 7.26), the friend without leaving
the land of the poem (7.27), the hero openly (7.28), anyone else freely (7.29).

**Tag ullurai only if all five hold:**

1. **Native vehicle.** The vehicle is a karu item of the poem (not a god, porul 1.50) and is listed
   in `karu` with `role: "ullurai"`.
2. **Tenor not stated.** No comparison marker joins the image to a human subject, and the poem does
   not draw the moral itself. If it does (the scene, and then "so you too..."), it is a
   `juxtaposition` or `explicit` comparison, not ullurai.
3. **At least two pairs.** You can name two or more separate correspondences between parts of the
   scene and parts of the love situation (who, what act, what harm). A single match of mood (a dry
   land for a sad heroine) is not ullurai: that is scene or mutal.
4. **Anchored.** The situation the pairs point to is stated in the poem or in its colophon thurai.
   `anchor` is Tamil words copied from one of them (check finds them).
5. **Speaker fit.** The vehicle is one the speaker may use (porul 7.26 to 7.29). Say how in
   `speaker_fit`.

    "ullurai": {"experimental": true,
                "vehicle": [{"form": "காரான்", "line": 1}],
                "tenor": "the hero and his new wife",
                "pairs": [{"scene": "நோன் தளை பரிந்து", "situation": "he breaks the household's bond"},
                          {"scene": "மீன்உடன் இரிய", "situation": "the household is thrown into flight"}],
                "anchor": "ஒருத்தியை நம்மனைத் தந்து",
                "speaker_fit": "the friend uses a marutham buffalo in a marutham poem (porul 7.27)"}

Ullurai is an akam device: check rejects it on a puram verse. A hidden image in a puram poem goes in
`comparisons` as `metaphor` or `juxtaposition`.

### Iraicchi: the sense that rises from a thing

What the Tholkappiyam says: iraicchi lies outside the uri itself (porul 5.33: இறைச்சிதானே உரிப்
புறத்ததுவே); a further meaning is born from it for those who know the craft (5.34); pointing, in
iraicchi, to tender things that befit love serves as reassurance when the heroine suffers (5.35:
அன்புறு தகுவன இறைச்சியுள் சுட்டலும் வன்புறை ஆகும் வருந்திய பொழுதே); what is seen on the
road may be told as iraicchi (porul 4.7, 4.29). The word book adds that a name used for iraicchi
points to the land, not to a person (col 5.42).

**Tag iraicchi only if all four hold:**

1. **One carrier.** A single karu item, or one pair of creatures acting together, listed in
   `karu` with `role: "iraicchi"`. A whole scene mapped part by part is ullurai (condition 3 above);
   one thing with one sense is iraicchi.
2. **An act.** The thing does something in the poem that a person of the situation does, fails to
   do, or should do: the male feeds or shades or guards its mate, the bird leaves the nest, the
   creature goes hungry together with its partner. A thing that only looks or sounds a certain way
   carries a mood, which is scene. Write the act in `act`.
3. **Deletion test.** Strike the carrier's lines: the poem's stated sense (who says what to whom,
   from the colophon and the closing lines) still stands. If the sense falls with it, the thing is
   the subject, not iraicchi. Set `deletion_test: true` only after doing this.
4. **One sense, about the people.** `sense` is one sentence: what the act implies for the lovers
   (as the stag does, so the hero will; even the beasts do not part, yet he went). Pointing to tender
   creatures to comfort the heroine is the textbook case (porul 5.35); look for it when the colophon
   says வற்புறுத்தியது or ஆற்றுவித்தது.

    "iraicchi": {"experimental": true,
                 "carrier": {"form": "இரலை", "line": 4},
                 "act": "the stag feeds the young doe and guards her while she sleeps",
                 "sense": "the hero, who has seen it, will hurry home to care for his wife",
                 "deletion_test": true}

One thing cannot be both the ullurai vehicle and the iraicchi carrier in the same poem. Iraicchi is
an akam device; check rejects it on a puram verse.

### Worked examples (Akananuru, in our own words)

Each example says which condition decides. These are our readings of the Tamil, offered as models of
the test, not as settled interpretations.

**Ullurai.**

1. *Akananuru 46 (marutham; the friend refuses the hero entry).* Lines 1 to 6 address the hero as
   lord of a town where a red-eyed buffalo, tired of standing in mud, breaks its strong tether in the
   night while the town sleeps, shoulders aside the thorn fence with its horn, sends the fish of the
   pond fleeing, tramples the valli creepers and grazes on the lotus. Lines 9 and 10 say he has
   brought another woman home and married her. All five conditions hold: the buffalo is karu of the
   poem's own land (1); there is no marker, and the friend never says "you are like the buffalo"
   (2); at least three pairs map (the broken tether to the broken bond of the house, the night to
   secrecy, the fleeing fish to the disturbed household, the eaten lotus to the new woman) (3); the
   anchor is ஒருத்தியை நம்மனைத் தந்து, line 9 (4); the friend speaks with a thing of the marutham
   field (porul 7.27) (5). Tag it. The Pandya's town in line 14 (அள்ளூர் அன்ன) is a separate
   explicit comparison, and செழியன் and அள்ளூர் are `entities`.
2. *Akananuru 56 (marutham; the heroine speaks to her friend).* A dark-horned buffalo stirs a clear
   pond, tears the water-lily leaves, gorges on the blue lilies and comes to rest with the pollen
   of the kaanji tree on its wet back; the lord of that cool ford has just embraced new brides (lines
   8, 9). Pairs: the buffalo's many flowers to his many women, the pollen on its back to the marks
   he brings home (3). Anchor: வதுவை நாள்அணிப் புதுவோர்ப் புணரிய (4). The speaker condition is the
   one to check: the heroine may use only what she knows (porul 7.26), and the buffalo at the pond
   of her own town is such a thing, so it passes (5). The two similes inside the scene (the pond
   like a gem, line 2; the horns like wrought iron, line 3) go in `comparisons` as explicit; they do
   not make the ullurai.
3. *Akananuru 2 (kurinji; the friend urges marriage). Not ullurai.* A male monkey drinks, without
   knowing it, the wine that ripe jackfruit has made in a rock pool, cannot climb the sandal tree,
   and sleeps happily on the flowered slope. The friend then says it herself (lines 8 to 10): the
   beasts of your hill get unplanned joy so easily; how can planned joy be hard for you? The tenor is
   stated, so condition 2 fails: tag it as a `juxtaposition` comparison (basis `payan`), give the
   monkey `role: "simile"` only if you list it as the vehicle, else `scene`, and set ullurai to
   `null`. A further hidden layer (the drunk monkey as the lover who will not climb to marriage) may
   go in `nuance` as a traditional reading.

**Iraicchi.**

1. *Akananuru 34 (mullai; the hero, his work done, speaks to his charioteer).* In the cool scrub, a
   stag with twisted horns feeds tender grass to his young doe and, on the sandbank, guards her back
   while she sleeps chewing; then the hero bids the chariot hurry so his heart may find ease with his
   shy wife. One pair of creatures (1); an act, feeding and guarding (2); strike lines 1 to 8
   and the stated sense (go fast, chariot, so I may reach her) stands (3); one sense: the stag's care
   is the care the hero means to bring home (4). Tag it. The stag also sits in an explicit simile
   (its horns like the forked stick a hunter carries, line 3), which goes in `comparisons`; that does
   not stop it carrying the iraicchi.
2. *Akananuru 91 (paalai; the friend comforts the heroine).* In a hill the sun has scorched, the
   elephant, finding no water, eats moss and shrinks together with his hungry mate (lines 5, 6); the
   friend says the man who crossed that land for wealth still has great love. One pair (1); an act,
   staying together in hunger (2); the comfort of lines 8 and 9 stands without them (3); the sense,
   even the beasts in drought keep together, is the reassurance porul 5.35 describes, and the
   colophon says வற்புறுத்தியது (4). Tag it. The buffalo that leaves the lotus to rest in the
   jackfruit shade (lines 15, 16) is not iraicchi: it describes Kuttuvan's rich land, which the hero
   would not stay for; it is `scene`, and குட்டுவன் and குடநாடு are entities.
3. *Akananuru 269 (paalai; the friend comforts the heroine). Not iraicchi.* The road the hero took
   is lined with hero-stones (lines 3 to 13), washed, smeared with turmeric and crowned with karanthai
   flowers. A reader may feel the danger of the road in them, but condition 2 fails: the stones do
   nothing that a person of the love situation does or should do; they carry a mood. Give them
   `role: "scene"`, and add a `herostone` entity with the word for the stone in line 7,
   `நெடுங்கல்`. The poem's closing simile (her eyes like the red water-lily of Vaanan's fields,
   lines 22 to 25) goes in `comparisons`.

## The Pattupattu: four notes

1. **Units are a mechanical cut, and you may move a boundary to a sense break.** The units were cut
   by a script at 10 to 25 lines, scored by how strongly a line closes a sentence (see the header of
   `scripts/build_sangam_core.py`); `show` prints each unit's break score (3 strong, 0 none). Where a
   cut falls in the middle of a sentence or a description, move it. Rename the affected units by
   their new line spans (`pattupattu:9:218-235` and `pattupattu:9:236-251`), and give each moved
   unit a `unit_note` that says the unit was adjusted, from which boundary, and which line ends the
   sentence. Check enforces: the chapter's units still cover exactly the chapter's lines with no gap
   or overlap, an adjusted unit is 6 to 30 lines, and every unit not in the core file has a
   `unit_note`. Do not move a boundary across a chapter or across a section of
   Thirumurugatruppadai (the six abodes). Links to a moved unit use its new id.
2. **The colophon belongs to the whole idyll; your thinai belongs to the unit.** Copy the idyll's
   colophon into every unit. Infer thinai, akam_puram and uri from the unit alone. They will often
   differ, and should: Pattinappalai is a paalai poem (செலவழுங்குதல், the hero gives up a journey)
   that spends most of its lines praising Karikalan's city; Nedunalvadai's colophon says vaakai
   while its palace scenes are of a queen waiting; Maduraikkanchi's kaanchi counsel frames a long
   description of Madurai. Mark such units `mixed` or by what they do, and give `thurai_akam` only
   to a unit with its own speaker.
3. **Five idylls are guide poems (ஆற்றுப்படை).** Thirumurugatruppadai, Porunaratruppadai,
   Sirupanatruppadai, Perumpanatruppadai and Malaipadukadam are spoken by one performer directing
   another to a patron (paadaan, thurai ஆற்றுப்படை). Their units are long catalogues of the road:
   lands, peoples, foods and gifts. This is where `karu` with `gift_food` and `seythi`, and
   `entities` (patron, hill, river, town), do most work. The speaker is not an akam person, so
   leave `thurai_akam` empty and use `puram_thurai`.
4. **Text and numbering.** Line numbers and unit ids are the idyll's own (1-based, the standard
   line counts, which all ten match). Mullaippattu's text is U. V. Swaminatha Aiyar's (pmuni0488),
   the others are Project Madurai's; Pattinappalai line 210 is two half-lines joined into one, as
   both editions number it. `show` prints every repaired line and repeated line; record any doubt in
   `source_issues`.

## Links

`links` is a list of `{"a", "b", "type", "note", "teaches"}`.

- `a` is one of your verse keys (a poem number, or a Pattupattu unit id).
- `b` may be a poem in the same book (an integer), another Sangam book (`purananuru:N`,
  `akananuru:N`, `pattupattu:<poem>:<start>-<end>`, any line span inside the idyll), or a marked
  book: `kural:N`, `naladiyar:N`, `tirumanthiram:N`, `thiruppugazh:N`, `siddhar:N` (the running
  number `show` printed for that book). Read the other verse before linking.
- Types as in SCHEMA.md: `tension`, `agrees`, `develops`, `qualifies`, `same_image`,
  `parallel_domain`. At most three links per verse.
- **`teaches` is required: one sentence that says what a reader learns from the pairing that neither
  verse shows alone.** A shared topic is not a lesson: "both are about giving" fails; "the Kural
  states as a rule what the Purananuru poet presents as one king's habit, so the rule had a heroic
  model before it was a maxim" passes. If you cannot write that sentence, do not make the link.
  Check rejects a `teaches` of fewer than six words or one that repeats the note.
- A `tension` must be an incompatible claim on at least one defensible reading, and the note says
  which. Good places to look: the Purananuru's kaanchi and pothuviyal poems against the Naladiyar's
  chapters on impermanence; its counsel to kings (செவியறிவுறூஉ) against the Kural's chapters on the
  state; the bard's gift poems against the Kural on giving; Akananuru situations against the Kural's
  third book, which retells many of them in two lines; the Thiruppugazh's love songs, which borrow
  akam's apparatus. Within the Sangam books, the same king, battle or town in a Purananuru poem and
  an Akananuru simile is a real `same_image` link when it tells us how akam poets used puram fame.

## Rules

- Read the Tamil first. Nothing in the corpus explains it for you.
- Every Tamil word you put in a field must be in the verse as written (check finds `karu` forms and
  `entities` on their line, and evidence, mutal, comparison and pair words in the verse).
- Never overwrite a colophon fact with an inference. Disagreements go in `thinai`, not in
  `colophon`; errors go in `source_issues`.
- Before marking a Purananuru poem, check the line-difference table in `docs/sangamtamil-review.md`
  section 4 and the flags `show` prints. If lines are missing from our text, mark what is there and
  say so in `source_issues`.
- Do not edit any file except your own chapter files. Do not commit.
- When every file passes `check`, reply with only: the chapters done, new concept ids, link counts
  (within the book, to each other Sangam book, and to each other book), how many verses you marked
  uncertain, how many ullurai and iraicchi you tagged, how many verses have your thinai different
  from the colophon, how many Pattupattu units you adjusted, and text problems.
