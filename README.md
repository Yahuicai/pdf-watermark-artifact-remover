# PDF Watermark Artifact Remover

Remove PDF content blocks that are explicitly marked as watermark artifacts:

```text
/Artifact << /Subtype /Watermark >> BDC
...
EMC
```

The tool edits the PDF content stream directly. It does not rasterize pages,
reduce image quality, or redact rectangular regions that may also contain
legitimate text.

## Scope

This tool only removes watermarks represented as marked PDF artifact blocks.
It does not remove:

- watermarks baked into scanned images;
- unmarked text or vector overlays;
- stamps, signatures, or document content.

Use it only on documents you own or are authorized to modify.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

## Usage

Remove marked watermark artifacts from all pages:

```bash
pdf-remove-marked-watermarks input.pdf output-clean.pdf
```

Generate a one-page preview:

```bash
pdf-remove-marked-watermarks input.pdf preview.pdf \
  --pages 1 \
  --only-selected
```

Process selected pages while retaining the complete document:

```bash
pdf-remove-marked-watermarks input.pdf output-clean.pdf \
  --pages 1,3-5
```

## Development

```bash
python -m pip install -e '.[dev]'
pytest
```

