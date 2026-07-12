#!/usr/bin/env bash
# setup-keys.sh — reads your .env and wires up your keys.
#
# Your keys go from the .env file straight into the tool. They are never printed,
# never sent to the AI, and never written into a chat. This script only ever
# reports OK or MISSING.
set -uo pipefail
cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "❌ No .env file found in this folder."
  echo "   Copy .env.template to .env, paste your keys into it, and run this again."
  exit 1
fi

# Load the .env WITHOUT printing anything.
set -a; . ./.env; set +a

missing=0
found=0
need() {  # need VAR "Human name"
  if [ -z "${!1:-}" ]; then echo "  ⬜ $2 — blank in .env ($1), skipping"; missing=$((missing+1))
  else echo "  ✅ $2"; found=$((found+1)); fi
}

echo "Checking your .env..."

need FIRECRAWL_API_KEY "Firecrawl — reads the listing photos"

if [ "$found" -eq 0 ]; then
  echo
  echo "❌ Nothing is filled in yet. Open the .env file, paste your key(s), save, and run this again."
  echo "   (See KEYS.md for where to get each one.)"
  exit 1
fi
echo

echo "Registering your servers with Claude Code..."
if [ -n "${FIRECRAWL_API_KEY:-}" ]; then
  claude mcp remove firecrawl --scope user >/dev/null 2>&1 || true
  if claude mcp add firecrawl --scope user --env FIRECRAWL_API_KEY="$FIRECRAWL_API_KEY" -- npx -y firecrawl-mcp >/dev/null 2>&1; then
    echo "  ✅ firecrawl connected"
  else
    echo "  ❌ firecrawl failed to register — is Claude Code installed?"
  fi
fi
echo; echo "Done. Now FULLY QUIT AND REOPEN Claude Code so it picks up your keys."
