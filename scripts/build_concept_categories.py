import json,sys
sys.path.insert(0,'.')
from tax import T
ESS = {
"aram":"Across the ethics books and beyond, virtue is judged by whether the mind matches the act: giving goes with a glad face, truth is measured by its harmlessness, restraint guards the senses, and harm done is said to return to the doer.",
"porul":"Wealth is praised for what it lets one give and blamed when hoarded; the ethics books tie the king to the just sceptre as the world is tied to rain, and the puram poems measure a king by his gifts to bards and his valour in the field.",
"inbam":"Love is read through the body and the land: the friend speaks for the lovers, gossip and the mother's watch press toward marriage, slipping bangles and pallor testify in separation before the woman speaks, and the sulk is prized only in measure.",
"veedu":"Birth is the evil and craving its seed: the Naladiyar, Tirumanthiram and Siddhars counsel giving up and knowing, the Saiva texts grade release up to union with Siva, and the Jain and Buddhist epics give it to the three jewels or the perfections.",
"udal":"The body is a frame that will not last, a leaking pot in the Naladiyar and a womb-born thing the Siddhars use to shame pride of caste; yet the Tirumanthiram and Siddhars also make it the field of practice, kept alive by breath, kalpa and nectar.",
"ullam":"The mind decides what an act is worth: outward observance without a clean mind is show; Tirumular maps waking, dream and sleep onto the tattvas, and the debate epics argue whether awareness is a lasting soul, a stream of moments or the elements combined.",
"irai":"The Kural names the Lord only by epithet, the Paripadal and Thiruppugazh praise Thirumal and Murugan, and the Tirumanthiram teaches Siva pervading all; across them grace comes to those who take refuge at his feet, while the Siddhars mock sect and outward rite.",
"yogam":"In the Tirumanthiram and the Siddhar songs the breath is the practice: ridden like a horse, held in the channels and raised through the centres to the crown where sun and moon become one, written in cipher and given only by a guru.",
"iyarkai":"Rain is the condition of life and the image of just rule; in the akam poems the seasons and the hour of evening keep time for love, the promised rains stand as proof of the absent man's return, and the wild road carries both danger and knowledge.",
"samugam":"The books pull both ways on birth: the Kural makes conduct flow from good family and also makes family a name earned by conduct, the Siddhars turn the womb's impurity against caste, and the Jain epics turn on refusing blood sacrifice.",
"aivu":"Learning is the wealth that does not decay, yet conduct can cancel it and fate can limit it; the Manimekalai and Neelakesi stage formal debate in which Buddhist, Jain, Ajivika, Sankhya and materialist views are tried by the means of valid knowledge.",
"pulamai":"Tamil stands beside Sanskrit as a tongue of revelation in the Tirumanthiram, the Paripadal weighs Madurai on the balance of learning, the puram poems turn battle and grief into named kinds of song, and the epics treat music and dance-drama as learned arts.",
"kaalam":"Youth, wealth and the body pass like lightning and Death roams looking for his own, so give and do good now; former deeds return to the doer, though the Kural lets unflagging effort see fate's back, and the puram poems answer death with hero-stones and renown.",
}
ids=[c['id'] for c in json.load(open('/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/themes/concepts.json'))]
cats=[]; place={}
for cid,ta,en,gl,glta,subs in T:
    S=[]
    for sid,sta,sen,sgl,prim,sec in subs:
        full=f"{cid}.{sid}"
        S.append({"id":full,"tamil":sta,"name":sen,"gloss":sgl,"concepts":prim,"also":sec})
        for x in prim:
            assert x not in place, x
            place[x]={"primary":full,"secondary":[]}
    cats.append({"id":cid,"tamil":ta,"name":en,"gloss":gl,"gloss_ta":glta,"essence":ESS[cid],"subthemes":S})
for c in cats:
    for s in c["subthemes"]:
        for x in s["also"]:
            assert x in place, x
            if s["id"]!=place[x]["primary"]: place[x]["secondary"].append(s["id"])
missing=[i for i in ids if i not in place]; extra=[i for i in place if i not in ids]
assert not missing and not extra, (missing, extra)
for c in cats: assert 4<=len(c["subthemes"])<=10, c["id"]
out={"about":"Two-level taxonomy of the explorer's concepts: the four classical aims (aram, porul, inbam, veedu) and nine cross-cutting families. Every concept has one primary subtheme ('concepts') and may be listed as secondary ('also') elsewhere. Glosses and essence lines are written for this graph from its own concept glosses and verse readings; no translation or commentary text.",
     "categories":cats,"placement":{i:place[i] for i in ids}}
