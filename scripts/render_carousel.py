"""
Solnest Carousel Sniper v2 Orchestrator
=======================================

Renders a complete carousel from a data JSON. Supports two photo modes:

  Mode A: Higgsfield enhanced (premium)
    - Photos are produced via Higgsfield's API and downloaded into the carousel
      folder immediately.
    - This script does NOT call Higgsfield directly. The orchestrator that runs
      this script is responsible for generating jobs and passing the resulting
      rawUrls into the data JSON as `photo_url` per slide.

  Mode B: BYOP (bring your own photos)
    - Photos come from a local path or URL specified per slide in the data JSON.

After photos are in place, this script composites the brand text overlay onto
the photo slides (via render_photo_overlay) and renders the text-only slides
(via render_playwright). Finally it verifies the folder contains exactly the
expected number of PNGs plus caption.txt before declaring done.

Usage:
    python3 render_carousel.py --data carousel_data.json --brand my-brand --out outputs/carousel-{slug}

Data JSON shape: see example_carousel_data.json.
"""
import argparse
import json
import os
import sys
import shutil
import urllib.request
from pathlib import Path

from render_photo_overlay import composite_photo_overlay
from render_playwright import render_html_to_png
from caption import generate_caption


def load_brand(plugin_root, slug):
    """Load brand JSON. If `template`, return the template starter."""
    brand_path = Path(plugin_root) / "brands" / f"{slug}.json"
    if not brand_path.exists():
        raise FileNotFoundError(
            f"No brand found at {brand_path}. Run /solnest-carousel-setup first."
        )
    with open(brand_path) as f:
        return json.load(f)


def download_photo(url, dest):
    """Download a photo from a URL. Retries once on failure."""
    for attempt in (1, 2):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; SolnestCarouselBot/2.0)"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            with open(dest, "wb") as f:
                f.write(data)
            return True
        except Exception as e:
            if attempt == 2:
                print(f"  WARNING: photo download failed after retry: {e}", file=sys.stderr)
                return False
            print(f"  retrying download ({e})", file=sys.stderr)
    return False


def resolve_photo(slide, working_dir):
    """Get the photo for a slide to a local path.
    Accepts file paths (BYOP), URLs (Higgsfield rawUrl), or attached files."""
    src = slide.get("photo_url") or slide.get("photo_path")
    if not src:
        return None
    local = working_dir / f".tmp_{slide['name']}_src.png"
    if src.startswith("http://") or src.startswith("https://"):
        ok = download_photo(src, local)
        return local if ok else None
    p = Path(src).expanduser()
    if not p.exists():
        print(f"  WARNING: photo not found at {p}", file=sys.stderr)
        return None
    if p != local:
        shutil.copy(str(p), str(local))
    return local


def render_slide(slide, brand, out_dir):
    """Render a single slide based on its type and renderer."""
    slide_type = slide["type"]
    photo_types = ("photo_cover", "photo_feature", "cta_with_offer")
    name = slide["name"]
    dest = out_dir / f"{name}.png"

    if slide_type in photo_types:
        photo = resolve_photo(slide, out_dir)
        if photo is None:
            return False, f"no photo resolved for {name}"
        ok = composite_photo_overlay(
            photo_path=photo,
            output_path=dest,
            brand=brand,
            slide=slide,
        )
        try:
            photo.unlink()
        except Exception:
            pass
        return ok, None if ok else "overlay composite failed"
    else:
        ok = render_html_to_png(
            slide_type=slide_type,
            slide=slide,
            brand=brand,
            output_path=dest,
        )
        return ok, None if ok else "html render failed"


def verify_folder(out_dir, expected_slide_count):
    """Verify the folder contains exactly the expected files. Returns (ok, message)."""
    pngs = sorted(p.name for p in out_dir.glob("*.png"))
    caption = (out_dir / "caption.txt").exists()
    expected = expected_slide_count
    if len(pngs) != expected:
        return False, f"expected {expected} PNG slides, found {len(pngs)}: {pngs}"
    if not caption:
        return False, "caption.txt is missing"
    return True, f"{len(pngs)} slides + caption.txt OK"


def main():
    parser = argparse.ArgumentParser(description="Solnest Carousel Sniper v2 carousel orchestrator")
    parser.add_argument("--data", required=True, help="Path to carousel data JSON")
    parser.add_argument("--brand", required=True, help="Brand slug (matches brands/{slug}.json)")
    parser.add_argument("--out", required=True, help="Output folder for the carousel")
    parser.add_argument(
        "--plugin-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Plugin root (parent of scripts/, brands/, templates/)",
    )
    args = parser.parse_args()

    with open(args.data) as f:
        data = json.load(f)

    brand = load_brand(args.plugin_root, args.brand)
    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    slides = data.get("slides", [])
    if not slides:
        print("ERROR: no slides in data JSON", file=sys.stderr)
        return 1

    print(f"Rendering {len(slides)} slides for brand '{brand['name']}' -> {out_dir}\n")

    failures = []
    for i, slide in enumerate(slides, 1):
        print(f"  [{i}/{len(slides)}] {slide['name']} ({slide['type']})")
        ok, err = render_slide(slide, brand, out_dir)
        if not ok:
            failures.append((slide["name"], err))
            print(f"    FAILED: {err}")
        else:
            print(f"    OK")

    print("\nGenerating caption...")
    caption = generate_caption(data, brand)
    (out_dir / "caption.txt").write_text(caption)
    print("    caption.txt written")

    print("\nVerifying folder...")
    ok, msg = verify_folder(out_dir, len(slides))
    if ok:
        print(f"    {msg}")
    else:
        print(f"    PROBLEM: {msg}", file=sys.stderr)
        return 2

    if failures:
        print(f"\nWARNING: {len(failures)} slide(s) had issues:")
        for name, err in failures:
            print(f"  - {name}: {err}")
        return 3

    print(f"\nDone. Folder: {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
