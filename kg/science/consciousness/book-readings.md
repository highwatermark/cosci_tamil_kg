# Reading across all 45 indexed Tamil collections

Start with a word that changes its meaning as it travels. In Kural 948 a physician should investigate an illness and its cause. In Ainthinai Ezhupathu 5 a lover's kindly glance is life-sustaining medicine. In Manimekalai 19 a bowl of food is called life medicine just before a king is asked to convert a prison into a charitable institution. A graph can correctly connect all three passages by vocabulary and still misrepresent all three if it assigns them the same kind of remedy.

There are **45 readings, one for each of the 45 book identifiers** in the snapshot of 41,583 indexed Tamil units. Some identifiers cover multiple works. Units can be couplets, stanzas, poems or editorial line ranges. All 45 selected passages received a Tamil-first interpretive reading. The other 41,538 units did not receive that treatment in this ledger. The English accounts are one machine reader's paraphrases. They have no human scholarly sign-off or independent translation accuracy score.

## Four paths through the evidence

- **What does knowing within change?** In Sivavakkiyam 215 inner realization has an explicit social consequence in the denial of caste difference. In Tirumanthiram 725 recognizing a temple within changes how the speaker cares for the body. In Prabandham 1222 an injunction addressed to the mind leads outward to a temple. A graph can label these outcomes separately as equality, bodily care and worship.
- **What did measurement mean to the speaker?** Pattupattu 9 traces goods going ashore and out to sea and calls their number beyond reckoning. Purananuru 18 makes water provision a ruler's practical responsibility. Thirumurai 2.99.9 imagines divine extent defeating two gods' attempt to measure it. Reading the verb alone loses the measured object, the agent and whether the attempt succeeds.
- **Which comparisons can lead to a study?** Akananuru 85 supplies a concrete animal-feeding scene that a reader can compare with other elephant scenes, coding food, recipient, location and narrative function. Thiruppugazh 344 supplies recurring syllables one could compare across identified performances, annotating pauses, duration and repetitions. These are research designs. The passages do not report the observations such studies would collect.
- **Where should a proposed link stop?** Paripadal 3 names elements and celestial bodies within a hymn to Māyōn. Its encompassing divine reality supports a comparison about devotional cosmology. The passage specifies no physical field, coupling, energy unit or detector that would make universal energy transfer a testable inference. Likewise, Tolkappiyam's attribution of one faculty to grasses and trees invites a history of classification. It cannot settle a contemporary question about subjective experience in plants.

## Following a reading

Find the listed Tamil phrase in the linked edition and read the surrounding lines. The link opens the whole edition. Project Madurai sometimes joins or separates words differently from the indexed line, so searching for a shorter portion may help. Ask who speaks, whom they address, what a comparison is doing and whether a second reading might account for the wording. Each entry gives an interpretive limit that a reviewer can challenge.

## Coverage and reproduction

Selection was purposive. We inspected Tamil passages containing words associated with illness, medicine, rain, sense, inquiry and measurement, as well as passages chosen for a relevant argument, fragment or counterexample. This selection overrepresents medical and weather vocabulary. The number of examples here cannot estimate the frequency of a theme, the accuracy of the full translation corpus or the strength of links within a tradition. Chronology and priority require separately dated witnesses.

The machine-readable ledger supplies the exact anchor, canonical identifier and Project Madurai edition key for every entry. To recheck from the repository root, run the following with Python 3. It compares the book set with the live index, verifies exact line membership, checks each local edition's catalogued SHA-256 digest and searches its visible text with spacing and punctuation folded. It verifies citation integrity. A second reader must still assess the English interpretation and plausible alternatives. When ingestion adds a book the set comparison reports the outstanding identifier.

