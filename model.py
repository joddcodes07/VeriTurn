import pandas as pd
import numpy as np
import sys
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler

def run_model(input_csv, output_csv):
    try:
        # -----------------------------
        # 1. Load Data
        # -----------------------------
        df = pd.read_csv(input_csv)

        # --- HACKATHON SAFETY CHECK ---
        required_columns = ["customer_id", "purchase_date", "return_date", "return_amount", "purchase_amount"]
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"❌ Error: The uploaded CSV is missing required columns: {missing_cols}")
            return
        
        # --- DATA CLEANSING: PREVENT DOUBLE COUNTING ---
        # Remove exact duplicates that might have been uploaded
        df = df.drop_duplicates() 
        # ----------------------------------------------

        df["purchase_date"] = pd.to_datetime(df["purchase_date"])
        df["return_date"] = pd.to_datetime(df["return_date"], errors="coerce")
        df["return_amount"] = df["return_amount"].fillna(0)

        # -----------------------------
        # 2. Calculate Return Days
        # -----------------------------
        df["return_days"] = (
            df["return_date"] - df["purchase_date"]
        ).dt.days

        # -----------------------------
        # 3. Customer Aggregation
        # -----------------------------
        customer = df.groupby("customer_id").agg(
            total_purchase_count=("purchase_amount", "count"),
            total_purchase_value=("purchase_amount", "sum"),
            total_return_count=("return_date", lambda x: x.notna().sum()),
            total_return_value=("return_amount", "sum"),
            avg_return_days=("return_days", "mean")
        ).reset_index()

        # --- REFINEMENT: CAP RETURN VALUE ---
        # Logic: A return cannot realistically be more than the purchase price.
        # This prevents "garbage" data from creating massive artificial losses.
        customer["total_return_value"] = customer[["total_return_value", "total_purchase_value"]].min(axis=1)
        # ------------------------------------

        # Return ratio
        customer["return_ratio"] = (
            customer["total_return_count"] /
            customer["total_purchase_count"]
        ).clip(0, 1) # Cannot return more items than purchased

        # Damage ratio (financial impact)
        customer["damage_ratio"] = (
            customer["total_return_value"] /
            customer["total_purchase_value"]
        ).replace([np.inf, -np.inf], 0).fillna(0).clip(0, 1)

        customer["avg_return_days"] = customer["avg_return_days"].fillna(0)

        # -----------------------------
        # 4. Isolation Forest
        # -----------------------------
        features = customer[
            ["return_ratio", "total_return_value",
             "avg_return_days", "damage_ratio"]
        ]

        scaler = MinMaxScaler()
        features_scaled = scaler.fit_transform(features)

        model = IsolationForest(
            n_estimators=200,
            contamination=0.1,
            random_state=42
        )

        model.fit(features_scaled)

        anomaly_score = model.decision_function(features_scaled)
        anomaly_score = MinMaxScaler().fit_transform(
            anomaly_score.reshape(-1, 1)
        ).flatten()

        customer["anomaly_score"] = 1 - anomaly_score

        # -----------------------------
        # 5. Final Risk Score (0–100)
        # -----------------------------
        customer["risk_score"] = (
            0.45 * customer["anomaly_score"] +
            0.25 * customer["return_ratio"] +
            0.20 * (1 - customer["avg_return_days"].rank(pct=True)) +
            0.10 * customer["damage_ratio"]
        ) * 100

        customer["risk_score"] = customer["risk_score"].clip(0, 100)

        # -----------------------------
        # 6. Risk Level
        # -----------------------------
        def classify(score):
            if score >= 70:
                return "High"
            elif score >= 40:
                return "Moderate"
            else:
                return "Low"

        customer["risk_level"] = customer["risk_score"].apply(classify)

        # -----------------------------
        # 7. Save Output
        # -----------------------------
        customer.to_csv(output_csv, index=False)

        print("✅ Model executed successfully.")
        print(f"Output saved to: {output_csv}")

    except Exception as e:
        print(f"❌ A critical error occurred while processing the data: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python model.py input.csv output.csv")
    else:
        run_model(sys.argv[1], sys.argv[2])