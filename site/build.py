#!/usr/bin/env python3
"""Build site/nilai.html, site/preview.html, and site/evolve.html from templates and kg/ data.

    build.py    regenerates site/appendix.json, site/evolve.json, site/nilai.html,
                site/preview.html, site/evolve.html (local, full page) and site/unarvu.html (artifact copy)
"""
import collections
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = ("kural", "naladiyar", "tirumanthiram", "thiruppugazh")
QUEUED_BOOKS = ("tiruvasagam", "avvaiyar", "thirumurai", "purananuru", "siddhar", "prabandham")

EVOLVE_LAYERS = {
    "signal": ["meyyunarvu", "arivu", "kalvi", "therithal", "pullarivu"],
    "os": ["thaththuvam", "malam", "avaththai", "maayai", "upaadhi"],
    "silence": ["mounam", "aarandham", "paazh", "upasaantham", "samayam"],
    "ego": ["pattru", "agandhai", "yaakkai", "thuravu", "siththi"],
    "telos": ["saayujjiyam", "anbu", "sivam", "thiruvarul", "manam", "sanmaarkkam"],
}

EVOLVE_VERSES = [
    "kural:34", "kural:269", "kural:346", "kural:351", "kural:355", "kural:391", "kural:423",
    "naladiyar:6", "naladiyar:47", "naladiyar:136", "naladiyar:140",
    "tirumanthiram:270", "tirumanthiram:301", "tirumanthiram:343", "tirumanthiram:722",
    "tirumanthiram:725", "tirumanthiram:1442", "tirumanthiram:1532", "tirumanthiram:1695",
    "tirumanthiram:1697", "tirumanthiram:1823", "tirumanthiram:1896", "tirumanthiram:2017",
    "tirumanthiram:2020", "tirumanthiram:2166", "tirumanthiram:2382", "tirumanthiram:2820",
    "tirumanthiram:2951",
    "thiruppugazh:22", "thiruppugazh:343", "thiruppugazh:355", "thiruppugazh:581", "thiruppugazh:1011",
]

