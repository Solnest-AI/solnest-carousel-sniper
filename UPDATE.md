# UPDATE — Solnest Carousel Sniper (Claude reads this)

**You are Claude. The user pasted this repo's link and asked you to update their Solnest Carousel Sniper. Do it FOR them, safely, in plain language.**

**The one rule that matters: this update must NOT wipe their brand.** Their brand colors, handle, and sign-off live *inside* the skill folder. Blow those away and they have to redo the whole setup wizard. Follow the preserve list below exactly.

---

## Step 0 — Find their install

The skill lives here:

- macOS / Linux: `~/.claude/skills/solnest-carousel-sniper/`
- Windows: `%USERPROFILE%\.claude\skills\solnest-carousel-sniper\`

Their slash commands live here:

- macOS / Linux: `~/.claude/commands/solnest-carousel.md`, `solnest-carousel-setup.md`, `solnest-carousel-demo.md`
- Windows: the same three files under `%USERPROFILE%\.claude\commands\`

If the skill folder isn't there, they never installed it. Don't "update" — tell them to grab the zip from the Skool community and drag it in to install fresh, and stop here.

## Step 1 — Check if they even need this

Read `VERSION` in their install folder, and compare it to `VERSION` in this repo.

If the numbers match, say so and stop:

> You're already on the latest version (`X.Y.Z`) — nothing to update. You're good.

Don't do the work if there's nothing to do.

## Step 2 — PRESERVE THIS (do not skip)

Before you copy a single file, back these up to a temp folder. These are **theirs**, not yours:

| Path (inside the skill folder) | What it is |
|---|---|
| `brands/*.json` — **except** `brands/template.json` | Their brand: colors, handle, sign-off. Irreplaceable. |
| `brands/_active.txt` | Which brand is currently selected. |

`brands/template.json` is shipped by the repo and SHOULD be overwritten — it's the starter template, not their brand.

Their fonts live at `~/.solnest-carousel/fonts/` — **outside** the skill folder. Leave that alone entirely; the update never touches it.

## Step 3 — Pull the latest

Download this repo fresh into a temp folder:

```bash
git clone --depth 1 https://github.com/Solnest-AI/solnest-carousel-sniper.git /tmp/scs-update
```

If `git` isn't available, download the zip instead:
`https://github.com/Solnest-AI/solnest-carousel-sniper/archive/refs/heads/main.zip`

## Step 4 — Copy the new files over

Overwrite the skill folder with the fresh copy, **but never delete the whole folder first** — copy file over file, so anything you preserved survives.

Update these:
- `SKILL.md` and everything under `skills/`
- `scripts/` (all of it)
- `templates/` (all of it)
- `brands/template.json` (the template only)
- `README.md`, `SETUP.md`, `START-HERE.md`, `CHANGELOG.md`, `VERSION`

Then refresh the three slash commands in `~/.claude/commands/`:
- `commands/solnest-carousel.md`
- `commands/solnest-carousel-setup.md`
- `commands/solnest-carousel-demo.md`

## Step 5 — Put their brand back

Restore everything you backed up in Step 2 into `brands/`. Then verify, out loud to yourself:

- Does `brands/{their-slug}.json` still exist?
- Does `brands/_active.txt` still name that same slug?

If either is missing, restore it from the backup before you say a word to the user. **Never tell them the update worked until you've confirmed their brand survived.**

## Step 6 — Tell them what changed

Read `CHANGELOG.md` from the fresh copy and summarize *only* the new version's entries — two or three plain-English bullets. Not the whole file.

Then close with something like:

> Updated to `X.Y.Z`. Your brand ({their brand name}) came through untouched — colors, handle, and sign-off are all still set. Just run `/solnest-carousel` like normal.

## If something goes wrong

Restore the backup from Step 2 and tell them in one friendly sentence what happened. Never paste a raw error at them. They can always reinstall from the Skool zip — nothing here is destructive if you kept the backup.
