---
description: Run the Solnest Carousel Sniper in demo mode. No setup required. Uses a neutral palette and drops carousels into a DEMO Carousels folder. Perfect for showing the tool live without configuring a brand.
---

# /solnest-carousel-demo

Demo mode for the Solnest Carousel Sniper. Skip the setup wizard, use a neutral warm-luxury palette, save outputs to `DEMO Carousels/` in the user's home directory (or wherever they mount).

## When to use

- Live demonstrations on podcasts, IG Lives, or sales calls
- Showing the tool to prospects who don't have their brand configured yet
- Quick tests of new property listings before deciding on a brand voice
- Teaching others how the workflow works without forcing them to commit

## Behavior

1. Skip the setup wizard entirely.
2. Load the built-in `warm-luxury` palette from the palette presets.
3. Set the output folder to `~/Dropbox/DEMO Carousels/` or `~/Documents/DEMO Carousels/` depending on what exists. If neither, create `~/Documents/DEMO Carousels/`.
4. Use the brand name "Demo Brand" and the handle "@demo" in any slide footer.
5. Use a generic CTA on the closing slide if no offer code is provided: "DM for details" rather than "Comment SAVE15."
6. Run the same Listing Mode / Topic Mode / YouTube Mode workflow as `/solnest-carousel`.

## Folder convention

```
DEMO Carousels/
└── carousel-{slug}/
    ├── 01_cover.png
    ├── 02_feature.png
    ├── 03_feature.png
    ├── 04_text.png
    ├── 05_text.png
    ├── 06_text.png
    ├── 07_cta.png
    └── caption.txt
```

Flat folder, numbered files, zero-padded prefixes, caption.txt at root. No `slides/` or `photos/` subfolders. Audit files (plan.json, source photos) only saved in `_source/` if the user explicitly asks for them.

## The slug

Ask the user once during intake: "What's the short nickname for this property?" Build the slug from kebab-cased nickname. Examples:
- "Crew Rest" → `carousel-crew-rest`
- "Emerald Lakes" → `carousel-emerald-lakes`
- "The Cabin in Colorado" → `carousel-cabin-in-colorado`

If the user doesn't give a nickname, default to a slugged version of the listing title. Never invent a slug from documentation examples or templates.

## After the run

Show the user:
- The carousel folder path (so they can find it in Finder)
- Inline thumbnails of all slides (via job_display or computer:// links)
- The caption.txt content
- A reminder that they can run `/solnest-carousel-setup` to configure their own brand for future runs

## What NOT to do in demo mode

- Do not reference any other brand (Solnest AI, another business, etc.) in copy or footers.
- Do not pull example offer codes from the documentation (SAVE15, SAVE10, etc.) into slides.
- Do not assume the user has any image-generation provider connected. If Higgsfield isn't installed, fall back to raw listing photos and tell the user.

## Footer in slides

Slide footers in demo mode should say `@demo` and a generic handle. The user can swap this later when they configure their brand.
