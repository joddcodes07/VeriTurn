from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import pandas as pd
import os
import model

import matplotlib

os.environ['MPLCONFIGDIR'] = "/tmp/matplotlib_cache" 
matplotlib.use('Agg') # Headless mode for server
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
# ==================================================

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["POST", "GET", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}}, supports_credentials=True)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static/charts"

# Create directories with write permissions
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# ADDED: Explicit route to serve generated chart images to the frontend
@app.route('/static/charts/<path:filename>')
def serve_charts(filename):
    return send_from_directory(STATIC_FOLDER, filename)

def generate_charts(df):
    """Generates and saves behavioral analysis charts as static PNGs."""
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

        path = f"cluster_scatter.png" # Path relative to STATIC_FOLDER
        plt.savefig(os.path.join(STATIC_FOLDER, path))
        plt.close()
        charts["cluster_scatter"] = f"static/charts/{path}"

    # 2. Purchase Value Distribution
    plt.figure(figsize=(8,6))
    plt.hist(df["total_purchase_value"], bins=30)
    plt.title("Purchase Value Distribution")
    plt.xlabel("Total Purchase Value (₹)")

    path = f"purchase_value.png"
    plt.savefig(os.path.join(STATIC_FOLDER, path))
    plt.close()
    charts["purchase_value"] = f"static/charts/{path}"

    # 3. Risk Level Pie Chart
    counts = df["risk_level"].value_counts()
    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%")
    plt.title("Risk Level Distribution")

    path = f"risk_level.png"
    plt.savefig(os.path.join(STATIC_FOLDER, path))
    plt.close()
    charts["risk_level"] = f"static/charts/{path}"

    return charts

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload_file():
    """Handles CSV ingestion, AI processing, and metric generation."""
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    # 1. Save raw file for processing
    file = request.files["file"]
    input_filepath = os.path.join(UPLOAD_FOLDER, "input.csv")
    file.save(input_filepath)

    # 2. Execute AI Model
    output_filepath = os.path.join(UPLOAD_FOLDER, "output.csv")
    model.run_model(input_filepath, output_filepath)

    # 3. Read processed results
    df = pd.read_csv(output_filepath)
    
    # --- CALCULATE MONTHLY SCALE FACTOR ---
    raw_df = pd.read_csv(input_filepath)
    raw_df['purchase_date'] = pd.to_datetime(raw_df['purchase_date'])
    days_span = (raw_df['purchase_date'].max() - raw_df['purchase_date'].min()).days
    months_count = max(1, days_span / 30.44) 

    # 4. Generate analytics charts
    charts = generate_charts(df)

    # 5. Dynamic Monthly KPI Metrics
    high_risk_df = df[df["risk_level"] == "High"]
    monthly_est_loss = float(high_risk_df["total_return_value"].sum()) / months_count
    
    total_col = "total_total_return_count" if "total_total_return_count" in df.columns else "total_return_count"
    monthly_total_returns = int(df[total_col].sum() / months_count)

    metrics = {
        "total_analyzed": monthly_total_returns, 
        "flagged_count": int(len(high_risk_df)),               
        "est_loss": monthly_est_loss,                                  
        "preventable_loss": monthly_est_loss * 0.85 
    }
    
    # 6. Flagged Intelligence Report Data
    top_frauds = df[df["risk_level"] == "High"].sort_values("risk_score", ascending=False)
    table_data = []
    
    for _, row in top_frauds.iterrows():
        reasons = []
        if row["return_ratio"] >= 0.9: reasons.append("Critical return frequency.")
        elif row["return_ratio"] > 0.7: reasons.append("High return volume.")
        if row["avg_return_days"] <= 1: reasons.append("Immediate return cycle detected.")
        elif row["avg_return_days"] < 3: reasons.append("Short-term return pattern.")
        
        ai_justification = " | ".join(reasons[:2]) if reasons else "Pattern matches known fraud profile."
        policy_recommendation = "Apply 5% Risk Premium surcharge on next transaction value."

        table_data.append({
            "id": str(row.get("customer_id", "Unknown")),
            "price": f"₹{float(row.get('total_purchase_value', 0)):,.2f}",
            "window": str(int(row.get('avg_return_days', 0))),
            "score": int(row.get('risk_score', 0)),
            "status": "Flagged",
            "reason": ai_justification,
            "usp_policy": policy_recommendation 
        })

    return jsonify({
        "metrics": metrics,
        "charts": charts,
        "table_data": table_data
    })

@app.route("/download-report")
def download_report():
    """Allows downloading the full AI-processed report."""
    output_path = os.path.join(UPLOAD_FOLDER, "output.csv")
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    return jsonify({"error": "No report found."}), 404

if __name__ == "__main__":
    # REQUIRED: Bind to 0.0.0.0 and dynamic PORT for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)