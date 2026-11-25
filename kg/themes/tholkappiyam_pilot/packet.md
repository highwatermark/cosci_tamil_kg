# Tholkappiyam pilot: blind re-tagging packet

You are the second, independent tagger in a pilot that tests Tholkappiyam's theory of meaning as a
tagging frame. Tag each of the 100 verses below by the brief `docs/tholkappiyam-tagging-brief.md`
(read it in full first; the sutras it cites are in `kg/core/tholkappiyam.jsonl`). Do not open
`kg/themes/tholkappiyam_pilot/tags_A.json` or `findings.md`: the point is agreement between two
taggers who have not seen each other's tags.

Read the Tamil first. The marked reading is given to help with hard words. For the Tirumanthiram,
the Thiruppugazh and the Siddhar songs it was written by a Claude agent and is a claim to check, not
evidence. The Kural and Naladiyar readings rest on the commentaries; Pope's gloss is given where
the corpus has it.

Write `kg/themes/tholkappiyam_pilot/tags_B.json`: a JSON array of 100 objects in the order below,
each with `id`, `book` and every field of the brief. Then run
`python3 -I scripts/tholkappiyam_agreement.py` to score agreement.

The sample: 20 verses per book, drawn with one `random.Random(7)` over the books in the order kural,
naladiyar, tirumanthiram, thiruppugazh, siddhar, each book's Verse ids sorted by number and
`rng.sample(ids, 20)`, then sorted by number. Siddhar ids are `siddhar:N` where N is the seq.


## kural

### kural:77

என்பி லதனை வெயில்போலக் காயுமே  
அன்பி லதனை அறம்  

Marked reading: Virtue burns what has no love, as the sun burns what has no bones.

Pope: So loveless beings virtue's power to nothing brings.

### kural:99

இன்சொல் இனிதீன்றல் காண்பான் எவன்கொலோ  
வன்சொல் வழங்கு வது?  

Marked reading: Why would one who sees how sweetly sweet speech yields use harsh words?

Pope: Why does he use harsh words, who sees the pleasure which sweet speech yields ?

### kural:119

சொற்கோட்டம் இல்லது செப்பம் ஒருதலையா  
உட்கோட்டம் இன்மை பெறின்  

Marked reading: Rectitude is speech without bend, provided one surely has no bend within.

Pope: F reedom from obliquity of speech is rectitude, if there be (corresponding) freedom from bias of mind.

### kural:144

எனைத்துணையர் ஆயினும் என்னாம் தினைத்துணையும்  
தேரான் பிறனில் புகல்  

Marked reading: However great they are, what does it come to, when one enters another's home without weighing it even a millet's worth?

Pope: However great one may be, what does it avail if, without at all considering his guilt, he goes unto the wife of another ?

### kural:149

நலக்குரியார் யாரெனின் நாமநீர் வைப்பின்  
பிறர்க்குரியாள் தோள்தோயா தார்  

Marked reading: Who deserve good on this world ringed by the awesome sea? Those who don't touch the shoulders of a woman belonging to another.

Pope: Is it asked, "who are those who shall obtain good in this world surrounded by the terror-producing sea ?" Those who touch not the shoulder of her who belongs to another.

### kural:177

வேண்டற்க வெஃகியாம் ஆக்கம் விளைவயின்  
மாண்டற் கரிதாம் பயன்  

Marked reading: Don't seek gain that comes by coveting: when it ripens, its fruit is hard to make good.

Pope: Desire not the gain of covetousness. In the enjoyment of its fruits there is no glory.

### kural:186

பிறன்பழி கூறுவான் தன்பழி யுள்ளும்  
திறன்தெரிந்து கூறப் படும்  

Marked reading: One who talks of another's faults will have his own faults picked out and talked about.

Pope: The character of the faults of that man who publishes abroad the faults of others will be sought out and published.

### kural:193

நயனிலன் என்பது சொல்லும் பயனில  
பாரித் துரைக்கும் உரை  

Marked reading: Expansive talk about useless things itself declares that the speaker is one without நயன்.

Pope: That conversation in which a man utters forth useless things will say of him "he is without virtue."

### kural:309

உள்ளிய தெல்லாம் உடனெய்தும் உள்ளத்தால்  
உள்ளான் வெகுளி எனின்  

Marked reading: All one has thought of comes together at once, if one doesn't think of anger in the heart.

Pope: If a man never indulges anger in his heart, he will at once obtain whatever he has thought of.

### kural:440

காதல காதல் அறியாமை உய்க்கிற்பின்  
ஏதில ஏதிலார் நூல்  

Marked reading: If you can enjoy what you love without others knowing of the love, your enemies' schemes come to nothing.

Pope: If (a king) enjoys, privately the things which he desires, the designs of his enemies will be useless.

### kural:493

ஆற்றாரும் ஆற்றி அடுப இடனறிந்து  
போற்றார்கண் போற்றிச் செயின்  

Marked reading: Even those without strength become strong and win, if they know the place and act against foes while guarding themselves.

Pope: Even the powerless will become powerful and conquer, if they select a proper field (of action), and guard themselves, while they make war on their enemies.

### kural:664

சொல்லுதல் யார்க்கும் எளிய அரியவாம்  
சொல்லிய வண்ணம் செயல்  

Marked reading: Speaking is easy for anyone; doing as one has spoken is hard.

Pope: To say (how an act is to be performed) is (indeed) easy for any one; but far difficult it is to do according to what has been said.

### kural:749

முனைமுகத்து மாற்றலர் சாய வினைமுகத்து  
வீறெய்தி மாண்ட தரண்  

Marked reading: A fort gains its distinction from the actions by which its people bring down enemies as soon as battle begins.

Pope: A fort is that which derives excellence from the stratagems made (by its inmates) to defeat their enemies in the battlefield.

### kural:809

கெடாஅ வழிவந்த கேண்மையார் கேண்மை  
விடாஅர் விழையும் உலகு  

Marked reading: The world loves those who do not give up the friendship of friends whose bond has come down unbroken.

Pope: They will be loved by the world, who have not forsaken the friendship of those with whom they have kept up an unbroken long-standing intimacy.

### kural:857

மிகல்மேவல் மெய்ப்பொருள் காணார் இகல்மேவல்  
இன்னா அறிவி னவர்  

Marked reading: Those of bitter understanding who hold to hostility do not see the true thing that holds victory.

Pope: Those whose judgement brings misery through its connection with hatred cannot understand the triumphant nature of truth.

### kural:889

எட்பக வன்ன சிறுமைத்தே ஆயினும்  
உட்பகை உள்ளதாங் கேடு  

Marked reading: Though only as small as a split sesame seed, inner enmity has ruin within it.

Pope: Although internal hatred be as small as the fragment of the sesamum (seed), still does destruction dwell in it.

### kural:1040

இலமென்று அசைஇ இருப்பாரைக் காணின்  
நிலமென்னும் நல்லாள் நகும்  

Marked reading: Seeing those who say 'we have nothing' and sit idle, the good woman called Land laughs.

Pope: The maiden, Earth, will laug h at the sight of those who plead poverty and lead an idle life.

### kural:1098

அசையியற்கு உண்டாண்டோ ர் ஏஎர்யான் நோக்கப்  
பசையினள் பைய நகும்  

Marked reading: The man says that when he looks, she softens and smiles gently, and there is something special about the swaying woman at that moment.

Pope: When I look, the pitying maid looks in return and smiles gently; and that is a comforting sign for me.

### kural:1129

இமைப்பின் கரப்பாக்கு அறிவல் அனைத்திற்கே  
ஏதிலர் என்னும் இவ் வூர்  

Marked reading: The woman says she won't blink, knowing he would be hidden, and for this much the town calls him loveless.

Pope: I will not wink, knowing that if I did, my lover would hide himself; and for this reason, this town says, he is unloving.

### kural:1194

வீழப் படுவார் கெழீஇயிலர் தாம்வீழ்வார்  
வீழப் படாஅர் எனின்  

Marked reading: The woman says that those who are esteemed are still without something, if they aren't loved by the one they love.

Pope: Even those who are esteemed (by other women) are devoid of excellence, if they are not loved by their beloved.


## naladiyar

### naladiyar:24

சென்றே எறிப ஒருகால் சிறுவரை  
நின்றே எறிப பறையினை - நன்றேகாண்  
முக்காலைக் கொட்டினுள் மூடித்தீக் கொண்டுஎழுவர்  
செத்தாரைச் சாவார் சுமந்து.  

Marked reading: The drummers beat once on arrival, wait a little and beat again, and at the third beat the corpse is covered and the fire taken up; the dying carry the dead.

Pope: They march and then strike once! A little while they wait, then strike the drum a second time. Behold, how fine! The third stroke sounds. They veil it, take the fire, and go forth :—the dying bear the deed!

### naladiyar:26

நார்த்தொடுத் தீர்க்கிலென் நன்றாய்ந் தடக்கிலென்  
பார்த்துழிப் பெய்யிலென் பல்லோர் பழிக்கிலென்  
தோற்பையுள் நின்று தொழிலறச் செய்தூடும்  
கூத்தன் புறப்பட்டக் கால்.  

Marked reading: Once the dancer who stayed in this skin bag and did its work has left, what does it matter whether the body is dragged off with a rope, buried with care, thrown anywhere or reviled by many?

Pope: When the 'soul', that, taking its stand in this skin clad frame, has fully wrought its works, and partaken of life's experiences, has gone forth, what matters it whether you attach ropes to the body and drag it away, or carefully bury it, or throw it aside in any place you light upon, or if many revile the departed ?

### naladiyar:31

அகத்தாரே வாழ்வார்என் றண்ணாந்து நோக்கிப்  
புகத்தாம் பெறாஅர் பறங்கடை பற்றி  
மிகத்தாம் வருந்தி இருப்பரே மேலைத்  
தவத்தால் தவம்செய்யா தார்.  

Marked reading: Those who, on the strength of earlier austerity, do no austerity now will look up at a house and say 'those inside are the ones who live', unable to enter, clinging to the outer door and grieving.

Pope: ‘Yet those within are blest,' so saying, they look up, but obtain no entrance: their place is at the outer gate. There will they suffer much, who thro' lack of former penitence do no penance now. [In a former state penance won for them a human shape. As men they have now failed.]

### naladiyar:32

ஆவாம்நாம் ஆக்கம் நசைஇ அறமறந்து  
போவாம்நாம் என்னாப் புலைநெஞ்சே - ஓவாது  
நின்றுஞற்றி வாழ்தி எனினும்நின் வாழ்நாள்கள்  
சென்றன செய்வ துரை.  

Marked reading: Base heart, which says 'let us prosper, desiring wealth and forgetting virtue', even if you live on toiling without rest, your days are gone: tell me what you will do.

Pope: Say not, O silly soul, we will live desiring wealth and die forgetting virtue! We'll say that ceaselessly toiling thou shalt live long; but tell me, what wilt thou do when all thy happy days are over?

