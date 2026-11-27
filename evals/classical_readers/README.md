# Two independent Tamil readers and five literary graph views

The [grammar reader](philology.md) attends to case, voice, agency, polarity and condition. The [genre reader](voice.md) attends to addressee, image, poetic convention, authority and the possibility of more than one sense. Each receives the same Tamil with a stable ID in a fresh context. Both record a reading, a rival, a limit, a confidence and a verbatim anchor. Shared model training remains a common source of error. The second stage can bring in neighbouring stanzas, named witnesses and edition variants after retaining the original decisions.

## What was run

Ten purposively chosen units from five books went to two independent Codex workers. Five were Siddhar verses. The rest supplied a didactic test, a bodily counterexample, a testimony and two devotional petitions. All twenty anchors occur in the source lines. Both readers rated the alchemical question and both devotional songs medium confidence. The voices can be characterized more securely than the identities of those speaking. A difference on Naladiyar 47 concerns confidence in the address and syntax; both see a rebuke of a fascinated admirer. Confidence agreement is no measure of edition accuracy. [Tamil packet](pilot.json) · [Philological readings](philology.json) · [Genre readings](voice.json)

Two additional independent workers judged five explicit link claims with the Tamil visible and earlier judgments hidden. The deliberate near-misses test what happens when a note silently alters a subject, claim or condition. Both workers accepted the shared moon-and-sea imagery and held the four claims whose wording outran the evidence. Use these as teaching cases. A score on this hand-built exercise cannot estimate link accuracy throughout the corpus. [Claims](link_pilot.json) · [Syntax judgments](syntax_links.json) · [Genre judgments](genre_links.json)

## Questions that change the reading

| Unit or pairing | Defensible reading and the limit on a link |
|---|---|
| Pattiragiriyar, Pulambal 125 (graph 127) | “When” makes freedom from caste distinctions an aspiration. The speaker invokes an attributed teaching to authorize it. This supports anti-caste inquiry while complicating a claim that critique always rejects textual authority. |
| Sivavakkiyam 46 and 494 (graph 1010 and 1458) | The first challenges caste differences by asking what bodies and gold ornaments have in common. The second asks whether a planted stone can speak while the Lord is within. Equal material, a divine presence within, and universal metaphysical identity are three increasingly strong claims. Record the claimed scope separately for each poem. |
| Pulambal 1 (graph 2) | The speaker longs for “sleeping without sleeping” after a line about pride and the senses. The paradox licenses an inquiry into disciplined awareness. It leaves the physiology and whether attainment has happened open. |
| Pattinathar, Thiruthillai 16 (graph 295) | Read the apparent medicine against death through the closing address to the mind. Remembering the feet of the lord of Tillai supplies the good medicine. Distinguish salvific metaphor, material claim, longevity wish and their combination. |
| Agathiyar Njanam 2.1 (graph 2414) | “If the mind is upright” governs three statements of what is unnecessary. The fourth line returns affirmatively to mantra. A graph can store a condition on a practice and its spiritual purpose without treating all verses as endorsing breath mastery. |
| Madurai Valaisami, Njanak Kummi 118 (graph 2635) | The guru is within, and the crookedness to be cut lies within. Craft vocabulary supplies a question about applying puṭam without understanding the poruḷ. Retain both the substance and inward readings; the verse does not identify an ingredient, clinical treatment or biochemical mechanism. |
| Tirumanthiram 725 and Naladiyar 47 | The first-person discovery in the body changes how the speaker cares for it. The second uses a vessel with nine openings to unsettle erotic praise. Compare what each image does to the listener. A direct contradiction about care for one's own body requires another premise. |
| Tirumanthiram 252, 270 and Kural 322 | Specific acts of feeding and kind speech in 252, the identification of love and Siva in 270, and sharing food to sustain living beings in 322 make three different candidates for a love-and-service inquiry. An ethical parallel can survive across books while the theological claim remains attributable to its own verse. |
| Thiruppugazh 1087 and 344 | Both enlist moon and sea in the suffering of a girl and turn to the deity for help. One asks for an embrace, the other for the words “fear not.” This yields both a shared image and a meaningful difference in what relief consists of. |

The Siddhar anthology here contains 43 works attributed to 26 poets. The attributed-poet inventory includes Agathiyar. Bhogar and Therayar are research targets for additional witnessed texts; this anthology’s poet list does not supply corpora under their names. Store attribution, edition, line, textual variants and uncertainty on future witnesses. Keep historical medical observation, technical vocabulary, claimed result, and symbolic use queryable independently. A modern comparison can also contradict a material claim.

## Ten ways to search the five books

[The query tool](slices.py) returns IDs, matched concept tags, Tamil and the stored reading. [The table](slice_counts.csv) counts verses tagged with at least one seed concept per lens. The collections overlap. Current marks can miss examples or return false positives. For example, tagging divine names cannot by itself establish that a verse locates the divine within. Examine the speaker, verb, object and stance before asserting a link.

Use inward divinity, ego and stillness, care for life, ritual and social authority, knowing and experience, body and liberation, breath and senses, medicine and longevity, alchemy and cipher, or devotional address. Within each result ask who acts, what changes, what licenses the change, which alternative the speaker rejects, and whether the speaker recalls, asks, promises or prescribes. Distinguish a goal voiced by a poet, a reported change during one life, historical change between dated witnesses, and a modern experimentally measured change. Only the third supports a history of ideas, and it requires independently justified dating.