```sh
python3 - <<'PYTHON'
from pathlib import Path
import hashlib, html, json, re, sys
sys.path.insert(0, 'scripts')
from science_inquiry import folded, rows, units
corpus = dict(units())
notes = list(rows(Path('kg/science/consciousness/book-readings.jsonl')))
books = {i.partition(':')[0] for i in corpus}
reviewed = {r['book'] for r in notes}
assert reviewed == books, sorted(books ^ reviewed)
assert len(notes) == len(reviewed)
catalog = {r['id']: r for r in rows(Path('data/catalog/documents.jsonl'))}
for r in notes:
    assert r['book'] == r['id'].partition(':')[0]
    assert any(r['anchor'] in line for line in corpus[r['id']]), r['id']
    edition = catalog['utf8__' + r['source']]
    assert r['source_url'] == edition['url']
    raw = Path(edition['raw_path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == edition['sha256']
    text = html.unescape(re.sub('<[^>]+>', ' ', raw.decode('utf-8-sig')))
    assert folded(r['anchor']) in folded(text), r['id']
print(len(notes), 'readings verified across', len(corpus), 'available units')
PYTHON
```

## Book-by-book readings

### acharakkovai:32

**உமிழ்வோடு** · Conduct

A person of discernment refrains from spitting or relieving themselves in ten named places. Path, cattle enclosure and sacred precinct share one rule of conduct.

The verse gives a rule of place and bodily comportment. An explanation in terms of germs would need separate evidence. [Tamil edition pmuni0024](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0024.html)

### ainkurunuru:243

**அறியா வேலன்** · Love lyric

The speaker asks whether the mother will accept a ritual specialist's account of a young woman's suffering. Calling him unknowing brings authority itself into question.

A contested explanation in a love poem cannot establish a medical diagnosis or a rejection of all ritual. [Tamil edition pmuni0028](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0028.html)

### ainthinai_aimpathu:5

**துளிகலந்து வீழ்தருங் கண்** · Love lyric

When clouds crowd the mountain and wind brings rain, drops also fall from the watching eye. The poem lets the reader feel a season through someone's tears.

The correspondence supplies no measure of how weather affects mood. [Tamil edition pmuni0027](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0027.html)

### ainthinai_ezhupathu:5

**இன்னுயிர் தாங்கும் மருந்து** · Love lyric

The addressee is asked to give the young woman a kindly look. His regard is the medicine that can sustain her life.

The proposed remedy is relational. No drug or preparation is identified. [Tamil edition pmuni0027](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0027.html)

### akananuru:85

**முற்றா மூங்கில் முளைதருபு, ஊட்டும்** · Love lyric

An elephant supplies tender bamboo in a scene of calf hunger and care. The friend places that scene within a reminder of the season when the absent lover promised to return.

This is evidence for the poem's representation of animal care. Frequency and species-wide behaviour remain unmeasured. [Tamil edition pmuni0229](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0229.html)

### avvaiyar:moodurai:20

**மாமலையில் உள்ள மருந்தே** · Moral verse

Disease can arise in one's own body while the cure grows on a distant mountain. The reversal prepares the point that someone outside the family can be a true help.

No particular mountain drug or curative effect can be recovered here. [Tamil edition pmuni0002](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0002.html)

### civaka_cintamani:2785

**வீழ்பிடிகள் சிந்தித்தும்** · Epic narrative

Wounded elephants tremble, remember their female companions and suffer inwardly. The narration gives animal memory a place in the cost of combat.

Narrative access to an animal's thoughts supplies neither an observation protocol nor neural evidence. [Tamil edition pmuni0672_03](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0672_03.html)

### elathi:57

**கருஞ்சிரங்கு வெண்தொழுநோய்** · Moral verse

The naming of bodily afflictions leads into a duty to relieve distress and feed sufferers. The verse imagines kingship as recompense for care.

Mapping these historical names to particular modern diseases needs more than a shared symptom. [Tamil edition pmuni0029](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0029.html)

### iniyavai_narpathu:2

**நிலையாமை நோக்கி** · Moral verse

The praise of household life is conditional. Contemplating impermanence can also make renunciation desirable.

Impermanence is a reason for choosing a way of life. No lifespan is calculated. [Tamil edition pmuni0025](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0025.html)

### innaa_narpathu:1

**மந்திரம் வாயா விடின்** · Moral verse

Among painful outcomes the poet includes the case where a mantra fails. The little conditional ending matters to how the claim is read.

The admission of failure gives no rate of success or test of efficacy. [Tamil edition pmuni0025](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0025.html)

### kainnilai:33

**களையாரோ நீயுற்ற நோய்** · Fragmentary love lyric

A question survives about whether a chariot-borne arrival might relieve someone's distress. Visible gaps in the opening lines interrupt the scene.

