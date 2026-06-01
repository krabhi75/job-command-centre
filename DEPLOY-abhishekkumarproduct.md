# Deploy Job Command Centre on abhishekkumarproduct.co.in

## Recommended URL

**https://jobs.abhishekkumarproduct.co.in**

A separate subdomain keeps your main portfolio site unchanged.

---

## Step 1 — Push to GitHub

Repo is set up in this folder. After push, enable **GitHub Pages**:

1. GitHub repo → **Settings** → **Pages**
2. **Build and deployment** → Source: **GitHub Actions**
3. Wait for the **Daily job dashboard update** workflow to finish (green check)

Your site will be live at: `https://<github-username>.github.io/<repo-name>/` until DNS is configured.

---

## Step 2 — Add Apify token (live daily scraping)

1. Repo → **Settings** → **Secrets and variables** → **Actions** → **Secrets** tab
2. **New repository secret** → Name: `APIFY_TOKEN` → paste token from https://console.apify.com/settings/integrations

Use **Secrets**, not **Variables** (variables can be visible in the UI).

If you already added it as an environment variable on `github-pages`, it still works — but move it to a **secret** for security and rotate the token if it was ever shared or screenshotted.

---

## Step 3 — Deploy the site first (fixes DNS check)

1. Push latest code to `main`
2. **Actions** → **Deploy Job Command Centre** → **Run workflow**
3. Wait for green checkmark
4. Then **Settings** → **Pages** → **Check again** on custom domain

GitHub often shows "DNS check unsuccessful" until the **first successful deploy** exists.

## Step 4 — DNS (CNAME for subdomain)

At your domain registrar (where you bought **abhishekkumarproduct.co.in**):

| Type  | Name | Value                    | TTL  |
|-------|------|--------------------------|------|
| CNAME | jobs | `<username>.github.io`   | 3600 |

Replace `<username>` with your GitHub username.

**Also in GitHub:** Settings → Pages → Custom domain → enter:

`jobs.abhishekkumarproduct.co.in`

GitHub will verify DNS and enable HTTPS (can take up to 24 hours).

The file `web-static/CNAME` already contains `jobs.abhishekkumarproduct.co.in`.

---

## Alternative: page on main domain (no subdomain)

If you want **https://abhishekkumarproduct.co.in/jobs** instead:

1. Upload everything in `web-static/` to your host’s `public_html/jobs/` folder.
2. **No CNAME** needed — only a folder on your existing site.
3. Link from your homepage: `<a href="/jobs/">Daily Job Tracker</a>`

Daily updates: run on your server or use GitHub Actions + FTP deploy (advanced).

---

## Daily updates (automatic)

Workflow: `.github/workflows/update-jobs.yml`

- Runs every day at **6:00 AM IST**
- Scrapes jobs (if `APIFY_TOKEN` is set)
- Updates `web-static/jobs.json`
- Redeploys GitHub Pages

Manual run: Actions → **Daily job dashboard update** → **Run workflow**

---

## Link from your portfolio

Add to your main site navigation:

```html
<a href="https://jobs.abhishekkumarproduct.co.in">Job Command Centre</a>
```

Or for path deploy:

```html
<a href="/jobs/">Job Command Centre</a>
```
