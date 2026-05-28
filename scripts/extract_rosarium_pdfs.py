#!/usr/bin/env python3
"""
Extract text, metadata, and images from Rosarium Philosophorum PDFs
for ingestion into ALCHEMYTIMELINEMAP database.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

try:
    import pdfplumber
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install pdfplumber")
    sys.exit(1)

# Configuration
DOWNLOADS_DIR = Path(os.path.expanduser("~")) / "Downloads"
OUTPUT_DIR = Path("C:/Dev/ALCHEMYTIMELINEMAP/rosarium_extracted")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

PDF_FILES = {
    "band1_facsimile": "Joachim Telle - Rosarium Philosophorum Band 1 Faksimile 1 (1992, VCH Verlagsgesellschaft) - libgen.li.pdf",
    "band2_commentary": "Joachim Telle, Luth Clären, Joachim Huber - Rosarium Philosophorum Band 2 2 (1992, VCH Verlagsgesellschaft) - libgen.li.pdf",
    "smith_translation": "The Rosary of the Philosophers Being the Rosarium Philosophorum (2008, Holmes Pub Group Llc, Smith, Patrick J) - libgen.li.pdf"
}

def extract_pdf_metadata(pdf_path):
    """Extract metadata from PDF."""
    metadata = {}
    try:
        with pdfplumber.open(pdf_path) as pdf:
            metadata['total_pages'] = len(pdf.pages)
            if pdf.metadata:
                metadata.update({
                    'title': pdf.metadata.get('Title'),
                    'author': pdf.metadata.get('Author'),
                    'subject': pdf.metadata.get('Subject'),
                    'creator': pdf.metadata.get('Creator'),
                    'producer': pdf.metadata.get('Producer'),
                })
    except Exception as e:
        print(f"Error extracting metadata: {e}")
    return metadata

def extract_text_from_pdf(pdf_path, output_markdown=True):
    """Extract text content from PDF."""
    content = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    content.append({
                        'page': i,
                        'text': text,
                        'has_tables': bool(page.extract_tables()),
                        'word_count': len(text.split())
                    })
    except Exception as e:
        print(f"Error extracting text: {e}")
    return content

def extract_tables_from_pdf(pdf_path):
    """Extract tables from PDF."""
    tables = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                page_tables = page.extract_tables()
                if page_tables:
                    for j, table in enumerate(page_tables):
                        tables.append({
                            'page': i,
                            'table_index': j,
                            'rows': len(table),
                            'cols': len(table[0]) if table else 0,
                            'content': table
                        })
    except Exception as e:
        print(f"Error extracting tables: {e}")
    return tables

def process_pdf(pdf_name, pdf_path):
    """Process a single PDF file."""
    print(f"\n{'='*70}")
    print(f"Processing: {pdf_name}")
    print(f"File: {pdf_path}")
    print(f"{'='*70}")

    if not pdf_path.exists():
        print(f"ERROR: File not found: {pdf_path}")
        return None

    result = {
        'filename': pdf_path.name,
        'pdf_name': pdf_name,
        'extracted_at': datetime.now().isoformat(),
        'file_size_mb': round(pdf_path.stat().st_size / (1024*1024), 2)
    }

    # Extract metadata
    print("Extracting metadata...")
    metadata = extract_pdf_metadata(pdf_path)
    result['metadata'] = metadata
    print(f"  Pages: {metadata.get('total_pages', 'unknown')}")

    # Extract text content
    print("Extracting text content...")
    text_content = extract_text_from_pdf(pdf_path)
    result['text_pages'] = len(text_content)
    result['total_words'] = sum(p['word_count'] for p in text_content)
    print(f"  Text-bearing pages: {len(text_content)}")
    print(f"  Total words: {result['total_words']}")

    # Extract tables
    print("Extracting tables...")
    tables = extract_tables_from_pdf(pdf_path)
    result['tables'] = len(tables)
    print(f"  Tables found: {len(tables)}")

    # Save text content to file
    text_output = OUTPUT_DIR / f"{pdf_name}_text.json"
    with open(text_output, 'w', encoding='utf-8') as f:
        json.dump(text_content, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {text_output}")

    # Save tables to file
    if tables:
        tables_output = OUTPUT_DIR / f"{pdf_name}_tables.json"
        with open(tables_output, 'w', encoding='utf-8') as f:
            json.dump(tables, f, ensure_ascii=False, indent=2)
        print(f"  Saved: {tables_output}")

    return result

def main():
    """Main processing function."""
    print("\n" + "="*70)
    print("ROSARIUM PHILOSOPHORUM PDF EXTRACTION")
    print("="*70)

    results = {}

    for pdf_name, filename in PDF_FILES.items():
        pdf_path = DOWNLOADS_DIR / filename
        result = process_pdf(pdf_name, pdf_path)
        if result:
            results[pdf_name] = result

    # Save summary report
    summary_file = OUTPUT_DIR / "extraction_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print("EXTRACTION COMPLETE")
    print(f"{'='*70}")
    print(f"Summary saved to: {summary_file}")
    print(f"Output directory: {OUTPUT_DIR}")

    # Print summary
    for pdf_name, result in results.items():
        print(f"\n{pdf_name}:")
        print(f"  File: {result['filename']}")
        print(f"  Size: {result['file_size_mb']} MB")
        print(f"  Pages: {result['metadata'].get('total_pages')}")
        print(f"  Text content: {result['text_pages']} pages, {result['total_words']} words")
        print(f"  Tables: {result['tables']}")

if __name__ == '__main__':
    main()
