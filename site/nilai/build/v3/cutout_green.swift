// cutout_green.swift IN OUT [lo hi [strong|edge]] : chroma-key matte for #00FF00 backgrounds.
// Matte from green dominance g - max(r,b): <= lo is subject (opaque), >= hi is background (clear), soft in between.
// Then: remove small speckle (keep alpha 0 only where connected to the border or clearly green),
// feather the edge with a small blur of the alpha, and despill (clamp green to max(r,b) where it dominates).
// Writes a straight-alpha PNG.
import AppKit
let a = CommandLine.arguments
guard a.count >= 3, let img = NSImage(contentsOfFile: a[1]) else { print("usage: cutout_green IN OUT [lo hi]"); exit(1) }
let lo = a.count > 3 ? Double(a[3])! : 40     // green excess below which a pixel is fully kept
let hi = a.count > 4 ? Double(a[4])! : 110    // green excess above which a pixel is fully removed
// despill mode: "strong" (default) clamps green to the mean of red and blue over the whole subject, which removes
// green reflections on bronze, brass, gold and marble; "edge" only despills near the matte edge (for subjects that are
// themselves green or teal, e.g. the banana leaf or the circuit board).
let strong = !(a.count > 5 && a[5] == "edge")
var r = CGRect(origin: .zero, size: img.size)
let cg = img.cgImage(forProposedRect: &r, context: nil, hints: nil)!
let w = cg.width, h = cg.height, n = w*h
var px = [UInt8](repeating: 0, count: n*4)
let cs = CGColorSpace(name: CGColorSpace.sRGB)!
let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w*4, space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))

// 0. measure the actual screen colour: median of the border pixels (generators rarely give exact #00FF00)
var br: [Int] = [], bgc: [Int] = [], bb: [Int] = []
for x in stride(from: 0, to: w, by: 2) { for y in [0, 1, h-2, h-1] { let i = (y*w+x)*4; br.append(Int(px[i])); bgc.append(Int(px[i+1])); bb.append(Int(px[i+2])) } }
for y in stride(from: 0, to: h, by: 2) { for x in [0, 1, w-2, w-1] { let i = (y*w+x)*4; br.append(Int(px[i])); bgc.append(Int(px[i+1])); bb.append(Int(px[i+2])) } }
func med(_ v: [Int]) -> Double { Double(v.sorted()[v.count/2]) }
let BR = med(br), BG = med(bgc), BB = med(bb)
print("screen", Int(BR), Int(BG), Int(BB))
// 1. raw matte from green excess
var al = [Double](repeating: 1, count: n)
for p in 0..<n {
  let i = p*4
  let R = Double(px[i]), G = Double(px[i+1]), B = Double(px[i+2])
  let ex = G - max(R, B)
  // dark greens (shadow on the screen) also count as background: scale excess by brightness of green
  var t = (ex - lo) / (hi - lo)
  // shadowed screen: green clearly dominant even if not bright
  if G > 60 && ex > 0.55 * G { t = max(t, (ex / G - 0.55) / 0.2) }
  al[p] = 1 - min(1, max(0, t))
}
// 2. only clear pixels connected to the border are true background; enclosed fully-clear holes stay clear
//    only if strongly green (they are real holes, e.g. between legs). Nothing to do: matte is colour based.
// 3. small morphological cleanup: kill isolated opaque specks in the background (alpha>0 with <=1 opaque neighbour in 3x3)
var a2 = al
for y in 1..<(h-1) { for x in 1..<(w-1) {
  let p = y*w + x
  if al[p] > 0 && al[p] < 1 {
    var s = 0.0
    for dy in -1...1 { for dx in -1...1 { s += al[p + dy*w + dx] } }
    if s < 1.5 { a2[p] = 0 }
  }
}}
al = a2
let raw = al   // colour-derived alpha, used for un-mixing
// 4. feather: 3x3 box blur of the alpha, applied twice, but never raise alpha above the raw matte by much
func blur(_ s: [Double]) -> [Double] {
  var o = s
  for y in 1..<(h-1) { for x in 1..<(w-1) {
    let p = y*w + x
    var t = 0.0
    for dy in -1...1 { for dx in -1...1 { t += s[p + dy*w + dx] } }
    o[p] = t / 9
  }}
  return o
}
let fb = blur(blur(al))
let zone = blur(blur(blur(fb)))   // edge zone: anything within ~5 px of transparency
for p in 0..<n { al[p] = min(al[p], fb[p] * 1.15 > 1 ? 1 : fb[p] * 1.15) }
// 5. despill + write straight alpha
var out = [UInt8](repeating: 0, count: n*4)
for p in 0..<n {
  let i = p*4
  var R = Double(px[i]), G = Double(px[i+1]), B = Double(px[i+2])
  let A = al[p]
  if A <= 0.003 { continue }
  // un-mix the green screen from semi-transparent edge pixels: C = A*F + (1-A)*Green
  let U = raw[p]
  if U < 0.999 && U > 0.2 {
    G = (G - (1 - U) * BG) / U
    R = (R - (1 - U) * BR) / U; B = (B - (1 - U) * BB) / U
    R = min(255, max(0, R)); G = min(255, max(0, G)); B = min(255, max(0, B))
  }
  // despill: green may not exceed the mean of red and blue by much (keeps teal/olive, kills fringe)
  let lim = max((R + B) / 2 + 4, max(R, B) * 0.88)
  if G > lim && (zone[p] < 0.999 || G - max(R, B) > 60) {
    let spill = G - lim
    G = lim
    // return a little of the removed energy as neutral luminance so edges don't go dark
    let k = spill * 0.12; R = min(255, R + k); G = min(255, G + k); B = min(255, B + k)
  }
  if strong { let m = max((R + B) / 2 + 3, R * 0.80); if G > m { let sp = G - m; G = m; let k = sp * 0.10; R = min(255, R + k); G = min(255, G + k); B = min(255, B + k) } }
  // neutral subjects (marble, steel, white flour): remove any green cast across the whole subject.
  // Only low-saturation pixels where green is the top channel; saturated greens/teals are left alone.
  let mx = max(R, G, B), mn = min(R, G, B)
  if G > max(R, B) && mx - mn < 45 { G = max(R, B) }
  // never let the edge swing to magenta: green no lower than the smaller of red and blue near the edge
  if zone[p] < 0.999 { G = max(G, min(R, B)) }
  out[i] = UInt8(R); out[i+1] = UInt8(G); out[i+2] = UInt8(B); out[i+3] = UInt8((A * 255).rounded())
}
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: w, pixelsHigh: h, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bitmapFormat: .alphaNonpremultiplied, bytesPerRow: w*4, bitsPerPixel: 32)!
out.withUnsafeBufferPointer { src in memcpy(rep.bitmapData!, src.baseAddress!, n*4) }
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
print("ok", w, h)
