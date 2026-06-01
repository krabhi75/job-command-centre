# Host Job Command Centre on your domain

The **Cursor canvas** only runs inside Cursor IDE. For a live URL on your domain, use the **`web/`** app — a static site that loads `jobs.json` and auto-updates when you run the scraper.

## Quick start (no npm required)

Upload the **`web-static/`** folder to your host — it is plain HTML/CSS/JS:

- `web-static/index.html`
- `web-static/styles.css`
- `web-static/app.js`
- `web-static/jobs.json`

Open the URL in a browser. To refresh jobs, replace `jobs.json` after running the scraper.

## Optional: Vite dev server

```bash
cd web
npm install
npm run dev
```

Open http://localhost:5173 — no Cursor required.

## Build for production

```bash
python scripts/export_jobs_for_web.py   # refresh jobs.json from scraper
cd web
npm install
npm run build
```

Upload everything inside **`web/dist/`** to your hosting (cPanel `public_html/jobs/`, S3, etc.).

---

## Option A: Subdomain on your domain (recommended)

Example: `jobs.yourdomain.com`

### Using Vercel (free, easy)

1. Push this project to GitHub.
2. Go to [vercel.com](https://vercel.com) → Import repo.
3. Set **Root Directory** to `web`.
4. Build command: `npm run build`  
   Output directory: `dist`
5. Add domain: Project Settings → Domains → `jobs.yourdomain.com`
6. At your DNS provider, add a **CNAME**: `jobs` → `cname.vercel-dns.com`

### Using Netlify

Same as Vercel: root = `web`, publish = `dist`, add custom subdomain in Netlify DNS.

### Using cPanel / shared hosting

1. Run `npm run build` locally.
2. Upload contents of `web/dist/` to `public_html/jobs/` (or a subfolder).
3. Point subdomain `jobs` to that folder in cPanel.

---

## Option B: GitHub Pages + custom domain

1. Enable GitHub Pages on repo (Settings → Pages → source: `gh-pages` branch).
2. The workflow `.github/workflows/update-jobs.yml` builds and deploys daily.
3. Add **Secrets** → `APIFY_TOKEN` for live scraping.
4. Custom domain: Settings → Pages → Custom domain → `jobs.yourdomain.com`
5. DNS: **CNAME** `jobs` → `<username>.github.io`

---

## Auto-update jobs (no manual localhost)

### 1. GitHub Actions (already included)

- Runs daily at 6 AM IST.
- Needs repo secret: **APIFY_TOKEN**
- Commits updated `jobs.json` and redeploys site.

### 2. Cron on your VPS

```cron
0 6 * * * cd /path/to/empty-window && APIFY_TOKEN=xxx python job_scraper_enhanced.py && python scripts/export_jobs_for_web.py && cd web && npm run build && rsync -av dist/ /var/www/jobs/
```

### 3. Manual refresh

```bash
python job_scraper_enhanced.py          # writes job_output.json
python scripts/export_jobs_for_web.py # updates web/public/jobs.json
cd web && npm run build
# upload dist/ or push to trigger deploy
```

---

## Embed on your main website

Add a page that links or iframes the dashboard:

```html
<a href="https://jobs.yourdomain.com">Open Job Command Centre</a>
```

Or iframe (same-origin or allowed CSP):

```html
<iframe src="https://jobs.yourdomain.com" width="100%" height="900" title="Job tracker"></iframe>
```

---

## Troubleshooting

| Issue | Fix |
|--------|-----|
| Blank page after deploy | Ensure `base: './'` in `vite.config.js` (already set) |
| Jobs not updating | Run `export_jobs_for_web.py`; check `APIFY_TOKEN` |
| Canvas not loading in Cursor | Use [web app](web/) instead; canvas is IDE-only |
| 404 on refresh | Configure host SPA fallback to `index.html` |

---

## Files

| Path | Purpose |
|------|---------|
| `web/` | Hosted React dashboard |
| `web/public/jobs.json` | Data file the site loads |
| `scripts/export_jobs_for_web.py` | Scraper → JSON for web |
| `.github/workflows/update-jobs.yml` | Daily scrape + deploy |
