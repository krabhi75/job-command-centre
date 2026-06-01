# Free job scraping (no Apify)

Your project now defaults to **open-source scraping** — **$0 Apify usage**.

## What runs by default

| Tool | License | Sources | Cost |
|------|---------|---------|------|
| **[python-jobspy](https://github.com/speedyapply/JobSpy)** | MIT | Indeed, LinkedIn, Glassdoor, Google Jobs, **Naukri** | Free |
| **RemoteOK API** | Public API | Remote PM roles | Free |

Entry point: `python job_scraper_enhanced.py`  
Implementation: `job_scraper_free.py`

## Setup

```bash
pip install -r requirements.txt
python job_scraper_enhanced.py
python scripts/export_jobs_for_web.py
```

No `APIFY_TOKEN` required.

## GitHub Actions

The daily workflow uses `SCRAPER_BACKEND=free` automatically.  
You can **remove** `APIFY_TOKEN` from GitHub secrets to avoid accidental Apify charges.

## Switch back to Apify (optional)

Only if you want 24+ portals and can pay for credits:

```bash
# .env
SCRAPER_BACKEND=apify
APIFY_TOKEN=apify_api_xxxx
```

## Limitations (free tier)

| Topic | Reality |
|-------|---------|
| **LinkedIn** | Often rate-limits; may return fewer jobs without proxies |
| **Naukri / Indeed** | Usually work; sites change HTML → JobSpy updates help |
| **Instahyre, Hirist, CutShort** | Not in JobSpy — need custom scrapers or Apify |
| **Legal** | Respect robots.txt & terms; personal job search use |
| **Reliability** | DIY — blocks happen; re-run or slow down |

## Other open-source options

| Project | Use for |
|---------|---------|
| [JobSpy](https://github.com/speedyapply/JobSpy) | **Already integrated** |
| [jobspy-js](https://github.com/borgius/jobspy-js) | Node.js version + Naukri |
| [Scrapy](https://scrapy.org/) | Build custom spiders per site |
| [Playwright](https://playwright.dev/python/) | Naukri when API blocks (heavy) |
| Company **RSS / careers JSON** | Free, very stable for named companies |

## Add more free sources later

Edit `job_scraper_free.py`:

1. Add a function like `scrape_remoteok()`
2. Call it from `collect_all_jobs()`
3. Reuse `base_job()` and `dedupe_jobs()`

## Compare: Free vs Apify

| | Free (JobSpy) | Apify |
|--|---------------|-------|
| Cost | $0 | ~$5+ / month typical |
| India portals | Indeed, Naukri, Google, Glassdoor, LinkedIn | 24+ including Hirist, CutShort |
| Setup | `pip install` | API token |
| Maintenance | You | Apify actors updated by authors |

**Recommendation:** Stay on **free** until you hit limits; then enable Apify only for missing portals.
