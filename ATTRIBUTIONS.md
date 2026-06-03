# Attributions and Source Audit

This repository contains an original implementation written for this project.
No source code, images, or documentation were copied from the watermark-removal
repositories listed below.

## Runtime Dependency

| Project | Usage | License | Link |
| --- | --- | --- | --- |
| `pikepdf` | Parse and rewrite PDF content streams | MPL-2.0 | [GitHub](https://github.com/pikepdf/pikepdf) |

## Optional Demo Dependencies

These packages are only used by `scripts/generate_demo_assets.py`. They are not
required to install or run the watermark-removal CLI.

| Project | Usage | License | Link |
| --- | --- | --- | --- |
| `PyMuPDF` | Render the generated demo PDFs to PNG files | AGPL-3.0 or Artifex commercial license | [GitHub](https://github.com/pymupdf/PyMuPDF) |
| `Pillow` | Compose the generated before/after comparison image | MIT-CMU | [GitHub](https://github.com/python-pillow/Pillow) |

## Development Dependency

| Project | Usage | License | Link |
| --- | --- | --- | --- |
| `pytest` | Run automated tests | MIT | [GitHub](https://github.com/pytest-dev/pytest) |

## Evaluated Repositories

The following repositories were evaluated while comparing approaches. Their
source code and assets are not included in this project.

| Project | Evaluated approach | Incorporated code or assets |
| --- | --- | --- |
| [`StuHude/PDF-Watermark-Removal`](https://github.com/StuHude/PDF-Watermark-Removal) | Rasterize pages and apply image thresholding | None |
| [`0xViKi/pdf-watermark-remover`](https://github.com/0xViKi/pdf-watermark-remover) | Remove matching text drawing operations with `PyPDF4` | None |
| [`banatibalazs/pdf-watermark-remover`](https://github.com/banatibalazs/pdf-watermark-remover) | Use masks, thresholds, and image inpainting | None |

## Project Implementation

This project uses a separate approach: it parses PDF content streams with
`pikepdf`, detects marked-content blocks explicitly tagged with
`/Subtype /Watermark`, and removes those complete blocks while preserving the
remaining vector content.

All committed demo PDFs, PNG images, and the workflow diagram are generated
inside this repository by `scripts/generate_demo_assets.py` or authored
specifically for this project.

