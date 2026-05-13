import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

tickets   = pd.read_csv(r"C:\Users\Shama_Innodata\Desktop\Customer Support Analytics\data\tickets.csv")
customers = pd.read_csv(r"C:\Users\Shama_Innodata\Desktop\Customer Support Analytics\data\customers.csv")

# merge for loyalty queries
df = tickets.merge(customers, on="customer_id", how="left")

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(18, 12))
fig.suptitle("Customer Support Analytics Dashboard", fontsize=16, fontweight="bold")

#SLA Breach by Channel
channel_stats = (tickets.groupby("channel")
                 .agg(breach_pct=("sla_breached", lambda x: round(x.mean()*100, 1)))
                 .reset_index()
                 .sort_values("breach_pct", ascending=False))

sns.barplot(data=channel_stats, x="channel", y="breach_pct", 
            palette="Reds_r", ax=axes[0,0])
axes[0,0].set_title("SLA Breach Rate by Channel")
axes[0,0].set_ylabel("Breach Rate (%)")
axes[0,0].set_xlabel("")
for bar, val in zip(axes[0,0].patches, channel_stats["breach_pct"]):
    axes[0,0].text(bar.get_x() + bar.get_width()/2, 
                   bar.get_height() + 1, f"{val}%", 
                   ha="center", fontsize=9, fontweight="bold")

#Monthly Ticket Volume
tickets["created_at"] = pd.to_datetime(tickets["created_at"])
monthly = (tickets.groupby(tickets["created_at"].dt.to_period("M"))
           .size().reset_index(name="ticket_count"))
monthly["created_at"] = monthly["created_at"].astype(str)

axes[0,1].plot(monthly["created_at"], monthly["ticket_count"], 
               color="steelblue", linewidth=2, marker="o", markersize=3)
axes[0,1].set_title("Monthly Ticket Volume")
axes[0,1].set_ylabel("Ticket Count")
axes[0,1].set_xlabel("")
axes[0,1].tick_params(axis="x", rotation=30)
axes[0,1].set_xticks(range(0, len(monthly), 2))

# highlight peaks
peak_idx = monthly["ticket_count"].idxmax()
axes[0,1].annotate("Peak", 
                    xy=(peak_idx, monthly["ticket_count"][peak_idx]),
                    xytext=(peak_idx - 3, monthly["ticket_count"][peak_idx] + 150),
                    arrowprops=dict(arrowstyle="->", color="red"),
                    color="red", fontsize=9)

# Wait Time Bucket vs CSAT
tickets["wait_bucket"] = pd.cut(tickets["wait_time"], 
                                 bins=[0, 10, 20, 30, 60, 999],
                                 labels=["0-10", "11-20", "21-30", "31-60", "60+"])
bucket_stats = (tickets.groupby("wait_bucket", observed=True)
                .agg(avg_csat=("csat_score", "mean"),
                     escalation_pct=("escalated", lambda x: x.mean()*100))
                .reset_index())

color = "coral"
ax2 = axes[1,0]
ax2_twin = ax2.twinx()
ax2.bar(bucket_stats["wait_bucket"].astype(str), 
        bucket_stats["avg_csat"], color=color, alpha=0.7, label="Avg CSAT")
ax2_twin.plot(bucket_stats["wait_bucket"].astype(str), 
              bucket_stats["escalation_pct"], 
              color="darkred", marker="o", linewidth=2, label="Escalation %")
ax2.set_title("Wait Time vs CSAT & Escalation")
ax2.set_ylabel("Avg CSAT", color=color)
ax2.set_xlabel("Wait Time (min)")
ax2_twin.set_ylabel("Escalation %", color="darkred")
ax2.set_ylim(3, 5)

#Breach Rate by Loyalty Tier
loyalty_stats = (df.groupby("loyalty_tier")
                 .agg(breach_pct=("sla_breached", lambda x: round(x.mean()*100, 1)),
                      avg_wait=("wait_time", "mean"))
                 .reset_index())
order = ["Platinum", "Gold", "Silver", "Bronze"]
loyalty_stats["loyalty_tier"] = pd.Categorical(loyalty_stats["loyalty_tier"], 
                                                categories=order, ordered=True)
loyalty_stats = loyalty_stats.sort_values("loyalty_tier")

sns.barplot(data=loyalty_stats, x="loyalty_tier", y="breach_pct",
            palette="Blues_r", ax=axes[1,1])
axes[1,1].set_title("SLA Breach Rate by Loyalty Tier")
axes[1,1].set_ylabel("Breach Rate (%)")
axes[1,1].set_xlabel("")
for bar, val in zip(axes[1,1].patches, loyalty_stats["breach_pct"]):
    axes[1,1].text(bar.get_x() + bar.get_width()/2,
                   bar.get_height() + 0.3, f"{val}%",
                   ha="center", fontsize=10, fontweight="bold")

for bar, val in zip(axes[1,1].patches, loyalty_stats["breach_pct"]):
    axes[1,1].text(bar.get_x() + bar.get_width()/2,
                   bar.get_height() + 0.3, f"{val}%",
                   ha="center", fontsize=10, fontweight="bold")

# Adding title padding
axes[0,0].set_title("SLA Breach Rate by Channel", pad=15)

axes[0,1].set_title("Monthly Ticket Volume", pad=15)

ax2.set_title("Wait Time vs CSAT & Escalation", pad=15)

axes[1,1].set_title("SLA Breach Rate by Loyalty Tier", pad=15)

#layout
plt.subplots_adjust(hspace=0.35, wspace=0.25)
plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig("dashboard.png", dpi=150, bbox_inches="tight")
plt.show()