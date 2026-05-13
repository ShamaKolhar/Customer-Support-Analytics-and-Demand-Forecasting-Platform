import pandas as pd
import numpy as np
import random
from faker import Faker
fake = Faker()


n = 100_000

#lookup tables
issue_types   = ["Booking Modification", "Cancellation Request", 
                 "Refund Inquiry", "Payment Issue", "Hotel Complaint"]
issue_weights = [0.22, 0.18, 0.16, 0.13, 0.10]
channels        = ["chat", "email", "call"]
channel_weights = [0.45, 0.30, 0.25]

base_wait_map = {
    "Booking Modification" : 12,
    "Cancellation Request" : 18,
    "Refund Inquiry"       : 22,
    "Payment Issue"        : 25,
    "Hotel Complaint"      : 15,
}

channel_mult = {"chat": 0.7, "email": 2.5, "call": 1.0}

# Generating categorical columns
issue_col   = random.choices(issue_types,   weights=issue_weights,   k=n)
channel_col = random.choices(channels,      weights=channel_weights, k=n)

# Generating wait_time 
wait_col = []
for i in range(n):
    base = base_wait_map[issue_col[i]] * channel_mult[channel_col[i]]
    wait = max(1, int(np.random.normal(loc=base, scale=base * 0.3)))
    wait_col.append(wait)

# Generating CSAT based off wait time
csat_col = []
for wait in wait_col:
    base  = 4.5 - (wait / 150)
    score = int(np.clip(np.random.normal(loc=base, scale=0.9), 1, 5))
    csat_col.append(score)

#Generating escalation
escalated = []
for i in range(n):
    prob = 0.08
    if issue_col[i]=="Payment Issue": prob += 0.10
    if wait_col[i] > 30:               prob += 0.08 # long wait
    if csat_col[i] <= 2:               prob += 0.15
    escalated.append(random.random() < prob)

import random
from datetime import datetime, timedelta

#Seasonal weights: higher in Dec-Jan and Jun-Aug
monthly_weights = [0.10, 0.07, 0.07, 0.07, 0.08, 0.09, 0.10, 0.09, 0.07, 0.07, 0.08, 0.11]

months     = random.choices(range(1, 13), weights=monthly_weights, k=n)
hours      = random.choices(range(0, 24),
                weights=[0.01,0.01,0.01,0.01,0.01,0.02,0.03,0.05,0.07,
                         0.09,0.08,0.07,0.06,0.06,0.07,0.07,0.06,0.05,
                         0.04,0.03,0.03,0.02,0.02,0.01], k=n)

created_at = []
for i in range(n):
    year = random.choice([2023, 2024])
    month = months[i]
    day = random.randint(1, 28)
    hour = hours[i]
    minute = random.randint(0, 59)
    dt = datetime(year, month, day, hour, minute)
    created_at.append(dt)

countries        = ["Thailand", "Indonesia", "Vietnam", "Philippines", "India", "Singapore"]
country_weights  = [0.22, 0.20, 0.18, 0.15, 0.15, 0.10]
country_col      = random.choices(countries, weights=country_weights, k=n)

resolution_col   = [max(wait_col[i], int(np.random.normal(loc=wait_col[i]*1.4, scale=10)))
                    for i in range(n)]

sla_col          = [w > 30 for w in wait_col]

refund_weights_map = {
    "Booking Modification" : 0.10,
    "Cancellation Request" : 0.40,
    "Refund Inquiry"       : 0.70,
    "Payment Issue"        : 0.55,
    "Hotel Complaint"      : 0.20,
}
refund_col = [random.random() < refund_weights_map[issue_col[i]] for i in range(n)]

customer_col = [f"CUST{random.randint(1, 18000):06d}" for _ in range(n)]
booking_col  = [f"BKG{random.randint(1, 50000):07d}" for _ in range(n)]
agent_col    = [f"AGT{random.randint(1, 150):04d}" for _ in range(n)]
#Building dataframe
df = pd.DataFrame({
    "ticket_id"       : [f"TKT{i:07d}" for i in range(1, n + 1)],
    "customer_id"     : customer_col,
    "booking_id"      : booking_col,
    "agent_id"        : agent_col,
    "issue_type"      : issue_col,
    "channel"         : channel_col,
    "country"         : country_col,
    "created_at"      : created_at,
    "wait_time"       : wait_col,
    "resolution_time" : resolution_col,
    "csat_score"      : csat_col,
    "escalated"       : escalated,
    "refund_requested": refund_col,
    "sla_breached"    : sla_col,
})

# For self Verification
print(df.head())
print(df.describe())
print(f"\nEscalation rate: {df['escalated'].mean()*100:.1f}%")

# ── STEP 7: save ──────────────────────────
df.to_csv("tickets.csv", index=False)
print("Saved tickets.csv successfully!")

df.head()
df.describe()
print(df.shape)
print(df.dtypes)
print(f"SLA breach rate: {df['sla_breached'].mean()*100:.1f}%")
print(f"Refund request rate: {df['refund_requested'].mean()*100:.1f}%")


# Customers table
unique_customers = df["customer_id"].unique()
nc = len(unique_customers)

loyalty_tiers        = ["Bronze", "Silver", "Gold", "Platinum"]
loyalty_weights      = [0.50, 0.25, 0.15, 0.10]

loyalty_col     = random.choices(loyalty_tiers, weights=loyalty_weights, k=nc)

# Booking value correlated with loyalty tier
avg_booking_map = {"Bronze": 80, "Silver": 150, "Gold": 280, "Platinum": 500}
booking_value_col = [
    round(max(20, np.random.lognormal(
        mean=np.log(avg_booking_map[loyalty_col[i]]), sigma=0.4)), 2)
    for i in range(nc)
]

repeat_col = [
    random.random() < (0.20 if loyalty_col[i] == "Bronze"
                  else 0.45 if loyalty_col[i] == "Silver"
                  else 0.65 if loyalty_col[i] == "Gold"
                  else 0.85)
    for i in range(nc)
]

customers_df = pd.DataFrame({
    "customer_id"       : unique_customers,
    "loyalty_tier"      : loyalty_col,
    "avg_booking_value" : booking_value_col,
    "repeat_customer"   : repeat_col,
    "country"           : random.choices(countries, weights=country_weights, k=nc),
})

print(customers_df.shape)
print(customers_df.head())
print(customers_df["loyalty_tier"].value_counts())

customers_df.to_csv("customers.csv", index=False)
print("Saved customers.csv ✅")

print("DEBUG: reached customers section")
print(f"Unique customers: {nc}")