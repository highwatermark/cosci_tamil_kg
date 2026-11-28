# Nilai v3 reel: image and video shot list (Google Flow: its image model, and Veo for short clips)

Source: `site/nilai/v3_script_final.md` (31 scenes) and the stage in `site/nilai/build/v3/` (a 1000 x 1000 SVG art space, wall above, floor band below the horizon at y = 760, feet of characters at the horizon, myna drawn facing right).

Purpose: painted cut-outs that replace the flat SVG art. Every image is one object or one character on a flat background, so it can be keyed out, layered over the coloured stage, and animated as a sprite. A few hero transformations are also made as short Veo clips on the same background (section 5).

## 0. How to use this list

- **Prompt = subject line + master style prompt.** Character images also take the character lock (section 2).
- **Background: pure chroma green `#00FF00`, for every image.** White was rejected because too much of our art is white: kolam flour, the whitewashed ceiling, the screwpine petal, paper, foil, flames, and the myna's wing patches. Our palette has no saturated green, so green keys cleanly. The few green subjects (banana leaf, lotus leaf, grass, trees) are directed to a deep, dull teal-green that is far from `#00FF00`.
- **Aspect and size:** 1:1, 1024 px or larger. Pick 1:1 in Flow's image settings as well as saying it in the prompt. Ask for the subject to fill about 80% of the frame with clear green on all four sides.
- **Reference images.** Generate the two character sheets first. In Flow, save each approved sheet and attach it as a reference image (an ingredient) with every pose prompt. Once the first hero object is approved (the kuthuvilakku), feed it as a style reference for every other object, with the line "match the paint handling and lighting of the reference; do not copy its subject".
- **Facing.** Characters and vehicles face right, as in `art.py`. Flipping a sprite in SVG also flips the light, so do not flip hero objects. For the keeper and the myna a flip is tolerable in small sizes.
- **Text is never painted.** Readouts (`0.0000 g`, `FAIR`, `TARE?`), labels, seals, the ledger lines, Tamil letters and numbers stay as live SVG text over a blank painted surface. Every screen, page, label and slate below is generated blank.
- **Tone tag.** The script's colour rules put light art on dark walls and dark art on light walls (odd scenes are dark, even scenes are light). Each object carries a tone tag; add the matching clause to the prompt:
  - `tone light` (dark-wall scenes): "Overall light in value: chalk white, palm-leaf tan and turmeric dominate, with indigo only in the deepest shadows."
  - `tone dark` (light-wall scenes): "Overall dark in value: night indigo, peacock teal and laterite dominate, with chalk white only in the highlights."
  - `tone mid` (reused on both wall groups): natural colour; add a 1.5 px keyline in the wall colour in CSS (`filter: drop-shadow`) so the edge always separates.
- **Keying.** Key on distance from `#00FF00` with a soft tolerance, then despill the edge. The contact shadow comes out as dark green: keep it as a separate multiply layer or drop it and use the stage's own `shadow()`. Flames and glows are generated as solid paint shapes with no halo; add the glow in CSS.
- **Stays as SVG (not generated):** all text and readouts, chat bubbles, sliders, dials, the heart trace, the receipt, paper tails, the two-page spread, the river, the rain curtain, the haze, the map legend, the village map and its spreading line, stars and star routes, the neural-network lights, exploded-diagram leader lines, and the kolam line when it is being drawn. These are motion graphics, and they need to morph.

## 1. Master style prompt (append to every image)

> Hand-painted gouache cut-out illustration, matte opaque paint with visible brushwork, crisp cut-paper silhouette and subtle paper grain; warm editorial collage feel rooted in Tamil material culture. Limited palette only: turmeric yellow, laterite red-brown, peacock teal, palm-leaf tan, kolam-chalk white, night indigo, kumkum red, brass accents. Soft key light from upper left, one gentle contact shadow directly beneath. Single subject, centred, whole and uncropped, on a flat solid pure chroma green #00FF00 background. No scenery, no text, no letters, no watermark.

Palette hexes, for a colour-swatch reference image if the model drifts: chalk `#F7F2E6`, tan `#CDAE78`, turmeric `#F2B21B`, brass `#AE7F1B`, indigo `#171C45`, stone grey `#4B4D50`, teal `#0A5C63`, laterite `#9A3B21`, kumkum `#BE1230`.

Negative line to add when a result goes wrong: "not a photograph, not 3D render, not vector flat art, not anime, no gradient background, no floor, no horizon, no frame, no border, no second object, no hands unless stated".

## 2. Recurring characters (generate first)

### 2.1 The keeper of 2526

**Character lock (append to every keeper prompt, before the master style):**
> The same character as the reference sheet: a South Indian girl of about fourteen, warm brown skin, short cropped black hair, calm attentive face, an iron stylus tucked behind her right ear. Outfit, old and future mixed: a knee-length hand-loom tunic in turmeric with a narrow kumkum-red temple border, loose indigo trousers gathered at the ankle, a slim peacock-teal sash, flat leather sandals, one plain thin band on the left wrist. Across her body, a flat satchel woven from palm-leaf strips, in tan. Full figure, head to feet.

- **K0** · character sheet · tone mid — "Character turnaround sheet of one character on a single image: front view, three-quarter view, side view facing right, and back view, standing relaxed, same height and same outfit in all four, evenly spaced in a row; plus two small head studies, one calm and one smiling." + lock + master. (The only image with more than one figure. It is a reference, not a sprite.)
- **K1** · walk — "Walking to the right in mid-stride, left foot forward, right arm swinging forward, satchel swinging slightly, looking ahead. Side-on three-quarter view."
- **K2** · point — "Standing, facing right, right arm fully extended and index finger pointing up and to the right, left hand resting on the satchel strap, eyebrows raised, mouth slightly open as if explaining."
- **K3** · write — "Kneeling on one knee facing right, left hand steadying a long narrow blank palm-leaf strip, right hand incising it with the iron stylus held like a pen, head bowed in concentration. The space behind her ear is empty because the stylus is in her hand."
- **K4** · startled — "Standing, facing right, rocked back on her heels, both hands raised with fingers spread, eyes wide, mouth a small o, satchel flying out behind her."
- **K5** · delighted — "Standing, facing right, up on her toes, both fists raised near her shoulders, wide open smile, eyes crinkled."
- **K6** · sitting — "Sitting cross-legged on the ground, facing three-quarters right, back straight, hands resting on her knees, satchel on the ground beside her, calm half-smile."

Extra keeper poses, lower priority, each used once or twice:
- **K7** · lying down (scene 25) — "Lying on her back on the ground, seen from the side, hands behind her head, one knee up, looking straight up."
- **K8** · taper and leaf (scene 31) — "Standing, facing the viewer, right hand holding out a thin lit taper towards the viewer, left hand holding a long blank palm-leaf strip, quiet smile."
- **K9** · paddling (scene 24) — "Kneeling, facing right, both hands on a short wooden paddle held low on her right side, mid-stroke." (No boat; the coracle is a separate image.)
- **K10** · carrying (scenes 11, 15, 18) — "Walking to the right, both arms out in front at waist height as if carrying one end of a large flat panel, leaning back a little against the weight." (Hands empty.)

### 2.2 The myna

**Character lock (append to every myna prompt, before the master style):**
> The same bird as the reference sheet: a common myna, Acridotheres tristis, drawn accurately. Glossy black head, nape and throat like a hood. Chocolate-brown body and wings. A bare, bright yellow patch of skin behind and below the eye, shaped like a teardrop. Bright yellow bill and bright yellow legs and feet. A white patch at the base of the flight feathers, white tip to the dark tail, white under the tail. Stocky, upright, short-tailed, no crest. One bird only.

- **M0** · character sheet · tone mid — "Reference sheet of one bird on a single image: side view facing right standing, front view, three-quarter back view, and one view in flight from the side with wings fully spread, showing the large white wing patches and the white tail tip." + lock + master.
- **M1** · walk — "Striding to the right with a jaunty, self-important walk, one yellow foot lifted, head pushed forward, tail level."
- **M2** · point — "Standing facing right, body upright, one wing held out straight to the right like a pointing arm, bill open as if announcing something."
- **M3** · write — "Standing facing right, head bent low, holding a tiny iron stylus in its bill and scratching with it at ground level, one foot braced forward."
- **M4** · startled — "Leaping straight up with both feet off the ground, wings half open showing the white patches, head feathers raised, bill open, eye wide."
- **M5** · delighted — "Standing facing right, chest puffed out, head tilted back and bill wide open in song, wings slightly lifted, tail cocked up."
- **M6** · sitting — "Perched and settled, facing right, body fluffed and round, legs folded so only the yellow toes show gripping, head turned to look at the viewer." (The default perch pose: on the board, the pan, the masthead, the rung.)

