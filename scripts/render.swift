// Render PDF pages to grayscale TIFF for OCR, cropped to the printed area.
//
//   swiftc -O scripts/render.swift -o /tmp/render
//   /tmp/render FILE.pdf FIRST LAST OUTDIR [DPI]   -> OUTDIR/p0001.tif ...
//
// Scanned books often sit small on a white A4 page; cropping to the darker area lets Tesseract
// find the lines. TIFF is used because Tesseract read nothing from these grayscale PNGs.
import AppKit
import Foundation
import PDFKit

let args = CommandLine.arguments
guard args.count >= 5, let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    print("usage: render FILE FIRST LAST OUTDIR [DPI]"); exit(1)
}
let first = Int(args[2])!, last = min(Int(args[3])!, doc.pageCount), outDir = args[4]
let dpi = args.count > 5 ? CGFloat(Double(args[5])!) : 300
let blank: UInt8 = 248
let margin = 20

for index in first...last {
    guard let page = doc.page(at: index - 1) else { continue }
    let box = page.bounds(for: .mediaBox)
    let width = Int(box.width * dpi / 72), height = Int(box.height * dpi / 72)
    let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: width, pixelsHigh: height,
                               bitsPerSample: 8, samplesPerPixel: 1, hasAlpha: false, isPlanar: false,
                               colorSpaceName: .deviceWhite, bytesPerRow: width, bitsPerPixel: 8)!
    let context = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = context
    context.cgContext.setFillColor(gray: 1, alpha: 1)
    context.cgContext.fill(CGRect(x: 0, y: 0, width: width, height: height))
    context.cgContext.scaleBy(x: dpi / 72, y: dpi / 72)
    page.draw(with: .mediaBox, to: context.cgContext)
    NSGraphicsContext.restoreGraphicsState()

    // Bounding box of everything darker than the blank page.
    let pixels = rep.bitmapData!
    var top = height, bottom = -1, left = width, right = -1
    for y in 0..<height {
        let row = pixels + y * width
        for x in 0..<width where row[x] < blank {
            if y < top { top = y }; if y > bottom { bottom = y }
            if x < left { left = x }; if x > right { right = x }
        }
    }
    var image = rep.cgImage!
    if bottom > top && right > left {
        let crop = CGRect(x: max(0, left - margin), y: max(0, top - margin),
                          width: min(width, right + margin) - max(0, left - margin),
                          height: min(height, bottom + margin) - max(0, top - margin))
        image = image.cropping(to: crop) ?? image
    }
    let out = NSBitmapImageRep(cgImage: image)
    let path = String(format: "%@/p%04d.tif", outDir, index)
    try! out.representation(using: .tiff, properties: [:])!.write(to: URL(fileURLWithPath: path))
}
print("rendered \(first)-\(last) of \(doc.pageCount)")
