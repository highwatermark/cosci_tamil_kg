# Brief: marking the epics

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph builds a knowledge graph of the
meanings, themes and threads of Tamil literature. The Kural, Naladiyar, Tirumanthiram, Thiruppugazh
and Siddhar songs are marked and linked, and the Sangam books are being marked. You are marking one
of the ten epics: the five great (ஐம்பெருங்காப்பியம்) and the five minor (ஐஞ்சிறுங்காப்பியம்).

| Book key | Work | Core file | Unit and verse key |
|---|---|---|---|
| `silappathikaram` | Silappathikaram | `kg/core/silappathikaram_units.jsonl` | 434 reading units of the patikam, 30 kaathais and the closing pieces; key `silappathikaram:<kaathai>:<start>-<end>` |
| `manimekalai` | Manimekalai | `kg/core/manimekalai_units.jsonl` | 288 reading units of the patikam and 30 kaathais; key `manimekalai:<kaathai>:<start>-<end>` |
| `civaka_cintamani` | Civaka Cintamani | `kg/core/civaka_cintamani.jsonl` | 3,145 verses in 13 ilampakams; verse number |
| `valayapathi` | Valayapathi | `kg/core/valayapathi.jsonl` | 72 surviving verses (with `quoted_in`, the work that preserved each); verse number |
| `kundalakesi` | Kundalakesi | `kg/core/kundalakesi.jsonl` | 19 surviving verses; verse number |
| `soolamani` | Soolamani | `kg/core/soolamani.jsonl` | 2,128 verses in 12 sarukkams; verse number |
| `neelakesi` | Neelakesi | `kg/core/neelakesi.jsonl` | 885 verses in 10 sarukkams, most of them debates; verse number |
| `naga_kumara_kaviyam` | Naga Kumara Kaviyam | `kg/core/naga_kumara_kaviyam.jsonl` | 171 verses in 5 sarukkams; verse number |
| `udayana_kumara_kaviyam` | Udayana Kumara Kaviyam | `kg/core/udayana_kumara_kaviyam.jsonl` | 367 verses in 6 kandams; verse number |
| `yasodhara_kaviyam` | Yasodhara Kaviyam | `kg/core/yasodhara_kaviyam.jsonl` | 330 verses in 5 sarukkams; verse number |

The epics teach by story. Their group's concern (`docs/corpus-groups.md`) is justice, karma and
renunciation, and the Jain and Buddhist ethics behind them; the minor epics add doctrine and
open debate. So besides the house fields (reading, nuance, concepts, uncertain, links) every unit
records who speaks, who acts, what happens, and what doctrinal or ethical claims it makes, and for
which school.

## Read first

- `kg/themes/SCHEMA.md`: the house marking rules. Follow them, with the changes below.
- `docs/sangam-marking-brief.md`, the last section, "Lessons from grading round 1", and its
  Pattupattu notes (the unit rule there is the unit rule here).
- `docs/siddhar-marking-brief.md`: renunciation, the body and karma in the Siddhars, where several
  of your bridges go.
- `docs/corpus-groups.md`: the epics are two groups (great and minor); one bridge it tests is "epics'
  karma and renunciation to the Siddhars and Naladiyar".