### naladiyar:64

நேர்த்து நிகரல்லார் நீரல்ல சொல்லியக்கால்  
வேர்த்து வெகுளார் விழுமியோர் - ஓர்த்ததனை  
உள்ளத்தான் உள்ளி உரைத்துராய் ஊர்கேட்பத்  
துள்ளித்தூண் முட்டுமாம் கீழ்.  

Marked reading: The excellent do not grow hot with anger when people beneath them confront them with unfit words; the base brood on it, rant for the town to hear, leap about and butt a pillar.

Pope: When men who are beneath them confront them, and speak unseemly words, the excellent wax not hot with anger. The base man will brood over it, chafe and rave for all the town to hear, and leap, and dash his head against a post.

### naladiyar:69

உபகாரம் செய்ததனை ஓராதே தங்கண்  
அபகாரம் ஆற்றச் செயினும் - உபகாரம்  
தாம்செய்வ தல்லால் தவற்றினால் தீங்கூக்கல்  
வான்தோய் குடிப்பிறந்தார்க் கில்.  

Marked reading: Even when people forget the help they received and do great harm, those born in families whose fame touches the sky only keep doing good, and do not seek to repay the fault with harm.

Pope: Though men think not of good received, and do much ill to men of family whose fame has touched the sky, these still do good; nor are they wont provoked by faults, to render evil to the thankless ones.

### naladiyar:74

அறிவ தறிந்தடங்கி அஞ்சுவ தஞ்சி  
உறுவ துலகுவப்பச் செய்து - பெறுவதனால்  
இன்புற்று வாழும் இயல்பினார் எஞ்ஞான்றும்  
துன்புற்று வாழ்தல் அரிது.  

Marked reading: Those who know what must be known, keep restraint, fear what must be feared, do what is due so that the world rejoices, and live content with what they get, are hardly ever in suffering.

Pope: Those who know what should be known and rule themselves thereby; who fear what should be feared ; who use all their faculties to bless the world; and whose nature rejoices in all good gained: are for ever free from woes.

### naladiyar:114

விடுவிலா வையத்து மன்னிய மூன்றில்  
நடுவண தெய்த இருதலையும் எய்தும்  
நடுவண தெய்தாதான் எய்தும் உலைப்பெய்து  
அடுவது போலும் துயர்.  

Marked reading: Of the three that endure in this world, whoever gains the middle one gains both ends as well; whoever does not gains a suffering like being boiled in a furnace.

Pope: Of the three things that endure upon this faultless earth, he who gains the midmost gains the two extremes also. He who gains not the midmost gains the cruel smart that the turtle feels when put into the pot to boil.

### naladiyar:115

நல்லாவின் கன்றாயின் நாகும் விலைபெறூஉம்  
கல்லாரே யாயினும் செல்வர்வாய்ச் சொற்செல்லும்  
புல்லீரப் போழ்தின் உழவேபோல் மீதாடிச்  
செல்லாவாம் நல்கூர்ந்தார் சொல்.  

Marked reading: Even a young calf fetches a price if its mother is a good cow, and the words of the rich are accepted even if they are unlearned; the words of the poor glance off like a plough in barely moist soil.

Pope: A young heifer fetches a good price when it is the calf of a good cow; so the words of rich men though unlearned, pass current. Poor men's words, like the plough when moisture is scanty, merely graze the surface and are of no avail.

### naladiyar:149

செல்லா விடத்தும் குடிப்பிறந்தார் செய்வன  
செல்லிடத்தும் செய்யார் சிறியவர் - புல்வாய்  
பருமம் பொறுப்பினும் பாய்பரி மாபோல்  
பொருமுரண் ஆற்றுதல் இன்று.  

Marked reading: What the well-born do even when they cannot, the small will not do even when they can; an antelope may bear a saddle, but it cannot do battle like a leaping horse.

Pope: Men of mean descent, even when all goes well with them, will not perform the good deeds that the well-born will do, even when things do not go well with them. Though the antelope should bear a pillion, it rushes not to war like the prancing charger.

### naladiyar:204

உலகறியத் தீரக் கலப்பினும் நில்லா  
சிலபகலாம் சிற்றினத்தார் கேண்மை - நிலைதிரியா  
நிற்கும் பெரியோர் நெறியடைய நின்றனைத்தால்  
ஒற்கமி லாளர் தொடர்பு.  

Marked reading: The friendship of small-natured people does not last beyond a few days, even when they mingle so fully that the world knows it; the bond with those who never falter holds as steadily as the ascetics who keep to their path to the goal.

Pope: Though mingled in a complete intimacy so that all the world knows of it, the friendship of the little will last but little time. Connection with the firm unyielding men endures till the great one's path, who never swerve, is reached.

### naladiyar:215

கோட்டுப்பூப் போல மலர்ந்துபிற் கூம்பாது  
வேட்டதே வேட்டதாம் நட்பாட்சி - தோட்ட  
கயப்பூப்போல் முன்மலர்ந்து பிற்கூம்பு வாரை  
நயப்பாரும் நட்பாரும் இல்.  

Marked reading: The true conduct of friendship is to go on loving what it first loved, like a tree's flower that opens and doesn't close again; no one esteems or befriends those who open first and close later, like the flowers of a dug pond.

Pope: The use and wont of friendship is that, what once it has loved it loves always,— like the flower on the tree-branch which having once unfolded afterwards closes not; but who will esteem, or make friends of those who are like flowers on the surface of the excavated tank, which unfold and afterwards close themselves?

### naladiyar:218

நாய்க்கால் சிறுவிரல்போல் நன்கணிய ராயினும்  
ஈக்கால் துணையும் உதவாதார் நட்பென்னாம்?  
சேய்த்தானும் சென்று கொளல்வேண்டும், செய்விளைக்கும்  
வாய்க்கால் அனையார் தொடர்பு.  

Marked reading: What use is the friendship of those as close as the little toe on a dog's foot who give not even a fly's foot of help? Go even far to gain the bond of those who are like the channel that makes the field yield.

Pope: Of what value is the friendship of those who being very near like the little claw on a dog's leg, afford not help as much as a fly's foot? Though you go far to seek it, lay hold of the friendship of those who are like the water channel that causes the crops in the field to flourish.

### naladiyar:286

உள்கூர் பசியால் உழைநசைஇச் சென்றார்கட்கு  
உள்ளூ ரிருந்துமோன் றாற்றாதான் - உள்ளூர்  
இருந்துயிர் கொன்னே கழியாது தான்போய்  
விருந்தினன் ஆதலே நன்று.  

Marked reading: One who lives in his own village but can give nothing to those who come to him driven by hunger had better go away and be a guest somewhere than waste his life staying there.

Pope: Although he dwells within the village, and sees the poor draw nigh with hungry soul desiring aid, he yields them none : why then in the village does he vainly pass his days? It were better he went to be a guest himself !

### naladiyar:290

ஆர்த்த பொறிய அணிகிளர் வண்டினம்  
பூத்தொழி கொம்பின்மேல் செல்லாவாம் - நீர்த்தருவி  
தாழா உயர்சிறப்பின் தண்குன்ற நன்னாட  
வாழாதார்க் கில்லை தமர்.  

Marked reading: Lord of the cool, good hill land whose waterfalls never fail: the bright, humming, spotted bees do not go to the branch that has flowered and finished; those who have lost their prosperity have no kin.

Pope: The humming spotted beetle tribes all bright in hue gather not on the branch that has ceased to blow. Lord of the good cool hilly land, of high renown, whence bounteous streams flow down unceasingly—the unprosperous have no kin! --------------

### naladiyar:296

மல்லன்மா ஞாலத்து வாழ்பவ ருள்ளெல்லாம்  
செல்வ ரெனினும் கொடாதவர் நல்கூர்ந்தார்  
நல்கூர்ந்தக் கண்ணும் பெருமுத் தரையரே,  
செல்வரைச் சென்றிரவா தார்.  

Marked reading: Among all who live in this rich, wide world, those who do not give are poor even if they are rich; and those who, even in poverty, do not go and beg from the rich are the great Muttaraiyar.

Pope: Poor are the men that give not, even though deemed wealthiest of all that flourish on the teeming apple earth! They who even when they are poor seek not as suppliants wealthy men are 'Lords of the three mighty lands.'

### naladiyar:299

நச்சியார்க் கீயாமை நாணன்று நாணாளும்  
அச்சத்தால் நாணுதல் நாணன்றாம் - எச்சத்தின்  
மெல்லிய ராகித்தம் மேலாயார் செய்தது  
சொல்லா திருப்பது நாண்.  

Marked reading: Not giving to those who come wanting is no shame, and shrinking each day from fear is no shame; the shame, when one is reduced by want, is to leave unspoken what one's superiors did to one.

