"""
One-time font installer for the Solnest Carousel Sniper.

Downloads the Google Fonts that the typography presets depend on into
~/.solnest-carousel/fonts/. Called automatically the first time a user runs
the carousel builder after /solnest-carousel-setup, OR manually by the user.

Why local fonts: Pillow (used by render_photo_overlay) needs file paths, not
CSS @font-face. Playwright loads Google Fonts via CSS link directly, but for
the PIL-based photo composite we need the actual TTF files on disk.

Total download: about 4 MB.
"""
import os
import sys
import urllib.request
from pathlib import Path

FONT_DIR = Path.home() / ".solnest-carousel" / "fonts"

FONTS = {
    "Inter-Regular.ttf":              "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
    "Inter-Bold.ttf":                 "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
    "Inter-Italic.ttf":               "https://github.com/google/fonts/raw/main/ofl/inter/Inter-Italic%5Bopsz%2Cwght%5D.ttf",
    "BodoniModa-Bold.ttf":            "https://github.com/google/fonts/raw/main/ofl/bodonimoda/BodoniModa%5Bopsz%2Cwght%5D.ttf",
    "PlayfairDisplay-Bold.ttf":       "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    "CormorantGaramond-Bold.ttf":     "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",
    "CormorantGaramond-Regular.ttf":  "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",
    "CormorantGaramond-Italic.ttf":   "https://github.com/google/fonts/raw/main/ofl/cormorantgaramond/CormorantGaramond-Italic%5Bwght%5D.ttf",
    "DMSerifDisplay-Regular.ttf":     "https://github.com/google/fonts/raw/main/ofl/dmserifdisplay/DMSerifDisplay-Regular.ttf",
    "Allura-Regular.ttf":             "https://github.com/google/fonts/raw/main/ofl/allura/Allura-Regular.ttf",
}


def main():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Installing fonts to {FONT_DIR}\n")
    failed = []
    for name, url in FONTS.items():
        dest = FONT_DIR / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"  OK {name} (already present)")
            continue
        print(f"  DL {name}", end=" ", flush=True)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SolnestCarouselBot/2.0)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            dest.write_bytes(data)
            print(f"({len(data) // 1024} KB)")
        except Exception as e:
            print(f"FAILED: {e}")
            failed.append(name)
    if failed:
        print(f"\nWARNING: {len(failed)} fonts failed: {failed}", file=sys.stderr)
        print("The carousel builder will fall back to system fonts for those typographies.", file=sys.stderr)
        return 1
    print(f"\nAll fonts installed. The carousel builder is typography-ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
