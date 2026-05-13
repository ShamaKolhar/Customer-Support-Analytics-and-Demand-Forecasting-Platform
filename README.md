---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python (pandas, numpy) | Data generation & wrangling |
| SQL Server | Exploratory data analysis |
| Matplotlib, Seaborn | Data visualisation |
| Prophet | Time series forecasting |
| Scikit-learn (K-Means) | Customer segmentation |

---

## Dataset

Synthetically generated dataset of **100,000 support tickets** and **17,929 customers** 
across 2 years (2023–2024), designed to reflect realistic OTA support patterns:

- Seasonal peaks in December/January and June/July
- Email channel with 2.5× longer wait times than chat
- Escalation probability correlated with issue type, wait time, and CSAT
- Loyalty tiers: Bronze, Silver, Gold, Platinum

---

## Key Findings

### 1. Email Channel is Failing SLA
- Email SLA breach rate: **75.2%**
- Chat SLA breach rate: **0.1%**
- Email handles 30% of volume but accounts for the majority of SLA failures

### 2. Payment Issues Take Longest to Resolve
- Average wait time: **32.3 minutes**
- SLA breach rate: **33.8%**
- These tickets are complex and require specialist knowledge

### 3. Long Waits Directly Drive Escalations
| Wait Time | Avg CSAT | Escalation Rate |
|---|---|---|
| 0–10 min | 3.91 | 9.0% |
| 11–20 min | 3.87 | 10.6% |
| 31–60 min | 3.69 | 18.6% |
| 60+ min | 3.51 | 22.4% |

### 4. Seasonal Demand Peaks are Predictable
- December and January consistently see 5,000–5,500 tickets/month
- Mid-year (February–April) drops to ~3,400–3,600 tickets/month
- 2025 forecast confirms the same pattern will continue

### 5. High-Value Customers Receive No Priority Treatment
- Platinum and Bronze customers have identical wait times (~23 min)
- Escalation rates are the same across all loyalty tiers
- No evidence of priority queue routing for premium customers

---

## Business Recommendations

### R1 — Redistribute Email Volume to Chat
**Finding:** Email breaches SLA 75% of the time vs 0.1% for chat  
**Action:** Introduce chat-first routing with email as fallback only. Add automated 
email acknowledgements within 5 minutes to reset customer expectations.  
**Expected Impact:** Reduce overall SLA breach rate from 24% to under 15%

### R2 — Create a Specialist Payment Team
**Finding:** Payment Issues have the highest wait times and breach rates  
**Action:** Dedicate 10–15 agents exclusively to Payment and Refund tickets with 
deeper training and direct escalation paths.  
**Expected Impact:** Reduce Payment Issue average wait from 32 min to under 20 min

### R3 — Set a 45-Minute Hard Cap with Supervisor Alerts
**Finding:** Escalation rate jumps to 22% for tickets over 60 minutes  
**Action:** Implement automated supervisor alerts at the 45-minute mark before 
tickets reach the critical threshold.  
**Expected Impact:** Reduce escalation rate from 12.6% to under 8%

### R4 — Pre-Hire Seasonal Contractors for December & July
**Finding:** December/January and June/July see 30–40% more tickets than off-peak  
**Action:** Based on the 2025 forecast, begin contractor hiring in November and May 
to avoid SLA degradation during peak periods.  
**Expected Impact:** Maintain consistent SLA performance year-round

### R5 — Implement Loyalty-Based Queue Routing
**Finding:** Platinum customers wait as long as Bronze customers  
**Action:** Route Platinum and Gold tickets to a dedicated fast-track queue with 
a 15-minute SLA target.  
**Expected Impact:** Improve Platinum CSAT and reduce churn among high-value customers

---

## Forecasting

Using Facebook Prophet on 24 months of historical data (2023–2024):

- **Model:** Prophet with yearly seasonality
- **Forecast horizon:** 12 months (Jan–Dec 2025)
- **Key prediction:** December 2025 expected to reach **5,400–5,800 tickets**
- **Confidence interval:** 95%

<img width="2676" height="1766" alt="dashboard" src="https://github.com/user-attachments/assets/eb539e71-33bc-419f-bcc8-576437c2e86b" />
<img width="800" height="400" alt="Figure_1" src="https://github.com/user-attachments/assets/5a766e19-df6d-4e11-829d-44bd5fcb600f" />


---

## Customer Segmentation

K-Means clustering (k=4) on 6 behavioural features:

| Segment | Size | Avg Wait | Escalation Rate | Action |
|---|---|---|---|---|
| Happy & Efficient | 32.6% | 16.4 min | 4% | Retain via loyalty rewards |
| At Risk | 29.3% | 22.6 min | 11% | Proactive outreach |
| Frustrated & Waiting | 21.5% | 34.2 min | 10% | Reduce wait times urgently |
| High Risk | 16.6% | 22.6 min | 36% | Assign specialist agents |

<img width="700" height="700" alt="3" src="https://github.com/user-attachments/assets/3f47d67b-6d7b-41f2-806e-d385ccea8f80" />


---

## Dashboard

<img width="2676" height="1766" alt="dashboard" src="https://github.com/user-attachments/assets/6ae4a3e5-541c-4a58-b7a2-80f9f4e7cb2f" />


---

## Author
Built as a portfolio project for a Data Analyst role in the OTA/travel domain.