- `kg/themes/concepts.json`: the shared list of 264 concepts. Reuse ids: oozh, vinai, piravi,
  marumai, naragam, veedu, aram, sengol, kodungol, arasu, vendhan, karpu, nirai, thuravu, thavam,
  kollaamai, pulaal, nilaiyaamai, yaakkai, samayam, nindhai, eegai, pasi, arul, kaamam, pirivu,
  saakkaadu, kootru, anangu, vazhipaadu, iraivan and the rest. Add a concept only when none fits, and
  name what the text names. Likely additions: பத்தினி (the chaste wife whose word has power), நோன்பு
  (the vow), அளவை (the means of valid knowledge, Manimekalai 27 and 29), சார்பு (dependent arising,
  Manimekalai 30), வாதம் (formal debate: the Neelakesi's sarukkams are named for it), உண்ணாநோன்பு
  or வடக்கிருத்தல் (death by fasting) if the verse uses the word. Declare each in `new_concepts` and
  tag it only on your own verses.

## Commands (from the repository root)

- Chapters: `python3 -I scripts/book_marks.py manimekalai chapters`
- Your chapters' units or verses, with line numbers, block labels and text flags:
  `python3 -I scripts/book_marks.py manimekalai show 27`
- Validate: `python3 -I scripts/book_marks.py manimekalai check 27`
- Marked verses of the other books: `python3 -I scripts/verse.py kural:55 naladiyar:42 tirumanthiram:2104`
- An index of every marked Kural, Naladiyar, Tirumanthiram and Thiruppugazh verse, one line each:
  `python3 -I scripts/book_marks.py index <your scratch dir>/index.txt`, then grep it. Marked Siddhar,
  Purananuru and Akananuru chapters are in `kg/themes/<book>/chNNN.json`.

If `chapters` says the book is unknown, the tool support for the epics has not landed yet: stop and
report it. Do not write a checker of your own.

Chapters: for the Silappathikaram and Manimekalai, one kaathai (long kaathais split into runs of at
most 24 units); for the verse epics, one section (ilampakam, sarukkam or kandam), split into runs of
at most 25 verses; Valayapathi in runs of 25, Kundalakesi as one chapter.

## Units

**Silappathikaram and Manimekalai are marked by reading unit.** The units were cut by the same
script as the Pattupattu's (`scripts/build_epics_core.py`): 10 to 25 lines, at the line that most
strongly closes a sentence, never across a change of metre or a rubric (வேறு, வெண்பா, உரைப்பாட்டு
மடை). Every numbered song of a vari or kuravai and every closing venba is its own unit, however
short: the Kaanal Vari, Vettuva Vari, Aaychiyar Kuravai, Kunra Kuravai and Vaazhthu Kaathai songs are
units of four to eight lines, and that is right. `show` prints each unit's break score (3 strong,
0 none).

- **You may move a boundary of an akaval unit to a sense break,** as in the Pattupattu: rename the
  units by their new line spans, give each moved unit a `unit_note` (which boundary moved, which line
  ends the sentence), keep every adjusted unit at 6 to 30 lines, cover the chapter's lines with no
  gap or overlap, and never move a boundary across a kaathai, a block or a song. Links to a moved
  unit use its new id.
- Line numbers are the kaathai's own (1-based), as `show` prints them.
- Silappathikaram 22 (அழற்படு காதை) has lines the edition marks as later additions
  (`interpolation_note_lines`: 17-33, 37-50, 67-84, 89-96, 111). Mark them, and say in `nuance` that
  the edition doubts them; do not build a claim or a link on them alone.

**The other eight are marked by verse.** A verse of the Cintamani or Soolamani is usually one
moment of a long scene; mark what it adds. Consecutive verses that only continue a description may
share `event` and concepts.

**Valayapathi and Kundalakesi are fragments.** The verses survive because later works quoted them
(`quoted_in`: mostly the anthology புறத்திரட்டு). Their order is the editor's, and the story cannot be
rebuilt from them. Set `event` to `null` unless the verse itself tells an event, do not guess a
speaker from what the lost story is said to have been, and put a fragment's claim in `claims` like
any other.

## Copyright

Only the Tamil verse lines and traditional facts (book, section, number, the rubric of a song) are
in the core files. The build read editions that carry commentary or prose (P. V. Somasundaranar on
the Cintamani, Avvai Duraisamy Pillai on Yasodhara Kaviyam, a modern prose rendering of Naga Kumara
Kaviyam, the commentary of the Kundalakesi and Udayana Kumara Kaviyam editions) and kept none of it.

- **No translation** in your files, Tamil or English, and none used for wording: not V. R.
  Ramachandra Dikshitar's 1939 Silappathikaram, not any later one, not any you remember.
- **No commentary text**, old or modern: not Adiyarkku Nallar or the Arumpadavurai on the
  Silappathikaram, not Naccinarkkiniyar on the Cintamani, not the commentaries named above. Do not
  open the mirrored e-texts in `data/text/` to read them.
- The Tamil verse is public domain. Readings, events and claims are your own words.

## What a chapter file looks like

`kg/themes/<book key>/chNNN.json`, with the house fields `chapter_no`, `chapter_theme`, `verses`
(keyed by unit id or verse number), `links`, `new_concepts`, `source_issues`, and a `cast` list (below).
No `positions` and no `contested`.

