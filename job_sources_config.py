"""
Job portal sources configuration.
Edit SEARCH_ROLES, LOCATION, and source lists here.
"""

# Roles sent to every scraper (PM-focused; add more if needed)
SEARCH_ROLES = [
    "Product Manager",
    "Senior Product Manager",
    "Product Lead",
    "Associate Product Manager",
    "Group Product Manager",
]

LOCATION = "India"
LOCATION_CITIES = "Bangalore, Mumbai, Delhi NCR, Hyderabad, Pune, Chennai"

# Daily Job Pulse — 24+ platforms in one Apify actor
# https://apify.com/lenient_grove/daily-job-pulse-multi-source-job-opportunity-aggregator
DAILY_JOB_PULSE_ACTOR = "lenient_grove/daily-job-pulse-multi-source-job-opportunity-aggregator"

ALL_PULSE_SOURCES = [
    # Global
    "indeed",
    "glassdoor",
    "monster",
    "remoteok",
    "weworkremotely",
    "simplyhired",
    "ziprecruiter",
    "dice",
    "flexjobs",
    "stackoverflow",
    "github",
    "careerbuilder",
    "angellist",
    "toptal",
    "turing",
    "arc",
    # India
    "naukri",
    "shine",
    "timesjobs",
    "foundit",
    "instahyre",
    "hirist",
    "cutshort",
]

# Dedicated Apify actors (better coverage for these platforms)
DEDICATED_ACTORS = {
    "linkedin": "afanasenko/linkedin-jobs-scraper",
    "naukri": "automation-lab/naukri-scraper",
    "wellfound": "clearpath/wellfound-api-job-scraper",
    "internshala": "solidcode/internshala-scraper",
    "indeed": "mukeshrana90/indeed-jobs-scraper",
    "glassdoor": "orgupdate/glassdoor-jobs-scraper",
}

# When True: run aggregator + dedicated LinkedIn/Wellfound/Internshala
# When False: only dedicated actors (lower Apify cost)
USE_AGGREGATOR = True

# Skip dedicated Naukri if aggregator already includes naukri
SKIP_DEDICATED_WHEN_IN_PULSE = {"naukri", "indeed", "glassdoor"}

MAX_RESULTS_PER_SOURCE = 40
MAX_DAYS_OLD = 7
MIN_JOBS_TO_KEEP = 20
