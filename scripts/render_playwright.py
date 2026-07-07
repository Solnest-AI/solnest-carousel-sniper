"""
Render text-only slides via Playwright (HTML to PNG).

We use Playwright because PIL produces utilitarian typography. HTML lets us
load real Google Fonts and get pixel-perfect editorial type.

If Playwright is not installed, falls back to PIL via render_text_fallback.

Templates live in ../templates/html/. Each slide type maps to a template file:

  info_card    → info-card.html
  event_card   → event-card.html
  quote        → quote.html
  framework    → framework.html
  prompt       → prompt.html
  stat         → stat.html
  comparison   → comparison.html

Each template uses Jinja-style placeholders. We do a simple string replace
to keep dependencies minimal.
"""
from pathlib import Path
import json
import re
import sys

CANVAS_W, CANVAS_H = 1080, 1350
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "html"

TYPOGRAPHY_GOOGLE_LINKS = {
    "editorial-luxury": "Bodoni+Moda:wght@400;700&family=Inter:wght@400;500;700",
    "soft-romantic": "Allura&family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500",
    "modern-editorial": "DM+Serif+Display&family=Inter:wght@400;500;700",
    "bold-direct": "Inter:wght@400;500;700;900",
    "heritage": "Playfair+Display:wght@400;700&family=Cormorant+Garamond:ital,wght@0,400;1,400",
}

TYPOGRAPHY_CSS = {
    "editorial-luxury": {
        "headline": "'Bodoni Moda', serif",
        "eyebrow": "'Inter', sans-serif",
        "body": "'Inter', sans-serif",
        "italic": "'Inter', sans-serif",
    },
    "soft-romantic": {
        "headline": "'Cormorant Garamond', serif",
        "eyebrow": "'Allura', cursive",
        "body": "'Inter', sans-serif",
        "italic": "'Cormorant Garamond', serif",
    },
    "modern-editorial": {
        "headline": "'DM Serif Display', serif",
        "eyebrow": "'Inter', sans-serif",
        "body": "'Inter', sans-serif",
        "italic": "'Inter', sans-serif",
    },
    "bold-direct": {
        "headline": "'Inter', sans-serif",
        "eyebrow": "'Inter', sans-serif",
        "body": "'Inter', sans-serif",
        "italic": "'Inter', sans-serif",
    },
    "heritage": {
        "headline": "'Playfair Display', serif",
        "eyebrow": "'Inter', sans-serif",
        "body": "'Cormorant Garamond', serif",
        "italic": "'Cormorant Garamond', serif",
    },
}


def build_css_vars(brand):
    palette = brand.get("palette", {})
    typo_key = brand.get("typography", "editorial-luxury")
    fonts = TYPOGRAPHY_CSS[typo_key]
    google_query = TYPOGRAPHY_GOOGLE_LINKS[typo_key]

    return {
        "--cream": palette.get("cream", "#F5F0E8"),
        "--bg": palette.get("background", "#EBE4D8"),
        "--text": palette.get("text", "#1F1B17"),
        "--accent": palette.get("accent", "#5C2024"),
        "--gold": palette.get("gold", "#C5A572"),
        "--dark": palette.get("dark_surface", "#1F1B17"),
        "--font-headline": fonts["headline"],
        "--font-eyebrow": fonts["eyebrow"],
        "--font-body": fonts["body"],
        "--font-italic": fonts["italic"],
        "--google-query": google_query,
    }


def render_html(template_name, vars):
    path = TEMPLATES_DIR / template_name
    if not path.exists():
        raise FileNotFoundError(f"template not found: {path}")
    html = path.read_text()
    for k, v in vars.items():
        html = html.replace("{{" + k + "}}", str(v))
    return html


def render_html_to_png(slide_type, slide, brand, output_path):
    template_map = {
        "info_card": "info-card.html",
        "event_card": "event-card.html",
        "quote": "quote.html",
        "framework": "framework.html",
        "prompt": "prompt.html",
        "stat": "stat.html",
        "comparison": "comparison.html",
    }
    template_name = template_map.get(slide_type)
    if not template_name:
        print(f"  no template for slide type '{slide_type}'", file=sys.stderr)
        return False

    css_vars = build_css_vars(brand)

    template_vars = {**css_vars}
    template_vars["handle"] = brand.get("handle", "@brand")
    template_vars["eyebrow"] = slide.get("eyebrow", "")
    template_vars["headline"] = slide.get("headline", "")
    template_vars["subtitle"] = slide.get("subtitle", "")
    template_vars["closer"] = slide.get("closer", "")
    template_vars["quote"] = slide.get("quote", "")
    template_vars["attribution"] = slide.get("attribution", "")
    template_vars["date"] = slide.get("date", "")
    template_vars["offer_pill"] = slide.get("offer_pill", "")

    items = slide.get("items", [])
    if items and isinstance(items[0], list):
        items_html = "".join(
            f'<li><span class="label">{label}</span><span class="value">{value}</span></li>'
            for label, value in items
        )
    elif items:
        items_html = "".join(f"<li>{i}</li>" for i in items)
    else:
        items_html = ""
    template_vars["items"] = items_html

    try:
        html = render_html(template_name, template_vars)
    except FileNotFoundError as e:
        print(f"  template missing, falling back to PIL: {e}", file=sys.stderr)
        return _pil_fallback(slide, brand, output_path)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  Playwright not installed. Falling back to PIL.", file=sys.stderr)
        return _pil_fallback(slide, brand, output_path)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": CANVAS_W, "height": CANVAS_H}, device_scale_factor=1)
            page.set_content(html, wait_until="networkidle")
            page.screenshot(path=str(output_path), full_page=False, omit_background=False)
            browser.close()
        return True
    except Exception as e:
        print(f"  Playwright render failed: {e}", file=sys.stderr)
        return _pil_fallback(slide, brand, output_path)


def _pil_fallback(slide, brand, output_path):
    """Lo-fi PIL fallback when Playwright is not available."""
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), tuple(int(brand.get("palette", {}).get("background", "#EBE4D8").lstrip("#")[i:i+2], 16) for i in (0, 2, 4)))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 64)
    except Exception:
        font = ImageFont.load_default()
    text = slide.get("headline", "") or slide.get("quote", "")
    d.text((60, 600), text[:60], fill=tuple(int(brand.get("palette", {}).get("text", "#1F1B17").lstrip("#")[i:i+2], 16) for i in (0, 2, 4)), font=font)
    img.save(output_path, "PNG", optimize=True)
    return True