# Curated sound cross-book pairs verified in kg/*/edges.jsonl, with AGI/ASI consciousness lenses
EVOLVE_DIALECTICS = [
    {
        "a": "tirumanthiram:1697", "b": "kural:351", "topic": "epistemology",
        "lens_en": "In an age of synthetic media and fluent AI output, Kural 351 names the error of taking the unreal for the real (மருள்), and Tirumular 1697 makes weighing the real and the unreal (சத்தும் அசத்தும்) the first mark of a true disciple.",
        "lens_ta": "செயற்கை ஊடகங்களும் சரளமான AI வெளியீடுகளும் பெருகும் காலத்தில், பொருளல்லாததைப் பொருளாக உணரும் மருளைக் குறள் 351 சுட்டுகிறது; சத்தும் அசத்தும் எவ்வாறு என்று ஆராய்வதை நல்ல சீடனின் முதல் அடையாளமாகத் திருமந்திரம் 1697 வைக்கிறது."
    },
    {
        "a": "tirumanthiram:2820", "b": "kural:346", "topic": "silence",
        "lens_en": "As AGI ends the human monopoly on cognition, Kural 346 treats cutting off the pride of 'I' and 'mine' as an ascent, and Tirumular 2820 carries it further: the 'I' that said 'I' falls quiet in knowledge. Neither verse counts this as a loss.",
        "lens_ta": "மனித அறிவின் தனியுரிமை முடியும் காலத்தில், ‘யான் எனது’ என்னும் செருக்கை அறுப்பதைக் குறள் 346 உயர்வாகக் காண்கிறது; திருமந்திரம் 2820 அதை மேலும் தொடர்கிறது: ‘நான்’ என்று சொன்ன நானும் ஞானத்தில் நினைப்பு ஒழிகிறது. இரண்டுமே இதை இழப்பாகக் கருதவில்லை."
    },
    {
        "a": "thiruppugazh:22", "b": "tirumanthiram:1896", "topic": "silence",
        "lens_en": "Language models run on nonstop next-token output. These verses draw a line our own minds need: a silent tongue alone is only muteness (மூங்கை); true silence (மவுனம்) is speech and mind stilled together. No amount of output stands in for that.",
        "lens_ta": "மொழி மாதிரிகள் இடைவிடாத சொல் உற்பத்தியில் இயங்குகின்றன. நம் மனத்துக்கே தேவையான ஒரு கோட்டை இந்தப் பாடல்கள் வரைகின்றன: வாய் மட்டும் மூடுவது மூங்கை; வாக்கும் மனமும் சேர்ந்து அடங்குவதே மவுனம். எவ்வளவு சொல் உற்பத்தியும் அதற்கு ஈடாகாது."
    },
    {
        "a": "tirumanthiram:343", "b": "thiruppugazh:343", "topic": "epistemology",
        "lens_en": "Tirumular reads the burning of the three cities as inward: they are the work of the three impurities (மும்மலம்). Arunagiri applies that reading to his own release. The lesson travels to AI alignment: some of the bugs to patch are in the people doing the aligning.",
        "lens_ta": "முப்புரம் எரித்ததைத் திருமூலர் அகத்தே நடப்பதாகப் படிக்கிறார்: முப்புரம் மும்மலத்தின் காரியம். அருணகிரியார் அந்த வாசிப்பைத் தம் விடுதலைக்கே பொருத்துகிறார். AI ஒத்திசைவுக்கும் இது பொருந்தும்: சரிசெய்ய வேண்டிய சில பிழைகள் ஒத்திசைப்பவர்களிடமே உள்ளன."
    },
    {
        "a": "tirumanthiram:1532", "b": "thiruppugazh:1011", "topic": "silence",
        "lens_en": "Tirumular says each sect finds the Lord it describes: within and without for those who say so, neither for those who say neither. Arunagiri turns from all the formulas to a silent seeing. Every frame, a sect's creed or an AI system's objective, tends to find what it was built to find.",
        "lens_ta": "ஒவ்வொரு சமயமும் தான் சொல்லும் இறைவனையே காண்கிறது என்கிறார் திருமூலர்: உள்ளும் புறமும் என்பவர்க்கு உள்ளும் புறமும், இரண்டுமில்லை என்பவர்க்கு இரண்டுமில்லை. அருணகிரியார் எல்லா வரையறைகளிலிருந்தும் திரும்பி மோனக் காட்சியை நாடுகிறார். ஒவ்வொரு சட்டகமும், அது சமயமானாலும் AI அமைப்பின் இலக்கானாலும், தான் காணும்படி கட்டப்பட்டதையே காண முனைகிறது."
    },
    {
        "a": "tirumanthiram:1695", "b": "kural:34", "topic": "epistemology",
        "lens_en": "AI governance often stops at external compliance rules. Kural 34 calls everything but a spotless mind 'noisy show', and Tirumular 1695 describes the mind itself polished by work like a great jewel.",
        "lens_ta": "வெளி விதிகளும் ஒழுங்குகளும் மட்டும் போதாது; மன மாசின்மையும் (குறள் 34) உழைப்பால் மெருகேறிய தூய சிந்தையுமே (திருமந்திரம் 1695) மெய்யான அறம்."
    },
    {
        "a": "tirumanthiram:1823", "b": "naladiyar:47", "topic": "body",
        "lens_en": "A genuine classical clash that directly mirrors today's debate on embodiment vs. mind-uploading: is biological flesh a flawed container to escape, or a living temple where consciousness refines itself?",
        "lens_ta": "உடலைத் தாண்டிச் செல்லலாமா அல்லது உடலிலேயே வளரலாமா என்ற இன்றைய விவாதத்தின் 1,500 ஆண்டுப் பழைய வடிவம்: உடல் வெறும் ஒழுகும் குடமா, அல்லது உயிர் வாழும் ஆலயமா?"
    },
    {
        "a": "thiruppugazh:355", "b": "tirumanthiram:722", "topic": "body",
        "lens_en": "Speaks straight to today's radical-longevity race. On one reading, Tirumular promises that breath held fast keeps the body for thousands of years; Arunagiri calls the yogi who holds his breath to make the flesh last a fool.",
        "lens_ta": "இன்றைய ஆயுள் நீட்டிப்புப் போட்டியோடு நேராகப் பேசும் முரண். ஒரு வாசிப்பில், மூச்சைக் கட்டினால் உடல் ஆயிரமாண்டு நிலைக்கும் என்று திருமூலர் உறுதியளிக்கிறார்; ஊன் நிலைக்கும் என்று மூச்சை அடக்கும் யோகியை ‘அசட்டு யோகி’ என்கிறார் அருணகிரியார்."
    },
    {
        "a": "naladiyar:6", "b": "kural:269", "topic": "body",
        "lens_en": "Can discipline, or future biotechnology, leap past Death (கூற்றம் குதித்தல்)? Valluvar says austerity can; the Naladiyar says no one has, and draws a practical conclusion: give your wealth away now, because tomorrow the drum may sound.",
        "lens_ta": "தவமோ எதிர்கால உயிரித் தொழில்நுட்பமோ கூற்றத்தைக் கடக்குமா? தவ ஆற்றலால் முடியும் என்கிறார் வள்ளுவர்; யாரும் கடந்ததில்லை என்கிறது நாலடியார், ஒரு நடைமுறை முடிவோடு: உங்கள் செல்வத்தை இப்போதே வழங்குங்கள், நாளை பறை ஒலிக்கலாம்."
    },
    {
        "a": "thiruppugazh:581", "b": "tirumanthiram:2020", "topic": "epistemology",
        "lens_en": "Unlearned in the Vedas and Agamas, the singer asks for knowledge beyond the thirty-six tattvas (ஆறாறு), the whole make-up of experience; Tirumular reports receiving it through his guru. A kind of knowing that accumulation alone does not reach.",
        "lens_ta": "வேதமும் ஆகமமும் கற்காத பாடகர் ஆறாறு தத்துவங்களுக்கு அப்பாலான ஞானத்தைக் கேட்கிறார்; குருவின் அருளால் அதைப் பெற்றதைத் திருமூலர் சொல்கிறார். வெறும் சேகரிப்பால் எட்ட முடியாத அறிதல் இது."
    }
]