The surviving text leaves the full circumstances of the affliction unresolved. [Tamil edition pmuni0051](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0051.html)

### kalavazhi_narpathu:3

**களிற்றுக்கோ டூன்றி யெழுவர்** · Battle poem

People slipping amid flowing blood use an elephant tusk for support to rise. The sound of rain belongs to the description of the battle drum.

A literal search for rain would misclassify the setting. The episode gives no casualty rate. [Tamil edition pmuni0025](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0025.html)

### kalittokai:99

**வடுக் காட்டக், கண் காணாதற்று** · Love lyric

An eye with reach into the distance cannot see its own blemish. The speaker uses this asymmetry to expose the powerful addressee's failure to see a woman's suffering.

The comparison turns on recognition and responsibility. No test of eyesight is described. [Tamil edition pmuni0221](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0221.html)

### kar_narpathu:40

**நோய்தீர் மருந்தாகி** · Seasonal love lyric

For the woman distressed that the promised signs have come while her lover has stayed away, the darkening sky becomes medicine. Expectation changes the sky's significance.

The poem does not identify a pharmacological action of clouds. [Tamil edition pmuni0029](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0029.html)

### kundalakesi:5

**நெய்யினா லவிக்க லாமோ** · Argument in verse

Can ghee extinguish a fire? The question challenges the claim that indulging desire will consume desire itself.

An argumentative analogy cannot determine the effects of a treatment for addiction. [Tamil edition pmuni0507](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0507.html)

### kural:948

**நோய்முதல் நாடி** · Medical maxim

Investigate the illness, its source and the means of easing it, then act fittingly. Repetition of the verb for inquiry makes the order of reasoning audible.

The maxim names no clinical trial, remedy or outcome. [Tamil edition pmuni0001](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0001.html)

### kuruntokai:3

**கருங்கோற் குறிஞ்சிப் பூக்கொண்டு** · Love lyric

Land, sky and water become measures that a bond exceeds. Then a bee's mountain flower and its honey bring the scale of the claim close to hand.

The superlatives measure the speaker's attachment. They give no cosmological dimensions. [Tamil edition pmuni0110](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0110.html)

### manimekalai:19:144-162

**உயிர் மருந்து இது** · Epic dialogue

A miraculous begging bowl relieves hunger. Asked what he can do, the king receives a request to turn the prison into a charitable institution. The movement from food to policy matters to what 'life medicine' means.

The narrative can motivate a question about institutions and hunger. Its bowl supplies no reproducible treatment. [Tamil edition pmuni0141](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0141.html)

### muthumozhikkanchi:33

**நாணில் வாழ்க்கை** · Moral maxim

A life without a sense of shame is weighed against hunger. The ethical cost is expressed in terms of a bodily deprivation anyone can recognize.

This comparison gives no physiological ranking of hunger and shame. [Tamil edition pmuni0025](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0025.html)

### naga_kumara_kaviyam:22

**கறமழை யைப்பெயுந்** · Epic devotional scene

The ascetic's teaching falls as a rain of virtue upon living beings. The devotee reveres the teacher whose words carry it.

Reading rain as actual precipitation would erase the teacher and the act of hearing. [Tamil edition pmuni0601](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0601.html)

### naladiyar:247

**பிரியப் பிரியுமாம் நோய்** · Moral verse

Association with discerning people increases joy. Distance from people who fail to understand lets distress recede. The repeated verbs convey a gradual change.

The relation is an ethical judgment about company. It supplies no psychiatric diagnosis. [Tamil edition pmuni0016](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0016.html)

### nanmanikkadigai:47

**மழையின்றி மாநிலத்தார்க் கில்லை** · Moral verse

The need for rain begins a chain that also makes rain depend on ascetics, austerity on kingship and kingship on householders. The circular dependence puts ordinary households inside political order.

Ecological dependence and a moral account of rain have different evidential standing. [Tamil edition pmuni0047](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0047.html)

### natrinai:160

**மழைக் கண் காணா ஊங்கே** · Love lyric

The speaker claims to have understood honour and right conduct before seeing the woman's rain-like eyes. Encounter changes what that earlier confidence is worth.

