---
description: Snipe an Airbnb, VRBO, topic, YouTube URL, or photo set into a 7 to 12 slide Instagram carousel in your brand voice. Run /solnest-carousel-setup first to configure your brand.
argument-hint: "[listing URL, topic, photo paths, or property nickname]"
---

# /solnest-carousel

The main Solnest Carousel Sniper command. Listing URL, topic, YouTube link, or photos in. A magazine-grade Instagram carousel out.

## Preflight check

Before doing anything else:

1. Read `brands/_active.txt` to find the active brand slug.
2. If missing, stop and tell the user: "Run `/solnest-carousel-setup` first so I know your brand voice. Or run `/solnest-carousel-demo` for a one-off without setup."
3. If present, read `brands/{active_slug}.json` for palette, handle, offer code, voice rules.

## Mandatory upfront question (before anything else)

Ask ONE question before any work begins:

> "Do you have Higgsfield (or another image generator you plan to use) for AI photo enhancement? Or are you bringing your own photos?"

Two valid answers:
- **Higgsfield / image generator** → Mode A. It will scrape the listing URL, enhance photos via Higgsfield Nano Banana 2, compose slides on top.
- **BYOP (bring your own photos)** → Mode B. It will use the user's photos (attached, dropped in a folder, or linked via URL) and composite text overlays on top.

If the user has neither, say:
> "To build a carousel you need either (a) Higgsfield credits (paid AI enhancement, about 8 credits per carousel) or (b) your own property photos. Raw listing scraping produces inconsistent quality, so we don't ship that path. Want help getting Higgsfield set up, or can you send your photos?"

Stop. Wait for an answer. Do not proceed without one of these two paths.

## Other input signals

After the photo path is locked, parse the rest of the request:

| Signal | Mode | Action |
|---|---|---|
| Airbnb or VRBO URL pasted | Listing source | Firecrawl scrape for property facts, reviews, locations |
| YouTube URL pasted | Repurpose source | Pull transcript, extract actionable moments |
| Plain topic ("carousel about...") | Topic source | Plan slides from scratch |
| Photos attached or folder mentioned | Confirms BYOP | Use those photos in order |

## Intake (per run)

Ask these in order, ONE at a time, and only the ones not already inferred:

1. **Property nickname**: "What's the short name for this property?"
   - Skip if already in conversation context (e.g., user wrote "snipe my Lake House listing")
   - Used to build the folder slug: `carousel-{nickname-kebab-case}`

2. **Slide count**: 7, 10, or 12 (default to brand's saved preference)

3. **Post date and event anchor**: "When is this scheduled to post?"
   - Check upcoming holidays within 14 days of the post date
   - If a match, ask: "Want me to add an event slide for {holiday}?"

4. **Offer code override**: "Use your default offer code ({brand.offer.default_code}) or override?"
   - Default to brand's saved code if no override

5. **Photo enhancement mode** (only ask if Mode A is available):
   - "Use Higgsfield to enhance the photos (cinematic luxury magazine look, uses credits), OR keep raw photos (free, faster)?"
   - Skip if user is in BYO Photo Mode — their photos go in as-is

## Slide plan

Build a slide plan table and SHOW IT TO THE USER. Wait for explicit approval before generating any photos.

Example structure:

| # | Type | Headline | Photo source |
|---|------|----------|------|
| 1 | photo_cover | Pack the family | Higgsfield enhanced exterior |
| 2 | photo_feature | Soak year-round | Higgsfield enhanced hot tub |
| 3 | photo_feature | Tournament-ready | Higgsfield enhanced game loft |
| 4 | info_card | Closer than you think | Text only, location |
| 5 | event_card | Long weekend, last call | Text only, Memorial Day |
| 6 | quote | 5-star pull quote | Text only |
| 7 | cta_with_offer | Book the retreat | Higgsfield enhanced + SAVE15 pill |

## Generation

After user approves the plan:

### Mode A — Higgsfield enhanced
1. Call `mcp__...generate_image` with `model: nano_banana_2`, `aspect_ratio: 4:5`, reference image from the listing scrape.
2. Poll `job_display` until status is `completed`.
3. **Immediately download** `results.rawUrl` to `{carousel_folder}/0X_{name}.png` using `curl -L` or `requests.get`. Do not move on until the file is on disk.
4. Composite the brand text overlay on top via Playwright (eyebrow, headline, subtitle, dots).
5. Save as `{carousel_folder}/0X_{name}.png`.
6. If the download fails (network, expired URL, etc.), retry once. If still failing, stop and tell the user explicitly with a direct download link. Do not proceed past this point with a missing file.

### Mode B — BYOP (bring your own photos)
1. Identify the user's photos: chat attachments, folder reference, or linked URLs.
2. Copy or download each photo into a temporary working location.
3. Use Playwright to composite the brand text overlay on top of each photo.
4. Save as `{carousel_folder}/0X_{name}.png`.
5. If a photo is missing or unreadable, stop and ask the user for a replacement before continuing.

### Text-only slides
1. Use Playwright HTML to PNG rendering with the brand palette.
2. Save as `{carousel_folder}/0X_{name}.png`.

## Caption

Generate caption using brand voice. Strip em dashes, en dashes, hashtags, banned phrases. Append brand signoff line if configured. Save as `{carousel_folder}/caption.txt`.

## Verification

Before declaring done:

1. Count files in `{carousel_folder}`. Should equal `slide_count + 1` (PNGs + caption.txt).
2. If short by any photo slide, retry that one slide.
3. List the actual contents. If any expected file is missing, name it explicitly.

## Presentation

1. Show all slides as inline thumbnails (via `present_files` or `job_display`).
2. Provide a `computer://` link to the carousel folder so user can open in Finder.
3. Show the caption content.
4. Offer next steps: "Want me to queue for posting, build a Reels script from this same property, or snipe another listing?"

## Multi-week / multi-carousel mode

If user says "snipe FOUR carousels..." or "weekly carousel drop":

1. Confirm: "Four carousels for [Property] starting [date], one per week. Anchor events in window: [list]. Use [SAVE15 / escalating offers / same code each week]?"
2. Run the full workflow 4 times, varying:
   - The hook angle (lifestyle, ROI, location, design, etc.)
   - The CTA urgency (early bird, last call, escalating discount)
   - Event anchors per week
3. Save each carousel in its own folder: `carousel-{slug}-w1`, `carousel-{slug}-w2`, etc.

## Universal rules

- No em dashes, no en dashes, no hashtags, no engagement bait in slide copy or captions.
- US spelling only.
- Use the user's brand frameworks verbatim if mentioned. Never paraphrase a named framework.
- Default to 1080x1350 (4:5 portrait) for IG feed.
- Sleep 3 seconds between Higgsfield API calls to respect rate limits.
- Retry once on failure before skipping.
- Never declare done if any slide is missing from the folder. Verify file count.

## Output (the final folder)

```
{output_folder}/carousel-{slug}/
├── 01_cover.png
├── 02_feature.png
├── 03_feature.png
├── 04_text.png
├── 05_text.png
├── 06_text.png
├── 07_cta.png
└── caption.txt
```

Numbered. Flat. Scheduler-ready.
