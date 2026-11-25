#!/usr/bin/env python3
"""Rebuild kg/core/purananuru.jsonl and repair the base text (Project Madurai pmuni0057).

Run: python3 -I scripts/repair_purananuru.py

Steps:
  1. Run scripts/parse_purananuru.py, so the repairs always start from the unrepaired build.
  2. Apply the repairs below to the poem lines and colophon fields.
  3. Write kg/core/purananuru.jsonl (each record gets a `repairs` list of log ids) and
     kg/core/purananuru_repairs.jsonl, one record per change ("action": "changed") and one per
     edition difference where our reading is kept ("action": "kept").
  4. Refresh the Purananuru entries of kg/core/sangam_text_flags.jsonl with the check in
     build_sangam_core.py. Entries for other books are left exactly as they are.

Authorities (only these count):
  tvu    tamilvu.org, Tamil Virtual Academy library l1280 (புறநானூறு), the verse text and
         colophons of U. V. Swaminatha Aiyar's edition, pages l1280101.htm-l1280140.htm
  dp     the poem lines of Avvai S. Duraisamy Pillai's edition in Project Madurai pmuni0494_01-03
         and pmuni0531_01-03 (already in data/text/ and in each record's duraisamy_pillai.tamil)
  pm     Project Madurai pmuni0057 itself (the base text)
Only short readings (a word or a verse line) are written here. No commentary is copied.

Rules:
  * Where both authorities, or one authority and the base text's own evidence, show a plain
    typing or encoding fault, the base text is corrected and the other readings are logged.
  * Where the editions genuinely differ, our reading is kept and the variant is logged and flagged.
  * Inserted lines are given in the tvu spelling (words separated), since the base text also
    separates most words; dp's sandhi-joined spelling is logged beside it.
"""
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "kg" / "core"
OUT = CORE / "purananuru.jsonl"
LOG = CORE / "purananuru_repairs.jsonl"
FLAGS = CORE / "sangam_text_flags.jsonl"

TVU = "tvu (tamilvu.org l1280, U. V. Swaminatha Aiyar's text)"
DP = "dp (Duraisamy Pillai's text, Project Madurai pmuni0494/pmuni0531)"
PM = "pm (Project Madurai pmuni0057, the base text)"

# ---------------------------------------------------------------------------------------------
# (a) The vowel sign ொ is lost after ய and ள everywhere in pmuni0057 (the file has no யொ or ளொ
# at all, while யோ occurs 170 times), so the comitative -ஒடு is printed யடு / ளடு. The rule
# below finds யடு / ளடு at the end of a word (or before -ம்), which leaves genuine words such as
# அடுக்கத்து alone. Every hit was checked against tvu and dp; the table gives their readings
# (letters only; dp often joins the word to the next line's first letter). The script refuses
# to run if the rule finds anything not in this table.
ODU_RULE = re.compile(r"([யள])டு(?=ம்|[^஀-௿]|$)")
ODU_CHECKED = {  # (poem, base line): (tvu reading, dp reading or None if dp lacks the line)
    (15, 12): ("பலகையொடு", "பலகையொடு"), (16, 1): ("புரவியொடு", "புரவியொடு"),
    (19, 10): ("வாயொடு", "வாயொடு"), (21, 12): ("இசையொடு", "இசையொடு"),
    (24, 19): ("மிழலையொடு", "மிழலையொடு"), (41, 15): ("மாக்களொடு", "மாக்களொடு"),
    (44, 1): ("தொழுதியொடு", "தொழுதியொடு"), (50, 4): ("உழிஞையொடு", "உழிஞையொடு"),
    (58, 29): ("கெண்டையொடு", "கெண்டையொடு"), (62, 6): ("தானையொடு", "தானையொடு"),
    (64, 1): ("பதலையொடு", "பதலையொடு"), (70, 15): ("விறலியொடு", "விறலியொடு"),
    (76, 7): ("மாலையொடு", "மாலையொடு"), (90, 2): ("குளவியொடு", "குளவியொடு"),
    (98, 11): ("கழியொடு", "கழியொடு"), (100, 5): ("வேங்கையொடு", "வேங்கையொடு"),
    (125, 3): ("மண்டையொடு", "மண்டையொ டூழ்"), (126, 8): ("கிளையொடும்", "கிளையொடும்"),
    (126, 19): ("யானையொடு", "யானையொடு"), (132, 6): ("பிணையொடு", "பிணையொடு"),
    (136, 8): ("கிளையொடு", "கிளையொடு"), (141, 2): ("மாலையொடு", "மாலையொடு"),
    (147, 6): ("நெய்யொடு", None), (152, 29): ("குவையொடும்", "குவையொடும்"),
    (158, 21): ("வழையொடு", "வழையொடு"), (158, 27): ("வண்மையொடு", "வண்மையொடு"),
    (159, 1): ("நாளோடு", "நாளோ டியாண்டு"), (159, 6): ("மேனியொடு", "மேனியொடு"),
    (161, 4): ("கருவியொடு", "கருவியொடு"), (161, 12): ("நாளொடும்", "நாளொடும்"),
    (161, 16): ("கையொடு", "தடக்கையொடு"), (167, 3): ("யாக்கையொடு", "யாக்கையொடு"),
    (167, 6): ("யாக்கையொடு", "யாக்கையொடு"), (168, 3): ("கிளையொடு", "கிளையொடு"),
    (178, 1): ("யானையொடு", "யானையொடு"), (190, 11): ("கேண்மையொடு", "கேண்மையொ டியைந்த"),
    (197, 1): ("இவுளியொடு", "இவுளியொடு"), (197, 3): ("தானையொடு", "தானையொடு"),
    (197, 12): ("சொன்றியொடு", "சொன்றியொடு"), (210, 2): ("காட்சியொடு", "காட்சியொடு"),
    (211, 12): ("பொய்யொடு", "பொய்யொடு"), (212, 9): ("பொத்தியொடு", "பொத்தியொடு"),
    (213, 6): ("காட்சியொடு", "காட்சியொடு"), (214, 13): ("யாக்கையொடு", "யாக்கையொடு"),
    (225, 5): ("தானையொடு", "றானையொ டாற்றல்"), (225, 10): ("பறையொடு", "பறையொடு"),
    (250, 5): ("மனைவியொடு", "மனைவியோ டினியே"), (257, 12): ("குழிசியொடு", "குழிசியொடு"),
    (260, 19): ("நிரையொடு", "நிரையொடு"), (261, 2): ("மண்டையொடு", "மண்டையொடு"),
    (261, 17): ("தலையொடு", "தலையொடு"), (264, 2): ("கண்ணியொடு", "கண்ணியொ டணி"),
    (266, 5): ("வளையொடு", "வளையொடு"), (271, 5): ("குருதியொடு", "குருதியொடு"),
    (278, 6): ("வாளொடு", "வாளொடு"), (283, 4): ("முதலையொடு", "முதலையொ டூழ்"),
    (288, 8): ("குருதியொடு", "குருதியொடு"), (304, 5): ("தம்பியொடு", "றம்பியொ டொராங்கு"),
    (310, 2): ("அஞ்சியொடு", "லஞ்சியோ டுயவொடு"), (318, 2): ("மாஅயோளொடு", "யோளொடு"),
    (318, 8): ("பெடையொடு", "பெடையொடு"), (320, 1): ("முஞ்ஞையொடு", "முஞ்ஞையொடு"),
    (320, 11): ("கோழியோடு", "கோழியொ டிதல்"), (328, 10): ("அரிசியொடு", "லரிசியோடு"),
    (335, 5): ("அவரையொடு", "ரவரையொ டிந்"), (336, 11): ("நகையொடு", "நகையொடு"),
    (339, 5): ("வாளையொடு", "வானையொ டுகளுந்து"), (341, 11): ("அவளொடு", "யவளொடு"),
    (342, 10): ("பிள்ளையொடு", "பிள்ளையொடு"), (356, 2): ("கூகையொடு", "கூகையொடு"),
    (359, 2): ("கூகையொடு", "கூகையொடு"), (360, 17): ("கள்ளொடு", "கள்ளொடு"),
    (361, 14): (None, "பொறையொடு"),  # tvu: 'பொறையொ......' (the rest of its line is lost)
    (362, 17): ("கூகையொடு", "கூகையொடு"), (371, 3): ("பறையொடு", "பறையொடு"),
    (373, 5): ("குருதியொடு", "குருதியொ டேந்திய"), (373, 36): ("பேயொடு", "பேயொடு"),
    (376, 10): ("துளையொடு", "துளையொடு"), (380, 7): ("குளவியொடு", "குளவியொடு"),
    (384, 9): ("மிசையொடு", "மிசையொடு"), (391, 18): ("வெய்யோளொடு", "யோளொ டின்றுயில்"),
    (393, 2): ("துணையொடு", "துணையொடு"), (394, 10): ("உவகையொடு", "யுவகையொ டணுகல்"),
    (395, 25): ("தடாரியொடு", "றடாரியோ டாங்கு"), (397, 21): ("தீயொடு", "தீயொடு"),
    (399, 32): ("ஊர்தியொடு", "ஊர்தியொடு"),
}

