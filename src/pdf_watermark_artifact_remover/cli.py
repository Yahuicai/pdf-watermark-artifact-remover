"""Command-line interface for removing marked PDF watermark artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pikepdf

from .core import parse_pages, remove_marked_watermarks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remove PDF blocks explicitly marked as /Subtype /Watermark artifacts."
    )
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    parser.add_argument(
        "--pages",
        help="Process 1-based pages or ranges, for example: 1 or 1,3-5. Default: all pages.",
    )
    parser.add_argument(
        "--only-selected",
        action="store_true",
        help="Write only selected pages to the output. Useful for preview files.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    with pikepdf.open(args.input_pdf) as pdf:
        selected = parse_pages(args.pages, len(pdf.pages))
        removed_blocks = 0

        for index, page in enumerate(pdf.pages):
            if index in selected:
                count = remove_marked_watermarks(pdf, page)
                removed_blocks += count
                print(f"page {index + 1}: removed {count} marked watermark block(s)")

        if args.only_selected:
            for index in reversed(range(len(pdf.pages))):
                if index not in selected:
                    del pdf.pages[index]

        args.output_pdf.parent.mkdir(parents=True, exist_ok=True)
        pdf.save(args.output_pdf)

    print(f"saved: {args.output_pdf}")
    print(f"total removed blocks: {removed_blocks}")


if __name__ == "__main__":
    main()

