# Brief: marking the ethics works of the Pathinenkilkanakku

The repository at /Users/harilakshmanan/Cursor/cosci_knowledge_graph builds a knowledge graph of the
meanings, themes and threads of Tamil literature. The Kural and the Naladiyar, the two long works of
the ethics group (`docs/corpus-groups.md`), are marked and linked. You are marking one of the nine
short ethics works of the same eighteen:

| Book key | Work | Core file | Verses | Form |
|---|---|---|---|---|
| `nanmanikkadigai` | Nanmanikkadigai | `kg/core/nanmanikkadigai.jsonl` | 2 invocations (0) and 104 | four "gems" per verse |
| `innaa_narpathu` | Innaa Narpathu | `kg/core/innaa_narpathu.jsonl` | invocation and 40 | four painful things per verse |
| `iniyavai_narpathu` | Iniyavai Narpathu | `kg/core/iniyavai_narpathu.jsonl` | invocation and 40 | three or four sweet things per verse |
| `thirikadugam` | Thirikadugam | `kg/core/thirikadugam.jsonl` | invocation and 100 | three things, like the three pungent drugs |
| `acharakkovai` | Acharakkovai | `kg/core/acharakkovai.jsonl` | 100 | rules of conduct, many of them ritual |
| `pazhamozhi_nanooru` | Pazhamozhi Nanooru | `kg/core/pazhamozhi_nanooru.jsonl` | payiram, invocation and 399, under 34 headings | a counsel closed by a proverb |
| `sirupanchamoolam` | Sirupanchamoolam | `kg/core/sirupanchamoolam.jsonl` | payiram, invocation and 96 | five things, like the five small roots |
| `muthumozhikkanchi` | Muthumozhikkanchi | `kg/core/muthumozhikkanchi.jsonl` | 100 lines in ten tens | one saying per line |
| `elathi` | Elathi | `kg/core/elathi.jsonl` | payiram, invocation and 80 | six things, like cardamom and its five partners |

These works teach by counting. A verse names three, four, five or six things and gives them one
predicate (they are medicine, they are painful, they are sweet, they ruin a house). So besides the
house fields (reading, nuance, concepts, uncertain, links) each verse records its counted `items`,
who the counsel is for (`domain`), and, in Pazhamozhi, its proverb and the story it is applied to.

## Read first

- `kg/themes/SCHEMA.md`: the house marking rules. Follow them, with the changes below.
- `docs/sangam-marking-brief.md`, the last section, "Lessons from grading round 1". Its numbers
  shaped the linking rules here.
- `docs/naladiyar-marking-brief.md`: how the Naladiyar was linked to the Kural. These works are linked
  the same way, with the tighter rules below.
- `docs/corpus-groups.md`: these nine works sit with the Kural and Naladiyar in one group; links to
  the Purananuru are a bridge between groups ("puram ethics of giving to the ethics works").
