"""
AI-Powered Job Hunting System with Apify Integration
Scrapes jobs from LinkedIn, Naukri, Wellfound, and Internshala
Calculates fit scores based on resume profile
"""

import os
import json
import requests
from typing import List, Dict, Any
from datetime import datetime

# Apify API Configuration
APIFY_TOKEN = os.getenv('APIFY_TOKEN', 'YOUR_APIFY_TOKEN_HERE')
APIFY_API_BASE = 'https://api.apify.com/v2'

# Resume Profile (extracted from PDF)
PROFILE = {
    'name': 'Abhishek Kumar',
    'title': 'Product Manager',
    'experience_years': 5,
    'location': 'India',
    'domains': ['fintech', 'saas', 'edtech', 'lending', 'crm', 'lms', 'nbfc', 'collections'],
    'core_skills': [
        'product strategy', 'roadmapping', 'prd', 'user research', 'a/b testing',
        'funnel optimization', 'kpi', 'okr', 'uat', 'agile', 'scrum',
        'go-to-market', 'stakeholder management'
    ],
    'tech_skills': ['sql', 'python', 'power bi', 'google analytics', 'excel'],
    'ai_skills': ['llm', 'prompt engineering', 'n8n', 'chatgpt', 'claude'],
    'tools': ['jira', 'confluence', 'figma', 'notion', 'postman', 'git', 'salesforce'],
    'keywords': [
        'product manager', 'pm', 'fintech', 'lending', 'collections', 'crm',
        'saas', 'enterprise', 'b2b', '0 to 1', 'digital product', 'gold loan',
        'credit', 'kyc', 'workflow', 'automation'
    ]
}

# Apify Actor IDs
ACTORS = {
    'linkedin': 'afanasenko/linkedin-jobs-scraper',
    'naukri': 'automation-lab/naukri-scraper',
    'wellfound': 'clearpath/wellfound-api-job-scraper',
    'internshala': 'solidcode/internshala-scraper',
}


