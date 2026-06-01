# 🤖 AI-Powered Job Hunting System

A comprehensive job hunting command center that scrapes real job listings from LinkedIn, Naukri, Wellfound, and Internshala using Apify, then matches them to your profile with an intelligent scoring algorithm.

## 🎯 Features

### ✨ Interactive Dashboard
- **Daily Job Alert Panel** with check-in streak tracking
- **Smart Categorization** (High/Medium/Stretch roles based on fit score)
- **Visual Indicators** for new jobs, hot opportunities, and closing deadlines
- **Filterable Views** by company type, location, and application status
- **Live Application Links** for one-click job applications

### 🔍 Intelligent Matching
- **AI-Powered Fit Scoring** (0-100) based on:
  - Domain expertise match (30%)
  - Skills alignment (30%)
  - Experience level (20%)
  - Location preference (10%)
  - Keyword relevance (10%)

### 🕷️ Multi-Platform Job Scraping
- **LinkedIn** - Professional network jobs
- **Naukri.com** - India's largest job portal
- **Wellfound** - Startup and scaleup roles
- **Internshala** - Entry-level and internships
- **Company Career Pages** (expandable)

---

## 📊 Your Profile Summary

**Name:** Abhishek Kumar  
**Role:** Product Manager  
**Experience:** 5+ years  
**Location:** India

**Domain Expertise:**
- Fintech (NBFC, Lending, Gold Loans, Collections)
- Enterprise SaaS (CRM, LMS)
- EdTech

**Core PM Skills:**
- Product Strategy, Roadmapping, PRD, A/B Testing
- Go-To-Market, Stakeholder Management
- Agile, Scrum, UAT

**Technical Skills:**
- SQL, Python, Power BI, Google Analytics, Excel

**AI & Automation:**
- LLM Applications, Prompt Engineering, n8n

**Key Achievements:**
- ₹118 Cr+ revenue contribution
- 50% TAT reduction on Gold Loan product
- Built 0→1 Collections CRM (18% recovery improvement)

---

## 🚀 Quick Start

### 1. View the Interactive Dashboard

Open the canvas dashboard in Cursor:

```
/home/abhishek/.cursor/projects/empty-window/canvases/job-tracker-dashboard.canvas.tsx
```

The dashboard contains **22 curated demo jobs** matching your profile, categorized by fit score:
- **8 High Probability** (80+) - Strong matches to your fintech/SaaS background
- **9 Medium Probability** (65-79) - Good fits with some skill development needed
- **5 Stretch Roles** (50-64) - Career growth opportunities

### 2. Get Live Job Data with Apify

