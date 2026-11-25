# Brief: reading layers for the Siddhar songs (pilot)

The flat marking of the Siddhar songs (`kg/themes/siddhar/chNNN.json`, per
`docs/siddhar-marking-brief.md`) gives each verse one reading. Blind grading found that links
between Siddhar verses are only 53% sound and links between the devotional books 48%, against 82%
inside the Kural. Graders mark links weak or forced because a link rests on a cipher reading the
Tamil does not fix, or on a stock attack on ritual that two verses merely share. One reading per
verse hides which kind of claim a link is making.

This pilot gives each verse several **reading layers** held at once, each with its own confidence
and the Tamil words that carry it, and makes every link name the layer it depends on. A link that
holds only on a coded layer is then visible as such, and can be graded as such.

Files go in `kg/themes/siddhar_layers/chNNN.json`, one per chapter, using the chapter numbers and
`seq` verse keys of `python3 -I scripts/book_marks.py siddhar show N`. Validate with
`python3 -I scripts/siddhar_layers_check.py [N ...]`. The flat marks are not edited; the layer file
sits beside them.

## The five layers

| id | layer | what it reads |
|---|---|---|
| `literal` | literal | What the words say on their plain sense, technical words taken as named (a verse that says மூலநாடி names a channel; that is literal, not coded). Required on every verse. |
| `breath` | breath and yoga | The body practice: வாசி, prana and its counts, the nadis (இடை, பிங்கலை, சுழுமுனை), the ஆதாரம் centres, the gates, kundalini, the nectar, the inner sound and light. |
| `alchemy` | alchemy and medicine | Claims about medicines, pills (குளிகை), mercury (இரசம்), metals, herbs (மூலிகை), the humours (வாதம், பித்தம், கபம்), disease and long life. **Recorded as historical claims only**: what the verse claims and how it reasons. Never restate a preparation, a quantity, a dose or a method of use; never present a claim as a remedy. |
| `consciousness` | consciousness and non-duality | God within, the self known by itself, ego dissolution (ஆங்காரம், நான்), மௌனம், சூனியம், வெளி, the states (சாக்கிரம் to துரியம்), the beyond of the tattvas. |
| `social` | social critique | Caste, ritual, temple images and pilgrimage, mantras for hire, false gurus and garb, book-learning, sects. |

Add a layer to a verse only when Tamil words in the verse carry it. Do not add a breath layer
because the poet is a Siddhar, a social layer because the chapter attacks ritual elsewhere, or a
consciousness layer to every mention of God. Most verses have two or three layers; a verse with
five is suspect.

Each layer present on a verse has:

| field | required | meaning |
|---|---|---|
| `reading` | yes | One or two sentences: what the verse says on this layer, in your own words. |
| `confidence` | yes | `high`, `med` or `low` (below). |
| `carriers` | yes | 1 to 5 Tamil words or phrases, copied exactly from the verse (spacing may differ), that carry this reading. |
| `keys` | yes | A list of cipher-key ids (table below) this reading applies; `[]` if it applies none. |
| `lexicon` | yes | Ids of the double-reading words (`kg/themes/siddhar_layers/cipher_lexicon.json`) this reading depends on; `[]` if none. |

**Confidence.** `high`: the Tamil fixes the reading, no key needed or the key is stated in the
verse itself. `med`: one standard key or one gloss is needed and the context supports it, or the
plain words allow two senses and this is the likelier. `low`: the reading needs a key the context
does not support, or a word that may be corrupt, or it is one of several live guesses. The literal
layer can be `low` too, when a line is corrupt or does not construe.

**Carriers** are evidence, not decoration: if you cannot point to the words, the layer is not there.

## Cipher keys

A key is a traditional decoding of a word, number or figure into a term of yoga, medicine or
doctrine. Applying one is a claim about how tradition reads the verse, not a fact about the verse.
Name every key you use. Add a key to this table only if you need it; the checker reads the table.

