# Nilai v4: the 13 chapters, curator's review

Data: `site/nilai/v4/chapters.json`. Choices are in `chapters_curate.py`, which copies every Tamil line, reading, flag and link text from `kg/` at run time. `validate_chapters.py` checks the result and passes: every Tamil line matches `kg/core`, every link is sound and present in `bridges.jsonl` or `all_link_audit.json`, and every reading matches its graph node. Spread: 39 verses, 16 books, all 9 groups. No verse is used twice. 23 new images are needed (`new_images.md`).

How the paths were found: every sound link (1,856 cross-group bridges plus 1,405 sound within-group links from `all_link_audit.json`) was searched for three-verse walks in which all three verses express a concept of the chapter's category, at least two groups take part, and the three books differ. The walks were then ranked by whether each verse names a drawable object, by whether the links carry a `teaches` sentence with `teaches_holds` true, and by the number of groups. The pick among the top walks was made by reading them. The category the brief calls *arivaayvu* has the id `aivu` in `concept_categories.json` (Tamil அறிவாய்வு), and the file uses that id.

General compromise: four chapters (udal, ullam, yogam, aivu) rest on links marked from the devotional books (`siddhar_marks`, `tirumanthiram_marks`, `thiruppugazh_marks`). Those links are graded sound in `bridges.jsonl`, but they have no `teaches` sentence (`teaches_holds` is null) and no row in `all_link_audit.json`, so these chapters show the link's `note`. The validator accepts a sound grade in either file and flags none of these.

## அறம் aram · the balance that levels itself

Path: Purananuru 6 → Maduraikkanchi 489–506 → Kural 118. Groups: Ettuthogai puram, Pattuppattu, ethics. All three verses name the beam of a balance (தெரிகோல் ஞமன், ஞெமன்கோல், சீர்தூக்குங் கோல்), and both links are `develops` with holding teaches. The walk follows impartiality through three stages. The puram poet wishes it on one king's person. The Madurai idyll makes it the work of a court and names the five passions that court must set aside. The Kural compresses it to the balance that "first makes itself level". The forward beat (machines that weigh, and who levels them) follows from the Kural's condition. Compromise: one image (02-T) serves all three verses. The page can vary its scale or pose; a second balance image would add nothing the verses name.

## பொருள் porul · the parasol, and who falls outside its shade

Path: Purananuru 35 → Kalittokai 99 → Kural 559. Groups: puram, akam, ethics. Both links hold. The puram counsellor tells the king that his parasol exists to shade the suffering, not the sun. The Kalittokai friend turns the same counsel on a husband and asks whether her friend fell outside its shade. The Kural link adds the edge: the rule that ties rain to public justice can be met in full while a wife is wronged. The forward beat (whose shade a system misses) is the friend's own question, carried over, and it touches inequality. Compromise: Kural 559 names rain, not the parasol; the rain cloud is a new image.

## இன்பம் inbam · the hill that played every instrument

Path: Akananuru 82 → Paripadal 21:30–38 → Thinaimalai Nootraimpathu 111. Groups: Ettuthogai akam, Paripadal, Kilkanakku akam, so three groups. Both links are `same_image` with holding teaches. The richest object path in the corpus: wind in bored bamboo is the flute, the waterfall the drum, the bees the yazh, the peacock the dancer. The links show one figure moving through three settings: a love poem's setting, worship of the hill's own god, and the mullai season of a promised return. The beat (sound made to order, and what still reaches a heart left alone) touches creativity and what stays human. The yazh (21-T) is an existing asset. Nothing compromised.

## வீடு veedu · the raft across the sea of deeds

Path: Kural 10 → Civaka Cintamani 3019 → Neelakesi 155. Groups: ethics, great epics, minor epics. Both links hold. The Kural states the crossing of the sea of births and leaves its cause open. The Jain epic supplies the cause: deeds that kick the swimmer down and whirl him like thread in a weaver's shuttle. The Neelakesi hymn adds that the sea is made of the swimmer's own deeds and that the Lord's part is to build the raft. The forward beat (a craft for a darker sea; swimmers or passengers) touches star-faring and steering. The raft becomes the existing solar-sail image (26-F). The lamp path (Naladiyar 51 → Soolamani 2018 → Tirumanthiram 2293) was the runner-up and would have used the 31-T lamp. It was dropped to keep the Naladiyar from carrying five chapters.

## உடல் udal · the boat, the mist and the lock

Path: Siddhar 987 (Sivavakkiyar) → Naladiyar 28 → Thiruppugazh 548. Groups: devotional and ethics only. Each verse names the body as a thing: a boat poled on water, a mist on a hill, a string-worked contraption shut with a lock. Together they teach use while it lasts, then do not trust it. The beat turns the lock and strings toward medicine and biomimicry. Compromises: two groups, not three. Both links are devotional-marked, so the page shows the note. 24-T is a round coracle standing in for the verse's ஓடம். The food-as-medicine path (Tirumanthiram 872 → Kural 942 → Nanmanikkadigai 50) has a holding teaches but names almost no drawable object, so it was not used.

## உள்ளம் ullam · from the tossed pot to the lit temple

Path: Siddhar 1166 → Naladiyar 47 → Tirumanthiram 1823. Groups: devotional and ethics. All three verses also carry udal concepts; their ullam concept is manam, pedhaimai or manam. The walk makes one body into three minds: a pot tossed on water until it fills and settles, a seeping pot that dazzles a fool's eye, and a temple whose five thieving senses become bright lamps. The `tension` link to the Naladiyar carries the turn. The beat (a mind lit from outside: can it still light itself?) touches the evolution of consciousness, and lets the 31-T lamp become the 31-N bulb. Compromise: two groups and note-only links. Of the 31 ullam walks that cross two or more groups, only 6 have a named object in every verse, and this is the strongest of them.

