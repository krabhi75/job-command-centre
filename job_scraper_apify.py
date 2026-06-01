"""
AI-Powered Job Hunting System — multi-source Apify scraping.
Aggregates 24+ portals via Daily Job Pulse + dedicated LinkedIn / Wellfound / Internshala scrapers.
"""

import os
import json
import re
import requests
from typing import List, Dict, Any, Callable, Optional
from datetime import datetime

from job_sources_config import (
    SEARCH_ROLES,
    LOCATION,
    LOCATION_CITIES,
    DAILY_JOB_PULSE_ACTOR,
    ALL_PULSE_SOURCES,
    DEDICATED_ACTORS,
    USE_AGGREGATOR,
    SKIP_DEDICATED_WHEN_IN_PULSE,
    MAX_RESULTS_PER_SOURCE,
    MAX_DAYS_OLD,
)

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "YOUR_APIFY_TOKEN_HERE")
APIFY_API_BASE = "https://api.apify.com/v2"
OUTPUT_FILE = "job_output.json"

PROFILE = {
    "name": "Abhishek Kumar",
    "title": "Product Manager",
    "experience_years": 5,
    "location": "India",
    "domains": ["fintech", "saas", "edtech", "lending", "crm", "lms", "nbfc", "collections"],
    "core_skills": [
        "product strategy", "roadmapping", "prd", "user research", "a/b testing",
        "funnel optimization", "kpi", "okr", "uat", "agile", "scrum",
        "go-to-market", "stakeholder management",
    ],
    "tech_skills": ["sql", "python", "power bi", "google analytics", "excel"],
    "ai_skills": ["llm", "prompt engineering", "n8n", "chatgpt", "claude"],
    "tools": ["jira", "confluence", "figma", "notion", "postman", "git", "salesforce"],
    "keywords": [
        "product manager", "pm", "fintech", "lending", "collections", "crm",
        "saas", "enterprise", "b2b", "0 to 1", "digital product", "gold loan",
        "credit", "kyc", "workflow", "automation",
    ],
}


def run_apify_actor(actor_id: str, input_data: Dict[str, Any], timeout: int = 600) -> List[Dict]:
    if not APIFY_TOKEN or APIFY_TOKEN == "YOUR_APIFY_TOKEN_HERE":
        return []

    run_url = f"{APIFY_API_BASE}/acts/{actor_id}/run-sync-get-dataset-items"
    params = {"token": APIFY_TOKEN, "timeout": timeout}

    print(f"Running Apify actor: {actor_id}")
    try:
        response = requests.post(
            run_url,
            json=input_data,
            params=params,
            headers={"Authorization": f"Bearer {APIFY_TOKEN}"},
            timeout=timeout + 30,
        )
        response.raise_for_status()
        results = response.json()
        print(f"  Retrieved {len(results)} items from {actor_id}")
        return results if isinstance(results, list) else []
    except requests.exceptions.RequestException as e:
        print(f"  Error running {actor_id}: {e}")
        return []


def base_job(
    source: str,
    title: str,
    company: str,
    location: str,
    salary: str,
    url: str,
    description: str = "",
    skills: Optional[List] = None,
    experience: str = "",
    posted_date: str = "",
) -> Dict[str, Any]:
    return {
        "source": source,
        "title": title or "Product Manager",
        "company": company or "Unknown",
        "location": location or LOCATION,
        "salary": salary or "Not disclosed",
        "experience": experience,
        "description": description,
        "skills": skills or [],
        "url": url or "#",
        "posted_date": posted_date,
    }


