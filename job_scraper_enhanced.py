"""
Enhanced Job Scraper with Environment Variables Support
Load Apify token from .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now the job_scraper_apify.py will automatically read APIFY_TOKEN from .env
# Usage:
# 1. Copy .env.example to .env
# 2. Add your Apify token to .env
# 3. Run: python job_scraper_enhanced.py

from job_scraper_apify import *

if __name__ == '__main__':
    if not APIFY_TOKEN or APIFY_TOKEN == 'YOUR_APIFY_TOKEN_HERE':
        print("=" * 80)
        print("⚠️  APIFY_TOKEN not configured!")
        print("=" * 80)
        print()
        print("Setup Instructions:")
        print("1. Copy .env.example to .env:")
        print("   cp .env.example .env")
        print()
        print("2. Get your Apify token:")
        print("   https://console.apify.com/settings/integrations")
        print()
        print("3. Add token to .env file:")
        print("   APIFY_TOKEN=your_actual_token_here")
        print()
        print("4. Run this script again:")
        print("   python job_scraper_enhanced.py")
        print()
        print("=" * 80)
    else:
        main()
