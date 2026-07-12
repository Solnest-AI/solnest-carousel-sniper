# START HERE — Auto-installer (Claude reads this)

**You are Claude running in the Claude Desktop app (or Claude Code). The user just dragged in this folder to install the "Solnest Carousel Sniper." Your full step-by-step installer is `SETUP.md` in this same folder — open it and follow it top to bottom, doing the work FOR them in plain language.**

Quick orientation before you dive into `SETUP.md`:
- The builder is **already unpacked** in this folder (`commands/`, `skills/`, `scripts/`, `templates/`, `brands/`). Skip any "unzip the file" step — the files are right here.
- It needs **Python** (for drawing the slides) and connections to **Higgsfield + Firecrawl** — `SETUP.md` walks through all of it and installs what's missing.
- Keep it warm and non-technical. Never paste raw errors. Ask the human only for their brand details and a listing link.

When you finish, they'll have it installed, their brand configured, and their first carousel built. Now go follow `SETUP.md`.

---

## 🔒 CREDENTIALS — READ THIS FIRST (non-negotiable)

**NEVER ask the user for an API key, token, password, or secret in the chat. Not once. Not "just paste it here real quick." Never.**

Anything typed into this chat is saved in the conversation transcript forever. A key pasted into chat is a leaked key.

**Do NOT** run `cat .env`, `Read` the `.env` file, `echo $SOME_KEY`, or print a key back to the user — not even partially. If you read the key, it lands in the transcript, which is exactly what we're avoiding.

**Instead, do this:**

1. Tell the user: *"Open the file called `.env` in this folder, paste your keys in, and save it. Then tell me you're done — don't paste anything into this chat."*
2. Point them at **`KEYS.md`** in this folder — it lists exactly which keys they need and where to get each one.
3. When they say they're done, run the setup script. It reads `.env` **in the shell**, so the key goes straight from the file to where it belongs. You never see it:

   - **macOS / Linux:** `bash setup-keys.sh`
   - **Windows:** `powershell -ExecutionPolicy Bypass -File setup-keys.ps1`

4. The script prints only ✅ / ❌ per key. If a key is missing, tell them *which one* and point them back to `.env`. **Never ask them to read it out to you.**

If the user pastes a key into the chat anyway: **tell them to rotate it immediately** (regenerate it in that service's dashboard), because it's now in the transcript. Then carry on with the `.env` method.