# ---------------------------------------------------------------------------------------------
# Explicit edits, matched by the exact text of the line(s) they replace, so they are applied
# once and only to the line they were written for. op:
#   replace  old line -> new lines (one or more)
#   after    insert new lines after the anchor line (old is the anchor and is not changed)
#   before   insert new lines before the anchor line
# Applied after the -ஒடு rule and the backtick/underscore rules, so 'old' is written in the
# text as it stands at that point.
EDITS = [
    # (a') the same lost ொ inside a word
    dict(n=31, kind="vowel_sign_o", op="replace", old="பாசறை யல்லது நீயல் லாயே;",
         new=["பாசறை யல்லது நீயொல் லாயே;"], auth=[TVU, DP],
         readings={"tvu": "நீ ஒல்லாயே", "dp": "நீயொல் லாயே"}),
    dict(n=109, kind="vowel_sign_o", op="replace",
         old="விரையலி கூந்தல் நும் விறலியர் பின் வர,",
         new=["விரையொலி கூந்தல் நும் விறலியர் பின் வர,"], auth=[TVU, DP],
         readings={"tvu": "விரை ஒலி", "dp": "விரையொலி"}),

    # (b) font junk
    dict(n=69, kind="font_junk", op="replace", old="வையகம் முழுவதுடன் வ¨ளைப், பையென",
         new=["வையகம் முழுவதுடன் வளைஇப், பையென"], auth=[DP, TVU],
         readings={"tvu": "வளைஇ,", "dp": "வளைஇப்"},
         note="'¨' is a font leftover; both editions read the lengthened form வளைஇ"),
    dict(n=100, kind="font_junk", op="replace", old="கையது வேலே; காலன பு¨ ழல்;",
         new=["கையது வேலே; காலன புனைகழல்;"], auth=[DP, TVU],
         readings={"tvu": "புனை கழல்", "dp": "புனைகழல்"}),
    dict(n=100, kind="font_junk", op="replace", old="மெய்யது வியரே; மிடற்றது பசும்புண்;னக",
         new=["மெய்யது வியரே; மிடற்றது பசும்புண்;"], auth=[DP, TVU],
         readings={"tvu": "பசும் புண்;", "dp": "பசும்புண்"},
         note="stray letters 'னக' after the semicolon removed"),
    dict(n=283, kind="font_junk", op="replace", old="மன்றுள் என்பது கெட .. .. .. ¡னே பாங்கற்கு",
         new=["மன்றுள் என்பது கெட .. .. .. னே பாங்கற்கு"], auth=[PM],
         readings={"tvu": "கெட... / ....ானே பாங்கற்கு", "dp": "கெட...தானே பாங்கற்"},
         note="'¡' (a font leftover for a lost letter) removed; the fragment stays after the "
              "lacuna. dp fills the word as தானே, tvu keeps only ானே; not adopted"),
    dict(n=352, kind="font_junk", op="replace", old="சிறுகோல் உளையும் புரவி¦ . . .",
         new=["சிறுகோல் உளையும் புரவி . . ."], auth=[PM],
         readings={"tvu": "புரவி ெ..................", "dp": "புரவியொடு.........."},
         note="'¦' is the TSCII leftover for a vowel sign ெ whose consonant is lost; removed, "
              "the lacuna kept. dp reads புரவியொடு; not adopted"),
    dict(n=373, kind="font_junk", op="replace", old="சென்றோன் மன்ற சொ¦ . . . .",
         new=["சென்றோன் மன்ற சொ . . . ."], auth=[PM, TVU],
         readings={"tvu": "சொெ", "dp": "கொலைவற் சென்றெறி"},
         note="'¦' (a dangling vowel sign ெ, as in tvu) removed, the lacuna kept. dp has a full "
              "line here (கொலைவற் சென்றெறி); not adopted"),

    dict(n=24, kind="stray_char", op="replace", old="புனலம் புதவின் மிழலையொடு- கழனிக்",
         new=["புனலம் புதவின் மிழலையொடு கழனிக்"], auth=[TVU, DP],
         readings={"tvu": "மிழலையொடு கழனிக்", "dp": "மிழலையொடு கழனிக்"},
         note="here the underscore sits inside a phrase (மிழலையொடு கழனி), so no dash is kept"),

    # (c) misprints
    dict(n=84, kind="misprint", op="replace", old="போறெதிர்ந்து என் ஜ் போர்க்களம் புகினே,",
         new=["போரெதிர்ந்து என்னை போர்க்களம் புகினே,"], auth=[TVU, DP],
         readings={"tvu": "போர் எதிர்ந்து என்னை", "dp": "போரெதிர்ந் தென்னை"},
         note="stray ஜ் for னை; போறெதிர்ந்து (ற for ர) is not a possible sandhi"),
    dict(n=209, kind="misprint", op="replace", old="செருவெம் சேஎய்! நின் மகிழ்இரு க்கையே!",
         new=["செருவெம் சேஎய்! நின் மகிழ்இருக்கையே!"], auth=[TVU, DP],
         readings={"tvu": "மகிழ் இருக்கையே", "dp": "மகிழிருக் கையே"},
         note="stray space inside the word"),
    dict(n=269, kind="misprint", op="replace", old="கொடுஞ்சிறைக் க்ரூஉப்பருந்து ஆர்ப்பத்,",
         new=["கொடுஞ்சிறைக் குரூஉப்பருந்து ஆர்ப்பத்,"], auth=[TVU, DP],
         readings={"tvu": "குரூஉப் பருந்து", "dp": "குரூஉப்பருந்"}),
    dict(n=361, kind="misprint", op="replace", old="உருள்நடைப் ப்ஃறேர் ஒன்னார்க் கொன்றுதன்",
         new=["உருள்நடைப் பஃறேர் ஒன்னார்க் கொன்றுதன்"], auth=[DP],
         readings={"tvu": "உருள் நடை ........................ான்றதன்",
                   "dp": "உருணடைப் பஃறே ரொன்னார்க் கொன்றதன்"},
         note="ப்ஃ is impossible (pulli before ஃ); tvu has a lacuna here"),
    dict(n=56, kind="misprint", op="replace", old="விண்ணுயர் புல்கொடி, விறல்வெய் யனும்,",
         new=["விண்ணுயர் புல்கொடி, விறல்வெய் யோனும்,"], auth=[TVU, DP],
         readings={"tvu": "வெய்யோனும்", "dp": "வெய்யோனும்"},
         note="lost vowel sign ோ (the parallel line 8 has ஒண்செய் யோனும்)"),
    dict(n=88, kind="misprint", op="replace", old="யாவிர் அயினும், கூழை தார்கொண்டு",
         new=["யாவிர் ஆயினும், கூழை தார்கொண்டு"], auth=[TVU, DP],
         readings={"tvu": "ஆயினும்", "dp": "யாவி ராயினுங்"}),
    dict(n=88, kind="misprint", op="replace", old="யாம்பொருதும் என்றல் ஓம்புமின் ஓன்ங்குதிறல்;",
         new=["யாம்பொருதும் என்றல் ஓம்புமின் ஓங்குதிறல்;"], auth=[TVU, DP],
         readings={"tvu": "ஓங்கு திறல்", "dp": "னோங்குதிறல்"}),
    dict(n=88, kind="misprint", op="replace", old="ஓளிறுஇலங்கு நெடுவேல் மழவர் பெருமகன்,",
         new=["ஒளிறுஇலங்கு நெடுவேல் மழவர் பெருமகன்,"], auth=[TVU, DP],
         readings={"tvu": "ஒளிறு இலங்கு", "dp": "ஒளிறிலங்கு"}),
    dict(n=109, kind="misprint", op="replace",
         old="மூன்றே, கொழுங்கொடி வள்ளிக் கிழங்கு லீழ்க்கும்மே;",
         new=["மூன்றே, கொழுங்கொடி வள்ளிக் கிழங்கு வீழ்க்கும்மே;"], auth=[DP],
         readings={"dp": "கிழங்குவீழ்க்கும்மே"}, note="லீழ் is not a word (ல for வ)"),
    dict(n=126, kind="misprint", op="replace", old="வல்ல்ஞ்ம் அல்லேம் ஆயினும், வல்லே",
         new=["வல்லேம் அல்லேம் ஆயினும், வல்லே"], auth=[TVU, DP],
         readings={"tvu": "வல்லேம் அல்லேம்", "dp": "வல்லே மல்லே"}),
    dict(n=152, kind="misprint", op="replace", old="பன்மணிக் கு வையொடும் விரைஇக், ‘கொண்ம்’ எனச்,",
         new=["பன்மணிக் குவையொடும் விரைஇக், ‘கொண்ம்’ எனச்,"], auth=[TVU, DP],
         readings={"tvu": "குவையொடும்", "dp": "குவையொடும்"}, note="stray space inside the word"),
    dict(n=215, kind="misprint", op="replace", old="செல்வ்க் காலை நிற்பினும்,",
         new=["செல்வக் காலை நிற்பினும்,"], auth=[TVU, DP],
         readings={"tvu": "செல்வக் காலை", "dp": "செல்வக் காலை"}),

    # (d) lines missing in the base text. Most are eye-skips: the base joins the start of one
    # line to the end of a later one, and the lines between are lost.
    dict(n=48, kind="line_gap", op="after", old="அஃதுஎம் ஊரே; அவன்எம் இறைவன்;",
         new=["அன்னோற் படர்தியாயின், நீயும்"], auth=[TVU, DP],
         readings={"dp": "அன்னோற் படர்தி யாயி னீயும்"}),
    dict(n=58, kind="line_gap", op="replace", old="காதல் நெஞ்சின்நும் புணர்ச்சி; வென்று வென்று",
         new=["காதல் நெஞ்சின் நும் இடை புகற்கு அலமரும்", "ஏதில் மாக்கள் பொதுமொழி கொள்ளாது,",
              "இன்றே போல்க நும் புணர்ச்சி; வென்று வென்று"], auth=[TVU, DP],
         readings={"dp": "காத னெஞ்சினும் மிடைபுகற் கலமரும் / ஏதின் மாக்கள் பொதுமொழி கொள்ளா / "
                         "தின்றே போல்கநும் வேலே கொடுவரிக் (dp itself skips from புணர்ச்சி to வேலே)"},
         note="eye-skip from காதல் நெஞ்சின் to நும் புணர்ச்சி; two lines restored"),
    dict(n=77, kind="line_gap", op="after", old="தாலி களைந்தன்றும் இலனே; பால்விட்டு",
         new=["அயினியும் இன்று அயின்றனனே; வயின்வயின்"], auth=[TVU, DP],
         readings={"dp": "டயினியு மின்றயின் றனனே வயின்வயின்"}),
    dict(n=77, kind="line_gap", op="after", old="உடன்றுமேல் வந்த வம்ப மள்ளரை",
         new=["வியந்தன்றும், இழிந்தன்றும், இலனே; அவரை"], auth=[TVU, DP],
         readings={"dp": "வியந்தன்று மிழிந்தன்று மிலனே யவரை"}),
    dict(n=77, kind="line_gap", op="after", old="அழுந்தபற்றி, அகல்விசும்பு ஆர்ப்புஎழக்",
         new=["கவிழ்ந்து நிலம் சேர அட்டதை"], auth=[TVU, DP],
         readings={"dp": "கவிழ்ந்துநிலஞ் சேர வட்டதை"}),
    dict(n=86, kind="line_gap", op="after", old="சிற்றில் நற்றூண் பற்றி, நின்மகன்",
         new=["யாண்டு உளனோ? என வினவுதி; என் மகன்"], auth=[TVU, DP],
         readings={"dp": "யாண்டுள னோவென வினவுதி யென்மகன்"},
         note="tvu's closing quote mark left out, since the base has no opening one"),
    dict(n=88, kind="line_gap", op="after", old="கதிர்விடு நுண்பூண் அம்பகட்டு மார்பின்",
         new=["விழவு மேம்பட்ட நல் போர்"], auth=[TVU, DP],
         readings={"dp": "விழவுமேம் பட்ட நற்போர்"}),
    dict(n=88, kind="misprint", op="replace", old="விழ்வுத்தோள் என்னையைக் காணா ஊங்கே.",
         new=["முழவுத்தோள் என்னையைக் காணா ஊங்கே."], auth=[TVU, DP],
         readings={"tvu": "முழவுத் தோள்", "dp": "முழவுத்தோ ளென்னையைக்"},
         note="the lost line's விழவு has run into முழவு"),
    dict(n=116, kind="line_gap", op="after", old="நோகோ யானே; தேய்கமா காலை!",
         new=["பயில் பூஞ் சோலை மயில் எழுந்து ஆலவும்,"], auth=[TVU, DP],
         readings={"dp": "பயில்பூஞ் சோலை மயிலெழுந் தாலவும்"}),
    dict(n=126, kind="lineation", op="replace",
         old="ஒன்னார் யானை ஓடைப் பொன் கொண்டு, பாணர் சென்னி பொலியத் தைஇ,",
         new=["ஒன்னார் யானை ஓடைப் பொன் கொண்டு,", "பாணர் சென்னி பொலியத் தைஇ,"],
         auth=[TVU, DP], note="two verse lines printed as one; split as in both editions"),
    dict(n=160, kind="line_gap", op="after", old="குய்கொள் கொழுந்துவை நெய்யுடை அடிசில்,",
         new=["மதி சேர் நாள்மீன் போல, நவின்ற"], auth=[TVU, DP],
         readings={"dp": "மதிசேர் நாண்மீன் போல நவின்ற"}),
    dict(n=160, kind="line_gap", op="after", old="உள்ளம் துரப்ப வந்தனென்; எள்ளுற்று,",
         new=["இல் உணாத் துறத்தலின், இல் மறந்து உறையும்"], auth=[TVU, DP],
         readings={"dp": "றில்லுணாத் துறத்தலி னின்மறந் துறையும்"}),
    dict(n=160, kind="misprint", op="replace", old="இல்லுளைக் குடுமிப் புதல்வன் பன்மாண்",
         new=["புல்லுளைக் குடுமிப் புதல்வன் பன்மாண்"], auth=[TVU, DP],
         readings={"tvu": "புல் உளைக் குடுமி", "dp": "புல்லுளைக் குடுமிப்"},
         note="the lost line's இல் has run into புல்லுளை"),
    dict(n=209, kind="line_gap", op="replace", old="தெரியிழை அன்ன மார்பின்,",
         new=["தெரியிழை மகளிர் பாணி பார்க்கும்", "பெரு வரை அன்ன மார்பின்,"], auth=[TVU, DP],
         readings={"tvu": "தெரிஇழை மகளிர் பாணி பார்க்கும் / பெரு வரை அன்ன மார்பின்,",
                   "dp": "தெரியிழை மகளிர் பாணி பார்க்கும் / பெருவரை யன்ன மார்பிற்"},
         note="eye-skip from தெரியிழை to அன்ன மார்பின்"),
    dict(n=230, kind="line_gap", op="replace", old="வீழ்குடி உழவன் உண்ணாய் ஆயின்,",
         new=["வீழ்குடி உழவன் வித்து உண்டாஅங்கு", "ஒருவன் ஆர் உயிர் உண்ணாய் ஆயின்,"],
         auth=[TVU, DP],
         readings={"dp": "வீழ்குடி யுழவன் வித்துண் டாஅங் / கொருவ னாருயி ருண்ணா யாயின்"},
         note="eye-skip from உழவன் to உண்ணாய்"),
    dict(n=235, kind="line_gap", op="replace", old="இரப்போர் புன்கண் பாவை சோர,",
         new=["இரப்போர் கையுளும் போகி,", "புரப்போர் புன்கண் பாவை சோர,"], auth=[TVU, DP],
         readings={"dp": "இரப்போர் கையுளும் போகிப் / புரப்போர் புன்கண் பாவை சோர"},
         note="eye-skip from இரப்போர் to புரப்போர்"),
    dict(n=325, kind="line_gap", op="replace", old="அருமிளை இருக்கை யதுவே-வென்வேல்ஊரே.",
         new=["அருமிளை இருக்கை யதுவே-வென்வேல்", "வேந்து தலைவரினும் தாங்கும்,",
              "தாங்கா ஈகை, நெடுந்தகை ஊரே."], auth=[TVU, DP],
         readings={"dp": "அருமிளை யிருக்கை யதுவே வென்வேல் / வேந்துதலை வரினுந் தாங்கும் / "
                         "தாங்கா வீகை நெடுந்தகை யூரே."},
         note="eye-skip from வென்வேல் to ஊரே; two lines restored"),
    dict(n=371, kind="line_gap", op="before", old="போதவிழ் அலரி நாரின் தொடுத்துத்,",
         new=["அகன் தலை வையத்துப் புரவலர்க் காணாது,", "மரந்தலைச் சேர்ந்து, பட்டினி வைகி,"],
         auth=[TVU, DP],
         readings={"dp": "அகன்றலை வையத்துப் புரவலர்க் காணாது / மரந்தலைச் சேர்ந்து பட்டினி வைகிப்"},
         note="the base text starts at the third line"),
    dict(n=377, kind="line_gap", op="replace", old="பிறர்க்கு உவமம் பிறர் இல், என",
         new=["பிறர்க்கு உவமம் தான் அல்லது,", "தனக்கு உவமம் பிறர் இல், என"], auth=[TVU, DP],
         readings={"dp": "பிறர்க்குவமந் தானல்லது / தனக்குவமம் பிறரில்லென"},
         note="eye-skip from the first உவமம் to the second"),
    dict(n=378, kind="line_gap", op="after", old="அரைக்கமை மரபின மிடற்றியாக் குநரும்,",
         new=["மிடற்று அமை மரபின அரைக்கு யாக்குநரும்,"], auth=[TVU, DP],
         readings={"dp": "மிடற்றமை மரபின அரைக்கியாக் குநரும்"}),
    dict(n=384, kind="line_gap", op="replace", old="உண்ட நன்கலம் பெய்து நுடக்கவும்.",
         new=["உண்ட நன்கலம் பெய்து நுடக்கவும்,", "தின்ற நண் பல் ஊன் தோண்டவும்,"],
         auth=[TVU, DP], readings={"dp": "தின்ற நண்ப லூஉன் றோண்டவும்"},
         note="the full stop after நுடக்கவும் becomes a comma, as in tvu"),
    dict(n=386, kind="line_gap", op="after", old="குணதிசை நின்று குடமுதற் செலினும்,",
         new=["குட திசை நின்று குணமுதல் செலினும்,"], auth=[TVU, DP],
         readings={"dp": "குடதிசை நின்று குணமுதற் செலினும்"}),
]

