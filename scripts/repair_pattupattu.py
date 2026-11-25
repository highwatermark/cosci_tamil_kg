#!/usr/bin/env python3
"""Repairs to the Pattupattu verse text, applied by scripts/build_sangam_core.py.

Not run on its own: build_sangam_core.py loads this file, calls repair() on each idyll after its
own character repairs, and writes the log to kg/core/pattupattu_repairs.jsonl (one record per
change, "action": "changed", and one per checked reading that is deliberately left alone,
"action": "kept"). Each change and each kept reading is also flagged in sangam_text_flags.jsonl.

Run (through the build): python3 -I scripts/build_sangam_core.py

Authorities (only these count):
  tvu    tamilvu.org, Tamil Virtual Academy library l1100 (பத்துப்பாட்டு), U. V. Swaminatha
         Aiyar's edition with Nachinarkkiniyar's commentary, verse lines of the pages
         /slet/l1100/l1100pd1.jsp?bookid=20&auth_pub_id=68&pno=<page> (the page is given below)
  pm     the Project Madurai base text itself (pmuni0063-0078, pmuni0488). The 2000 versions of
         the same files on projectmadurai.org were also collated: they carry every fault below
         unchanged, so they are one witness with the base text, not a second authority.
Only short readings (a word or a few letters of a verse line) are written here. No commentary is
copied. tvu's own text has encoding losses of its own (ை dropped, ெ/ோ printed as a quote mark in
Sirupanatruppadai); its readings are given as printed.

Rules:
  * Where tvu has the reading and the base text has a form that is not a word (a lost vowel
    sign, an impossible letter cluster, a stray or doubled letter, words run together by a
    punctuation mark), the base text is corrected. The base text's own word division is kept:
    only the faulty letters change, never the edition's sandhi or spacing style.
  * Where the editions differ but the base reading is a possible word, our reading is kept and
    logged ("kept") so that it is flagged, not changed.
  * A genuine -அடு (அடும்பு, the verb அடு) is never turned into -ஒடு: those places are listed in
    GENUINE_ADU and the script refuses to run if the -ஒடு rule finds a place in neither table.
"""
import re

TVU = "tvu (tamilvu.org l1100, U. V. Swaminatha Aiyar's text)"
PM = "pm (the Project Madurai base text)"