The rain epithet characterizes eyes within the encounter. It records no weather event. [Tamil edition pmuni0296](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0296.html)

### neelakesi:235

**வீடு பேறும் வினையு முரைப்புழி** · Debate narrative

A seated teacher expounds liberation and action before an audience. Attribution to a particular speaker matters in a work staged around debate.

This scene alone cannot establish the narrator's assent to every doctrine taught there. [Tamil edition pmuni0538](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0538.html)

### paripadal:3

**தீ வளி விசும்பு நிலன் நீர் ஐந்தும்** · Devotional hymn

Fire, air, space, earth and water join sun, moon and other beings in a catalogue addressed to Māyōn. Multiplicity is gathered into the relation to the deity.

A sacred whole here gives no physical field, instrument or test of cosmic consciousness. [Tamil edition pmuni0087](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0087.html)

### patitruppattu:45

**மழைகொளக் குறையாது புனல்புக நிறையாது** · Royal praise

An ocean neither visibly emptied by rain-taking nor filled by incoming water magnifies the feat of facing its waves. Observe where the description lands in this praise of power.

The apparent constancy of the sea gives no quantified water balance. [Tamil edition pmuni0038](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0038.html)

### pattupattu:9:127-139

**நீரினின்று நிலத்தேற்றவும்** · Port-city poem

Rain and mountain runoff introduce cargo moving in both directions between ship and land. The tiger mark and piled sacks make the movement of goods unusually concrete.

The weather analogy gives no rainfall or cargo volumes. The text itself calls the goods beyond reckoning. [Tamil edition pmuni0077](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0077.html)

### pazhamozhi_nanooru:93

**விதைத்தாலும் நாறாத வித்துள** · Proverb verse

Some flowers yield no fruit and some sown seeds never sprout. These everyday failures challenge the expectation that anyone instructed will acquire understanding.

The counterexamples work rhetorically. They give neither a germination rate nor a general law of learning. [Tamil edition pmuni0036](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0036.html)

### prabandham:1222

**வணங்கென் மனனே** · Devotional hymn

Cuckoos, peacocks and rain-washed groves locate the temple at Nāṅgūr. The closing direction to the speaker's own mind is to bow there.

Inner address coexists with public temple worship. A simple inward-versus-external classification misses this. [Tamil edition pmuni0006_01](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0006_01.html)

### purananuru:18

**நீரும் நிலனும்** · Counsel to a king

Joining water and land is credited with creating bodily life. The address to a ruler makes provision for water a public obligation and connects it to food.

A practical rationale for water management does not supply a measured yield or hydraulic design. [Tamil edition pmuni0057](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0057.html)

### siddhar:sivavakkiyam:215

**தம்முளே பெற்றுணர்ந்த ஞானிகள்** · Siddhar verse

The verse moves from an expansive divine radiance to knowers who realize it within themselves, then denies caste difference. Social equality is part of what this realization entails here.

The sequence establishes a religious and social claim. It identifies no universal energy signal or means of measuring one. [Tamil edition pmuni0269](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0269.html)

### silappathikaram:7:186-189

**வண்டல் திரைஅழிப்பக்** · Coastal song within an epic

Waves destroy a construction on the shore and hands scoop sand in response. The coastal voice surrounds an accusation about the lingering affliction brought to women.

The seaside action belongs to an address with emotional stakes. It gives no erosion rate. [Tamil edition pmuni0046](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0046.html)

### sirupanchamoolam:payiram

**சிறுபஞ்ச மூலம்செய் தான்** · Prefatory praise

The preface names the maker and the work and praises relief from affliction. Its threshold position matters when interpreting the medicinal title of a book of ethical verses.

Praise in a preface does not establish the ingredients, dose or efficacy of a five-root medicine. [Tamil edition pmuni0029](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0029.html)

### soolamani:396

**ரழிபசி யகற்றும்** · Epic praise

Relieving the severe hunger of the distressed opens the verse. Praise then turns to virtue, restraint of sensory enjoyment and the holy teacher's words.

The conjunction invites inquiry into the ethics of feeding. It supplies no biological mechanism of liberation. [Tamil edition pmuni0035_02](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0035_02.html)

### thinaimalai_nootraimpathu:142

