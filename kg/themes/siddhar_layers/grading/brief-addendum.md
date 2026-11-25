# Addendum to the Siddhar grader brief: reading layers

Read `docs/siddhar-grader-brief.md` first; everything there still applies. This addendum covers
what is new in `packet.md` (part 1) and `lexicon_packet.md` (part 2). Read only those two packets
and this addendum. Do not edit any file in the repository except your output files.

## Part 1: links that name a layer

Each Siddhar verse now carries several **reading layers** at once, each with a confidence and the
Tamil words that carry it:

- `literal`: the plain sense, technical words taken as named (a verse that says மூலநாடி names a
  channel; that is literal).
- `breath`: breath and yoga: வாசி, the nadis, the centres, the gates, the nectar.
- `alchemy`: alchemy and medicine, recorded as historical claims only.
- `consciousness`: god within, the self, silence, the void.
- `social`: caste, ritual, pilgrimage, false gurus, sects, book-learning.

Each link names the **one layer it depends on** (`layer=` in the header) and the other layers on
which the proposer says it **also holds** by itself. The packet prints each Siddhar verse's literal
reading and its reading on every layer the link names; for the other books it prints the marked
reading as before. All readings were written by Claude agents; they are claims to check.

Some readings and links apply a **cipher key**: a traditional decoding of a word, number or figure
(the sun and moon as the two breaths, the nine as the body's nine openings, the upper door as the
crown). A new link type, **SHARED_KEY**, joins two verses that decode together under one key, where
at least one verse needs the key to be read that way. Judge it by these questions: is the key a
fair, traditional one; is it fairly applied to each verse (do the carrying words support it); and,
read with the key, do the two verses really say the same thing? A shared-key link is not weak merely
because it is a cipher link, but it is forced if the key is stretched or the plain words resist it.

Grade every link sound, weak, forced or wrong exactly as in the grader brief. A layer label does not
rescue a link: two verses sharing a stock attack on ritual are weak on the social layer as on any
other. Add three fields to each object:

    {"a": ..., "b": ..., "type": ..., "layer": "breath",
     "grade": "sound|weak|forced|wrong", "better_type": null or a type,
     "layer_ok": "yes|partly|no",
     "holds_without_layer": true or false,
     "key_fair": true, false or null,
     "reason": "two or three sentences citing the deciding Tamil words",
     "text_issue": null or a short note}

- `layer_ok`: is the named layer the one the link actually depends on, and is each verse's reading
  on that layer fair to its Tamil? `partly` if one end's layer reading is stretched.
- `holds_without_layer`: would the link still hold on the literal readings alone (for a link whose
  layer is `literal`, answer whether it holds without any of the also-holds layers, which is usually
  true)?
- `key_fair`: for a link or reading that applies a cipher key, is the key traditional and fairly
  applied to both verses? `null` if no key is involved.

Write the array to the output path you were given, one object per LINK header, in packet order,
with `a` and `b` exactly as the header shows them. Validate that it parses and that its count
matches the LINK headers (47).

## Part 2: the double-reading lexicon

`lexicon_packet.md` lists words from the pilot verses that the proposer says carry two traditional
senses (for example வாசி, read both as a horse and as the breath as practice). For each entry you
see both senses, the pilot verses that use it with the readings that depend on it, and how many
units of the whole corpus contain the word.

Accept an entry only if **both** senses are genuinely traditional for this word (not invented for
the verse), **and** in at least one cited verse the second sense is a fair reading of the Tamil.
Reject it if either sense is not attested as a reading of the word, if the double reading is only
a pun the proposer made, or if no cited verse supports the second sense. An entry can be accepted
while one of its cited uses is stretched; say so.

Write a JSON array, one object per ENTRY in packet order:

    {"id": "vaasi", "status": "accepted|rejected",
     "bad_uses": [list of verse numbers whose use of the entry is stretched, or []],
     "reason": "one or two sentences"}

The lexicon's acceptance rate (accepted / reviewed) is reported as its quality metric, so do not
aim for any particular share. Reply with only the counts: grades for part 1 and accepted/rejected
for part 2.