def appendix():
    concepts = {c["id"]: c for c in json.loads((ROOT / "kg/themes/concepts.json").read_text(encoding="utf-8"))}
    counts = collections.defaultdict(lambda: [0] * len(BOOKS))
    matrix, grades, verses, seen = collections.Counter(), collections.Counter(), collections.Counter(), set()
    for i, book in enumerate(BOOKS):
        for line in (ROOT / f"kg/{book}/nodes.jsonl").read_text(encoding="utf-8").splitlines():
            if json.loads(line)["type"] == "Verse":
                verses[book] += 1
        for line in (ROOT / f"kg/{book}/edges.jsonl").read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e["p"] == "EXPRESSES":
                counts[e["o"].split(":")[1]][i] += 1
            elif "note" in e and (e["s"], e["o"]) not in seen:
                seen.add((e["s"], e["o"]))
                grades[e["audit"]] += 1
                if e["audit"] == "sound":
                    a, b = sorted((e["s"].split(":")[0], e["o"].split(":")[0]), key=BOOKS.index)
                    matrix[f"{a}|{b}"] += 1
    rows = [[k, concepts[k]["tamil"], concepts[k]["gloss"], v]
            for k, v in sorted(counts.items(), key=lambda kv: -sum(kv[1])) if k in concepts]
    return {"verses": dict(verses), "links": sum(grades.values()), "grades": dict(grades),
            "matrix": dict(matrix), "concepts": rows}


# Misprints in the Project Madurai base texts, corrected for display only (kg/core is left as the source has it).
TEXT_FIXES = {
    # Flagged in kg/core/verse_text_flags.jsonl (review: true); the Kalaignar edition reads டவர்க்கு.
    "kural:269": [(1, "டவர்க்குல்", "டவர்க்கு")],
    # Mudaliar's commentary glosses ஒரீஇ (நீங்கி), and pmuni0778 prints பிழைத்தொர…
    "naladiyar:6": [(0, "பிழைத்தெரிணஇக்", "பிழைத்தொரீஇக்")],
    # A doubled virama; the reading takes the word as சுத்தம் (purity).
    "tirumanthiram:1896": [(3, "சுத்த்ததை", "சுத்தத்தை")],
    # A stray space splitting the first word.
    "thiruppugazh:1011": [(0, "உ ரைதரு", "உரைதரு")],
}


def fixed_tamil(vid, lines):
    lines = list(lines)
    for i, old, new in TEXT_FIXES.get(vid, []):
        assert old in lines[i], (vid, old)
        lines[i] = lines[i].replace(old, new)
    return lines