### Fields of every unit or verse

| Field | Required | What goes in it |
|---|---|---|
| `reading` | yes | one sentence on what the unit says or does, in your own words |
| `concepts` | yes | 1 to 4 concept ids, most central first |
| `nuance` | no | what a quick reader would miss; omit unless there is something real to say |
| `uncertain` | no | `true` when the sense turns on a corrupt line, a rare word, a doubtful speaker or a reading you cannot fix |
| `speaker` | yes | who speaks the unit; see below |
| `agents` | yes | the characters who act in the unit; `[]` if none |
| `event` | yes | what happens, in one line; `null` for pure description, praise or argument with no event |
| `claims` | yes | doctrinal or ethical claims stated in the unit; `[]` if none |
| `echoes` | when present | words matching a Kural couplet or Naladiyar quatrain; see below |
| `unit_note` | moved units | as above |

### `speaker` and `agents`

`speaker` is `{"who": id, "form": "Tamil as written" or null, "line": n or null, "addressee": id or null}`.
`who` is `narrator` for the poet's own voice (the narration of the Silappathikaram and Manimekalai,
the verse epics' storytelling), or a character id from the chapter's `cast`. `form` and `line` give
the words that name the speaker, when the text names one (check finds them); a speech whose speaker
is known only from the story so far gets `form: null`. In the songs, the singer may be a group (the
herdswomen of the kuravai, the hunters of the vari): give the group an id in `cast`.

`agents` is a list of `{"id", "form", "line"}`: each character who acts in this unit (not one who is
only mentioned), with the word that names them on that line. A character acting without being
named in the unit gets `form: null`.