def normalize_from_pulse(item: Dict) -> Dict[str, Any]:
    title = item.get("jobTitle") or item.get("title") or item.get("job_title") or ""
    company = item.get("company") or item.get("companyName") or ""
    location = item.get("location") or item.get("jobLocation") or LOCATION
    url = item.get("applyLink") or item.get("jobUrl") or item.get("url") or "#"
    source = item.get("source") or item.get("platform") or "Aggregator"
    if isinstance(source, str):
        source = source.replace("_", " ").title()
    return base_job(
        source=str(source),
        title=title,
        company=company,
        location=location,
        salary=item.get("salary") or item.get("salaryRange") or "Not disclosed",
        url=url,
        description=item.get("description") or item.get("jobDescription") or "",
        posted_date=item.get("postedDate") or item.get("posted_date") or "",
    )


def scrape_daily_job_pulse() -> List[Dict]:
    """24+ platforms: Naukri, Shine, TimesJobs, Foundit, Instahyre, Hirist, CutShort, Indeed, Glassdoor, etc."""
    input_data = {
        "roles": SEARCH_ROLES,
        "location": LOCATION,
        "sources": ALL_PULSE_SOURCES,
        "maxResultsPerSource": MAX_RESULTS_PER_SOURCE,
        "maxDaysOld": MAX_DAYS_OLD,
    }
    raw = run_apify_actor(DAILY_JOB_PULSE_ACTOR, input_data, timeout=900)
    return [normalize_from_pulse(j) for j in raw if normalize_from_pulse(j).get("title")]


def scrape_linkedin_jobs() -> List[Dict]:
    jobs = run_apify_actor(
        DEDICATED_ACTORS["linkedin"],
        {
            "keywords": " OR ".join(SEARCH_ROLES[:3]),
            "location": LOCATION,
            "datePosted": "pastWeek",
            "experienceLevel": ["midSenior", "director"],
            "maxResults": MAX_RESULTS_PER_SOURCE,
            "scrapeJobDetails": True,
        },
    )
    out = []
    for job in jobs:
        out.append(
            base_job(
                "LinkedIn",
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                job.get("salary", "Not disclosed"),
                job.get("url", ""),
                job.get("description", ""),
                job.get("skills", []) if isinstance(job.get("skills"), list) else [],
                job.get("seniority", ""),
                job.get("postedDate", ""),
            )
        )
    return out


def scrape_naukri_jobs() -> List[Dict]:
    jobs = run_apify_actor(
        DEDICATED_ACTORS["naukri"],
        {
            "keyword": "product manager",
            "location": LOCATION_CITIES,
            "experienceMin": 3,
            "experienceMax": 10,
            "sortBy": "relevance",
            "maxJobs": MAX_RESULTS_PER_SOURCE,
            "includeDescriptions": True,
        },
    )
    out = []
    for job in jobs:
        skills = job.get("skills", [])
        if not isinstance(skills, list):
            skills = []
        out.append(
            base_job(
                "Naukri",
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                job.get("salary", "Not disclosed"),
                job.get("url", ""),
                job.get("description", ""),
                skills,
                job.get("experience", ""),
                job.get("postedAt", ""),
            )
        )
    return out


def scrape_wellfound_jobs() -> List[Dict]:
    jobs = run_apify_actor(
        DEDICATED_ACTORS["wellfound"],
        {
            "urls": [
                "https://wellfound.com/role/r/product-manager",
                "https://wellfound.com/role/l/product-manager/india",
            ],
            "maxResults": MAX_RESULTS_PER_SOURCE,
            "onlyRemoteJobs": False,
        },
    )
    out = []
    for job in jobs:
        sal = "Not disclosed"
        if job.get("salaryMin"):
            sal = f"₹{job.get('salaryMin', 0) / 100000:.0f}-{job.get('salaryMax', 0) / 100000:.0f} LPA"
        out.append(
            base_job(
                "Wellfound",
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", "India"),
                sal,
                job.get("url", ""),
                job.get("description", ""),
                job.get("skills", []) if isinstance(job.get("skills"), list) else [],
                job.get("experience", ""),
                job.get("postedDate", ""),
            )
        )
    return out


