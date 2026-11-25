# Brief: grading Sangam links and the experimental fields

You are grading marks in a knowledge graph of the meanings and themes of Tamil literature. Your
packet comes from one of three Sangam books: the Purananuru (`purananuru:N`), the Akananuru
(`akananuru:N`) or the Pattupattu (`pattupattu:<poem>:<start>-<end>`, a span of lines of one of the
ten idylls, numbered as in the idyll). Another agent marked each verse by
`docs/sangam-marking-brief.md` and proposed the links. Your job is an independent, careful judgment.
Grade on the merits: don't aim for any particular share of passes or failures. Read only your
packet. Do not edit any file in the repository.

The packet has up to two parts. **Part A** is links. **Part B**, when present, is a blind re-tag of
the two experimental fields, ullurai and iraicchi, for measuring agreement; there you see the poem
and its colophon but not the marker's tags.

**Nothing in the corpus explains these poems.** There is no commentary in the packet. The marked
reading, nuance and Tholkappiyam fields were written by Claude agents, by the same agent that
proposed the link, so they are a claim to check, not evidence. Read the Tamil first. The colophon
(thinai, thurai, poet, patron) is the tradition's fact; the marker's own `thinai` is an inference
and may differ from it. Do not use or quote any modern translation or commentary, including any
you remember: your reasons cite the Tamil.

## Part A: links

Each link starts from a Sangam verse and points to another Sangam verse or to a verse of the Kural
(`kural:N`), the Naladiyar (`naladiyar:N`), the Tirumanthiram (`tirumanthiram:N`), the Thiruppugazh
(`thiruppugazh:N`) or the Siddhar songs (`siddhar:N`). Each has a type, the proposer's `note`, and a
`teaches` sentence that says what the pairing teaches. For both verses the packet prints the Tamil,
the marked reading, and for a Sangam verse its colophon and, where given, its thinai, akam/puram
and uri.

What to watch for in this corpus:

- **Shared topic is not a link.** The Sangam books and the didactic books share a handful of large
  subjects: giving, death, the king, war, love's separation. Two verses that both praise giving, or
  both lament a death, are at best weak unless `teaches` names something specific that the pairing
  shows (a rule and its heroic instance, a change of attitude between periods, one book answering
  the other). A `teaches` sentence that restates the shared topic in grander words is the commonest
  failure; grade the link weak or forced.
- **Akam and the Kural's third book.** Many Akananuru situations appear again in the Kural's book
  of love. A link that only notes the same situation (the heroine waits, the friend speaks for her)
  is weak. It is sound when the two treat the situation differently or one sharpens the other.
- **Puram names.** A king, battle or town named in a Purananuru poem and again in an Akananuru
  simile is a real connection; grade whether the note says what the akam poet does with it.
- **Colophon versus poem.** If a note leans on the colophon's thurai or patron for a claim the poem
  does not make, say so: the colophon is tradition about the poem, not the poem.
- **Readings of rare words.** A link that turns on one sense of an ambiguous word (மா, ஏறு, கலை,
  அன்ன, இல) is weak or forced unless the Tamil fixes that sense.
- Earlier graders were too lenient: a link that needs a generous reading is weak, not sound.
  Base-text misprints and dropped vowel signs are common in the Purananuru; if a verse looks
  corrupted, say so in `text_issue` instead of building on it.

### Link types

- tension: the two verses make incompatible claims about the same thing, on at least one defensible
  reading. Shared words, a shared topic, or different advice for different situations are NOT
  tensions. The note should say which reading the conflict depends on.
- agrees: they make the same claim, and pairing them teaches something (e.g. it appears in
  different books, domains or periods).
- develops: one extends, deepens or applies the other's idea.
- qualifies: one limits or adds a condition to the other.
- same_image: they share a distinctive image, word or figure, and the shared use is meaningful.
- parallel_domain: the same pattern or logic appears in a different domain (love and war,
  for instance).

### Grades

- sound: the connection is real, the type fits, the note is accurate about both verses, and
  `teaches` is true and specific: a reader learns something from the pair that neither verse shows
  alone.