#### Step 1: Get Apify API Token
1. Sign up at [Apify](https://apify.com/)
2. Go to [Settings → Integrations](https://console.apify.com/settings/integrations)
3. Copy your API token

#### Step 2: Install Dependencies
```bash
pip install requests
```

#### Step 3: Set Up Environment
```bash
export APIFY_TOKEN='your_apify_token_here'
```

Or add to your `.bashrc` / `.zshrc`:
```bash
echo 'export APIFY_TOKEN="your_token"' >> ~/.bashrc
source ~/.bashrc
```

#### Step 4: Run the Job Scraper
```bash
python job_scraper_apify.py
```

This will:
- ✅ Scrape 50+ jobs from each platform (200+ total)
- ✅ Calculate fit scores for each job
- ✅ Categorize into High/Medium/Stretch roles
- ✅ Save results to `jobs_YYYYMMDD_HHMMSS.json`
- ✅ Display top 5 matches

---

## 📋 Apify Actors Used

### 1. LinkedIn Jobs Scraper
**Actor:** `afanasenko/linkedin-jobs-scraper`  
**Capabilities:**
- Search by keyword, location, experience level
- Filter by job type, posting date
- Extract full job descriptions, skills, salary
- No LinkedIn account required

**Example Search:**
```json
{
  "keywords": "product manager",
  "location": "India",
  "datePosted": "pastWeek",
  "experienceLevel": ["midSenior", "director"],
  "maxResults": 50
}
```

### 2. Naukri.com Scraper
**Actor:** `automation-lab/naukri-scraper`  
**Capabilities:**
- India's largest job portal (500K+ listings)
- Filter by experience, salary, work type (remote/hybrid/office)
- Structured salary data, skills arrays
- Company ratings from AmbitionBox

**Example Search:**
```json
{
  "keyword": "product manager",
  "location": "Bangalore, Mumbai, Delhi",
  "experienceMin": 4,
  "experienceMax": 8,
  "maxJobs": 50
}
```

### 3. Wellfound (AngelList) Scraper
**Actor:** `clearpath/wellfound-api-job-scraper`  
**Capabilities:**
- Startup jobs with equity information
- Funding stage, team size, tech stack
- Remote-first opportunities
- Salary and equity ranges

**Example Search:**
```json
{
  "urls": [
    "https://wellfound.com/role/r/product-manager",
    "https://wellfound.com/role/l/product-manager/india"
  ],
  "maxResults": 50
}
```

### 4. Internshala Scraper
**Actor:** `solidcode/internshala-scraper`  
**Capabilities:**
- Internships and entry-level jobs
- Work-from-home filters
- Stipend/salary data
- Full job descriptions

**Example Search:**
```json
{
  "listingType": "jobs",
  "category": "product-management",
  "location": "bangalore, mumbai",
  "maxListings": 30
}
```

---

## 🎯 Fit Score Algorithm

The system calculates a **0-100 fit score** for each job:

### Scoring Breakdown:

| Criteria | Weight | Calculation |
|----------|--------|-------------|
| **Domain Match** | 30% | Checks for: fintech, saas, edtech, lending, crm, collections, nbfc |
| **Skills Match** | 30% | Matches against 20+ skills in your profile |
| **Experience Level** | 20% | Looks for 4-7 years, senior, mid-level mentions |
| **Location** | 10% | India, Bangalore, Mumbai, Delhi, Hyderabad, Pune, Chennai |
| **Keywords** | 10% | Product manager, PM, 0-1, digital product, workflow, etc. |

### Score Categories:

- **🎯 High Probability (80-100):** Direct skill and domain match
- **💼 Medium Probability (65-79):** Good fit, some upskilling needed
- **🚀 Stretch Roles (50-64):** Career pivot opportunities
- **⚪ Low Fit (<50):** Filtered out

---

## 📈 Dashboard Features

### 1. Daily Job Alert Panel
- **Check-in Streak** - Gamified daily tracking
- **New Jobs Counter** - Shows jobs posted since last visit
- **Hot Opportunities** - High-match + actively hiring
- **Closing Soon** - Urgent applications (<48 hours)

### 2. Job Cards
Each job displays:
- Title, company, location, salary
- Fit score with visual indicator
- Skills badges
- Source platform
- Application status
- Quick apply button

### 3. Filtering & Views
- **By Category:** High/Medium/Stretch
- **By Company Type:** Startup, Scaleup, MNC, Consulting
- **By Location:** City-based filtering
- **Table View:** Sortable data table with all jobs

### 4. Profile Summary
Shows your matched criteria:
- Domain expertise
- Core PM skills
- Technical skills
- Key achievements

---

## 🔄 Automation Setup

### Daily Job Alerts (Cron)

Add to crontab (`crontab -e`):
```bash
# Run job scraper every day at 9 AM
0 9 * * * cd /path/to/project && /usr/bin/python3 job_scraper_apify.py
```

### Weekly Deep Scan

```bash
# Run comprehensive search every Monday at 8 AM
0 8 * * 1 cd /path/to/project && /usr/bin/python3 job_scraper_apify.py --deep-scan
```

### Real-time Notifications

Extend the script to send notifications:
```python
# Add to job_scraper_apify.py
def send_notification(high_priority_jobs):
    # Email via SMTP
    # Slack webhook
    # Telegram bot
    pass
```

---

## 💡 Usage Tips

### 1. Optimize Your Search
Edit `PROFILE` in `job_scraper_apify.py` to fine-tune matching:
```python
PROFILE = {
    'domains': ['fintech', 'saas'],  # Add/remove domains
    'keywords': ['product manager', 'pm'],  # Customize keywords
    'experience_years': 5,  # Adjust experience level
}
```

### 2. Expand Job Sources
Add more Apify actors:
```python
ACTORS = {
    'indeed': 'curious_coder/indeed-scraper',
    'glassdoor': 'your-actor/glassdoor-scraper',
}
```

### 3. Track Applications
Add status tracking to the JSON:
```json
{
  "job_id": "jb001",
  "application_status": "applied",
  "applied_date": "2024-06-01",
  "follow_up_date": "2024-06-08"
}
```

### 4. Customize Dashboard
Edit `job-tracker-dashboard.canvas.tsx`:
- Change color scheme
- Add more filters
- Create new visualizations
- Add notes/reminders

---

## 📊 Expected Results

Based on your profile, you should see:

### High Probability Matches (80+)
- **Senior PM - Fintech:** Razorpay, Cred, Paytm, PhonePe
- **PM - Lending:** MoneyTap, Lendingkart, credit platforms
- **PM - Collections:** Fintech NBFCs
- **PM - Enterprise SaaS:** Freshworks, Zoho, Salesforce
- **PM - EdTech:** upGrad, BYJU'S (matching your Meritto experience)

### Medium Probability (65-79)
- **PM - Payments:** BharatPe, Pine Labs
- **PM - B2B SaaS:** Different domains but SaaS experience relevant
- **PM - Workflow Automation:** Kissflow, similar to your CRM work

### Stretch Roles (50-64)
- **PM - E-commerce:** Flipkart, Meesho (domain shift)
- **PM - HealthTech:** Practo (new vertical)
- **Associate PM roles** (junior but good companies)

---

## 🛠️ Troubleshooting

### Issue: "Actor failed to run"
**Solution:** Check Apify token and quota
```bash
curl -H "Authorization: Bearer $APIFY_TOKEN" \
  https://api.apify.com/v2/users/me
```

### Issue: "No jobs found"
**Solution:** 
1. Verify search keywords match job market terms
2. Check location filters (some platforms are region-specific)
3. Adjust experience level filters

### Issue: "Fit scores all low"
**Solution:** 
1. Review profile keywords - add more domain-specific terms
2. Check skill names match industry standards
3. Adjust scoring weights in `calculate_fit_score()`

### Issue: "Dashboard not loading"
**Solution:**
1. Ensure file is at correct path: `~/.cursor/projects/empty-window/canvases/`
2. Check for TypeScript errors in canvas file
3. Restart Cursor IDE

---

## 📚 Resources

### Apify Documentation
- [Apify Platform Docs](https://docs.apify.com/)
- [Actor Development](https://docs.apify.com/academy/apify-platform/getting-started)
- [API Reference](https://docs.apify.com/api/v2)

### Job Search Platforms
- [LinkedIn Jobs](https://www.linkedin.com/jobs/)
- [Naukri.com](https://www.naukri.com/)
- [Wellfound](https://wellfound.com/)
- [Internshala](https://internshala.com/)

### Product Manager Resources
- [Product Hunt Jobs](https://www.producthunt.com/jobs)
- [YC Startup Jobs](https://www.ycombinator.com/jobs)
- [AngelList (Wellfound)](https://wellfound.com/)

---

## 🎓 Next Steps

1. **Get Apify Token** and run your first scrape
2. **Review Top 10** high-probability matches
3. **Customize Applications** for your top 3 picks
4. **Track in Dashboard** - mark applied/interviewing
5. **Set Up Automation** for daily updates
6. **Refine Profile** based on results
7. **Expand Sources** - add more job boards

---

## 🤝 Contributing

Want to improve the system? Ideas:
- Add more job sources (Indeed, Glassdoor, etc.)
- Build email notification system
- Create mobile app version
- Add ML-based scoring
- Integrate with ATS (Applicant Tracking System)

---

## 📝 License

MIT License - Feel free to use and modify for your job search!

---

## 💬 Support

For questions or issues:
1. Check the Troubleshooting section
2. Review Apify actor documentation
3. Test individual components separately

---

**Good luck with your job search! 🚀**

Remember: Quality over quantity. Focus on high-probability matches where your unique experience (fintech lending + enterprise SaaS + 0→1 products) gives you a competitive edge.
