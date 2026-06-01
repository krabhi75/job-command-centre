# Job sources (all platforms)

Your scraper pulls from **24+ portals** so listings are not missed.

## Via Daily Job Pulse aggregator

| Platform | Region |
|----------|--------|
| Naukri | India |
| Shine | India |
| TimesJobs | India |
| Foundit (Monster India) | India |
| Instahyre | India |
| Hirist | India |
| CutShort | India |
| Indeed | Global / India |
| Glassdoor | Global / India |
| Monster | Global |
| RemoteOK | Remote |
| WeWorkRemotely | Remote |
| ZipRecruiter | US/Global |
| Dice | Tech |
| StackOverflow Jobs | Tech |
| GitHub Jobs | Tech |
| CareerBuilder | Global |
| AngelList / Wellfound | Startups |
| + more | See `job_sources_config.py` |

## Dedicated scrapers (extra coverage)

| Platform | Why separate |
|----------|----------------|
| LinkedIn | Not in aggregator list; best PM volume |
| Wellfound | Startup PM roles |
| Internshala | Product management category |

Naukri / Indeed / Glassdoor are **skipped** as dedicated runs when the aggregator is on (avoids duplicates).

## Configure

Edit `job_sources_config.py`:

- `SEARCH_ROLES` — job titles to search
- `ALL_PULSE_SOURCES` — enable/disable portals
- `USE_AGGREGATOR` — set `False` to use only dedicated actors (cheaper)
- `MAX_RESULTS_PER_SOURCE` — jobs per portal (default 40)

## Apify cost note

Full scrape uses many actor credits. Monitor usage at https://console.apify.com/billing

## Output

- `job_output.json` — full scrape result
- `web-static/jobs.json` — live dashboard (via `scripts/export_jobs_for_web.py`)