**மாலும்மா றாநோய் மருந்து** · Love lyric

The woman's persistent affliction finds its remedy in the man's chest. The opening image of water birds belongs to an address to the man of the cultivated fields.

Literalizing the remedy would miss its bodily and relational referent. [Tamil edition pmuni0056](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0056.html)

### thinaimozhi_aimpathu:45

**உடலுள் உறுநோய்** · Coastal love lyric

Pearls and the women who wear them locate the coastal lord. A friend's affliction is said to be inside the body as her condition is voiced to him.

An embodied description of longing is insufficient for retrospective diagnosis. [Tamil edition pmuni0027](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0027.html)

### thirikadugam:96

**பெய்எனப் பெய்யும் மழை** · Moral verse

The wife who discerns intention, the ascetic who acts fittingly and the king who avoids wrongdoing are granted the power to call rain. Gender and rank organize this ideal of conduct.

The praise gives no observations testing whether virtue changes weather. [Tamil edition pmuni0048](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0048.html)

### thirumurai:2.99.9

**சென்றளந்துங் காண்கிலா** · Temple hymn

Vishnu and Brahma go to measure and cannot see the divine extent. The movement of the stanza is toward visiting Kōṭikāvu, with relief from affliction promised.

The thwarted attempt marks divine immeasurability. No measurement result or medical outcome is recorded. [Tamil edition pmuni0162](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0162.html)

### thiruppugazh:344

**இச்சிறுமி நொந்து** · Devotional petition

The moon and the sounding sea trouble a young woman. The voice asks for reassurance and turns to the peacock-riding lord. Repeated syllables give the petition an insistent audible shape.

The words support a study of repetition in performance. Effects on listeners would require recordings and a listening study. [Tamil edition pmuni0187](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0187.html)

### tholkappiyam:porul:9:28

**புல்லும் மரனும் ஓர் அறிவினவே** · Classification in a grammar

Grasses and trees are grouped as beings with one faculty of knowing. The next line explicitly allows other members of the same class: a category is taught through examples without closing its membership.

This historical sensory taxonomy provides no evidence that plant signalling today equals a particular subjective experience. [Tamil edition pmuni0100](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0100.html)

### tirumanthiram:725

**உடம்பினுக் குள்ளே யுறுபொருள் கண்டேன்** · Devotional reflection

The speaker formerly despised the body. Finding an abiding reality within and recognizing the divine temple there changes the speaker's practice to caring for the body.

The verse's reversal gives a reason for bodily care. It prescribes no breathing schedule, drug or quantum mechanism. [Tamil edition pmuni0009_01](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0009_01.html)

### tiruvasagam:640

**வீணை முரன்றெழும் ஓசையில்** · Devotional hymn

The sound of the vīṇā and anticipated delight belong to a succession of questions that culminate in the Lord's gracious appearance. The music is imagined within that condition.

This evocation of sound supplies neither a recording nor evidence for a therapeutic frequency. [Tamil edition pmuni0003_02](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0003_02.html)

### udayana_kumara_kaviyam:361

**பொறிகளை மனத்தடக்கிப்** · Ascetic epic

Protecting six classes of embodied beings stands beside drawing the senses under the mind, vows and meditation. Cultivation of attention occurs within an ethic of care.

The scene offers no controlled assessment of fasting or meditation and no warrant for medical prescriptions. [Tamil edition pmuni0597](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0597.html)

### valayapathi:59

**கொம்பிடை வாழுங் குரங்கும்** · Fragmentary moral verse

Women depicted as moving from the less wealthy lover to the wealthier are compared to branch-dwelling monkeys. The simile exposes the speaker's judgment about attachment and wealth.

This gendered comparison cannot establish the actual behaviour of either women or monkeys. [Tamil edition pmuni0062](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0062.html)

### yasodhara_kaviyam:255

**பிறவியின் மறுகு வெந்நோய்** · Religious epic

A collective voice recalls earlier births and credits a religious teacher with escape from the burning sickness of rebirth. Memory is narrated within a claim about liberation.

The testimony gives the narrative's understanding of rebirth. It supplies no independent verification of past-life recall. [Tamil edition pmuni0508_02](https://www.projectmadurai.org/pm_etexts/utf8/pmuni0508_02.html)
