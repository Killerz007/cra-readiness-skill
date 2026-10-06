# Report artefact generation

## Capability discovery

Before rendering, inspect the executing environment for document-generation capability, in order of preference: a dedicated report or document-authoring skill with DOCX export; a PDF export skill; a trusted local toolchain. Do not use slide or presentation tooling for the formal report.

## Toolchain fallback

Most agents have no document skill. With a shell available:

1. Pandoc for DOCX from the canonical Markdown:

   ```bash
   pandoc 20-cra-readiness-report.md --from gfm --to docx --toc --output 20-cra-readiness-report.docx
   ```

2. PDF via Pandoc with a PDF engine (`--pdf-engine=xelatex`, `weasyprint`, `wkhtmltopdf` or `typst`), or LibreOffice headless from the DOCX:

   ```bash
   soffice --headless --convert-to pdf 20-cra-readiness-report.docx
   ```

   or a headless browser printing an HTML render of the Markdown.

3. Python libraries (`python-docx`, `reportlab`, `weasyprint`) as a last resort.

Record the tool and version in the rendering manifest. Only when none of the above can run, record `BLOCKED_RENDERING` for the affected format and tell the user.

## Canonical-content rule

Finalise all statuses, gaps and counts; freeze the canonical Markdown; compute its SHA-256; render DOCX and PDF from that content; never rewrite one output independently of the others.

## Rendering manifest (`schemas/report-rendering-manifest.schema.json`)

Canonical path and hash; DOCX and PDF paths and hashes; rendering status per format; capability or renderer and version; timestamp; page count where available; visual QA status; limitations.

## Visual QA

Inspect the rendered outputs for orphan headings, missing gap sections, clipped tables, broken footers or page numbers, blank pages, missing appendices, inconsistent counts, missing disclaimers and unreadable text. Correct and re-render before delivery. A rendering limitation is a deliverable limitation, not a provision result.
