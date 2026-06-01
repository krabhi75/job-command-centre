"""
Free / open-source job scraper (no Apify).
Uses python-jobspy (MIT) + public APIs. Zero Apify credits.
"""

import json
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import requests

from job_sources_config import SEARCH_ROLES, LOCATION, MAX_DAYS_OLD
from job_scraper_apify import (
    PROFILE,
    OUTPUT_FILE,
    calculate_fit_score,
    categorize_jobs,
    dedupe_jobs,
    base_job,
)

# Sites supported by python-jobspy (https://github.com/speedyapply/JobSpy)
JOBSPY_SITES = ["indeed", "linkedin", "glassdoor", "google", "naukri"]

HOURS_OLD = min(MAX_DAYS_OLD * 24, 168)


def scrape_with_jobspy() -> List[Dict]:
    try:
        from jobspy import scrape_jobs
    except ImportError:
        print("Install: pip install python-jobspy pandas")
        return []

    search_term = " OR ".join(SEARCH_ROLES[:3])
    print(f"JobSpy: {JOBSPY_SITES} | query={search_term!r} | location={LOCATION}")

    try:
        df: pd.DataFrame = scrape_jobs(
            site_name=JOBSPY_SITES,
            search_term=search_term,
            location=LOCATION,
            results_wanted=35,
            hours_old=HOURS_OLD,
            country_indeed="India",
            linkedin_fetch_description=False,
        )
    except Exception as e:
        print(f"JobSpy error: {e}")
        return []

    if df is None or df.empty:
        return []

    jobs = []
    for _, row in df.iterrows():
        site = str(row.get("site", row.get("job_url", "Unknown")))
        if hasattr(site, "name"):
            site = site.name
        source = str(site).replace("_", " ").title()
        if "Indeed" in source or site == "indeed":
            source = "Indeed"
        elif "linkedin" in str(site).lower():
            source = "LinkedIn"
        elif "glassdoor" in str(site).lower():
            source = "Glassdoor"
        elif "google" in str(site).lower():
            source = "Google Jobs"
        elif "naukri" in str(site).lower():
            source = "Naukri"

        salary = "Not disclosed"
        min_amt = row.get("min_amount")
        max_amt = row.get("max_amount")
        if pd.notna(min_amt) and pd.notna(max_amt):
            salary = f"₹{min_amt}-{max_amt} LPA"
        elif pd.notna(row.get("salary")):
            salary = str(row.get("salary"))

        jobs.append(
            base_job(
                source=source,
                title=str(row.get("title", "")),
                company=str(row.get("company", "")),
                location=str(row.get("location", LOCATION)),
                salary=salary,
                url=str(row.get("job_url", row.get("link", "#"))),
                description=str(row.get("description", "")),
                posted_date=str(row.get("date_posted", "")),
            )
        )
    return jobs


def scrape_remoteok() -> List[Dict]:
    """RemoteOK public JSON API — free, no key."""
    print("RemoteOK: public API")
    try:
        r = requests.get(
            "https://remoteok.com/api",
            headers={"User-Agent": "JobCommandCentre/1.0"},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"RemoteOK error: {e}")
        return []

    keywords = ["product", "pm", "manager"]
    jobs = []
    for item in data:
        if not isinstance(item, dict) or "position" not in item:
            continue
        title = (item.get("position") or "").lower()
        if not any(k in title for k in keywords):
            continue
        jobs.append(
            base_job(
                source="RemoteOK",
                title=item.get("position", ""),
                company=item.get("company", ""),
                location=item.get("location", "Remote"),
                salary=item.get("salary", "Not disclosed") or "Not disclosed",
                url=item.get("url") or item.get("apply_url") or "#",
                description=item.get("description", ""),
                posted_date=item.get("date", ""),
            )
        )
        if len(jobs) >= 40:
            break
    print(f"  RemoteOK: {len(jobs)} PM-related jobs")
    return jobs


def collect_all_jobs() -> List[Dict]:
    all_jobs: List[Dict] = []
    all_jobs.extend(scrape_with_jobspy())
    all_jobs.extend(scrape_remoteok())
    before = len(all_jobs)
    all_jobs = dedupe_jobs(all_jobs)
    print(f"Total: {before} -> after dedupe: {len(all_jobs)}")
    return all_jobs


def main():
    print("=" * 80)
    print("Job Command Centre — FREE open-source scrape (no Apify)")
    print(f"Profile: {PROFILE['name']} — {PROFILE['title']}")
    print("=" * 80)
    print()

    all_jobs = collect_all_jobs()
    if not all_jobs:
        print("No jobs found. Try again later or add proxies for LinkedIn.")
        print("See FREE-SCRAPING.md")
        return

    for job in all_jobs:
        job["fit_score"] = calculate_fit_score(job)
    all_jobs.sort(key=lambda x: x["fit_score"], reverse=True)
    categorized = categorize_jobs(all_jobs)
    sources_used = sorted({j["source"] for j in all_jobs})

    output_data = {
        "profile": PROFILE,
        "scrape_timestamp": datetime.now().isoformat(),
        "scraper": "jobspy+remoteok",
        "sources_scraped": sources_used,
        "total_jobs": len(all_jobs),
        "summary": {
            "high_probability": len(categorized["high_probability"]),
            "medium_probability": len(categorized["medium_probability"]),
            "stretch_roles": len(categorized["stretch_roles"]),
            "low_fit": len(categorized["low_fit"]),
        },
        "jobs": {
            "high_probability": categorized["high_probability"],
            "medium_probability": categorized["medium_probability"],
            "stretch_roles": categorized["stretch_roles"],
        },
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print()
    print(f"High (80+): {output_data['summary']['high_probability']}")
    print(f"Sources: {', '.join(sources_used)}")
    print(f"Saved: {OUTPUT_FILE}")
    print("=" * 80)


if __name__ == "__main__":
    main()
