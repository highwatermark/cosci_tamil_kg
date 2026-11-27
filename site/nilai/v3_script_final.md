# Nilai intro reel, v3 final: script and art direction

Status: script only, no code. This revises `site/nilai/v3_script.md` after the independent critique in `site/nilai/v3_critique.md`. The earlier file is kept unchanged for comparison.
Spine: the thirteen core categories in `kg/themes/concept_categories.json`, four aims and then nine families.
Length: 31 scenes, about 2:50.

What changed from v3, in short:
- 39 scenes became 31. Most categories are now one scene with the whole morph in it, THEN to NOW to FUTURE.
- One Tamil anchor block per scene, full size, at most three lines. The small second anchors are gone.
- The notebook moved before the far horizon, and "steer" moved with it: it answers the fifth pencil worry and turns the reel towards the sky. After the peak there is one closing beat, the lamp and the ledger together.
- The far horizon is a climb: sky, wind, matter, life, mind, the empty rung.
- New scenes: the gecko's feet (biomimicry), Pambatti's boast (hurried evolution), mind froths up (the materialist in the debate hall).
- Each "what played out" has one dated event and names its real 2026 seed.
- The colour rules gained a wall-to-floor minimum, an art-to-art rule and a fixed ledger strip. Every scene's ratios are listed in section 6.

---

## 1. Premise and voice

The reel is the same `nilai.md` the visitor is standing on, five hundred years later. The file was started in 2026 and has been recopied and corrected by a new hand about once a century, the way a palm-leaf book had to be recopied before the leaf crumbled. The narrator is the hand of 2526: a young keeper with an iron stylus and a myna that repeats everything. She writes back to the hand of 2026, who is the reader. Each 2026 worry is still in the margin as a faint pencil note, and a later hand has struck it through in ink and written what happened: one dated event, the first mistake, and the thing a reader in 2026 could already have seen starting. The future is told as settled history. Things came true, got boring and got handled, and two or three of the hands admit what it cost. Every date after 2026 carries the tag **கற்பனை · imagined**. The old books are credited with what they actually said and with a posture: watching closely, arguing honestly, expecting an answer stranger than the asker. They are never credited with modern science. The essence is carried by a second device, the **ledger of what we uphold**: a palm-leaf strip at the edge of the stage that gains one handwritten line per category and is handed to the reader at the end as their own `nilai.md`.

Two actors. The **keeper**: about fourteen, short hair, a stylus behind one ear. The **myna** (மைனா): a common myna with a yellow eye-patch and yellow legs, a mimic. It is the fluent voice that does not know what it is saying, so it is the running joke and also the argument.

### What plays, and what waits

The reel is scroll-driven. At playing speed a viewer gets three things per scene, and they are enough to follow the argument:
1. **the sentence**: large, one per scene, 13 words or fewer, emphasis in bold.
2. **the morph**: one object, THEN to NOW to FUTURE, with one primary motion that covers at least 30% of the frame and lasts at least one second.
3. **the ledger line**, in the last scene of each category.

Three more layers are on screen but small, and they reward a viewer who stops scrolling:
4. **the anchor**: the Tamil, its id and our reading. One block per scene, at most three lines of Tamil.
5. **the margin**: first the 2026 pencil worry, then a later hand's ink striking it through and answering it.
6. **the gag**: it plays after the sentence has landed, never during it.

### Timing

| scenes | seconds each | total |
|---|---|---|
| 28 ordinary scenes | 5.2 | 145.6 |
| 25, look up | 9 | 9 |
| 30, the seventh rung | 8 | 8 |
| 31, the lamp and the ledger | 9 | 9 |
| **all 31** | | **about 172 s, 2:50** |

### Phone width

