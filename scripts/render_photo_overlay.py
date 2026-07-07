"""
Composite brand text overlays on top of a base photo.

Input: a photo (typically 4:5 portrait, but any aspect ratio works), the brand
config, and the slide spec (eyebrow, headline, subtitle, optional offer pill).

Output: 1080x1350 PNG with the photo centered/cropped to fill, a subtle dark
gradient at the bottom for legibility, and the brand-styled text overlay.

This implementation uses Pillow for compositing. Typography is loaded from
~/.solnest-carousel/fonts/ (downloaded once by setup) so we get real Bodoni /
Cormorant / Allura / Inter without depending on system fonts.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math

CANVAS = (1080, 1350)
FONT_DIR = Path.home() / ".solnest-carousel" / "fonts"

TYPOGRAPHY_PRESETS = {
    "editorial-luxury": {
        "headline": "BodoniModa-Bold.ttf",
        "eyebrow": "Inter-Bold.ttf",
        "body": "Inter-Regular.ttf",
        "italic": "Inter-Italic.ttf",
    },
    "soft-romantic": {
        "headline": "CormorantGaramond-Bold.ttf",
        "eyebrow": "Allura-Regular.ttf",
        "body": "Inter-Regular.ttf",
        "italic": "CormorantGaramond-Italic.ttf",
    },
    "modern-editorial": {
        "headline": "DMSerifDisplay-Regular.ttf",
        "eyebrow": "Inter-Bold.ttf",
        "body": "Inter-Regular.ttf",
        "italic": "Inter-Italic.ttf",
    },
    "bold-direct": {
        "headline": "Inter-Bold.ttf",
        "eyebrow": "Inter-Bold.ttf",
        "body": "Inter-Regular.ttf",
        "italic": "Inter-Italic.ttf",
    },
    "heritage": {
        "headline": "PlayfairDisplay-Bold.ttf",
        "eyebrow": "Inter-Bold.ttf",
        "body": "CormorantGaramond-Regular.ttf",
        "italic": "CormorantGaramond-Italic.ttf",
    },
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def find_font(font_name, size):
    """Try the user's ~/.solnest-carousel/fonts/ dir, then fall back to DejaVu."""
    p = FONT_DIR / font_name
    if p.exists():
        return ImageFont.truetype(str(p), size)
    for fallback in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]:
        if Path(fallback).exists():
            return ImageFont.truetype(fallback, size)
    return ImageFont.load_default()


def cover_resize_to(image, target_w, target_h):
    """Resize image to cover target dims, centered. Preserves aspect ratio."""
    iw, ih = image.size
    scale = max(target_w / iw, target_h / ih)
    new_w, new_h = int(iw * scale), int(ih * scale)
    resized = image.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def draw_letter_spaced(draw, xy, text, font, fill, spacing=8):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, fill=fill, font=font)
        bbox = draw.textbbox((0, 0), ch, font=font)
        x += (bbox[2] - bbox[0]) + spacing


def add_bottom_gradient(img, height_fraction=0.4, max_alpha=180):
    """Overlay a dark gradient on the bottom portion for text legibility."""
    w, h = img.size
    grad_h = int(h * height_fraction)
    grad = Image.new("RGBA", (w, grad_h), (0, 0, 0, 0))
    px = grad.load()
    for y in range(grad_h):
        a = int(max_alpha * (y / grad_h) ** 1.5)
        for x in range(w):
            px[x, y] = (0, 0, 0, a)
    img.paste(grad, (0, h - grad_h), grad)


def composite_photo_overlay(photo_path, output_path, brand, slide):
    """Main entry. Returns True on success."""
    try:
        base = Image.open(photo_path).convert("RGB")
    except Exception as e:
        print(f"  cannot open photo {photo_path}: {e}")
        return False

    canvas = cover_resize_to(base, CANVAS[0], CANVAS[1]).convert("RGBA")
    add_bottom_gradient(canvas, height_fraction=0.45)

    draw = ImageDraw.Draw(canvas)

    palette = brand.get("palette", {})
    cream = hex_to_rgb(palette.get("cream", "#F5F0E8"))
    gold = hex_to_rgb(palette.get("gold", "#C5A572"))
    dark = hex_to_rgb(palette.get("dark_surface", "#1F1B17"))

    typography_key = brand.get("typography", "editorial-luxury")
    fonts = TYPOGRAPHY_PRESETS.get(typography_key, TYPOGRAPHY_PRESETS["editorial-luxury"])

    eyebrow_font = find_font(fonts["eyebrow"], 26)
    headline_font = find_font(fonts["headline"], 92)
    subtitle_font = find_font(fonts["body"], 28)

    eyebrow = slide.get("eyebrow", "")
    headline = slide.get("headline", "")
    subtitle = slide.get("subtitle", "")

    bottom_anchor = CANVAS[1] - 180
    margin = 60

    if subtitle:
        bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sub_h = bbox[3] - bbox[1]
        draw.text((margin, bottom_anchor), subtitle, fill=cream, font=subtitle_font)
        bottom_anchor -= sub_h + 18

    if headline:
        lines = headline.split("\n")
        for line in reversed(lines):
            bbox = draw.textbbox((0, 0), line, font=headline_font)
            line_h = bbox[3] - bbox[1]
            draw.text((margin, bottom_anchor - line_h - 8), line, fill=cream, font=headline_font)
            bottom_anchor -= line_h + 18

    if eyebrow:
        bbox = draw.textbbox((0, 0), eyebrow, font=eyebrow_font)
        eb_h = bbox[3] - bbox[1]
        draw_letter_spaced(draw, (margin, bottom_anchor - eb_h - 30), eyebrow, eyebrow_font, gold, spacing=8)

    if slide.get("type") == "cta_with_offer":
        offer_code = slide.get("offer_code") or brand.get("offer", {}).get("default_code")
        offer_amount = slide.get("offer_amount") or brand.get("offer", {}).get("default_amount")
        if offer_code:
            pill_text = f"  Comment {offer_code} for {offer_amount}  "
            pill_font = find_font(fonts["body"], 30)
            bbox = draw.textbbox((0, 0), pill_text, font=pill_font)
            pw, ph = bbox[2] - bbox[0], bbox[3] - bbox[1]
            pill_x = (CANVAS[0] - pw) // 2 - 30
            pill_y = CANVAS[1] - 270
            draw.rounded_rectangle(
                [pill_x, pill_y, pill_x + pw + 60, pill_y + ph + 40],
                radius=40, fill=dark
            )
            draw.rounded_rectangle(
                [pill_x, pill_y, pill_x + pw + 60, pill_y + ph + 40],
                radius=40, outline=gold, width=3
            )
            draw.text((pill_x + 30, pill_y + 18), pill_text.strip(), fill=gold, font=pill_font)

    handle = brand.get("handle", "@brand")
    footer_font = find_font(fonts["body"], 22)
    draw.text((margin, CANVAS[1] - 60), handle, fill=cream, font=footer_font)

    canvas.convert("RGB").save(output_path, "PNG", optimize=True)
    return True
