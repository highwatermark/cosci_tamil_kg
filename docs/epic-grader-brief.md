# Brief: grading epic links and the claims fields

You are grading marks in a knowledge graph of the meanings and themes of Tamil literature. Your
packet comes from the ten epics: the Silappathikaram and Manimekalai, marked by reading units of
10 to 25 lines (`silappathikaram:<kaathai>:<start>-<end>`, `manimekalai:<kaathai>:<start>-<end>`, the
kaathai's own line numbers; songs are their own shorter units), and the Civaka Cintamani,
Valayapathi, Kundalakesi, Soolamani, Neelakesi, Naga Kumara Kaviyam, Udayana Kumara Kaviyam and
Yasodhara Kaviyam, marked by verse (`neelakesi:N`). Another agent marked each unit by
`docs/epic-marking-brief.md` and proposed the links. Your job is an independent, careful judgment.
Grade on the merits: don't aim for any particular share of passes or failures. Read only your
packet. Do not edit any file in the repository.

The packet has up to two parts. **Part A** is links. **Part B**, when present, is a blind re-tag of
the `claims` and `echoes` fields, for measuring agreement; there you see the unit but not the
marker's tags.

**Nothing in the corpus explains these texts.** There is no commentary in the packet. The marked
reading, event and claims were written by Claude agents, by the same agent that proposed the link,
so they are a claim to check, not evidence. Read the Tamil first. Do not use or quote any translation
(Dikshitar's 1939 Silappathikaram included) or any commentary, old or modern (Adiyarkku Nallar,
the Arumpadavurai, Naccinarkkiniyar, or any you remember): your reasons cite the Tamil. Pope's
renderings of the Kural and Naladiyar, which the packet prints, are a third reading, not the verse.

## Part A: links

Each link starts from an epic unit or verse and points to another unit of the same epic, another
epic, or a verse of the Kural (`kural:N`), the Naladiyar (`naladiyar:N`), the Siddhar songs
(`siddhar:N`), the Tirumanthiram (`tirumanthiram:N`), the Purananuru (`purananuru:N`) or another
marked book. Each has a type, the proposer's `note`, and a `teaches` sentence. A link that leaves the
two epic groups (a **bridge**) also has `gains`: what the epic side and what the other side each gain
from the pairing. For both ends the packet prints the Tamil and the marked reading, and for an epic
end its `speaker`, `event` and `claims`.

What to watch for in this group:

- **Sequence is not a link.** Two units of one epic in story order are connected by the plot, which
  the graph already records. A within-epic link is sound when the later unit answers, fulfils or
  reverses the earlier (a dream and its event, a curse and its fruit, a claim and the scene that
  refutes it) and the note says which.
- **Illustration is not a link.** An episode that shows a virtue a Kural couplet praises is at best
  weak unless `teaches` names what the story adds to the rule: a test of it, a limit, a cost, a case
  the rule does not foresee. In round 1 of the Sangam grading, "agrees" links were sound only 39% of
  the time; "develops" and "qualifies" did better (67%, 64%).
- **Whose claim is it?** The epics put doctrine in characters' mouths, and the debates (Manimekalai
  27, the Neelakesi, the Kundalakesi fragments) state a rival school's view in order to refute it. A
  note that treats a refuted view as the work's own, or a polemic's account of a school as that
  school's doctrine, is wrong on that point.
- **Echoes and quotations.** A note that says the epic quotes or echoes a Kural couplet must be true
  of the words: a run of at least four words or a whole line in common, allowing for word division
  and sandhi. A shared idea in other words is not a quotation; if the note calls it one, grade it
  weak or wrong by how central the claim is.
- **Same name is not same person.** The Silappathikaram's Pandya Nedunjeliyan is not the
  Purananuru's Talaiyalanganattu Nedunjeliyan. A link that joins two kings by name alone, without the
  Tamil fixing that they are one, is forced.
- **`gains` on bridges.** Both clauses must be true and specific. If the other book gains nothing
  (the epic only illustrates the couplet), the bridge is weak at best. Bridges to the Siddhars and
  the Tirumanthiram on karma, renunciation and the body are the ones this round tests: a real
  `tension` there is an incompatible claim (release by the wearing away of karma, or by grace) on a
  defensible reading, not a difference of tone.
- **Units and fragments.** A moved unit carries a `unit_note`; if the cut splits a sentence the link
  depends on, say so in `text_issue`. Valayapathi and Kundalakesi are fragments in an editor's order:
  a link that relies on a reconstructed plot the verse does not state is forced. Silappathikaram 22
  has lines the edition marks as later additions; a link resting only on them is weak at best.
- Earlier graders were too lenient: a link that needs a generous reading is weak, not sound. The
  Cintamani and Soolamani texts carry many flags; if a verse looks corrupted, say so in `text_issue`
  instead of building on it.

### Link types