# ---------------------------------------------------------------------------------------------
# (a) The vowel sign ொ is lost after ய and ள in these e-texts, so the comitative -ஒடு is printed
# யடு / ளடு (the same fault as in Purananuru, see scripts/repair_purananuru.py). The rule finds
# யடு / ளடு at the end of a word (or before -ம்). Every hit was checked against tvu; the table
# gives tvu's word as printed and its page.
ODU_RULE = re.compile(r"([யள])டு(?=ம்|[^஀-௿]|$)")
ODU_CHECKED = {  # (poem, line): (tvu reading, tvu page)
    (1, 23): ("வுத்தியொடு", 5), (1, 49): ("கூகையொடு", 8), (1, 79): ("யோடையொடு", 11),
    (1, 84): ("முடியொடு", 12), (1, 102): ("வள்ளியொடு", 13), (1, 114): ("தொடியொடு", 14),
    (1, 175): ("மடந்தையொடு", 19), (1, 191): ("குளவியொடு", 20), (1, 212): ("றொகுதியொடு", 22),
    (1, 219): ("கொடியொடு", 23), (1, 227): ("கொடியொடு", 24), (1, 228): ("நெய்யோ டையவி", 24),
    (1, 233): ("குருதியொடு", 25), (1, 235): ("மஞ்சளொடு", 25), (1, 240): ("யருவியொ டின்னியங்", 25),
    (2, 44): ("நோயொடு", 86), (2, 125): ("குழவியொடு", 92), (2, 214): ("தேனெய்யொடு", 99),
    (2, 215): ("மீனெய்யொடு", 99), (2, 217): ("மான்குறையொடு", 99), (3, 55): ("ரொழுகையொடு", 134),
    (3, 92): ("புரவியொடு", 137), (3, 110): ("காரியொடு", 138), (3, 126): ("கொள்கயொடு", 139),
    (3, 142): ("யானயொடு", 140), (3, 195): ("கலவையொடு", 144), (3, 226): ("பச்சையொடு", 146),
    (3, 246): ("வென்றியொடு", 147), (3, 253): ("நேமியொடு", 148), (4, 17): ("கனலியொடு", 181),
    (4, 27): ("புரவியொடு", 181), (4, 112): ("ஞமலியொடு", 187), (4, 120): ("பலகையொடு", 187),
    (4, 123): ("புதையொடு", 187), (4, 153): ("துருவையொடு", 189), (4, 176): ("நிரையொடு", 191),
    (4, 188): ("டுருளையொடு", 191), (4, 293): ("குவளையொடு", 198), (4, 299): ("கோழியொடு", 198),
    (4, 320): ("புரவியொடு", 199), (4, 345): ("தடியொடு", 201), (4, 434): ("வெறுக்கையொடு", 205),
    (4, 492): ("லிவுளியொடு", 209), (6, 172): ("செருந்தியொடு", 300),
    (6, 180): ("வியன்றானையொடு", 300), (6, 269): ("பாண்சேரியொடு", 307), (6, 276): ("பிணையொடு", 307),
    (6, 281): ("முசுண்டையொடு", 307), (6, 299): ("ளருவியொடு", 309), (6, 369): ("றானையொடு", 313),
    (6, 372): ("கொடியொடு", 313), (6, 434): ("வாளொடு", 318), (6, 557): ("நோயொடு", 325),
    (6, 607): ("மடையொடு", 327), (6, 677): ("புலியொடு", 331), (6, 720): ("தொடியொடு", 333),
    (7, 46): ("பெடையொடு", 436), (7, 82): ("நாளொடு", 438), (7, 84): ("தாழொடு", 438),
    (7, 142): ("வளையொடு", 441), (7, 169): ("ரோடையொடு", 443), (7, 178): ("பிடியொடு", 443),
    (9, 232): ("புரவியொடு", 526), (9, 241): ("குவளையொடு", 526), (9, 245): ("டிரலையொடு", 527),
    (9, 251): ("யானையொடு", 527), (9, 259): ("கூளியொடு", 527),
}
ODU_VARIANTS = {(1, 228): "tvu: நெய்யோ (-ஓடு)", (7, 84): "tvu: தாழொடு (ழ for ள)"}

# Genuine -அடு found by the same rule: left as they are (tvu reads the same).
GENUINE_ADU = {  # (poem, line): (tvu reading, tvu page, note)
    (2, 195): ("வறளடும்பி", 98, "அடும்பு, the beach creeper (வறள் அடும்பின்)"),
    (4, 339): ("கள்ளடு", 200, "கள் அடு மகளிர், women who brew toddy (அடு, to cook)"),
    (8, 87): ("யடும்பம", 471, "அடும்பு, the beach creeper (அடும்பமர் ஆத்தி)"),
    (9, 65): ("வறளடும்பின்", 517, "அடும்பு, the beach creeper"),
}