# (e) colophon fields. colophon_raw stays as printed in pmuni0057.
COLOPHON = [
    dict(n=5, field="thurai", old="வெவியறிவுறூஉ: பொருண் மொழிக் காஞ்சியும் ஆம்",
         new="செவியறிவுறூஉ: பொருண் மொழிக் காஞ்சியும் ஆம்", auth=[TVU, DP],
         readings={"tvu": "செவியறிவுறூஉ", "dp": "செவியறிவுறூஉ"}, note="வெ for செ"),
    dict(n=336, field="thurai", old="பாற் பாற் காஞ்சி", new="மகட்பாற் காஞ்சி", auth=[TVU, DP],
         readings={"tvu": "மகட்பாற் காஞ்சி", "dp": "மகட்பாற் காஞ்சி"}),
    dict(n=15, field="poet", old="கபிலர்", new="நெட்டிமையார்", auth=[TVU, DP],
         readings={"tvu": "...முதுகுடுமிப் பெருவழுதியை நெட்டிமையார் பாடியது",
                   "dp": "...முதுகுடுமிப் பெருவழுதியை நெட்டிமையார் பாடியது"},
         note="the base text repeats poem 14's colophon"),
    dict(n=15, field="patron", old="சேரமான் செல்வக் கடுங்கோ வாழியாதன்",
         new="பாண்டியன் பல்யாகசாலை முதுகுடுமிப் பெருவழுதி", auth=[TVU, DP],
         note="the base text repeats poem 14's colophon; thinai and thurai are 'அவை' (as in 14) "
              "in both editions, so they stay"),
    dict(n=144, field="poet", old="கபிலர்", new="பரணர்", auth=[TVU, DP],
         readings={"tvu": "அவனை அவள் காரணமாகப் பரணர் பாடியது",
                   "dp": "அவனை யவள் காரணமாகப் பரணர் பாடியது"},
         note="the base text repeats poem 143's poet"),
    dict(n=145, field="poet", old="கபிலர்", new="பரணர்", auth=[TVU, DP],
         readings={"tvu": "அவனை அவள் காரணமாக அவர் பாடியது (அவர் = பரணர், 144)",
                   "dp": "அவனை யவள் காரணமாக அவர் பாடியது"},
         note="the base text itself adds 'பரணர் பாட்டு எனவும் கொள்வர்'"),
    dict(n=145, field="thurai", old="குறுங்கலி. 'பரணர் பாட்டு' எனவும் கொள்வர்", new="குறுங்கலி",
         auth=[PM], note="the base text's remark on the poet moved from thurai to note"),
    dict(n=145, field="note", old=None, new="'பரணர் பாட்டு' எனவும் கொள்வர்", auth=[PM],
         note="moved from thurai"),
]

