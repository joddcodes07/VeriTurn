import pandas as pd
import os

# ==================================================
# MAC CRASH FIX: Force Headless Mode
# MUST BE BEFORE IMPORTING PYPLOT
# ==================================================
import matplotlib
matplotlib.use('Agg')
# ==================================================

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

os.makedirs("charts", exist_ok=True)

# Note: Make sure 'output.csv' is actually in your VERITURN folder!
df = pd.read_csv("output.csv")

# --------------------------------
# 1. Cluster Scatter Plot
# --------------------------------
if {"return_ratio", "total_return_value"}.issubset(df.columns):

    X = df[["return_ratio", "total_return_value"]]

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X)

    plt.figure()
    plt.scatter(
        X["return_ratio"],
        X["total_return_value"],
        c=clusters
    )
    plt.xlabel("Return Ratio")
    plt.ylabel("Total Return Value")
    plt.title("Customer Behaviour Clusters")
    plt.savefig("charts/cluster_scatter.png")
    plt.close()

# --------------------------------
# 2. Purchase Value Histogram
# --------------------------------
plt.figure()
plt.hist(df["total_purchase_value"], bins=25)
plt.title("Purchase Value Distribution")
plt.xlabel("Total Purchase Value")
plt.savefig("charts/purchase_value.png")
plt.close()

# --------------------------------
# 3. Return Ratio Histogram
# --------------------------------
plt.figure()
plt.hist(df["return_ratio"], bins=25)
plt.title("Return Ratio Distribution")
plt.xlabel("Return Ratio")
plt.savefig("charts/return_ratio.png")
plt.close()

# --------------------------------
# 4. Risk Score Histogram
# --------------------------------
plt.figure()
plt.hist(df["risk_score"], bins=25)
plt.title("Risk Score Distribution")
plt.xlabel("Risk Score")
plt.savefig("charts/risk_score.png")
plt.close()

# --------------------------------
# 5. Risk Level Pie Chart
# --------------------------------
counts = df["risk_level"].value_counts()

plt.figure()
plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
plt.title("Risk Level Distribution")
plt.savefig("charts/risk_level.png")
plt.close()

# --------------------------------
# 6. Top 10 Customers by Purchase
# --------------------------------
top_customers = df.sort_values(
    "total_purchase_value",
    ascending=False
).head(10)

plt.figure()
plt.bar(
    top_customers["customer_id"].astype(str),
    top_customers["total_purchase_value"]
)
plt.xticks(rotation=60)
plt.title("Top 10 Customers by Purchase Value")
plt.savefig("charts/top_customers.png")
plt.close()

# ======================================
# FRAUD SECTION
# ======================================

frauds = df[df["risk_level"] == "High"]

if len(frauds) > 0:

    # --------------------------------
    # 7. Top 20 High-Risk Customers
    # --------------------------------
    top_frauds = frauds.sort_values(
        "risk_score",
        ascending=False
    ).head(20)

    plt.figure()
    plt.bar(
        top_frauds["customer_id"].astype(str),
        top_frauds["risk_score"]
    )
    plt.xticks(rotation=60)
    plt.title("Top 20 High-Risk Customers")
    plt.savefig("charts/top_20_high_risk.png")
    plt.close()

    # --------------------------------
    # 8. Fraud Return Ratio Histogram
    # --------------------------------
    plt.figure()
    plt.hist(frauds["return_ratio"], bins=20)
    plt.title("Fraud Return Ratio Distribution")
    plt.savefig("charts/fraud_return_ratio.png")
    plt.close()

    # --------------------------------
    # 9. Fraud Damage Ratio Histogram
    # --------------------------------
    plt.figure()
    plt.hist(frauds["damage_ratio"], bins=20)
    plt.title("Fraud Damage Ratio Distribution")
    plt.savefig("charts/fraud_damage_ratio.png")
    plt.close()

    # --------------------------------
    # 10. Fraud Avg Return Days
    # --------------------------------
    plt.figure()
    plt.hist(frauds["avg_return_days"], bins=20)
    plt.title("Fraud Avg Return Days")
    plt.savefig("charts/fraud_return_days.png")
    plt.close()

print("🔥 All charts (including Top 20 High-Risk) generated successfully!")