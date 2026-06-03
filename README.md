# PDF Watermark Artifact Remover

English | [简体中文](docs/README.zh-CN.md)

Remove PDF content blocks that are explicitly marked as watermark artifacts:

```text
/Artifact << /Subtype /Watermark >> BDC
...
EMC
```

The tool edits the PDF content stream directly. It does not rasterize pages,
reduce image quality, or redact rectangular regions that may also contain
legitimate text.

![Before and after comparison](docs/assets/demo-comparison.png)

<table>
  <tr>
    <th>Before</th>
    <th>After</th>
  </tr>
  <tr>
    <td><img src="docs/assets/demo-before.png" alt="PDF page before cleanup"></td>
    <td><img src="docs/assets/demo-after.png" alt="PDF page after cleanup"></td>
  </tr>
</table>

## Scope

This tool is suitable for:

- watermark layers added by PDF software;
- text or vector watermarks tagged as `/Subtype /Watermark`;
- documents where page dimensions, vector content, and searchable text must
  remain intact.

It does not remove:

- watermarks baked into scanned images;
- unmarked text or vector overlays;
- stamps, signatures, or document content.

Use it only on documents you own or are authorized to modify.

## Install

```bash
git clone https://github.com/Yahuicai/pdf-watermark-artifact-remover.git
cd pdf-watermark-artifact-remover

python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
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

## How It Works

![Workflow](docs/assets/workflow.svg)

```text
Read PDF
  -> parse each page content stream
  -> locate /Subtype /Watermark artifacts
  -> remove their marked-content blocks
  -> save a new PDF
```

Because the utility only removes explicitly marked watermark blocks, it
preserves body text, images, diagrams, and page dimensions.

## Demo Files

The repository includes reproducible demo files:

- [`examples/demo-watermarked.pdf`](examples/demo-watermarked.pdf)
- [`examples/demo-clean.pdf`](examples/demo-clean.pdf)

Generate the demo PDFs and screenshots again with:

```bash
python -m pip install -e '.[dev,demo]'
python scripts/generate_demo_assets.py
```

## Development

```bash
python -m pip install -e '.[dev]'
pytest
```

## Attributions

See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for the source audit, dependency
licenses, and repositories evaluated during research.