`cast` (one per chapter file) defines each id once: `{"id": "kannaki", "tamil": "கண்ணகி", "role":
"Kovalan's wife"}`. Ids are lowercase romanized names, reused across chapters and kept the same in
every chapter of a book (look at the book's earlier chapter files before coining one). Gods,
deities and groups may be cast too (`manimekala_deyvam`, `kuravai_women`).

### `event`

One line, plain past or present tense, naming who does what: "Kovalan sells Kannaki's anklet to the
royal goldsmith, who accuses him of theft." Not a summary of meaning (that is `reading`) and not a
judgment.

### `claims`: doctrinal and ethical claims

A list of `{"claim", "school", "line", "stance", "voiced_by"}`, one object per claim the unit states
(not one it merely illustrates):

- `claim`: the claim in a short English clause of your own ("deeds of a former birth ripen and must be
  eaten", "a wife who worships only her husband commands the rain", "the soul is not other than the
  body").
- `school`: `jain`, `buddhist`, `vedic`, `saiva`, `vaishnava`, `ajivika`, `lokayata` or `general` (an ethical
  claim not tied to a school: a king's duty to protect, the wrong of false witness). Give the school
  the claim belongs to as the text presents it, not the work's own affiliation. Sankhya, Vaisheshika,
  Nyaya, Mimamsa and Vedanta are `vedic`; the materialists (பூதவாதம், Lokayata) have their own value, `lokayata`. Name
  the sub-school in `school_detail` (`sankhya`, `vaisheshika`, `nyaya`, `mimamsa`), which
  is optional elsewhere.
- `line`: the line where the claim is stated (`show`'s numbers; for a verse epic, 1 to 4).
- `stance`: `asserted` (the work, through its narrator or a speaker it endorses, holds the claim),
  `refuted` (the claim is put in order to be answered: the pūrvapakṣa of a debate), or `reported`
  (a character holds it and the work neither endorses nor answers it here).
- `voiced_by`: the cast id of the one who states it.

**Polemic presents the rival school through its own eyes.** The Neelakesi's account of Buddhism is
a Jain's account; Manimekalai 27's accounts of the other schools are a Buddhist's. Record what the
text says the school holds, with `stance: "refuted"`, and say in `nuance` when the account is one
the school itself would not accept, if the Tamil shows it. Never present a polemic's version of a
school as that school's doctrine.

### `echoes`: the epics' borrowings from the Kural and Naladiyar

The epics quote and echo the Kural. Mark an echo **only when the words match**: a run of at least
four words, or a whole line, that is the couplet's or quatrain's own wording, allowing for the
editions' different word division and sandhi. A shared idea in other words is not an echo; it may be
a link.

    "echoes": [{"b": "kural:55", "line": 59, "words": "தெய்வம் தொழா அள் கொழுநன் தொழுது எழுவாள்",
                "kind": "quote", "marked": "பொய்யில் புலவன் பொருளுரை"}]

- `words`: the unit's words as written (check finds them); `b`: the couplet or quatrain.
- `kind`: `quote` (the unit sets the words off as a saying: an introducing or closing phrase such as
  என்ற, a named source) or `echo` (the words appear in the unit's own sentence).
- `marked`: the words that introduce the quotation, or `null`.

Worked example. Manimekalai 22, lines 59 to 61: a speaker urges a woman to trust the word of "the
poet who never lies" (பொய்யில் புலவன்) and gives Kural 55 almost whole: the wife who rises worshipping
her husband rather than a god can bid the rain fall. Mark it as a `quote` of `kural:55`, add a claim
(`school: "general"`, `stance: "asserted"`), and consider a link: the epic applies the couplet as a
test a woman has failed, which the couplet alone does not show.

## What matters most

Read for these five, and mark them with care when a unit carries one:

1. **Karma (ஊழ்வினை).** The Silappathikaram's patikam sets its three morals at lines 55 to 57:
   அரைசியல் பிழைத்தோர்க்கு அறம்கூற்று ஆவதூஉம், உரைசால் பத்தினிக்கு உயர்ந்தோர் ஏத்தலும், ஊழ்வினை
   உருத்துவந்து ஊட்டும் என்பதூஉம். Track where the story says a past deed comes to fruit, who says so,
   and whether a character's own choice is also blamed. Tag `oozh` and `vinai`, and record the claim.
   Mark in `nuance` the places where karma and the king's fault are both given as the cause.
2. **Justice: அறம் and the king's sceptre.** Silappathikaram 20: Kannaki's plea names the Chola who
   relieved the bird's distress and the one who put his own son under the chariot wheel for a calf
   (lines 61 to 65), says her husband came to Madurai driven by ஊழ்வினை (line 69), and the Pandya
   gives his own verdict, யானோ அரசன் யானே கள்வன் (line 85), and dies. Also Manimekalai's prison
   turned into a hall of charity (Manimekalai 19). Tag `sengol`, `kodungol`, `aram`.
3. **Chastity (கற்பு).** Kannaki's karpu as power (the rain, the burning of Madurai), Madhavi's and
   Manimekalai's turn from the courtesan's life, the Cintamani's eight marriages. `karpu` is glossed
   as a wife's steadfastness; tag `nirai` for self-containment, and add பத்தினி if the text names it.
   Report the epic's view of women's virtue as the epic's view.
4. **Renunciation.** Madhavi and Manimekalai taking robes, Civakan's last ilampakam (முத்தி
   இலம்பகம்), the Soolamani's துறவுச் சருக்கம், the deaths by fasting. Tag `thuravu`, `thavam`,
   `veedu`, `nilaiyaamai`, `yaakkai`.
5. **Debate between schools.** Manimekalai 27 (சமயக் கணக்கர் தம் திறம் கேட்ட காதை), 29 and 30;
   the Neelakesi's nine debate sarukkams after its opening sermon (with Kundalakesi, Arkkachandra,
   Mokkala, the Buddha, the Ajivikas, Sankhya, Vaisheshika, the Veda and the materialists); the
   Kundalakesi fragments. Here nearly every verse has a `claims` entry,
   and `stance` matters more than anywhere else.

Two cautions:

- **The works' affiliations are tradition, and not all settled.** The Cintamani, Valayapathi, the
  Neelakesi and the five minor epics are Jain works by tradition; the Manimekalai and Kundalakesi are
  Buddhist; the Silappathikaram's affiliation is debated. Do not tag a claim with the work's school
  unless the unit makes it.
- **Same name is not same person.** The Silappathikaram's Pandya Nedunjeliyan is not the
  Purananuru's Talaiyalanganattu Nedunjeliyan; a Karikalan or Senguttuvan named in an epic may be
  the Sangam king or a later memory of him. Say which the Tamil supports before linking.

## Links

`links` is a list of `{"a", "b", "type", "note", "teaches"}`, with one more field, `gains`, for
bridges. Types as in SCHEMA.md: `tension`, `agrees`, `develops`, `qualifies`, `same_image`,
`parallel_domain`. At most three links per unit or verse. `teaches` is required: one sentence that
says what a reader learns from the pairing that neither verse shows alone; check rejects one under
six words or one that repeats the note.

`b` may be a unit or verse of your epic (an integer, or a unit id), another epic
(`neelakesi:212`, `manimekalai:27:1-17`), or a marked book: `kural:N`, `naladiyar:N`,
`tirumanthiram:N`, `thiruppugazh:N`, `siddhar:N`, `purananuru:N`, `akananuru:N`,
`pattupattu:<poem>:<start>-<end>`. Read the other verse before linking.

1. **Within the epic (plot).** The graph already knows the order of units; sequence alone is not a
   link. Link two units of one epic when the later one answers, fulfils or reverses the earlier: a
   dream or prophecy and its event (Kannaki's dream in Silappathikaram 9), a curse of a former birth
   and its fruit, a vow and its keeping, a claim a character makes and a later scene that refutes it.
   `develops` for fulfilment, `tension` for a reversal or a claim the story contradicts, `same_image`
   for a recurring thing that changes meaning (the anklet, the begging bowl அமுதசுரபி). Links between
   epics (Manimekalai continues the Silappathikaram's story; Neelakesi answers Kundalakesi) count
   as within the group.
2. **The Kural and Naladiyar.** Where the epic tells as a story what a couplet states as a rule, or
   quotes it. A story that merely illustrates a virtue the couplet praises is weak (round 1: "agrees"
   was sound only 39% of the time). It is sound when the story tests the rule, limits it, or shows its
   cost: Kannaki's karpu against Kural 55, the Pandya's death against the Kural's chapter on the bent
   sceptre, a Jain epic's renunciation against the Kural's defence of the householder. Prefer
   `qualifies` and `develops`.
3. **The Siddhars and the Tirumanthiram.** On renunciation, karma and the body: Manimekalai's burning
   ground (சக்கரவாளக் கோட்டம், Manimekalai 6) against the Siddhars on the body as a perishable frame;
   the Jain epics' karma that must be worn away against Tirumular's grace that burns it; the attacks
   on sacrifice (Yasodhara Kaviyam) against Sivavakkiyar's attack on ritual. These are the bridge
   `docs/corpus-groups.md` tests, and the place where a real `tension` is most likely: Jain and
   Buddhist release without a god against the Saiva texts' release by grace.
4. **The Purananuru.** Kings and gifts: an epic king's justice or bounty and a Purananuru poem on the
   same king or the same act. A named king (Karikalan, the Chola of the dove) is a real link if the
   note says what the epic does with the Sangam memory. "Both praise a just king" is not.

**Bridges must say what each side gains.** A link from an epic to a book outside the two epic groups
(the Kural, Naladiyar, Siddhars, Tirumanthiram, Thiruppugazh, the Sangam books) must carry

    "gains": {"a": "what the epic unit gains from the pairing",
              "b": "what the other verse gains from it"}

each a clause of its own. If one side gains nothing (the epic only illustrates the couplet), the
link is weak; make it only if `teaches` can still name something specific.

## Rules

- Read the Tamil first. Nothing in the corpus explains it for you.
- Every Tamil word you put in a field must be in the unit or verse as written: `speaker.form`,
  `agents[].form`, `echoes[].words` and `echoes[].marked` are checked on their lines.
- Doctrine is reported, not endorsed: a reading says "the narrator holds" or "the Jain teacher
  argues", and `stance` says whose claim it is. Do not settle the debates.
- Record corrupt lines, doubled units, misnumbering and doubtful song boundaries in `source_issues`.
  `show` prints each text flag (there are many for the Cintamani and Soolamani).
- Do not edit any file except your own chapter files. Do not commit.
- When every file passes `check`, reply with only: the chapters done, new concept ids, link counts
  (within the epic, to other epics, to the Kural, Naladiyar, Siddhars, Tirumanthiram, Purananuru and
  each other book), claim counts by school and by stance, echoes found (with couplet numbers), how
  many units you adjusted, how many you marked uncertain, and text problems.
