#!/usr/bin/env python3
"""
Extract images (emblematic woodcuts, diagrams) from Rosarium Philosophorum Band 1 facsimile.
Uses pdfimages (poppler-utils) to extract images at high quality for archival.
"""

import subprocess
import os
import json
from pathlib import Path
from datetime import datetime

# Configuration
DOWNLOADS_DIR = Path(os.path.expanduser("~")) / "Downloads"
ASSETS_DIR = Path("assets/rosarium_emblems")
ASSETS_DIR.mkdir(exist_ok=True, parents=True)

PDF_FILE = "Joachim Telle - Rosarium Philosophorum Band 1 Faksimile 1 (1992, VCH Verlagsgesellschaft) - libgen.li.pdf"
PDF_PATH = DOWNLOADS_DIR / PDF_FILE

def extract_images_with_pdfimages():
    """Extract images using pdfimages (poppler-utils)."""
    print("Attempting image extraction with pdfimages...")

    if not PDF_PATH.exists():
        print(f"ERROR: PDF not found: {PDF_PATH}")
        return False

    # Create output prefix
    output_prefix = str(ASSETS_DIR / "rosarium_emblem")

    # Try pdfimages command
    try:
        # -j for JPEG output, -list to get image info first
        result = subprocess.run(
            ["pdfimages", "-list", str(PDF_PATH)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print("[OK] pdfimages found. Image inventory:")
            print(result.stdout)

            # Now extract images as JPEGs
            result = subprocess.run(
                ["pdfimages", "-j", str(PDF_PATH), output_prefix],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                print(f"[OK] Images extracted to: {ASSETS_DIR}")
                return True
            else:
                print(f"[ERROR] pdfimages extraction failed: {result.stderr}")
                return False
        else:
            print(f"[ERROR] pdfimages not available: {result.stderr}")
            return False

    except FileNotFoundError:
        print("[ERROR] pdfimages command not found. Install with: pip install poppler-utils")
        return False
    except subprocess.TimeoutExpired:
        print("[ERROR] pdfimages command timed out")
        return False
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

def extract_images_with_pdfplumber():
    """Fallback: Extract images using pdfplumber."""
    print("\nAttempting image extraction with pdfplumber...")

    try:
        import pdfplumber
    except ImportError:
        print("[ERROR] pdfplumber not available")
        return False

    try:
        image_count = 0
        with pdfplumber.open(PDF_PATH) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                if hasattr(page, 'extract_image'):
                    # This method may not be available in all pdfplumber versions
                    try:
                        imgs = page.extract_image()
                        if imgs:
                            image_count += 1
                    except:
                        pass

        if image_count > 0:
            print(f"[OK] Found {image_count} images via pdfplumber")
            return True
        else:
            print("[INFO] pdfplumber did not extract images")
            return False

    except Exception as e:
        print(f"[ERROR] pdfplumber extraction failed: {e}")
        return False

def catalog_extracted_images():
    """Catalog any extracted images."""
    if not ASSETS_DIR.exists():
        print("[INFO] No images extracted")
        return

    image_files = sorted(list(ASSETS_DIR.glob("*.jpg")) + list(ASSETS_DIR.glob("*.jpeg")) + list(ASSETS_DIR.glob("*.png")))

    if not image_files:
        print("[INFO] No image files found in assets directory")
        return

    print(f"\n[FOUND] {len(image_files)} images extracted:")

    catalog = []
    for i, img_path in enumerate(image_files, 1):
        size_mb = img_path.stat().st_size / (1024 * 1024)
        print(f"  {i}. {img_path.name} ({size_mb:.2f} MB)")

        catalog.append({
            "filename": img_path.name,
            "path": str(img_path),
            "size_mb": round(size_mb, 2),
            "extracted_from": "Rosarium Philosophorum Band 1 Facsimile (1992)"
        })

    # Save catalog
    catalog_file = ASSETS_DIR / "image_catalog.json"
    with open(catalog_file, 'w', encoding='utf-8') as f:
        json.dump({
            "extracted_at": datetime.now().isoformat(),
            "source_pdf": PDF_FILE,
            "total_images": len(catalog),
            "images": catalog
        }, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Catalog saved: {catalog_file}")

def create_image_metadata_template():
    """Create a template for cataloging images as database assets."""
    template = {
        "emblem_catalog": {
            "source": "Rosarium Philosophorum Band 1 (Telle Facsimile, 1992)",
            "total_emblems_documented": "20+",
            "description": "Emblematic woodcuts from the medieval/Renaissance alchemical text, depicting stages of the Great Work, the King-Queen conjunction, distillation apparatus, and rose-garden symbolism.",
            "image_metadata_template": {
                "emblem_id": "rosarium-emblem-001",
                "filename": "rosarium_emblem-001.jpg",
                "page_reference": "p. XX",
                "description": "Brief description of the emblem and its symbolic significance",
                "depicts": ["King and Queen conjunction", "Mercury distillation", "Rose garden stage"],
                "related_concepts": ["conjunction", "distillation", "emblematic-alchemy"],
                "scholarly_interpretation": "Brief note on how modern scholars interpret this emblem"
            },
            "notes": "Images can be linked to timeline events and concept entries to enhance visual understanding of alchemical operations and symbolism."
        }
    }

    template_file = ASSETS_DIR / "emblem_metadata_template.json"
    with open(template_file, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

    print(f"[OK] Metadata template created: {template_file}")

def main():
    """Main function."""
    print("="*70)
    print("ROSARIUM PHILOSOPHORUM IMAGE EXTRACTION")
    print("="*70)
    print(f"\nSource: {PDF_PATH}")
    print(f"Output: {ASSETS_DIR}")

    # Try extraction
    success = extract_images_with_pdfimages()

    if not success:
        print("\nFalling back to pdfplumber...")
        success = extract_images_with_pdfplumber()

    # Catalog any extracted images
    catalog_extracted_images()

    # Create metadata template for future cataloging
    create_image_metadata_template()

    print("\n" + "="*70)
    if success:
        print("IMAGE EXTRACTION COMPLETE")
    else:
        print("IMAGE EXTRACTION REQUIRES TOOLS")
        print("\nTo extract images, install one of:")
        print("  1. poppler-utils: pip install poppler-utils (Windows) or apt-get install poppler-utils")
        print("  2. Or manually use PDF viewer to export emblems as images")
    print("="*70)

if __name__ == '__main__':
    main()
