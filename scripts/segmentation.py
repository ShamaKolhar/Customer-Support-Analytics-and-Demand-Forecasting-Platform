import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


tickets   = pd.read_csv(r"C:\Users\Shama_Innodata\Desktop\Customer Support Analytics\data\tickets.csv")
customers = pd.read_csv(r"C:\Users\Shama_Innodata\Desktop\Customer Support Analytics\data\customers.csv")
df = tickets.merge(customers, on="customer_id", how="left")

# One row per customer, summarising their ticket history
customer_features = df.groupby("customer_id").agg(
    total_tickets    = ("ticket_id",    "count"),
    avg_wait         = ("wait_time",    "mean"),
    avg_csat         = ("csat_score",   "mean"),
    escalation_rate  = ("escalated",    "mean"),
    sla_breach_rate  = ("sla_breached", "mean"),
    refund_rate      = ("refund_requested", "mean"),
).reset_index()

print(customer_features.shape)
print(customer_features.head())
print(customer_features.describe().round(2))

features = ["total_tickets", "avg_wait", "avg_csat", 
            "escalation_rate", "sla_breach_rate", "refund_rate"]

scaler = StandardScaler()
X = scaler.fit_transform(customer_features[features])

#finding optimal number of clusters using elbow method
inertia = []
k_range = range(2, 10)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertia.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(k_range, inertia, marker="o", color="steelblue", linewidth=2)
plt.title("Elbow Method — Optimal Number of Clusters", fontsize=13, fontweight="bold")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.xticks(k_range)
plt.tight_layout()
plt.savefig("elbow_chart.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved elbow_chart.png")

#training model with k=4
km_final = KMeans(n_clusters=4, random_state=42, n_init=10)
customer_features["segment"] = km_final.fit_predict(X)

segment_profile = customer_features.groupby("segment").agg(
    customer_count   = ("customer_id",     "count"),
    avg_tickets      = ("total_tickets",   "mean"),
    avg_wait         = ("avg_wait",        "mean"),
    avg_csat         = ("avg_csat",        "mean"),
    escalation_rate  = ("escalation_rate", "mean"),
    sla_breach_rate  = ("sla_breach_rate", "mean"),
    refund_rate      = ("refund_rate",     "mean"),
).round(2)

print(segment_profile)

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle("Customer Segments — Profile Comparison", 
             fontsize=14, fontweight="bold")

metrics = ["avg_wait", "avg_csat", "escalation_rate"]
titles  = ["Avg Wait Time (min)", "Avg CSAT Score", "Escalation Rate"]
colors  = ["steelblue", "coral", "darkred"]

for i, (metric, title, color) in enumerate(zip(metrics, titles, colors)):
    axes[i].bar(segment_profile.index.astype(str), 
                segment_profile[metric], color=color, alpha=0.8)
    axes[i].set_title(title, fontsize=12)
    axes[i].set_xlabel("Segment")
    for bar, val in zip(axes[i].patches, segment_profile[metric]):
        axes[i].text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + 0.01,
                     f"{val:.2f}", ha="center", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("segments.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved segments.png")


#Adding business labels
segment_names = {
    0: "At Risk",
    1: "Happy & Efficient",
    2: "High Risk",
    3: "Frustrated & Waiting"
}

customer_features["segment_name"] = customer_features["segment"].map(segment_names)

size = customer_features["segment_name"].value_counts()
print(size)

#pie chart
fig, ax = plt.subplots(figsize=(7, 7))
colors = ["steelblue", "seagreen", "crimson", "darkorange"]
ax.pie(size.values, labels=size.index, autopct="%1.1f%%",
       colors=colors, startangle=140,
       textprops={"fontsize": 12})
ax.set_title("Customer Segment Distribution", 
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("segment_distribution.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved segment_distribution.png")

customer_features.to_csv(r"C:\Users\Shama_Innodata\Desktop\Customer Support Analytics\data\customers_segmented.csv", index=False)
print("Saved customers_segmented.csv")