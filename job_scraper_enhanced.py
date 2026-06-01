"""
Job scraper entry point.
Default: FREE open-source (JobSpy) — no Apify credits.
Set SCRAPER_BACKEND=apify in .env to use Apify (paid).
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

SCRAPER_BACKEND = os.getenv("SCRAPER_BACKEND", "free").strip().lower()


def run():
    if SCRAPER_BACKEND == "apify":
        from job_scraper_apify import APIFY_TOKEN, main as apify_main

        if not APIFY_TOKEN or APIFY_TOKEN == "YOUR_APIFY_TOKEN_HERE":
            print("SCRAPER_BACKEND=apify but APIFY_TOKEN is missing.")
            print("Set APIFY_TOKEN in .env or use SCRAPER_BACKEND=free (default).")
            sys.exit(1)
        apify_main()
    else:
        from job_scraper_free import main as free_main

        free_main()


if __name__ == "__main__":
    run()
