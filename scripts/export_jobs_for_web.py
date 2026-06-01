#!/usr/bin/env python3
"""
Export scraper output to web/public/jobs.json for the hosted dashboard.
Reads: job_output.json (from scraper) or sample_output.json as fallback.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_PATHS = [
    ROOT / "web" / "public" / "jobs.json",
    ROOT / "web-static" / "jobs.json",
]
SOURCES = [ROOT / "job_output.json", ROOT / "sample_output.json"]


def normalize_job(raw: dict, idx: int) -> dict:
    posted = raw.get("posted_date", "")
    is_new = any(x in str(posted).lower() for x in ("1 day", "2 day", "today", "hour"))
    score = int(raw.get("fit_score", 0))
    return {
        "id": str(raw.get("id", idx)),
        "title": raw.get("title", "Product Manager"),
        "company": raw.get("company", "Unknown"),
        "location": raw.get("location", "India"),
        "salary": raw.get("salary", "Not disclosed"),
        "fitScore": score,
        "url": raw.get("url", "#"),
        "source": raw.get("source", ""),
        "isNew": is_new,
        "isHot": score >= 88,
    }


def flatten_jobs(data: dict) -> list:
    jobs = []
    bucket = data.get("jobs")
    if isinstance(bucket, dict):
        for key in ("high_probability", "medium_probability", "stretch_roles", "low_fit"):
            for j in bucket.get(key, []):
                jobs.append(j)
    elif isinstance(bucket, list):
        jobs = bucket
    return jobs


def main() -> int:
    source_path = None
    data = None
    for p in SOURCES:
        if p.exists():
            source_path = p
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            break

    if not data:
        print("No job_output.json or sample_output.json found.", file=sys.stderr)
        return 1

    raw_jobs = flatten_jobs(data)
    if len(raw_jobs) < 15:
        seed_path = ROOT / "web-static" / "jobs.json"
        if seed_path.exists():
            with open(seed_path, encoding="utf-8") as f:
                seed = json.load(f)
            raw_jobs = [
                {
                    "title": j["title"],
                    "company": j["company"],
                    "location": j["location"],
                    "salary": j["salary"],
                    "fit_score": j["fitScore"],
                    "url": j["url"],
                    "source": j.get("source", ""),
                    "posted_date": "1 day ago" if j.get("isNew") else "5 days ago",
                }
                for j in seed.get("jobs", [])
            ]
            print(f"Using {len(raw_jobs)} jobs from web-static/jobs.json seed", file=sys.stderr)
    if not raw_jobs:
        print("No jobs in source file.", file=sys.stderr)
        return 1

    raw_jobs.sort(key=lambda j: j.get("fit_score", 0), reverse=True)
    jobs = [normalize_job(j, i + 1) for i, j in enumerate(raw_jobs)]

    profile = data.get("profile", {"name": "Abhishek Kumar", "title": "Product Manager"})
    payload = {
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "jobs": jobs,
    }

    for out in OUT_PATHS:
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"Exported {len(jobs)} jobs -> {out} (from {source_path.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