Extra myna poses, lower priority:
- **M7** · head under wing (scene 06) — "Standing on one leg asleep, head turned back and tucked under one wing."
- **M8** · flying (landing on the pan, the sail) — "In flight to the right, side view, wings fully spread on the downstroke, large white wing patches and white tail tip clearly visible, yellow feet tucked."
- **M9** · tipsy (scene 29) — "Standing unsteadily, leaning to one side, one wing out for balance, eyes half closed, bill slightly open."
- **M10** · head sway (scene 28) — "Standing facing right, neck stretched tall, head tilted far to one side as if swaying."

### 2.3 Supporting people (lowest priority; the SVG `person()` can stand in)

Same paint handling, plainer and quieter than the keeper, no faces in close detail. All tone as their scene.
- **P1** · woman listening (12, tone dark) — "A South Indian woman in a plain cotton sari standing still, head tilted up and to one side as if listening to something above her, hands pressed together at her chest. Full figure, facing three-quarters right."
- **P2** · bard singing (20, 21, tone dark) — "A South Indian bard, a wiry older man in a white veshti with a cloth over one shoulder, standing and singing with his mouth wide open, one hand raised, palm up. Full figure, facing right."
- **P3** · Pambatti the charmer (28, tone dark) — "A South Indian snake charmer sitting cross-legged, lean, with matted hair tied up and a plain cloth wrap, both hands raised as if holding a pipe to his mouth. Hands empty. Full figure, facing right."
- **P4** · old woman next door (18, tone dark) — "An elderly South Indian woman in a plain cotton sari, standing a little stooped, smiling in surprise, hands half raised. Full figure, facing left."

## 3. Objects, scene by scene

Format: **ID** · object · tone · view, then the subject line. Default view is "three-quarter view from slightly above, as if standing on a floor". `reuse:` names the scenes that take the same image. A variant made by editing an approved image ("edit of") should be made in Flow by attaching that image as the reference and asking for the edit, which keeps the two stages registered for the morph.

### 01 · the hand of 2526 (dark wall)
- **01-T** · palm-leaf manuscript bundle · tone mid · reuse: 23, thumbnails — "An ōlaiccuvaḍi, a Tamil palm-leaf manuscript bundle, closed. About forty long narrow leaves, each roughly 4 cm by 35 cm, stacked evenly between two plain wooden boards slightly larger than the leaves. Two string holes pass through the whole stack, one third in from each end. A cotton cord runs through one hole and is wound several times around the bundle. Leaf edges are tan and slightly uneven. Seen long side on, three-quarter view from above."
- **01-T2** · the bundle fanned · tone mid · reuse: 23 — "Edit of 01-T: the same bundle untied, the top board lifted off and set beside it, the leaves fanned out on the cord like a hand of cards so that faint incised lines of lampblack writing show as tiny illegible marks."
- **01-N** · phone · tone mid · reuse: 06, 12, 16 — "A plain modern smartphone standing upright, seen from the front at a slight angle, thin, rounded corners, dark blank screen with a soft reflection, no logo, no icons. A short charging cable plugged into the bottom, lying loosely to one side."
- **01-F** · the ledger leaf · tone mid · reuse: every scene, 19, 31 — "One single long palm leaf strip standing vertically, tan, with two string holes, slightly curled at the ends, faintly luminous as if lit from within. Thirteen fine ruled lines run across it, evenly spaced, with nothing written on them. Flat front view." (Generate tall in the square; it is cropped to a strip. Ledger text is SVG.)
- **01-P** · iron stylus · tone mid · reuse: 27 and as a prop — "An eḻuttāṇi, an iron writing stylus about 15 cm long: a slim dark iron shaft with a sharp point at one end, a small flat knife-like blade at the other end, and a turned knob in the middle. Lying diagonally."

### 02 · the beam that levels first (light wall)
- **02-T** · tharasu · tone dark — "A hand-held tarācu, a traditional Tamil two-pan balance. A straight wooden beam a forearm long. At its centre, an upright pointer tongue sitting inside a small metal fork, with a hanging loop above the fork to lift it by. From each end of the beam hang three thin cords that meet a shallow round brass pan. Both pans empty and exactly level. Front view, the whole scale hanging in the air." (No hand. The hand is 02-H.)
- **02-H** · hand on the loop · tone dark · reuse: 13 base hand — "A single brown-skinned right hand and wrist coming down from the top of the frame, thumb and two fingers pinched together as if holding a small loop. Nothing in the hand."
- **02-N** · laboratory balance · tone dark · covers NOW and FUTURE — "A modern laboratory analytical balance: a low base with a small blank rectangular display, a round steel weighing pan, and a clear glass draft-shield box with sliding doors around the pan. Empty. Three-quarter front view." (The readout and `FAIR` are SVG.)

### 03 · the king who did not check (dark wall)
- **03-T** · the anklet · tone light — "A cilampu, an ancient Tamil anklet: one thick hollow gold ring, slightly oval, with a visible seam and a small screw-like clasp, a row of tiny beads around the outer edge. Standing on its edge, three-quarter view."
- **03-T2** · the anklet broken · tone light — "Edit of 03-T: the same hollow gold anklet broken open into two curved halves lying on their sides, the hollow interior visible." (Stones are separate.)
- **03-G** · one red stone · tone light · reuse: scattered many times — "One small rough-cut ruby, deep kumkum red, with a single bright highlight. Macro view."
- **03-N** · counter-top terminal · tone light — "A small counter-top card payment terminal with a keypad of blank keys, a blank screen, and a slot at the top where paper would come out. Chunky, slightly dated. Three-quarter view." (The receipt is SVG.)
- **03-F** · terminal opened · tone light — "Edit of 03-N: the same terminal with its top casing cracked and lifted off like a lid, showing a simple circuit board and a paper roll inside."

### 04 · the hoard becomes a tank (light wall)
- **04-T** · Roman coin hoard in a clay pot · tone dark — "A narrow-necked, round-bellied unglazed terracotta pot, laterite red, filled to the neck with ancient Roman gold coins, a few spilling over the rim and lying at its foot. Each coin shows an emperor's head in profile with a laurel wreath, worn and irregular in outline, hand-struck. The lettering around the rim of the coins is worn to illegible ticks."
- **04-C** · one coin · tone dark · reuse: copies blurred and blanked in post — "One ancient Roman gold aureus, seen flat from the front: an emperor's head in profile facing right with a laurel wreath, slightly off-centre strike, irregular edge, lettering worn to illegible ticks. Macro view."
- **04-N** · the sealed vault · tone dark — "A heavy round steel vault door set in a short thick ring of wall, shaped like the mouth of a pot, shut, with a spoked wheel handle; through a small round window, rows of tiny server lights. Front view."
- **04-F1** · the cracked pot · tone dark — "Edit of 04-T: the same pot empty of coins, with one long vertical crack down its belly." (Water is SVG.)
- **04-F2** · the village tank (ēri) · tone dark · reuse: 12 — "An ēri, a South Indian village irrigation tank, as a single cut-out island of land: a long curved earthen bund planted with a few palmyra palms, still water held behind it, and a small stone sluice with two upright granite posts and a slab across them where water leaves. Seen from high three-quarter view. A piece of landscape cut out like a model, with nothing around it."
- **04-F3** · temple tank with steps · tone dark · reuse: 12 (alternate for the tank under the lotus leaf), 23 thumbnail — "A South Indian temple tank, a kuḷam with a teppam pavilion, as a single cut-out block of ground: a square pool of still dark-teal water at ground level, wide shallow granite steps descending evenly on all four sides in about eight courses, a low parapet with a gap and a small stone stair on each side, and a small square pillared stone maṇḍapam standing in the middle of the water. High three-quarter view, cut out like an architect's model, with nothing beyond its edges." (The script's scene 04 FUTURE is the ēri, **04-F2**, which stays canonical there; this tank is made because it carries scene 12's lotus and kingfisher better if the ēri reads as plain ground.)