def scrape_internshala_jobs() -> List[Dict]:
    jobs = run_apify_actor(
        DEDICATED_ACTORS["internshala"],
        {
            "listingType": "jobs",
            "category": "product-management",
            "location": "bangalore, mumbai, delhi, hyderabad, pune",
            "workFromHome": False,
            "maxListings": min(MAX_RESULTS_PER_SOURCE, 40),
            "scrapeDetails": True,
        },
    )
    out = []
    for job in jobs:
        out.append(
            base_job(
                "Internshala",
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                job.get("salary", "Not disclosed"),
                job.get("url", ""),
                job.get("fullDescription", job.get("description", "")),
                job.get("skills", []) if isinstance(job.get("skills"), list) else [],
                job.get("duration", ""),
                job.get("postedAt", ""),
            )
        )
    return out


def scrape_indeed_jobs() -> List[Dict]:
    jobs = run_apify_actor(
        DEDICATED_ACTORS["indeed"],
        {
            "query": "product manager",
            "country": "in",
            "location": LOCATION_CITIES.split(",")[0].strip(),
            "maxResults": MAX_RESULTS_PER_SOURCE,
        },
        timeout=600,
    )
    out = []
    for job in jobs:
        out.append(
            base_job(
                "Indeed",
                job.get("title") or job.get("jobTitle", ""),
                job.get("company") or job.get("companyName", ""),
                job.get("location") or job.get("jobLocation", ""),
                job.get("salary") or job.get("formattedSalary", "Not disclosed"),
                job.get("url") or job.get("jobUrl", ""),
                job.get("description") or job.get("jobDescription", ""),
                posted_date=job.get("postedAt") or job.get("datePosted", ""),
            )
        )
    return out


def scrape_glassdoor_jobs() -> List[Dict]:
    jobs = run_apify_actor(
        DEDICATED_ACTORS["glassdoor"],
        {
            "includeKeyword": "product manager",
            "locationName": "India",
            "countryName": "india",
            "datePosted": "week",
            "pagesToFetch": 3,
        },
        timeout=600,
    )
    out = []
    for job in jobs:
        out.append(
            base_job(
                "Glassdoor",
                job.get("title") or job.get("jobTitle", ""),
                job.get("company") or job.get("companyName", ""),
                job.get("location") or job.get("locationName", ""),
                job.get("salary") or "Not disclosed",
                job.get("jobURL") or job.get("url", ""),
                job.get("description", ""),
                posted_date=job.get("datePosted", ""),
            )
        )
    return out