- `kg/themes/concepts.json`: the shared list of 264 concepts. Reuse ids: aram, ozhukkam, kalvi,
  arivu, natpu, eegai, oppuravu, inchol, porai, vekuli, kollaamai, pulaal, ilvaazhkkai, thuravu,
  thavam, arasu, sengol, amaichu, padai, kudi, pirappu, andhanar, thooimai, theettu, karpu,
  nilaiyaamai, yaakkai, oozh, vinai, marumai, kayamai, saandror and the rest. Add a concept only when
  none fits, and name what the text names. Likely additions: ஆசாரம் (rule-bound conduct, the
  Acharakkovai's own word), எச்சில் (the impurity of the mouth and hand after eating), விருந்தோம்பல்
  if `virundhu` does not cover the act, பழமொழி (the proverb as a form of proof). Declare each in the
  chapter's `new_concepts` and tag it only on your own verses.

## Commands (from the repository root)

- Chapters: `python3 -I scripts/book_marks.py thirikadugam chapters`
- Your chapters' verses, with line numbers and text flags: `python3 -I scripts/book_marks.py thirikadugam show 2`
- Validate: `python3 -I scripts/book_marks.py thirikadugam check 2`
- Marked verses of the other books: `python3 -I scripts/verse.py kural:972 naladiyar:58`
- An index of every marked Kural, Naladiyar, Tirumanthiram and Thiruppugazh verse, one line each
  (`id | concepts | reading`): `python3 -I scripts/book_marks.py index <your scratch dir>/index.txt`,
  then grep it. Marked Purananuru poems are in `kg/themes/purananuru/chNNN.json`.

If `chapters` says the book is unknown, the tool support for this group has not landed yet: stop
and report it. Do not write a checker of your own.

Chapters: Pazhamozhi by its 34 headings (`chapter_no`; long headings split at 20 verses);
Muthumozhikkanchi by its ten tens; the others in runs of 20 verse numbers, the invocation and
payiram going with chapter 1. Verse keys are the `number` field; the payiram is `payiram`.

## Copyright

Only the Tamil verse lines and plain facts (author, section, Pazhamozhi heading) are in the core
files. No modern translation, commentary or heading, in Tamil or English, goes in your files: not
Project Madurai's per-verse headings for Acharakkovai and Thirikadugam (the build dropped them; do not
fetch them), not any modern prose rendering you may remember. Readings are your own words. Pope's
translations of the Kural and Naladiyar, which `verse.py` and the grading packets print, are public
domain but are a third reading, not the verse.

## What a chapter file looks like

`kg/themes/<book key>/chNNN.json`, with the house fields `chapter_no`, `chapter_theme`, `verses`,
`links`, `new_concepts`, `source_issues`. There is no commentary in the corpus, so there are no
`positions` and no `contested`.

### Fields of every verse

| Field | Required | What goes in it |
|---|---|---|
| `reading` | yes | one sentence on what the verse says, in your own words |
| `concepts` | yes | 1 to 4 concept ids, most central first |
| `nuance` | no | what a quick reader would miss; omit unless there is something real to say |
| `uncertain` | no | `true` when the sense turns on a corrupt line, a rare word, or a reading you cannot fix |
| `domain` | yes | who the counsel is for: `king`, `householder`, `ascetic`, `all`, `ritual-conduct` |
| `domain_note` | no | one clause, when the domain needs it (e.g. "the king's minister", "a wife") |
| `items` | counted works | the counted things; see below |
| `count_word` | counted works | the verse's own count word as written (இம்மூன்றும், இவ்வைந்தும், இவைஎட்டும்), or `null` |
| `pazhamozhi` | Pazhamozhi | the proverb and the story it is applied to; see below |
| `norm` | Acharakkovai, and any verse with a ritual or birth rule | see "Ritual purity and caste" |

The invocations and payirams get the house fields and `domain: "all"`; `items` only if they count.

### `items`: the counted things

A list of `{"thing", "claim", "line"}`, one object per counted thing, in the verse's order.

- `thing`: Tamil words copied from the verse (check finds them on `line`). Keep the case ending and
  sandhi as written; do not lemmatise.
- `claim`: what the verse says of that thing, in a short English clause of your own. Where the
  verse gives one predicate to all its things (they are painful; they are a medicine), the claim is
  that predicate applied to this thing, sharpened if the thing has its own condition ("a house
  without a bond is painful" is the predicate; "beauty in a house with no tie of kin is painful"
  is the claim).
- `line`: the line number `show` prints, where the thing begins.
- `domain`: optional, only when this item's audience differs from the verse's (a Sirupanchamoolam
  verse may put the king and the ascetic side by side).

Expected counts:

| Work | Items per verse | Notes |
|---|---|---|
| Thirikadugam | 3 | closes with இம்மூன்றும் and a medicine or poison image |
| Nanmanikkadigai | 4 | each "gem" is a whole clause, often "X is born of Y" or "X is known by Y" |
| Innaa Narpathu | 4 | each line ends with இன்னா; the fourth often shares the closing line |
| Iniyavai Narpathu | 3 or 4 | each thing ends with இனிது or இனிதே |
| Sirupanchamoolam | 5 (at times 6) | count the verse's own items, not the title's five |
| Elathi | 6 (at times 5) | as above |
| Acharakkovai | when the verse counts | many verses count (இவைஎட்டும், இவ்வைந்தும்); give `items` then, else omit |
| Muthumozhikkanchi | 1 | the line's saying; `thing` is the subject, `claim` reads it with the ten's predicate (see below) |
| Pazhamozhi | none | it argues, it does not count; use `pazhamozhi` |

