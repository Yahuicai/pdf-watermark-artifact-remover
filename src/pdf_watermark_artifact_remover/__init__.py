"""Remove explicitly marked watermark artifacts from PDFs."""

from .core import parse_pages, remove_marked_watermarks

__all__ = ["parse_pages", "remove_marked_watermarks"]