### 05 · the third voice (dark wall)
- **05-T** · the screwpine petal letter · tone light — "One long, narrow, creamy white petal-like bract of the screwpine flower, tāḻai, slightly curled lengthwise, lying flat. Beside it, one small closed jasmine bud whose tip is stained with red lac." (Writing is SVG.)
- **05-T2** · the petal rolled — "Edit of 05-T: the same white petal rolled into a loose scroll and tied with a single thread."
- **05-F** · the unrolled letter · tone light — "A long sheet of cream handmade paper, unrolled, its two ends still curling, with one round water stain the size of a thumbprint near the lower right. Otherwise blank. Flat front view."

### 06 · the lamp that can go out (light wall)
- **06-T** · agal lamp, unlit · tone dark · reuse: 06 FUTURE, 31 thumbnails — "An akal, a palm-sized unglazed terracotta oil lamp: a shallow round saucer pinched into one small spout, a pool of oil, and a single twisted cotton wick lying in the spout with its blackened tip just over the lip. No flame. Three-quarter view from above."
- **FL** · one flame · tone light · reuse: 06, 11, 31 (every lamp, the taper, the cooking fire) — "One small oil-lamp flame alone: a teardrop of turmeric yellow with a paler core and a kumkum-tinged tip, painted as a solid shape with a hard edge, no glow, no halo, no smoke, no wick."
- (NOW reuses **01-N** lying face up; the wall of rectangles is SVG.)

### 07 · the row (dark wall)
- **07-T** · banana leaf with a meal, tip to the left · tone light · view straight down — "Top-down view of one banana leaf laid out for a South Indian meal. The leaf is the tip section of a banana leaf, placed horizontally: its narrow tapering tip points to the LEFT of the image and its wide cut edge is on the RIGHT. The central midrib runs horizontally across the middle. The eater sits at the bottom edge of the image. On the leaf: a small pinch of white salt at the top left corner, and a mound of plain white steamed rice in the centre of the lower half. Nothing else. The leaf is a deep, dull peacock teal-green with paler parallel veins, never bright lime green."
- **07-T2** · the full meal, served in order · tone light · view straight down · hero version of 07-T — "Edit of 07-T: the same leaf, tip still pointing LEFT, eater at the bottom edge. Placement, all directly on the leaf: at the top-left corner a pinch of white salt; immediately to its right a small spoon of red-orange mango or lime pickle; continuing left to right along the upper half above the midrib, small separate portions of a pale curd pachadi, a yellow lentil-and-cucumber kosambari, a dry green-and-coconut poriyal, a soft kootu, and a mixed avial; at the upper right a crisp round appalam and one vadai; at the lower left, near the tip, a small ripe banana and a little sweet; in the centre of the lower half a mound of plain white rice with a ladle of yellow paruppu dal and a spoon of ghee on top. No bowls, no cups, no plates, no cutlery." (Common Tamil order; it varies by household and region. The script itself claims only the tip to the left, salt at the top corner and rice in the middle, so this image is never labelled with dish names.)
- **07-E** · empty banana leaf · tone mid · reuse: 08 (many copies), 07 row — "Edit of 07-T: the same leaf, same placement, completely empty and clean, a few water droplets on it."
- **07-N** · server blade · tone light — "One thin horizontal server blade as pulled from a data-centre rack: a long flat metal tray with a perforated front face, a row of small indicator lights, two handles. Proportions long and narrow like a leaf. Three-quarter view." (The rack is a stack of copies; lights are SVG.)
- **07-F** · open rack laid flat · tone light — "A long low open-topped bench made from a server rack laid on its side with its doors removed, like a communal dining table at floor height, running left to right, seen from three-quarter view above. Nobody at it."

### 08 · nothing written in flesh (light wall)
- **08-T** · the cloth screen · tone dark — "A long plain cotton cloth hung as a screen from a rope tied between two short bamboo poles, hanging to the ground, with soft vertical folds. Front view." 
- **08-F** · the screen rolled up — "Edit of 08-T: the same cloth rolled up tight to the rope like a blind, the poles still standing."
- (Leaves reuse **07-E**. The score sheet, seat numbers and place cards are SVG.)

### 09 · rain first (dark wall)
Five painted stage flats. Each is one object: a flat, upright wooden theatre panel with a visible plank edge and a small wooden brace foot, and a landscape painted on its face. The landscape stays inside the panel. Tone light for all (the same flats return in 10 and 11 on other walls, where the wall-colour keyline carries them).
- **09-K** · kuṟiñci flat — "…painted with steep forested hills at midnight under a small moon, a waterfall, and two tiny figures meeting under a tree."
- **09-M** · mullai flat — "…painted with the edge of a forest at evening, jasmine in flower, a small house, and a tiny figure of a woman waiting in the doorway."
- **09-R** · marutam flat — "…painted with flooded paddy fields at dawn, a buffalo, a village behind, and two tiny figures turned away from each other."
- **09-N** · neytal flat · reuse: 10, 11 — "…painted with a sandy shore at sunset, screwpine bushes, a fishing boat pulled up, and one tiny figure looking out to sea."
- **09-P** · pālai flat · reuse: 11 — "…painted with cracked dry ground at harsh noon, one bare tree, and a tiny figure walking away into the distance."
- **09-S** · satellite map tile · tone light — "A square tile of a satellite view of the southern Indian peninsula and the sea around it, painted loosely, with one thin broken band of white cloud across it. A flat tile lying down, three-quarter view from above, with a thin edge. No labels, no borders, no grid."
- **09-U** · the myna's umbrella · tone light — "A very small umbrella made of dried palm leaf: a shallow cone of overlapping palmyra-leaf strips stitched around a thin bamboo stick handle. Open, upright."

### 10 · the names (light wall)
- **10-H** · the heron · tone dark — "A small pond heron standing in profile facing right on thin, pale green legs like millet stalks, neck drawn in, long dagger bill pointing down as if watching water. Streaked buff and white plumage."
- **10-E** · eel — "One slender freshwater eel in an S-curve, side view, smooth and dark, a small eye and a long fin along the back."
- **10-L** · water lily — "One water lily flower, white with a turmeric centre, half open, with a single round floating pad beside it in deep dull teal-green."
- **10-S** · screwpine · reuse: 05 context — "One screwpine shrub, tāḻai: a short trunk on stilt-like prop roots, long sword-shaped leaves with saw edges in spiral tufts, and one pale cream flower spike."
- **10-D** · drum — "A paṟai, a Tamil frame drum: a shallow round wooden frame with cowhide stretched over one side, with two sticks, one short and thick, one long and thin, lying across it."
- **10-N** · fishing net — "A small hand-cast fishing net of knotted cotton cord with little lead weights around the rim, heaped loosely with part spread open."
- **10-F** · the cabinet of drawers · tone dark · reuse: 12 (as the tower) — "A tall narrow wooden cabinet of many small square drawers in a grid, like an old seed or apothecary cabinet, each drawer with a small brass pull and a blank paper label. Two drawers slightly open. Three-quarter front view."

### 11 · the wasteland is made (dark wall)
- **11-N** · stilt house · tone light — "A small coastal house of timber and palm thatch raised on four tall wooden stilts, with a short ladder. Three-quarter view." (Scaled to three heights in SVG.)
- **11-F1** · line of trees and channel · tone light — "A short row of five young trees planted along a straight hand-dug earthen water channel, as a single cut-out strip of ground, three-quarter view from above."
- **11-F2** · the Mars flat · tone light — "The same kind of upright wooden theatre flat as the others, painted with rust-red rocky ground, a small pale sun, two tiny moons in the sky, and a tiny figure walking away."
- **11-G** · the tortoise in the pot · tone light — "A wide round clay cooking pot sitting on three hearth stones, with small sticks of firewood beneath and no flames. In the water in the pot, a small tortoise floats happily on its back with its legs spread, head out, contented." (Flame is **FL**.)

