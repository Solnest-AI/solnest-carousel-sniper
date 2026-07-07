---
name: solnest-carousel-sniper
description: >
  Create a 7 to 12 slide magazine-grade Instagram carousel from a property listing (with Higgsfield enhancement) or from user-provided photos (BYOP). Use this skill whenever the user says snipe this carousel, snipe my listing, snipe this Airbnb, build me a carousel, make me a carousel, 7-slide carousel, 10-slide carousel, Instagram carousel for my Airbnb, carousel for this listing, carousel for this property, build me an IG carousel, luxury STR carousel, BYOP carousel, snipe four carousels, weekly carousel drop, or build me four Instagram carousels. Also triggers when the user pastes a listing URL or attaches photos and asks for marketing assets, social content, scheduled drops, or weekly content. Supports single carousels and multi-week series. Brand-agnostic, event-aware. Offer-code CTA built in. Voice rules enforced automatically. Output is numbered PNGs plus a voice-clean caption, all flat in one carousel folder. Final ship = images + caption.txt only.
---

# Solnest Carousel Sniper

When this skill fires, execute the workflow defined in `commands/solnest-carousel.md`. That document is the source of truth.

## Two photo input modes

The carousel builder supports TWO ways to source photos. ALWAYS ask the user upfront which one they want. Never assume.

### Mode A: Higgsfield enhanced (premium)
- Triggered when: user says yes to "Do you have Higgsfield (or plan to use an image generator)?"
- It scrapes the listing via Firecrawl, picks the best photos, runs them through Higgsfield Nano Banana 2 for cinematic luxury magazine enhancement, composes brand-styled text overlays on top.
- Higgsfield CDN URLs are publicly accessible — download the rawUrl into the carousel folder immediately after generation. Never leave photos stranded on Higgsfield.

### Mode B: BYOP (bring your own photos)
- Triggered when: user attaches photos to the chat, drops them in a folder, provides direct image URLs (Dropbox, Google Drive, etc.), or says they have professional photography.
- The carousel builder uses the user's photos as-is for the photo slides, composites brand-styled text overlays via Playwright on top.
- Best path for luxury STR owners with a photographer, product brands, lifestyle brands, anyone who already has assets.

### The upfront ask (mandatory first question)

Before any work begins, ask:

> "Do you have Higgsfield or plan to use an image generator for cinematic photo enhancement? Or are you bringing your own photos (BYOP)?"

Two answers only. If the user has neither, tell them:
> "To build a carousel you need either (a) Higgsfield credits for AI enhancement, or (b) your own property photos. Listing photo scraping alone produces inconsistent quality, so we don't ship that path. Want me to walk you through getting Higgsfield set up, or do you have photos you can attach?"

The tool does NOT scrape Airbnb listing photos and use them raw. That path is dropped from v2.

When the user pastes a URL AND attaches photos, default to BYOP. Their photos beat scraped photos every time.

## First-time setup required

The skill MUST check for `brands/_active.txt` before running. If it does not exist, point the user to `/solnest-carousel-setup` and stop. Do not invent a brand.

Exception: `/solnest-carousel-demo` skips this check and uses the neutral "warm-luxury" palette built into the skill, with @demo as the handle.

## Folder convention (locked)

Every carousel run produces this exact folder structure:

```
{output_folder}/carousel-{slug}/
├── 01_cover.png
├── 02_*.png
├── 03_*.png
├── ...
├── 07_cta.png
└── caption.txt
```

Rules:
- All slide PNGs at the root of the carousel folder, no subdirectories
- Zero-padded numerical prefixes (01, 02, ... not 1, 2, ...)
- Slide count is whatever the user picked at setup or per-run (7, 10, or 12)
- caption.txt at the root
- NO `slides/`, `photos/`, or `enhanced/` subfolders
- Audit files (plan.json, render scripts, source photos) ONLY saved if user explicitly asks. If saved, hide in `_source/` subdirectory.

The slug:
- Always kebab-case
- Always derived from the property NICKNAME the user provides during intake
- If user doesn't provide a nickname, ask "What's the short name for this property?" before generating any photos
- NEVER invent a slug from documentation examples or templates

## Voice rules (universal, enforced automatically)

All captions and slide headlines are stripped of:
- Em dashes
- En dashes
- Hashtags
- Engagement-bait questions (configurable per brand in `voice_rules.banned_phrases`)
- Generic AI phrasing

US spelling only.

## Step-by-step workflow

When the skill triggers:

