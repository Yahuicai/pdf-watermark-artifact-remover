from __future__ import annotations

from pathlib import Path

import pikepdf
import pytest

from pdf_watermark_artifact_remover.core import parse_pages, remove_marked_watermarks


def make_test_pdf(path: Path) -> None:
    with pikepdf.new() as pdf:
        page = pdf.add_blank_page(page_size=(300, 300))
        page.Contents = pdf.make_stream(
            b"""BT /F1 12 Tf 20 260 Td (keep-before) Tj ET
/Artifact << /Subtype /Watermark >> BDC
BT /F1 12 Tf 20 200 Td (remove-me) Tj ET
EMC
BT /F1 12 Tf 20 140 Td (keep-after) Tj ET
"""
        )
        pdf.save(path)


def test_remove_marked_watermarks(tmp_path: Path) -> None:
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    make_test_pdf(input_pdf)

    with pikepdf.open(input_pdf) as pdf:
        assert remove_marked_watermarks(pdf, pdf.pages[0]) == 1
        pdf.save(output_pdf)

    with pikepdf.open(output_pdf) as pdf:
        content = bytes(pdf.pages[0].Contents.read_bytes())
        assert b"keep-before" in content
        assert b"keep-after" in content
        assert b"remove-me" not in content
        assert b"/Watermark" not in content


def test_parse_pages() -> None:
    assert parse_pages(None, 4) == {0, 1, 2, 3}
    assert parse_pages("1,3-4", 4) == {0, 2, 3}


@pytest.mark.parametrize("value", ["0", "5", "3-1", "1,"])
def test_parse_pages_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        parse_pages(value, 4)

