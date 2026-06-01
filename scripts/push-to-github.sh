#!/usr/bin/env bash
# Run from your machine (not inside read-only Cursor sandbox):
#   bash scripts/push-to-github.sh
set -euo pipefail

REPO_NAME="${1:-job-command-centre}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -d .git ]; then
  git init -b main
fi

git add -A
git status

if ! git diff --cached --quiet; then
  git commit -m "$(cat <<'EOF'
Add Job Command Centre with daily GitHub Pages deploy.

Hosted static dashboard for abhishekkumarproduct.co.in subdomain.
EOF
)"
fi

echo ""
echo "Creating GitHub repo and pushing (requires: gh auth login)..."
gh repo create "$REPO_NAME" --public --source=. --remote=origin --push 2>/dev/null || {
  echo "If repo exists, run: git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
  echo "Then: git push -u origin main"
  git push -u origin main
}

echo ""
echo "Next steps:"
echo "1. GitHub → Settings → Pages → Source: GitHub Actions"
echo "2. Settings → Secrets → APIFY_TOKEN (for live daily scrape)"
echo "3. DNS CNAME: jobs → YOUR_USERNAME.github.io"
echo "4. Pages → Custom domain: jobs.abhishekkumarproduct.co.in"
echo ""
echo "See DEPLOY-abhishekkumarproduct.md"
