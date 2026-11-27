// cutout.swift IN OUT : removes the edge-connected near-white background, feathers the edge, writes a PNG with alpha.
import AppKit
let a = CommandLine.arguments
let img = NSImage(contentsOfFile: a[1])!
var r = CGRect(origin: .zero, size: img.size)
let cg = img.cgImage(forProposedRect: &r, context: nil, hints: nil)!
let w = cg.width, h = cg.height
var px = [UInt8](repeating: 0, count: w*h*4)
let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w*4, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
func light(_ i: Int) -> Int { Int(min(px[i], px[i+1], px[i+2])) }   // whiteness = darkest channel
let T = 232            // pixels lighter than this on every channel count as background
var bg = [Bool](repeating: false, count: w*h)
var stack: [Int] = []
for x in 0..<w { stack.append(x); stack.append((h-1)*w + x) }
for y in 0..<h { stack.append(y*w); stack.append(y*w + w-1) }
while let p = stack.popLast() {
  if bg[p] || light(p*4) < T { continue }
  bg[p] = true
  let x = p % w, y = p / w
  if x > 0 { stack.append(p-1) }; if x < w-1 { stack.append(p+1) }
  if y > 0 { stack.append(p-w) }; if y < h-1 { stack.append(p+w) }
}
// alpha: background 0; foreground pixels next to background get a soft edge from their whiteness
for p in 0..<(w*h) {
  let i = p*4
  if bg[p] { px[i] = 0; px[i+1] = 0; px[i+2] = 0; px[i+3] = 0; continue }
  let x = p % w, y = p / w
  var edge = false
  for (dx, dy) in [(-1,0),(1,0),(0,-1),(0,1)] { let nx = x+dx, ny = y+dy; if nx>=0 && nx<w && ny>=0 && ny<h && bg[ny*w+nx] { edge = true } }
  if edge { let l = light(i); let al = max(0, min(255, (255 - l) * 255 / (255 - 200))); let f = Double(al)/255
    px[i] = UInt8(Double(px[i])*f); px[i+1] = UInt8(Double(px[i+1])*f); px[i+2] = UInt8(Double(px[i+2])*f); px[i+3] = UInt8(al) }
}
let out = ctx.makeImage()!
let rep = NSBitmapImageRep(cgImage: out)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
print("ok", w, h)