# ---------------------------------------------------------------------------------------------
# (b) Explicit edits: (poem, line, wrong, right, kind, tvu reading, tvu page, note). `wrong` must
# occur exactly once in the line as it stands after (a). kinds:
#   vowel_sign_o  the same lost ொ after ய / ள, here at the start of a joined word (யொழுகிய)
#   misprint      a letter typed wrong, doubled or dropped, giving a form that is not a word
#   spacing       two words run together across a punctuation mark
EDITS = (
    (1, 92, "ஒருமுகம்;ஒருமுகம்", "ஒருமுகம்; ஒருமுகம்", "spacing", "றொருமுக மொருமுக", 12, None),
    (1, 94, "தன்றே;ஒருமுகம்", "தன்றே; ஒருமுகம்", "spacing", "தன்றே யொருமுக", 12, None),
    (1, 96, "கும்மே;ஒருமுகம்", "கும்மே; ஒருமுகம்", "spacing", "கும்மே யொருமுக", 13, None),
    (1, 98, "கும்மே;ஒருமுகம்", "கும்மே; ஒருமுகம்", "spacing", "கும்மே யொருமுகஞ்", 13, None),
    (1, 100, "டன்றே;ஒருமுகம்", "டன்றே; ஒருமுகம்", "spacing", "டன்றே யொருமுகங்", 13, None),
    (1, 173, "மருங்கிந்தம்", "மருங்கிற்றம்", "misprint", "மருங்கிற்றம்", 18,
     "ந்த for ற்ற (மருங்கில் + தம்)"),
    (1, 188, "பெரிந்துஉவந்து", "பெரிதுஉவந்து", "misprint", "பெரிதுவந்", 19,
     "stray ந் (பெரிது உவந்து); the base text's joined spelling kept"),
    (1, 285, "பெரும!நின்", "பெரும! நின்", "spacing", "பெருமநின்", 29, None),
    (1, 295, "நல்கும்;அதி", "நல்குமதி", "misprint", "னல்குமதி", 30,
     "one word, நல்கு with the particle -மதி; the semicolon split it"),
    (1, 314, "கருந்கோட்டு", "கருங்கோட்டு", "misprint", "கருங்கோட்", 31, "ந்க is not possible: ங்க"),
    (2, 62, "யராஅல்", "யொராஅல்", "vowel_sign_o", "யொராஅல்", 87, "ஒராஅல்"),
    (2, 105, "கொழூங்குறை", "கொழுங்குறை", "misprint", "கொழுங்குறை", 91, "ூ for ு"),
    (2, 111, "யருநாள்", "யொருநாள்", "vowel_sign_o", "யொருநா", 91, "ஒருநாள்"),
    (2, 183, "மாங்திய", "மாந்திய", "misprint", "பலிமாந்திய", 98, "ங்த is not possible: ந்த"),
    (2, 206, "ஒங்கு திரை யலிவெரீ இத்", "ஓங்கு திரை யொலிவெரீஇத்", "vowel_sign_o",
     "னோங்குதிரை யொலிவெரீஇத்", 99,
     "lost ொ (ஒலி); also ஒங்கு for ஓங்கு and a stray space inside வெரீஇ"),
    (3, 21, "யழுகிய", "யொழுகிய", "vowel_sign_o", "யொழுகிய", 131, "ஒழுகிய"),
    (3, 108, "நாகக்துக்", "நாகத்துக்", "misprint", "நாகத்க்", 138,
     "க்து for த்து (நாகத்து); tvu itself drops the ு"),
    (3, 154, "யட்டகந்", "யொட்டகந்", "vowel_sign_o", "யொட்டகந்", 141, "ஒட்டகம்"),
    (3, 154, "துயுன்மடிந்", "துயின்மடிந்", "misprint", "யின்மடிந்", 141,
     "ு for ி (துயில் > துயின்); tvu has lost the first letter"),
    (3, 212, "கூற்றத்த்து", "கூற்றத்து", "misprint", "கூற்றத்து", 145, "doubled த்"),
    (3, 243, "றெள்ளூந்", "றெள்ளுந்", "misprint", "றெள்ளுந்", 147, "ூ for ு"),
    (4, 4, "யழித்த", "யொழித்த", "vowel_sign_o", "யொழித்த", 180, "ஒழித்த"),
    (4, 71, "யள்வாள்", "யொள்வாள்", "vowel_sign_o", "யொள்வாள்", 183, "ஒள்வாள்"),
    (4, 102, "யண்டொழிற்", "யொண்டொழிற்", "vowel_sign_o", "யொண்டொழிற்", 186, "ஒண்டொழில்"),
    (4, 214, "கட்கனழ்", "கட்கமழ்", "misprint", "கட்கமழ்", 193, "ன for ம (கமழ்)"),
    (4, 251, "செவிவிஅம்", "செவிலியம்", "misprint", "செவிலியம்", 195, "செவிலி"),
    (4, 260, "துங்சாக்", "துஞ்சாக்", "misprint", "துஞ்சா", 196, "ங்ச is not possible: ஞ்ச"),
    (4, 290, "ளண்பூ", "ளொண்பூ", "vowel_sign_o", "ளொண்பூ", 197, "ஒண்பூ"),
    (6, 264, "கவிகொள்", "கலிகொள்", "misprint", "கலிகொள்", 307, "வ for ல (கலி)"),
    (6, 264, "யலிகொ", "யொலிகொ", "vowel_sign_o", "யொலிகொ", 307, "ஒலி"),
    (6, 284, "வல்லொன்", "வல்லோன்", "misprint", "வல்லோன்", 308, "ொ for ோ"),
    (6, 456, "சூழ்சூடர்", "சூழ்சுடர்", "misprint", "சூழ்சு", 320, "ூ for ு (சுடர்)"),
    (6, 461, "யண்குறு", "யொண்குறு", "vowel_sign_o", "யொண்குறு", 320, "ஒண்"),
    (6, 498, "பழியரீஇ", "பழியொரீஇ", "vowel_sign_o", "பழியொரீஇ", 322, "ஒரீஇ"),
    (6, 507, "மழையழுக்", "மழையொழுக்", "vowel_sign_o", "மழையொழுக்", 323, "ஒழுக்கு"),
    (6, 746, "பெருற்செய்", "பெருஞ்செய்", "misprint", "பெருஞ்செ", 335, "ற் for ஞ் (பெருஞ்செய்)"),
    (8, 122, "நறுத்தார்", "நறுந்தார்", "misprint", "நறுந்தார்", 473, "த் for ந்"),
    (8, 166, "யய்யெனத்", "யொய்யெனத்", "vowel_sign_o", "யொய்யெனத்", 475, "ஒய்யென"),
    (8, 198, "களித்திற்", "களத்திற்", "misprint", "களத்திற்", 477, "ி for அ (களம்)"),
    (9, 60, "அகந்திட்டை", "அகன்திட்டை", "misprint", "லகன்றிட்டை", 517,
     "ந் for ன் (அகன் திட்டை); the base text's joined spelling kept"),
    (9, 71, "பெருங்சினத்தாற்", "பெருஞ்சினத்தாற்", "misprint", "பெருஞ்சினத்தாற்", 518,
     "ங்ச is not possible: ஞ்ச"),
    (9, 84, "தாட்டழ்ந்த", "தாட்டாழ்ந்த", "misprint", "தாட்டாழ்ந்த", 518, "lost ா (தாழ்ந்த)"),
    (9, 119, "வியந்தெருவின்", "வியன்தெருவின்", "misprint", "வியன்றெருவி", 520,
     "ந் for ன் (வியன் தெரு); the base text's joined spelling kept"),
    (9, 162, "உருறுகெழு", "உருகெழு", "misprint", "றுருகெழு", 522, "stray று"),
    (9, 162, "ஓண்பூப்", "ஒண்பூப்", "misprint", "னொண்பூப்", 522, "ஓ for ஒ"),
    (9, 201, "நல்லனெடு", "நல்லானொடு", "misprint", "நல்லானொடு", 523,
     "lost ா and ெ for ொ (நல்லான் + ஒடு)"),
    (9, 219, "யழிய", "யொழிய", "vowel_sign_o", "யொழிய", 525, "ஒழிய"),
    (9, 221, "வளர்ந்தாந்கும்", "வளர்ந்தாங்கும்", "misprint", "வளர்ந்தாங்குப்", 525,
     "ந்க is not possible: ங்க (tvu ends the word in -ப், not adopted)"),
    (9, 290, "ஒருவேனெப்", "ஒருவேமெனப்", "misprint", "தொருவேமெனப்", 529,
     "lost ம (ஒருவேம் எனப்)"),
    (10, 460, "றாரஅய்க்கண்", "றராய்க்கண்", "misprint", "றராய்க்கண்", 595, "தராய் (a raised bank)"),
)

