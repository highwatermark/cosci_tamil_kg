# Brief: grading ethics-work links and the counted fields

You are grading marks in a knowledge graph of the meanings and themes of Tamil literature. Your
packet comes from the nine short ethics works of the Pathinenkilkanakku: Nanmanikkadigai
(`nanmanikkadigai:N`), Innaa Narpathu (`innaa_narpathu:N`), Iniyavai Narpathu (`iniyavai_narpathu:N`),
Thirikadugam (`thirikadugam:N`), Acharakkovai (`acharakkovai:N`), Pazhamozhi Nanooru
(`pazhamozhi_nanooru:N`), Sirupanchamoolam (`sirupanchamoolam:N`), Muthumozhikkanchi
(`muthumozhikkanchi:N`) and Elathi (`elathi:N`). Another agent marked each verse by
`docs/ethics-marking-brief.md` and proposed the links. Your job is an independent, careful judgment.
Grade on the merits: don't aim for any particular share of passes or failures. Read only your
packet. Do not edit any file in the repository.

The packet has up to two parts. **Part A** is links. **Part B**, when present, is a blind re-tag of
the fields new to this group (`domain`, the counted `items`, `norm`, and Pazhamozhi's story), for
measuring agreement; there you see the verse but not the marker's tags.

**Nothing in the corpus explains these verses.** There is no commentary in the packet. The marked
readings were written by Claude agents, by the same agent that proposed the link, so they are a
claim to check, not evidence. Read the Tamil first. Pope's renderings of the Kural and Naladiyar,
which the packet prints, are a nineteenth-century translation that sometimes adds ideas; they do not
decide what a verse says. Do not use or quote any modern translation or commentary, including any you
remember: your reasons cite the Tamil.

## Part A: links

Each link starts from an ethics-work verse and points to another verse of the nine works, or to the
Kural (`kural:N`), the Naladiyar (`naladiyar:N`), the Purananuru (`purananuru:N`) or another marked
book. Each has a type, the proposer's `note`, and a `teaches` sentence that says what the pairing
teaches. A link to the Kural or Naladiyar also has `list_adds`: what the ethics verse's list does that
the couplet or quatrain does not. A link may name `item`: which of the verse's counted things it is
about. For both verses the packet prints the Tamil and the marked reading, and for an ethics verse
its `items`, `domain` and, for Pazhamozhi, the proverb.

What to watch for in this group:

- **A shared virtue word is not a link.** These works and the Kural share a small vocabulary:
  கல்வி, நட்பு, ஈகை, பொறை, இன்சொல், கொல்லாமை. Two verses that both praise learning, or both condemn
  anger, are at best weak unless `teaches` names something the pairing shows: a condition, a cost, a
  ranking, a change of domain. In round 1 of the Sangam grading, "agrees" links were sound only 39% of
  the time, and this was why. A `teaches` that restates the shared virtue in grander words is the
  commonest failure.
- **Agrees, qualifies or contradicts.** The marker had to say which. Check it against both texts. A
  verse that adds a condition the couplet lacks is `qualifies`, not `agrees`. A `tension` must be an
  incompatible claim on at least one defensible reading; different advice for different audiences
  (the king and the ascetic, the householder and the renouncer) is not a tension unless the two claim
  to cover the same case.
- **`list_adds`.** It must be true of the verse and must name what the grouping does (ranks the
  things, makes unlike things one kind, sets a virtue among its causes or fruits, carries it into
  another domain, turns on the last item). "It lists several virtues" is not an answer. If `list_adds`
  is empty talk and the claim is the same as the couplet's, the link is weak at best.
- **`item`.** If the link names an item, the item must carry the connection. A link that names
  item 2 but rests on item 4 is wrong on that point; grade it as you would a note with a false claim.
- **Ritual and birth rules.** A link from an Acharakkovai rule (or any purity, caste or gender rule)
  must treat the rule as a historical norm the text states. A note that endorses the rule, or that
  restates it as advice, is wrong on that point. A `tension` between a birth-rank rule and the Kural's
  பிறப்பொக்கும் (972) or a Siddhar's attack on caste is sound only if both speak of the same thing:
  a purity rule about the body after eating and a verse on inner purity are different things.
- **Pazhamozhi stories.** If a note leans on an identification the verse does not make (naming the
  king the verse calls only சோழன்), say so: that is tradition about the verse, not the verse.
- **Puram links.** A link to the Purananuru is sound when the two meet on a specific act or person
  (a rule a named patron keeps, a king the Pazhamozhi story names). "Both praise giving" is weak.
- Earlier graders were too lenient: a link that needs a generous reading is weak, not sound.
  Dropped vowel signs and split words are common in these texts; if a verse looks corrupted, say so in
  `text_issue` instead of building on it.

### Link types

- tension: the two verses make incompatible claims about the same thing, on at least one defensible
  reading. Shared words, a shared topic, or different advice for different situations are NOT
  tensions. The note should say which reading the conflict depends on.
- agrees: they make the same claim, and pairing them teaches something (e.g. it appears in
  different books, domains or periods).
- develops: one extends, deepens or applies the other's idea.
- qualifies: one limits or adds a condition to the other.
- same_image: they share a distinctive image, word or figure, and the shared use is meaningful.
- parallel_domain: the same pattern or logic appears in a different domain (the king's and the
  householder's, for instance).

### Grades

- sound: the connection is real, the type fits, the note is accurate about both verses, `teaches`
  is true and specific (a reader learns something from the pair that neither verse shows alone), and
  `list_adds`, where required, is true.
- weak: a real connection, but thin or generic; or the note overstates it; or `teaches` is only the
  shared virtue; or `list_adds` says nothing; or it would be sound under a different type (give
  better_type).
- forced: depends on stretching a word, a reading or a traditional identification; or it is only a
  shared virtue word dressed up as more.
- wrong: misreads or misdescribes a verse, cites the wrong text, names the wrong item, presents a
  ritual or birth rule as advice, or claims something the verses contradict.

Grade the link as written, every field included. A true connection with a false claim in the note
is weak or wrong depending on how central the false claim is. A fluent, careful-sounding note is not
evidence: check each claim it makes against the Tamil.

### Output for Part A

A JSON array, one object per link, in packet order:

    {"a": "acharakkovai:6", "b": "kural:972", "type": "TENSION", "grade": "sound|weak|forced|wrong",
     "better_type": null or a lowercase type name,
     "teaches_holds": true or false,
     "list_adds_holds": true, false, or null when the link has no list_adds,
     "reason": "two or three sentences citing the deciding Tamil words",
     "text_issue": null or a short note on a corrupt line}

Write `a` and `b` exactly as the packet's LINK header shows them, as strings. `teaches_holds` is
false when the `teaches` sentence is untrue, or is only the shared virtue. `list_adds_holds` is false
when `list_adds` is untrue of the verse or names nothing the list does.

## Part B: blind re-tag of the counted fields

The marking brief adds four fields for this group. Part B measures whether two readers apply them
the same way. For each verse you see its Tamil with line numbers, the work, and (for Pazhamozhi) the
editor's heading. Apply the rules below yourself. Do not guess what the marker said.

**`domain`.** Who the counsel is for, by its audience, not its topic: `king` (the ruler and those in
his service: minister, envoy, soldier, courtier), `householder` (marriage, guests, kin, earning and
giving from the house), `ascetic` (the one who has renounced), `all` (anyone), `ritual-conduct`
(rules of bodily and ritual conduct: purity, eating, bathing, the hours, the directions, what not to
look at or touch). One value; if the items address different audiences, give the one most of them
address.

**`items`.** The counted things, in order, each as the first Tamil words that name it and its line.
Count by the Tamil: the verse's own count word (இம்மூன்றும், இவ்வைந்தும், இவைஎட்டும்) if it has one,
else the predicates the lines repeat (இன்னா, இனிது). Expected: Thirikadugam 3, Nanmanikkadigai 4,
Innaa Narpathu 4, Iniyavai Narpathu 3 or 4, Sirupanchamoolam 5 or 6, Elathi 6 or 5, Muthumozhikkanchi
1, Acharakkovai only when it counts, Pazhamozhi none. If your count differs from the expected one,
say why in `note`.

**`norm`.** Required when the verse states a rule of purity, pollution, birth, varna or gender:
`kinds` from `purity`, `caste`, `gender`, `ritual`, `diet`. `null` when it states none (an
Acharakkovai verse on gratitude or patience has none). A word that ranks people by birth (புலை,
புலையன், பார்ப்பார் used in a rule) makes it `caste`.

**Pazhamozhi `story`.** The proverb (the quoted words, with their lines) and what it is applied to:
`kind` is `named` (a person or episode the verse names or plainly points to), `exemplum` (an unnamed
but specific case) or `general` (no story; applied to a type of person). `who` is Tamil words from
the verse or `null`. Use only what the verse says; do not supply a name from tradition.

### Output for Part B

A JSON array, one object per verse, in packet order:

    {"id": "acharakkovai:6",
     "domain": "ritual-conduct",
     "items": [["புலை", 1], ["திங்கள்", 1], ["ஞாயிறு", 1], ["நாய்", 1], ["தக்கவீழ் மீனோடே", 2]] or null,
     "count_word": "இவ்வைந்தும்" or null,
     "norm": null or {"kinds": ["purity", "caste"]},
     "pazhamozhi": null or {"proverb_lines": [3, 4], "kind": "named", "who": "சோழன்"},
     "note": "one sentence if a rule was hard to apply here, else null"}

## When you finish

Validate that the file parses as JSON and that its counts match the packet's LINK headers and
VERSE headers. Write it to the output path you were given. Then reply with only: the counts by grade,
how many `teaches` and how many `list_adds` failed, and for Part B your counts by domain, how many
verses you gave a `norm` (by kind), and how many item counts differed from the expected ones.
