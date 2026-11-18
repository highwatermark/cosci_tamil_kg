#!/bin/bash
# OCR scanned Tamil PDFs the owner placed in data/incoming/<folder>/ (git ignores it).
#
#   scripts/ocr_incoming.sh siddha "file one.pdf" "file two.pdf" ...
#
# Writes data/incoming/<folder>/ocr/<file stem>/pNNNN.txt, one file per page, and skips pages
# already done, so it can be stopped and restarted. Needs Tesseract with tam.traineddata (see
# SECURITY.md) and Xcode's swiftc for scripts/render.swift.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FOLDER="$1"; shift
RENDER="${TMPDIR:-/tmp}/kg_render"
[ -x "$RENDER" ] || swiftc -O "$ROOT/scripts/render.swift" -o "$RENDER" 2>/dev/null
JOBS="${JOBS:-6}"

for pdf in "$@"; do
  src="$ROOT/data/incoming/$FOLDER/$pdf"
  stem="${pdf%.pdf}"
  out="$ROOT/data/incoming/$FOLDER/ocr/$stem"
  mkdir -p "$out/img"
  pages=$(mdls -raw -name kMDItemNumberOfPages "$src" 2>/dev/null || echo 0)
  [ "$pages" = "(null)" ] && pages=2000
  for ((start = 1; start <= pages; start += 20)); do
    end=$((start + 19))
    [ -f "$out/p$(printf %04d $((end < pages ? end : pages))).txt" ] && continue
    "$RENDER" "$src" "$start" "$end" "$out/img" >/dev/null
    # BSD xargs -I caps arguments at 255 bytes, too short for Tamil paths, so pass each file as $1.
    find "$out/img" -name '*.tif' -print0 | OUT="$out" xargs -0 -n 1 -P "$JOBS" sh -c \
      'tesseract "$1" "$OUT/$(basename "$1" .tif)" -l tam --psm 6 >/dev/null 2>&1; rm -f "$1"' _
  done
  echo "$pdf: $(ls "$out"/p*.txt 2>/dev/null | wc -l | tr -d ' ') pages"
done