# ---------------------------------------------------------------------------------------------
# (c) Readings kept: the base text differs from tvu (or looks faulty), but its reading is a
# possible word, or tvu has no usable line here. Flagged, not changed.
KEPT = (  # (poem, line, base word, tvu reading or None, tvu page or None, note)
    (2, 168, "முறையுழிக்", "முறையுளிக்", 96, "முறையுளி is the usual form; possible misprint"),
    (4, 481, "மாடுவண் டிமிரா வழல்தவிர்", "ஆடுவண் டிமிரா வழலவிர்", 208,
     "tvu: அழல் அவிர் (bright as flame); the base reads அழல் தவிர்"),
    (6, 308, "கமழ்சூழ்", "கமஞ்சூழ்", 309, "tvu: கமம் சூழ் (full, laden); possible misprint"),
    (6, 662, "களிதொடை", "களிநொடை", 330, "tvu: நொடை (selling); possible misprint"),
    (8, 42, "வலத்த", "வலந்த", 468, "tvu: வலந்த (woven); possible misprint"),
    (8, 142, "னென்றென", "னென்றன", 474, "tvu: என்றனன்"),
    (9, 30, "வல்லாய்ப்", "வல்வாய்ப்", 516, "tvu: வல்வாய் (strong-mouthed, of the boat)"),
    (9, 175, "மிசைச்கூம்பி னசைச்கொடியும்", None, None,
     "ச்கூ / ச்கொ are not possible (read மிசைக்கூம்பின் நசைக்கொடியும்?); tvu has no verse line "
     "here and pmuni0479 has மிசைச்கூம்பி னசைக்கொடியும்: not changed"),
    (9, 190, "பயுனும்", None, None,
     "read பயனும்? tvu has no verse line here and pmuni0479 also has பயுனு: not changed"),
    (10, 68, "சுரக்குஅவ நாடுபடு", None, None,
     "word division faulty (சுரக்கும் அவன் நாடுபடு?); tvu's line here is garbled: not changed"),
    (10, 72, "சுரக்கும்அவ நீகை", "சுரக்குமவ னீகை", 570,
     "word division faulty: சுரக்கும் அவன் ஈகை; not changed, since a fix would re-divide words"),
    (10, 407, "தலையிரும்பு", "தலையிறும்பு", 592, "tvu: இறும்பு (thicket); the base has இரும்பு"),
)


