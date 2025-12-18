#!/bin/bash

# ryze CMS v2 - GitHub Remote Setup Script
# This script configures remote branches and syncs with GitHub

REPO_URL="https://github.com/yourusername/ryze-beglobal.git"

echo "🔗 Setting up remote repository..."
git remote add origin $REPO_URL

echo "📤 Pushing all local branches to remote..."

# Push main branch
git push -u origin main

# Create and push remote branches
git push -u origin develop
git push -u origin feature
git push -u origin test
git push -u origin ready
git push -u origin archive

# Create additional remote branches for the sync pipeline
git checkout -b int
git push -u origin int

git checkout -b qa
git push -u origin qa

git checkout -b prod
git push -u origin prod

# Return to main
git checkout main

echo "✅ Remote setup complete!"
echo ""
echo "Next steps:"
echo "1. Replace 'yourusername' in REPO_URL with your GitHub username"
echo "2. Make sure the GitHub repository 'ryze-beglobal' exists"
echo "3. Run: bash .github-setup.sh"
echo ""
echo "Syncing branches (run from terminal):"
echo "  git push origin int:qa"
echo "  git push origin qa:prod"
echo "  git push origin prod:main"
