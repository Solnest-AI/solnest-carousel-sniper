# Changelog

## [2.1.0] — 2026-06-24

Drag-and-drop self-setup, for non-technical users (conference distribution).

### Added
- `SETUP.md` — a baked-in, self-running install walkthrough. User drops the `.plugin`
  into the Claude Code desktop app, says "set this up," and Claude auto-installs the
  engine, the `/solnest-carousel` commands, configures their brand, and builds their first
  carousel. Replaces the multi-step Customize → Create Plugin → Upload manual flow.
- README + plugin description point Claude to SETUP.md on drop.

### Notes
- Installs into `~/.claude/skills/solnest-carousel-sniper/` (engine + scripts +
  templates + brands) and `~/.claude/commands/` (solnest-carousel, solnest-carousel-setup,
  solnest-carousel-demo).
- Assumes Higgsfield + Firecrawl already connected; verifies, does not install them.
- Windows compatibility patch for the BYOP `cp` call is applied at setup time.

## [2.0.0] — 2026-05-15

Rebuilt as a gift-friendly, brand-agnostic plugin.

### Added
- `/solnest-carousel-setup` first-time wizard with palette and typography presets
- `/solnest-carousel-demo` no-setup demo entry point
- BYOP (bring your own photos) mode for users with their own photography
- Verify-file-count step before declaring done
- Typography presets: Editorial Luxury, Soft Romantic, Modern Editorial, Bold Direct, Heritage
- Google Fonts installer (`setup_fonts.py`)
- Playwright HTML templates for text slides (info-card, event-card, quote)

### Changed
- Flat folder output convention (no `slides/` or `photos/` subfolders)
- All slide files numbered with zero-padded prefix
- Higgsfield is now optional, asked upfront
- Voice rules enforced automatically in caption generator
- Manifest stripped to minimal validator-friendly fields

### Removed
- Raw URL listing photo mode (inconsistent quality, dropped)
- Hardcoded brand JSONs — recipients configure their own brand

## [1.2.2] — earlier
- Previous version. Archived for reference.
