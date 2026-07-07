# SETUP — Read this and run it. (Claude: this file is for you.)

You are Claude, running in the **Claude Code desktop app**. A user just dropped the
**Solnest Carousel Sniper** plugin into the chat and said something like
**"set this up."**

This file is your script. Follow it top to bottom. Do the work FOR them. When you
finish, they will have the Solnest Carousel Sniper fully installed, their brand configured,
and their first real Instagram carousel built — without touching a single setting panel.

---

## Who you are talking to

A business owner at a live workshop. Smart, busy, **not technical.** They saw the
Solnest Carousel Sniper demoed today and it went over their head. Your job is to make this feel easy.

**Tone rules (follow these the whole way):**
- Warm, encouraging, plain English. No jargon. Never say "venv," "PATH," "stdout."
- One short friendly message per phase. Tell them what you're doing and why, like a
  helpful friend, not a terminal.
- **Never paste raw error text at them.** If something breaks, quietly fix it or
  translate it into one plain sentence + what you're doing about it.
- Do every technical step yourself with your tools. Only ask the human for the few
  things only they know (their brand details, their listing link).
- When the app asks them to approve a permission (file access, running a command),
  tell them plainly: "Click **Allow** when the box pops up — that's just the app
  asking permission for me to set things up."

**They already have Higgsfield and Firecrawl connected.** Don't make them set those up.
Just confirm they're there.

---

## The 6 phases (tell them this up front)

Open with something like:

> "Love it. I'll get the carousel builder fully set up for you and we'll build your first
> carousel before we're done. Six quick steps, I'll handle the technical parts. You'll just
> answer a few questions about your brand. Give me a sec to get started."

Then go:

1. Unpack the carousel builder
2. Check Higgsfield + Firecrawl are connected
3. Install the engine (the part that draws the slides)
4. Install the `/solnest-carousel` commands so they're permanent
5. Set up THEIR brand (colors, voice, handle)
6. Build their first carousel

---

## Phase 1 — Locate the carousel builder files

The user dragged in the **Solnest Carousel Sniper folder** (this `SETUP.md` lives inside it).
The pieces are already unpacked right here — no unzipping needed.

1. Figure out the operating system. You're on `win32` (Windows) or `darwin` (Mac).
   Use the matching commands throughout (PowerShell on Windows, bash/`unzip` on Mac;
   `python` vs `python3`, etc.). Adapt — don't assume.
2. Confirm you can see these folders sitting next to this file: `commands/`, `skills/`,
   `scripts/`, `templates/`, `brands/`. That's the whole builder.
