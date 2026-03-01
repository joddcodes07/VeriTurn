from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os
import model

# ==================================================
# MAC/BACKGROUND MATPLOTLIB FIX 
# ==================================================
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# ==================================================

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static/charts"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

def generate_charts(df):
    charts = {}

    # 1. Behaviour Cluster Scatter
    if {"return_ratio", "total_return_value"}.issubset(df.columns):
        X = df[["return_ratio", "total_return_value"]]
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X)

        plt.figure(figsize=(8,6))
        plt.scatter(X["return_ratio"], X["total_return_value"], c=clusters)
        plt.xlabel("Return Ratio")
        plt.ylabel("Total Return Value (₹)")
        plt.title("Customer Behaviour Clusters")

        path = f"{STATIC_FOLDER}/cluster_scatter.png"
        plt.savefig(path)
        plt.close()
        charts["cluster_scatter"] = path

    # 2. Purchase Value Distribution
    plt.figure(figsize=(8,6))
    plt.hist(df["total_purchase_value"], bins=30)
    plt.title("Purchase Value Distribution")
    plt.xlabel("Total Purchase Value (₹)")

    path = f"{STATIC_FOLDER}/purchase_value.png"
    plt.savefig(path)
    plt.close()
    charts["purchase_value"] = path

    # 3. Risk Level Pie Chart
    counts = df["risk_level"].value_counts()
    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
    plt.title("Risk Level Distribution")

    path = f"{STATIC_FOLDER}/risk_level.png"
    plt.savefig(path)
    plt.close()
    charts["risk_level"] = path

    return charts

@app.route("/upload", methods=["POST"])
def upload_file():
    # 1. Save raw file
    file = request.files["file"]
    input_filepath = os.path.join(UPLOAD_FOLDER, "input.csv")
    file.save(input_filepath)

    # 2. RUN AI MODEL
    output_filepath = os.path.join(UPLOAD_FOLDER, "output.csv")
    model.run_model(input_filepath, output_filepath)

    # 3. Read processed data
    df = pd.read_csv(output_filepath)
    
    # --- CALCULATE MONTHLY SCALE FACTOR ---
    raw_df = pd.read_csv(input_filepath)
    raw_df['purchase_date'] = pd.to_datetime(raw_df['purchase_date'])
    days_span = (raw_df['purchase_date'].max() - raw_df['purchase_date'].min()).days
    months_count = max(1, days_span / 30.44) 

    # 4. Generate charts
    charts = generate_charts(df)

    # 5. DYNAMIC MONTHLY KPI METRICS
    high_risk_df = df[df["risk_level"] == "High"]
    monthly_est_loss = float(high_risk_df["total_return_value"].sum()) / months_count
    
    # Check for correct column naming for total returns
    total_col = "total_total_return_count" if "total_total_return_count" in df.columns else "total_return_count"
    monthly_total_returns = int(df[total_col].sum() / months_count)

    metrics = {
        "total_analyzed": monthly_total_returns, 
        "flagged_count": int(len(high_risk_df)),               
        "est_loss": monthly_est_loss,                                  
        "preventable_loss": monthly_est_loss * 0.85 
    }
    
    # 6. Flagged Intelligence Report Data with ALL Customers & NEW USP
    # Sorted by risk score, including ALL flagged customers (no .head() limit)
    top_frauds = df[df["risk_level"] == "High"].sort_values("risk_score", ascending=False)
    table_data = []
    
    for _, row in top_frauds.iterrows():
        # --- REASONING ENGINE ---
        reasons = []
        if row["return_ratio"] >= 0.9:
            reasons.append("Critical return frequency.")
        elif row["return_ratio"] > 0.7:
            reasons.append("High return volume.")

        if row["avg_return_days"] <= 1:
            reasons.append("Immediate return cycle detected.")
        elif row["avg_return_days"] < 3:
            reasons.append("Short-term return pattern.")

        if row["damage_ratio"] > 0.8:
            reasons.append("Severe financial impact.")
        elif row["damage_ratio"] > 0.5:
            reasons.append("Significant revenue loss.")
        
        final_reasons = reasons[:2] 
        ai_justification = " | ".join(final_reasons) if final_reasons else "Pattern matches known fraud profile."

        # --- REFINED USP POLICY: NEXT PURCHASE RECOMMENDATION ---
        # Providing a policy recommendation instead of a fixed calculation
        policy_recommendation = "Apply 5% Risk Premium surcharge on next transaction value."
        # --------------------------------------------------------

        table_data.append({
            "id": str(row.get("customer_id", "Unknown")),
            "price": f"₹{float(row.get('total_purchase_value', 0)):,.2f}",
            "window": str(int(row.get('avg_return_days', 0))),
            "score": int(row.get('risk_score', 0)),
            "status": "Flagged",
            "reason": ai_justification,
            "usp_policy": policy_recommendation # Dynamic policy recommendation
        })

    return jsonify({
        "metrics": metrics,
        "charts": charts,
        "table_data": table_data
    })

@app.route("/download-report")
def download_report():
    output_path = os.path.join(UPLOAD_FOLDER, "output.csv")
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return jsonify({"error": "No report found."}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)