def dedupe_jobs(jobs: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []
    for job in jobs:
        url = (job.get("url") or "").strip().lower().split("?")[0].rstrip("/")
        if url and url not in ("#", ""):
            key = url
        else:
            title = re.sub(r"\s+", " ", (job.get("title") or "").lower().strip())
            company = re.sub(r"\s+", " ", (job.get("company") or "").lower().strip())
            key = f"{title}|{company}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(job)
    return unique


def run_scraper(name: str, fn: Callable[[], List[Dict]]) -> List[Dict]:
    try:
        jobs = fn()
        print(f"  {name}: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"  {name} failed: {e}")
        return []


def calculate_fit_score(job: Dict[str, Any]) -> int:
    score = 0
    job_text = f"{job['title']} {job['company']} {job['description']}".lower()
    skills_text = " ".join(job.get("skills", [])).lower()

    domain_matches = sum(1 for domain in PROFILE["domains"] if domain in job_text)
    score += min(domain_matches * 5, 30)

    all_profile_skills = (
        PROFILE["core_skills"] + PROFILE["tech_skills"] + PROFILE["ai_skills"] + PROFILE["tools"]
    )
    skill_matches = sum(1 for skill in all_profile_skills if skill in job_text or skill in skills_text)
    score += min(skill_matches * 2, 30)

    exp_text = job.get("experience", "").lower()
    if any(term in exp_text for term in ["5", "4-6", "5-7", "4-7", "senior", "mid"]):
        score += 20
    elif any(term in exp_text for term in ["3-5", "4", "6"]):
        score += 15

    location = job.get("location", "").lower()
    if "india" in location or any(
        c in location for c in ["bangalore", "mumbai", "delhi", "pune", "hyderabad", "chennai", "gurgaon", "noida"]
    ):
        score += 10

    keyword_matches = sum(1 for keyword in PROFILE["keywords"] if keyword in job_text)
    score += min(keyword_matches, 10)

    return min(score, 100)


def categorize_jobs(jobs: List[Dict]) -> Dict[str, List[Dict]]:
    categorized = {
        "high_probability": [],
        "medium_probability": [],
        "stretch_roles": [],
        "low_fit": [],
    }
    for job in jobs:
        score = job["fit_score"]
        if score >= 80:
            categorized["high_probability"].append(job)
        elif score >= 65:
            categorized["medium_probability"].append(job)
        elif score >= 50:
            categorized["stretch_roles"].append(job)
        else:
            categorized["low_fit"].append(job)
    return categorized


def collect_all_jobs() -> List[Dict]:
    all_jobs: List[Dict] = []
    print("Scraping from all configured sources...")
    print()

    if USE_AGGREGATOR:
        print("Multi-source aggregator (24+ portals):")
        all_jobs.extend(run_scraper("Daily Job Pulse", scrape_daily_job_pulse))
        print()

    print("Dedicated scrapers:")
    dedicated = [
        ("LinkedIn", scrape_linkedin_jobs),
        ("Wellfound", scrape_wellfound_jobs),
        ("Internshala", scrape_internshala_jobs),
    ]
    if not USE_AGGREGATOR or "naukri" not in SKIP_DEDICATED_WHEN_IN_PULSE:
        dedicated.insert(0, ("Naukri", scrape_naukri_jobs))
    if not USE_AGGREGATOR or "indeed" not in SKIP_DEDICATED_WHEN_IN_PULSE:
        dedicated.append(("Indeed", scrape_indeed_jobs))
    if not USE_AGGREGATOR or "glassdoor" not in SKIP_DEDICATED_WHEN_IN_PULSE:
        dedicated.append(("Glassdoor", scrape_glassdoor_jobs))

    for name, fn in dedicated:
        all_jobs.extend(run_scraper(name, fn))

    before = len(all_jobs)
    all_jobs = dedupe_jobs(all_jobs)
    print()
    print(f"Total raw: {before} -> after dedupe: {len(all_jobs)}")
    return all_jobs


def main():
    print("=" * 80)
    print("AI Job Command Centre — multi-source scrape")
    print(f"Profile: {PROFILE['name']} — {PROFILE['title']}")
    print("=" * 80)
    print()

    if APIFY_TOKEN == "YOUR_APIFY_TOKEN_HERE":
        print("APIFY_TOKEN not set. Add it to .env or GitHub Secrets.")
        return

    all_jobs = collect_all_jobs()
    if not all_jobs:
        print("No jobs found. Check Apify token balance and actor availability.")
        return

    for job in all_jobs:
        job["fit_score"] = calculate_fit_score(job)

    all_jobs.sort(key=lambda x: x["fit_score"], reverse=True)
    categorized = categorize_jobs(all_jobs)

    sources_used = sorted({j["source"] for j in all_jobs})

    output_data = {
        "profile": PROFILE,
        "scrape_timestamp": datetime.now().isoformat(),
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
    print("=" * 80)
    print(f"High (80+): {output_data['summary']['high_probability']}")
    print(f"Medium (65-79): {output_data['summary']['medium_probability']}")
    print(f"Stretch (50-64): {output_data['summary']['stretch_roles']}")
    print(f"Sources: {', '.join(sources_used)}")
    print(f"Saved: {OUTPUT_FILE}")
    print("=" * 80)


if __name__ == "__main__":
    main()
