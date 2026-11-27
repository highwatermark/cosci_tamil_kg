# How the Tamil texts describe knowing and measuring

The organizing unit is a question. Each [inquiry](inquiries.jsonl) records a Tamil anchor, the kind of evidence the passage supplies, a missing observation and a feasible next test. Each [comparison](comparisons.jsonl) links stable passage or source IDs, gives its reasoning and states the limit of the inference. The [source register](sources.jsonl) distinguishes physical measurements, human experiments, technical exposition, clinical interpretation and philosophical proposals. This initial batch is editorially proposed. The existing blinded science run has its own candidate pool, controls and threshold in the parent folder.

## A result from searching the growing corpus

A search with five Tamil expressions across the current core returned seven units. The query recovered the five seed passages and two additional hits. One is Akananuru 43, where timekeepers are singled out during rain that hides the sun. Mullaippattu 55–58 puts the same water-clock expression in a military camp where attendants report time to the king. The published translation notes cross-reference these passages. The second extra hit, Thirumurai 2.99.9, describes a divine search that fails to find its object. Counting every occurrence of “went and measured” as evidence of an instrument would introduce a false positive. This small seeded search demonstrates discovery and a failure mode; its yield cannot estimate corpus-wide prevalence. [Translator’s notes on the parallel](https://learnsangamtamil.com/mullaipattu/)

The water-clock pair supplies a practical problem, specialist roles, an instrument name and a reported output. Neither passage fixes vessel geometry, flow direction, calibration, or the numerical precision achieved. An Egyptian outflow clock with physical divisions gives a comparative example of what a surviving instrument can tell us. Its provenance belongs to Egypt. Investigation of the Tamil device needs evidence local to its tradition. Preserve the poem’s composition-date range, the edition or manuscript date and the date of any material witness as separate fields when evidence becomes available. [Museum object record](https://isac-idb.uchicago.edu/id/da9f903b-b1c7-4294-a5e4-d53068a08617)

## Research tracks

| Question | Tamil starting point | Evidence that would advance it |
|---|---|---|
| How was time kept when the sun was hidden? | Akananuru 43 and Mullaippattu 55–58 | Compare recensions and instrument descriptions. Test predicted timing error across plausible vessel designs. |
| How did builders establish orientation? | Nedunalvadai 65–80 places two rods, midday, a measuring cord and a building layout in one scene. | Compare rival geometries and their shadow predictions. Record latitude, season and rod dimensions as assumptions. |
| What counted as measuring the cosmos? | Purananuru 30 describes people speaking *as if* they had gone and measured celestial things, in a poem praising a ruler. | Compare observational reports, calendars and rhetorical comparisons. A number needs an object, unit, procedure and provenance before entering a measurement dataset. |
| How did grammar teach duration? | Tolkappiyam, Eluttu 1.7 uses a blink and a nodi as a reference for māttirai. | Test competing readings of the bodily reference and relative speech duration across reciters. Record speaker variability and historical uncertainty. |
| What distinguished medical reasoning from evidence of efficacy? | Kural 948 orders inquiry into illness, cause, possible relief and suitable action. | Find witnessed cases that also report an outcome or comparison. Lind’s scurvy account gives a later worked comparison. [1753 treatise](https://www.jameslindlibrary.org/lind-j-1753/) |
| What changes when a speaker reports losing the individual “I”? | Sivavakkiyam 327 first brings “he” and “I” together and then denies the “I.” | Compare bodily self-boundary, agency, speaker identity and devotional union separately. A modern meditation experiment explicitly manipulated the self-boundary task. [MEG study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12742028/) |

For a numerical correlation, first choose two independently measurable variables, a unit of analysis and a comparison set. A feasible study would count instrument–operator–readout descriptions per thousand lines by genre and compare them with instrument mentions in similes. Match on text length, deduplicate repeated witnesses, and reserve entire works for evaluation. A different study could examine measured timing variation across physical reconstructions. Literary affinity and empirical correlation have different denominators.

## Modern sources and competing explanations

* Pollan provides a way to juxtapose testimony with research. Maté’s event-versus-inner-response distinction suggests a question about the abandoned lover’s voice in Akananuru 1; a literary character cannot supply a clinical history. Kaku’s account of anticipation can be compared with Kural 467’s demand for deliberation before action. Tyson’s cosmic kinship can be set alongside Purananuru 192 and Sivavakkiyam 46 to compare the differing grounds for an ethical inference. Specific sources and respective limits accompany each graph edge.
* Feynman gives a concrete test for use of the word superposition: what physical alternatives contribute amplitudes, and what interference would distinguish them? The sodium-cluster experiment supplies a measured example. D’Ariano and Faggin propose an account of individual experience in quantum-informational terms. Masi offers a different proposal about universal consciousness and agency. The two theories generate different questions for Sivavakkiyam 327. Neither is an empirical identification of that speaker’s experience.
* The Hameroff–Penrose proposal specifies a microscopic substrate, and Tegmark supplies a competing timescale argument for the systems he models. The graph retains the proposed microscopic explanation of Sivavakkiyam 327 as **withheld**. An edge between the theories records a dispute. Neither side measured the speaker or the practice.
* The strongest immediate AI application is to retrieve evidence and its counterexamples together. Ithaca provides an experimental precedent for evaluating AI assistance on ancient Greek inscriptions. For Tamil, compare blinded readers with and without retrieval on held-out works. Measure how often they recover genuine parallel witnesses, preserve negation and simile, and abstain on unsupported instrument designs. [Ithaca study](https://doi.org/10.1038/s41586-022-04448-z)

## Reproduce and extend

Run from the repository root. The search reads Tamil-bearing core records, uses reading units for long poems where available, folds whitespace and punctuation, and emits a stable ID and original Tamil for each candidate. Its literal matching misses variants and can cross a word boundary. Inspect the original wording before adding an edge.

```sh
python3 -I scripts/science_inquiry.py check
python3 -I scripts/science_inquiry.py find 'குறுநீர்க்கன்ன' 'இருகோற்' 'சென்றளந்து' 'கண் இமை நொடி' 'நோய்முதல் நாடி'
```

New core texts become searchable on the next run. Compare new candidates with known descriptive, devotional and figurative controls before graduating any to a graded relationship. Snapshot counts belong to the corpus available when this batch was run.

[From living bodies to the open universe](parallelisms.md) extends the search across biology, sensory capacities, atomism, ecology, cosmology and concepts of pervasive reality. It includes a reproducible corpus scan and nine additional comparisons.

[Siddhar readings on unity, experience and fields](siddhar-unity.md) traces adjacent verses, contrasting poets and modern tests.