For example, the medicine and longevity query finds 60 Siddhar units, the body and liberation query 497, and the breath and senses query 293. These are starting points for review. Pull adjacent stanzas when the voice or a technical word is unresolved. Retain results that resist the initial theme.

## Tolkāppiyam as a reading instrument

The local edition contains 1,602 numbered sutras and a prefatory poem. [Six extracted sutras](grammar.jsonl) preserve edition IDs and Tamil. Porul 1.3 suggests recording setting, associated objects and the human situation. Porul 8.1 makes the utterance, audience, place and time explicit questions. Porul 2.23 gives a textual reason to test the use of love conventions in address to a god. Porul 7.1 asks what is actually shared by a simile. Porul 6.3 helps distinguish an expressed or depicted feeling from the identity of the person feeling it. Porul 1.49 prompts a distinction between explicit and implied comparison. Record a grammar category as native, extended by analogy or inapplicable. Optional corroboration is available in the local Naccinarkkiniyar witness for Akattinaiyiyal (catalog row 638).

For 1087 and 344, the girl suffers, an intercessor speaks and the deity hears. Searching that arrangement plus the paired moon-and-sea image yields a more discriminating comparison than searching for “devotion.” For a Siddhar cipher, start by identifying what property is being transferred and what local word warrants the transfer. The grammar can be a constraint on imaginative readings. In the existing 100-item pilot the two taggers agreed on the presence of a comparison with kappa 0.84, but on the presence of ullurai with kappa 0.48. Keep the latter as a disputable annotation. [Original agreement table](../../kg/themes/tholkappiyam_pilot/agreement.txt)

## Modern comparisons and consciousness

A contemporary analogy should carry four fields: the passage’s actual claim, the modern observation and experimental task, the property they share, and where the analogy breaks. Record direction separately as compatible, contradictory, open or figurative. The existing science pass found 17 of 300 candidates above threshold with two AI graders, including five contradictions and four without a single directional verdict. None of 100 random controls reached grade two. These outcomes measure how this grading procedure treats pairings. [Scored historical run](../../kg/science/threshold_summary.json)

* **Breath and perception.** A 2026 experiment found higher sensitivity to near-threshold visual stimuli during inspiration. Another found better performance during exhalation on its heartbeat-discrimination and tactile-detection tasks. The task, modality and meaning of “better” matter. Ask which perceptual faculty a verse even claims to change, and keep a value such as a well-ordered mind distinct from a detection score. [Visual detection experiment](https://www.nature.com/articles/s41467-026-71604-8) · [Interoceptive and tactile experiments](https://pubmed.ncbi.nlm.nih.gov/42045067/)
* **Competing accounts.** The Cogitate collaboration tested preregistered predictions about consciously experienced visual stimuli and found challenges for both theories it examined. The methodological borrowing for Tamil reading is to state in advance what textual feature would favour each rival reading. Neither awakening nor liberation was an endpoint of that experiment. [Primary consciousness study](https://doi.org/10.1038/s41586-025-08888-1)
* **Quantum superposition.** A 2026 interferometry study found matter-wave interference for sodium clusters. Its evidence is a physical interference pattern in a defined apparatus. The Tamil question about puṭam allows more than one reading because the utterance and its context underdetermine its sense. One may compare how context discriminates alternatives, provided the graph labels the comparison as a modern metaphor. A proposed physical account of contemplative awareness would require defined physical states, measurable coherence or interference and evidence connecting those measurements to experience. These sources supply no demonstrated quantum route to liberation. [Primary physics paper](https://www.nature.com/articles/s41586-025-09917-9)

## Run again as the corpus grows

From the repo root:

```sh
python3 -I evals/classical_readers/packet.py siddhar:2414 tiruvasagam:1 pattupattu:1:1-16 > /tmp/tamil-review.json
python3 -I evals/classical_readers/review.py prompt philology /tmp/tamil-review.json
python3 -I evals/classical_readers/review.py prompt voice /tmp/tamil-review.json
python3 -I evals/classical_readers/review.py join evals/classical_readers/pilot.json evals/classical_readers/philology.json evals/classical_readers/voice.json
python3 -I evals/classical_readers/slices.py medicine-and-longevity --book siddhar
python3 -I evals/classical_readers/slices.py grammar
```

For a fresh local run with an authenticated Codex CLI, use `python3 -I evals/classical_readers/review.py run /tmp/tamil-review.json`. The launcher starts two ephemeral sessions in separate temporary directories, validates both outputs, and prints the joined JSON. Pass `--model` to pin a model. The live pilot used independent Codex subagents; the CLI launcher was tested by replaying their saved outputs.

Alternatively, send each generated prompt to a fresh independent worker with only that prompt, retaining each JSON response before revealing any earlier mark or comparison. The join command accepts the packet and both response paths and checks each anchor. Its output is a side-by-side evidence record. It deliberately preserves disagreements; confidence and word overlap cannot adjudicate grammar. Keep subsequent adjudication attributable and versioned.

The packet tool works with built verse IDs and core IDs of ingested texts, including Sangam reading units. [Graph views](views/README.md) incorporate new books after graded edges exist and document how to extend their membership. Compare same poet, other poet within the tradition and outside the tradition in separately sampled candidate pools, controlling for refrain, length and relation. Evaluate discoveries per ten suggestions and coverage of previously isolated verses. Preserve exceptions and rejected proposals. Compare like-for-like snapshots as new books arrive.