The verse's own count decides. If the verse says five and you find six, or the count word is
missing, give what the Tamil supports, set `count_word` as written, and say in `nuance` how you
divided the things. A different division from the traditional count is data, not an error, but it
must be defensible line by line. Check warns (it does not fail) when a count differs from the
table.

**Muthumozhikkanchi.** Each ten has a predicate in its title (சிறந்த பத்து "the ten that excel",
அறிவுப் பத்து, பழியாப் பத்து, துவ்வாப் பத்து, அல்ல பத்து, இல்லைப் பத்து, பொய்ப் பத்து, எளிய பத்து,
நல்கூர்ந்த பத்து, தண்டாப் பத்து), and the first line of each ten (ஆர்கலி யுலகத்து மக்கட்கெல்லாம்) frames
all ten. Read each saying with its ten's predicate; the reading should not repeat the frame.

### `pazhamozhi`: the proverb and its story

Every Pazhamozhi verse ends with a proverb, set in quotation marks in our text. It is the verse's
proof: the first lines make a counsel and the proverb clinches it.

    "pazhamozhi": {"proverb": "குலவிச்சை கல்லாமல் பாகம் படும்",
                   "lines": [3, 4],
                   "literal": "a family's craft is half-known without being learnt",
                   "story": {"kind": "named", "who": "சோழன்", "act": "a young Chola king, doubted by
                             grey elders, put on grey hair and judged their case to their satisfaction",
                             "tradition": "identified by tradition as Karikalan; the verse does not name him"},
                   "applied_to": "inherited capacity: the king judges well though young"}

- `proverb`: the quoted words exactly as written, quotation marks removed (check finds them).
  `lines`: the lines it spans.
- `literal`: what the proverb says taken by itself, in your own words.
- `story`: what the verse applies the proverb to. `kind` is `named` (a person or episode the verse
  names or plainly points to: a king, a figure of the epics or puranas, a Sangam patron), `exemplum`
  (an unnamed but specific case: the man who sold the boat after crossing), or `general` (no story;
  the proverb is applied to a type of person). `who` is Tamil words from the verse, or `null`. `act`
  is the episode in one clause, as the verse tells it. `tradition` is used only to report an
  identification the verse does not make; say "by tradition", and never fill a gap from a commentary.
  If you cannot tell what the allusion is, set `uncertain` and say what the words allow.
- `applied_to`: the counsel the proverb proves, in one clause.

The Pazhamozhi heading (`chapter`) is the editor's grouping of verses by theme. It is a fact of
the edition, not of the verse: if a verse's counsel does not fit its heading, say so in `nuance`.

Worked example of `general`: Pazhamozhi 1 says a man who will not learn when young cannot expect
learning to come in old age, and closes with the proverb that no toll was ever levied after the
wilderness road was crossed, nor wages taken after the tree was felled. There is no named story;
the proverb is the instance (`kind: "general"`, `who: null`).

### `domain`: who the counsel is for

| Value | Use it when the verse addresses |
|---|---|
| `king` | the ruler and those in his service: minister, envoy, soldier, courtier (say which in `domain_note`) |
| `householder` | the man or woman of the house: marriage, guests, kin, earning, giving from the house |
| `ascetic` | the one who has renounced: penance, restraint of senses, release |
| `all` | anyone: speech, friendship, learning, anger, gratitude |
| `ritual-conduct` | rules of bodily and ritual conduct: purity, eating, bathing, the hours, the directions, what not to look at or touch |