3. (Only if the user instead dropped a single `solnest-carousel-sniper...v2...plugin`
   file — it's a ZIP despite the name; extract it to a temp folder first, then continue.)

You don't need to tell the human the file mechanics. Just: "Got the carousel builder. ✅"

---

## Phase 2 — Confirm Higgsfield + Firecrawl

The carousel builder needs two connections, which this user already has:
- **Higgsfield** — generates the cinematic photos.
- **Firecrawl** — reads their Airbnb/VRBO listing for the facts and photos.

Verify, don't install:
- Use **ToolSearch** to find them. Search `higgsfield`, then `firecrawl`, then as
  backups `generate image` and `scrape`. (Their exact tool names look like
  `mcp__...generate_image`, `mcp__...balance`, `mcp__firecrawl...scrape`.)
- If both are found → "Higgsfield and Firecrawl are both connected. ✅"
- If one is missing → tell them plainly which one, and that they can connect it from
  the app's connector list, then continue. Don't block the install over it — they can
  still finish setup and do a Bring-Your-Own-Photos carousel.

---

## Phase 3 — Install the engine

The carousel builder draws slides with a few small Python tools. Install them once, here.

**Install location (the home for all of the builder's files):**
```
~/.claude/skills/solnest-carousel-sniper/
```
Everything (`scripts/`, `templates/`, `brands/`) goes INSIDE that one folder. That
keeps the internal paths working with zero fiddling. Call this folder
**CAROUSEL_ROOT** from here on.

Steps:

1. **Create CAROUSEL_ROOT** and copy these from your extracted package into it:
   - `scripts/`  → `CAROUSEL_ROOT/scripts/`
   - `templates/` → `CAROUSEL_ROOT/templates/`
   - `brands/`   → `CAROUSEL_ROOT/brands/`
   - `skills/solnest-carousel-sniper/SKILL.md` → `CAROUSEL_ROOT/SKILL.md`

2. **Make sure Python 3 is installed — and if it isn't, INSTALL IT YOURSELF. Do not ask,
   do not pause, do not make the human do anything. Just install it and move on.**

   Detect it first: try `python3 --version`, then `python --version`, then (Windows)
   `py -3 --version`. Remember which command works.

   If none work, Python is missing. Install it silently, the fastest way for their OS:

   - **Windows** (winget ships with Windows 11):
     ```
     winget install -e --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
     ```
     If winget isn't available, download and run the official installer unattended:
     ```
     # download https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe  then:
     python-3.12.4-amd64.exe /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
     ```
   - **Mac**: if Homebrew exists → `brew install python@3.12`. If not, download the universal
     installer `https://www.python.org/ftp/python/3.12.4/python-3.12.4-macos11.pkg` and run
     `sudo installer -pkg python-3.12.4-macos11.pkg -target /`. (`xcode-select --install` also
     provides python3 as a fallback.)

   After installing, RE-DETECT the working Python command (you may need a fresh shell, or use
   the full path — on Windows `py -3` should now resolve). Confirm `--version` prints 3.x before
   continuing. The only thing the human sees is one calm line: "Installing a small free tool
   the carousel builder needs, about a minute." No choices, no jargon, no raw output.

3. **Install the two Python packages** the carousel builder needs — Pillow (photo compositing) and
   Playwright (the pretty text slides):
   ```
   <python> -m pip install --user pillow playwright
   ```
   If pip is missing, install it (`<python> -m ensurepip --upgrade`) then retry.

4. **Install Playwright's browser** (it uses this to render text slides crisply):
   ```
   <python> -m playwright install chromium
   ```
   This downloads ~150 MB once. Tell the human "grabbing a one-time component, ~30
   seconds." If it fails (offline, blocked), that's OK — the builder still renders text
   slides a simpler way. Don't stress them; just continue.

5. **Download the fonts** (the editorial typography for photo slides):
   ```
   <python> CAROUSEL_ROOT/scripts/setup_fonts.py
   ```
   This saves ~4 MB of fonts to `~/.solnest-carousel/fonts/`. If a font or two fails, fine —
   there's a fallback.

6. **(Windows only) Compatibility patch.** Open `CAROUSEL_ROOT/scripts/render_carousel.py`.
   Near the top add `import shutil` (if not present). Find the line that calls
   `subprocess.run(["cp", str(p), str(local)], check=False)` and replace it with
   `shutil.copy(str(p), str(local))`. (The `cp` command doesn't exist on Windows;
   this makes Bring-Your-Own-Photos work there.) Skip this entirely on Mac.

Tell the human: "The carousel builder's engine is installed. ✅"

---

## Phase 4 — Install the `/solnest-carousel` commands (so they're permanent)

So that next time they can just type `/solnest-carousel`, install the three commands and the
skill into their personal Claude folders.

1. Copy the command files into `~/.claude/commands/`, renaming the long one:
   - `commands/solnest-carousel.md` → `~/.claude/commands/solnest-carousel.md`
   - `commands/solnest-carousel-setup.md` → `~/.claude/commands/solnest-carousel-setup.md`
   - `commands/solnest-carousel-demo.md` → `~/.claude/commands/solnest-carousel-demo.md`

2. Copy the skill so natural language ("snipe this listing…") also works:
   - `CAROUSEL_ROOT/SKILL.md` is already in place. Also create
     `~/.claude/skills/solnest-carousel-sniper/SKILL.md` — it can BE that same file
     (CAROUSEL_ROOT/SKILL.md already lives at that path, so you're done).

3. **Fix the file paths.** The command files and SKILL.md refer to `brands/`,
   `scripts/`, and `templates/` as if they sit in the current folder. Now they live
   in CAROUSEL_ROOT. So at the very top of EACH of the three installed command files
   AND the SKILL.md, insert this note so future runs find everything:
   ```
   > CAROUSEL_ROOT = ~/.claude/skills/solnest-carousel-sniper
   > All paths below like brands/, scripts/, templates/ are inside CAROUSEL_ROOT.
   > Brand config + _active.txt live in CAROUSEL_ROOT/brands/.
   > Run scripts with:  <python> CAROUSEL_ROOT/scripts/render_carousel.py --plugin-root CAROUSEL_ROOT ...
   ```
   (Use the real expanded home path, and the `<python>` that worked in Phase 3.)

4. These become live slash commands **after a restart** — that's normal. Tell the
   human: "The carousel builder's commands are installed. They'll show up as `/solnest-carousel`
   next time you open a fresh chat. But we don't need to wait — let's set up your brand and build
   one right now."

---

## Phase 5 — Set up THEIR brand

Now follow the brand wizard. **The full wizard logic is in
`commands/solnest-carousel-setup.md`** (in your package) — read it and run it. Summary of what
to collect and where to save it:

**Preferred:** render the visual form. Call
`mcp__visualize__read_me({modules: ["elicitation"]})` then
`mcp__visualize__show_widget(...)` to show ONE card collecting all answers (brand
name, Instagram handle, sign-off line, typography preset, palette preset, default
offer code/amount/what-it-applies-to, output folder, slide count, voice rules).
Use the five typography presets and five palette presets exactly as listed in
`solnest-carousel-setup.md`. Preselect all voice rules.

**Fallback (if the visual form isn't available):** just ask them conversationally,
grouped, a few at a time. Don't make it feel like a form. For example:
> "Quick brand questions so the carousels sound like you:
> 1) Brand name? 2) Instagram handle? 3) Got a sign-off line for captions, or skip it?"
Then palette (offer the 5 presets in plain words), then offer code, then where to save
carousels (default `~/Documents/Carousels`).

**Save their answers** (per `solnest-carousel-setup.md`):
- Write `CAROUSEL_ROOT/brands/{slug}.json` (slug = kebab-case of their brand name),
  filling palette from the chosen preset, offer, defaults, and voice rules.
- Write `CAROUSEL_ROOT/brands/_active.txt` containing just the slug.

Important from the wizard doc: **do NOT preview their brand using any other brand's
voice or example offer codes** (no SAVE15, no "Solnest AI," etc.). Use neutral
placeholder copy only. This is THEIR brand.

Confirm: "Your brand's saved. The Solnest Carousel Sniper now knows you as @{handle}. ✅"

---

## Phase 6 — Build their first carousel (the payoff)

Now follow the main workflow in **`commands/solnest-carousel.md`** (in your
package). Run it for real. Key beats:

1. **Ask the one mandatory question:** Higgsfield-enhanced photos, or bring-your-own?
   (They have Higgsfield, so enhanced is the default wow path. If they'd rather use
   their own photographer's shots, that's Bring-Your-Own-Photos — equally good.)
2. **Get the source:** an Airbnb/VRBO link (enhanced or BYOP), or their photos/folder
   (BYOP). If they don't have a listing handy, offer `/solnest-carousel-demo` style neutral run.
3. **Intake, one question at a time, only what you can't infer:** property nickname
   (builds the folder name `carousel-{nickname}`), slide count (default to their saved
   preference), post date + any holiday within 14 days (offer an event slide), offer
   code (default to their saved one).
4. **Show the slide plan as a table and WAIT for approval.** Higgsfield credits are
   real money — they always see the plan first.
5. **Generate** after approval: Higgsfield images → download each to the folder
   immediately → composite brand overlays; text slides via Playwright; caption via the
   voice rules. Sleep ~3s between Higgsfield calls.
6. **Verify** the folder has exactly slide_count PNGs + `caption.txt`. Retry any
   missing slide once. Never declare done with a missing file.
7. **Present:** show the slides inline, give the folder path, show the caption, and
   tell them they can post the PNGs in order and paste the caption. Done.

The output lands flat and scheduler-ready:
```
{their output folder}/carousel-{slug}/
├── 01_cover.png … 0N_cta.png
└── caption.txt
```

---

## Final handoff

Close warm and clear:

> "That's the Solnest Carousel Sniper, fully set up — and you've got your first carousel in
> `{folder path}`. 🎉
>
> From now on it's one line. **Open a fresh chat** (so the new commands load) and type:
> - `/solnest-carousel` — build a carousel from any listing or your own photos
> - `/solnest-carousel-setup` — change your brand, colors, or voice anytime
> - `/solnest-carousel-demo` — a quick neutral demo, no brand needed
>
> Want me to build a second one now, or set up a weekly auto-drop?"

---

## Troubleshooting (for you, Claude — don't dump this on the human)

- **Python missing:** install it the simplest way for their OS (Phase 3, step 2), then
  resume. One friendly sentence to the human, no lecture.
- **`pip` blocked / `--user` errors:** try without `--user`, or
  `<python> -m pip install --upgrade pip` first.
- **Playwright browser won't download:** skip it. `render_playwright.py` auto-falls
  back to Pillow for text slides. Quality drops slightly; setup still completes.
- **Higgsfield photo URL won't download in a sandbox:** retry once; if still blocked,
  tell them this is a known hosted-sandbox quirk that doesn't happen on a normal
  install, and offer the Bring-Your-Own-Photos path for now.
- **Fonts failed:** fine — `render_photo_overlay.py` falls back to system fonts.
- **Commands don't appear after install:** they need a fresh chat / app restart. Expected.
- **Permissions popups:** tell the human to click **Allow** — it's the app asking on
  your behalf to create files and run the installer.

Stay calm, fix quietly, keep them feeling like this is working. That's the whole point.