# Edition differences where our reading is kept (flagged as edition_variant), and readings that
# look like misprints but are real words, so they are not changed (flagged misprint_candidate).
KEPT = [
    dict(n=355, kind="edition_variant", match="ஊரது நிலைமையும் இதுவே;",
         readings={"tvu": "same three lines as ours, then nothing",
                   "dp": "ஊரது நிலைமைமயு மிதுவே மற்றே / எண்ணா மையலன் றந்தை தன்னையர் / "
                         "கண்ணார் கண்ணிக் கடுமான் கிள்ளி / ..............."},
         note="dp has two more lines before the gap; tvu agrees with the base text"),
    dict(n=382, kind="edition_variant", match="நல் குரவின் பசித் துன்பின் நின்",
         readings={"tvu": "நல்குரவின் பசித் துன்பின் நின் (as ours)",
                   "dp": "நல்குவனின் பசித்துன்பற / என்பநின் பொருநர் பெரும வதற்கொண்டு"},
         note="dp has a different line and one more line; tvu agrees with the base text"),
    dict(n=383, kind="edition_variant", match="தன்புகழ் ஏத்தினெ னாக, ஊன்புலந்து,",
         readings={"tvu": "as ours", "dp": "தன்புக ழேத்தினெ னாக வென்வலத் / திடுக்க ணிரியல் போல வூன்புலந்"},
         note="dp has one more line"),
    dict(n=383, kind="edition_variant", match="எற் பெயர்ந்த நோக்கி . . . . .",
         readings={"tvu": "as ours", "dp": "மெல்லணைக் கிடந்தோன்................... / வெறபெயர்ந்த...நோக்கி"},
         note="dp has one more (damaged) line"),
    dict(n=366, kind="edition_variant", match="காவு தோறும் . . . . . . . .",
         readings={"tvu": "காவுதொறும் (then nothing)",
                   "dp": "காவு தோறிழைத்த வெறியயர் களத்தின் / இடங்கெத் தொகுத்த விடையின்"},
         note="dp fills the lacuna and adds a line; its lines 16-19 are also in another order"),
    dict(n=366, kind="edition_variant", match="கெடல் அருந் திருவ . . . . . . .",
         readings={"tvu": "கெடல் அருந் திருவ!", "dp": "கெடலருந் திருவ வுண்மோ.........."}),
    dict(n=384, kind="edition_variant", match=". . .",
         readings={"tvu": "no line here", "dp": "அரிகாற் கருப்பை யலைக்கும் பூழின்"},
         note="our lacuna line; dp gives a full line, tvu none"),
    dict(n=209, kind="edition_variant", match="பெறாது பெயரும் புள்ளினம் போல, நின்",
         readings={"tvu": "no such line", "dp": "பெறாது பெயரும் புள்ளிமை போலநின்"},
         note="dp has the line (புள்ளிமை for புள்ளினம்); tvu lacks it"),
    dict(n=283, kind="edition_variant", match="பெறாஅ உறையரா வராஅலின் மயங்கி",
         readings={"tvu": "பௌவ உறை அளவா, / ................ வி மயக்கி,",
                   "dp": "பெறாஅ வுறையரா வராஅலின் மயங்கி (as ours)"}),
    dict(n=147, kind="edition_variant", match="நெய்யொடு துறந்த மையிருங் கூந்தல்",
         readings={"tvu": "நெய்யொடு துறந்த மை இருங் கூந்தல் (as ours)", "dp": "no such line"}),
    dict(n=48, kind="edition_variant", match="அஃதுஎம் ஊரே; அவன்எம் இறைவன்;",
         readings={"tvu": "அஃது எம் ஊரே; அவன் எம் இறைவன்; (as ours)", "dp": "no such line"}),
    dict(n=393, kind="edition_variant", match="குறுநெடுந் துணையொடும் கூமை வீதலிற்,",
         readings={"tvu": "குறு நெடுந் துணையொடு கூமை வீதலின்,", "dp": "குறுநெடுந் துணையொடு கூர்மை வீதலிற்"}),
    dict(n=361, kind="misprint_candidate", match="உருள்நடைப் பஃறேர் ஒன்னார்க் கொன்றுதன்",
         readings={"tvu": "...ான்றதன்", "dp": "கொன்றதன்"}, note="கொன்றுதன் against கொன்றதன்"),
    dict(n=77, kind="misprint_candidate", match="மகிழ்ந்தன்றும்,இகழ்ந்தன்றும்,அதனினும் இலனே.",
         readings={"tvu": "மலிந்தன்றும்", "dp": "மலிந்தன்று"}, note="இகழ்ந்தன்றும் against மலிந்தன்றும்"),
    dict(n=69, kind="misprint_candidate", match="வையகம் முழுவதுடன் வளைஇப், பையென",
         readings={"tvu": "முழுதுடன்", "dp": "முழுதுடன்"}, note="முழுவதுடன் against முழுதுடன்"),
    dict(n=160, kind="misprint_candidate", match="நெறிகொள் வரிக்குடர் குனிப்பத் தண்ணெனக்,",
         readings={"tvu": "குளிப்ப", "dp": "குளிப்பத்"}, note="குனிப்ப against குளிப்ப"),
    dict(n=160, kind="misprint_candidate", match="“கோடின் றாக, பாடுநர் கடும்பு” என,",
         readings={"tvu": "கேடு இன்றாக", "dp": "கேடின் றாக"}, note="கோடின்றாக against கேடின்றாக"),
    dict(n=160, kind="misprint_candidate", match="செல்குவை யாயின், நல்குவை, பெரிது’ எனப்,",
         readings={"tvu": "நல்குவன்", "dp": "னல்குவன்"}, note="நல்குவை against நல்குவன்"),
    dict(n=160, kind="misprint_candidate", match="உள்ளில் வருங்கலம் திறந்து, அழக் கண்டு,",
         readings={"tvu": "வறுங் கலம்", "dp": "வறுங்கலந்"}, note="வருங்கலம் against வறுங்கலம்"),
    dict(n=298, kind="colophon_variant", field="poet",
         readings={"tvu": "ஆலியார் பாடியது", "dp": "ஆவியார் (our value, filled from dp)"}),
    dict(n=381, kind="colophon_variant", field="poet",
         readings={"tvu": "கரும்பனூர் கிழானை நன்னாகனார் பாடியது", "pm": "புறத்திணை நன்னகனார்"}),
]


