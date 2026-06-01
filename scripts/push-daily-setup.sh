#!/usr/bin/env bash
# Run on your machine to push and trigger first daily deploy
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Project: $(pwd)"
echo "Remote:  https://github.com/krabhi75/job-command-centre.git"
echo ""

git add -A
git status

if git diff --cached --quiet; then
  echo "No changes to commit."
else
  git commit -m "$(cat <<'EOF'
Switch to free JobSpy scraper and daily GitHub deploy.

- Free scraping (no Apify credits)
- Daily workflow 6 AM IST + auto deploy to jobs.abhishekkumarproduct.co.in
EOF
)"
fi

git push origin main

echo ""
echo "Done. Next:"
echo "1. https://github.com/krabhi75/job-command-centre/actions"
echo "2. Open 'Daily job dashboard update' -> Run workflow"
echo "3. Settings -> Actions -> General -> Allow all actions"
echo "4. Settings -> Pages -> Source: GitHub Actions"
echo ""
echo "Live site: https://jobs.abhishekkumarproduct.co.in"
