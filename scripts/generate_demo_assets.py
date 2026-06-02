#!/usr/bin/env python3
"""Generate reproducible demo PDFs and before/after screenshots for the README."""

from __future__ import annotations

from pathlib import Path
import sys

import fitz
from PIL import Image, ImageDraw
import pikepdf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from pdf_watermark_artifact_remover.core import remove_marked_watermarks  # noqa: E402


def make_demo_pdf(path: Path) -> None:
    with pikepdf.new() as pdf:
        page = pdf.add_blank_page(page_size=(612, 792))
        font = pdf.make_indirect(
            pikepdf.Dictionary(
                Type=pikepdf.Name("/Font"),
                Subtype=pikepdf.Name("/Type1"),
                BaseFont=pikepdf.Name("/Helvetica"),
            )
        )
        page.Resources = pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font))
        page.Contents = pdf.make_stream(
            b"""BT /F1 24 Tf 72 700 Td (Quarterly Project Notes) Tj ET
BT /F1 13 Tf 72 650 Td (This document contains legitimate vector text.) Tj ET
BT /F1 13 Tf 72 620 Td (The cleanup keeps text searchable and avoids rasterization.) Tj ET
0.85 0.85 0.85 RG 72 590 m 540 590 l S
BT /F1 13 Tf 72 540 Td (1. Review the marked artifact blocks in the PDF content stream.) Tj ET
BT /F1 13 Tf 72 510 Td (2. Remove only blocks explicitly tagged as watermark artifacts.) Tj ET
BT /F1 13 Tf 72 480 Td (3. Preserve the original page dimensions and vector content.) Tj ET
/Artifact << /Subtype /Watermark >> BDC
q 0.94 0.35 0.35 rg BT /F1 52 Tf 0.82 0.35 -0.35 0.82 125 265 Tm (SAMPLE WATERMARK) Tj ET Q
EMC
BT /F1 13 Tf 72 180 Td (Use this utility only for documents you own or are authorized to modify.) Tj ET
"""
        )
        pdf.save(path)


def clean_demo_pdf(input_pdf: Path, output_pdf: Path) -> None:
    with pikepdf.open(input_pdf) as pdf:
        removed = remove_marked_watermarks(pdf, pdf.pages[0])
        if removed != 1:
            raise RuntimeError(f"Expected one watermark block, removed {removed}")
        pdf.save(output_pdf)


def render_pdf(pdf_path: Path, image_path: Path) -> None:
    with fitz.open(pdf_path) as doc:
        pixmap = doc[0].get_pixmap(matrix=fitz.Matrix(1.4, 1.4), alpha=False)
        pixmap.save(image_path)


def compose_comparison(before_path: Path, after_path: Path, output_path: Path) -> None:
    before = Image.open(before_path).convert("RGB")
    after = Image.open(after_path).convert("RGB")
    padding = 36
    header = 58
    canvas = Image.new(
        "RGB",
        (before.width * 2 + padding * 3, before.height + header + padding),
        "white",
    )
    canvas.paste(before, (padding, header))
    canvas.paste(after, (before.width + padding * 2, header))
    draw = ImageDraw.Draw(canvas)
    draw.text((padding, 20), "Before: marked watermark artifact", fill="#222222")
    draw.text((before.width + padding * 2, 20), "After: vector content preserved", fill="#222222")
    canvas.save(output_path)


def main() -> None:
    assets = ROOT / "docs" / "assets"
    examples = ROOT / "examples"
    assets.mkdir(parents=True, exist_ok=True)
    examples.mkdir(parents=True, exist_ok=True)

    input_pdf = examples / "demo-watermarked.pdf"
    output_pdf = examples / "demo-clean.pdf"
    before_png = assets / "demo-before.png"
    after_png = assets / "demo-after.png"
    comparison_png = assets / "demo-comparison.png"

    make_demo_pdf(input_pdf)
    clean_demo_pdf(input_pdf, output_pdf)
    render_pdf(input_pdf, before_png)
    render_pdf(output_pdf, after_png)
    compose_comparison(before_png, after_png, comparison_png)

    print(f"generated: {comparison_png}")


if __name__ == "__main__":
    main()