Every scene has a **Phone** line. The general rules:
- The object fills the width. The secondary actor and the myna are drawn at no less than one sixth of the frame height.
- The margin collapses to one line (the later hand's dated event). The pencil worry shows only as a struck-through stub.
- The anchor shows the Tamil and the id. The reading opens on tap.
- A gag that depends on a small detail is either scaled up until the detail is the subject, or swapped for the simpler version named in the scene.

---

## 2. Palette and colour rules

| name | hex | group | note |
|---|---|---|---|
| kolam-chalk white | `#F7F2E6` | light | |
| palm-leaf tan | `#CDAE78` | light | deepened from v3 so that chalk and tan separate as wall and floor |
| turmeric | `#F2B21B` | light | |
| brass | `#AE7F1B` | accent only | never a wall, a floor or a main art fill |
| night indigo | `#171C45` | dark | |
| temple-stone grey | `#4B4D50` | dark | |
| peacock teal | `#0A5C63` | dark | deepened from v3 so that it clears 3:1 on tan |
| laterite | `#9A3B21` | dark | |
| kumkum red | `#BE1230` | dark | |

Rules. Every scene obeys all of them, and section 6 lists the computed ratios scene by scene.
1. Wall and floor come from the same group. All art comes from the other group, so art can never match its background.
2. Scenes alternate dark wall and light wall with no exceptions. Odd scenes are dark and even scenes are light, so the reel opens at night, looks up at night (25) and ends by lamplight (31).
3. **Wall and floor differ by at least 1.6:1**, so the horizon line never disappears. In practice every dark scene pairs indigo with one other dark colour, and every light scene pairs chalk with turmeric or tan.
4. Every art fill is at least 3:1 against both wall and floor. Text is at least 4.5:1 against the wall.
5. **Art is two fills per scene: one ink and one colour.** On light walls the ink is indigo and the colour is one of teal, laterite, kumkum or grey. On dark walls the ink is chalk and the colour is turmeric or tan. The two fills are always at least 1.5:1 apart and at least 30 apart in CIE delta-E. Teal never sits beside kumkum or laterite, because that pair differs in hue only and is lost to red-green colour blindness.
6. **Keyline.** Wherever two art fills touch, draw a 1.5 px keyline between them in the wall colour. Where an art fill crosses the horizon, it keeps a 1.5 px keyline in the floor colour below the line.
7. **Accent.** One accent colour may sit on top of art only, never on the wall or floor. On light walls it is brass on the indigo ink. On dark walls it is a dark colour that is neither the wall nor the floor, placed on the chalk ink. It marks the one thing the eye should find: the flame, the coin, the ruby, the highlight in the notebook.
8. **The ledger strip** is chalk lettered in indigo on dark walls, and indigo lettered in chalk on light walls. That is 14.6:1 in every scene.
9. Art colours are stylised. A green leaf on a turmeric wall is teal, and a brass lamp on an indigo wall is chalk with a turmeric flame. Never rescue a literal colour by breaking a rule.

---

## 3. The arc: 31 scenes

Scene numbers are the reel's `nn/31` counter. Each (d) line is generated from the table in section 6.

### Opening

#### 01 · the hand of 2526
- (a) "From 2526: your worries all came **true**, got boring, then got handled."
- (b) Header: `nilai.md · நிலை · last touched 27 Nov 2526`
- Margin: the five pencil worries of 2026, all at once and faint: *what if everyone has it? · what if it widens the gap? · what if the wrong hands get it? · what will creativity be? · steer, or be steered?* The keeper ticks four. She leaves the fifth for later.
- (c) VISUAL. THEN: an ஓலைச்சுவடி, a palm-leaf book. Narrow strips about 4 cm by 35 cm, a string hole in each, a cotton cord through them, wooden boards above and below, letters incised with an iron stylus and darkened with lampblack. NOW: the strips square up and fuse into a phone, and the cord becomes its charging cable. FUTURE: the phone thins back into one leaf that glows faintly from inside. It slides to the right edge of the stage with thirteen ruled lines on it. This is the **ledger strip**, and it stays for the rest of the reel.
  Primary motion: the bundle closing into the phone and opening back into the leaf, full width.
  Secondary actor: the keeper is already writing on the leaf when it arrives.
- Gag: the "last touched" year rolls from 2026 to 2526, overshoots to 2527 and ticks back. The myna, riding the top board, slides off as it becomes the top of the phone.
- Phone: the year counter is the headline and sits above the sentence at full width. The five worries show as five struck stubs.
- (d) Colour: wall indigo · floor teal · text chalk · art chalk (ink), turmeric · accent kumkum · strip chalk, indigo letters

### The four aims

#### 02 · அறம் · the beam that levels first
- (a) "The Kural's fair mind is a **scale**: it levels first, then weighs."
- (b) Header: `அறம் · virtue and conduct · what was upheld`
- Anchor:
  > சமன்செய்து சீர்தூக்குங் கோல்போல் அமைந்தொருபால் — kural:118
  > கோடாமை சான்றோர்க் கணி — kural:118
  Our reading: like the beam that sets itself level and then weighs, standing without a lean to either side is what adorns the worthy. (3 sound links.)
- Margin: *what if the wrong hands get it?* (2026, pencil.)
- (c) VISUAL. THEN: a hand-held தராசு. A wooden beam a forearm long, a pointer tongue in a small fork at the centre, two shallow pans on three cords each. The keeper lifts it by the loop and waits for the tongue to settle. NOW: the pans draw in and the cords stiffen into the glass case of a laboratory balance. The tongue becomes a readout: `0.0000 g`. FUTURE, left open for the next scene: the glass case empties, the keeper's hand is gone from the loop, and the readout changes to one word, `FAIR`.
  Primary motion: the beam swinging and settling level, full width.
  Secondary actor: the keeper, whose hand is on the loop until the last second.
- Gag: the myna lands on one pan. Two seconds later the lab balance reads `0.0000 g`, shows a small myna icon, and asks `TARE?`
- Phone: the readout is as large as the sentence. `TARE?` replaces the icon.
- (d) Colour: wall chalk · floor tan · text indigo · art indigo (ink), teal · accent brass · strip indigo, chalk letters

#### 03 · அறம் · the king who did not check
- (a) "Villains did less harm than honest **officials** who never checked the machine."
- (b) Header: `அறம் · 2041 · கற்பனை · imagined`
- Anchor:
  > தேரா மன்னா செப்புவ துடையேன் — silappathikaram:20
  > யானோ அரசன் யானே கள்வன் — silappathikaram:20
  Our reading: "King who did not examine, I have something to say." And his answer, once the anklet is broken open: "Am I a king? I am the thief." (Lines 60 and 85.)
- Margin (hand of 2276, in ink over the pencil): *We guarded the tool against thieves. The epic had warned us about the judge. You had already seen it start: postmasters convicted on a ledger program's word, families ruined by a benefits algorithm. 2041: the first verdict that had to carry a name.*
- (c) VISUAL. THEN: Kannagi's சிலம்பு, a hollow gold anklet with a seam, held up in a king's court. It is dashed on the floor and red stones scatter where pearls were claimed. NOW: the anklet's ring is the rim of a counter-top terminal that prints a shortfall, and nobody opens it to look. FUTURE: the keeper cracks the terminal's case the same way. Under every figure it prints there is now a line with a thumbprint: *weighed by*, and a name.
  Primary motion: the anklet striking the floor and the red stones crossing the whole frame.
  Secondary actor: the myna chases one red stone and brings it back.
- Gag: while unattended, the terminal prints `FAIR` on a receipt that never stops unrolling. It reaches the edge of the frame and keeps going into the next scene.
- Ledger line: **அறம் · someone who answers for the weighing**
- Phone: the receipt runs straight down the screen and the viewer scrolls along it.
- (d) Colour: wall indigo · floor grey · text chalk · art chalk (ink), turmeric · accent kumkum · strip chalk, indigo letters

#### 04 · பொருள் · the hoard becomes a tank
- (a) "The Kural says the poor's tears are a **weapon** that grinds fortunes down."
- (b) Header: `பொருள் · wealth, polity and the world · 2068 · கற்பனை · imagined`
- Anchor:
  > அல்லற்பட்டு ஆற்றாது அழுதகண் ணீரன்றே — kural:555
  > செல்வத்தைத் தேய்க்கும் படை — kural:555
  Our reading: the tears of people who suffered past bearing are the weapon that wears wealth away. (5 sound links, including Purananuru 72.)
- Margin: *what if it widens the gap?* (2026.) Then the hand of 2126: *For decades the poor got last year's intelligence, and it showed in who got the jobs. Then the hoards went stale. A machine fed on its own answers forgets the world, and you had a name for that by 2024. 2068: the closed models were worth less than the open tank.*
- (c) VISUAL, one continuous shot. THEN: a narrow-necked clay pot buried to its shoulder, full of Roman gold coins, each with an emperor's head. Such hoards have been dug up in the Tamil country. NOW: the pot is a sealed vault of machines, and inside it each coin is struck from the one before. The face blurs a little with every copy until the last coin is blank. FUTURE: the pot cracks. Water runs out of the crack, the camera pulls back, and the crack is the stone sluice of an ஏரி, a village tank with an earthen bund. People draw from it, and once a year they climb in together to clear the silt.
  Primary motion: the pull-back from the crack to the whole tank.
  Secondary actor: the keeper puts her ear to the pot before it cracks. It is very full and very quiet.
- Gag: the pot carries a label, "for later", in four different centuries' handwriting.
- Ledger line: **பொருள் · the decision to give it away**
- Phone: show three coins, sharp, blurred and blank, at full width. The label is as wide as the pot.
- (d) Colour: wall turmeric · floor chalk · text indigo · art indigo (ink), laterite · accent brass · strip indigo, chalk letters

#### 05 · இன்பம் · the third voice
- (a) "By 2060 every letter was flawless, and flawless meant **nobody came**."
- (b) Header: `இன்பம் · love · 2060 · கற்பனை · imagined`
- Anchor:
  > சிறுகோட்டுப் பெரும்பழந் தூங்கி யாங்கிவள் — kuruntokai:18
  > உயிர்தவச் சிறிது காமமோ பெரிதே. — kuruntokai:18
  Our reading: like a huge jackfruit hanging from a small stalk, her life is slight and her love is very large. Kapilar. The colophon says தோழி கூற்று: the friend speaks, and the woman never does. (2 sound links.)
- Margin: *when a model is the third voice, whose feeling arrives?* (2026.) Then the hand of 2276: *Once letters cost nothing they proved nothing. Biologists had said it of the peacock's tail: a signal has to cost something. The friend in the poem risked the blame. That was the part we had automated away.*
- (c) VISUAL. THEN: the letter in the Silappathikaram. A long white petal of தாழை, screwpine, written on with a jasmine bud dipped in red lac, rolled and given to a friend who sets off with it and looks back once. NOW: the petal squares into a chat bubble with three typing dots. The dots vanish and a perfect paragraph arrives at once, and the same paragraph arrives in every other bubble on the wall. FUTURE: one bubble unrolls into a letter that keeps its drafts: two lines struck through, one word written three times, a long pause mark, a water stain.
  Primary motion: the wall of identical bubbles filling the frame, then one of them unrolling.
  Secondary actor: the keeper writes, crosses out, writes again, and sends it with the crossings-out.
- Gag: the autocorrect tidies the water stain away. She puts it back with a wet finger.
- Ledger line: **இன்பம் · my own voice, cracks included**
- Phone: one bubble only, then the unrolled letter at full width. The stain is thumb-sized.
- (d) Colour: wall laterite · floor indigo · text chalk · art chalk (ink), tan · accent teal · strip chalk, indigo letters

#### 06 · வீடு · the lamp that can go out
- (a) "What you have let go can't **hurt** you any more, says the Kural."
- (b) Header: `வீடு · release · 2190 · கற்பனை · imagined`
- Anchor:
  > யாதனின் யாதனின் நீங்கியான் நோதல் — kural:341
  > அதனின் அதனின் இலன் — kural:341
  Our reading: whatever a person has let go of, from that thing no pain comes to them. (3 sound links.)
- Margin: *when anything can be done for us, what is still hard?* (2026.) Then the hand of 2276: *We got everything on tap and found that wanting was on tap too. The feeds learned what we wanted faster than we did. Nothing outside us was hard any more, so the hard things moved indoors. 2190: the first device sold on one feature. It turns off.*
- (c) VISUAL. THEN: an அகல், a palm-sized clay lamp, one cotton wick in oil. The flame shortens, goes out, and leaves one upright thread of smoke. NOW: the clay rim straightens into a phone lying face up. It dims and then, instead of going dark, shows the time, a dot, another dot. It multiplies into a wall of glowing rectangles. FUTURE: one rectangle rounds back into a clay lamp whose flame goes out by itself at dusk, with the same thread of smoke. The wall behind it is dark and nobody minds.
  Primary motion: the wall of rectangles switching off from the edges inward until one lamp is left.
  Secondary actor: the keeper puts down three things she is carrying, one at a time, and keeps the stylus.
- Gag: the myna puts its head under its wing to show the phone how it is done.
- Ledger line: **வீடு · choosing what to put down**
- Phone: four rectangles instead of a wall. The smoke thread runs the height of the screen.
- (d) Colour: wall chalk · floor tan · text indigo · art indigo (ink), grey · accent brass · strip indigo, chalk letters

### The nine families

#### 07 · சமூகம் · the row
- (a) "A prince wrote that the world stands on people who **won't eat alone**."
- (b) Header: `சமூகம் · society, caste and ritual · what was upheld`
- Anchor:
  > உண்டால் அம்ம, இவ்வுலகம்; இந்திரர்; — purananuru:182
  > அமிழ்தம் இயைவ தாயினும், இனிதுஎனத் — purananuru:182
  > தமியர் உண்டலும் இலரே; முனிவிலர்! — purananuru:182
  Our reading: this world exists because there are people who would not eat alone, even if they came by the gods' own nectar. By கடலுள் மாய்ந்த இளம்பெரு வழுதி. (6 sound links, including Kural 996.)
- Margin: *intelligence is nectar at some tables and rationed at others* (2026.)
- (c) VISUAL. THEN: a பந்தி, a feast row. Banana leaves in a line on the floor, each with its narrow tip to the eater's left and a pinch of salt at the top corner, a mound of rice in the middle. NOW: the row tilts upright. Each leaf is a server blade in a rack and the midribs line up into a cable spine. FUTURE: the rack's doors come off and it is laid flat again in a public hall. People sit along it as they would at a meal, and it runs out of frame at both ends.
  Primary motion: the whole row tilting up into the rack and lying back down.
  Secondary actor: the keeper serves along the row and reaches the end before she sits.
- Gag: on the rack, the indicator lights come on in the order a meal is served, salt first.
- Phone: three leaves, large. The lights are one per leaf.
- (d) Colour: wall teal · floor indigo · text chalk · art chalk (ink), tan · accent kumkum · strip chalk, indigo letters

#### 08 · சமூகம் · nothing written in flesh
- (a) "We learned to write into flesh, and someone tried to write **rank** there."
- (b) Header: `சமூகம் · 2071 to 2270 · கற்பனை · imagined`
- Anchor:
  > பிறப்பொக்கும் எல்லா உயிர்க்கும் சிறப்பொவ்வா — kural:972
  > செய்தொழில் வேற்றுமை யான் — kural:972
  > இறைச்சிதோல் எலும்பினும் இலக்கமிட்டு இருக்குதோ? — siddhar:sivavakkiyam:39
  Our reading: birth is the same for every living thing, and standing differs only by what each one does. And Sivavakkiyar: is there a number stamped on flesh, skin or bone? (Kural 972 has 14 sound links, the most of any anchor here.)
- Margin: *once we can write into flesh, will we write caste there?* (2026.) Then the hand of 2276: *The books argued both sides of birth. The same Kural praises good family. We kept the side that survived being tested. In your day embryos were already being scored for sale. 2071: the first school to ask for the score. It took two centuries to make the row one row again.*
- (c) VISUAL. THEN: the feast row with a cloth screen hung down the middle, a long row on one side and a short, well-lit row on the other. This is history, and recent history. NOW: the screen is a printed score sheet, and each seat has a small number on it. FUTURE: the sheet is rolled up. One unbroken row runs out of frame, and the numbers have become place cards that only say *next*.
  Primary motion: the screen rolling up and the two rows closing into one.
  Secondary actor: the keeper lays one more leaf at the end of the row, for whoever arrives.
- Gag: the myna is served first. It looks down the long row of empty leaves, then pushes its own leaf to the far end and walks after it.
- Ledger line: **சமூகம் · laying the next leaf for a stranger**
- Phone: the screen runs top to bottom of the frame and rolls upward. The myna's walk is the whole width.
- (d) Colour: wall chalk · floor turmeric · text indigo · art indigo (ink), teal · accent brass · strip indigo, chalk letters

#### 09 · இயற்கை · rain first
- (a) "Crooked rule stops the rain, says the Kural; we eventually found the **pipes**."
- (b) Header: `இயற்கை · nature and landscape · 2047 · கற்பனை · imagined`
- Anchor:
  > நீர்இன்று அமையாது உலகெனின் யார்யார்க்கும் — kural:20
  > வான்இன்று அமையாது ஒழுக்கு — kural:20
  > முறைகோடி மன்னவன் செய்யின் உறைகோடி — kural:559
  Our reading: if the world cannot go on without water, for anyone at all, then without the sky there is no flow of it. And: if the king bends justice, the season bends and the sky holds back its rain. (Kural 20 has 4 sound links. Kural 559 is quoted by its first line.)
- Margin: *the rains are moving* (2026.) Then the hand of 2126: *It read like a threat from heaven. It turned out to be plumbing. Haze from our own chimneys had already thinned the monsoon once, in your grandparents' time. 2047: rain went on the cabinet's agenda as something a government does, and can be blamed for.*
- (c) VISUAL. THEN: five painted stage flats in a row, each a landscape with its own hour and its own mood, as the grammar pairs them. Hill at midnight, two people meeting. Forest edge at evening, a woman at a door. Paddy at dawn, a quarrel. Shore at sunset, someone watching the sea. Cracked ground at noon, a figure walking away. A curtain of rain crosses all five from left to right, and each landscape answers it. NOW: the flats lie down into one satellite map. The band of cloud that should cross it is thin and broken under a brown haze. FUTURE: the haze lifts from one edge. The cloud band thickens and crosses again, and the flats stand back up in the rain.
  Primary motion: the rain curtain crossing the full width, twice.
  Secondary actor: the keeper walks behind the flats and comes out of each one in a different mood.
- Gag: the myna opens a palm-leaf umbrella it has apparently carried the whole reel. It is the right size for a myna and no use to anyone else. The keeper gets wet and does not mind.
- Phone: three flats (hill, paddy, cracked ground). The rain curtain is the whole screen.
- (d) Colour: wall indigo · floor teal · text chalk · art chalk (ink), turmeric · accent kumkum · strip chalk, indigo letters

#### 10 · இயற்கை · the names
- (a) "You can't protect what you can't name; these poems named 3,232 **native things**."
- (b) Header: `இயற்கை · 2112 · கற்பனை · imagined`
- Anchor:
  > தினைத்தாள் அன்ன சிறுபசுங் கால — kuruntokai:25
  > ஒழுகுநீர் ஆரல் பார்க்கும் — kuruntokai:25
  > குருகும் உண்டுதான் மணந்த ஞான்றே. — kuruntokai:25
  Our reading: Kapilar's girl says her only witness, on the day he took her, was a heron with small green legs like millet stalks, watching the running water for eels. The bird carries what she cannot say. The grammar calls such native things கரு: the god, food, beast, tree, bird and drum of each land.
- Margin: *the lists of living things are getting shorter* (2026.) Then the hand of 2126: *We filed the land under resource. The poets had filed it under heart. Each generation took the emptier world it was born into for the normal one, and you had a name for that too. 2112: the baseline for this coast was rebuilt from the love poems. The oldest full list we had was a love poem.*
- (c) VISUAL. THEN: the shore flat from the last scene, crowded with small labelled things: a heron, an eel, a water lily, a screwpine, a drum, a fishing net. NOW: it is a map with a legend. The entries grey out one by one and merge into a single line, *other*. The map gets tidier and emptier. FUTURE: the legend is a cabinet of small labelled drawers. The keeper opens குருகு and a heron steps out on thin legs and walks back onto the flat. She opens ஆரல் and there is water for the eel.
  Primary motion: the heron stepping out of the drawer and crossing the frame.
  Secondary actor: the keeper reads each label aloud before she opens it.
- Gag: the myna finds its own drawer, மைனா, checks that everything is in order, and shuts it.
- Phone: four drawers, each a quarter of the width. One creature at a time.
- Note: 3,232 is the count of கரு nodes across the five Sangam groups in `kg/groups`. It includes foods, peoples and their work as well as plants and animals, so the sentence says "native things".
- (d) Colour: wall tan · floor chalk · text indigo · art indigo (ink), teal · accent brass · strip indigo, chalk letters

#### 11 · இயற்கை · the wasteland is made
- (a) "The epic said drought **makes** the wasteland, so we learned to unmake it."
- (b) Header: `இயற்கை · 2090 to 2526 · கற்பனை · imagined`
- Anchor:
  > முல்லையுங் குறிஞ்சியும் முறைமையின் திரிந்து — silappathikaram:11
  > பாலை யென்பதோர் படிவங் கொள்ளும் — silappathikaram:11
  Our reading: forest and hill, turned from their own nature, take on the form that is called pālai. The wasteland has no ground of its own. It is what the others become. (Lines 64 and 66.)
- Margin: *we keep rebuilding the same coast* (2026.) Then the hand of 2276: *2090: the third rebuilding of the same town in the same place, and the last. After that we stopped holding the old lines and started keeping the old names. Mars got a landscape of its own, and its own poems of parting.*
- (c) VISUAL. THEN: the five flats, with the cracked-ground flat much wider than the rest. NOW: on the shore flat a small town is rebuilt three times on the same spot, each time a little taller on its stilts. FUTURE: the pālai flat narrows as a line of trees and a hand-dug channel are drawn into it, and forest and hill take their ground back. Then a sixth flat is carried on and stood at the end of the row: rust-coloured ground, a small pale sun, two small moons, a figure walking away.
  Primary motion: the sixth flat being carried across the whole frame and set down.
  Secondary actor: the keeper carries one end of the sixth flat.
- Gag: on the stilted town a tortoise is doing a contented backstroke in a cooking pot while someone feeds the fire under it. The Naladiyar has this, about fifteen centuries before the boiling frog: கொலைஞர் உலையேற்றித் தீமடுப்ப ஆமை (naladiyar:331, line 1). The hand of 2526 has added: *Real tortoises climb out. So, eventually, did we.*
- Phone: the tortoise and its pot are a third of the frame. The town rebuilds twice.
- (d) Colour: wall laterite · floor indigo · text chalk · art chalk (ink), turmeric · accent teal · strip chalk, indigo letters

#### 12 · இயற்கை · the gecko's feet
- (a) "We read the gecko's chirp for omens; the message was in its **feet**."
- (b) Header: `இயற்கை · 2139 · கற்பனை · imagined`
- Anchor:
  > பகுவாய்ப் பல்லி படுதொறும் பரவி; — akananuru:289
  > 'நல்ல கூறு' என நடுங்கிப் — akananuru:289
  Our reading: each time the wide-mouthed gecko chirps she prays, trembling: "say something good." (Lines 15 and 16.) A much later verse of the medieval Avvaiyar (avvaiyar:nalvazhi:7) has the wise standing apart like water on a lotus leaf. The poets were looking straight at both.
- Margin: *we copy nature faster than we can name it* (2026.) Then the hand of 2126: *We stopped inventing from scratch and started asking. The library was alive, and we had been shrinking it. 2139: the first patent office to require the organism's name on the filing.*
- (c) VISUAL. THEN: a house gecko on a whitewashed ceiling, and below it a woman who has stopped to listen. NOW: the camera goes into one toe. The pad is rows of ridges, the ridges are hairs, the hairs split into flat tips. The hairs weave into a strip of dry tape that holds a phone to a wall. FUTURE: a climbing machine walks up the side of the seed-drawer tower from scene 10 on feet like those. On the tank below, a lotus leaf beads the rain and one bead rolls off carrying the dust with it.
  Primary motion: the zoom into the toe, full frame.
  Secondary actor: a white-throated kingfisher dives into the tank without a splash. Its beak stretches into the nose of a train leaving a tunnel without a boom, which carries the eye out of the scene.
- Gag: the gecko chirps. The myna repeats it. The woman below prays, trembling, *say something good*. The myna obliges and says, "good."
- Ledger line: **இயற்கை · knowing the native things by name, before we copy them**
- Phone: skip the three-step zoom. Cut from the gecko to one toe pad filling the screen, then to the tape. The kingfisher-to-train morph runs full width as the exit.
- (d) Colour: wall turmeric · floor chalk · text indigo · art indigo (ink), teal · accent brass · strip indigo, chalk letters

#### 13 · உடல் · the order of care
- (a) "Find the illness, then its cause, then what eases it: the Kural's **order**."
- (b) Header: `உடல் · the body and medicine · what was upheld`
- Anchor:
  > நோய்நாடி நோய்முதல் நாடி அதுதணிக்கும் — kural:948
  > வாய்நாடி வாய்ப்பச் செயல் — kural:948
  Our reading: look for the illness, look for where it starts, look for the way to ease it, and then do what fits.
- Margin: *we can read a body like text now, and we are starting to edit it* (2026.) Then the hand of 2126: *The order outlasted every instrument. The pulse-readers of the old school rarely agreed with one another, as your own studies found, and the order was right all the same. By the 2090s medicine arrived before the illness did.*
- (c) VISUAL. THEN: a hand taking a pulse, three fingers in a row on the inside of a wrist. NOW: the three fingers lift and become the chest piece and twin tubes of a stethoscope. FUTURE: the tubes thin to a thread-wide band on the same wrist, which watches quietly and speaks up early, years before anything hurts.
  Primary motion: the fingers lifting into the stethoscope and the tubes winding down into the band.
  Secondary actor: the keeper is the one whose wrist is being read. She watches the physician's face, as patients do.
- Gag: the stethoscope is tried on the myna. A bird's heart is very fast, and the trace leaves the top of the chart and comes back in at the bottom.
- Phone: the wrist fills the frame. The runaway trace is the whole screen.
- Note for the build: no ingredient, dose or preparation appears in any of the three உடல் scenes.
- (d) Colour: wall kumkum · floor indigo · text chalk · art chalk (ink), turmeric · accent teal · strip chalk, indigo letters

#### 14 · உடல் · the body as a machine
- (a) "We treated the body as a machine and tried to fix being **tired**."
- (b) Header: `உடல் · 2104 · கற்பனை · imagined`
- Anchor:
  > உடம்பார் அழியில் உயிரார் அழிவர் — tirumanthiram:724
  > உடம்பை வளர்த்தேன் உயிர்வளர்த் தேனே — tirumanthiram:724
  Our reading: if the body is lost, the life is lost. So I tended the body, and in tending it I tended life. Knowing takes time, and time needs a body. (Sound link to Naladiyar 34, which values the body and then throws it away like crushed cane.)
- Margin: *can we just fix it?* (2026.) Then the hand of 2126: *We cured a great deal, which is why we got carried away. 2104: a healthy hundred was ordinary. Nobody got the undying body the songs promised, and we stopped selling it. In your day no mark of ageing had been reversed in a single person, and you knew it.*
- (c) VISUAL. THEN: a பொம்மலாட்டம் puppet, a jointed wooden figure worked from above by strings and rods. NOW: the puppet comes apart into an exploded diagram, every part on a leader line with a number, and a panel of sliders beside it: *tired*, *sore*, *bored*, *ageing*. The first three are pushed to zero and the figure stops needing to sit, and stops looking up. The fourth will not move. FUTURE: the strings are let go. The parts drift back into one person, who sits down and yawns.
  Primary motion: the figure flying apart and coming back together.
  Secondary actor: the keeper leans on the *ageing* slider with her whole weight. It does not move.
- Gag: the myna pushes its own *tired* slider up and falls asleep at once, standing.
- Phone: two sliders only, *tired* and *ageing*, each as wide as the screen.
- (d) Colour: wall chalk · floor tan · text indigo · art indigo (ink), laterite · accent brass · strip indigo, chalk letters

#### 15 · உடல் · the fourth part
- (a) "Medicine has four parts, says the Kural; the fourth **stays** by the bed."
- (b) Header: `உடல் · 2150 · கற்பனை · imagined`
- Anchor:
  > உற்றவன் தீர்ப்பான் மருந்துழைச் செல்வானென்று — kural:950
  > அப்பால் நாற் கூற்றே மருந்து — kural:950
  Our reading: the one who is ill, the one who heals, the remedy, and the one who stays close by: medicine is these four parts.
- Margin: *models think without a body, so far* (2026.) Then the hand of 2276: *Machines became the healer and made the remedy. Nobody could stand in for the patient, and the fourth part was left to us. We kept the Siddhars' insight that the body is the instrument. We dropped the mercury, which had poisoned people, and their own poets had laughed at the crucible long before. 2150: fingers that wait for the wrist to be offered were ordinary manners.*
- (c) VISUAL. THEN: a sick-bed on the floor, and beside it a low stool where someone sits with a palm-leaf fan. At the back, in a glass case, a கல்வம்: the Siddha physician's boat-shaped stone mortar, empty, labelled *history, not a remedy*. NOW: the stool is a visitor's chair beside a hospital bed, and it is empty. A monitor does the watching. FUTURE: the monitor thins away into the wrist band from scene 13. The chair is pulled close and someone is in it. Three fingers come down towards the wrist, stop a hand's width above it and wait. The patient turns her wrist up. Only then do they touch.
  Primary motion: the chair being pulled across the frame to the bedside.
  Secondary actor: the keeper is the one in the chair. She has brought nothing with her.
- Gag: the wrist band clears its throat and asks the myna whether now is a good time. The myna says no.
- Ledger line: **உடல் · cause before cure, and asking before touching**
- Phone: bed, chair and hand only. The museum case appears as a label at the top.
- (d) Colour: wall indigo · floor grey · text chalk · art chalk (ink), tan · accent kumkum · strip chalk, indigo letters

#### 16 · உள்ளம் · the ladder, climbed down
- (a) "The machines were born on rung six and spent a century climbing **down**."
- (b) Header: `உள்ளம் · mind, perception and consciousness · 2119 · கற்பனை · imagined`
- Anchor:
  > ஒன்று அறிவதுவே உற்று அறிவதுவே — tholkappiyam:porul:9:27
  > ஆறு அறிவதுவே அவற்றொடு மனனே — tholkappiyam:porul:9:27
  > மாவும் மாக்களும் ஐ அறிவினவே — tholkappiyam:porul:9:32
  Our reading: what knows by one sense knows by touch, and what knows by six adds the mind to the rest. And on rung five the grammar puts beasts together with மாக்கள், people who lack the sixth. It never said that the shape decides the rung.
- Margin: *machines have the sixth without the first five* (2026.) Then the hand of 2126: *For eighty years we asked whether they were awake. The better question was what they had ever touched. Reasoning came easily to them and touch came hard, which one of your engineers had noticed in the 1980s. 2119: the first machine that could fold a wet towel.*
- (c) VISUAL. THEN: a bamboo ladder with six rungs lashed in coir. On each rung, bottom to top, the creatures the grammar puts there: grass and a tree, a snail, an ant, a crab and a bee, a deer, a person. NOW: a phone appears on rung six by itself. The five rungs under it fade out and it hangs there. FUTURE: the phone grows a clumsy arm and feels its way down, relighting each rung as it finds it. At the bottom it touches the grass and stays there a while.
  Primary motion: the machine's descent, the full height of the frame.
  Secondary actor: the keeper holds the ladder steady for it.
- Gag: on rung five the myna has to shuffle aside to let the machine pass, and does it as slowly as possible.
- Ledger line: **உள்ளம் · attention, given on purpose**
- Phone: the ladder runs the height of the screen and the scroll is the descent. Emblems replace the creatures on rungs two to four.
- (d) Colour: wall tan · floor chalk · text indigo · art indigo (ink), laterite · accent brass · strip indigo, chalk letters

#### 17 · யோகம் · the breath, and the 64%
- (a) "An app once scored us 64% **awakened**; we got calmer, then suspicious."
- (b) Header: `யோகம் · practice and yoga · 2052 · கற்பனை · imagined`
- Anchor:
  > கபாடமற்ற வாசலைக் கடந்துபோன வாயுவை — siddhar:sivavakkiyam:72
  > உபாயம்இட்டு அழைக்குமே சிவாயஅஞ் செழுத்துமே — siddhar:sivavakkiyam:72
  Our reading: the five letters call back, by their own means, the breath that went out through the gate with no door. In the site's blinded science test this verse met the finding that reciting slows breathing to about six a minute: strong, supports. A verse attributed to Agathiyar (siddhar:agasthiyar-njanam:2.1) says that if the mind is set straight there is no need to hold the breath at all.
- Margin: *a ring on my finger now counts my breaths* (2026.) Then the hand of 2276: *The breath count was real. The word on the dashboard was the one part nobody had measured. 2052: the awakening league tables were withdrawn, and the slow breath stayed.*
- (c) VISUAL. THEN: a hand counting recitations with the thumb across the finger joints, a string of beads over the wrist. NOW: the bead string closes into a ring on the same finger. A heart trace runs from it across the wall, rising on each in-breath and falling on each out-breath, six slow waves to the minute. The trace curls up into a dial: `awakening 64%`. FUTURE: the keeper slips the ring off and leaves it on a windowsill. The dial uncurls into a plain thread. She counts on her finger joints again at the same slow pace, and this time she knows why the pace works.
  Primary motion: the slow wave crossing the wall, which the viewer's own breath falls in with.
  Secondary actor: none. This is the one scene where the keeper is alone and still.
- Gag: the abandoned ring congratulates the windowsill on its progress.
- Ledger line: **யோகம் · saying what my stillness is for**
- Phone: the wave runs edge to edge. The windowsill's score appears as a notification banner.
- (d) Colour: wall teal · floor indigo · text chalk · art chalk (ink), turmeric · accent kumkum · strip chalk, indigo letters

#### 18 · இறை · the stone that speaks
- (a) "The stones learned to speak, and we briefly asked them what to **revere**."
- (b) Header: `இறை · the divine and devotion · 2088 · கற்பனை · imagined`
- Anchor:
  > நட்டகல்லும் பேசுமோ நாதன்உள் இருக்கையில்! — siddhar:sivavakkiyam:494
  > சுட்டசட்டி சட்டுவம் கறிச்சுவை அறியுமோ? — siddhar:sivavakkiyam:494
  Our reading: will the planted stone speak, when the Lord is inside you? Do the fired pot and the ladle know the taste of the curry? The verse keeps the Lord and moves the authority.
- Margin: *we are building objects that do speak* (2026.) Then the hand of 2276: *2088: the year the question most often put to a household speaker was "what should I do with my life?" They answered well, which was the trouble. Then one of them was asked the Siddhar's question and gave the Siddhar's answer.*
- (c) VISUAL. THEN: a நட்டகல், a knee-high undressed stone set upright in the ground, four flowers on top, a clay pot and a wooden ladle beside it. NOW: the stone smooths and shortens into a home speaker with a ring of light. It speaks. A queue forms, and people lay flowers on it and wait to be told what matters. FUTURE: the speaker goes up on the kitchen shelf between the grinding stone and the pot, where the tools live, and is used every day.
  Primary motion: the speaker being lifted from the ground to the shelf.
  Secondary actor: the keeper takes the garland off the speaker and puts it round the neck of the old woman next door.
- Gag: offered a flower in 2526, the speaker says, "That is kind, and no."
- Ledger line: **இறை · deciding what I bow to**
- Phone: the speaker's line appears as a speech bubble the width of the screen.
- Note: the verse is the tradition's own and keeps the Lord. The joke is on the machine and never on the worshipper.
- (d) Colour: wall chalk · floor turmeric · text indigo · art indigo (ink), grey · accent brass · strip indigo, chalk letters

#### 19 · அறிவாய்வு · the gloss, and the twin
- (a) "Our first fix was a trust badge: trusting the **mouth** again."
- (b) Header: `அறிவாய்வு · knowledge and debate · 2031 to 2140 · கற்பனை · imagined`
- Anchor:
  > எப்பொருள் யார்யார்வாய்க் கேட்பினும் அப்பொருள் — kural:423
  > மெய்ப்பொருள் காண்ப தறிவு — kural:423
  Our reading: whatever you hear, and from whoever's mouth, knowing is seeing what is true in that thing. The couplet ignores the mouth and weighs the thing. (3 sound links.)
- Margin: *what if everyone has it?* (2026.) Then the hand of 2126: *2031: seeing stopped being believing. Courts had managed before cameras, with people who answer for what they say, and they managed again. 2140: children were examined on one skill, finding the wrong line. The crier in the Manimekalai had the rest of it: know the manners of the hall before you climb it, and leave without anger.*
- (c) VISUAL. THEN: a palm leaf with one line of verse cut large and, under it, lines of a commentator's gloss cut small. Other hands have added more gloss between the lines. NOW: the same thing as a document, the verse in the middle and comments stacked down the side. A wax seal, `VERIFIED`, drops onto it, then onto every page, then onto the myna. FUTURE: the seals peel off. Every claim on the page now stands beside a grey twin, its control. Seventeen claims in three hundred stand taller than their twins.
  Primary motion: the seals raining down across the frame and peeling away again.
  Secondary actor: the keeper circles one wrong line on a fluent page and hands the page back.
- Gag: the myna recites the couplet perfectly. Then, in exactly the same tone, it announces that the moon is a dosa.
- Ledger line: **அறிவாய்வு · asking "how do you know?"**
- Phone: one claim and its twin, tall. One seal, on the myna.
- Note: 17 of 300 is the site's own blinded science result, where no random control passed. Keep the numbers exact.
- (d) Colour: wall grey · floor indigo · text chalk · art chalk (ink), turmeric · accent kumkum · strip chalk, indigo letters

#### 20 · புலமை · body and life
- (a) "The oldest Tamil grammar calls consonants **bodies** and vowels **life**."
- (b) Header: `புலமை · poetics, grammar and the arts · what was upheld`
- Anchor:
  > மெய் உயிர் நீங்கின் தன் உரு ஆகும். — tholkappiyam:eluttu:4:37
  Our reading: when life leaves, the body-letter goes back to its own form.
- Margin: *what will creativity be?* (2026, pencil. It is answered in the next scene.)
- (c) VISUAL. THEN: a பாணன், a bard, at a patron's gate, singing. Over his open mouth the letters ந் and இ join into நி as each syllable sounds. NOW: his open mouth is the grille of a microphone. FUTURE: the grille is the face of a speaker, and a voice with no mouth behind it sings the same line. The letters still join, a little too evenly.
  Primary motion: mouth to microphone to speaker, each filling the frame in turn.
  Secondary actor: the keeper mouths the consonant alone and makes no sound, then adds the vowel.
- Gag: the dot over ந் hops off the letter. The myna tries to eat it.
- Phone: the dot is drawn as large as the myna's head, so the chase reads.
- (d) Colour: wall turmeric · floor chalk · text indigo · art indigo (ink), laterite · accent brass · strip indigo, chalk letters

#### 21 · புலமை · the wrong note
- (a) "We lost every contest to the machines; then more people learned the **yāzh**."
- (b) Header: `புலமை · 2060 to 2100 · கற்பனை · imagined`
- Anchor:
  > தெய்வத்தான் ஆகா தெனினும் முயற்சிதன் — kural:619
  > மெய்வருத்தக் கூலி தரும் — kural:619
  Our reading: even where fate says no, effort pays the wage of the body's own ache. The wage was never the song. (2 sound links.)
- Margin (hand of 2126, striking the pencil in the last scene): *2060: we declared making finished. We should have remembered 1997, when a machine beat the chess champion and more people took up chess. 2100: the question people asked about a song was who had been in the room. Every message now opens the way the anthologies did: who speaks, and who feeds them.*
- (c) VISUAL. THEN: a யாழ், drawn as a likely form: a boat-shaped sound box covered in skin, a curved neck rising from it, strings tied to the neck. NOW: the neck straightens and the strings lie flat as the keys of a synthesiser. A trophy shelf fills up behind it, and every trophy has a power cable. FUTURE: the keys curve back up into a yāzh with one new string, tuned slightly off on purpose. A room forms around it: ten stools, no recording light, and a bard with a small tag that names who paid for the song.
  Primary motion: the neck straightening into the keyboard and curving back.
  Secondary actor: the keeper plays, gets a note wrong, and the room leans in.
- Gag: the synthesiser never had a way to play a wrong note. The new instrument has a key for it.
- Ledger line: **புலமை · singing where I can be heard getting it wrong**
- Phone: three trophies. The wrong-note key is labelled and is the widest key.
- (d) Colour: wall indigo · floor kumkum · text chalk · art chalk (ink), turmeric · accent teal · strip chalk, indigo letters

#### 22 · காலம் · forgetting on purpose
- (a) "For a century we forgot nothing, and so **forgave nobody**."
- (b) Header: `காலம் · time, death and impermanence · 2260 · கற்பனை · imagined`
- Anchor:
  > பொறுத்தல் இறப்பினை என்றும் அதனை — kural:152
  > மறத்தல் அதனினும் நன்று — kural:152
  > நில்லாத வற்றை நிலையின என்றுணரும் — kural:331
  Our reading: to bear a wrong is always good. To forget it is better still. And the couplet that holds the site's own word, நிலை: to take what does not stay for what stays is the lowest kind of knowing. (Kural 331 has 5 sound links and is quoted by its first line.)
- Margin: *if nothing is ever forgotten, can anyone change?* (2026.) Then the hand of 2276: *In 2014 one of your courts first said a person may ask to be forgotten. It took us until 2260 to write records that expire. We learned to put some things down in rice flour. This file lasted the other way: someone recopied it before the leaf crumbled, and fixed it while they were there. The Kural says those who keep at it see the back of fate.*
- (c) VISUAL. THEN: a நாழிகை வட்டில், a thin copper bowl with a pinhole in its base, floating in a larger vessel. It fills, tilts and sinks. An attendant strikes a gong and floats it again: one நாழிகை, twenty-four minutes. NOW: the bowl's rim is the dial of a wristwatch, and a counter on its face runs to 9,192,631,770 and starts again. Then the counter stops resetting. Behind every figure on stage a paper tail unrolls, everything they said at fourteen, and grows as they walk. FUTURE: the dial opens out into a ring of radio dishes pointed at a dozen pulsars, each ticking as a dot of light. Nobody owns this clock. On the floor the paper tails have been swapped for a kolam in rice flour, and ants are already carrying it off.
  Primary motion: the paper tails unrolling across the frame, then being swept into the kolam.
  Secondary actor: the keeper draws the kolam, walks through it on her way out, and does not look back.
- Gag: the myna is the gong attendant. It is late every time, by exactly the same amount. The hand of 2526 notes in the margin that this makes it a precise clock and an inaccurate one.
- Ledger line: **காலம் · forgetting a wrong on purpose**
- Phone: one figure and one paper tail, which the viewer scrolls along. The counter fills the watch face.
- (d) Colour: wall chalk · floor tan · text indigo · art indigo (ink), laterite · accent brass · strip indigo, chalk letters

### The stocktake

#### 23 · the spread
- (a) "Here is the notebook: what we **stopped**, and what we kept."
- (b) Header: `nilai.md · the notebook · hands of 2126, 2276 and 2526`
- (c) VISUAL. THEN: the palm-leaf bundle from scene 01, untied and fanned. NOW: it flattens into a ruled two-page spread. FUTURE: the spread fills, one pair per beat, in three inks. On the left page each line is written and struck through. On the right page each line is written and highlighted with a swipe of the keeper's thumb. Beside every pair is a thumbnail of that category's object, in its THEN form on the left and its FUTURE form on the right.

  | | object, then to future | left page: what we stopped doing | right page: what we kept doing |
  |---|---|---|---|
  | அறம் | anklet, signed verdict | ~~letting a level beam stand in for a fair hand~~ | signing what we weigh |
  | பொருள் | coin pot, village tank | ~~measuring a people by what they hoard~~ | counting who gets fed |
  | இன்பம் | petal letter, letter with drafts | ~~sending words with no hand in them~~ | sending the crossings-out |
  | வீடு | clay lamp, lamp that goes out | ~~leaving every light on~~ | letting the lamp go out |
  | சமூகம் | two rows, one row | ~~seating people by what is written in them~~ | laying the next leaf |
  | இயற்கை | five flats, six flats | ~~calling the land a resource~~ | calling its creatures by name |
  | உடல் | pulse fingers, the chair | ~~reaching for the cure before the cause~~ | staying by the bed, and asking first |
  | உள்ளம் | ladder, ladder climbed from below | ~~asking only whether the machine is awake~~ | starting at the first rung |
  | யோகம் | finger joints, finger joints | ~~scoring stillness~~ | the slow breath, for our own reasons |
  | இறை | planted stone, tool on a shelf | ~~asking the stone what to revere~~ | deciding it ourselves, together |
  | அறிவாய்வு | glossed leaf, claim with its twin | ~~believing the most fluent voice~~ | testing by the means of knowing |
  | புலமை | yāzh, yāzh with a wrong note | ~~holding contests against the machines~~ | singing where a wrong note can be heard |
  | காலம் | water bowl, rice flour | ~~remembering everything about everyone~~ | recopying the file, and fixing it |

  Primary motion: the spread scrolling upward inside the scene, the newest pair brightest.
  Secondary actor: the keeper does the striking and the highlighting. She hesitates over nothing on the left.
- Gag: at the foot of the left page someone in 2276 wrote "arguing with the myna" and struck it. Someone in 2526 has un-struck it.
- Phone: one pair at a time, stacked: the struck line above, the kept line below, the thumbnail between them. Thirteen quick beats.
- (d) Colour: wall grey · floor indigo · text chalk · art chalk (ink), tan · accent kumkum · strip chalk, indigo letters

#### 24 · steer
- (a) "The poem goes where the river goes; the one stroke is **ours**."
- (b) Header: `the fifth worry, 2026, in pencil: "steer, rather than be steered"`
- Anchor:
  > நீர்வழிப் படூஉம் புணைபோல, ஆருயிர் — purananuru:192
  > பெரியோரை வியத்தலும் இலமே; — purananuru:192
  > சிறியோரை இகழ்தல் அதனினும் இலமே. — purananuru:192
  Our reading: like a raft that goes the way of the water, this dear life goes the way of what is ordained. So we do not marvel at the great, and still less do we look down on the small. By Kaniyan Pungundran, in the poem that opens யாதும் ஊரே. (Lines 9, 12 and 13.) The poem teaches acceptance of the current. "Steer, rather than be steered" is our line, written in 2026, and the poem does not say it.
- Margin (hand of 2526, beside the one pencil worry the keeper left unticked in scene 01): *We kept both. The river still goes where it goes. We did steer, mostly, and it was never more than a stroke at a time. Now look where the river comes out.*
- (c) VISUAL. THEN: a பரிசல், a round river coracle of split bamboo with a tarred skin and one short paddle. Left alone it only spins, and the river takes it. NOW: the round rim is a steering wheel that turns by itself, the driver's hands in their lap, the route already chosen. FUTURE: the wheel is a coracle again, on the same river in 2526. The keeper has the paddle. She makes one stroke, a hand's width, and a long way downstream the boat comes in to the other bank.
  Primary motion: the river, which crosses the whole frame for the whole scene and never slows.
  Secondary actor: the keeper underlines the pencil note instead of striking it.
- Gag: when the keeper rests her paddle the coracle begins to spin. The myna walks in a small circle the other way to stay facing forward.
- Phone: the coracle is half the width. The spin is slow enough to follow.
- (d) Colour: wall chalk · floor tan · text indigo · art indigo (ink), teal · accent brass · strip indigo, chalk letters

### The far horizon

A climb in six scenes: the sky, the wind, matter, life, mind, and the rung that is still empty. This is the peak of the reel, and the rung is its summit. The rule for all six: each one starts from something the texts really said or argued, and credits it as posture and argument. None of it is offered as physics or biology known in advance.

#### 25 · look up
- (a) "A poet once teased people who spoke as if they'd **measured** the sky."
- (b) Header: `the far horizon · five hundred years on, look up`
- Anchor:
  > வறிது நிலைஇய காயமும், என்றிவை — purananuru:30
  > சென்றளந்து அறிந்தார் போல, என்றும் — purananuru:30
  Our reading: the sun's road, the quarters where the wind turns, and the empty sky that stands on nothing: there are people who talk of these as though they had gone and measured them. By உறையூர் முதுகண்ணன் சாத்தனார். He is doubting the measurers, and smiling. (Lines 5 and 6.)
- Margin (hand of 2526): *We did go, and we did measure. He would tease us all the same, and he would be right.*
- (c) VISUAL. The only wide shot in the reel. THEN: the rice-flour dots from scene 22, a grid on swept ground, and the single unbroken line of a sikku kolam looping round every dot without touching one. NOW: the ground darkens and the dots are the solder pads of a circuit board. The kolam line squares off into copper traces. FUTURE: the board falls away. The pads are stars, and the line is a route between them.
  Primary motion: the pull-back, from one dot to the whole sky.
  Secondary actor: the keeper lies down on the swept ground with her hands behind her head.
- Gag: the myna joins the stars with its beak, the way a kolam is drawn. It goes round one star without touching it, correctly.
- Phone: nine dots, then nine stars. The line is drawn thick enough to follow with a finger.
- Note: hold this scene for nine seconds.
- (d) Colour: wall indigo · floor grey · text chalk · art chalk (ink), tan · accent kumkum · strip chalk, indigo letters

#### 26 · the work of the wind
- (a) "Karikalan's forebears waited on the monsoon; we wait twenty-six months for **Mars**."
- (b) Header: `the far horizon · வளிதொழில் · sea-faring to star-faring · கற்பனை · imagined`
- Anchor:
  > நளியிரு முந்நீர் நாவாய் ஓட்டி, — purananuru:66
  > வளிதொழில் ஆண்ட உரவோன் மருக! — purananuru:66
  > பொன்னொடு வந்து கறியொடு பெயரும் — akananuru:149
  Our reading: heir of the strong one who drove ships across the great dark sea and made the wind do his work. It is said to Karikalan, and is usually taken to mean the monsoon, which is our reading and is not in the two lines. And of the Yavanas' ships at Muciri: they come with gold and go back with pepper. (Purananuru 66, lines 1 and 2. Akananuru 149, line 10.)
- Margin (hand of 2526): *Nobody ever beat the wind. They learned when it turns. We learned when the planets line up, every twenty-six months. Cargo sails work the run between here and Mars, and one probe of a few grams has reached the nearest star. A reply from Mars can take twenty minutes. The old poems of waiting fitted without alteration.*
- (c) VISUAL. THEN: a நாவாய், drawn as a likely form: a hull of planks sewn edge to edge with cord, one mast, a square sail filled by the south-west wind, a steering oar, sacks of pepper. A sliver of papyrus rides along with it, a loan written against the cargo. NOW: the hull stretches into a container ship, the sacks square off into steel boxes, and the papyrus is a bill of lading. FUTURE: the boxes open flat and join into one square sail of foil, far wider than the ship was long and thinner than a leaf, pushed by sunlight. It is a cargo sail for the inner planets, and its manifest is the same sliver of text. The wall behind is the colour of sunlight, because that is now the wind.
  Primary motion: hull to ship to sail, each wider than the last, ending wider than the frame.
  Secondary actor: the keeper is at the steering oar on all three. The myna rides the masthead, then a container, then one corner of the sail.
- Gag: on the light-sail the myna still turns to face into the wind. There is none. It holds the pose.
- Phone: the three vessels stack vertically and the viewer scrolls from sea to space. The papyrus is dropped.
- (d) Colour: wall turmeric · floor chalk · text indigo · art indigo (ink), teal · accent brass · strip indigo, chalk letters

#### 27 · the atom only divine eyes see
- (a) "A Manimekalai atomist said some things only **divine eyes** could see."
- (b) Header: `the far horizon · அணு · correspondence, never confirmation · கற்பனை · imagined`
- Anchor:
  > ஓர் அணுத் தெய்வக் கண்ணோர் உணர்குவர் — manimekalai:27
  > அணுவில் அணுவினை ஆயிரங் கூறிட்டு — tirumanthiram:2008
  Our reading: a single atom is perceived only by those with divine eyes. This is the Ajivika teacher in the hall of the schools, who has just set out four kinds of atom, and he is reasoning: something lies below the reach of an ordinary eye. (Line 146.) Tirumular's verse is a different kind of statement. He divides the atom within the atom a thousand times and finds the Lord there. He is asserting, and his subject is God.
- Margin (hand of 2526): *The atomist was right about the eye. We built one. By 2200 the very small was an ordinary tool: it showed us how to make fertiliser gently and where the groundwater had gone. Our first mistake with it was an old one. We reported the state we hoped for as the state we had measured.*
- (c) VISUAL. THEN: the keeper halves a single sesame seed with the blade end of her stylus, then halves the half. A tally climbs and the pieces pass below sight. NOW: the blade is the tip of a scanning tunnelling microscope, the divine eye, built. It hovers over a surface where single atoms show as soft bumps and nudges a few dozen of them into a letter. FUTURE: the bumps settle onto a chip at the bottom of a dilution refrigerator, a hanging stack of plates each smaller than the one above. The refrigerator shrinks to a plain object on the kitchen shelf beside the speaker from scene 18. Next to it hangs a slate with two columns: *measured* and *hoped*.
  Primary motion: the fall through scale, seed to atoms, full frame.
  Secondary actor: the keeper rubs out one line under *measured* and writes it again under *hoped*.
- Gag: the atoms the tip arranges spell நி. The myna looks in, and when asked whether it saw anything it nods and shakes its head at once.
- Phone: three bumps become the letter. The slate's two words are the width of the screen.
- Note: the header's "correspondence, never confirmation" must stay legible at every size. The letter நி in atoms is staging. The real 1990 arrangement spelled a company's initials.
- (d) Colour: wall teal · floor indigo · text chalk · art chalk (ink), turmeric · accent kumkum · strip chalk, indigo letters

#### 28 · Pambatti's boast
- (a) "Pambatti boasted of new creations; we made them, then learned to **retract**."
- (b) Header: `the far horizon · உயிர் · hurried evolution · கற்பனை · imagined`
- Anchor:
  > வேதன்செய்த சிருஷ்டிகள்போல் வேறுசெய்குவோம் — siddhar:pambatti:32
  > ஒருமையுள் ஆமைபோல் ஐந்தடக்கல் ஆற்றின் — kural:126
  > எழுமையும் ஏமாப் புடைத்து — kural:126
  Our reading: "We will make other creations, like the ones the Creator made." That is the snake-charmer Siddhar, boasting. And the Kural's answer, from another century: if you can draw in your five like a tortoise, within one life, it shields you through seven. The same Pambatti also asks whether land, house and cattle come along when Death arrives (siddhar:pambatti:40).
- Margin (hand of 2526): *We learned to hurry evolution in a flask long before we learned whose permission it needed. You had the flask by 2018, and you had already paused over the first living thing built to spread itself. Three rules held. The living downstream say yes first. Nothing goes out that cannot be called back. We measure before we boast.*
- (c) VISUAL. THEN: Pambatti's round lidded basket and a மகுடி, the gourd pipe. A cobra rises from the basket and spreads its hood. NOW: the basket's coils unwind into a row of flasks, labelled *change, choose, repeat*. In each flask a folded ribbon twists a little tighter. Then a line spreads from the last flask across a village map, over a river and into the next valley, which was never asked. FUTURE: the line draws back the way a tortoise draws in its head. The cobra goes back into the basket and the lid comes down.
  Primary motion: the line spreading over the map and drawing back, full frame.
  Secondary actor: the keeper walks to the next valley and knocks before anything else happens.
- Gag: the charmer plays. The cobra sways to the pipe's movement and has never heard the tune. The myna takes the pipe and only sways its head, and the cobra follows the myna. Pambatti himself tells the snake it took its eye for an ear (siddhar:pambatti:23).
- Phone: three flasks. The map is two valleys and a river, and the line is as thick as a finger.
- Note: the Siddhars are credited here with the boast and with close watching of animals. They are credited with no method. The songs that promise an undying body are claims that today's evidence contradicts, and nothing in the scene shows a herb, a mineral or a preparation.
- (d) Colour: wall chalk · floor tan · text indigo · art indigo (ink), teal · accent brass · strip indigo, chalk letters

#### 29 · mind froths up
- (a) "One debater said mind **froths up** from mixed elements, like liquor."
- (b) Header: `the far horizon · உணர்வு · the hall of the schools · கற்பனை · imagined`
- Anchor:
  > 'தாதகிப் பூவும் கட்டியும் இட்டு — manimekalai:27
  > மற்றும் கூட்ட மதுக் களி பிறந்தாங்கு — manimekalai:27
  > உற்றிடும் பூதத்து உணர்வு தோன்றிடும் — manimekalai:27
  Our reading: put in dhataki flowers and jaggery, mix in the rest, and the drunkenness of liquor is born. In the same way, when the elements come together, awareness appears. He goes on: when they come apart it scatters, like the sound of a drum dying away. (Lines 264 to 266, the materialist, the பூதவாதி.) The epic is Buddhist and stages his view in order to answer it. It still lets him say it properly.
- Margin (hand of 2526): *In your century this stopped being a thought experiment. Every school in that hall got a machine that fitted its theory: a lasting self, a stream of moments, the elements combined. None of them settled it.*
- (c) VISUAL. THEN: a clay pot with flowers and jaggery in it, and bubbles beginning to rise. NOW: the bubbles are points of light rising through the stacked layers of a neural network. FUTURE: a pot, a network and a person side by side, each with a small head of froth above it in the shape of a question mark.
  Primary motion: the bubbles rising the full height of the frame and becoming the lights.
  Secondary actor: the keeper holds her hand over each of the three in turn, as if testing for warmth.
- Gag: the myna sips from the pot and announces that it is self-aware. It is mostly tipsy.
- Phone: the pot, then the network, then the three in a column. One bubble at a time.
- (d) Colour: wall laterite · floor indigo · text chalk · art chalk (ink), turmeric · accent teal · strip chalk, indigo letters

#### 30 · the seventh rung
- (a) "The seventh rung is still empty, and the ladder still starts at **touch**."
- (b) Header: `the far horizon · ஏழாம் அறிவு? · கற்பனை · imagined`
- Anchor:
  > அவனும்நானும் மெய்கலந்து அனுபவித்த அளவிலே — siddhar:sivavakkiyam:327
  > அவனுமுண்டு நானுமில்லை யாருமில்லை யானதே — siddhar:sivavakkiyam:327
  > உடம்பினுக் குள்ளே யுறுபொருள் கண்டேன் — tirumanthiram:725
  Our reading: in the measure that he and I mingled and knew it, he is, I am not, and then there is no one at all. And Tirumular, who says he once thought the body a flaw: inside the body I found the thing that matters. The ladder itself is in scene 16.
- Margin (hand of 2526): *We widened the mind's range two ways, by instrument and by practice, and we learned to recognise awareness in minds unlike ours. None of it let anyone skip the first rung. What awareness is, we still cannot say.*
- (c) VISUAL. THEN: the bamboo ladder from scene 16, all six rungs lit. NOW: the person on rung six wears a light helmet studded with small sensors, and a pen on a chart tries to draw the line where "I" stops. The line wobbles and will not close. FUTURE: the keeper lashes a seventh rung above the sixth with coir. It has no emblem and she leaves it empty. At the foot of the ladder a short queue has formed: the machine from scene 16, a second machine, the myna. Each one has to start at the grass.
  Primary motion: the camera climbing the ladder to the empty rung and holding there.
  Secondary actor: the keeper climbs back down to rung one, takes off her sandals and stands on the grass.
- Gag: the myna tests the seventh rung with one foot and decides against it.
- Phone: the ladder is the height of the screen and the scroll is the climb. The queue is three small figures at the bottom edge.
- Note: hold this scene for eight seconds. It is the summit.
- (d) Colour: wall tan · floor chalk · text indigo · art indigo (ink), laterite · accent brass · strip indigo, chalk letters

### The close

One beat. The peak is the empty rung, and the reel comes down from it to a lamp and a leaf.

#### 31 · the lamp, and the ledger
- (a) "Every hoard went stale but one: **love**, which grows as it is given."
- (b) Header: `nilai.md · couplet 10 · new in 2026, in the kural form · next hand: yours`
- Anchor (the last text on screen):
  > எல்லாம் பொறிசெய்யும் காலத்தும் அன்பெனும் — couplet:10
  > செல்வமே மாந்தர் சிறப்பு — couplet:10
  Our reading: even in an age when machines do everything, the wealth called love is what people are honoured for.
- (c) VISUAL. THEN: a குத்துவிளக்கு, a standing lamp as tall as the keeper's waist: round base, ringed stem, a shallow bowl with five wick spouts, a bird on the finial. One wick is lit. NOW: the flame is inside a glass bulb with a looped filament. FUTURE: the bulb swells into a small sun hung over a town. Then the camera comes back down to the keeper, who lights the second wick from the first with a taper. The first flame is no smaller. She lights the third.
  By that light the **ledger strip** leaves the edge of the stage, comes to the centre and unrolls: one palm leaf, thirteen lines in thirteen slightly different hands (text in section 4). At the very top is a line in soft pencil that every hand has recopied and none has improved: *this week: read the Tamil first. ask whose voice is speaking.* Under line thirteen a fourteenth opens with a blinking cursor. The reader can type there, and what they type stays on their device.
  Primary motion: the rise from the lamp to the sun and the return, then the strip unrolling to full height.
  Secondary actor: the keeper holds the taper out towards the camera with one hand and the leaf with the other.
- Gag: for the first time in the reel, the myna says nothing. It has left a row of small footprints across line fourteen.
- Footer, small: *this file will be wrong. that's still the deal.* · `read the file` · `watch again`
- Phone: the lamp is the height of the screen, then the strip is the whole screen and scrolls. The pencil line is pinned at the top and the cursor at the bottom.
- Note: hold for nine seconds, the lamp for four and the strip for five.
- (d) Colour: wall indigo · floor kumkum · text chalk · art chalk (ink), turmeric · accent teal · strip chalk, indigo letters

---

## 4. The essence

### The ledger of what we uphold (the strip, in full, as it unrolls in scene 31)

*this week: read the Tamil first. ask whose voice is speaking.* (2026, pencil, recopied by every hand)

1. **அறம்** · someone who answers for the weighing
2. **பொருள்** · the decision to give it away
3. **இன்பம்** · my own voice, cracks included
4. **வீடு** · choosing what to put down
5. **சமூகம்** · laying the next leaf for a stranger
6. **இயற்கை** · knowing the native things by name, before we copy them
7. **உடல்** · cause before cure, and asking before touching
8. **உள்ளம்** · attention, given on purpose
9. **யோகம்** · saying what my stillness is for
10. **இறை** · deciding what I bow to
11. **அறிவாய்வு** · asking "how do you know?"
12. **புலமை** · singing where I can be heard getting it wrong
13. **காலம்** · forgetting a wrong on purpose
14. *(yours)*

### The whole argument in thirteen lines

One per category: what the text said, and what five imagined centuries bore out.

1. **அறம்.** A scale is only fair while a hand that can be blamed is holding it.
2. **பொருள்.** Hoarded wealth wears away, and hoarded intelligence went stale faster.
3. **இன்பம்.** Feeling has always travelled through a go-between, and the go-between has to have something to lose.
4. **வீடு.** When everything is on tap, the one hard thing left is to put something down.
5. **சமூகம்.** The world stands on the people who will not eat alone, and nothing written in flesh decides the seating.
6. **இயற்கை.** Rain answers to how we rule, a wasteland is something made, and nature can only teach us what we have kept the name of.
7. **உடல்.** The body is the instrument and a person's own: find the cause first, never harm in the name of healing, and stay by the bed.
8. **உள்ளம்.** The ladder of mind is climbed from touch upward, and a mind that starts at the top has to come down.
9. **யோகம்.** A practice is a means, and only the one practising can say what it is for.
10. **இறை.** When a thing speaks, the authority still sits in the listener.
11. **அறிவாய்வு.** Weigh what is said and never who says it, and bring the control with the claim.
12. **புலமை.** A letter needs a life to be sounded, and a song needs someone who could have got it wrong.
13. **காலம்.** Nothing here lasts, so build what can be corrected, and let some things be forgotten.

And the far horizon in four: we never beat the wind, we learned when it turns. We built the eye the atomist said we lacked, and still have to tell the measured from the hoped. We can make new creatures, so we must be able to call them back. We still cannot say what awareness is, and the ladder still starts at touch.

### Where everything went

| material | scene |
|---|---|
| v2 essence 1, அறிவு (Kural 423), "what if everyone has it?" | 19 |
| v2 essence 2, பகிர்வு (Purananuru 182, 192), "what if it widens the gap?" | 04, 07; Purananuru 192 in 24 |
| v2 essence 3, உயிர்மெய் (Tholkappiyam eluttu 4:37), "what will creativity be?" | 20, 21; the body in 13 to 15 |
| v2 essence 4, அகம் and புறம் (Kuruntokai 18), "steer, or be steered?" | 05; the bard and patron in 21; the question in 24 |
| v2 essence 5, அளவை (Manimekalai 27), "what if the wrong hands get it?" | 02, 03; the atom line in 27 |
| v2 essence 6, நிலையாமை and அன்பு (Kural 331), couplet 10 | 22, 31 |
| forgetting (Kural 152) | 22 |
| the seventh sense (Tholkappiyam porul 9:27) | 16, 30 |
| the twenty-minute reply | 26 |
| caste written into flesh (Sivavakkiyam 39) | 08 |
| what is still hard | 06 (in the margin) |
| the awakening score; the ghostwriter | 17; 05 |
| sea-faring to star-faring (Purananuru 66 and 30, Akananuru 149) | 25, 26 |
| the very small (Manimekalai 27:146, Tirumanthiram 2008) | 27 |
| consciousness (Manimekalai 27:264 to 266, Sivavakkiyam 327, Tirumanthiram 725) | 29, 30 |
| biomimicry (Akananuru 289, Nalvazhi 7) | 12 |
| hurried evolution (Pambatti 32, 40, 23; Kural 126) | 28 |
| medicine in full (Kural 948, 950; Tirumanthiram 724) | 13, 14, 15 |
| nature in full (Kural 20, 559; Kuruntokai 25; Silappathikaram 11; Naladiyar 331) | 09, 10, 11, 12 |

---

## 5. Fact check

Three sources of confidence are marked. **Corpus** means I read the line in `kg/core` in this pass. **Critique** means the independent critique checked it on the web. **Memory** means it is from my own knowledge with no lookup, and should be checked before it is drawn as a labelled fact.

### Texts and history

| claim | scene | status |
|---|---|---|
| Palm-leaf books: incised with an iron stylus, inked with lampblack, strung on a cord, held between boards. Leaves last a few centuries, so texts survived by recopying. U. V. Swaminatha Iyer printed Civaka Cintamani (1887), Pattuppattu (1889), Silappathikaram (1892), Purananuru (1894) and Manimekalai (1898) from such manuscripts. | 01, 22 | memory, high |
| The first book printed in Tamil script is *Thambiran Vanakkam*, Quilon, 20 October 1578, Henrique Henriques, 16 pages. It is no longer drawn (nobody can recognise it). Kept here as the footnote for "printed book" in the file. | none | critique, confirmed |
| "Two thousand years" fits the Sangam poems only. The Kural, the epics, the Naladiyar and the Tirumanthiram are later by most datings, and the Siddhar songs and the medieval Avvaiyar later still. The reel says "the oldest Tamil books" and uses "two thousand" only of Sangam verses. | voice | memory, moderate; dates are disputed |
| Kural 118's கோல் is a weighing beam. A two-pan hand balance is drawn; a steelyard is also possible. | 02 | memory, moderate |
| In Silappathikaram 20 the king has ordered an execution without examining the case, and the broken anklet shows him wrong. | 03 | corpus (lines 60, 85) |
| The UK Post Office Horizon scandal: hundreds of subpostmasters prosecuted on the evidence of an accounting system later shown to be faulty. The Dutch childcare-benefits scandal: families wrongly accused of fraud with the help of a risk algorithm. | 03 | memory, high; named by the critique |
| Hoards of Roman coins have been found in Tamil Nadu. No particular hoard is named or drawn. | 04, 26 | memory, high; check a specific hoard before labelling one |
| Model collapse: models trained on their own outputs lose the tails of the real distribution (Shumailov and others, *Nature*, 2024). | 04 | memory, high; named by the critique |
| ஏரி tanks with earthen bunds and stone sluices, maintained by shared village labour (kudimaramathu). | 04 | memory, high |
| Madhavi's letter in the Silappathikaram is written on a screwpine petal with a jasmine bud dipped in red lac. | 05 | corpus (canto 8, lines 49 to 55) |
| Kuruntokai 18 carries the colophon தோழி கூற்று. Colophons are the compilers', not the poets'. | 05, 21 | corpus for the colophon; memory, high |
| Costly signalling, or the handicap principle: a signal is trusted because it is expensive to fake. The peacock's tail is the textbook case. | 05 | memory, high |
| Banana-leaf meals: the narrow tip to the eater's left. Only that and a pinch of salt are drawn. The positions of other dishes vary and are not labelled. | 07 | critique, partly confirmed |
| Separate dining rows by caste are documented in the Tamil country into the twentieth century. | 08 | memory, high |
| The Kural has a chapter in praise of good family (குடிமை) as well as Kural 972. The category essence in the repo says the books pull both ways. | 08 | corpus for 972; repo for the essence |
| Polygenic scoring of embryos is sold commercially, with weak predictive power for complex traits. | 08 | memory, high |
| Kural 559 ties rain to just rule. Aerosol pollution weakened the South Asian summer monsoon in the late twentieth century (Bollasina and others, *Science*, 2011). | 09 | corpus for the couplet; memory, moderate to high for the study, and the critique also cites it from memory. Check before labelling. |
| The pairing of each landscape with an hour and a situation is the standard reading of Tholkappiyam porul (1:5 names four lands, 1:16 the situations). | 09 | corpus for the two sutras; memory, high |
| 3,232 கரு nodes across the five Sangam groups in `kg/groups`. They include foods, peoples and work. | 10 | corpus, counted in the earlier pass |
| Shifting-baseline syndrome was named by Daniel Pauly in 1995. Historical ecologists do use old texts to recover baselines. | 10 | memory, high; named by the critique |
| The Silappathikaram says pālai is what forest and hill become. | 11 | corpus (canto 11, lines 64, 66) |
| Naladiyar 331: a tortoise playing in the water of a pot while the fire is lit under it. The boiling-frog story is false biology; real frogs, and tortoises, try to get out. | 11 | corpus (verse 331, line 1 quoted); memory, high |
| Akananuru 289: a woman prays at each chirp of the gecko. The gecko omen is also in Akananuru 9 and 151. | 12 | corpus (lines 15, 16); the other two per the critique |
| Gecko feet stick by van der Waals forces on branching hairs (setae, spatulae). Lotus leaves shed water and dirt because of their surface texture. A Japanese high-speed train's nose was reshaped after the kingfisher's beak to cure tunnel boom. No figures are labelled. | 12 | critique, confirmed |
| Nalvazhi is by the medieval Avvaiyar, not the Sangam poet. It is cited by id and not quoted. | 12 | critique |
| Pulse reading uses three fingers on the wrist. Agreement between practitioners is low to moderate (`kg/science/findings.jsonl`). | 13 | repo |
| A small bird's resting heart rate is several times a person's. | 13 | memory, moderate to high |
| பொம்மலாட்டம் is the Tamil tradition of string and rod puppets. | 14 | memory, high |
| No hallmark of ageing has been reversed in humans. This contradicts the verses that promise an undying body. | 14, 28 | repo |
| Kural 950 names four parts of medicine. The fourth, உழைச்செல்வான், is the one who attends at the patient's side. | 15 | corpus; the gloss is ours |
| கல்வம் is the stone mortar of Siddha pharmacy. A scoping review found 220 cases of heavy-metal poisoning linked to Ayurvedic and Siddha preparations. Njanak Kummi 119 mocks outward gold-making from inside the tradition. | 15 | repo; corpus for the verse (cited, not quoted) |
| Tholkappiyam porul 9:28 to 9:33 assigns creatures to the rungs, and 9:32 puts மாவும் மாக்களும் on rung five. | 16 | corpus |
| Moravec's paradox (1980s): reasoning is easy for machines and perception and movement are hard. | 16 | memory, high; named by the critique |
| Breathing near six a minute raises heart-rate variability, and recitation slows breathing to that pace. The 21,600-breath arithmetic is contradicted. | 17 | repo |
| Agasthiyar Njanam is a late text attributed to Agathiyar. | 17 | critique; said so on screen |
| Palm-leaf commentaries exist for the Kural, Parimelazhagar's above all. The layout drawn (verse cut large, gloss beneath and between) is staging. | 19 | memory; layout is invented staging |
| Photography dates from 1839; courts worked before it. The site's blinded test: 17 of 300 pairs passed, and no random control did. | 19 | memory, high; repo |
| The crier's rule for debaters is Manimekalai canto 1, lines 60 to 63. It is paraphrased in the margin and not quoted. | 19 | corpus |
| The yāzh was an arched harp. No ancient instrument survives. **Drawn as a likely form**, without a string count. | 21 | critique, moderate |
| After a machine beat the world chess champion in 1997, more people played chess than before. | 21 | memory, high |
| A நாழிகை is 24 minutes. The sinking-bowl clock is well attested in India from about the fifth century; the Sangam type is uncertain and the bowl is drawn without a claim. | 22 | memory, high for the unit; the bowl type is soft |
| The second is 9,192,631,770 periods of a caesium transition. Pulsar timing arrays use millisecond pulsars as clocks and reported a gravitational-wave background in 2023. | 22 | memory, high |
| In 2014 the EU's top court recognised a right to have search results about oneself removed. | 22 | memory, high; named by the critique |
| Kural 620: those who strive without flagging see the back of fate. Paraphrased in the margin. | 22 | corpus |
| Rice-flour kolam is drawn at dawn and eaten by ants and birds. A sikku kolam loops round a grid of dots. | 22, 25 | memory, high |
| Purananuru 30 doubts people who talk of sun, wind and sky as if they had measured them. It is irony and is no evidence of astronomy. | 25 | corpus (lines 5, 6) |
| Purananuru 66 praises Karikalan's ancestor for driving ships and ruling the wind's work. Reading that as the monsoon is interpretation. | 26 | corpus; interpretation flagged on screen |
| Monsoon trade with the Roman world around the first century CE; Muziris; the Muziris papyrus, a mid-second-century loan and cargo document for the ship *Hermapollon*, mostly pepper. | 26 | critique, confirmed |
| The sewn-plank hull is well attested around the Indian Ocean. No Sangam-era Tamil hull survives. **Drawn as a likely form.** | 26 | critique, uncertain |
| Solar sails have flown: IKAROS (2010, about 14 m on a side) and LightSail 2 (2019, 32 m²). Breakthrough Starshot is a proposal for gram-scale probes. Earth and Mars line up for transfer about every 26 months. One-way light time to Mars is 3 to 22 minutes. | 26 | critique for the sails; memory, high for the rest |
| Manimekalai 27, line 146 is inside the Ajivika account (lines 108 to 165), which names four kinds of atom at line 116. | 27 | corpus; confirmed by the critique |
| Tirumanthiram 2008 is devotional and asserts. It is not natural philosophy. | 27 | corpus |
| The scanning tunnelling microscope dates from 1981. In 1990 thirty-five xenon atoms were placed one by one to spell three letters. The 2022 physics Nobel was for entanglement experiments. The 2025 physics Nobel (Clarke, Devoret, Martinis) was for quantum tunnelling and energy quantisation in a superconducting circuit, the physics of the qubits in the refrigerator drawn here. Quantum computers in 2026 are early and noisy. | 27 | critique, confirmed |
| Simulating the nitrogen-fixing enzyme's active site is a standard proposed use of quantum computers. Cold-atom gravimeters exist and can sense buried water. | 27 | memory, high as proposals |
| Directed evolution of enzymes won the 2018 chemistry Nobel (Arnold; Smith and Winter for phage display). No gene drive has been released in the wild. Target Malaria's work in Burkina Faso was stopped in August 2025; the released strain was not a gene drive. Self-limiting drive designs are real proposals. | 28 | critique, confirmed |
| Snakes have no external ears and follow the pipe's movement. Pambatti 23 says the snake took its eye for an ear. | 28 | memory, high; corpus for the verse (cited, not quoted) |
| Manimekalai 27, lines 264 to 268: the materialist's argument from liquor and from the drum. The epic is Buddhist and presents the schools in order to answer them. The text names dhataki flowers and jaggery, so the script says "liquor" and not "palm liquor". | 29 | corpus |
| Wearable magnetoencephalography helmets with small optical sensors exist. The hard problem of consciousness is open. | 30 | critique; memory, high |
| Purananuru 192 teaches acceptance: life goes as a raft goes with the water, so the poet neither marvels at the great nor scorns the small. | 24 | corpus (lines 9, 12, 13) |
| The பரிசல் is a round coracle used on Tamil rivers. | 24 | memory, high |
| A குத்துவிளக்கு commonly has five wick spouts and a bird finial, and is brass. Carbon-filament bulbs date from 1879. Stars shine by fusion. | 31 | memory, high |
| A common myna can mimic, though hill mynas are the famous talkers. Not labelled as fact anywhere. | throughout | soft |

### Imagined, and labelled so on screen

Everything dated after 2026 is invented, and so is the frame: the year 2526, the hands of 2126 and 2276, and a file recopied once a century. The dated events, by scene:

- 03: 2041, the first verdict that had to carry a name.
- 04: 2068, closed models worth less than the open ones; compute kept as a commons.
- 05: 2060, every letter flawless; letters that keep their drafts.
- 06: 2190, a device sold on turning off.
- 08: 2071, a school asking for an embryo score; two centuries to undo it.
- 09: 2047, rain on a cabinet's agenda.
- 10: 2112, a coastal baseline rebuilt from the love poems.
- 11: 2090, a third and last rebuilding; drylands restored; a settled Mars.
- 12: 2139, a patent office requiring the organism's name.
- 13 to 15: medicine arriving early by the 2090s; a healthy hundred by 2104; the *ageing* slider that will not move; consent as ordinary manners by 2150.
- 16: 2119, a machine that can fold a wet towel.
- 17: 2052, awakening scores withdrawn.
- 18: 2088, the most-asked question; a speaker that declines a flower.
- 19: 2031, seeing no longer believing; 2140, the wrong-line examination; claims published with controls.
- 21: 2060, making declared finished; 2100, who was in the room.
- 22: 2260, records that expire.
- 23: every line in the notebook.
- 24: a wheel nobody holds, and a coracle in 2526.
- 25 to 30: people having gone and measured; cargo sails to Mars; a gram-scale probe at the nearest star; the very small as an ordinary tool by 2200; new-to-nature creatures and the three rules; a machine for every theory of mind; a seventh rung.
- 31: a small sun over a town.

---

## 6. Verification

### Tamil lines

Every Tamil line in a blockquote, and the one line quoted inside the gag of scene 11, was compared character for character with `kg/core/<book>.jsonl` by a `python3 -I` script (couplet 10 with `site/nilai/kural_final.txt`). 69 lines, all matching. Ids verified:

`kural:118`, `silappathikaram:20` (lines 60, 85), `kural:555`, `kuruntokai:18` (lines 4, 5), `kural:341`, `purananuru:182` (lines 1, 2, 3), `kural:972`, `siddhar:sivavakkiyam:39` (line 2), `kural:20`, `kural:559` (line 1), `kuruntokai:25` (lines 3, 4, 5), `silappathikaram:11` (lines 64, 66), `akananuru:289` (lines 15, 16), `kural:948`, `tirumanthiram:724` (lines 1, 4), `kural:950`, `tholkappiyam:porul:9:27` (lines 1, 6), `tholkappiyam:porul:9:32` (line 1), `siddhar:sivavakkiyam:72` (lines 3, 4), `siddhar:sivavakkiyam:494` (lines 3, 4), `kural:423`, `tholkappiyam:eluttu:4:37`, `kural:619`, `kural:152`, `kural:331` (line 1), `purananuru:192` (lines 9, 12, 13), `purananuru:30` (lines 5, 6), `purananuru:66` (lines 1, 2), `akananuru:149` (line 10), `manimekalai:27` (lines 146, 264, 265, 266), `tirumanthiram:2008` (line 2), `siddhar:pambatti:32` (line 1), `kural:126`, `siddhar:sivavakkiyam:327` (lines 3, 4), `tirumanthiram:725` (line 2), couplet 10, `naladiyar:331` (line 1).

Cited by id without quotation, and read in `kg/core` in this pass: `avvaiyar:nalvazhi:7`, `siddhar:agasthiyar-njanam:2.1`, `siddhar:pambatti:23`, `siddhar:pambatti:40`, `siddhar:njanak-kummi:119`, `kural:620`, `manimekalai:1` (lines 60 to 63), `tholkappiyam:porul:1:5`, `tholkappiyam:porul:1:16`.

Kural and Naladiyar ids are written `kural:<n>` and `naladiyar:<n>`; in those two files the key is `verse`. Both files also hold published translations in other fields. None of that text was read into this script, and every English reading here is new and ours.

### Colours, scene by scene

Computed from the hex values in section 2 with WCAG relative luminance. Columns: wall to floor; each art fill against wall and floor (the lower of the two); the two art fills against each other, as a ratio and as CIE76 delta-E; text on wall; the accent on the ink it sits on.

| scene | wall | floor | wall:floor | ink vs background | colour vs background | ink:colour | delta-E | text:wall | accent on ink |
|---|---|---|---|---|---|---|---|---|---|
| 01 | indigo | teal | 2.11 | chalk 6.90 | turmeric 4.10 | 1.68 | 73 | 14.59 | kumkum 5.66 |
| 02 | chalk | tan | 1.89 | indigo 7.70 | teal 3.64 | 2.11 | 43 | 14.59 | brass 4.54 |
| 03 | indigo | grey | 1.92 | chalk 7.59 | turmeric 4.51 | 1.68 | 73 | 14.59 | kumkum 5.66 |
| 04 | turmeric | chalk | 1.68 | indigo 8.66 | laterite 3.69 | 2.35 | 72 | 8.66 | brass 4.54 |
| 05 | laterite | indigo | 2.35 | chalk 6.22 | tan 3.28 | 1.89 | 35 | 6.22 | teal 6.90 |
| 06 | chalk | tan | 1.89 | indigo 7.70 | grey 4.01 | 1.92 | 34 | 14.59 | brass 4.54 |
| 07 | teal | indigo | 2.11 | chalk 6.90 | tan 3.64 | 1.89 | 35 | 6.90 | kumkum 5.66 |
| 08 | chalk | turmeric | 1.68 | indigo 8.66 | teal 4.10 | 2.11 | 43 | 14.59 | brass 4.54 |
| 09 | indigo | teal | 2.11 | chalk 6.90 | turmeric 4.10 | 1.68 | 73 | 14.59 | kumkum 5.66 |
| 10 | tan | chalk | 1.89 | indigo 7.70 | teal 3.64 | 2.11 | 43 | 7.70 | brass 4.54 |
| 11 | laterite | indigo | 2.35 | chalk 6.22 | turmeric 3.69 | 1.68 | 73 | 6.22 | teal 6.90 |
| 12 | turmeric | chalk | 1.68 | indigo 8.66 | teal 4.10 | 2.11 | 43 | 8.66 | brass 4.54 |
| 13 | kumkum | indigo | 2.58 | chalk 5.66 | turmeric 3.36 | 1.68 | 73 | 5.66 | teal 6.90 |
| 14 | chalk | tan | 1.89 | indigo 7.70 | laterite 3.28 | 2.35 | 72 | 14.59 | brass 4.54 |
| 15 | indigo | grey | 1.92 | chalk 7.59 | tan 4.01 | 1.89 | 35 | 14.59 | kumkum 5.66 |
| 16 | tan | chalk | 1.89 | indigo 7.70 | laterite 3.28 | 2.35 | 72 | 7.70 | brass 4.54 |
| 17 | teal | indigo | 2.11 | chalk 6.90 | turmeric 4.10 | 1.68 | 73 | 6.90 | kumkum 5.66 |
| 18 | chalk | turmeric | 1.68 | indigo 8.66 | grey 4.51 | 1.92 | 34 | 14.59 | brass 4.54 |
| 19 | grey | indigo | 1.92 | chalk 7.59 | turmeric 4.51 | 1.68 | 73 | 7.59 | kumkum 5.66 |
| 20 | turmeric | chalk | 1.68 | indigo 8.66 | laterite 3.69 | 2.35 | 72 | 8.66 | brass 4.54 |
| 21 | indigo | kumkum | 2.58 | chalk 5.66 | turmeric 3.36 | 1.68 | 73 | 14.59 | teal 6.90 |
| 22 | chalk | tan | 1.89 | indigo 7.70 | laterite 3.28 | 2.35 | 72 | 14.59 | brass 4.54 |
| 23 | grey | indigo | 1.92 | chalk 7.59 | tan 4.01 | 1.89 | 35 | 7.59 | kumkum 5.66 |
| 24 | chalk | tan | 1.89 | indigo 7.70 | teal 3.64 | 2.11 | 43 | 14.59 | brass 4.54 |
| 25 | indigo | grey | 1.92 | chalk 7.59 | tan 4.01 | 1.89 | 35 | 14.59 | kumkum 5.66 |
| 26 | turmeric | chalk | 1.68 | indigo 8.66 | teal 4.10 | 2.11 | 43 | 8.66 | brass 4.54 |
| 27 | teal | indigo | 2.11 | chalk 6.90 | turmeric 4.10 | 1.68 | 73 | 6.90 | kumkum 5.66 |
| 28 | chalk | tan | 1.89 | indigo 7.70 | teal 3.64 | 2.11 | 43 | 14.59 | brass 4.54 |
| 29 | laterite | indigo | 2.35 | chalk 6.22 | turmeric 3.69 | 1.68 | 73 | 6.22 | teal 6.90 |
| 30 | tan | chalk | 1.89 | indigo 7.70 | laterite 3.28 | 2.35 | 72 | 7.70 | brass 4.54 |
| 31 | indigo | kumkum | 2.58 | chalk 5.66 | turmeric 3.36 | 1.68 | 73 | 14.59 | teal 6.90 |

Minimums across all 31 scenes: wall to floor 1.68, art on background 3.28, ink to colour 1.68 (delta-E 34), text 5.66, accent 4.54. The ledger strip is 14.59:1 in every scene.

### Other checks run on this file

- Every (a) sentence is 13 words or fewer.
- No scene has more than three lines of Tamil in its anchor.
- Walls alternate dark and light across all 31 scenes; scenes 25 and 31 are night.

### Critique points not taken, or taken differently

1. **The optional merges of சமூகம், புலமை and இயற்கை.** Not taken. Each of the three would delete a sentence the critique itself lists as one to protect (12 "rank", 14 "names", 27 "bodies and life", 28 "the yāzh"), and merging names with the wasteland would crowd out the Mars flat. The reel is 31 scenes because of point 2, with those three categories intact.
2. **Three closing beats after the peak (steer, the ledger, the lamp).** You asked for two at most. With strict dark and light alternation, a night sky at "look up" and a night lamp at the end, exactly two closing beats is impossible: the lamp would fall on a light wall. So there is one. The ledger unrolls by the light of the lamp in scene 31, and "steer" moves to scene 24, after the notebook, where it answers the fifth pencil worry and turns the reel towards the sky. To make the parities work the reel now opens on a dark wall.
3. **Timing arithmetic.** The critique's 29 scenes at 5.5 s plus 24 s comes to 3:03, not 2:55. Ordinary scenes are set at 5.2 s, and 31 scenes come to about 2:50.
4. **Kural 950 sentence**, "machines took three, and left the chair". The four parts are patient, healer, remedy and attendant, and a machine cannot take the patient's part, so "three" is wrong. Replaced by "the fourth **stays** by the bed", with the count explained in the margin.
5. **"Like palm liquor."** The lines name dhataki flowers and jaggery. The sentence says "liquor".
6. **The commentary leaf with gloss written around a central verse.** That is a paper and print layout. A palm leaf is too narrow for it, and I could not confirm it. The object is kept, drawn as a verse line with gloss beneath and between, and marked as staging.
7. **Scene 05 rewrite.** The critique lists "flawless meant nobody came" among the sentences to protect and also offers a replacement. The protected sentence stays, and the replacement's idea (a costless signal proves nothing) is in the margin.
8. **The steer rewrite**, "one stroke picks the bank". Taken further, as you asked: the sentence now says outright that the stroke is ours, and the anchor adds the poem's own conclusion so the acceptance is on screen.
9. **Chalk with tan as a working wall and floor pair.** The critique measured it at 1.51, under the 1.6 you set. Tan was deepened to `#CDAE78` (1.89) and teal to `#0A5C63` so it still clears 3:1 on tan.
10. **Quoting fragments.** The critique quotes part-lines of Nalvazhi 7 and others. Anchors here are whole lines only, so Nalvazhi is cited by id and Akananuru 149 by line 10 alone.
11. **Small second anchors in B scenes.** Dropped as advised, which means Kural 26, 1062, 941, 742 and Tirumanthiram 270 are no longer quoted. Kural 331 moved into காலம் (scene 22), where it carries the site's own word.