def run_apify_actor(actor_id: str, input_data: Dict[str, Any], timeout: int = 300) -> List[Dict]:
    """
    Run an Apify actor and return results
    
    Args:
        actor_id: Apify actor ID (e.g., 'automation-lab/naukri-scraper')
        input_data: Input parameters for the actor
        timeout: Maximum wait time in seconds
    
    Returns:
        List of job listings
    """
    headers = {'Authorization': f'Bearer {APIFY_TOKEN}'}
    
    # Start actor run
    run_url = f'{APIFY_API_BASE}/acts/{actor_id}/run-sync-get-dataset-items'
    params = {'token': APIFY_TOKEN, 'timeout': timeout}
    
    print(f"🚀 Running Apify actor: {actor_id}")
    print(f"📥 Input: {json.dumps(input_data, indent=2)}")
    
    try:
        response = requests.post(
            run_url,
            json=input_data,
            params=params,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        
        results = response.json()
        print(f"✅ Retrieved {len(results)} jobs from {actor_id}")
        return results
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error running actor {actor_id}: {e}")
        return []


def scrape_linkedin_jobs() -> List[Dict]:
    """Scrape jobs from LinkedIn using Apify"""
    input_data = {
        'keywords': 'product manager',
        'location': 'India',
        'datePosted': 'pastWeek',
        'experienceLevel': ['midSenior', 'director'],
        'maxResults': 50,
        'scrapeJobDetails': True,
    }
    
    jobs = run_apify_actor(ACTORS['linkedin'], input_data)
    
    # Normalize format
    normalized = []
    for job in jobs:
        normalized.append({
            'source': 'LinkedIn',
            'title': job.get('title', ''),
            'company': job.get('company', ''),
            'location': job.get('location', ''),
            'salary': job.get('salary', 'Not specified'),
            'experience': job.get('seniority', ''),
            'description': job.get('description', ''),
            'skills': job.get('skills', []),
            'url': job.get('url', ''),
            'posted_date': job.get('postedDate', ''),
            'raw': job
        })
    
    return normalized


def scrape_naukri_jobs() -> List[Dict]:
    """Scrape jobs from Naukri.com using Apify"""
    input_data = {
        'keyword': 'product manager',
        'location': 'Bangalore, Mumbai, Delhi, Hyderabad, Pune',
        'experienceMin': 4,
        'experienceMax': 8,
        'sortBy': 'relevance',
        'workType': '',  # All: office, remote, hybrid
        'maxJobs': 50,
        'includeDescriptions': True,
    }
    
    jobs = run_apify_actor(ACTORS['naukri'], input_data)
    
    # Normalize format
    normalized = []
    for job in jobs:
        normalized.append({
            'source': 'Naukri',
            'title': job.get('title', ''),
            'company': job.get('company', ''),
            'location': job.get('location', ''),
            'salary': job.get('salary', 'Not specified'),
            'experience': job.get('experience', ''),
            'description': job.get('description', ''),
            'skills': job.get('skills', []) if isinstance(job.get('skills'), list) else [],
            'url': job.get('url', ''),
            'posted_date': job.get('postedAt', ''),
            'raw': job
        })
    
    return normalized


def scrape_wellfound_jobs() -> List[Dict]:
    """Scrape startup jobs from Wellfound (AngelList) using Apify"""
    input_data = {
        'urls': [
            'https://wellfound.com/role/r/product-manager',
            'https://wellfound.com/role/l/product-manager/india',
        ],
        'maxResults': 50,
        'onlyRemoteJobs': False,
    }
    
    jobs = run_apify_actor(ACTORS['wellfound'], input_data)
    
    # Normalize format
    normalized = []
    for job in jobs:
        normalized.append({
            'source': 'Wellfound',
            'title': job.get('title', ''),
            'company': job.get('company', ''),
            'location': job.get('location', 'Remote/India'),
            'salary': f"₹{job.get('salaryMin', 0)/100000:.0f}-{job.get('salaryMax', 0)/100000:.0f} LPA" if job.get('salaryMin') else 'Not specified',
            'experience': job.get('experience', ''),
            'description': job.get('description', ''),
            'skills': job.get('skills', []),
            'url': job.get('url', ''),
            'posted_date': job.get('postedDate', ''),
            'raw': job
        })
    
    return normalized


def scrape_internshala_jobs() -> List[Dict]:
    """Scrape internships/jobs from Internshala using Apify"""
    input_data = {
        'listingType': 'jobs',  # 'internships' or 'jobs'
        'category': 'product-management',
        'location': 'bangalore, mumbai, delhi, hyderabad, pune',
        'workFromHome': False,
        'maxListings': 30,
        'scrapeDetails': True,
    }
    
    jobs = run_apify_actor(ACTORS['internshala'], input_data)
    
    # Normalize format
    normalized = []
    for job in jobs:
        normalized.append({
            'source': 'Internshala',
            'title': job.get('title', ''),
            'company': job.get('company', ''),
            'location': job.get('location', ''),
            'salary': job.get('salary', 'Not specified'),
            'experience': job.get('duration', ''),
            'description': job.get('fullDescription', job.get('description', '')),
            'skills': job.get('skills', []),
            'url': job.get('url', ''),
            'posted_date': job.get('postedAt', ''),
            'raw': job
        })
    
    return normalized


def calculate_fit_score(job: Dict[str, Any]) -> int:
    """
    Calculate fit score (0-100) based on resume match
    
    Scoring criteria:
    - Domain match: 30 points
    - Skills match: 30 points
    - Experience match: 20 points
    - Location match: 10 points
    - Keywords in job description: 10 points
    """
    score = 0
    
    job_text = f"{job['title']} {job['company']} {job['description']}".lower()
    skills_text = ' '.join(job.get('skills', [])).lower()
    
    # Domain match (30 points)
    domain_matches = sum(1 for domain in PROFILE['domains'] if domain in job_text)
    score += min(domain_matches * 5, 30)
    
    # Skills match (30 points)
    all_profile_skills = (
        PROFILE['core_skills'] + 
        PROFILE['tech_skills'] + 
        PROFILE['ai_skills'] + 
        PROFILE['tools']
    )
    skill_matches = sum(1 for skill in all_profile_skills if skill in job_text or skill in skills_text)
    score += min(skill_matches * 2, 30)
    
    # Experience match (20 points)
    exp_text = job.get('experience', '').lower()
    if any(term in exp_text for term in ['5', '4-6', '5-7', '4-7', 'senior', 'mid']):
        score += 20
    elif any(term in exp_text for term in ['3-5', '4', '6']):
        score += 15
    
    # Location match (10 points)
    location = job.get('location', '').lower()
    if 'india' in location or any(city in location for city in ['bangalore', 'mumbai', 'delhi', 'pune', 'hyderabad', 'chennai']):
        score += 10
    
    # Keywords match (10 points)
    keyword_matches = sum(1 for keyword in PROFILE['keywords'] if keyword in job_text)
    score += min(keyword_matches, 10)
    
    return min(score, 100)  # Cap at 100


def categorize_jobs(jobs: List[Dict]) -> Dict[str, List[Dict]]:
    """Categorize jobs by fit score into high/medium/stretch"""
    categorized = {
        'high_probability': [],  # 80+
        'medium_probability': [],  # 65-79
        'stretch_roles': [],  # 50-64
        'low_fit': []  # < 50
    }
    
    for job in jobs:
        score = job['fit_score']
        
        if score >= 80:
            categorized['high_probability'].append(job)
        elif score >= 65:
            categorized['medium_probability'].append(job)
        elif score >= 50:
            categorized['stretch_roles'].append(job)
        else:
            categorized['low_fit'].append(job)
    
    return categorized


def main():
    """Main execution function"""
    print("=" * 80)
    print("🤖 AI-Powered Job Hunting Machine")
    print(f"👤 Profile: {PROFILE['name']} - {PROFILE['title']}")
    print("=" * 80)
    print()
    
    # Check Apify token
    if APIFY_TOKEN == 'YOUR_APIFY_TOKEN_HERE':
        print("⚠️  WARNING: APIFY_TOKEN not set!")
        print("Get your token at: https://console.apify.com/settings/integrations")
        print("Set it as environment variable: export APIFY_TOKEN='your_token'")
        print()
        return
    
    all_jobs = []
    
    # Scrape from all sources
    print("📡 Scraping job listings from multiple sources...")
    print()
    
    try:
        linkedin_jobs = scrape_linkedin_jobs()
        all_jobs.extend(linkedin_jobs)
        print(f"✅ LinkedIn: {len(linkedin_jobs)} jobs")
    except Exception as e:
        print(f"❌ LinkedIn failed: {e}")
    
    try:
        naukri_jobs = scrape_naukri_jobs()
        all_jobs.extend(naukri_jobs)
        print(f"✅ Naukri: {len(naukri_jobs)} jobs")
    except Exception as e:
        print(f"❌ Naukri failed: {e}")
    
    try:
        wellfound_jobs = scrape_wellfound_jobs()
        all_jobs.extend(wellfound_jobs)
        print(f"✅ Wellfound: {len(wellfound_jobs)} jobs")
    except Exception as e:
        print(f"❌ Wellfound failed: {e}")
    
    try:
        internshala_jobs = scrape_internshala_jobs()
        all_jobs.extend(internshala_jobs)
        print(f"✅ Internshala: {len(internshala_jobs)} jobs")
    except Exception as e:
        print(f"❌ Internshala failed: {e}")
    
    print()
    print(f"📊 Total jobs scraped: {len(all_jobs)}")
    print()
    
    if not all_jobs:
        print("❌ No jobs found. Check your Apify token and try again.")
        return
    
    # Calculate fit scores
    print("🧮 Calculating fit scores...")
    for job in all_jobs:
        job['fit_score'] = calculate_fit_score(job)
    
    # Sort by fit score
    all_jobs.sort(key=lambda x: x['fit_score'], reverse=True)
    
    # Categorize
    categorized = categorize_jobs(all_jobs)
    
    # Print summary
    print()
    print("=" * 80)
    print("📈 JOB MATCH SUMMARY")
    print("=" * 80)
    print(f"🎯 High Probability (80+):     {len(categorized['high_probability'])} jobs")
    print(f"💼 Medium Probability (65-79): {len(categorized['medium_probability'])} jobs")
    print(f"🚀 Stretch Roles (50-64):      {len(categorized['stretch_roles'])} jobs")
    print(f"⚪ Low Fit (<50):               {len(categorized['low_fit'])} jobs")
    print("=" * 80)
    print()
    
    # Show top 5 high probability matches
    print("🏆 TOP 5 HIGH PROBABILITY MATCHES:")
    print()
    for i, job in enumerate(categorized['high_probability'][:5], 1):
        print(f"{i}. [{job['fit_score']}] {job['title']}")
        print(f"   🏢 {job['company']} | 📍 {job['location']}")
        print(f"   💰 {job['salary']} | 📱 Source: {job['source']}")
        print(f"   🔗 {job['url']}")
        print()
    
    # Save results to JSON
    output_file = f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_data = {
        'profile': PROFILE,
        'scrape_timestamp': datetime.now().isoformat(),
        'total_jobs': len(all_jobs),
        'summary': {
            'high_probability': len(categorized['high_probability']),
            'medium_probability': len(categorized['medium_probability']),
            'stretch_roles': len(categorized['stretch_roles']),
            'low_fit': len(categorized['low_fit']),
        },
        'jobs': {
            'high_probability': categorized['high_probability'],
            'medium_probability': categorized['medium_probability'],
            'stretch_roles': categorized['stretch_roles'],
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Results saved to: {output_file}")
    print()
    print("✅ Job scraping complete!")
    print()
    print("📊 Next steps:")
    print("1. Review the high probability matches")
    print("2. Customize your applications for top roles")
    print("3. Track applications in the interactive dashboard")
    print("4. Set up daily/weekly automation with this script")


if __name__ == '__main__':
    main()
