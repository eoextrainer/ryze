#!/bin/bash
# error-check.sh: Run a command, log output, scan for errors, and auto-fix common issues.

COMMAND="$@"
LOGFILE="error.log"
KNOWLEDGE="llm-brain.txt"

# 1. Run the command and log output
: > "$LOGFILE"
echo "[COMMAND] $COMMAND" >> "$KNOWLEDGE"
echo "[DATE] $(date)" >> "$KNOWLEDGE"

$COMMAND > "$LOGFILE" 2>&1

# 2. Scan for errors
if grep -iE 'error|exception|traceback|failed|missing' "$LOGFILE"; then
    echo "[ERROR DETECTED]" >> "$KNOWLEDGE"
    grep -iE 'error|exception|traceback|failed|missing' "$LOGFILE" >> "$KNOWLEDGE"
    # 3. Handle missing files
    if grep -i 'No such file\|not found' "$LOGFILE"; then
        FILES=$(grep -oE "[A-Za-z0-9_./-]+\.(py|sh|sql|ini|json|yml|yaml|txt)" "$LOGFILE")
        for FILE in $FILES; do
            echo "[SEARCHING FOR FILE] $FILE" >> "$KNOWLEDGE"
            find . -name "$FILE" >> "$KNOWLEDGE"
        done
    fi
    # 4. Handle missing dependencies
    if grep -i 'ModuleNotFoundError\|No module named\|not installed' "$LOGFILE"; then
        MODULES=$(grep -oE "No module named '[^']+'" "$LOGFILE" | awk -F\' '{print $2}')
        for MOD in $MODULES; do
            echo "[INSTALLING DEPENDENCY] $MOD" | tee -a "$KNOWLEDGE"
            pip install "$MOD" >> "$KNOWLEDGE" 2>&1
        done
    fi
    echo "[ERRORS FOUND] See $LOGFILE and $KNOWLEDGE for details. Fix errors before proceeding."
    exit 1
else
    echo "[SUCCESS] $COMMAND" >> "$KNOWLEDGE"
    echo "[NO ERRORS]" >> "$KNOWLEDGE"
    exit 0
fi

# Script to stage all changes, commit with relevant messages, and push all commits, logging all output and errors
LOGFILE="error.log"

# Clear previous log
> "$LOGFILE"

# Save all changes
{
  echo "==== git status ===="
  git status
} &>> "$LOGFILE"

# Stage all changes (including untracked)
{
  echo "==== git add ===="
  git add -A .
} &>> "$LOGFILE"

# Commit all staged changes with a single relevant message
{
  echo "==== git commit ===="
  if git diff --cached --quiet; then
    echo "No changes to commit."
  else
    git commit -m "Stage, commit, and push all changes via error-check.sh"
  fi
} &>> "$LOGFILE"

# Always push
{
  echo "==== git push ===="
  git push git@github.com:eoextrainer/ryze.git main
} &>> "$LOGFILE"

# Check for errors
if grep -i "error" "$LOGFILE"; then
  echo "Errors found in $LOGFILE. Please review and fix."
else
  echo "All steps completed successfully."
fi

git add -A . && git commit -m "Stage and commit all changes via error-check.sh" && git push git@github.com:eoextrainer/ryze.git main