"""Check a couplet against the rules of kural venba (simplified classical prosody).

Usage: python3 -I scripts/venba_check.py FILE   (couplets separated by blank lines; line 1 = 4 words, line 2 = 3 words)

Rules applied:
  asai   nēr = one short or long letter (+ trailing consonants); nirai = short + short/long (+ consonants)
  seer   2-asai: tēmā (nn), puḷimā (Nn), kūviḷam (nN), karuviḷam (NN); 3-asai ending nēr (kāy) allowed;
         3-asai ending nirai (kani) not allowed in venba
  thalai after mā (ends nēr) the next word starts nirai; after viḷam (ends nirai) next starts nēr;
         after kāy the next starts nēr
  ending the 7th word is nāḷ (n), malar (N), kāsu (n + kutriyalukaram) or pirappu (N + kutriyalukaram)
A word-final kutriyalukaram drops before a following vowel (sandhi) before the word is scanned. Edhugai (second-letter
rhyme of the two lines' first words) is reported, not required.
"""
import sys, unicodedata

VOW_IND = {"அ": "s", "இ": "s", "உ": "s", "எ": "s", "ஒ": "s", "ஆ": "l", "ஈ": "l", "ஊ": "l", "ஏ": "l", "ஐ": "l", "ஓ": "l", "ஔ": "l"}
SIGN = {"ா": "l", "ி": "s", "ீ": "l", "ு": "s", "ூ": "l", "ெ": "s", "ே": "l", "ை": "l", "ொ": "s", "ோ": "l", "ௌ": "l"}
PULLI = "்"
HARD = set("கசடதபற")


def letters(word):
    """Split a Tamil word into (letter, kind) with kind s=short, l=long, o=consonant (ottu)."""
    out, i, w = [], 0, unicodedata.normalize("NFC", word)
    while i < len(w):
        c = w[i]
        if c in VOW_IND:
            out.append((c, VOW_IND[c])); i += 1
        elif c == "ஃ":
            out.append((c, "o")); i += 1
        elif "க" <= c <= "ஹ":
            nxt = w[i + 1] if i + 1 < len(w) else ""
            if nxt == PULLI:
                out.append((c + nxt, "o")); i += 2
            elif nxt in SIGN:
                out.append((c + nxt, SIGN[nxt])); i += 2
            else:
                out.append((c, "s")); i += 1
        else:
            i += 1  # punctuation, spaces
    return out


def asais(word):
    L = letters(word)
    res, i = [], 0
    while i < len(L):
        t, k = L[i]
        if k == "o":  # stray leading consonant: attach to previous
            if res: res[-1] = (res[-1][0] + t, res[-1][1])
            i += 1; continue
        j = i + 1
        while j < len(L) and L[j][1] == "o": j += 1
        if k == "s" and j == i + 1 and j < len(L) and L[j][1] in "sl":
            # nirai: short + next vowel-bearing letter
            end = j + 1
            while end < len(L) and L[end][1] == "o": end += 1
            res.append(("".join(x[0] for x in L[i:end]), "N")); i = end
        else:
            res.append(("".join(x[0] for x in L[i:j]), "n")); i = j
    return res


def kutr(word):
    """Word ends in a short u (kutriyalukaram after a hard consonant, or muttriyalukaram as in அறிவு);
    both close a venba as kāsu or pirappu."""
    L = letters(word)
    return len(L) >= 2 and L[-1][1] == "s" and L[-1][0][-1] == "ு"


SEER = {"nn": "tēmā", "Nn": "puḷimā", "nN": "kūviḷam", "NN": "karuviḷam"}


def classify(pat):
    if len(pat) == 2: return SEER[pat]
    if len(pat) == 3: return ("kāy" if pat[-1] == "n" else "kani") + ":" + pat
    if len(pat) == 1: return {"n": "nāḷ", "N": "malar"}[pat]
    return "too long:" + pat


def check(couplet):
    lines = [l.split() for l in couplet.strip().splitlines() if l.strip()]
    errs = []
    if len(lines) != 2 or len(lines[0]) != 4 or len(lines[1]) != 3:
        return [f"shape {[len(l) for l in lines]} (need 4 + 3 words)"], []
    words = lines[0] + lines[1]
    # Sandhi: a word-final kutriyalukaram (short u after a hard consonant) drops before a vowel,
    # leaving the consonant as an ottu, so the word scans shorter (உலகிற்கு ஊறு = உலகிற் கூறு).
    scan = []
    for n, w in enumerate(words):
        nxt = words[n + 1] if n + 1 < len(words) else ""
        L = letters(w)
        if nxt and nxt[0] in VOW_IND and len(L) >= 2 and L[-1][1] == "s" and L[-1][0] == L[-1][0][0] + "ு" \
                and L[-1][0][0] in HARD:
            w = w[:-1] + PULLI
        scan.append(w)
    pats = ["".join(k for _, k in asais(w)) for w in scan]
    rows = []
    for n, (w, p) in enumerate(zip(words, pats), 1):
        last = n == 7
        if last:
            ok = p in ("n", "N") or (p in ("nn", "Nn") and kutr(w))
            name = {"n": "nāḷ", "N": "malar"}.get(p) or ({"nn": "kāsu", "Nn": "pirappu"}[p] if p in ("nn", "Nn") and kutr(w) else "?")
            if not ok: errs.append(f"word 7 '{w}' ({p}) must be nāḷ, malar, kāsu or pirappu")
        else:
            name = classify(p)
            if name.startswith("kani") or name.startswith("too long") or len(p) == 1:
                errs.append(f"word {n} '{w}' is {name}: not allowed in venba")
        rows.append((w, "-".join(a for a, _ in asais(scan[n - 1])), p, name))
    for n in range(6):
        p, q = pats[n], pats[n + 1]
        need = "N" if (len(p) == 2 and p[-1] == "n") else "n"
        if q[0] != need:
            rule = "mā→nirai" if need == "N" else ("viḷam→nēr" if len(p) == 2 else "kāy→nēr")
            errs.append(f"link {n+1}→{n+2} '{words[n]}'→'{words[n+1]}' breaks {rule}")
    a, b = letters(lines[0][0]), letters(lines[1][0])
    ed = len(a) > 1 and len(b) > 1 and a[1][0][0] == b[1][0][0]
    rows.append(("edhugai", "yes" if ed else "no", "", ""))
    return errs, rows


if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read()
    blocks = [b for b in text.split("\n\n") if b.strip() and not b.strip().startswith("#")]
    bad = 0
    for i, b in enumerate(blocks, 1):
        errs, rows = check(b)
        print(f"--- {i}: {'OK' if not errs else 'FAIL'}")
        for r in rows: print("   ", *r)
        for e in errs: print("   !", e)
        bad += bool(errs)
    sys.exit(1 if bad else 0)
