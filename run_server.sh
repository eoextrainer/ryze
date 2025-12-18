#!/bin/bash

# ryze Basketball Platform - Flask Server Launcher
cd /media/eoex/DOJO/CONSULTING/PROJECTS/ryze/cms-v2 || exit 1

# Check if .venv exists, activate it
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Kill any existing Flask processes on port 5000
echo "🧹 Cleaning up any existing processes..."
fuser -k 5000/tcp 2>/dev/null || true
sleep 1

# Start Flask app
echo "🚀 Starting ryze Basketball Flask Server..."
echo "📍 Server will be available at http://localhost:5000"
echo ""
echo "🔐 Demo Credentials:"
echo "   Club: contact@parisbball.fr / password123"
echo "   Player: player1@ryze.fr / password123"
echo ""

python app.py
