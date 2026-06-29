#!/usr/bin/env python3
"""Convert PDF files to markdown format using pdfplumber and pytesseract."""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

try:
    import pdfplumber
except ImportError:
    print("ERROR: pdfplumber not installed. Install with: pip install pdfplumber")
    sys.exit(1)

SOURCES_DIR = Path("sources_new")
MARKDOWN_OUTPUT_DIR = Path("staging/pdfs_to_markdown")
CONVERSION_LOG = MARKDOWN_OUTPUT_DIR / "conversion_log.json"

def convert_pdf_to_markdown(pdf_path: Path) -> str:
    """Extract text from PDF and convert to markdown."""

    text_blocks = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Add metadata
            text_blocks.append(f"# {pdf_path.stem}\n")
            text_blocks.append(f"**Source:** {pdf_path.name}\n")
            text_blocks.append(f"**Pages:** {len(pdf.pages)}\n")
            text_blocks.append(f"**Extracted:** {datetime.now().isoformat()}\n")
            text_blocks.append("---\n\n")

            # Extract text from each page
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_blocks.append(f"## Page {page_num}\n\n")
                    text_blocks.append(text)
                    text_blocks.append("\n\n")

                # Extract tables if present
                tables = page.extract_tables()
                if tables:
                    for table_num, table in enumerate(tables, 1):
                        text_blocks.append(f"### Table {page_num}-{table_num}\n\n")
                        for row in table:
                            text_blocks.append("| " + " | ".join(str(cell or "") for cell in row) + " |\n")
                        text_blocks.append("\n")

    except Exception as e:
        print(f"  [ERROR extracting {pdf_path.name}]: {e}")
        return None

    return "\n".join(text_blocks)

def main():
    """Convert all PDFs in sources_new to markdown."""

    # Create output directory
    MARKDOWN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Find all PDFs
    pdf_files = list(SOURCES_DIR.rglob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files to convert\n")

    conversion_results = {}
    success_count = 0
    error_count = 0

    for idx, pdf_path in enumerate(sorted(pdf_files), 1):
        try:
            print(f"[{idx}/{len(pdf_files)}] Converting {pdf_path.name}...", end=" ", flush=True)

            markdown_content = convert_pdf_to_markdown(pdf_path)

            if markdown_content:
                # Write markdown file
                md_filename = pdf_path.stem + ".md"
                md_output_path = MARKDOWN_OUTPUT_DIR / md_filename

                with open(md_output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)

                conversion_results[pdf_path.name] = {
                    "status": "success",
                    "output": str(md_output_path),
                    "word_count": len(markdown_content.split()),
                    "char_count": len(markdown_content)
                }

                print(f"[OK] ({len(markdown_content)} chars)")
                success_count += 1
            else:
                conversion_results[pdf_path.name] = {
                    "status": "empty",
                    "error": "No text extracted"
                }
                error_count += 1
                print("[EMPTY]")

        except Exception as e:
            conversion_results[pdf_path.name] = {
                "status": "error",
                "error": str(e)
            }
            error_count += 1
            print(f"[ERROR] ({str(e)[:50]})")

    # Save conversion log
    log_data = {
        "conversion_date": datetime.now().isoformat(),
        "total_files": len(pdf_files),
        "successful": success_count,
        "errors": error_count,
        "results": conversion_results
    }

    with open(CONVERSION_LOG, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"CONVERSION COMPLETE")
    print(f"{'='*60}")
    print(f"Total files processed: {len(pdf_files)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Output directory: {MARKDOWN_OUTPUT_DIR}")
    print(f"Conversion log: {CONVERSION_LOG}")

if __name__ == "__main__":
    main()