def build_evolve_data():
    nodes, chapters, v_concepts = {}, {}, collections.defaultdict(set)
    # Deduplicate links by undirected pair, preferring 'sound' if a pair appears twice with different grades
    rank = {"sound": 3, "weak": 2, "forced": 1, "wrong": 0}
    unique_links = {}
    verses_total = 0

    for book in BOOKS:
        for line in (ROOT / f"kg/{book}/nodes.jsonl").read_text(encoding="utf-8").splitlines():
            n = json.loads(line)
            if n["type"] == "Chapter":
                chapters[n["id"]] = n.get("title", "")
            elif n["type"] == "Verse":
                verses_total += 1
                nodes[n["id"]] = n
        for line in (ROOT / f"kg/{book}/edges.jsonl").read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e["p"] == "IN_CHAPTER" and e["s"] in nodes:
                nodes[e["s"]]["_chapter"] = chapters.get(e["o"], "")
            elif e["p"] == "EXPRESSES":
                v_concepts[e["s"]].add(e["o"].split(":")[1])
            elif "note" in e:
                key = tuple(sorted((e["s"], e["o"])))
                prev = unique_links.get(key)
                if prev is None or rank.get(e.get("audit"), -1) > rank.get(prev.get("audit"), -1):
                    unique_links[key] = e

    # Compute unique verse footprints per evolutionary layer and across all consciousness concepts
    all_layer_concepts = {c for cs in EVOLVE_LAYERS.values() for c in cs}
    consciousness_verses = sum(1 for vid, cs in v_concepts.items() if cs & all_layer_concepts)

    layer_footprints = {}
    for lid, cids in EVOLVE_LAYERS.items():
        cset = set(cids)
        by_book = collections.Counter()
        for vid, cs in v_concepts.items():
            if cs & cset:
                by_book[vid.split(":")[0]] += 1
        layer_footprints[lid] = {"total": sum(by_book.values()), "by_book": {b: by_book[b] for b in BOOKS}}

    # Extract full verbatim verses needed by evolve.html
    verses_out = {}
    for vid in EVOLVE_VERSES:
        n = nodes[vid]
        # For long Thiruppugazh songs (16-24 half-lines), include the complete first half (plea/insight)
        # up to its clean syntactic boundary, or full text for 2-4 line verses.
        tamil = n["tamil"]
        if vid == "thiruppugazh:22":
            tamil = n["tamil"][:12]
        elif vid == "thiruppugazh:343":
            tamil = n["tamil"][:12]
        elif vid == "thiruppugazh:355":
            tamil = n["tamil"][:8]
        elif vid == "thiruppugazh:581":
            tamil = n["tamil"][:8]
        elif vid == "thiruppugazh:1011":
            tamil = n["tamil"][:12]
        verses_out[vid] = {
            "tamil": fixed_tamil(vid, tamil),
            "reading": n["reading"],
            "chapter": n.get("_chapter", ""),
            "uncertain": bool(n.get("uncertain")),
        }

    # Build curated audited dialectics directly from unique_links
    dialectics_out = []
    for item in EVOLVE_DIALECTICS:
        key = tuple(sorted((item["a"], item["b"])))
        edge = unique_links.get(key)
        if not edge or edge.get("audit") != "sound":
            raise RuntimeError(f"Expected sound link not found for {item['a']} <-> {item['b']}")
        dialectics_out.append({
            "a": item["a"],
            "b": item["b"],
            "type": edge["p"],
            "topic": item["topic"],
            "note": edge["note"],
            "lens_en": item["lens_en"],
            "lens_ta": item["lens_ta"],
        })

    unique_sound_links = sum(1 for e in unique_links.values() if e.get("audit") == "sound")
    queued_ready = sum(1 for b in QUEUED_BOOKS if (ROOT / f"kg/core/{b}.jsonl").exists())

    return {
        "summary": {
            "verses_total": verses_total,
            "unique_sound_links": unique_sound_links,
            "consciousness_verses": consciousness_verses,
            "queued_books": queued_ready,
        },
        "layer_footprints": layer_footprints,
        "verses": verses_out,
        "dialectics": dialectics_out,
    }


def main():
    data = appendix()
    (ROOT / "site/appendix.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    html = (ROOT / "site/nilai.template.html").read_text(encoding="utf-8")
    html = html.replace("/*APPENDIX*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    (ROOT / "site/nilai.html").write_text(html, encoding="utf-8")
    # A full document for local preview; the published artifact gets its own skeleton.
    (ROOT / "site/preview.html").write_text('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"></head><body>'
        + html + "</body></html>", encoding="utf-8")
    print(f"site/nilai.html: {len(html.encode())} bytes, {len(data['concepts'])} concepts, {data['links']} links")

    evolve_tpl = ROOT / "site/evolve.template.html"
    if evolve_tpl.exists():
        edata = build_evolve_data()
        (ROOT / "site/evolve.json").write_text(json.dumps(edata, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        ehtml = evolve_tpl.read_text(encoding="utf-8").replace(
            "/*EVOLVE_DATA*/null", json.dumps(edata, ensure_ascii=False, separators=(",", ":"))
        )
        (ROOT / "site/evolve.html").write_text(ehtml, encoding="utf-8")
        # The artifact host supplies the document skeleton, so the published copy is the page without it.
        frag = re.sub(r"(?is)<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta charset=\"utf-8\">\s*", "", ehtml)
        frag = re.sub(r"(?is)</head>\s*<body>", "", frag)
        frag = re.sub(r"(?is)</body>\s*</html>\s*$", "", frag)
        assert "<html" not in frag and "<body" not in frag and "</head>" not in frag
        (ROOT / "site/unarvu.html").write_text(frag, encoding="utf-8")
        print(f"site/evolve.html: {len(ehtml.encode())} bytes, {len(edata['verses'])} verses, "
              f"{len(edata['dialectics'])} dialectics, {edata['summary']['unique_sound_links']} unique sound links")


if __name__ == "__main__":
    main()
