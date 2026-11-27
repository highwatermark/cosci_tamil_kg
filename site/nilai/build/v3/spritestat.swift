// spritestat.swift IMG [IMG ...] : one JSON line per image, for build.py (stdlib Python has no image decoder).
// Fields: w, h; bbox [x0,y0,x1,y1] of alpha > 32; mean [r,g,b] of pixels with alpha > 128 (straight colour);
// runs: column runs of the figures in the top 80% of the frame (multi-view sheets), each with the bbox of its
// first connected block of rows; quads: the alpha bbox inside each quarter of the frame (tl, tr, bl, br).
import AppKit

func stat(_ path: String) -> String {
  guard let img = NSImage(contentsOfFile: path) else { return "{\"error\":\"unreadable\"}" }
  var r = CGRect(origin: .zero, size: img.size)
  guard let cg = img.cgImage(forProposedRect: &r, context: nil, hints: nil) else { return "{\"error\":\"no bitmap\"}" }
  let w = cg.width, h = cg.height
  var px = [UInt8](repeating: 0, count: w * h * 4)
  let cs = CGColorSpace(name: CGColorSpace.sRGB)!
  let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs,
                      bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
  ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
  @inline(__always) func a(_ x: Int, _ y: Int) -> Int { Int(px[(y * w + x) * 4 + 3]) }
  func box(_ X0: Int, _ Y0: Int, _ X1: Int, _ Y1: Int) -> [Int] {
    var x0 = X1, y0 = Y1, x1 = X0 - 1, y1 = Y0 - 1
    for y in Y0..<Y1 { for x in X0..<X1 where a(x, y) > 32 { if x < x0 { x0 = x }; if x > x1 { x1 = x }; if y < y0 { y0 = y }; if y > y1 { y1 = y } } }
    return x1 < x0 ? [0, 0, 0, 0] : [x0, y0, x1 + 1, y1 + 1]
  }
  let bb = box(0, 0, w, h)
  var sr = 0.0, sg = 0.0, sb = 0.0, cnt = 0.0
  for i in stride(from: 0, to: w * h * 4, by: 4) where px[i + 3] > 128 {
    let al = Double(px[i + 3]) / 255
    sr += Double(px[i]) / al; sg += Double(px[i + 1]) / al; sb += Double(px[i + 2]) / al; cnt += 1
  }
  let mean = cnt > 0 ? [Int(sr / cnt), Int(sg / cnt), Int(sb / cnt)] : [0, 0, 0]
  // column runs in the top band
  let band = Int(Double(h) * 0.8)
  var occ = [Int](repeating: 0, count: w)
  for x in 0..<w { var c = 0; for y in 0..<band where a(x, y) > 32 { c += 1 }; occ[x] = c }
  var runs: [[Int]] = []
  var x = 0
  let gap = max(3, w / 160)
  while x < w {
    if occ[x] > 2 {
      var e = x
      var k = x
      while k < w && (occ[k] > 2 || (k - e) <= gap) { if occ[k] > 2 { e = k }; k += 1 }
      if e - x > w / 40 { runs.append([x, e + 1]) }
      x = e + 1
    } else { x += 1 }
  }
  var rjs: [String] = []
  for rr in runs {
    // first connected block of rows inside the run (stops at a clear gap, e.g. above the head studies)
    var rows = [Bool](repeating: false, count: h)
    for y in 0..<h { for xx in rr[0]..<rr[1] where a(xx, y) > 32 { rows[y] = true; break } }
    var y0 = -1, y1 = -1, blank = 0
    for y in 0..<h {
      if rows[y] { if y0 < 0 { y0 = y }; y1 = y; blank = 0 } else if y0 >= 0 { blank += 1; if blank > h / 60 { break } }
    }
    let b = box(rr[0], max(0, y0), rr[1], y1 + 1)
    rjs.append("[\(b[0]),\(b[1]),\(b[2]),\(b[3])]")
  }
  let q = [box(0, 0, w / 2, h / 2), box(w / 2, 0, w, h / 2), box(0, h / 2, w / 2, h), box(w / 2, h / 2, w, h)]
  let qs = q.map { "[\($0[0]),\($0[1]),\($0[2]),\($0[3])]" }.joined(separator: ",")
  return "{\"w\":\(w),\"h\":\(h),\"bbox\":[\(bb[0]),\(bb[1]),\(bb[2]),\(bb[3])],\"mean\":[\(mean[0]),\(mean[1]),\(mean[2])],\"runs\":[\(rjs.joined(separator: ","))],\"quads\":[\(qs)]}"
}

for p in CommandLine.arguments.dropFirst() { print(stat(p)) }