<!-- keys -->
| key | Tamil signals | as tradition decodes it | usual layer |
|---|---|---|---|
| `sun_moon` | சூரியன், பரிதி, கதிர், பானு, அருக்கன் / சந்திரன், மதி, திங்கள், நிலா | the right and left breaths (பிங்கலை, இடை), and the hot and cool poles of the body | breath |
| `three_lights` | முச்சுடர், சுடர் மூன்று, மண்டலம் மூன்று | the three regions or lights of sun, moon and fire: the two breaths and the fire at the root | breath |
| `fire_nectar` | வன்னி, அங்கி, அனல், தீ in the root / நீர், அமுதம், பால் from above | kundalini fire raised from the root, and the nectar that falls from the moon in the head | breath |
| `vaasi_horse` | வாசி, பரி, புரவி, குதிரை | the breath as a practice, ridden and reined | breath |
| `serpent` | பாம்பு, அரவு, நாகம் | the coiled power at the root (kundalini) | breath |
| `root_channel` | மூலநாடி, தந்தி, மேருநாடி, நடுநாடி | the central channel, சுழுமுனை | breath |
| `middle` | நடு, நட்டநடு, நடுவறிந்து | the central channel, or the point between the brows | breath |
| `nine_gates` | ஒன்பது வாசல், ஒன்பது (of the body), நவத்துவாரம் | the nine openings of the body | literal |
| `upper_door` | மேலை வாசல், பெருவழி, உச்சி, சிரம், பிரமரந்திரம் | the crown aperture, the exit above the six centres | breath |
| `three_bolts` | மூன்று தாள், வாசல் மூன்று, முடிச்சு | the three knots (granthi) on the central channel, or the three lower channels | breath |
| `eight_counts` | எட்டு, எட்டெட்டு, எட்டும் இரண்டும், பதினாறு | breath counts, the sixty-four, or the numeral letters அ (8) and உ (2) | breath |
| `triangle_root` | திரிகோணம், முக்கோணம் | the triangle of the root centre (மூலாதாரம்) | breath |
| `crown_lotus` | கமலம், தாமரை, சிரமதில் கமலம் | a centre as a lotus; in the head, the thousand-petalled crown | breath |
| `letters_aum` | அகாரம், உகாரம், மகாரம், ஓம் | the three parts of the pranava as stages, bonds or persons (ம as malam or maya) | consciousness |
| `letters_five` | ந, ம, சி, வ, ய, அஞ்செழுத்து, சீ, அவ், யவ் | the five syllables as categories: சி Siva, வ grace, ய the soul, ம malam, ந concealment | consciousness |
| `void` | சூனியம், பாழ், வெளி, பரவெளி | the empty ground that is the Supreme, or the crown's space | consciousness |
| `body_shrine` | names of shrines (சிதம்பரம், அண்ணாமலை, காசி, தில்லை) | places in the body: the heart as Chidambaram, the root or crown as the hill | social |
| `kuligai` | குளிகை, கமனக் குளிகை | the alchemist's pill (claimed to transmute or to give flight), or the retained breath or seed | alchemy |
| `rasa` | இரசம், ரசம், ரசபானம் | mercury, the alchemist's base, or the inner nectar | alchemy |
| `metals` | செம்பு, செப்பு, பொன், களங்கு | base metal turned to gold, the body or mind refined | alchemy |
| `muppu_salt` | உப்பு, முப்பு | the alchemists' three salts (முப்பு), or the body that dissolves | alchemy |
| `maranam` | மாரணம் | the 'killing' (calcination) of a metal, or the tantric rite of killing | alchemy |
<!-- /keys -->

## Stance

The Siddhar corpus has no single doctrine, and its poets sometimes hold views that cannot be
reconciled. Do not assume monism, and do not read one poet's position into another's verse. Each
verse gets a `stance`: a list of one or two values, the main one first, for the position the
verse itself takes.

<!-- stances -->
| stance | meaning |
|---|---|
| `shakta_tantric` | the goddess or kundalini in the body; the yogic body (centres, channels, breath) as the way |
| `saiva_siddhanta` | devotional and graded: grace, the Lord's feet, the four paths, the guru, the tattvas as a ladder |
| `void_nondual` | the void or open space (வெட்டவெளி, சூனியம், பரவெளி), non-dual knowing, everything named set aside |
| `alchemical_physical` | bodily perfection: the undying body, pills, mercury, medicine for long life |
| `ethical_social` | conduct and critique: ritual, caste, false gurus, pilgrimage, sects, the conduct of life |
| `unclear` | the verse takes no position among these (a roll call, a catalogue, a figure of transience), or its Tamil does not fix one |
<!-- /stances -->