### 12 · the gecko's feet (light wall)
- **12-T** · house gecko · tone dark — "A common Asian house gecko seen from directly above, pale sandy grey-pink with slightly translucent skin, large dark lidless eyes, body in a gentle S-curve, all four feet splayed flat with five broad toes each, tail curled a little."
- **12-N1** · gecko toe pads, macro · tone dark — "Extreme macro of the underside of one gecko foot: five toes spread like a fan, each toe widening to a pad, and each pad crossed by a neat stack of thin overlapping horizontal ridges, like tiny slats, with a small claw at the tip."
- **12-N2** · the hairs · tone dark — "Scientific-illustration macro of gecko setae: a dense field of fine upright hairs, each hair branching at its tip into many tiny flat spatula-shaped ends. Painted, not a micrograph."
- **12-N3** · the tape · tone dark — "A short strip of matte dry adhesive tape, one end curling, its sticky face showing a fine velvety texture." (The phone is **01-N**.)
- **12-F1** · the climbing machine · tone dark · reuse: 30 (second machine in the queue) — "A small four-legged climbing robot, about the size of a cat, with a slim body and four broad flat feet that have ridged gecko-like pads, shown clinging to nothing, as if climbing straight up, seen from the side."
- **12-F2** · lotus leaf with water beads · tone dark · view three-quarter from above — "One large round lotus leaf, slightly cupped, with fine veins radiating from the centre, in deep dull teal-green with a matte waxy bloom. On it sit several perfectly round, bright beads of water like glass marbles, not wetting the surface, one bead larger near the centre and one rolling off the rim."
- **12-K** · kingfisher diving · tone dark — "A white-throated kingfisher in a steep head-first dive, pointing down and to the right, wings folded tight against the body, long heavy red bill leading. Chestnut-brown head and belly, white throat and breast, bright turquoise-blue back, wings and tail, red feet tucked."
- **12-S** · shinkansen nose · tone dark — "The front car of a Japanese high-speed train of the 500 series type, side view facing right: a very long, low, tapering pointed nose like a kingfisher's bill, a small cockpit window set far back, smooth pale grey body with a darker band. No logos, no numbers. Cropped cleanly after the first door."

### 13 · the order of care (dark wall)
- **13-T** · pulse reading · tone light — "Two hands only: one forearm resting palm up, and a second hand laid across the inside of the wrist with its index, middle and ring fingers in a row on the pulse, thumb underneath. Gentle. No bodies."
- **13-N** · stethoscope · tone light — "A classic stethoscope lying in a loose loop: round chest piece, single tube splitting into two, metal ear tubes with small ear tips."
- **13-F** · the wrist band · tone light · reuse: 15 — "A single plain, very thin flexible band, thread-narrow, closed in a ring as if on a wrist, with one tiny glowing dot. No screen."

### 14 · the body as a machine (light wall)
- **14-T** · the puppet · tone dark — "A pommalāṭṭam puppet from Tamil Nadu: a jointed wooden figure about knee high in a painted costume with a tall crown, large painted eyes, jointed shoulders, elbows, hips and knees. Strings run up from the head and hands to a wooden control ring above, and two thin rods run to the hands. Hanging in the air, front view."
- **14-F** · the person, reassembled · tone dark — "A South Indian man of about forty in a plain cotton shirt and veshti, sitting on the ground with his knees up, mid-yawn with one hand over his mouth and the other arm stretched up, relaxed and tired in an ordinary way. Full figure, facing three-quarters right." (Same paint and proportions as the supporting people in 2.3.)
- **14-N** · the puppet apart · tone dark — "Edit of 14-T: the same puppet as an exploded view, every part separated and floating a little apart in its correct relative place: head, crown, torso, upper arms, forearms, hands, thighs, shins, feet. No strings, no lines, no numbers." (Slice into parts for the fly-apart; leader lines are SVG.)

### 15 · the fourth part (dark wall)
- **15-T1** · sick-bed on the floor · tone light — "A thin woven grass mat on the ground with a folded cotton sheet and a small pillow, as a sick-bed, empty. Three-quarter view from above."
- **15-T2** · low stool · tone light · reuse: 21 (ten stools) — "A low round wooden stool with three short turned legs. Three-quarter view."
- **15-T3** · palm-leaf fan · tone light — "A hand fan, a vicirī, made from one dried palmyra leaf trimmed into a rounded shape with its stalk as the handle and a stitched cloth border."
- **15-T4** · kalvam · tone light — "A kalvam, the stone mortar of a Siddha physician: a heavy boat-shaped trough carved from one block of dark granite, long and oval with a rounded hollow, and a stone pestle with a flat rubbing end lying across it. Empty and clean. Three-quarter view from above." (The glass case and the label are SVG. Nothing in the mortar.)
- **15-N1** · hospital bed · tone light — "A modern hospital bed with raised head section, side rails and wheels, white sheet, empty. Side-on three-quarter view."
- **15-N2** · visitor's chair · tone light — "A plain hospital visitor's chair with a metal frame and a padded seat, empty, facing left."
- **15-N3** · patient monitor · tone light — "A bedside patient monitor on a pole stand, with a blank dark screen and a few blank buttons."

### 16 · the ladder, climbed down (light wall)
- **16-T** · bamboo ladder · tone dark · reuse: 30 — "A tall straight ladder of two bamboo poles with exactly six bamboo rungs, each rung lashed to the poles with criss-crossed coir rope. Standing upright, front view, the rungs evenly spaced and clearly countable." (The seventh rung is 30-F.)
- **16-C1** · grass tuft · reuse: 30 — "One tuft of grass with a few seed heads, in deep dull teal-green, and a little soil at its base."
- **16-C2** · small tree — "One small neem-like tree with a slim trunk and a rounded crown in deep dull teal-green."
- **16-C3** · snail — "One garden snail, side view facing right, spiral shell, eye stalks out."
- **16-C4** · ant — "One black ant, macro side view facing right, three body segments, six legs, bent antennae." Reuse: 22 (ants carrying the kolam).
- **16-C5** · crab — "One small shore crab, front view, two claws raised, eyes on stalks."
- **16-C6** · bee — "One honeybee in flight, side view facing right."
- **16-C7** · deer — "One spotted deer, a chital doe, standing, side view facing right, head turned to the viewer."
- **16-F** · the phone with an arm · tone dark · reuse: 30 (first machine in the queue) — "A smartphone with a blank screen that has grown one clumsy, thin, jointed mechanical arm from its side, ending in a soft three-fingered gripper, reaching downward and feeling for something."

### 17 · the breath, and the 64% (dark wall)
- **17-T** · counting hand · tone light — "One open brown-skinned right hand, palm towards the viewer, the thumb tip touching the middle joint of the index finger as if counting on the finger joints. A string of dark round rudraksha beads is looped twice over the wrist."
- **17-N** · the ring · tone light — "One plain smooth smart ring, a thick band of dark metal with a faint line of light on the inside. Macro, three-quarter view."
- **17-F** · the windowsill · tone light — "A short section of a plain wooden windowsill, seen from the front, as a single plank shelf with nothing on it." (The ring is placed on it in SVG.)

### 18 · the stone that speaks (light wall)
- **18-T** · the planted stone · tone dark — "A naṭṭakal: one rough, undressed, knee-high upright stone set in a small mound of earth, with four fresh flowers laid on its top. Beside it, a small round clay pot and a wooden ladle. No carving, no face, no paint on the stone."
- **18-N** · home speaker · tone dark · reuse: 20, 27 — "A small cylindrical home smart speaker covered in woven fabric, with a thin ring of light around its top. No logo."
- **18-F** · the kitchen shelf · tone dark · reuse: 27 — "A simple wooden kitchen wall shelf, front view. On it, at the left, a flat granite grinding stone with its cylindrical roller, an ammi, and at the right a round clay pot. A clear empty space in the middle of the shelf."
- **18-G** · garland — "A short garland of jasmine and marigold strung on thread, hanging in a U shape."

### 19 · the gloss, and the twin (dark wall)
- **19-T** · the glossed leaf · tone light — "One long narrow palm-leaf strip lying flat, front view, tan, two string holes. Across its middle, one line of large incised marks; above and below it, several rows of much smaller incised marks; squeezed between some of the rows, a few even tinier marks added later in a darker lampblack. All marks are abstract, illegible scratches, never real letters." (Real verse and gloss, if shown, are SVG text over **01-F** instead; this image gives the texture.)
- **19-N** · wax seal · tone light — "One round wax seal in kumkum red with a raised rim and a smooth blank centre, slightly irregular edge. Front view." (`VERIFIED` is SVG. The leaf is **01-F** laid flat; the document and the grey twins are SVG.)

