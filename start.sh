#!/bin/bash

# Dunes Basketball Platform - Universal Startup Script
# Usage: ./start.sh

# Activate Python virtual environment if present
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Kill any existing Flask processes on port 5000
fuser -k 5000/tcp 2>/dev/null || true
sleep 1

# Start Flask app
python3 app.py
