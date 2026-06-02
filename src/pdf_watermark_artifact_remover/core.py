"""Core PDF watermark artifact removal functions."""

from __future__ import annotations

import pikepdf
from pikepdf import ContentStreamInstruction, parse_content_stream, unparse_content_stream


def is_watermark_artifact(instruction: ContentStreamInstruction) -> bool:
    """Return whether an instruction starts a marked watermark artifact block."""
    if str(instruction.operator) != "BDC" or len(instruction.operands) < 2:
        return False

    properties = instruction.operands[1]
    return (
        isinstance(properties, pikepdf.Dictionary)
        and str(properties.get("/Subtype", "")) == "/Watermark"
    )


def remove_marked_watermarks(pdf: pikepdf.Pdf, page: pikepdf.Page) -> int:
    """Remove marked watermark artifact blocks from one page content stream."""
    filtered = []
    watermark_depth = 0
    removed_blocks = 0

    for instruction in parse_content_stream(page):
        operator = str(instruction.operator)

        if watermark_depth:
            if operator in {"BMC", "BDC"}:
                watermark_depth += 1
            elif operator == "EMC":
                watermark_depth -= 1
            continue

        if is_watermark_artifact(instruction):
            watermark_depth = 1
            removed_blocks += 1
            continue

        filtered.append(instruction)

    if watermark_depth:
        raise ValueError("Unbalanced marked-content block in PDF content stream")

    if removed_blocks:
        page.Contents = pdf.make_stream(unparse_content_stream(filtered))

    return removed_blocks


def parse_pages(value: str | None, page_count: int) -> set[int]:
    """Parse a comma-separated list of 1-based pages and inclusive ranges."""
    if not value:
        return set(range(page_count))

    selected = set()
    for item in value.split(","):
        item = item.strip()
        if not item:
            raise ValueError("Page list contains an empty item")

        if "-" in item:
            start, end = (int(part) for part in item.split("-", 1))
            if start > end:
                raise ValueError(f"Invalid descending page range: {item}")
            selected.update(range(start - 1, end))
        else:
            selected.add(int(item) - 1)

    invalid = sorted(page + 1 for page in selected if page < 0 or page >= page_count)
    if invalid:
        raise ValueError(f"Page numbers out of range: {invalid}")
    return selected

