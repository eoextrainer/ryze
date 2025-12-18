#!/usr/bin/env bash
set -euo pipefail

# Dunes CI helper: commit, push, trigger Render deploy, and open browser
# Requirements:
# - git configured with remote "origin" pointing to GitHub
# - Render auto-deploy enabled for the connected service
# - $BROWSER available in Codespaces (provided)
# - Optional: set RENDER_URL env var or add to .env / dunes.config

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$ROOT_DIR"

# Load optional config
RENDER_URL_DEFAULT=""
if [[ -f .env ]]; then
    # shellcheck disable=SC2046
    export $(grep -E '^(RENDER_URL|SERVICE_NAME)=' .env | xargs -d '\n') || true
fi
if [[ -f dunes.config ]]; then
    # shellcheck disable=SC2046
    export $(grep -E '^(RENDER_URL|SERVICE_NAME)=' dunes.config | xargs -d '\n') || true
fi

RENDER_URL="${RENDER_URL:-${RENDER_URL_DEFAULT}}"
SERVICE_NAME="${SERVICE_NAME:-dunes}"

echo "== Dunes Runner =="
echo "Repo: $(git remote get-url origin 2>/dev/null || echo 'no origin remote')"
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"

# Ensure a clean venv for any build steps (optional)
if [[ -d .venv ]]; then
    . .venv/bin/activate || true
fi

# Stage all changes and create a descriptive commit message
CHANGES="$(git status --porcelain)"
if [[ -z "$CHANGES" ]]; then
    echo "No local changes to commit. Proceeding to push and open Render URL."
else
    echo "Local changes detected. Creating safety stash checkpoint and committing."
    # Create a safety stash (kept for rollback/reference)
    STASH_REF="$(git stash create "pre-commit-snapshot-$(date +%Y%m%d-%H%M%S)")" || true
    if [[ -n "${STASH_REF:-}" ]]; then
        echo "Checkpoint stash created: $STASH_REF"
    fi

    # Auto-generate a concise commit message
    LAST_DIFF_SUMMARY="$(git diff --stat)"
    COMMIT_MSG="chore: dunes runner auto-commit

Summary:
${LAST_DIFF_SUMMARY}"

    git add -A
    git commit -m "$COMMIT_MSG" || {
        echo "Commit failed (possibly no staged changes). Continuing.";
    }
fi

# Push to origin to trigger Render auto-deploy
echo "Pushing to origin..."
git push origin "$(git rev-parse --abbrev-ref HEAD)"

echo "Push complete. If Render auto-deploy is enabled, a new deploy will start."

# Try to discover Render URL if not provided
if [[ -z "$RENDER_URL" ]]; then
    # Heuristic: read from render.yaml service name and infer common hostname
    if [[ -f render.yaml ]]; then
        YAML_NAME="$(grep -A2 'type: web' render.yaml | grep -E 'name:' | awk '{print $2}')"
        if [[ -n "$YAML_NAME" ]]; then
            SERVICE_NAME="$YAML_NAME"
        fi
    fi
    # Note: Actual Render URL is assigned per service; cannot be reliably inferred.
    echo "Render URL not set. Please set RENDER_URL in .env or dunes.config (e.g., https://dunes.onrender.com)."
fi

# Open the service URL if available
if [[ -n "$RENDER_URL" ]]; then
    echo "Opening Render service: $RENDER_URL"
    "$BROWSER" "$RENDER_URL" || true
else
    echo "Skipping browser open: Render URL unknown."
fi

echo "== Done =="