def repair(n, verse):
    """Repair one idyll's lines (a list, changed in place). Returns the log records, without ids."""
    log = []
    hits = set()
    for i, line in enumerate(verse, 1):
        if not ODU_RULE.search(line):
            continue
        if (n, i) in GENUINE_ADU:
            tvu, page, note = GENUINE_ADU[(n, i)]
            log.append({"action": "kept", "kind": "genuine_adu", "line": i, "old": line, "new": None,
                        "authority": [TVU], "readings": {"tvu": tvu}, "tvu_page": page,
                        "variants": None, "note": "a genuine -அடு, not the comitative: " + note})
            continue
        if (n, i) not in ODU_CHECKED:
            raise SystemExit(f"-ஒடு rule hit not checked against tvu: pattupattu {n}:{i} {line!r}")
        new = ODU_RULE.sub(lambda m: m.group(1) + "ொடு", line)
        tvu, page = ODU_CHECKED[(n, i)]
        verse[i - 1] = new
        hits.add((n, i))
        var = ODU_VARIANTS.get((n, i))
        log.append({"action": "changed", "kind": "vowel_sign_odu", "line": i, "old": line, "new": new,
                    "authority": [TVU], "readings": {"tvu": tvu}, "tvu_page": page,
                    "variants": [var] if var else None,
                    "note": "ொ lost after ய/ள (யடு/ளடு for யொடு/ளொடு)"})
    missing = {k for k in ODU_CHECKED if k[0] == n} - hits
    if missing:
        raise SystemExit(f"checked -ஒடு places not found by the rule: {sorted(missing)}")
    gone = {k for k in GENUINE_ADU if k[0] == n and not ODU_RULE.search(verse[k[1] - 1])}
    if gone:
        raise SystemExit(f"genuine -அடு places not found: {sorted(gone)}")

    for p, i, wrong, right, kind, tvu, page, note in EDITS:
        if p != n:
            continue
        line = verse[i - 1]
        if line.count(wrong) != 1:
            raise SystemExit(f"edit for pattupattu {n}:{i} finds {wrong!r} {line.count(wrong)} times in {line!r}")
        new = line.replace(wrong, right)
        verse[i - 1] = new
        log.append({"action": "changed", "kind": kind, "line": i, "old": line, "new": new,
                    "authority": [TVU, PM] if kind != "spacing" else [PM], "readings": {"tvu": tvu},
                    "tvu_page": page, "variants": None,
                    "note": f"{wrong} -> {right}" + (f": {note}" if note else "")})

    for p, i, word, tvu, page, note in KEPT:
        if p != n:
            continue
        if word not in verse[i - 1]:
            raise SystemExit(f"kept reading for pattupattu {n}:{i} not found: {word!r}")
        log.append({"action": "kept", "kind": "misprint_candidate", "line": i, "old": verse[i - 1],
                    "new": None, "authority": None, "readings": {"tvu": tvu} if tvu else None,
                    "tvu_page": page, "variants": None, "note": f"{word}: {note}"})
    return log