- tension: the two make incompatible claims about the same thing, on at least one defensible
  reading. Shared words, a shared topic, or different advice for different situations are NOT
  tensions. The note should say which reading the conflict depends on.
- agrees: they make the same claim, and pairing them teaches something (e.g. it appears in
  different books, schools or periods).
- develops: one extends, deepens, applies or fulfils the other (a prophecy and its event).
- qualifies: one limits or adds a condition to the other.
- same_image: they share a distinctive image, object or figure (the anklet, the begging bowl), and
  the shared use is meaningful.
- parallel_domain: the same pattern or logic appears in a different domain (the king's justice and
  the householder's, for instance).

### Grades

- sound: the connection is real, the type fits, the note is accurate about both ends, `teaches` is
  true and specific (a reader learns something from the pair that neither shows alone), and on a
  bridge both `gains` clauses are true.
- weak: a real connection, but thin or generic; or the note overstates it; or `teaches` is only the
  shared theme; or one side gains nothing; or it would be sound under a different type (give
  better_type).
- forced: depends on stretching a word, a reading, a reconstructed plot or a shared name; or it is
  only a shared theme dressed up as more.
- wrong: misreads or misdescribes a unit, cites the wrong text, gives a refuted view as the work's
  own, calls a paraphrase a quotation, or claims something the texts contradict.

Grade the link as written, every field included. A true connection with a false claim in the note
is weak or wrong depending on how central the false claim is. A fluent, careful-sounding note is not
evidence: check each claim it makes against the Tamil.

### Output for Part A

A JSON array, one object per link, in packet order:

    {"a": "manimekalai:22:58-68", "b": "kural:55", "type": "QUALIFIES", "grade": "sound|weak|forced|wrong",
     "better_type": null or a lowercase type name,
     "teaches_holds": true or false,
     "gains_holds": true, false, or null when the link is not a bridge,
     "reason": "two or three sentences citing the deciding Tamil words",
     "text_issue": null or a short note on a corrupt line or a bad unit cut}

Write `a` and `b` exactly as the packet's LINK header shows them, as strings. `teaches_holds` is
false when the `teaches` sentence is untrue, or is only the shared theme. `gains_holds` is false when
either clause is untrue or names nothing specific.

## Part B: blind re-tag of claims and echoes

The marking brief asks for every doctrinal or ethical claim a unit states, with its school and
stance, and for every echo of the Kural or Naladiyar. Part B measures whether two readers find the
same ones. For each unit you see its Tamil with line numbers, the book and section, and the units on
either side in one line each (for context, not for tagging). Apply the rules below yourself. Do not
guess what the marker said.

**Claims.** A claim is stated, not merely illustrated: a speaker or the narrator says that something
is so (deeds of a former birth ripen; a wife's chastity commands the rain; the soul is the body).
A scene that shows karma at work without anyone saying so has no claim. For each claim give:

- `line`: where it is stated.
- `school`: `jain`, `buddhist`, `vedic`, `saiva`, `vaishnava`, `ajivika`, `lokayata` or `general` (an ethical
  claim not tied to a school), by the school the claim belongs to as the text presents it, not the
  work's affiliation. Sankhya, Vaisheshika, Nyaya, Mimamsa and Vedanta are `vedic`; the materialists
  (பூதவாதம்) are `lokayata`.
- `stance`: `asserted` (the work holds it, through its narrator or a speaker it endorses), `refuted`
  (put in order to be answered), or `reported` (held by a character, neither endorsed nor answered
  here).

**Echoes.** Words in the unit that match a Kural couplet or Naladiyar quatrain: a run of at least
four words or a whole line, allowing for word division and sandhi. Give the couplet number only if
you can name it from the words; if you recognise the wording but not the number, give the words and
`b: null`. `kind` is `quote` when the unit sets the words off as a saying (என்ற, a named source),
else `echo`.

### Output for Part B

A JSON array, one object per unit, in packet order:

    {"id": "manimekalai:22:58-68",
     "claims": [{"line": 59, "school": "general", "stance": "asserted", "school_detail": null,
                 "gist": "a wife who worships her husband commands the rain"}],
     "claims_rejected": [{"line": 65, "why": "illustrated, not stated"}],
     "echoes": [{"line": 59, "b": "kural:55", "kind": "quote", "words": "தெய்வம் தொழா அள்"}],
     "note": "one sentence if a rule was hard to apply here, else null"}

`claims_rejected` records the strongest candidate you turned down and why (illustrated not stated;
a question, not a claim; too corrupt to read). It is how we learn where readers part.

## When you finish

Validate that the file parses as JSON and that its counts match the packet's LINK headers and UNIT
headers. Write it to the output path you were given. Then reply with only: the counts by grade, how
many `teaches` and how many `gains` failed, and for Part B your claim counts by school and by
stance, how many candidates you rejected, and the echoes you found.