Decide by the verse's audience, not its topic: a verse on giving addressed to the king is `king`.
When a verse mixes audiences (Elathi's payiram says the work joins the householder's and the
renouncer's codes), pick the one most of its items address, and give the others per item. Domain is
graded blind, so give it on the Tamil, not on the heading.

## Ritual purity and caste

Acharakkovai is the one book in the corpus that is mostly ritual rule. Several of the other works
also carry rules about birth (Innaa Narpathu 2 on brahmins' houses; பார்ப்பார், அந்தணர், புலையர்),
about women's conduct, and about pollution. Record these as what they are: **historical norms of
the period, stated by the text**. Never present them as advice.

- **Reporting voice.** Write the reading as a report: "The verse lists five things a person in a
  state of எச்சில் does not look at", not "Do not look at the moon after eating". The same holds for
  `claim` in `items`.
- **The `norm` field**, required on every verse that states a rule of purity, pollution, birth,
  varna or gender:

      "norm": {"historical": true,
               "kinds": ["purity"],
               "note": "a pollution rule of the period: what is barred while the mouth is unclean"}

  `kinds` is one or more of `purity` (pollution and its removal: எச்சில், தீட்டு, bathing, the
  directions for bodily acts), `caste` (birth-rank: who may be seen, fed, touched or entered, and
  words like புலையர், பார்ப்பார் when they rank people), `gender` (rules for women's conduct or
  bodies, menstrual pollution included), `ritual` (offerings, mantras, the order of the day) and
  `diet`.
- **Words that rank people.** When a word for a birth-group carries a rule (புலை, புலையன்), say in
  `nuance` that it is a caste term and how it is used; mark `uncertain` if the word might be read as
  an impure thing rather than a person. Do not soften it and do not translate it as a slur.
- **Concepts.** Tag `theettu`, `thooimai`, `pirappu`, `kudi` or `andhanar` as the verse requires.
  An ethics verse in the Acharakkovai (verse 1 lists gratitude, patience, sweet speech, doing no
  harm to any creature, learning, oppuravu, wisdom and the company of the good as the eight seeds of
  ஆசாரம்) is `domain: "all"` and needs no `norm`: the book is not all ritual, and the field marks
  only the verses that are.
- **Worked example.** Acharakkovai 6: those in the state of எச்சில் do not look at five things:
  புலை, the moon, the sun, a dog and a falling star (`தக்கவீழ் மீன்`), and those who know this
  well keep it daily. `domain: "ritual-conduct"`; five `items`; `count_word: "இவ்வைந்தும்"`; `norm`
  with `kinds: ["purity", "caste"]`, because புலை here is most likely the outcaste person, and
  `uncertain: true` with that doubt said in `nuance`.
- **Links.** These verses link best where another book takes the opposite view. The Kural's
  பிறப்பொக்கும் எல்லா உயிர்க்கும் (972) and the Siddhars' attacks on caste and ritual purity
  (Sivavakkiyar; search the index for `theettu` and `pirappu`) are candidates for `tension`, if the
  two make incompatible claims about the same thing on a defensible reading. A rule about
  purity and a verse in praise of inner purity are not a tension; they are different things.

## Links

`links` is a list of `{"a", "b", "type", "note", "teaches"}`, with two extra fields for this group:

| Field | When | What |
|---|---|---|
| `item` | when the link is about one counted thing | the 1-based position in `items` |
| `list_adds` | links to the Kural or Naladiyar | one sentence: what this verse's list does that the couplet or quatrain does not |

- `a` is one of your verse keys. `b` is a verse of your book (an integer), of another ethics work
  (`thirikadugam:12`), or a marked book: `kural:N`, `naladiyar:N`, `purananuru:N`, `akananuru:N`,
  `tirumanthiram:N`, `thiruppugazh:N`, `siddhar:N`. Read the other verse before linking.
- Types as in SCHEMA.md: `tension`, `agrees`, `develops`, `qualifies`, `same_image`,
  `parallel_domain`. At most three links per verse.
- `teaches` is required: one sentence that says what a reader learns from the pairing that neither
  verse shows alone. Check rejects a `teaches` under six words or one that repeats the note.

### The main target: the Kural and the Naladiyar

These verses are four lines long and make several small claims each, so most of their links go to
the two long works of their own group. For each verse, look in the index for the Kural couplet or
Naladiyar quatrain that makes the same claim as one of its items, and decide which of three things
holds:

- **It agrees**, and the pairing still teaches something: the list puts the Kural's claim beside
  things the Kural keeps apart (Thirikadugam makes a chaste wife, the worthy of an old family and
  learned friends one medicine), or it moves a claim into another domain. Type `agrees`, or
  `parallel_domain` when the domain moves.
- **It qualifies** the couplet: adds a condition, an exception, a ranking or a cost. Type
  `qualifies` (or `develops` when it extends or applies the couplet rather than limiting it).
- **It contradicts** the couplet on a defensible reading. Type `tension`; the note says which
  reading. The Jain works here (Elathi, Sirupanchamoolam, the Naladiyar itself) often press harder on
  renunciation, non-killing and diet than the Kural; the Acharakkovai ranks by birth where the Kural
  ranks by conduct. These are the places to look.

**Avoid the generic `agrees`.** In round 1 the "agrees" links were sound only 39% of the time, and
the commonest failure was two verses that share a virtue word (கல்வி, நட்பு, ஈகை) and nothing more.
A link from a Thirikadugam verse that names learning to Kural 391 because both praise learning is
not a link. It becomes one when the verse says something about learning the couplet does not (when,
by whom, at what cost, ranked against what) and `teaches` names it. Prefer `qualifies` and `develops`
when the two differ in scope: they were sound 64% and 67% of the time.

**What the list form adds.** `list_adds` is required on every link to the Kural or Naladiyar. Say
what the grouping does: it ranks the things, it makes unlike things one kind (a wife's virtue and a
friend's learning as one medicine), it sets a virtue among its causes or its fruits, it carries the
claim into the king's or the ascetic's domain, or it adds a rhetorical turn (the last item undoes the
first). If the list adds nothing and the claim is the same, the link is weak; make it only if the
pairing teaches something else, and say what.

Worked example (our reading, offered as a model of the test). Thirikadugam 1 names three things as
like the three pungent drugs: the shoulders of a wife whose chastity is Arundhati's, keeping company
with the worthy of an old, well-ordered family, and the friendship of those whose learning clears the tangle of words. A
link to the Kural's chapter on friendship that says "both praise good friends" fails. A link to a
couplet on choosing friends by their learning, typed `develops`, with `item: 3`, and `list_adds`
"it makes a learned friend one of three remedies with a chaste wife and the worthy of an old
family, so friendship is ranked with household and lineage as a cure", can pass, if `teaches` says what the
pairing shows.

### Within the group

Links between the nine works, and within one work, are welcome when one verse sharpens another:
Innaa Narpathu and Iniyavai Narpathu often name the same thing as painful and sweet; Elathi and
Sirupanchamoolam share a Jain diet and non-killing code; Pazhamozhi applies by story what the counted
works state bare. An `Innaa` line and an `Iniyavai` line about the same thing are a real pair; the
note must say whether they say the same thing from two sides or disagree.

### The Purananuru, when specific

The bridge from puram ethics to these works was the strongest kind in round 1 (68% sound). Link a
verse to a Purananuru poem only when the two meet on a specific act or person: the same rule about
giving that a named patron keeps or breaks, a king's duty that a செவியறிவுறூஉ poem urges, a Pazhamozhi
story whose king is a Purananuru patron. A Pazhamozhi verse that names a Sangam king is the best
case: link it to the poem that names him, and say what the ethics work does with the heroic memory.
"Both praise giving" is not a link.

## Rules

- Read the Tamil first. Nothing in the corpus explains it for you.
- Every Tamil word you put in a field must be in the verse as written: `items[].thing`, `proverb`,
  `story.who` and `count_word` are checked on their lines.
- Readings and claims report the verse. They never give advice in the verse's voice, least of all
  on purity, caste, gender or diet.
- Record corrupt lines, doubled verses, misnumbering and doubtful quotation marks in `source_issues`.
  `show` prints any text flag for the verse.
- Do not edit any file except your own chapter files. Do not commit.
- When every file passes `check`, reply with only: the chapters done, new concept ids, link counts
  (within the book, to the other ethics works, to the Kural, to the Naladiyar, to each other book),
  counts by `domain`, how many verses carry `norm` (by kind), how many counts differed from the
  table, how many verses you marked uncertain, and text problems.