Pope: It is no shame (disgrace) not to (be able to give to those who desire it of us. The shrinking on account of fear (felt) day by day is not shame (modesty). But to become reduced in other ways, and not to [dare to] tell what injuries those who love us not have inflicted on us is shame (disgrace, or self-respect).

### naladiyar:300

கடமா தொலைச்சிய கானுறை வேங்கை  
இடம்வீழ்ந்த துண்ணா திறக்கும் - இடமுடைய  
வானகம் கையுறினும் வேண்டார் விழுமியோர்  
மானம் மழுங்க வரின்.  

Marked reading: The forest tiger that has killed a great beast will starve to death rather than eat it if it falls on its left; so the excellent would not want even wide heaven placed in their hands if it came at the dulling of their honour.

Pope: The jungle-haunting tiger that slays the wild cow, refuses to eat and passes by what has fallen (of itself) in its path (i. e. carrion); so the excellent, though the wide realms of heaven were within their reach, would not desire them, if to be obtained (only) by the loss of honour. --------------

### naladiyar:322

அவ்வியம் இல்லார் அறத்தா றுரைக்குங்கால்  
செவ்விய ரல்லார் செவிகொடுத்தும் கேட்கலார்  
கவ்வித்தோல் தின்னும் குணுங்கர்நாய் பாற்சோற்றின்  
செவ்விய கொளல்தேற்றா தாங்கு.  

Marked reading: When those free of crookedness explain the way of virtue, those not rightly disposed do not hear it even when they lend an ear, just as the tanner's dog that chews leather cannot take the taste of milk-rice.

Pope: When men of ungrudging soul declare the way of virtue, those who are not rightly disposed, although they give ear, hear not. Even so the currier's dog seizes on and devours leather, not appreciating the flavour of milk and rice.

### naladiyar:323

இமைக்கும் அளவிற்றம் இன்னுயிர்போம் மார்க்கம்  
எனைத்தானும் தாங்கண் டிருந்தும் - தினைத்துணையும்  
நன்றி புரிகல்லா நாணின் மடமாக்கள்  
பொன்றிலென் பொன்றாக்கா லென்?  

Marked reading: What does it matter whether they die or live, those dull and shameless people who see in every way that their dear life may leave in the blink of an eye, and still do not a millet grain's worth of good?

Pope: What matters it whether they live or die—the shameless stupid people who do no good, not even as much as a grain of millet, though they see by every species of example the way in which their life so sweet to them, passes away in the twinkling of an eye?


## tirumanthiram

### tirumanthiram:245

வேந்தன் உலகை மிகநன்று காப்பது  
வாய்ந்த மனிதர்கள் அவ்வழி யாநிற்பர்  
போந்திவ் வுலகைப் பிறர்க்கொள்ளத் தாங்கொள்ளப்  
பாய்ந்த புலியன்ன பாவகத் தானே.  

Marked reading: When the king guards the world well, worthy people follow the same path; but one who comes to seize the world, for others or for himself, has the evil nature of a pouncing tiger.

### tirumanthiram:258

திளைக்கும் வினைக்கடல் தீர்வுறு தோணி  
இளைப்பினை நீக்கும் இருவழி உண்டு  
கிளைக்கும் தனக்கும் அக் கேடில் புகழோன்  
விளைக்கும் தவமறம் மேற்றுணை யாமே.  

Marked reading: There are two ways that end weariness and are a boat across the surging sea of deeds: austerity and virtue, which the Lord of unfailing renown makes fruitful, are the highest support for oneself and one's kin.

### tirumanthiram:400

ஆகாய மாதி சதாசிவ ராதியென்  
போகாத சத்தியுட் போந்துடன் போந்தனர்  
மாகாய ஈசன் அரன்மால் பிரமனாம்  
ஆகாயம் பூமி காண அளித்தலே  

Marked reading: Space and the rest, and Sadasiva and the others, went out together within the unfailing Shakti: the great-bodied Isa, Hara, Mal and Brahma, so that space and earth are cared for.

### tirumanthiram:423

பதஞ்செய்யும் பாரும் பனிவரை எட்டும்  
உதஞ்செய்யும் ஏழ்கடல் ஓதம் முதலாங்  
குதஞ்செய்யும் அங்கி கொளுவியா காசம்  
விதஞ்செய்யும் நெஞ்சில் வியப்பில்லை தானே  

Marked reading: The earth that gives footing, the eight snowy mountains, the seven seas with their tides and all the rest, the fire takes hold of and burns, and space too; there is no wonder in the heart that knows it.

### tirumanthiram:483

கொண்டநல் வாயு இருவர்க்கும் ஒத்தெழில்  
கொண்ட குழவியுங் கோமள மாயிடுங்  
கொண்டநல் வாயு இருவர்க்குங் குழறிடில்  
கொண்டதும் இல்லையாங் கோள்வளை யாட்கே  

Marked reading: If the good breath rises evenly in both, the child conceived will be fair; if it falters in both, the bangled woman conceives nothing.

### tirumanthiram:741

உற்றறி வைந்தும் உணர்ந்தறி வாறேழுங்  
கற்றறி வெட்டுங் கலந்தறி வொன்பதும்  
பற்றிய பத்தும் பலவகை நாழிகை  
அற்ற தறியா தழிகின்ற வாறே  

Marked reading: Whatever people know by the five senses, by understanding, by learning and by mixing these, they perish without noticing the many naazhigai of their life being cut away.

### tirumanthiram:770

வைத்தகை சென்னியில் நேரிதாய்த் தோன்றிடில்  
உத்தம மிக்கிடில் ஓராறு தங்களா  
மத்த மிகுத்திட் டிரட்டிய தாயிடில்  
நித்தல் உயிர்க்கொரு திங்களில் ஓசையே  

Marked reading: If the hand placed on the head appears straight, the span is six months; if the sign is doubled in excess, it is one month, and a sound is heard daily by the life.

### tirumanthiram:844

பாரில்லை நீரில்லை பங்கயம் ஒன்றுண்டு  
தாரில்லை வேரில்லை தாமரை பூத்தது  
ஊரில்லை காணும் ஒளியது ஒன்றுண்டு  
கீழில்லை மேலில்லை கேள்வியிற் பூவே  

Marked reading: There is no earth and no water, yet there is a lotus; no stalk, no root, yet the lotus bloomed; there is no town, yet there is a light one sees; no below and no above: it is a flower in hearing.

### tirumanthiram:1528

இரவும் பகலும் இலாத இடத்தே  
குரவஞ் செய்கின்ற குழலியை உன்னி  
அரவஞ்செய் யாமல் அவளுடன் சேரப்  
பரிவொன்றி லாளும் பராபரை தானே.  

Marked reading: Thinking of her with flowing hair who makes fragrance in the place where there is neither night nor day, join her without a sound, and the Supreme, with no other care, will rule you.

### tirumanthiram:1790

நானிது தானென நின்றவன் நாடோ றும்  
ஊனிது தானுயிர் போலுணர் வானுளன்  
வானிரு மாமுகில் போற்பொழி வானுளன்  
நானிது அம்பர நாதனும் ஆமே.  

Marked reading: He who stood saying 'I am this' every day is there as the awareness within, as life in this flesh; he is there pouring like the great cloud of the sky; and I become the Lord of the space as well.

### tirumanthiram:2298

ஆனந்த தத்துவம் அண்டா சலத்தின்மேல்  
மேனிஐந்தாக வியாத்தம்முப் பத்தாறாய்க்  
தான்அந்த மில்லாத தத்துவம் ஆனவை  
ஈனமி லா அண்டத்து எண்மடங்கு ஆமே.  

Marked reading: Above the cosmic mountain the bliss tattva, with five bodies, pervades as the thirty-six; the endless tattvas it becomes are eightfold in the flawless egg.

### tirumanthiram:2479

மூன்றுள மாளிகை மூவர் இருப்பிடம்  
மூன்றினில் முப்பத் தாறும் உதிப்புள  
மூன்றினின் உள்ளே முளைத்தெழும் சோதியைக்  
காண்டலும் காயக் கணக்கற்ற வாறே.  

Marked reading: Three mansions are the seat of the three; in the three the thirty-six arise; on seeing the light that sprouts and rises within the three, the body's reckoning ceases.

### tirumanthiram:2508

அன்ன துரியமே ஆத்தும சுத்தியும்  
முன்னிய சாக்கிரா தீதத் துறுபுரி  
மன்னும் பரங்காட்சி யாவது உடனுற்றுத்  
தன்னின் வியாத்தி தனில்உப சாந்தமே.  

Marked reading: That turiya is the purifying of the soul; the state beyond waking that it reaches, the lasting vision of the Supreme that comes with it, and upasantam lie in the Lord's pervading of oneself.

### tirumanthiram:2559

கூடகில் லார்குரு வைத்த குறிகண்டு  
நாடகில் லார்நயம் பேசித் திரிவர்கள்  
பாடகில் லாரவன் செய்த பரிசறிந்  
தாடவல் லாரவர் பேறெது வாமே.  

Marked reading: Those who cannot join the mark the guru set, and do not seek it, wander about talking fine words; they cannot sing of what he gave, so what gain can they have beside those who know it and can dance?

### tirumanthiram:2576

பூரணி யாது புறம்பொன்றி லாமையின்  
பேரணி யாதது பேச்சொன்றி லாமையின்  
ஓரணை யாததுவொன்றுமி லாமையிற்  
காரண மின்றியே காட்டுந் தகைமைத்தே.  

Marked reading: It is not filled up, since nothing is outside it; it takes no name, since no speech reaches it; it joins nothing, since there is nothing else; without any cause it shows itself, such is its nature.

### tirumanthiram:2603

எய்துவ தெய்தா தொழிவ திதுவருள்  
உய்ய அருள்செய்தான் உத்தமன் சீர்நந்தி  
பொய்செய்புலன் நெறியொன்பதுந்தாட்கொளின்  
மெய்யென் புரவியை மேற்கொள்ள லாமே.  

Marked reading: What comes and what fails to come: this is grace; the excellent, glorious Nandi gave grace so that one may be saved; if one masters the nine paths of the lying senses, one can mount the horse called truth.

### tirumanthiram:2604

கைகலந் தானை கருத்தினுள் நந்தியை  
மெய்கலந் தான்தன்னை வேத முதல்வனைப்  
பொய்கலந் தார்முன் புகுதாப் புனிதனைப்  
பொய்யொழிந் தார்க்கே புகலிட மாமே  

Marked reading: The one who joined hands with me, Nandi in my thought, the one who mingled in truth, the first of the Veda, the pure one who does not enter before the false, is a refuge only to those who have cast off falsehood.

### tirumanthiram:2647

அந்தக் கருவை யருவை வினைசெய்தற்  
பந்தம் பணியச்சம் பல்பிறப் பும்வாட்டிச்  
சிந்தை திருத்தலுஞ் சேர்ந்தாரச் சோதனை  
சந்திக்கத் தற்பர மாகுஞ் சதுரர்க்கே.  

Marked reading: Wasting away that embryo and the formless, the bond of making deeds, fearful servitude and the many births, and setting the mind right: for the skilled who meet that test, it becomes the Supreme itself.

### tirumanthiram:2800

தீத்திரன் சோதி திகழ்ஒளி உள்ஒளி  
கூத்தனைக் கண்டஅக் கோமளக் கண்ணினள்  
மூர்த்திகள் மூவர் முதல்வன் இடைசெல்லப்  
பார்த்தனன் வேதங்கள் பாடினள் தானே.  

Marked reading: The fierce one's light, the shining light, the inner light: she of tender eyes who saw the Dancer, as the first of the three murtis went between, looked on and sang the Vedas.

### tirumanthiram:2881

கூப்பிடு கொள்ளாக் குறுநரி கொட்டகத்து  
ஆப்பிடு பாசத்தை அங்கியுள் வைத்திட்டு  
நாட்பட நின்று நலம்புகுந்து ஆயிழை  
ஏற்பட இல்லத்து இனிதிருந்தானே.  

Marked reading: Placing in the fire the wedging noose for the little jackal in the shed that won't come when called, standing long and entering into good, he lived sweetly in the house with the jewelled woman.


## thiruppugazh

### thiruppugazh:168

திமிர வுததி யனைய நரக  
செனன மதனில் … விடுவாயேல்  
செவிடு குருடு வடிவு குறைவு  
சிறிது மிடியு … மணுகாதே  
அமரர் வடிவு மதிக குலமு  
மறிவு நிறையும் … வரவேநின்  
அருள தருளி யெனையு மனதோ  
டடிமை கொளவும் … வரவேணும்  
சமர முகவெ லசுரர் தமது  
தலைக ளுருள … மிகவேநீள்  
சலதி யலற நெடிய பதலை  
தகர அயிலை … விடுவோனே  
வெமர வணையி லினிது துயிலும்  
விழிகள் நளினன் … மருகோனே  
மிடறு கரியர் குமர பழநி  
விரவு மமரர் … பெருமாளே.  

Marked reading: The poet asks that if Murugan leaves him in birth, which is like a dark sea of hell, he not be deaf, blind, deformed or the least poor, but have a fine form, high family, knowledge and fullness, and that Murugan give his grace and come to take him, mind and all, into service. The praise names the vel that made the asuras' heads roll, the sea wail and the mountain break, Vishnu on the serpent bed as uncle and the dark-throated Siva as father, at Palani.

### thiruppugazh:370

துகிலு ம்ருகமத பரிமள அளகமு  
நெகிழ இருதன கிரியசை தரஇடை  
துவள மனிதரு மமரரு முநிவரு … முடனோடித்  
தொடர வனமணி மகரமி லகுகுழை  
யடரு வனவிட மிளிர்வன ரதிபதி  
சுருதி மொழிவன கயல்விழி புரள்தர … நடுவாக  
வகிரு மதிபுரை தநுநுதல் பனிவர  
வனச பதயுக பரிபுர மொலிபட  
மறுகு தொறுமுல வியினிய கலவியை … விலைகூறும்  
வரைவி லரிவையர் தருசுக சலதியி  
லலையு மெனதுயி ரநுதின நெறிதரு  
மவுன சிவசுக சலதியில் முழுகுவ … தொருநாளே  
முகிலு மதியமும் ரவியெழு புரவியு  
நெடிய குலைமிட றிடறமு துககன  
முகடு கிழிபட வளர்வன கமுகின … மிசைவாளை  
முடுகு கயலுகள் வயல்களு முருகவிழ்  
தடமு முளரிய அகழியு மதிள்களு  
முழுது முடையதொ ரருணையி லுறைதரு … மிளையோனே  
அகிலு மருதமு முகுளித வகுளமு  
மமுத கதலியும் அருணமும் வருடையு  
மபரி மிதமத கரிகளு மரிகளு … முடனேகொண்  
டருவி யிழிதரு மருவரை தனிலொரு  
சவர வனிதையை முநிதரு புனிதையை  
அவச முடன்மல ரடிதொழு துருகிய … பெருமாளே.  

Marked reading: The poet pictures the women without bounds who sell their sweet lovemaking at a price in every street, their hair and garments loosening, breasts swaying, eyes speaking Kama's scripture, so that men, gods and sages run after them, and asks when his life, tossing in the sea of pleasure they give, will plunge instead into the sea of silent Siva-bliss. The praise paints Arunai, its areca palms tearing the sky so that clouds, moon and the sun's horses stumble, its fields, tanks, moat and walls, and the hill stream carrying agil, flowers, gems, goats, elephants and lions, where Murugan bowed melting at the feet of the hunter girl born of a sage.

### thiruppugazh:501

சாந்துட னேபுழுகு தோய்ந்தழ கார்குழலை  
மோந்துப யோதரம … தணையாகச்  
சாய்ந்துப்ர தாபமுடன் வாழ்ந்த நுராகசுக  
காந்தமொ டூசியென … மடவார்பால்  
கூர்ந்தக்ரு பாமனது போந்துன தாள்குறுகி  
ஓர்ந்துண ராவுணர்வி … லடிநாயேன்  
கூம்பவிழ் கோகநக பூம்பத கோதிலிணை  
பூண்டுற வாடுதின … முளதோதான்  
பாந்தளின் மீதினிதி னோங்குக ணேதுயில்கொள்  
நீண்டிடு மாலொடய … னறியாது  
பாம்புரு வானமுநி வாம்புலி யானபதன்  
ஏய்ந்தெதிர் காணநட … மிடுபாதர்  
பூந்துணர் பாதிமதி வேய்ந்தச டாமகுட  
மாங்கன காபுரியி … லமர்வாழ்வே  
பூங்கமு கார்வுசெறி யூங்கந காபுரிசை  
சூழ்ம்புலி யூரிலுறை … பெருமாளே.  

Marked reading: The poet tells how he smelled women's perfumed hair, lay on their breasts and lived proudly in pleasure, drawn to them like a needle to a magnet, and asks whether a day will come when grace fills him and, knowing without reasoning, he wears Murugan's faultless lotus feet. The praise names Siva, whom Vishnu and Brahma could not know, dancing before the serpent sage and the tiger-footed sage, wearing the half moon in his matted hair in the golden city, and Murugan as his treasure, at Puliyur with its golden walls.

### thiruppugazh:510

மச்ச மெச்சு சூத்ரம் ரத்த பித்த மூத்ரம்  
வைச்சி றைச்ச பாத்ர … மநுபோகம்  
மட்க விட்ட சேக்கை உட்பு ழுத்த வாழ்க்கை  
மட்டு லப்ப தார்த்த … மிடிபாறை  
எய்ச்சி ளைச்ச பேய்க்கு மெய்ச்சி ளைச்ச நாய்க்கு  
மெய்ச்சி ளைச்ச ஈக்கு … மிரையாகும்  
இக்க டத்தை நீக்கி அக்க டத்து ளாக்கி  
இப்படிக்கு மோக்ஷ … மருள்வாயே  
பொய்ச்சி னத்தை மாற்றி மெய்ச்சி னத்தை யேற்றி  
பொற்ப தத்து ளாக்கு … புலியூரா  
பொக்க ணத்து நீற்றை யிட்டொ ருத்த னார்க்கு  
புத்தி மெத்த காட்டு … புனவேடன்  
பச்சி லைக்கும் வாய்க்கு ளெச்சி லுக்கும் வீக்கு  
பைச்சி லைக்கு மாட்கொ … ளரன்வாழ்வே  
பத்தி சித்தி காட்டி அத்தர் சித்த மீட்ட  
பத்த ருக்கு வாய்த்த … பெருமாளே.  

Marked reading: The poet calls his body a vessel of flesh, blood, bile and urine bound together, a rotting bed of pleasures, a worm-eaten life that becomes food for the tired ghoul, the dog and the fly, and asks Murugan to remove this pot and place him in that other one, granting release. The praise names Murugan at Puliyur who turns false anger to true anger and places devotees at his golden feet, and the son of Hara who took into service the hunter of the field, who offered green leaves and water from his mouth.

### thiruppugazh:591

துஞ்சு கோட்டிச் சுழற்கண் காட்டிக்  
கொங்கை நோக்கப் பலர்க்குங் காட்டிக்  
கொண்ட ணாப்பித் துலக்கஞ் சீர்த்துத் … திரிமானார்  
தொண்டை வாய்ப்பொற் கருப்பஞ் சாற்றைத்  
தந்து சேர்த்துக் கலக்குந் தூர்த்தத்  
துன்ப வாழ்க்கைத் தொழிற்பண் டாட்டத் … துழலாதே  
கஞ்சம் வாய்த்திட் டவர்க்குங் கூட்டிக்  
கன்று மேய்த்திட் டவர்க்குங் கூற்றைக்  
கன்ற மாய்த்திட் டவர்க்குந் தோற்றக் … கிடையாநீ  
கண்டு வேட்டுப் பொருட் கொண்டாட்டத்  
தின்ப வாக்யத் தெனக்குங் கேட்கத்  
தந்து காத்துத் திருக்கண் சாத்தப் … பெறுவேனோ  
வஞ்ச மாய்ப்புக் கொளிக்குஞ் சூற்கைத்  
துன்று சூர்ப்பொட் டெழச்சென் றோட்டிப்  
பண்டு வாட்குட் களிக்குந் தோட்கொத் … துடையோனே  
வண்டு பாட்டுற் றிசைக்குந் தோட்டத்  
தண்கு ராப்பொற் புரக்கும் பேற்றித்  
தொண்டர் கூட்டத் திருக்குந் தோற்றத் … திளையோனே  
கொஞ்சு வார்த்தைக் கிளித்தண் சேற்கட்  
குன்ற வேட்டிச் சியைக்கண் காட்டிக்  
கொண்டு வேட்டுப் புனப்பைங் காட்டிற் … புணர்வோனே  
கொங்கு லாத்தித் தழைக்குங் காப்பொற்  
கொண்ட லார்த்துச் சிறக்குங் காட்சிக்  
கொங்கு நாட்டுத் திருச்செங் கோட்டுப் … பெருமாளே.  

Marked reading: The poet asks not to wander in the lewd, sorrowful trade of women who show rolling eyes and their breasts to many, deceive, and give the cane-sweet juice of their lips, and asks whether Murugan, whom Brahma, Vishnu and Siva the slayer of Death could not see, will protect him, let him hear the sweet words of the meaning, and look on him with grace. The praise names Murugan who drove out Sura hiding in deceit, who stands in the company of devotees in the kura groves, who wooed the hunter girl in the millet field, at Tiruchengodu in the Kongu country.

### thiruppugazh:615

கொண்டாடிக் கொஞ்சு மொழிகோடு  
கண்டாரைச் சிந்து விழிகொடு  
கொந்தாரச் சென்ற குழல்கொடு … வடமேருக்  
குன்றோடொப் பென்ற முலைகொடு  
நின்றோலக் கஞ்செய் நிலைகொடு  
கொம்பாயெய்ப் புண்ட விடைகொடு … பலரோடும்  
பண்டாடச் சிங்கி யிடுமவர்  
விண்டாலிக் கின்ற மயிலன  
பண்பாலிட் டஞ்செல் மருளது … விடுமாறு  
பண்டேசொற் றந்த பழமறை  
கொண்டேதர்க் கங்க ளறவுமை  
பங்காளர்க் கன்று பகர்பொருள் … அருள்வாயே  
வண்டாடத் தென்றல் தடமிசை  
தண்டாதப் புண்ட ரிகமலர்  
மங்காமற் சென்று மதுவைசெய் … வயலு஡ரா  
வன்காளக் கொண்டல் வடிவொரு  
சங்க்ராமக் கஞ்சன் விழவுதை  
மன்றாடிக் கன்பு தருதிரு … மருகோனே  
திண்டாடச் சிந்து நிசிசரர்  
தொண்டாடக் கண்ட வமர்பொரு  
செஞ்சேவற் செங்கை யுடையசண் … முகதேவே  
சிங்காரச் செம்பொன் மதிளத  
லங்காரச் சந்த்ர கலைதவழ்  
தென்சேரிக் குன்றி லினிதுறை … பெருமாளே.  

Marked reading: The poet lists women's cajoling speech, eyes, hair heavy with flowers, breasts like Meru, the posture of their display and slender waists, as they dance with many, like peacocks, and asks Murugan, to free him from the delusion of desire for them, to grant the meaning he told Siva of old, from the ancient Veda, ending all arguments. The praise names the lord of Vayalur's fields, nephew of the cloud-dark one who kicked Kamsa, the six-faced god holding the red cock, at Thenseri hill with its golden walls touched by the moon.

### thiruppugazh:616

ஐங்கரனை யொத்தமன மைம்புலம கற்றிவள  
ரந்திபக லற்றநினை … வருள்வாயே  
அம்புவித னக்குள்வளர் செந்தமிழ்வ ழுத்தியுனை  
அன்பொடுது திக்கமன … மருள்வாயே  
தங்கியத வத்துணர்வு தந்தடிமை முத்திபெற  
சந்திரவெ ளிக்குவழி … யருள்வாயே  
தண்டிகைக னப்பவுசு எண்டிசைம திக்கவளர்  
சம்ப்ரமவி தத்துடனெ … யருள்வாயே  
மங்கையர்சு கத்தைவெகு இங்கிதமெ னுற்றமன  
முன்றனைநி னைத்தமைய … அருள்வாயே  
மண்டலிக ரப்பகலும் வந்தசுப ரட்சைபுரி  
வந்தணைய புத்தியினை … யருள்வாயே  
கொங்கிலுயிர் பெற்றுவளர் தென்கரையி லப்பரருள்  
கொண்டுஉட லுற்றபொரு … ளருள்வாயே  
குஞ்சரமு கற்கிளைய கந்தனென வெற்றிபெறு  
கொங்கணகி ரிக்குள்வளர் … பெருமாளே.  

Marked reading: The song is a string of prayers, each ending 'grant': a mind like Ganapati's that has driven off the five senses and a thought beyond night and day; a mind to praise Murugan with love in the Tamil that grows on earth; the knowledge of austerity, so that as a servant he gains release and a way to the moon-space; a grand palanquin and splendour esteemed in the eight directions; a mind that turns from the pleasure of women to think of Murugan; and the meaning that a father gained by grace on the southern bank in Kongu. It ends with Murugan, younger brother of the elephant-faced one, at Konganagiri.

### thiruppugazh:645

மருவறா வெற்றி மலர்தொடா விற்கை  
வலிசெயா நிற்கு … மதனாலும்  
மதில்கள்தா வுற்ற கலைபடா வட்ட  
மதிசுடா நிற்கு … மதனாலும்  
இருகணால் முத்த முதிரயா மத்தி  
னிரவினால் நித்த … மெலியாதே  
இடருறா மெத்த மயல்கொளா நிற்கு  
மிவளைவாழ் விக்க … வரவேணும்  
கரிகள்சேர் வெற்பி லரியவே டிச்சி  
கலவிகூர் சித்ர … மணிமார்பா  
கனகமா ணிக்க வடிவனே மிக்க  
கதிரகா மத்தி … லுறைவோனே  
முருகனே பத்த ரருகனே முத்தி  
முதல்வனே பச்சை … மயில்வீரா  
முடுகிமே லிட்ட கொடியசூர் கெட்டு  
முறியவேல் தொட்ட … பெருமாளே.  

Marked reading: Spoken for a girl sick with love: wounded by Madana's flower bow and burned by the full moon above the walls, weeping pearls from both eyes through the night, she is wasting away in deep infatuation, and the speaker asks Murugan to come and give her life. The praise names his jewelled chest that delighted in the hunter girl, his form of gold and ruby, Murugan near to his devotees, the first of release, the hero on the green peacock whose vel broke Sura.

### thiruppugazh:705

ஏறா னாலே நீறாய் மாயா  
வேளே வாசக் … கணையாலே  
ஏயா வேயா மாயா வேயா  
லாமே ழோசைத் … தொளையாலே  
மாறா யூறா யீறாய் மாலாய்  
வாடா மானைக் … கழியாதே  
வாராய் பாராய் சேரா யானால்  
வாடா நீபத் … தொடைதாராய்  
சீறா வீறா ஈரேழ் பார்சூழ்  
சீரார் தோகைக் … குமரேசா  
தேவா சாவா மூவா நாதா  
தீரா கோடைப் … பதியோனே  
வேறாய் மாறா யாறா மாசூர்  
வேர்போய் வீழப் … பொருதோனே  
வேதா போதா வேலா பாலா  
வீரா வீரப் … பெருமாளே.  

Marked reading: A short akam song in the voice of someone pleading for a lovesick girl: Kama, who did not die though the rider of the bull burned him to ash, wounds her with his fragrant arrows, and the flute with its seven-note holes torments her; it asks Murugan not to let this deer-like girl, wasting into enmity, hurt, end and longing, perish, but to come, look on her and join her, or else give his unfading kadamba garland. The praise names the Kumara of the peacock who circles the fourteen worlds, the deathless, ageless lord of Kodai, who fought until great Sura fell uprooted, the hero of the vel.

### thiruppugazh:742

வெகுமாய விதத்துரு வாகிய  
திறமேப ழகப்படு சாதக  
விதமேழ்க டலிற்பெரி தாமதில் … சுழலாகி  
வினையான கருக்குழி யாமெனு  
மடையாள முளத்தினின் மேவினும்  
விதியாரும் விலக்கவொ ணாதெனு … முதியோர்சொல்  
தகவாம தெனைப்பிடி யாமிடை  
கயிறாலு மிறுக்கிம காகட  
சலதாரை வெளிக்கிடை யேசெல … வுருவாகிச்  
சதிகாரர் விடக்கதி லேதிரள்  
புழுவாக நெளித்தெரி யேபெறு  
மெழுகாக வுருக்குமு பாதிகள் … தவிர்வேனோ  
உ ககால நெருப்பதி லேபுகை  
யெழவேகு முறைப்படு பாவனை  
யுறவேகு கையிற்புட மாய்விட … வெளியாகி  
உ லவாநர குக்கிரை யாமவர்  
பலவோர்கள் தலைக்கடை போயெதிர்  
உ ளமாழ்கி மிகக்குழை வாகவு … முறவாடித்  
தொகலாவ தெனக்கினி தானற  
வளமாக அருட்பத மாமலர்  
துணையேப ணியத்தரு வாய்பரி … மயில்வேலா  
துதிமாத வர்சித்தர்ம கேசுரர்  
அரிமால்பி ரமர்க்கருள் கூர்தரு  
துறையூர்நக ரிற்குடி யாய்வரு … பெருமாளே.  

Marked reading: The poet says that through many forms and births, in a womb-pit made of deeds, he has learned the elders' word that fate cannot be turned aside; he fears the hour when he is seized and bound with rope, the body becomes a heap of worms, is melted like wax and burned with rising smoke, becomes food for hell, while his kin stand at the door weeping, and asks to be freed from these and given the flower feet of grace to bow to. The praise names Murugan of the vel on the galloping peacock, who gives grace at Thuraiyur to sages, siddhas, Maheswaras, Hari and Brahma.

### thiruppugazh:877

தோடுற்றுக் காதள வோடிய  
வேலுக்குத் தானிக ராயெழு  
சூதத்திற் காமனி ராசத … விழியாலே  
சோடுற்றத் தாமரை மாமுகை  
போலக்கற் பூரம ளாவிய  
தோல்முத்துக் கோடென வீறிய … முலைமானார்  
கூடச்சிக் காயவ ரூழிய  
மேபற்றிக் காதலி னோடிய  
கூளச்சித் தாளனை மூளனை … வினையேனைக்  
கோபித்துத் தாயென நீயொரு  
போதத்தைப் பேசவ தாலருள்  
கோடித்துத் தானடி யேனடி … பெறவேணும்  
வேடிக்கைக் காரவு தாரகு  
ணபத்மத் தாரணி காரண  
வீரச்சுத் தாமகு டாசமர் … அடுதீரா  
வேலைக்கட் டாணிம காரத  
சூரர்க்குச் சூரனை வேல்விடு  
வேழத்திற் சீரரு ளூறிய … இளையோனே  
ஆடத்தக் காருமை பாதியர்  
வேதப்பொற் கோவண வாடையர்  
ஆலித்துத் தானரு ளூறிய … முருகோனே  
ஆடப்பொற் கோபுர மேவிய  
ஆடிக்கொப் பாமதிள் சூழ்பழை  
யாறைப்பொற் கோயிலின் மேவிய … பெருமாளே.  

Marked reading: The poet describes women whose eyes run to the ears like spears and whose camphor-scented breasts are like lotus buds, and calls himself a rubbish-minded slave and sinner who, caught by them, took up their service and ran after them with love; he asks Murugan to be angry with him like a mother and speak one word of teaching, so that by that grace he gains the feet. The praise names the playful, generous hero who sent the vel at Sura in the sea, the younger brother of the elephant-faced one, the son of Siva who dances with Uma as his half and wears the Vedas as his loincloth, at the golden temple of Pazhaiyarai with its towers and walls like mirrors.

### thiruppugazh:921

வாசனை மங்கையர் போற்று சிற்றடி  
பூஷண கிண்கிணி யார்ப்ப ரித்திட  
மாமலை ரண்டென நாட்டு மத்தக … முலையானை  
வாடைம யங்கிட நூற்ற சிற்றிழை  
நூலிடை நன்கலை தேக்க இக்குவில்  
மாரன்வி டுங்கணை போற்சி வத்திடு … விழியார்கள்  
நேசிகள் வம்பிக ளாட்ட மிட்டவர்  
தீயர்வி ரும்புவர் போற்சு ழற்றியெ  
நீசனெ னும்படி யாக்கி விட்டொரு … பிணியான  
நீரின்மி குந்துழ லாக்கை யிற்றிட  
யோகமி குந்திட நீக்கி யிப்படி  
நீயக லந்தனில் வீற்றி ருப்பது … மொருநாளே  
தேசம டங்கலு மேத்து மைப்புய  
லாயநெ டுந்தகை வாழ்த்த வச்சிர  
தேகமி லங்கிய தீர்க்க புத்திர … முதல்வோனே  
தீரனெ னும்படி சாற்று விக்ரம  
சூரன டுங்கிட வாய்த்த வெற்புடல்  
தேயந டந்திடு கீர்த்தி பெற்றிடு … கதிர்வேலா  
மூசளி பம்பிய நூற்றி தழ்க்கம  
லாசனன் வந்துல காக்கி வைத்திடு  
வேதன கந்தையை மாற்றி முக்கண … ¡றிவாக  
மூதறி வுந்திய தீ¨க்ஷ செப்பிய  
ஞானம்வி ளங்கிய மூர்த்தி யற்புத  
மூவரி லங்குப ராய்த்து றைப்பதி … பெருமாளே.  

Marked reading: The poet describes fragrant women whose small feet ring with anklets, whose breasts stand like two hills and whose eyes redden like Kama's arrows, lovers and deceivers who spin him about until he is called vile, and asks whether there will be a day when, with yoga growing and the body that whirls in the water of disease removed, Murugan sits within his breast. The praise names the vel that wore down the mountain and made Sura tremble, and the wondrous one who changed the pride of Brahma, maker of the world, and spoke the initiation of ancient knowledge, at Paraithurai.

### thiruppugazh:930

குருவு மடியவ ரடியவ ரடிமையு  
மருண மணியணி கணபண விதகர  
குடில செடிலினு நிகரென வழிபடு … குணசீலர்  
குழுவி லொழுகுதல் தொழுகுதல் விழுகுதல்  
அழுகு தலுமிலி நலமிலி பொறையிலி  
குசல கலையிலி தலையிலி நிலையிலி … விலைமாதர்  
மருவு முலையெனு மலையினி லிடறியும்  
அளக மெனவள ரடவியில் மறுகியு  
மகர மெறியிரு கடலினில் முழுகியு … முழலாமே  
வயலி நகரியி லருள்பெற மயில்மிசை  
யுதவு பரிமள மதுகர வெகுவித  
வனச மலரடி கனவிலு நனவிலு … மறவேனே  
உ ருவு பெருகயல் கரியதொர் முகிலெனு  
மருது நெறிபட முறைபட வரைதனில்  
உ ரலி னொடுதவழ் விரகுள இளமையு … மிகமாரி  
உ மிழ நிரைகளி னிடர்கெட வடர்கிரி  
கவிகை யிடவல மதுகையு நிலைகெட  
வுலவில் நிலவறை யுருவிய வருமையு … மொருநூறு  
நிருப ரணமுக வரசர்கள் வலிதப  
விசயன் ரதமுதல் நடவிய வெளிமையு  
நிகில செகதல முரைசெயு மரிதிரு … மருகோனே  
நிலவு சொரிவளை வயல்களு நெடுகிய  
குடக தமனியு நளினமு மருவிய  
நெருவை நகருறை திருவுரு வழகிய … பெருமாளே.  

Marked reading: The poet sets himself against the virtuous company who worship the guru, the devotees and the devotees' servants as equal to the Lord, and calls himself one without their conduct, worship, falling at the feet or weeping, without goodness, patience, skill, sense or steadiness; he asks not to stumble on the hill of priced women's breasts, wander in the forest of their hair and drown in the sea of their eyes, and vows not to forget in dream or waking the lotus feet given him at Vayali. The praise is Krishna's: the dark child who crawled with the mortar and broke the marutha trees, lifted the hill as an umbrella against the rain for the cattle, came through the trap of the underground chamber, and humbly drove Arjuna's chariot to break the hundred kings, and calls Murugan his nephew, at Neruvai among paddy and lotuses.

### thiruppugazh:955

உ ரைத்த சம்ப்ரம வடிவு திரங்கிக்  
கறுத்த குஞ்சியும் வெளிறிய பஞ்சொத்  
தொலித்தி டுஞ்செவி செவிடுற வொண்கட் … குருடாகி  
உ ரத்த வெண்பலு நழுவிம தங்கெட்  
டிரைத்து கிண்கிணெ னிருமலெ ழுந்திட்  
டுளைப்பு டன்தலை கிறுகிறெ னும்பித் … தமுமேல்கொண்  
டரத்த மின்றிய புழுவினும் விஞ்சிப்  
பழுத்து ளஞ்செயல் வசனம் வரம்பற்  
றடுத்த பெண்டிரு மெதிர்வர நிந்தித் … தனைவோரும்  
அசுத்த னென்றிட வுணர்வத குன்றித்  
துடிப்ப துஞ்சிறி துளதில தென்கைக்  
கவத்தை வந்துயி ரலமரு மன்றைக் … கருள்வாயே  
திரித்தி ரிந்திரி ரிரிரிரி ரின்றிட்  
டுடுட்டு டுண்டுடு டுடுடுடு டுண்டுட்  
டிகுட்டி குண்டிகு டிகுடிகு டிண்டிட் … டிகுதீதோ  
திமித்தி மிந்திமி திமிதிமி யென்றிட்  
டிடக்கை துந்துமி முரசு முழங்கச்  
செருக்க ளந்தனில் நிருதர் தயங்கச் … சிலபேய்கள்  
தரித்து மண்டையி லுதிர மருந்தத்  
திரட்ப ருந்துகள் குடர்கள் பிடுங்கத்  
தருக்கு சம்புகள் நிணமது சிந்தப் … பொரும்வேலா  
தடச்சி கண்டியில் வயலியி லன்பைப்  
படைத்த நெஞ்சினி லியல்செறி கொங்கிற்  
றனிச்ச யந்தனி லினிதுறை கந்தப் … பெருமாளே.  

Marked reading: The poet pictures the body's ruin in old age: its once-proud form shrivels, black hair whitens like cotton, the ears go deaf, the eyes blind, the teeth loosen, cough and phlegm rise, the head reels with bile, the body rots worse than a bloodless worm, mind, deeds and speech run out of bounds, the wife who came reviles him, all call him unclean, sense fails and the pulse is barely there; on that day of the soul's distress he asks for grace. The praise is a battle in drum syllables where ghouls drink blood from skulls and kites pull entrails, and names Murugan the lord of Vayalur and of Thanichayam in Kongu.

### thiruppugazh:1015

விடமென அயிலென அடுவன நடுவன மிளிர்வன சுழல்விழி  
வித்தைத் குப்பக ரொப்புச் சற்றிலை … யென்றுபேசும்  
விரகுடை வனிதைய ரணைமிசை யுருகிய வெகுமுக கலவியில்  
இச்சைப் பட்டுயிர் தட்டுப் பட்டுவு … ழன்றுவாடும்  
நடலையில் வழிமிக அழிபடு தமியனை நமன்விடு திரளது  
கட்டிச் சிக்கென வொத்திக் கைக்கொடு … கொண்டுபோயே  
நரகதில் விடுமெனு மளவினி லிலகிய நறைகமழ் திருவடி  
முத்திக் குட்படு நித்யத் தத்துவம் … வந்திடாதோ  
இடியென அதிர்குரல் நிசிசரர் குலபதி யிருபது திரள்புய  
மற்றுப் பொற்றலை தத்தக் கொத்தொடு … நஞ்சுவாளி  
எரியெழ முடுகிய சிலையின ரழகொழு கியல்சிறு வினைமகள்  
பச்சைப் பட்சித னைக்கைப் பற்றிடு … மிந்த்ரலோகா  
வடவரை யிடிபட அலைகடல் சுவறிட மகவரை பொடிபட  
மைக்கட் பெற்றிடு முக்ரக் கட்செவி … யஞ்சசூரன்  
மணிமுடி சிதறிட அலகைகள் பலவுடன் வயிரவர் நடமிட  
முட்டிப் பொட்டெழ வெட்டிக் குத்திய … தம்பிரானே.  

Marked reading: The poet, ruined alone by passion for women who flatter a man's skill and melt in many-sided union, asks whether, when Death's host binds him tight and drags him off to hell, the fragrant holy feet, the eternal reality that is release, will not come. The praise tells of Rama's arrow scattering Ravana's twenty arms and golden heads, Murugan who takes Valli with her green parrot, and the vel that shattered Sura's crown while the Bhairavas danced.

### thiruppugazh:1077

முழுமதி யனைய முகமிரு குழையில்  
முனிவழி முனைகள் … கொண்முவா  
முதலறி வதனை வளைபவர் கலவி  
முழுகிய வினையை … மொண்டுநாயேன்  
வழிவழி யடிமை யெனுமறி வகல  
மனமுறு துயர்கள் … வெந்துவாட  
மதிதரு மதிக கதிபெறு மடிகள்  
மகிழ்வொடு புகழு … மன்புதாராய்  
எழுதிட அரிய எழில்மற மகளின்  
இருதன கிரிகள் … தங்குமார்பா  
எதிர்பொரு மசுரர் பொடிபட முடுகி  
இமையவர் சிறையை … யன்றுமீள்வாய்  
அழகிய குமர எழுதல மகிழ  
அறுவர்கள் முலையை … யுண்டவாழ்வே  
அமருல கிறைவ உ மைதரு புதல்வ  
அரியர பிரமர் … தம்பிரானே.  

Marked reading: The poet speaks of women with moon faces and eyes that rival their ear-rings, who ensnare the first understanding, and of the karma of plunging into union with them that he, a dog, has drawn on himself; he asks for the love that praises with joy the feet that give wisdom and the higher state, so that the sorrows of his mind wither. The praise names Murugan the chest where the hunter girl's breasts rest, the one who crushed the asuras and freed the gods, the beautiful Kumara who drank the milk of the six mothers, son of Uma, and lord of Hari, Hara and Brahma.

### thiruppugazh:1090

உ றவின்முறை யோர்க்கு முறுதுயரம் வாய்த்து  
உ ளமுருகு தீர்த்தி … வுடலு஡டே  
உ டலை முடிவாக்கு நெடியதொரு காட்டில்  
உ யர்கனலை மூட்டி … விடஆவி  
மறலிமற மார்த்த கயிறுதனை வீக்கி  
வலிவினொடு தாக்கி … வளையாமுன்  
மனமுமுனி வேட்கை மிகவு முன தாட்கள்  
மகிழ்வியல்கொ டேத்த … மதிதாராய்  
பிறைநுதலி சேற்க ணமையரிவை வேட்பு  
வரையில்மற வோ஡க்கு … மகவாகப்  
பிறிதுருவில் வாய்த்து நிறைதினைகள் காத்த  
பிடியினடி போற்று … மணவாளா  
அறுகுபிறை யாத்தி அலைசலமு மார்த்த  
அடர்சடையி னார்க்கு … மறிவீவாய்  
அடரவரு போர்க்கை அசுரர்கிளை மாய்த்து  
அமரர்சிறை மீட்ட … பெருமாளே.  

Marked reading: Before his kin are struck with grief, the body is laid on a high fire in the long forest of the dead, and Death binds his rope and strikes to bind the life, the poet asks for the mind to praise Murugan's feet with joy and eager longing. The praise names him the bridegroom who honours the feet of the girl with crescent brow and carp eyes, born in another form as child to the hunters to guard the millet, the one who gave knowledge to Siva of the matted hair with arugu, crescent, aththi and the Ganges, and the one who freed the gods.

### thiruppugazh:1178

புருவத்தை நெறித்து விழிக்கயல்  
பயிலிட்டு வெருட்டி மதித்திரு  
புதுவட்டை மினுக்கி யளிக்குல … மிசைபாடும்  
புயல்சற்று விரித்து நிரைத்தொளி  
வளையிட்ட கரத்தை யசைத்தகில்  
புனைமெத்தை படுத்த பளிக்கறை … தனிலேறிச்  
சரசத்தை விளைத்து முலைக்கிரி  
புளகிக்க அணைத்து நகக்குறி  
தனைவைத்து முகத்தை முகத்துட … னுறமேவித்  
தணிவித்தி ரதத்த தரத்துமி  
ழமுதத்தை யளித்து வுருக்கிகள்  
தருபித்தை யகற்றி யுனைத்தொழ … முயல்வேனோ  
பரதத்தை யடக்கி நடிப்பவர்  
த்ரிபுரத்தை யெரிக்க நகைப்பவர்  
பரவைக்குள் விடத்தை மிடற்றிடு … பவர்தேர்கப்  
பரையுற்ற கரத்தர் மிகப்பகி  
ரதியுற்ற சிரத்தர் நிறத்துயர்  
பரவத்தர் பொருப்பி லிருப்பவ … ருமையாளர்  
சுரர் சுத்தர் மனத்துறை வித்தகர்  
பணிபத்தர் பவத்தை யறுப்பவர்  
சுடலைப்பொடி யைப்பரிசிப்பவர் … விடையேறுந்  
துணையொத்த பதத்த ரெதிர்த்திடு  
மதனைக்கடி முத்தர் கருத்தமர்  
தொலைவற்ற க்ருபைக்கு ளுதித்தருள் … பெருமாளே.  

Marked reading: The poet describes women who knit their brows, flash carp eyes, spread their hair, wave bangled hands, lead a man to an aloe-scented bed in a crystal chamber, embrace him, mark him with nails and give the nectar of their lips, and asks whether, rid of the madness these melting women give, he will strive to worship Murugan. The praise is a long portrait of Siva, the dancer, burner of Tripura, holder of the poison, Ganga on his head, Uma's lord on the mountain, who cuts birth, smears cremation ash, rides the bull and burned Madana, and names Murugan as born of his boundless grace.

### thiruppugazh:1201

விரைசொரியு ம்ருகமதமு மலரும் வாய்த்திலகு  
விரிகுழலு மவிழநறு மெழுகு கோட்டுமுலை  
மிசையில்வரு பகலொளியை வெருவ வோட்டுமணி … வகையாரம்  
விடுதொடைகள் நகநுதியி லறவும் வாய்த்தொளிர  
விழிசெருக மொழிபதற அமுது தேக்கியகை  
விதறிவளை கலகலென அழகு மேற்பொழிய … அலர்மேவும்  
இருசரண பரிபுரசு ருதிக ளார்க்கவச  
மிலகுகடல் கரைபுரள இனிமை கூட்டியுள  
மிதம்விளைய இருவரெனு மளவு காட்டரிய … அநுராகத்  
திடைமுழுகி யெனதுமன தழியு நாட்களினு  
மிருசரண இயலும்வினை யெறியும் வேற்கரமு  
மெழுதரிய திருமுகமு மருளு மேத்தும்வகை … தரவேணும்  
அரிபிரம ரடிவருட வுததி கோத்தலற  
அடல்வடவை யனலுமிழ அலகை கூட்டமிட  
அணிநிணமு மலைபெருக அறையும் வாச்சியமு … மகலாது  
அடல்கழுகு கொடிகெருட னிடைவி டாக்கணமு  
மறுகுறளு மெறிகுருதி நதியின் மேற்பரவ  
அருணரண முகவயிர வர்களு மார்ப்பரவ … மிடநாளும்  
பரவுநிசி சரர்முடிகள் படியின் மேற்குவிய  
பவுரிகொடு திரியவரை பலவும் வேர்ப்பறிய  
பகர்வரிய ககனமுக டிடிய வேட்டைவரு … மயில்வீரா  
படருநெறி சடையுடைய இறைவர் கேட்குரிய  
பழயமறை தருமவுன வழியை யார்க்குமொரு  
பரமகுரு பரனெனவு மறிவு காட்டவல … பெருமாளே.  

Marked reading: After a long and frank picture of lovemaking until the two seem one, the poet asks that even in the days when his mind is lost in that passion he be given ways to praise Murugan's two feet, the vel hand that casts out karma, his holy face beyond depicting, and his grace. The praise has Vishnu and Brahma pressing his feet, a battlefield of ghouls, vultures and Bhairavas, and calls Murugan the supreme guru who showed the Lord of the matted hair the silent way that the ancient Veda gives.

### thiruppugazh:1249

திரைவஞ்ச இருவினைகள் நரையங் கமலமழிய  
சிவகங்கை தனில்முழுகி … விளையாடிச்  
சிவம்வந்து குதிகொளக வடிவுன்றன் வடிவமென  
திகழண்டர் முநிவர்கண … மயன்மாலும்  
அரன்மைந்த னெனகளிறு முகனெம்பி யெனமகிழ  
அடியென்க ணளிபரவ … மயிலேறி  
அயில்கொண்டு திருநடன மெனதந்தை யுடன்மருவி  
அருமந்த பொருளையினி … யருள்வாயே  
பரியென்ப நரிகள்தமை நடனங்கொ டொருவழுதி  
பரிதுஞ்ச வருமதுரை … நடராஜன்  
பழியஞ்சி யெனதருகி லுறைபுண்ட ரிகவடிவ  
பவளஞ்சொ லுமைகொழுந … னருள்பாலா  
இருள்வஞ்ச கிரியவுண ருடனெங்க ளிருவினையு  
மெரியுண்டு பொடியஅயில் … விடுவோனே  
எனதன்பி லுறைசயில மகிழ்வஞ்சி குறமகளொ  
டெணுபஞ்ச ணையின்மருவு … பெருமாளே.  

Marked reading: The poet asks that, with wrinkles, grey hair, the body's suffering and the two deceitful deeds destroyed, he bathe and play in the Sivaganga tank, that Sivam leap into him so that his inner form becomes Murugan's form, and that, with gods, sages, Brahma and Vishnu calling him Hara's son and Ganapati 'my younger brother', Murugan come on the peacock with the vel, join his father in the holy dance, and give the precious meaning. The praise names Siva, the dancer of Madurai who made foxes into horses for a Pandya king, and Murugan the vel that burns to powder the dark hill, the asuras and our two deeds, who dwells in the poet's love with Valli.


## siddhar

### siddhar:161 (பத்திரகிரியார், மெய்ஞ்ஞானப் புலம்பல்)

என்னை விட்டு நீங்காமல் என்னிடத்து நீ இருக்க  
உன்னை விட்டு நீங்காது ஒருப்படுவது எக்காலம்?  

Marked reading: Since you stay in me and never leave me, when will I become one-pointed and never leave you?

### siddhar:300 (பட்டினத்தார், முதலாவது கோயிற்றிருவகவல்)

நினைமின் மனனே! நினைமின் மனனே!  
சிவபெரு மானைச் செம்பொனம் பலவனை  
நினைமின் மனனே! நினைமின் மனனே!  
அலகைத் தேரி னலமரு காலின்  
உலகப்பொய் வாழ்க்கையை யுடலையோம் பற்க!  
பிறந்தன இறக்கும், இறந்தன பிறக்கும்;  
தோன்றின மறையும், மறைந்தன தோன்றும்;  
பெருத்தன சிறுக்கும், சிறுத்தன பெருக்கும்;  
உணர்ந்தன மறக்கும், மறந்தன வுணரும்;  
புணர்ந்தன பிரியும், பிரிந்தன புணரும்;  
அருந்தின மலமாம், புனைந்தன அழுக்காம்;  
உவப்பன வெறுப்பாம், வெறுப்பன உவப்பாம்;  
என்றிவை யனைத்து முணர்ந்தனை, அன்றியும்  
பிறந்தன பிறந்தன பிறவிக டோறும்  
கொன்றனை யனைத்தும், அனைத்துநினைக் கொன்றன,  
தின்றன யனைத்தும், அனைத்துநினைத் தின்றன;  
பெற்றன யனைத்தும், அனைத்துநினைப் பெற்றன;  
ஓம்பினை யனைத்தும், அனைத்துநினை யோம்பின;  
செல்வத்துக் களித்தனை, தரித்திரத் தழுகினை;  
சுவர்க்கத் திருந்தினை, நரகிற் கிடந்தனை,  
இன்பமும் துன்பமும் இருநிலத் தருந்தினை;  
ஒன்றென் றெழியா துற்றனை, அன்றியும்;  
புற்பதக் குரம்பைத் துச்சி லொதுக்கிடம்  
என்ன நின்றியங்கு மிருவினைக் கூட்டைக்  
கல்லினும் வலிதாக் கருதினை, இதனுள்,  
பீளையு நீரும் புலப்படு மொருபொறி;  
மீளுங் குறும்பி வெளிப்படு மொருபொறி;  
சளியு நீருந் தவழு மொருபொறி;  
உமிழ்நீர் கோழை யழுகு மொறிபொறி;  
வளியு மலமும் வழங்கு மொருவழி  
சலமுஞ் சீயுஞ் சரியு மொருவழி;  
உள்ளுறத் தொடங்கி வெளிப்பட நாறுஞ்  
சட்டக முடிவிற் சுட்டெலும் பாகும்  
உடலுறு வாழ்க்கையை யுள்ளுறத் தேர்ந்து,  
கடிமலர்க் கொன்றைச், சடைமுடிக் கடவுளை  
ஒழிவருஞ் சிவபெரும் போகவின் பத்தை;  
நிழலெனக் கடவா நீர்மையடு பொருந்தி,  
எனதற நினைவற இருவனை மலமற  
வரவொடு செலவற மருளற இருளற  
இரவொடு பகலற இகபர மறஒரு  
முதல்வனைத் தில்லையுண் முளைத்தெழுஞ் சோதியை  
அம்பலத் தரசனை, ஆனந்தக் கூத்தனை,  
நெருப்பினி லரக்கென நெக்குநெக் குருகித்  
திருச்சிற் றம்பலத் தொளிருஞ் சிவனை  
நினைமின் மனனே! நினைமின் மனனே!  
சிவபெருமானைச் செம்பொனம் பலவனை,  
நினைமின் மனனே! நினைமின் மனனே!  

Marked reading: Think, mind, of Siva of the golden hall and do not cherish the false life of the world or the body that staggers on the wheel of a demon's chariot: whatever is born dies and the dead are born, the large grows small and the small large, the known is forgotten and the forgotten known, what is eaten turns to excrement and what is adorned to dirt; through birth after birth you have killed all and all have killed you, eaten and been eaten, borne and been borne, rejoiced in wealth and wept in poverty, sat in heaven and lain in hell, and never once saw it as one; and this cage of the two deeds, a grass hut of a shelter with one opening for rheum, one for wax, one for mucus, one for spit and phlegm, one way for wind and excrement and one for urine and pus, stinking from within and ending as burnt bone, you took for firmer than stone. Knowing the bodily life from within, think of the god with konrai and matted hair, the unending Siva-bliss joined to you as a shadow that never leaves, free of 'I' and 'mine', of the two deeds and the malas, of coming and going, delusion and darkness, night and day, this world and the next, the First who rose as light in Tillai, the king of the hall, the dancer of bliss; melting like lac in fire, think of him, mind.

### siddhar:318 (பட்டினத்தார், திருப்பாடல் திரட்டு (தலப் பாடல்கள்))

இரைக்கே யிரவும் பகலுந் திரிந்திங் கிளைத்துமின்னார்  
அரைக்கே யவலக் குழியரு கேயசும் பார்ந்தொழுகும்  
புரைக்கே யுழலுந் தமியேனை யாண்டருள், பொன்முகலிக்  
கரைக்கேகல் லால நிழற்கீ ழமர்ந்தருள் காளத்தியே  

Marked reading: Wandering night and day for prey and growing weary here, circling the pit of misery at women's waists, the oozing hollow where fluid seeps, I am a lone one who goes round and round; take me and rule me, Kalathi who sits in grace under the stone banyan on the bank of the golden Mugali.

### siddhar:484 (பட்டினத்தார், அருட்புலம்பல் - முதல்வன் முறையீடு)

கண்டங் கறுத்துநின்ற காரணத்தைப் பாரேனோ !  
தொண்டர் குழுவினின்ற தோற்றமதைப் பாரேனோ !  

Marked reading: Shall I not see the cause of the throat that stood darkened? Shall I not see the sight of him standing in the devotees' company?

### siddhar:624 (பட்டினத்தார், அருட்புலம்பல் - இறந்தகாலத்திரங்கல்)

மெத்தமெத்தச்செல்வாக்கில்வேறுமருளடுத்துத்  
தத்தித்தலைகீழாய்த்தானடந்துகெட்டேனே  

Marked reading: As my influence grew and grew, a new delusion came upon me; I stumbled and walked head downward and was ruined.

### siddhar:677 (பட்டினத்தார், பூரணமாலை)

உருத்திரனையிருதயத்திலுண்மையுடன்பாராமல்  
கருத்தழிந்துநானுங்கலங்கினேன்பூரணமே  

Marked reading: Not seeing Rudra in the heart in truth, the poet says his purpose was lost and he was confused.

### siddhar:1287 (சிவவாக்கியர், சிவவாக்கியம்)

ஐம்புலனை வென்றவர்க்கு அன்னதானம் ஈவதால்  
நன்புலன்க ளாகிநின்ற நாதருக்கது ஏறுமோ  
ஐம்புலனை வென்றிடாது அவத்துமே உழன்றிடும்  
வம்பருக்கும் ஈவதும் கொடுப்பதும் அவத்தமே  

Marked reading: When food is given to those who have conquered the five senses, does it rise to the Lord who stands as the good senses? Giving and bestowing on wanderers who have not conquered the five senses and roll in vanity is itself vanity.

### siddhar:1395 (சிவவாக்கியர், சிவவாக்கியம்)

பாலகனாக வேணும்என்று பத்திமுற்றும் என்பிரேல்  
நாலுபாதம் உண்டதில் நினைந்திரண்டு அடுத்ததால்  
மூலநாடி தன்னில்வன்னி மூட்டிஅந்த நீருண  
ஏலவார் குழலியூடே ஈசர்பாதம் எய்துமே  

Marked reading: If you say your love has ripened to the wish to be her child: there are four steps, and since two of them come after thinking, kindle the fire in the root channel and drink that water; by way of the lady of fragrant hair you reach the feet of the Lord.

### siddhar:1403 (சிவவாக்கியர், சிவவாக்கியம்)

அடைவுளோர்கள் முத்தியே அறிந்திடாத மூடரே,  
படையுடைய தத்துவமும் பாதகங்கள் அல்லவோ?  
மடைதிறக்க வாரியின் மடையில் ஏறு மாறுபோல்  
உடலில்மூல நாடியைஉயர ஏற்றி ஊன்றிடே  

Marked reading: You fools who do not know the release of those who have reached: are not the tattvas with their army themselves the crimes? As the bull climbs the sluice when the sluice is opened into the channel, raise the root channel in the body upward and plant it firm.

### siddhar:1436 (சிவவாக்கியர், சிவவாக்கியம்)

புத்தகங் களைசுமந்து பொய்களைப் பிதற்றுவீர்.  
செத்திடம் பிறந்திடம் அதுஎங்ஙன்என்று அறிகிலீர்  
அத்தனைய சிந்தனை அறிந்துநோக்க வல்லீரேல்  
உத்தமத்துள் ஆயசோதி உணரும்போகம் ஆகுமே  

Marked reading: Carrying books, you babble lies; you do not know how the place of dying and the place of being born are; if you could know and look at all that thought, the light within the Highest would become the enjoyment you know.

### siddhar:1714 (அகப்பேய்ச் சித்தர், அகப்பேய்ச் சித்தர் பாடல்கள்)

சொல்ல லாகாதே .....அகப்பேய்!  
சொன்னாலும் தோடமடி  
இல்லை இல்லையடி .....அகப்பேய்!  
ஏகாந்தங் கண்டாயே  

Marked reading: It must not be said, demon; even if said, it is a fault; no, no: you have seen solitude.

### siddhar:1729 (அகப்பேய்ச் சித்தர், அகப்பேய்ச் சித்தர் பாடல்கள்)

தோன்றும் வினைகளெல்லாம் .....அகப்பேய்!  
சூனியங் கண்டாயே  
தோன்றாமல் தோன்றிவிடும் .....அகப்பேய்!  
சுத்த வெளிதனிலே  

Marked reading: All the deeds that appear, demon, you have seen to be void; they appear without appearing, in the pure space.

### siddhar:1870 (கொங்கணச் சித்தர், வாலைக் கும்மி)

அந்தரி சுந்தரி வாலைப்பெண் ணாமந்த  
அம்பிகை மேற்கும்மி பாடுதற்குச்  
சிந்தையில் முந்திநல் விந்தையாய் வந்திடும்  
நந்தீசர் பொற்பதங் காப்பாமே  

Marked reading: Antari and Sundari are the Maiden; to sing the kummi on that Ambika, the golden feet of Nandi, who comes first into the thought as a fine wonder, are our protection.

### siddhar:2004 (பாம்பாட்டிச் சித்தர், பாம்பாட்டிச் சித்தர் பாடல்)

எட்டுநாகந் தம்மைக்கையா லெடுத்தேயாட்டுவோம்  
இந்திரனார் உலகத்தை இங்கே காட்டுவோம்  
கட்டுக்கடங் காதபாம்பைக் கட்டி விடுவோம்  
கடுவிஷத் தன்னைக்கக்கி யாடு பாம்பே  

Marked reading: We will take the eight nagas in our hands and make them dance, we will show Indra's world right here, we will bind and release the snake that no binding holds; spit out your fierce poison and dance.

### siddhar:2036 (பாம்பாட்டிச் சித்தர், பாம்பாட்டிச் சித்தர் பாடல்)

மின்னற்கொடி யென்றுஞ்சோதி விளக் கென்றும்  
மெல்லியென்றும் வல்லியென்றும் மேனகை யென்றும்  
கன்னற்கட்டி யென்றுஞ்சீனிக் கற்கண் டென்றும்  
கழறாமற் கடிந்தோமென் றாடாய் பாம்பே  

Marked reading: Lightning-creeper, bright lamp, slender one, vine, Menaka, cane-sugar lump, sugar-candy: we have scolded these away without uttering them; dance.

### siddhar:2098 (பாம்பாட்டிச் சித்தர், பாம்பாட்டிச் சித்தர் பாடல்)

மூலத் தலத்திலே நின்ற கருத்தை  
முற்றுஞ் சுழுமுனை தன்னி லூடே  
மேலத் தலத்திலே விந்து வட்டம்  
வேலை வழியிலே மேவி வாழும்  
பாலத் திருத்தாய்க் கருணை யதனால்  
பரகதி ஞானசொ ரூபமாகி  
ஆலச் சயனத்து மாலுட னின்றே  
ஆனந்தஞ் சேர்ந்தோமென் றாடாய் பாம்பே  

Marked reading: Taking the thought that stood at the root place up through the whole sushumna to the bindu-circle in the upper place, it lives on that path; by the compassion of the holy young mother, becoming the form of knowledge of the supreme state, standing with Mal who sleeps on the banyan leaf, we joined bliss.

### siddhar:2287 (கஞ்சமலைச் சித்தர், கஞ்சமலைச் சித்தர் பாடல்)

பேச்சினால் என்னென்ன தோணும்-சும்மா  
பேசப்பேசப் பிழைஅல்லோ காணும்  
வாச்சுத லால்அம்பு பூணும்-நல்ல  
மாசற்ற ஞான விசாரணை வேணும்  

Marked reading: What does talk bring to light? Talking and talking is nothing but error, is it not? Because of ... one wears the arrow; what is needed is a flawless inquiry of jnana.

### siddhar:2349 (காகபுசுண்டர், காகபுசுண்டர் ஞானம்)

தானென்ற பிரமத்தை யடுத் திடாமல்  
தாரணியில் தெய்வமடா அனந்த மென்றும்  
ஊனென்ற குருவென்றுஞ் சீட னென்றும்  
உதயகிரி பாராத வுலுத்த மாடு  
வேனென்ற பொய்களவு கொலைகள் செய்து  
வேசையர்மே லாசைவைத்து வீண னாகிக்  
கோனென்ற குருபாதம் அடைய மாட்டான்  
கூடுவான் நரகமதில் வீழ்வான் பாரே  

Marked reading: Not approaching the Brahman that is self, saying the gods on earth are endless and this one a guru and that one a disciple, cattle that never saw the hill of rising, doing lies, theft and murder, lusting after prostitutes and becoming vain, such a one will not reach the guru's feet; he will fall into hell.

### siddhar:2377 (காகபுசுண்டர், காகபுசுண்டர் ஞானம்)

தானென்ற சிறுவீட்டுக் குள்ளே சென்று  
தலைமாறிப் போனதொரு வாசி யைத்தான்  
கோனென்ற பிரமத்தி லடக்க மாகக்  
குறித்திடுவாய் மனமடங்கிக் கூர்ந்து பார்க்க  
வானொன்றிப் போகுமடா பாணம் பாணம்  
மைந்தனே! உண்டிடவே பசிதான் தீரும்;  
தேனென்ற சட்டை களுங் கழன்று போகும்  
தேனுக்குந் தேவனா யிருக்க லாமே  

Marked reading: Entering the small house called self, fix the breath that has turned its head so that it subsides in Brahman called the king; with mind subdued look closely; the arrow joins the sky; when you eat, son, hunger ends; the coats slip off, and one can be a god even to the gods.

### siddhar:2436 (அகஸ்தியர், அகஸ்தியர் ஞானம்)

வாழாமல் உலகம்விட்டு வேடம் பூண்டு  
வயிற்றுக்கா வாய்ஞானம் பேசிப் பேசித்  
தாழ்வான குடிதோறும் இரப்பான் மட்டை  
தமையறியாச் சண்டாளர் முழுமா டப்பா!  
பாழாகப் பாவிகளின் சொற்கே ளாதே  
பதறாதே வயிற்றுக்கா மயங்கிடாதே;  
கேளாதே பேச்செல்லாங் கேட்டுக் கேட்டுக்  
கலங்காதே யுடலுயிரென் றுரைத்தி டாதே  

Marked reading: He who does not live, leaves the world, puts on the garb, talks and talks mouth-knowledge for his belly and begs from every low house is a husk, a chandala who does not know himself, a whole ox; do not listen to the words of such sinners and perish, do not panic, do not be bewildered for the belly; do not listen, do not keep hearing all the talk and be shaken, and do not say 'body and life' as two.

