# 🚀 Quick Start Guide - Job Hunting System

## ⚡ 5-Minute Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get Apify token
# Visit: https://console.apify.com/settings/integrations

# 3. Configure token
cp .env.example .env
nano .env  # Add your token

# 4. Run scraper
python3 job_scraper_enhanced.py
```

## 📊 View Dashboard

Open in Cursor:
```
canvases/job-tracker-dashboard.canvas.tsx
```

## 🎯 Your Profile Strengths

**Domain Expertise:**
- ✅ Fintech (Lending, Collections, Gold Loan)
- ✅ Enterprise SaaS (CRM/LMS)
- ✅ EdTech

**Differentiators:**
- ₹118 Cr+ revenue impact
- 0→1 product builds
- 50% TAT reduction
- Collections CRM (18% improvement)

## 🔍 Best Matching Keywords

Use these in your job search:
```
"product manager" + fintech
"product manager" + lending
"product manager" + collections
"product manager" + b2b saas
"product manager" + crm
"senior pm" + nbfc
"pm" + digital lending
"product" + workflow automation
```

## 💼 Target Companies

**Tier 1 (Best Fit):**
- Razorpay, Cred, Paytm (Fintech PM)
- Capri Global, Bajaj Finserv (NBFC PM)
- Freshworks, Zoho (Enterprise SaaS)

**Tier 2 (Strong Fit):**
- PhonePe, BharatPe (Payments)
- MoneyTap, Lendingkart (Lending)
- upGrad, BYJU'S (EdTech)

**Tier 3 (Growth):**
- Flipkart, Meesho (E-commerce)
- Practo, 1mg (HealthTech)

## 📈 Expected Fit Scores

| Category | Score | Job Examples |
|----------|-------|-------------|
| High | 80-100 | Fintech Lending PM, Collections CRM PM |
| Medium | 65-79 | Payments PM, Workflow Automation PM |
| Stretch | 50-64 | Consumer PM, New Domain PM |

## 🎨 Dashboard Features

- **Daily Alerts:** New jobs since last visit
- **Streak Tracker:** Gamified check-ins
- **Fit Scores:** AI-calculated match (0-100)
- **Hot Jobs:** High match + actively hiring
- **Closing Soon:** Apply within 48h
- **One-Click Apply:** Direct job links

## 📝 Application Strategy

### High Priority (80+ fit)
- ⏱️ Apply within 24 hours
- ✍️ Custom cover letter
- 💡 Highlight relevant achievement
- 📧 Follow up after 1 week

### Medium Priority (65-79)
- ⏱️ Apply within 48 hours
- ✍️ Standard cover letter
- 💡 Emphasize transferable skills
- 📧 Follow up after 2 weeks

### Stretch Roles (50-64)
- ⏱️ Apply within 1 week
- ✍️ Address skill gaps proactively
- 💡 Show learning mindset
- 📧 Optional follow-up

## 🔧 Commands Cheatsheet

```bash
# Run job scraper
python3 job_scraper_enhanced.py

# View results
cat jobs_*.json | jq '.summary'

# Setup automation (daily at 9 AM)
crontab -e
# Add: 0 9 * * * cd /path && python3 job_scraper_enhanced.py

# Check Apify quota
curl -H "Authorization: Bearer $APIFY_TOKEN" \
  https://api.apify.com/v2/users/me
```

## 🎯 Customization

### Adjust Fit Score Weights
Edit `job_scraper_apify.py`:
```python
def calculate_fit_score(job):
    score = 0
    score += domain_match * 0.30  # Change weights
    score += skills_match * 0.30
    score += experience * 0.20
    score += location * 0.10
    score += keywords * 0.10
```

### Add More Keywords
```python
PROFILE['keywords'].extend([
    'product owner',
    'technical pm',
    'growth pm',
])
```

### Filter by Salary
```python
min_salary = 30  # LPA
jobs = [j for j in jobs if extract_salary(j) >= min_salary]
```

## 📱 Daily Routine

**Morning (9:00 AM):**
1. Run job scraper (automated)
2. Check dashboard for new jobs
3. Review high-probability matches

**Afternoon:**
1. Apply to top 3 new high-fit roles
2. Customize applications
3. Update dashboard status

**Evening:**
1. Research companies
2. Connect with recruiters on LinkedIn
3. Prepare for interviews

## 🎓 Interview Prep

**Your Stories:**
1. Collections CRM (0→1 build)
   - Problem, Solution, Impact (18% improvement)

2. Gold Loan Product (TAT reduction)
   - How you reduced 40→20 mins
   - ₹118 Cr revenue contribution

3. Enterprise Onboarding (TAT -30%)
   - Process optimization
   - Stakeholder management

**Common Questions:**
- "Tell me about a 0→1 product you built"
  → Collections CRM story

- "How do you prioritize features?"
  → Talk about KPI/OKR framework

- "Experience with cross-functional teams?"
  → Mention engineering, ops, business stakeholders

## 🔗 Quick Links

- Dashboard: `canvases/job-tracker-dashboard.canvas.tsx`
- Scraper: `job_scraper_enhanced.py`
- Config: `.env`
- Docs: `README.md`
- Sample: `sample_output.json`

## 📞 Support

**Issue:** Actor fails
**Fix:** Check Apify quota/token

**Issue:** Low fit scores
**Fix:** Review profile keywords

**Issue:** Dashboard not loading
**Fix:** Check file path, restart Cursor

## 🎉 Success Metrics

Track weekly:
- [ ] Jobs scraped: ___
- [ ] Applications sent: ___
- [ ] Responses received: ___
- [ ] Interviews scheduled: ___
- [ ] Offers received: ___

---

**🎯 Goal:** Land a Senior PM role at a fintech/SaaS company leveraging your 5+ years of experience, domain expertise, and proven 0→1 product delivery track record.

**💪 Your Edge:** Unique combination of fintech lending + collections + enterprise SaaS + measurable business impact.

Good luck! 🚀
