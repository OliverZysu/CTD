"""Check built PDFs and retain compact evidence of final document validation."""
from pathlib import Path
import json
import re
import hashlib
import pymupdf as fitz

ROOT = Path(__file__).resolve().parent.parent
report = {"scope": "PDF structure, extracted text, page bounds, bibliography keys and TeX logs; not experimental reproduction"}
source = (ROOT / "source/manuscript.tex").read_text()
refs = set(re.findall(r"\\bibitem\{([^}]+)\}", (ROOT / "source/references.tex").read_text()))
cites = {key for group in re.findall(r"\\citep\{([^}]+)\}", source) for key in group.split(",")}
report["bibliography"] = {"references": len(refs), "cited": len(cites), "missing": sorted(cites - refs), "uncited": sorted(refs - cites)}
assert not cites - refs
for name in ("manuscript", "manuscript_submission", "supplementary"):
    path = ROOT / f"{name}.pdf"
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    pages = []
    for index, page in enumerate(doc):
        outside = []
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    r = fitz.Rect(span["bbox"])
                    if r.x0 < 0 or r.y0 < 0 or r.x1 > page.rect.width + 1 or r.y1 > page.rect.height + 1:
                        outside.append(span["text"])
        assert not outside, (name, index + 1, outside)
        pages.append({"page": index + 1, "text_characters": len(page.get_text()), "links": len(page.get_links())})
    assert "\ufffd" not in text
    assert "??" not in text
    log = (ROOT / f"build/{name}.log").read_text()
    assert "undefined references" not in log
    assert "Overfull" not in log, name
    report[name] = {"pages": len(doc), "bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "replacement_characters": text.count("\ufffd"),
                    "unresolved_references": text.count("??"), "page_details": pages,
                    "overfull_boxes": 0,
                    "underfull_boxes": log.count("Underfull")}
    (ROOT / f"review/{name}_extracted.txt").write_text(text)
    print(name, len(doc), "pages; no unresolved references or off-page text")
(ROOT / "review/final_pdf_validation.json").write_text(json.dumps(report, indent=2))
