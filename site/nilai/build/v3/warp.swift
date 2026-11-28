// warp.swift IN OUT TOPW TOPH : lays a flat-lay cut-out on the floor with a true perspective (keystone) transform.
// The bottom edge keeps the full width; the top edge is TOPW of it, raised to TOPH of the height (CIPerspectiveTransform).
import AppKit
import CoreImage
let a = CommandLine.arguments
let img = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let tw = Double(a[3])!, th = Double(a[4])!
let W = img.extent.width, H = img.extent.height
let f = CIFilter(name: "CIPerspectiveTransform")!
f.setValue(img, forKey: kCIInputImageKey)
f.setValue(CIVector(x: W * (1 - tw) / 2, y: H * th), forKey: "inputTopLeft")
f.setValue(CIVector(x: W * (1 + tw) / 2, y: H * th), forKey: "inputTopRight")
f.setValue(CIVector(x: 0, y: 0), forKey: "inputBottomLeft")
f.setValue(CIVector(x: W, y: 0), forKey: "inputBottomRight")
let out = f.outputImage!
let ctx = CIContext()
let cg = ctx.createCGImage(out, from: out.extent)!
let rep = NSBitmapImageRep(cgImage: cg)
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[2]))
print("ok", cg.width, cg.height)