- weak: a real connection, but thin or generic; or the note overstates it; or `teaches` is only the
  shared topic; or it would be sound under a different type (give better_type).
- forced: depends on stretching a word, a reading or a colophon; or it is only a shared topic or a
  shared word dressed up as more.
- wrong: misreads or misdescribes a verse, cites the wrong text, or claims something the verses
  contradict.

Grade the link as written, note and `teaches` included. A true connection with a false claim in the
note is weak or wrong depending on how central the false claim is. A fluent, careful-sounding note
is not evidence: check each claim it makes against the Tamil.

### Output for Part A

A JSON array, one object per link, in packet order:

    {"a": "akananuru:46", "b": "kural:1311", "type": "AGREES", "grade": "sound|weak|forced|wrong",
     "better_type": null or a lowercase type name,
     "teaches_holds": true or false,
     "reason": "two or three sentences citing the deciding Tamil words",
     "text_issue": null or a short note on a corrupt line}

Write `a` and `b` exactly as the packet's LINK header shows them, as strings. `teaches_holds` is
false when the `teaches` sentence is untrue, or is only the shared topic.

## Part B: blind re-tag of ullurai and iraicchi (experimental)

Two blind taggers disagreed on both fields in the Tholkappiyam pilot (kappa about 0.5). The marking
brief now gives a testable rule for each, and Part B measures whether the rule works. For each poem
in Part B you see the Tamil, its line numbers and its colophon. Apply the rules below to the poem
yourself. Do not guess what the marker said.

**Ullurai** (porul 1.49 to 1.51, 7.26 to 7.29). Tag a hidden comparison only if all five hold:

1. The vehicle is a native thing of the poem, not a god (porul 1.50).
2. No marker joins the image to a human subject, and the poem does not state the moral itself (if it
   does, it is an open comparison, not ullurai).
3. You can name at least two separate correspondences between parts of the scene and parts of the
   love situation. A single match of mood is not enough.
4. The situation the pairs point to is stated in the poem or its colophon thurai.
5. The speaker may use that vehicle: the heroine only what she knows, the friend only things of the
   poem's land, the hero openly, others freely (porul 7.26 to 7.29).

**Iraicchi** (porul 5.33 to 5.35, 4.7, 4.29). Tag a sense rising from a thing only if all four hold:

1. One carrier: a single native thing, or one pair of creatures acting together. (A whole scene
   mapped part by part is ullurai.)
2. The thing does something a person of the situation does, fails to do or should do. Looks and
   sounds alone carry mood, not iraicchi.
3. Strike the carrier's lines and the poem's stated sense still stands.
4. You can say in one sentence what the act implies for the lovers. Pointing to tender creatures to
   comfort a suffering heroine is the textbook case (porul 5.35).

Ullurai and iraicchi are akam devices: answer `null` for both on a puram poem. One thing cannot be
both the ullurai vehicle and the iraicchi carrier.

### Output for Part B

A JSON array, one object per poem, in packet order:

    {"id": "akananuru:46",
     "ullurai": null or {"vehicle": ["Tamil form", line], "pairs": 3, "anchor": "Tamil words",
                         "failed": null},
     "ullurai_candidate_rejected": null or {"vehicle": ["Tamil form", line], "failed": 2},
     "iraicchi": null or {"carrier": ["Tamil form", line], "act": "...", "sense": "..."},
     "iraicchi_candidate_rejected": null or {"carrier": ["Tamil form", line], "failed": 3},
     "note": "one sentence if the rule was hard to apply here, else null"}

The `_rejected` entries record the strongest candidate you turned down and the number of the
condition it failed. They are how we learn which condition separates the taggers.

## When you finish

Validate that the file parses as JSON and that its counts match the packet's LINK headers and
POEM headers. Write it to the output path you were given. Then reply with only: the counts by grade,
how many `teaches` failed, and for Part B how many ullurai and iraicchi you tagged and how many
candidates you rejected, by failed condition.
