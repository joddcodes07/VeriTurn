# VeriTurn: Explainable Returns Fraud Detection Dashboard

**One-line project description:** An AI-powered dashboard that detects e-commerce return fraud using anomaly detection while providing human-readable, explainable risk scores.

## 1. Problem Statement
* **Problem Title:** Returns Fraud Detection Dashboard
* **Problem Description:** E-commerce platforms face growing financial losses due to fraudulent return behaviors like serial returning, wardrobing, and receipt manipulation. Manual detection is impossible due to transaction volume, and basic rule-based systems fail to catch evolving fraud patterns.
* **Target Users:** E-commerce Trust & Safety Teams, Fraud Analysts, and Store Operations Managers.
* **Existing Gaps:** Current systems lack structured, explainable anomaly detection. They struggle with handling imbalanced datasets, suffer from high false-positive rates, and fail to explain *why* a specific user is flagged.

## 2. Problem Understanding & Approach
* **Root Cause Analysis:** Fraudsters constantly change tactics, rendering static rules obsolete. Furthermore, standard ML models act as "black boxes," making it hard for human reviewers to trust the system.
* **Solution Strategy:** We use unsupervised machine learning (Anomaly Detection) to find behavioral outliers rather than relying on predefined rules. We integrate an Explainable AI (XAI) layer that translates complex mathematical outputs into plain-English reasons.

## 3. Proposed Solution
* **Solution Overview:** VeriTurn is a web-based dashboard that ingests transaction logs, processes them through a machine learning pipeline, and visualizes high-risk users.
* **Core Idea:** Combine anomaly detection with explainability to strengthen return fraud management while balancing sensitivity and fairness.
* **Key Features:**
    * Automated ingestion of transaction/return logs.
    * Dynamic Risk Scoring (0-100 scale).
    * Explainable AI reasoning (e.g., "Critical return frequency" or "Immediate return cycle detected").
    * Interactive dashboard to view behavioral clusters.

## 4. System Architecture
* **High-Level Flow:** Transaction Logs uploaded → Python Backend processes data → ML Model scores data & generates explanations → API sends JSON to Frontend → JavaScript Dashboard renders UI.
* **Architecture Description:** A lightweight vanilla JS frontend communicating via Fetch API to a **Flask** backend. The backend hosts a scikit-learn anomaly detection model and an automated reasoning engine.

## 5. Database Design
* **Description:** VeriTurn utilizes a stateless file-based processing system. Uploaded CSVs are stored temporarily in an `uploads/` directory, processed into an `output.csv`, and then served as JSON data to the frontend.

## 6. Dataset Selected
* **Dataset Name:** Synthetic E-commerce Returns Log
* **Source:** Generated via custom Python script mimicking real-world behaviors.
* **Data Type:** Tabular (CSV) containing Customer ID, Purchase Date, Return Date, Total Purchase Value, and Return Status.
* **Selection Reason:** Real-world fraud data is highly proprietary. We generated a tailored dataset that accurately mimics "wardrobing" and "serial returner" behaviors.
* **Preprocessing Steps:** Feature engineering (calculating return ratios and return windows) and datetime normalization.

## 7. Model Selected
* **Model Name:** Isolation Forest (Anomaly Detection) with KMeans (Behavioral Clustering).
* **Selection Reasoning:** Isolation Forests are highly effective at isolating anomalies without needing perfectly labeled training data. KMeans segments behavioral patterns for visualization.
* **Evaluation Metrics:** Precision (to minimize flagging honest users), Recall (to catch as much fraud as possible), and F1-Score.

## 8. Technology Stack
* **Frontend:** HTML5, CSS3, Vanilla JavaScript.
* **Backend:** Python (**Flask** / **Gunicorn**).
* **ML/AI:** scikit-learn, Pandas, Matplotlib.
* **Hosting:** **Vercel** (Frontend) and **Render** (Backend).

## 9. VeriTurn USP Policy: Risk Premium Surcharge
* **Policy Overview:** To mitigate financial impact without banning customers, VeriTurn implements a "Risk Premium Surcharge".
* **Implementation:** High-risk users identified by the AI are recommended for a **5% surcharge** on their next transaction. This acts as a deterrent for serial returners while allowing the platform to recover operational losses from restocking fees.

## 10. API Documentation
* **`POST /upload`**: Ingests new CSV transaction data, runs the ML model, and returns metrics and flagged users.
* **`GET /static/charts/<filename>`**: Serves the AI-generated behavioral clustering and risk distribution graphs.
* **`GET /download-report`**: Provides a downloadable AI-processed CSV with detailed risk scores for every customer.

## 11. Module-wise Development & Deliverables
* **Checkpoint 1: Research & Planning** - README creation, Architecture definition. *(Completed)*
* **Checkpoint 2: Backend Development** - Setup Flask environment and CORS handling. *(Completed)*
* **Checkpoint 3: Frontend Development** - Build UI layout and JS Fetch integration. *(Completed)*
* **Checkpoint 4: Model Training** - Train Isolation Forest on synthetic dataset. *(Completed)*
* **Checkpoint 5: Model Integration** - Link ML model to Flask API and Matplotlib. *(Completed)*
* **Checkpoint 6: Deployment** - Deploy live to Vercel and Render. *(Completed)*

## 12. End-to-End Workflow
1. Admin uploads latest transaction logs via the Data Ingestion Portal.
2. Backend parses data and feeds it to the ML model.
3. Model scores each user and identifies behavioral anomalies.
4. Explainer module generates human-readable reasons (e.g., "Critical return frequency").
5. Dashboard updates to show monthly revenue loss, flagged anomalies, and policy recommendations.

## 13. Demo & Video
* **Live Demo Link:** https://veri-turn.vercel.app/
* **Demo Video Link:** [Google Drive Link](https://drive.google.com/file/d/1lgLO-KViJoKrn1ipxSnG_rwE2k4pJlGA/view?usp=drive_link)
* **GitHub Repository:** https://github.com/joddcodes07/VeriTurn.git
* **Powerpoint Presentation Link:** [Google Drive Link](https://drive.google.com/drive/folders/1Mh4FpW-31sVmxKNWG-h2_pfO0j8U1kwJ?usp=drive_link)

## 14. Hackathon Deliverables Summary
* [x] Checkpoint 1 README
* [x] Functional Flask Backend
* [x] Interactive Frontend Dashboard
* [x] Integrated ML Model
* [x] Live Deployment

## 15. Team Roles & Responsibilities
* **Mehran Ansari** | ML/Backend Developer | Model training, API creation, Python logic.
* **Yashpal Singh** | Synthetic data generation | Data implementation in the application.
* **Naman Katyal** | Frontend Developer | UI/UX design, JavaScript integration.

## 16. Future Scope & Scalability
* **Short-Term:** Integrate an LLM to generate highly conversational summaries of fraud risk.
* **Long-Term:** Connect directly to live payment gateways for real-time transaction blocking.

## 17. Impact
By shifting from rigid rules to explainable AI, platforms can reduce financial losses from serial returners while protecting honest customers, maintaining brand trust.