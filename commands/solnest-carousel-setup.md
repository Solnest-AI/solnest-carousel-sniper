---
description: One-time setup wizard for the Solnest Carousel Sniper. Run this first to configure your brand, folder location, and defaults.
---

# /solnest-carousel-setup

Brand-agnostic onboarding for the Solnest Carousel Sniper. The user runs this once. Their answers save to `brands/{slug}.json` in their plugin folder, and the path becomes `carouselDefaults.activeBrand`. Every future `/solnest-carousel` or `/solnest-carousel-demo` run reads from this config.

This command MUST be run before the main `/solnest-carousel` command if no brand JSON exists in `brands/`.

## What this does

1. Loads the elicitation form module (`mcp__visualize__read_me` with `modules: ["elicitation"]`).
2. Renders a single-card elicitation form via `mcp__visualize__show_widget` collecting the user's answers in one pass.
3. Writes the answers to `brands/{slug}.json` inside the plugin folder.
4. Optionally generates a starter `style_{slug}.png` reference image if the user picked a palette preset.
5. Confirms setup is complete and tells the user they can now run `/solnest-carousel`.

## The wizard form (HTML elicitation)

Use the elicitation module from `mcp__visualize__read_me({modules: ["elicitation"]})`. Render ONE form with these groups, in this order:

### Group 1: Brand basics (free text)
- "What's your brand name?" (data-name: brand_name)
- "What's your Instagram handle?" (data-name: instagram_handle, placeholder: "@yourhandle")
- "What's your sign-off line at the end of captions?" (data-name: signoff, placeholder: optional — example: 'Real estate that pays you back')

### Group 2: Typography (preview tile picker, single select)
Five preset tiles, each showing a sample headline rendered in that font family. The wizard renders each tile with a small inline SVG mock showing how "Pack the family" would look in that style. Pick a typography preset OR Custom (reveals font name inputs).

- **Editorial Luxury** — Bodoni Moda headlines, Inter body. Classic Vogue feel.
- **Soft Romantic** — Allura script eyebrows, Cormorant Garamond headlines, Inter body. Feminine luxury.
- **Modern Editorial** — DM Serif Display headlines, Inter body. Clean and modern.
- **Bold Direct** — Inter Bold everywhere, no serif. High contrast.
- **Heritage** — Playfair Display headlines, Cormorant body. Traditional luxury hospitality.

data-name: typography

The selected typography determines which Google Fonts get loaded into the Playwright HTML templates at render time. No font files ship with the plugin — they load from `fonts.googleapis.com` CDN.

### Group 3: Brand palette (preview tile picker, single select)
Five preset tiles, each with a small SVG illustration showing a swatch row, plus a Custom option:

- Warm luxury (cream + dark walnut + soft gold + burgundy accent)
- Modern editorial (warm white + true black + one bright accent)
- Feminine luxe (blush pink + cream + rose gold + deep mauve)
- Bold direct (black + white + electric accent + neutral gray)
- Earthy refined (sage + ivory + terracotta + clay)
- Custom (reveals 4 hex inputs: background, text, accent, gold-or-secondary)

data-name: palette

### Group 3: Default offer code (free text, optional)
- "Default offer code for your CTAs?" (data-name: offer_code, placeholder: "SAVE15")
- "Default discount amount?" (data-name: offer_amount, placeholder: "15% off")
- "What does the offer apply to?" (data-name: offer_thing, placeholder: "first stay", "your launch", etc.)

### Group 4: Folder location (file dropzone OR text path)
- "Where do you want your carousels saved?" (data-name: output_folder)
- Provide a textarea fallback for users to paste a path manually
- Default suggestion: `~/Documents/Carousels` if blank

### Group 5: Defaults (single-select pills)
- "Default slide count?" data-name: slide_count, options: 7, 10, 12
- "Folder prefix?" data-name: prefix, options: "carousel-", "drop-", "none"

### Group 6: Voice rules (multi-select pills, multi=true)
- "Enforce these voice rules in captions?" data-name: voice_rules
- Options (preselect all):
  - No em dashes
  - No en dashes
  - No hashtags
  - No engagement-bait questions
  - US spelling only

## After submit

The user's answers arrive as a single line. Parse them, then write the brand JSON.

```json
{
  "name": "{brand_name}",
  "slug": "{kebab-case of brand_name}",
  "handle": "{instagram_handle}",
  "signoff": "{signoff}",
  "palette": {
    "background": "...",
    "text": "...",
    "accent": "...",
    "gold": "..."
  },
  "offer": {
    "default_code": "{offer_code}",
    "default_amount": "{offer_amount}",
    "default_thing": "{offer_thing}"
  },
  "defaults": {
    "slide_count": 7,
    "folder_prefix": "carousel-",
    "output_folder": "~/Documents/Carousels"
  },
  "voice_rules": {
    "no_em_dashes": true,
    "no_en_dashes": true,
    "no_hashtags": true,
    "no_engagement_bait": true,
    "us_spelling": true,
    "banned_phrases": [
      "What would you automate?",
      "Which one are you trying first?",
      "Drop a comment if",
      "in today's fast-paced world",
      "unlock the power of"
    ]
  }
}
```

Save to: `brands/{slug}.json` inside the plugin folder.

Also write `brands/_active.txt` containing just the slug, so the main `/solnest-carousel` command knows which brand is active without re-asking.

## Palette presets (built-in)

```json
{
  "warm-luxury": {
    "background": "#EBE4D8",
    "text": "#1F1B17",
    "accent": "#5C2024",
    "gold": "#C5A572",
    "dark_surface": "#1F1B17",
    "cream": "#F5F0E8"
  },
  "modern-editorial": {
    "background": "#FAFAF8",
    "text": "#0A0A0A",
    "accent": "#D14C2A",
    "gold": "#0A0A0A",
    "dark_surface": "#0A0A0A",
    "cream": "#FAFAF8"
  },
  "feminine-luxe": {
    "background": "#F4E4DD",
    "text": "#2C1B1F",
    "accent": "#7A3147",
    "gold": "#B8896F",
    "dark_surface": "#2C1B1F",
    "cream": "#FAEDE8"
  },
  "bold-direct": {
    "background": "#FFFFFF",
    "text": "#000000",
    "accent": "#FF3B30",
    "gold": "#5E5E5E",
    "dark_surface": "#000000",
    "cream": "#F5F5F5"
  },
  "earthy-refined": {
    "background": "#EDE7D6",
    "text": "#2A2520",
    "accent": "#A0522D",
    "gold": "#7A8266",
    "dark_surface": "#2A2520",
    "cream": "#F2EDDF"
  }
}
```

## Confirmation message after save

```
Setup complete. The Solnest Carousel Sniper now knows you as @{handle}.

Your brand is saved as brands/{slug}.json.
Your carousels will save to {output_folder}.

You can now run:
- /solnest-carousel  (full carousel snipe with brand voice)
- /solnest-carousel-demo  (no-brand-needed demo run)

To change anything later, run /solnest-carousel-setup again.
```

## Voice rule reminder

When the user is going through setup, do NOT preview their brand using your own brand or any other example brand's voice. Use generic placeholder copy in any preview cards. The setup is for THEIR brand, not yours.