### 20 · body and life (light wall)
- **20-N** · microphone · tone dark — "One vintage broadcast microphone with a large rounded metal grille of fine horizontal slots, on a short stand, front view, the grille filling most of the frame."
- **20-F** · speaker face — "One round loudspeaker driver in a plain square wooden cabinet, front view: a dark cone behind a circular metal grille."
- (THEN is **P2**, the bard. Letters are SVG.)

### 21 · the wrong note (dark wall)
- **21-T** · the yāḻ, a likely form · tone light — "A reconstruction of an ancient Tamil yāḻ, an arched harp: a long boat-shaped wooden sound box covered with stretched hide, and from one end a single smoothly curved wooden neck rising up and over it like a bow. Gut strings run from the neck down to a wooden bar along the top of the sound box, getting shorter towards the curve. A modest number of strings. Plain, with no animal head, no pillar, no pedals. Side view, standing as if being played." 
- **21-F** · the yāḻ with one new string — "Edit of 21-T: the same harp with one additional string in a contrasting kumkum-red thread."
- **21-N1** · synthesiser · tone light — "A keyboard synthesiser seen from three-quarter view above: a long flat body, a row of white and black keys, a panel of blank knobs. No brand, no labels."
- **21-N2** · trophy with a cable · tone light — "One small gold trophy cup on a base, with a black power cable and plug trailing from the base."

