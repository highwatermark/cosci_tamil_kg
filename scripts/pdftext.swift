import Foundation
import PDFKit
// usage: pdftext FILE FIRST LAST   (1-based pages) -> prints text of each page
let a = CommandLine.arguments
guard let doc = PDFDocument(url: URL(fileURLWithPath: a[1])) else { print("cannot open"); exit(1) }
let first = Int(a[2])!, last = min(Int(a[3])!, doc.pageCount)
for i in first...last {
    let s = doc.page(at: i - 1)?.string ?? ""
    print("=== PAGE \(i) (\(s.count) chars) ===\n\(s)")
}