Links and old-link reviews record `stances`, a pair of stance lists for `a` and `b`. For a pilot
verse it must equal that verse's `stance`; for a verse of another book, or a Siddhar verse outside
the pilot, give the nearest value, using `unclear` freely: the vocabulary is built for the Siddhars.
Two verses are of the **same stance** when their lists share a value. A `tension` between verses of
different stances may be a difference of school rather than of claim; say so in the note.

## The double-reading lexicon

`kg/themes/siddhar_layers/cipher_lexicon.json` lists every word or phrase in the pilot chapters
that carries two traditional senses (வாசி as horse and as breath; தாள் as bolt and as the Lord's
foot; அத்தி as elephant and as channel). It is versioned, and each entry has a `status`:
`proposed` when an agent adds it, `accepted` or `rejected` after review. Each entry has:

| field | meaning |
|---|---|
| `id` | a short romanized id, cited from layer readings in `lexicon` |
| `tamil` | the word or phrase as the pilot verses spell it |
| `senses` | exactly two `{"sense", "layer"}`: the two traditional senses and the layer each belongs to |
| `uses` | `{"verse", "layers"}` for each pilot verse, naming the layers whose reading depends on the entry |
| `pattern` | the regular expression used to count it in the corpus (matched against each unit's Tamil with spaces removed) |
| `corpus_verses` | how many units of `kg/core/siddhar.jsonl` contain it; the checker recounts |
| `status`, `history` | the review state, and a list of `{"version", "status", "by", "note"}` changes |

A layer reading that rests on the second sense of such a word must cite the entry, and an entry's
`uses` must match the citations exactly. The lexicon's **acceptance rate** (accepted / reviewed) is
the metric for how far its double readings hold up under review; entries still `proposed` are not
counted in it.

## The shared-key link

`shared_key` is a seventh link type, for two verses that **decode together under one key**: read
with that key, they make the same claim or use the same figure, and at least one of them needs the
key to be read that way (if both state the key openly, the link is an ordinary `agrees` or
`same_image` that may list the key for reference). Example: two verses that speak of the sun and
the moon decode together under `sun_moon` as the two breaths. A shared-key link must:

- list the key in `keys`, and the key must appear in the named layer's `keys` on every pilot verse
  it joins;
- say in the note what each verse says before the key and after it;
- carry the confidence of its weaker end; a shared-key link between two `low` readings is not worth
  proposing.

A shared-key link is honest about being a cipher link. Graders judge whether the key is
traditional and fairly applied, not whether the plain senses match.

## Body place

`body_place` lists the places in the body the verse locates itself in, for a later body atlas:
which ஆதாரம், nadi, gate or tattva the verse names or, under a key, points to. `[]` if none. Each
entry: `place` (an id from the table), `tamil` (the words, copied from the verse), `basis`
(`named` if the verse names it, `key` if a cipher key supplies it) and `confidence`.

<!-- places -->
| place | kind | Tamil |
|---|---|---|
| `muulaadhaaram` | aadhaaram | மூலாதாரம், the root centre |
| `suvaadhittaanam` | aadhaaram | சுவாதிட்டானம் |
| `manipuuragam` | aadhaaram | மணிபூரகம், the navel centre |
| `anaagatham` | aadhaaram | அநாகதம், the heart centre |
| `visuththi` | aadhaaram | விசுத்தி, the throat centre |
| `aakkinai` | aadhaaram | ஆக்கினை, the brow centre |
| `aadhaaram_six` | aadhaaram | the six centres as a set (ஆறு ஆதாரம்) |
| `crown` | aadhaaram | the crown, உச்சி, சிரம், பிரமரந்திரம், the thousand-petalled |
| `suzhumunai` | naadi | சுழுமுனை, the central channel (மூலநாடி) |
| `idai_pingalai` | naadi | இடை and பிங்கலை, the left and right channels |
| `ten_nadis` | naadi | the ten nadis (தசநாடி) |
| `nine_gates` | opening | the nine openings of the body |
| `nose_tip` | region | நாசிமுனை, the tip of the nose |
| `brow` | region | the point between the eyes |
| `heart` | region | the heart (இதயம், நெஞ்சு) as a place |
| `three_mandalas` | region | the three regions of sun, moon and fire |
| `tattva_elements` | tattva | the five elements (பூதம்) |
| `tattva_senses` | tattva | the organs of knowledge (eye, ear, nose, tongue, skin) |
| `tattva_action` | tattva | the organs of action (வாக்காதி) |
| `tattva_subtle` | tattva | the five subtle elements (சத்தாதி, tanmatra) |
| `tattva_36` | tattva | the tattvas as a whole (ஆறாறு, தத்துவம்) |
| `humours` | tattva | the three humours (வாதம், பித்தம், கபம்/கோழை) |
| `body_whole` | whole | the body as such, 'within you', when no place is named |
<!-- /places -->

## Knows by

`knows_by` records how the verse says the thing is known, as a list of `{"mode", "stance",
"tamil"}`. `mode` is one of `senses`, `inference`, `teacher_or_book` and `direct_experience`.
`stance` is `relies` (the verse knows or tells us to know this way), `rejects` (it says this way
fails) or `reports` (it names the way without judging it). `tamil` lists the words that show it.
`[]` when the verse is silent about knowing; most invocations and catalogues are.

`direct_experience` is the verse's own claim (கண்டேன், உணர்ந்தேன், தெரிசித்தேன்), not our
judgment that the poet had an experience. `teacher_or_book` covers the guru, the sastras, the
Agamas and 'what was heard'.

## Links

Links may join two pilot verses (`"b": 1400`) or point to the four marked books (`"b":
"kural:350"`, `"naladiyar:47"`, `"tirumanthiram:975"`, `"thiruppugazh:894"`). At most three per
verse as `a`. Read the other verse before linking (`python3 -I scripts/verse.py tirumanthiram:975`).

| field | meaning |
|---|---|
| `a`, `b` | as in the flat marks |
| `type` | `tension`, `agrees`, `develops`, `qualifies`, `same_image`, `parallel_domain` or `shared_key` |
| `layer` | the one layer the link depends on. It must be present on `a`, and on `b` when `b` is a pilot verse. |
| `also_holds_on` | other layers on which the link also holds by itself, often `["literal"]`. `[]` means the link depends on one layer only. |
| `keys` | keys the link uses; required and non-empty for `shared_key` |
| `confidence` | the link's own confidence, no higher than the named layer's on either pilot end |
| `note` | what each verse says on that layer and what the pairing teaches. For a link on a coded layer, say what each verse says before the key. |
| `origin` | `kept` (an old link re-proposed with its old note), `renoted` (an old pair with a new layer, type or note) or `new` |
| `stances` | the stance lists of `a` and `b` (see Stance) |

`tension` keeps its old test: incompatible claims on at least one defensible reading, and the note
says which layer the conflict lives on. Two verses that share a stock attack on ritual are a
`social` link and are weak unless the pairing teaches something specific; the layer label does not
rescue them.

## Old links

Each chapter file reviews every old link that touches its verses (from the chapter's own file and
from other chapters), in `old_links`: `a`, `b`, `type`, `old_grade` (from
`kg/siddhar/link_audit.json`), `layer` (the layer it in fact depended on), `verdict` and
`action`, with `stances` and a `note`.

- `verdict`: `holds_literal` (holds on the plain words), `holds_on_layer` (holds on a non-literal
  layer that the Tamil supports), `cipher_artefact` (holds only under a key the Tamil does not fix,
  or joins two things that only share a coded word or number), `stock_attack` (a shared stock
  attack on ritual, caste or learning), `generic` (a shared commonplace), `misread` (one verse
  misdescribed).
- `action`: `kept`, `renoted`, `dropped`, or `out_of_scope` (the other end is a Siddhar verse
  outside the pilot, so the link is reviewed but not re-proposed).

## Rules

- Do not edit the flat marks, the graphs, `viz/` or `kg/themes/concepts.json`. Propose new concepts
  in the pilot's findings.
- Readings are your own words. No glosses quoted; no commentary exists for this corpus.
- **Alchemy and medicine are history.** Read a formula for its claim and its reasoning; never
  give a recipe, a quantity, a dose or a use. The checker rejects alchemy readings with dosage
  words.
- A low-confidence layer is worth recording: it shows where a reading would need a key. A link
  on it is usually not worth proposing.
- Do not commit.