open('/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/themes/concept_categories.json','w',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=1)+"\n")
print("ok", len(place), "placed;", sum(len(p['secondary']) for p in place.values()), "secondary")
for c in cats: print(f"  {c['tamil']} {c['name']}: {sum(len(s['concepts']) for s in c['subthemes'])} concepts, {len(c['subthemes'])} subthemes")
# search words: Sanskrit or English equivalents a reader may type, and the concept list's own aliases
KW = {
 "aram":["dharma","virtue","righteousness"],"vinai":["karma","action","deeds"],"oozh":["fate","destiny","karma","niyati"],
 "piravi":["samsara","rebirth","transmigration"],"veedu":["moksha","mukti","liberation","salvation"],"kaamam":["kama","lust"],
 "thavam":["tapas","penance"],"thuravu":["sannyasa","asceticism"],"gnaanam":["jnana","wisdom"],"arul":["karuna","mercy"],
 "thiruvarul":["grace","anugraha"],"praanan":["pranayama","breath control"],"vaasi":["vasi yoga","breathing"],
 "naadi":["nadi","ida","pingala"],"suzhumunai":["sushumna"],"kundalini":["shakti","serpent power"],"aadhaaram":["chakra","muladhara"],
 "yogam":["yoga"],"thiyaanam":["dhyana","meditation"],"samaadhi":["samadhi","absorption"],"mandhiram":["mantra"],
 "piranavam":["om","aum","pranava"],"maayai":["maya","illusion"],"malam":["mala","impurity","anava"],"selvam":["wealth","riches","artha"],
 "porai":["patience","kshama"],"kollaamai":["ahimsa","non-violence"],"pulaal":["vegetarian","meat"],"vaaimai":["satya","truth"],
 "kalvi":["education","study"],"arivu":["knowledge","intelligence","wisdom"],"manam":["mind","manas"],"nenju":["heart"],
 "meyyunarvu":["truth","realisation"],"avaththai":["avastha","waking","dream","turiya","consciousness"],"mukkunam":["gunas","sattva","rajas","tamas"],
 "pori":["senses","indriya"],"noy":["illness","sickness","medicine"],"marundhu":["medicine","cure","herbal"],"karpam":["kaya kalpa","rejuvenation"],
 "vaadham":["alchemy","rasavada"],"yaakkai":["body","flesh"],"nilaiyaamai":["anitya","transience"],"kootru":["yama","death"],
 "saakkaadu":["dying","death"],"sivam":["shiva","siva"],"iraivan":["god","lord","deity"],"paththi":["bhakti","devotion"],
 "puththan":["buddha"],"theerththagarar":["tirthankara","jina"],"arathanathirayam":["ratnatraya","three jewels"],"saarbu":["pratityasamutpada","dependent origination"],
 "kandham":["skandha","aggregates"],"kanam":["kshana","moment"],"alavai":["pramana","epistemology"],"anu":["atom","paramanu"],
 "pakuthi":["prakriti","sankhya"],"boothavaadham":["lokayata","charvaka","materialism"],"aaseevagam":["ajivika"],"vedham":["veda","vedic"],
 "velvi":["yajna","sacrifice"],"thamizh":["tamil","language"],"mazhai":["rain","monsoon"],"pirivu":["separation","viraha"],
 "kalaviyal":["kalavu","secret love","premarital"],"oodal":["sulking","lovers' quarrel"],"arasu":["king","state","polity"],
 "sengol":["justice","just rule","sceptre"],"maram":["valour","heroism","courage"],"natpu":["friend","friendship"],
 "ilvaazhkkai":["grihastha","householder","family"],"eegai":["charity","generosity","dana"],"guru":["teacher","master"],
 "isai":["music","raga"],"koothu":["dance","drama","theatre"],"nadukal":["hero stone","memorial"],"aatruppadai":["guide poem"],
 "uzhavu":["agriculture","farming","plough"],"koothir":["winter","cold season"],"ilavenil":["spring"],"thinai":[],
}
data=json.load(open('/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/themes/concept_categories.json',encoding='utf-8'))
al={c['id']:c.get('aliases',[]) for c in json.load(open('/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/themes/concepts.json'))}
for cid,p in data["placement"].items():
    kw=list(dict.fromkeys(KW.get(cid,[])+al.get(cid,[])))
    if kw: p["keywords"]=kw
data["about"]+=" 'keywords' are extra search words (Sanskrit or English equivalents, and the concept list's aliases)."
open('/Users/harilakshmanan/Cursor/cosci_knowledge_graph/kg/themes/concept_categories.json','w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,indent=1)+"\n")
print("keywords on", sum(1 for p in data["placement"].values() if "keywords" in p))
