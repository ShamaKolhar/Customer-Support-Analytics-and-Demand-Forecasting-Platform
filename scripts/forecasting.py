import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

tickets = pd.read_csv(r"C:\Users\Shama_Innodata\Desktop\Customer Support Analytics\data\tickets.csv")
tickets["created_at"] = pd.to_datetime(tickets["created_at"])

monthly = (tickets.groupby(tickets["created_at"].dt.to_period("M"))
           .size()
           .reset_index(name="y"))

monthly["ds"] = monthly["created_at"].dt.to_timestamp()
monthly = monthly[["ds", "y"]]

print(monthly)
print(f"\nShape: {monthly.shape}")


model = Prophet(
    yearly_seasonality=True,   # picks up Dec/Jan peaks
    weekly_seasonality=False,  # monthly data, so no weekly patterns
    daily_seasonality=False,
    interval_width=0.95        # 95% confidence band
)

model.fit(monthly)

# 12 month ahead forecast
future = model.make_future_dataframe(periods=12, freq="MS")
forecast = model.predict(future)

result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(12)
result.columns = ["month", "predicted", "lower_bound", "upper_bound"]
result["predicted"]    = result["predicted"].astype(int)
result["lower_bound"]  = result["lower_bound"].astype(int)
result["upper_bound"]  = result["upper_bound"].astype(int)

print("\n── 2025 Forecast ──")
print(result.to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly["ds"], monthly["y"], 
        "o-", color="steelblue", label="Actual", linewidth=2)
ax.plot(forecast["ds"], forecast["yhat"], 
        "--", color="darkorange", label="Forecast", linewidth=2)
ax.fill_between(forecast["ds"], 
                forecast["yhat_lower"], forecast["yhat_upper"],
                alpha=0.2, color="darkorange", label="95% Confidence")
ax.axvline(pd.Timestamp("2025-01-01"), 
           color="red", linestyle=":", linewidth=1.5, label="Forecast start")
ax.set_title("Monthly Ticket Volume Forecast (2025)", 
             fontsize=14, fontweight="bold")
ax.set_ylabel("Ticket Count")
ax.set_xlabel("")
ax.legend()
plt.tight_layout()
plt.savefig("forecast.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nSaved forecast.png")