### 22 · forgetting on purpose (light wall)
- **22-T** · copper water-clock bowl · tone dark — "A nāḻikai vaṭṭil, a sinking-bowl water clock: one thin, hammered, hemispherical copper bowl with a tiny pinhole in the centre of its base, floating upright, half full, in a larger wide vessel of water. A little water has entered the small bowl through the hole. Three-quarter view from above, with the larger vessel cut away slightly at the front so the floating bowl is seen."
- **22-G** · gong · tone dark — "A flat round bronze gong hanging by a cord from a small wooden frame, with a padded mallet beside it."
- **22-N** · wristwatch · tone dark — "One plain round wristwatch, front view, with a completely blank dial, no numerals, no hands, leather strap laid flat above and below."
- **22-F1** · radio dish · tone dark · reuse: copies form the ring — "One large radio telescope dish on a lattice mount, tilted to point up and to the right, three-quarter view." (The script's FUTURE is a ring of dishes listening to pulsars; this one image, copied and scaled, makes the ring. The pulses are SVG dots.)
- **22-N2** · caesium fountain clock · tone dark · NOW, behind the watch — "A laboratory caesium fountain atomic clock, without any room around it: a tall slim vertical column of polished steel tubes, about three times as tall as it is wide, with a small spherical glass-windowed vacuum chamber near the base where six thin beams cross, a taller narrow vertical tube above it rising to a cylindrical cavity section near the top, a few thin cables and small optical fittings on short arms, standing on a compact square base. Front view, symmetric. No screens, no labels." (The script's NOW is the wristwatch counting 9,192,631,770, which is the caesium second; the fountain stands behind the watch as the instrument that defines that count. The count is SVG.)
- **22-F2** · sikku kolam · tone dark · view straight down · reuse: 25 — "Top-down view of a cikku kōlam drawn in white rice flour. A neat grid of small white dots, 5 by 5. One single continuous white line loops and curves around the dots in a symmetric interlaced pattern, passing between the dots and around them without ever touching a dot, closing on itself. Slightly uneven hand-drawn line of powder. White only: no colour, no flowers, no filled shapes." (Use as texture and as the still frame; the drawn line stays SVG from `kolam_path()`.)

### 23 · the spread (dark wall)
- No new objects. **01-T2** fanned, then an SVG spread. Thumbnails are the THEN and FUTURE images of each category, scaled down: 02-T/02-N, 04-T/04-F2, 05-T/05-F, 06-T, 07-T/07-F, 09 flats, 13-T/13-F, 16-T, 17-T, 18-T/18-F, 01-F, 21-T, 22-T/22-F2.

### 24 · steer (light wall)
- **24-T** · coracle · tone dark — "A paricāl, a round South Indian river coracle: a shallow circular bowl-shaped boat about two metres across, woven of split bamboo in a basket weave, the outside covered with a dark tarred skin, a thick rim, and one short wooden paddle lying across it. Empty. Three-quarter view from above."
- **24-N** · steering wheel · tone dark — "One plain car steering wheel, front view, with a blank centre and no logo."

### 25 · look up (dark wall)
- **25-N** · circuit board · tone light · view straight down — "Top-down view of a square circuit board with a 5 by 5 grid of round solder pads and copper traces that run between the pads in right-angled paths without crossing the pads. No components, no markings."
- **25-F** · star grid · tone light · view straight down · Veo end frame for V3 — "Twenty-five small four-pointed stars in chalk white and turmeric, set in exactly the same 5 by 5 grid positions as the kolam dots, joined by one thin continuous pale-gold line that loops between them without touching any star, on a small square of night-indigo sky with soft edges." (In the reel the stars and route are SVG; this image exists so V3 has an end frame.)
- (THEN is **22-F2**, which is also the start frame of clip V3.)

### 26 · the work of the wind (light wall)
- **26-T** · stitched-plank ship, a likely form · tone dark — "A reconstruction of an ancient Indian Ocean sewn-plank trading ship, a nāvāy, side view sailing to the right. A double-ended wooden hull whose planks are joined edge to edge by stitching: rows of coir cord in a criss-cross pattern clearly visible along every seam, with no iron nails. One mast with one large square sail of woven matting or cotton, filled by the wind from behind. One long steering oar at the stern quarter. Sacks of pepper stacked amidships. No cannons, no flags, no cabin, no second mast."
- **26-T2** · pepper sack · tone dark — "One plump jute sack tied at the neck, with a few black peppercorns spilled at its foot."
- **26-T3** · papyrus sliver · tone dark · reuse: all three stages — "One small torn rectangular fragment of papyrus with a visible criss-cross fibre texture and frayed edges, with a few rows of faint illegible ink marks."
- **26-N** · container ship · tone dark — "A modern container ship in side view sailing to the right: a long low hull, the bridge tower near the stern, and containers stacked in even blocks along the deck, in laterite, teal and indigo. No names, no logos."
- **26-N2** · one container · tone dark — "One steel shipping container, corrugated sides, doors closed, three-quarter view. No markings."
- **26-F** · solar light-sail · tone dark — "A solar sail spacecraft: one enormous, perfectly square sail of mirror-thin reflective foil, slightly wrinkled, held taut by four slender diagonal booms that meet at a tiny central hub with a small cargo pod. Seen at an angle so the square reads as a diamond. The foil reflects warm turmeric light." (Foil must not pick up the green background; see notes.)

### 27 · the atom only divine eyes see (dark wall)
- **27-T** · sesame seed · tone light — "Extreme macro of one single pale sesame seed, teardrop shaped, and beside it the same seed cut cleanly in half."
- **27-N** · the microscope tip · tone light — "Scientific illustration of a scanning tunnelling microscope tip: a single sharp metal needle coming down from the top of the frame, ending in one atom, hovering just above a flat surface made of rows of soft round bumps like a tray of marbles. A few bumps sit raised above the rest. Painted, not a micrograph." (The letter in atoms is SVG.)
- **27-F1** · dilution refrigerator · tone light — "The inside of a dilution refrigerator for a quantum computer, without its outer shell, hanging from the top of the frame like a chandelier: a vertical stack of five round gold-plated metal plates, each plate smaller than the one above it, joined by thin vertical rods, with bundles of fine coiled cables running down between the plates, and a small square chip mount at the very bottom. Front view."
- **27-F2** · slate · tone light — "A small rectangular writing slate in a wooden frame, hanging from a nail by a string, blank, with one faint vertical chalk line dividing it into two columns and a stub of chalk on a string."

### 28 · Pambatti's boast (light wall)
- **28-T1** · the snake basket · tone dark — "A round, squat, lidded snake charmer's basket woven of cane in a coiled pattern, with its flat round lid resting half off."
- **28-T2** · the cobra · tone dark — "An Indian spectacled cobra rising upright from a coil, front view, hood fully spread, showing the spectacle mark on the back of the hood faintly through it, tongue out. Calm, not striking."
- **28-T3** · the gourd pipe · tone dark — "A makuṭi, a snake charmer's pipe: a dried bulbous gourd in the middle, a short blowing tube above it, and two thin reed pipes side by side below it, bound with thread and beeswax."
- **28-N** · flask with a folded ribbon · tone dark · reuse: copies form the row — "One round-bottomed glass laboratory flask, a third full of clear liquid, and floating inside it a single ribbon folded and twisted into a loose knot, like a diagram of a protein. No label."

### 29 · mind froths up (dark wall)
- **29-T** · the fermenting pot · tone light — "A round, wide-mouthed clay pot holding a dark liquid, with small red-orange dhataki flowers floating on it and a broken lump of brown jaggery resting on the rim. A head of pale froth is beginning to rise, and a few bubbles sit at the surface."
- **29-N** · the layered network · tone light — "A diagram-like object: four thin translucent rectangular panes stacked one above another with gaps between, each pane dotted with a grid of small round nodes. No wires, no lights, no text." (The rising lights and the froth question marks are SVG.)

### 30 · the seventh rung (light wall)
- **30-N** · the sensor helmet · tone dark — "A lightweight wearable brain-scanning helmet, like a rigid cap studded all over with small square sensor blocks, each with a thin cable, the cables gathered into one bundle at the back. Empty, three-quarter view."
- **30-F** · the seventh rung · tone dark — "One single bamboo rung with fresh pale coir rope lashings at both ends, the rope ends still loose, as a separate piece."
- **30-S** · sandals — "A pair of flat leather sandals, left neatly side by side." 

### 31 · the lamp, and the ledger (dark wall)
- **31-T** · kuthuvilakku, unlit · tone light · HERO — "A kuttuviḷakku, a traditional Tamil standing oil lamp cast in the style of a Chola bronze, aged warm brass, about waist high. From the ground up: a wide round stepped base; a slender vertical stem with a series of rounded ring mouldings and one larger ball knob at its middle; at the top of the stem, ONE single shallow round oil dish with exactly FIVE short pointed spouts spaced evenly around its rim like a five-pointed star; one twisted cotton wick lying in each spout with its tip at the spout's lip; and rising from the centre of the dish, a short stalk carrying a small finial in the shape of a swan-like haṁsa bird. No flames. Straight, symmetric, front view from slightly above so that all five spouts can be seen." (Flames are **FL**, placed on the spout tips one at a time.)
- **31-N** · carbon-filament bulb · tone light — "An early glass light bulb, pear-shaped clear glass with a pointed tip at the top, a single looped carbon filament inside on two wires, a brass screw base. Unlit."
- **31-F1** · the small sun · tone light — "A perfect glowing sphere of turmeric and pale gold, like a small artificial sun, with soft painted surface swirls and a hard edge. No rays, no halo."
- **31-F2** · the town · tone light — "A small South Indian town as one cut-out cluster seen from a distance: low tiled-roof houses, a few palms, a temple gopuram, a water tower, all in silhouette with a few lit windows."
- **31-P** · taper — "One thin wax taper, unlit, with a blackened wick tip." (Usually redundant with **K8**; make only if the taper has to move alone.)

## 4. Reuse across scenes

| image | made for | reused in |
|---|---|---|
| K poses, M poses | section 2 | every scene |
| 01-F ledger leaf | 01 | the strip in all 31 scenes; 19 (the glossed leaf); 31 (unrolled) |
| 01-T / 01-T2 bundle | 01 | 23; thumbnails |
| 01-N phone | 01 | 06 (face up, and the wall of rectangles as a silhouette), 12 (held by the tape), 16 (rung six) |
| 01-P stylus | 01 | 27 (the blade end), any keeper prop |
| FL flame | 06 | 11 (cooking fire), 31 (each of five wicks, and the taper) |
| 06-T agal | 06 | 06 FUTURE; thumbnails |
| 07-E empty leaf | 07 | 07 row, 08 both rows and the last leaf |
| 09 flats (5) | 09 | 10 (shore), 11 (all five, pālai stretched) |
| 09-S map tile | 09 | 10 (the map with a legend) |
| 10-F drawer cabinet | 10 | 12 (the tower the machine climbs) |
| 04-F2 ēri tank | 04 | 12 (the tank below; lotus leaf and kingfisher sit on it) |
| 04-F3 temple tank | 04 (alternate) | 12 (alternate tank), 23 thumbnail |
| 31-T, 01-T, 01-F, 02-T, 26-T, 22-F2 | their scenes | first or last frames of clips V1 to V5 |
| 31-N, 31-F1, 01-N, 26-N, 26-F, 25-N, 02-N | their scenes | middle references and last frames of the clips |
| 25-F star grid | 25 | clip V3 only |
| 12-F1 climbing machine | 12 | 30 (second machine in the queue) |
| 13-F wrist band | 13 | 15 |
| 15-T2 stool | 15 | 21 (ten stools) |
| 16-T ladder, 16-C creatures | 16 | 30 |
| 16-C4 ant | 16 | 22 (ants carrying off the kolam) |
| 16-F phone with arm | 16 | 30 (first in the queue) |
| 18-N speaker | 18 | 20 (alternate to 20-F), 27 |
| 18-F kitchen shelf | 18 | 27 (the refrigerator goes in the empty middle) |
| 22-F2 sikku kolam | 22 | 25 |
| 29-T pot shape | 29 | the plain pot in 18-T can be cropped from it if 18-T's pot fails |
| P2 bard | 20 | 21 |

Reuse removes about 45 generations that a strict scene-by-stage list would need.

### 4.1 Stage map: which image plays each era stage

One separate image per stage. `SVG` means the stage is a motion graphic or text and is not generated. An ID in *italics* is a reuse of an image made for an earlier scene.

| scene | THEN | NOW | FUTURE |
|---|---|---|---|
| 01 | 01-T (closed), 01-P | 01-N | 01-F |
| 02 | 02-T, 02-H | 02-N | *02-N* empty, readout SVG |
| 03 | 03-T, 03-T2, 03-G | 03-N, receipt SVG | *03-N* again, a crack of light seam SVG across the glass (the opened-terminal still is dropped: it no longer matches the monolith) |
| 04 | 04-T | 04-N, 04-C | 04-F1, then 04-F2 (04-F3 alternate) |
| 05 | 05-T, 05-T2 | SVG bubbles | 05-F |
| 06 | 06-T + FL | *01-N* face up | *06-T* + *FL* |
| 07 | 07-T (07-T2 hero) | 07-N | 07-F |
| 08 | *07-E* x n, 08-T | score sheet SVG over *08-T* | 08-F, *07-E* x n |
| 09 | 09-K, 09-M, 09-R, 09-N, 09-P, 09-U | 09-S | *09 flats* |
| 10 | *09-N*, 10-H, 10-E, 10-L, 10-S, 10-D, 10-N | *09-S*, legend SVG | 10-F, *10-H* |
| 11 | *09 flats* | 11-N | 11-F1, 11-F2, 11-G |
| 12 | 12-T, P1 | 12-N1, 12-N2, 12-N3, *01-N* | 12-F1 on *10-F*; 12-F2, 12-K, 12-S on *04-F2* or *04-F3* |
| 13 | 13-T | 13-N | 13-F |
| 14 | 14-T | 14-N, sliders SVG | 14-F |
| 15 | 15-T1, 15-T2, 15-T3, 15-T4 | 15-N1, 15-N2, 15-N3 | *15-N1*, *15-N2*, *13-F*, *K6* or *P1* in the chair |
| 16 | 16-T, 16-C1 to 16-C7 | *01-N* on rung six | 16-F |
| 17 | 17-T | 17-N, trace and dial SVG | 17-F + *17-N*, then *17-T* again |
| 18 | 18-T, 18-G | 18-N, queue of *P1*/*P4* | 18-F + *18-N* |
| 19 | 19-T | document SVG, 19-N | twins SVG |
| 20 | *P2* | 20-N | 20-F |
| 21 | 21-T | 21-N1, 21-N2 | 21-F, *15-T2* x 10, *P2* |
| 22 | 22-T, 22-G | 22-N, 22-N2 | 22-F1 x n, 22-F2, *16-C4* |
| 23 | *01-T2* | spread SVG | thumbnails of THEN and FUTURE images |
| 24 | 24-T | 24-N | *24-T* + *K9* |
| 25 | *22-F2* | 25-N | stars SVG (25-F for clip V3 only) |
| 26 | 26-T, 26-T2, 26-T3 | 26-N, 26-N2, *26-T3* | 26-F, *26-T3* |
| 27 | 27-T, *01-P* | 27-N | 27-F1, *18-F*, 27-F2 |
| 28 | 28-T1, 28-T2, 28-T3, P3 | 28-N x n, map SVG | *28-T1*, *28-T2* |
| 29 | 29-T | 29-N, lights SVG | *29-T*, *29-N*, *K6* |
| 30 | *16-T* | 30-N, chart SVG | 30-F, *16-F*, *12-F1*, *M1*, 30-S |
| 31 | 31-T + FL | 31-N | 31-F1, 31-F2, *K8*, *FL* on each wick |

## 5. Veo clips (five hero transformations)

These are made in Flow with Veo, from the approved stills, after those stills exist. They replace the SVG morph in five scenes; elsewhere the morph stays a cross-fade of stills.

**Rules for every clip.**
- **Frames to video.** Use Flow's start-and-end-frame mode: the THEN still is the first frame and the FUTURE still is the last frame, so the clip begins and ends on images that match the rest of the reel. The prompt describes the NOW stage in the middle.
- **Aspect.** If Flow does not offer 1:1 video, generate 16:9: place each square still in the centre of a 16:9 canvas of pure `#00FF00` before using it as a frame, keep all motion inside that centre square, and crop the result to 1:1.
- **Length.** 4 to 6 seconds of morph. If Flow returns a longer clip, the prompt asks for the object to hold still after the morph, and the tail is trimmed.
- **Locked.** Camera locked off; background constant `#00FF00`; one object, centred, never leaving the frame; one continuous transformation with no cut; no text. Veo may add sound: the prompt asks for none, and the clip is muted in any case.
- **Keying.** Key the clip with the same settings as the stills. Fast motion leaves green fringes; the prompt asks for slow, even motion and no motion blur.

**Shared tail (append to every clip prompt, 55 words):**
> Static locked-off camera, no camera movement, no zoom, no cuts. Flat solid pure chroma green #00FF00 background that never changes. Hand-painted gouache cut-out look with paper grain kept in every frame, soft key light from upper left, gentle contact shadow. Slow, even, continuous motion, no motion blur. No text, no letters, no people, no sound.

**V1 · kuthuvilakku → bulb → sun** (scene 31, 5 s) · first frame: 31-T with FL composited on the front spout · last frame: 31-F1 · middle reference: 31-N
> A brass kuthuvilakku standing lamp with one small lit wick transforms in one smooth continuous morph. The stem, base and five-spouted dish draw upward and inward around the single flame until the flame sits inside a pear-shaped clear glass bulb with a looped carbon filament glowing turmeric-gold on a brass screw base. Then the bulb swells and rounds into a perfect glowing sphere of turmeric and pale gold with soft painted swirls and a hard edge, a small sun, which hangs still in the centre. No smoke, no sparks, no halo spilling onto the background.

**V2 · stitched-plank ship → container ship → light-sail** (scene 26, 6 s) · first frame: 26-T scaled to about half the frame width · last frame: 26-F · middle reference: 26-N
> An ancient sewn-plank wooden trading ship with one square sail, sailing to the right, transforms in one smooth continuous morph. The hull stretches long and low into a modern container ship, the pepper sacks square off into stacked steel containers, the mast and sail fold down into a bridge tower. Then the containers open flat like boxes unfolding, tile edge to edge, and lift and spread into one enormous square sail of thin reflective foil held by four slender diagonal booms, turning to show it as a diamond, reflecting warm turmeric light. No water, no waves, no sky, no green reflections in the foil.

**V3 · kolam dots → circuit pads → stars** (scene 25, 5 s, top-down) · first frame: 22-F2 · last frame: 25-F · middle reference: 25-N
> Seen straight down. A white rice-flour sikku kolam, a 5 by 5 grid of dots with one continuous line looping around them, transforms in one smooth continuous morph. The swept earth under it darkens into a deep teal circuit board, each flour dot hardens into a round copper solder pad in the same position, and the looping line squares off into right-angled copper traces. Then the board deepens into night indigo, the pads brighten into small four-pointed white and turmeric stars, and the traces soften back into one thin pale-gold curving route between them. The grid never moves.

**V4 · palm leaf → phone → glowing leaf** (scene 01, 6 s) · first frame: 01-T · last frame: 01-F · middle reference: 01-N
> A closed Tamil palm-leaf manuscript bundle, long narrow tan leaves between two wooden boards tied with a cotton cord, transforms in one smooth continuous morph. The leaves square up and fuse into a thin dark smartphone standing upright with a blank screen, and the cord becomes its charging cable. Then the phone thins, lengthens and warms in colour into one single long palm-leaf strip standing upright, tan, with two string holes and faint blank ruled lines, glowing softly from within, and the cable is gone. No writing, no icons, no logo.

**V5 · tharasu → laboratory balance** (scene 02, 4 s) · first frame: 02-T · last frame: 02-N
> A hand-held Tamil two-pan balance, a wooden beam with a pointer tongue and two brass pans on three cords each, hanging level, transforms in one smooth continuous morph. The pans draw inward and flatten into one round steel weighing pan, the cords stiffen and turn into the clear glass walls of a draft-shield box, and the beam sinks and squares into the low base of a modern laboratory analytical balance with a small blank display. Nothing on the pan. No hand, no numbers.

## 6. Priority order

### 6.1 The first 12 images (characters first, then hero objects)

1. **K0** keeper character sheet
2. **M0** myna character sheet
3. **K3** keeper writing (scene 01 and every ledger line)
4. **M6** myna perched (its default pose)
5. **31-T** kuthuvilakku (the close; the style reference for every object after it; V1 first frame)
6. **01-T** palm-leaf manuscript bundle (the opening; V4 first frame)
7. **01-F** the ledger leaf (on screen in all 31 scenes; V4 last frame)
8. **02-T** tharasu (the first full morph; V5 first frame)
9. **26-T** stitched-plank ship (the widest morph; V2 first frame)
10. **22-F2** sikku kolam (22 and 25; V3 first frame)
11. **07-T** banana leaf with the meal (with 07-E as its edit, covers 07 and 08)
12. **04-T** Roman coin hoard in the clay pot

### 6.2 Then the clips

Each clip needs its partner stills first (9 images): **FL**, **31-N**, **31-F1** for V1; **01-N** for V4; **26-N**, **26-F** for V2; **25-N**, **25-F** for V3; **02-N** for V5. Then the clips in this order: **V1**, **V4**, **V2**, **V3**, **V5**.

### 6.3 Then the rest

- **The rest of the cast (10):** K1, K2, K4, K5, K6, M1, M2, M3, M4, M5.
- **Hero objects of the other scenes (14):** 16-T, 06-T, 21-T, 22-T, 24-T, 12-N1, 12-F2, 12-K, 12-S, 27-F1, 18-T, 07-T2, 22-N2, 04-F3.
- **NOW and FUTURE partners of objects already made (16):** 01-T2, 01-P, 02-H, 03-T, 03-T2, 03-G, 03-N, 03-F, 04-C, 04-N, 04-F1, 04-F2, 07-E, 07-N, 07-F, 22-F1.
- **Everything else, by scene number (80),** with the five 09 flats made in one sitting so they match: 05-T, 05-T2, 05-F, 08-T, 08-F, 09-K, 09-M, 09-R, 09-N, 09-P, 09-S, 09-U, 10-H, 10-E, 10-L, 10-S, 10-D, 10-N, 10-F, 11-N, 11-F1, 11-F2, 11-G, 12-T, 12-N2, 12-N3, 12-F1, 13-T, 13-N, 13-F, 14-T, 14-F, 14-N, 15-T1, 15-T2, 15-T3, 15-T4, 15-N1, 15-N2, 15-N3, 16-C1, 16-C2, 16-C3, 16-C4, 16-C5, 16-C6, 16-C7, 16-F, 17-T, 17-N, 17-F, 18-N, 18-F, 18-G, 19-T, 19-N, 20-N, 20-F, 21-F, 21-N1, 21-N2, 22-G, 22-N, 24-N, 26-T2, 26-T3, 26-N2, 27-T, 27-N, 27-F2, 28-T1, 28-T2, 28-T3, 28-N, 29-T, 29-N, 30-N, 30-F, 30-S, 31-F2.
- **Last (13):** extra poses K7 to K10 and M7 to M10, supporting people P1 to P4, and 31-P.

## 7. Count

| group | images |
|---|---|
| character sheets (K0, M0) | 2 |
| core poses, 6 each | 12 |
| extra poses, 4 each | 8 |
| supporting people | 4 |
| objects, scenes 01 to 31 | 128 |
| **total stills** | **154** |
| Veo clips | 5 |
| **total generations, before retakes** | **159** |

By wave: 12 first, 9 clip frames, 5 clips, 10 cast, 14 hero, 16 partners, 80 by scene, 13 last. Check with `grep -cE '^- \*\*[A-Z0-9]+(-[A-Z0-9]+)?\*\*' site/nilai/v3_shotlist.md` (154). Plan on two or three retakes per hero image and per clip.

## 8. Accuracy notes: what the model gets wrong, and what to say

**Common myna.** The model drifts to a hill myna (all black, orange bill, yellow wattles on the nape), a starling (spotted, iridescent) or a crested myna. Say: chocolate-brown body, black hood, bare yellow skin behind and below the eye and no wattles, yellow bill and legs, no crest, no spots. The white wing patch is a small sliver when the bird is perched and a large panel when it flies; if a perched bird comes back with a broad white stripe across the wing, regenerate. The white wing patch and white tail tip are also the reason the background is green.

**Kuthuvilakku.** The usual failures: several stacked dishes (that is a Kerala tiered lamp or a temple dīpastambha); candles or candle cups; a menorah or candelabra with arms; flames in the middle of the dish; four, six or seven spouts; a peacock with a fanned tail in place of the small haṁsa. The script's lamp has one dish, five spouts and a bird finial. The "tiers" are the ring mouldings on the stem and the steps of the base. Count the spouts on every result. Generate it unlit and add **FL** on the spout tips, so that wicks can be lit one, two, three in scene 31 and the first flame stays the same size. The script says brass; "Chola bronze style" is used for the casting and the mouldings only.

**Banana leaf.** The script commits to the narrow tip at the eater's left, a pinch of salt at the top corner and a rice mound in the middle. **07-T2** adds the common Tamil order: salt top left, pickle beside it, the vegetable dishes in a row along the upper half from left to right, appalam and vadai top right, banana and sweet lower left by the tip, rice with dal and ghee in the lower centre. That order varies by household and region, so the image is never labelled. The model's habits: it puts the rice dead centre on the midrib (it belongs below the midrib, on the eater's side), puts salt at the top right, scatters dishes over the lower half, and serves curries in steel cups. Failures to reject: the leaf vertical or diagonal; the tip on the right; a whole leaf with two pointed ends (it should be a tip section with one cut edge); steel bowls, cups, a thali plate, cutlery; flatbreads and gravies in bowls; a bright lime leaf that will key out with the background. State "the eater sits at the bottom edge of the image", or left and right are ambiguous.

**Green subjects on a green screen.** Banana leaf, lotus leaf, lily pad, grass, trees: always add "deep, dull peacock teal-green, never bright lime". Check the key before accepting. If a subject still breaks up, cut it by hand; do not switch the background for one image, because mixed backgrounds give mixed edge colours.

**Reflective and transparent subjects** (light-sail foil, glass bulb, flask, balance case, water beads, the smart ring) pick up the green. Add: "reflections are warm turmeric and chalk white only; no green reflections; glass is painted as opaque pale paint with a highlight, not as true transparency."

**Palm-leaf manuscript.** Failures: a bound codex or a scroll; leaves as wide as paper; ink writing with a brush. Say: long narrow strips, two string holes, a cord, two wooden boards, letters incised. Keep any writing as illegible marks, since the model will otherwise invent pseudo-Tamil.

**Tharasu.** Failures: a justice-statue scale with chains on a pedestal, or a steelyard. Say: hand-held, wooden beam, pointer tongue in a fork, three cords to each pan, loop on top, no stand. Pans must be level, because the scene is about the beam levelling first.

**Roman coins.** Failures: modern milled edges, legible fake Latin, coins of identical perfect circles. Say: hand-struck, irregular, lettering worn to ticks. No particular hoard is depicted.

**Ēri versus temple tank.** The script's scene 04 is a village irrigation tank with an earthen bund and a stone sluice, not a stepped temple tank. The model defaults to a stepwell from western India (deep, geometric, many flights). If the stepped alternate is used, say "South Indian temple tank, a square pool at ground level with a centre pavilion", and never "stepwell".

**Yāḻ and nāvāy.** Both are "drawn as a likely form", and the reel says so on screen. For the yāḻ reject a European pillar harp, a lyre, a veena or a peacock-shaped instrument, and do not assert a string count. For the ship reject a galleon, a lateen-rigged dhow, a Viking longship with shields, and visible nails; the stitching along the seams is the point.

**Gecko toe.** Failures: suction cups, round frog-like discs. Say: stacked thin horizontal ridges across a widened toe pad, and a claw.

**Kingfisher.** It is the white-throated kingfisher of Tamil tanks, not the small common kingfisher: big red bill, chestnut head and belly, white bib, turquoise back. No splash.

**Shinkansen.** The 500 series has the long pointed nose associated with the kingfisher story. Reject duck-billed later series and any livery text.

**Caesium fountain.** Failures: a glowing sci-fi tube, a wall clock, an hourglass. Say: a tall slim column of steel vacuum tubes on a base, a small spherical chamber low down where laser beams cross, a cavity section higher up, no screens. It is a laboratory instrument, plain and symmetric.

**Temple tank.** Failures: a western Indian stepwell sunk deep with zigzag flights, or a swimming pool. Say: square, at ground level, shallow even steps on all four sides, a small pillared maṇḍapam in the water.

**Dilution refrigerator.** Failures: a kitchen fridge, a sci-fi reactor. Say: hanging stack of gold plates, each smaller than the one above, with rods and coiled cables, like a chandelier, no outer can.

**Water-clock bowl.** Failures: an hourglass, a sundial, a clepsydra with a spout. Say: a small copper bowl with a pinhole floating inside a larger vessel.

**Sikku kolam.** Failures: a coloured rangoli, a mandala, flower petals, a line that runs through the dots. Say: white only, dots in a grid, one continuous line looping around the dots without touching them.

**Medicine scenes (13 to 15, 28).** The script forbids any ingredient, dose or preparation. The kalvam is empty and clean; no herbs, powders, minerals or vessels of medicine in any image.

**The stone (18).** The joke is on the machine and never on the worshipper. The naṭṭakal is plain and respectful: no face, no caricature.

**People.** The keeper is about fourteen, fully and practically dressed, in ordinary child-at-work poses. Supporting people are plain and dignified. No real person's likeness, no named living artist's style, and no reference to any other site's look in any prompt.

**Consistency checks before accepting any image:** light from the upper left (highlight on the left shoulder of the form); one soft shadow directly beneath and not cast far to one side; the whole subject inside the frame with green on all four sides; no text; palette within the nine colours.

**Veo clips.** Failures: the camera drifts or zooms; the background shifts from pure green or picks up a floor and a horizon; the object leaves the frame; the morph becomes a cross-fade or a cut instead of one shape changing; extra objects appear midway; the paint look turns into a glossy 3D render in the middle frames; gibberish text appears on the phone screen, the container sides or the balance display. Reject any clip whose first and last frames do not match the stills, since the reel cuts to and from those stills. If the middle stage comes out wrong, run the clip as two halves (THEN to NOW, NOW to FUTURE) with the NOW still as the shared frame, and join them on that frame.

