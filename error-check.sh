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