def opening(prev, nxt):
    return (not prev or prev.isspace() or prev in ",;:(") and bool(nxt) and not nxt.isspace()


def fix_quotes(line):
    """Backticks used as quote marks: `` -> “ ”, ` -> ‘ ’, opening or closing by position."""
    out, i = [], 0
    while i < len(line):
        if line[i] == "`":
            double = line[i:i + 2] == "``"
            step = 2 if double else 1
            prev = out[-1][-1] if out and out[-1] else ""
            nxt = line[i + step] if i + step < len(line) else ""
            mark = ("“" if double else "‘") if opening(prev, nxt) else ("”" if double else "’")
            out.append(mark)
            i += step
        else:
            out.append(line[i])
            i += 1
    return "".join(out)


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    load_module("parse_purananuru").main()  # step 1: the unrepaired build
    recs = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines()]
    by_n = {r["number"]: r for r in recs}
    # Each line carries a tag, so a log record can find its line again after later insertions
    # (and after a later step has changed the same line again).
    counter = iter(range(10 ** 9))
    tags = {r["number"]: [next(counter) for _ in r["tamil"]] for r in recs}
    log = []  # (record, tags of the lines it produced)
    succ = {}  # tag of a line replaced by a later edit -> tag of its first replacement line

    def add(n, rec, new_lines=None):
        rec = {"id": None, "poem": f"purananuru:{n}", "number": n, **rec}
        log.append((rec, new_lines))

    # (a) -ஒடு by rule, checked against the table
    hits = set()
    for r in recs:
        n = r["number"]
        for i, line in enumerate(r["tamil"], 1):
            if not ODU_RULE.search(line):
                continue
            if (n, i) not in ODU_CHECKED:
                raise SystemExit(f"-ஒடு rule hit not checked against the editions: {n}:{i} {line!r}")
            new = ODU_RULE.sub(lambda m: m.group(1) + "ொடு", line)
            tvu, dp = ODU_CHECKED[(n, i)]
            readings = {k: v for k, v in (("tvu", tvu), ("dp", dp)) if v}
            variants = [f"{k}: {v} (-ஓடு)" for k, v in readings.items()
                        if re.search(r"[யள]ோ(?:டு|\s|$)", v)]
            if n == 393:
                variants.append("tvu, dp: துணையொடு (without -ம்)")
            r["tamil"][i - 1] = new
            hits.add((n, i))
            add(n, {"kind": "vowel_sign_odu", "field": "tamil", "old": line, "new": new,
                    "authority": [a for a, k in ((TVU, "tvu"), (DP, "dp")) if k in readings],
                    "readings": readings, "variants": variants or None,
                    "note": "ொ lost after ய/ள in pmuni0057 (யடு/ளடு for யொடு/ளொடு)"},
                [tags[n][i - 1]])
    missing = set(ODU_CHECKED) - hits
    if missing:
        raise SystemExit(f"checked -ஒடு places not found by the rule: {sorted(missing)}")

    # (b) backticks and underscores
    for r in recs:
        n = r["number"]
        for i, line in enumerate(r["tamil"]):
            new = line
            if "`" in new:
                new = fix_quotes(new)
            if "_" in new:
                new = new.replace("_", "-")
            if new != line:
                kinds = [k for k, c in (("backtick", "`"), ("underscore", "_")) if c in line]
                r["tamil"][i] = new
                add(n, {"kind": "stray_char", "field": "tamil", "old": line, "new": new,
                        "authority": [PM], "readings": None, "variants": None,
                        "note": ("backticks used as quote marks made ‘ ’ / “ ”" if "backtick" in kinds else "")
                        + ("; " if len(kinds) == 2 else "")
                        + ("underscores used as dashes made '-' (the base text's dash)" if "underscore" in kinds else "")},
                    [tags[n][i]])

    # (c), (d) and the rest: explicit edits
    for e in EDITS:
        lines = by_n[e["n"]]["tamil"]
        idx = [i for i, l in enumerate(lines) if l == e["old"]]
        if len(idx) != 1:
            raise SystemExit(f"edit for {e['n']} matches {len(idx)} lines: {e['old']!r}")
        i = idx[0]
        t = tags[e["n"]]
        new_tags = [next(counter) for _ in e["new"]]
        if e["op"] == "replace":
            lines[i:i + 1] = e["new"]
            succ[t[i]] = new_tags[0]
            t[i:i + 1] = new_tags
            old = e["old"]
        elif e["op"] == "after":
            lines[i + 1:i + 1] = e["new"]
            t[i + 1:i + 1] = new_tags
            old = None
        else:
            lines[i:i] = e["new"]
            t[i:i] = new_tags
            old = None
        add(e["n"], {"kind": e["kind"], "field": "tamil", "op": e["op"],
                     "anchor": e["old"] if e["op"] != "replace" else None,
                     "old": old, "new": e["new"] if len(e["new"]) > 1 or e["op"] != "replace"
                     else e["new"][0], "authority": e["auth"], "readings": e.get("readings"),
                     "variants": None, "note": e.get("note")}, new_tags)

    # (e) colophon
    for c in COLOPHON:
        r = by_n[c["n"]]
        if r[c["field"]] != c["old"]:
            raise SystemExit(f"colophon {c['n']} {c['field']} is {r[c['field']]!r}, expected {c['old']!r}")
        r[c["field"]] = c["new"]
        add(c["n"], {"kind": "colophon", "field": c["field"], "old": c["old"], "new": c["new"],
                     "authority": c["auth"], "readings": c.get("readings"), "variants": None,
                     "note": c.get("note")})

    # line numbers in the repaired text, then ids
    for rec, new_tags in log:
        rec["action"] = "changed"
        tag = new_tags[0] if new_tags else None
        while tag in succ:
            tag = succ[tag]
        rec["line"] = tags[rec["number"]].index(tag) + 1 if new_tags else None
    for k in KEPT:
        lines = by_n[k["n"]]["tamil"]
        line = None
        if "match" in k:
            idx = [i for i, l in enumerate(lines) if l == k["match"]]
            if len(idx) != 1:
                raise SystemExit(f"kept reading for {k['n']} matches {len(idx)} lines: {k['match']!r}")
            line = idx[0] + 1
        log.append(({"id": None, "poem": f"purananuru:{k['n']}", "number": k["n"],
                     "kind": k["kind"], "field": k.get("field", "tamil"), "action": "kept",
                     "line": line, "old": k.get("match") or by_n[k["n"]][k["field"]],
                     "new": None, "authority": None, "readings": k["readings"], "variants": None,
                     "note": k.get("note")}, None))

    order = {"changed": 0, "kept": 1}
    log.sort(key=lambda x: (x[0]["number"], order[x[0]["action"]], x[0]["line"] or 0))
    seen = {}
    for rec, _ in log:
        seen[rec["number"]] = seen.get(rec["number"], 0) + 1
        rec["id"] = f"purananuru:{rec['number']}:r{seen[rec['number']]}"
    for r in recs:
        r["repairs"] = [rec["id"] for rec, _ in log if rec["number"] == r["number"]]

    keys = ("id", "poem", "number", "action", "kind", "field", "line", "op", "anchor", "old", "new",
            "authority", "readings", "variants", "note")
    with open(LOG, "w", encoding="utf-8") as out:
        for rec, _ in log:
            row = {k: rec.get(k) for k in keys}
            for k in ("op", "anchor"):
                if row[k] is None:
                    del row[k]
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    with open(OUT, "w", encoding="utf-8") as out:
        for r in recs:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")

    # step 4: refresh the Purananuru flags only
    core = load_module("build_sangam_core")
    report = core.check_purananuru(ROOT / "data" / "text", OUT)
    pur_flags = [f for f in core.flags if f["book"] == "purananuru"]
    others = [l for l in FLAGS.read_text(encoding="utf-8").splitlines()
              if json.loads(l)["book"] != "purananuru"]
    with open(FLAGS, "w", encoding="utf-8") as out:
        for l in others:
            out.write(l + "\n")
        for f in pur_flags:
            out.write(json.dumps(f, ensure_ascii=False) + "\n")

    changed = [rec for rec, _ in log if rec["action"] == "changed"]
    counts = {}
    for rec in changed:
        counts[rec["kind"]] = counts.get(rec["kind"], 0) + 1
    kept = {}
    for rec, _ in log:
        if rec["action"] == "kept":
            kept[rec["kind"]] = kept.get(rec["kind"], 0) + 1
    print(f"repairs: {len(changed)} changes {counts}; kept with variant: {kept}")
    print("purananuru check:", report)
    print("purananuru flags:", {k: sum(1 for f in pur_flags if f["kind"] == k)
                                for k in sorted({f["kind"] for f in pur_flags})})


if __name__ == "__main__":
    main()