## இறை irai · the stone that speaks

Unchanged from the approved prototype: Siddhar 1458 → Manimekalai 21:112–129 (tension) → Civaka Cintamani 2058 (develops), with its forward beat. One change follows from the four-line rule. The prototype shows lines 115–116 and 125–128 of the Manimekalai unit on wide screens (six lines). chapters.json lists the four it shows on a phone (115–116, 127–128) and records the difference in `image_note`.

## யோகம் yogam · the breath that kicks Death away

Path: Tirumanthiram 571 → Kural 269 → Siddhar 1119. Groups: devotional and ethics. This is the weakest chapter, and the reason is in the graph: no walk of three yogam verses crosses groups. All 39 walks with two yogam verses run devotional–Kural–devotional. This one keeps the subject the category names, the breath. Tirumular says the measure of the held breath kicks Death. The Kural says the power of austerity leaps past Death. Sivavakkiyar says the runner within settles and Death stands bewildered. Compromises: Kural 269 expresses thavam (a veedu concept), not a yogam one, and it names no concrete object, so the breath image carries over from verse 1. Both links are note-only. The alternative was the tortoise: Tirumanthiram 2304 → Kural 126, with all three verses naming a tortoise. It was rejected because the only second yogam-tagged tortoise verse, Tirumanthiram 2158, has a stray "Y" in its first line in `kg/core`, and the clean substitute, Siddhar 20, is not yogam-tagged.

## இயற்கை iyarkai · the tank, the well and the gift of food

Path: Purananuru 18 → Sirupanchamoolam 65 → Manimekalai 11:76–98. Groups: puram, ethics, great epics. Both links hold and share one teaching: the duty to bind water where the land dips moves from a king's public works, to a merit open to any man of means (tank, bank, road, field, shared well), to a renunciant's gift of food. The Purananuru and the Manimekalai share the line உண்டி கொடுத்தோர் உயிர் கொடுத்தோரே, and both are shown. The beat (with rain less certain, who binds the water) touches nature. Both tanks are existing assets (04-F2, 04-F3). Compromise: the Manimekalai lines name the raft of learning that hunger makes one drop, not the alms bowl, so the image is the raft, shared with veedu.

## சமூகம் samugam · the widow's leaf and the sun

Path: Purananuru 246 → Manimekalai 2:42–57 → Silappathikaram 18:34–53. Groups: puram and great epics. Both links hold. Queen Perunkoppendu refuses the widow's leaf-wrapped rice and bed of pebbles. Madhavi turns her single act into a ranked list of what widows do: sigh out life like a smith's bellows, enter the fire, or wear the body down in vows. Kannaki refuses all of these and asks the blazing sun whether her husband was a thief. The beat (who writes the rules for another's life) touches inequality, and the leaf becomes the 07-F rack, as in v3. Compromise: two groups. The caste walk (Siddhar 1003 → Naladiyar 195 → Manimekalai 13:57–69) crosses three groups, but Naladiyar 195 names no object, and Siddhar 1003 already carried a v3 scene.

## அறிவாய்வு aivu · the bird that drinks the milk and leaves the water

Path: Thiruppugazh 70 → Naladiyar 135 → Tirumanthiram 2720. Groups: devotional and ethics. All three images exist: the palm-leaf bundle (01-T) for "endless crores of books", the pond heron (10-H) for the bird that drinks milk and leaves the water, and the ship (26-T) for the precious vessel that reaches the farther shore. The walk answers endless learning with choosing. The Naladiyar's swan-test sits between Arunagirinathar's endless books and Tirumular's one letter. The beat (all learning on tap; who teaches the choosing) touches intelligence on tap. Compromise: two groups and note-only links. The Kural/Purananuru walk on learning had a holding teaches but no drawable objects.

## புலமை pulamai · the name cut in stone

Path: Purananuru 232 → Purananuru 264 → Akananuru 297. Groups: puram and akam. Pulamai has no valid walk in the graph: no three-verse walk across two groups contains even two strict pulamai verses. The pulamai verses that cross groups at all join only one other pulamai verse. This walk keeps two pulamai verses (kaiyarunilai, the lament genre) and has the strongest teaching on writing. The stone's offering reverses the gift (develops, holds). The name is carved to outlast death, and generations later the akam road walks past the worn letters unread (qualifies, holds). The beat (everything written, who stops to read) touches creativity and what stays human. Compromises: Akananuru 297 expresses no pulamai concept; two verses are from the Purananuru; two groups.

## காலம் kaalam · the staff that comes to every youth

Path: Purananuru 243 → Naladiyar 11 → Tirumanthiram 848. Groups: puram, ethics, devotional. One image, the old man leaning on a staff, draws three answers. The Sangam poet takes it as proof that youth was the best of life (tension, holds). The Jain moralist takes it as the reason to renounce in childhood. Tirumular says sea water drunk with its froth skimmed turns the grey back and keeps Yama away (tension, note). The beat (we can hold the staff off; who gets the long years, and what for) touches medicine and inequality. Compromise: Tirumanthiram 848 is flagged uncertain in the graph, and its link holds only if the verse is read literally; the note says so.

## Flags carried into the page

Readings the graph marks uncertain: Silappathikaram 18:34–53, Manimekalai 11:76–98, Akananuru 297, Thiruppugazh 548, Thiruppugazh 70, Tirumanthiram 848 and Civaka Cintamani 2058. Each carries `"uncertain": true` in chapters.json.