### Step 1: Check for active brand
- Read `brands/_active.txt`. If missing, tell the user to run `/solnest-carousel-setup` first. Stop.
- Read `brands/{active_slug}.json` for palette, handle, offer defaults, voice rules.

### Step 2: Detect photo mode
- If user attached photos OR mentioned BYO photos → Mode C.
- If user provided a URL AND `mcp__...balance` (Higgsfield) returns OK → Mode A.
- Otherwise → Mode B (raw photos from URL).

### Step 3: Ask for the property nickname
- "What's the short name for this property?" — accept user's answer verbatim, slugify it for the folder name.
- Examples: "Crew Rest" → carousel-crew-rest, "Lake House" → carousel-lake-house.

### Step 4: Slide plan
- Show the slide plan in a table.
- Verb-led headlines on photo_feature slides.
- Event-aware: if a holiday is within 14 days of the post date, suggest an event_card slide. Always confirm.
- Wait for user approval before generating any photos.

### Step 5: Generate photos
- Mode A: call Higgsfield generate_image with nano_banana_2 + reference images. Poll job_display. Download rawUrl to `{carousel_folder}/0X_{name}.png` immediately.
- Mode B: download listing photos directly from Firecrawl scrape results. Composite text overlays via Playwright.
- Mode C: copy user-provided photos into the carousel folder. Composite text overlays via Playwright.

### Step 6: Render text-only slides
- Use Playwright to render info_card, event_card, quote, framework, prompt, stat, comparison slides.
- Apply brand palette from `brands/{active_slug}.json`.
- Output as `{carousel_folder}/0X_{name}.png` at 1080x1350.

### Step 7: Caption
- Generate caption per the brand voice. Strip em dashes, en dashes, hashtags, banned phrases.
- Save as `{carousel_folder}/caption.txt`.
- Use the brand's signoff line at the end if configured.

### Step 8: Verify completeness
- Before declaring done, list the carousel folder contents.
- Verify file count matches expected slide count + 1 (for caption.txt).
- If any photo download failed, retry once. If still failing, tell the user explicitly which slide is missing and provide a direct download link.

### Step 9: Present
- Show all slides as inline thumbnails in the chat (via present_files or job_display).
- Provide computer:// link to the carousel folder.
- Offer to queue for posting if a scheduler is configured.

## Slide types

| Type | Renderer | Best for |
|------|----------|----------|
| `photo_cover` | photo_overlay | Hero opener with cursive headline over enhanced or raw photo |
| `photo_feature` | photo_overlay | Interior, amenity, or landmark with verb-led headline |
| `cta_with_offer` | photo_overlay | Closer with offer pill ("Comment SAVE15 for 15%") |
| `info_card` | playwright | Dark or cream card with structured items (distances, features) |
| `event_card` | playwright | Date-anchored push (Memorial Day, Spring Break, launch week) |
| `quote` | playwright | Guest review, client win, pull quote, Bible verse |
| `framework` | playwright | Numbered list of steps |
| `prompt` | playwright | Copy-paste AI prompt, monospace block |
| `stat` | playwright | Big number with caption |
| `comparison` | playwright | Side-by-side before/after |

## Brand JSON shape

```json
{
  "name": "Brand Name",
  "slug": "brand-slug",
  "handle": "@handle",
  "signoff": "Optional tagline at end of captions",
  "palette": {
    "background": "#HEX",
    "text": "#HEX",
    "accent": "#HEX",
    "gold": "#HEX",
    "dark_surface": "#HEX",
    "cream": "#HEX"
  },
  "offer": {
    "default_code": "CODE",
    "default_amount": "15% off",
    "default_thing": "first stay"
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
    "banned_phrases": []
  }
}
```

## Sniper prompt pattern (copy-paste for users)

```
Snipe four Instagram carousels for [Property Name], one a week starting [date]: [Airbnb URL]. Ask me anything you need before you build.
```

After that, the carousel builder confirms property nickname, photo mode, offer code, and any anchor events within the window.

## What to do first when triggered

1. Greet the user briefly.
2. Check `brands/_active.txt`. If missing, point to `/solnest-carousel-setup`.
3. If they pasted a URL or attached photos, infer the mode. If ambiguous, ask.
4. Ask for the property nickname.
5. Build and show the slide plan. Wait for approval.
6. Generate photos, render text slides, write caption.
7. Verify file count. Present folder.

Always show the slide plan and wait for approval before generation. Photo enhancement credits are real money and the user always sees the plan first.
