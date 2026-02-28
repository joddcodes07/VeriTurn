# VeriTurn: Explainable Returns Fraud Detection Dashboard

**One-line project description:** An AI-powered dashboard that detects e-commerce return fraud using anomaly detection while providing human-readable, explainable risk scores.

## 1. Problem Statement
* **Problem Title:** Returns Fraud Detection Dashboard
* **Problem Description:** E-commerce platforms face growing financial losses due to fraudulent return behaviors like serial returning, wardrobing, and receipt manipulation. Manual detection is impossible due to transaction volume, and basic rule-based systems fail to catch evolving fraud patterns.
* **Target Users:** E-commerce Trust & Safety Teams, Fraud Analysts, and Store Operations Managers.
* **Existing Gaps:** Current systems lack structured, explainable anomaly detection. They struggle with handling imbalanced datasets, suffer from high false-positive rates (flagging honest customers), and fail to explain *why* a specific user is flagged.

## 2. Problem Understanding & Approach
* **Root Cause Analysis:** Fraudsters constantly change tactics, rendering static rules obsolete. Furthermore, standard ML models act as "black boxes," making it hard for human reviewers to trust the system or justify action against a customer.
* **Solution Strategy:** We use unsupervised machine learning (Anomaly Detection) to find behavioral outliers rather than relying on predefined rules. To build trust, we integrate an Explainable AI (XAI) layer that translates complex mathematical outputs into plain-English reasons for the fraud analyst.

## 3. Proposed Solution
* **Solution Overview:** VeriTurn is a web-based dashboard that ingests transaction and return logs, processes them through a machine learning pipeline to detect anomalies, and visualizes high-risk users.
* **Core Idea:** Combine anomaly detection with explainability to strengthen return fraud management while balancing sensitivity and fairness.
* **Key Features:**
    * Automated ingestion of transaction/return logs.
    * Dynamic Risk Scoring (0-100 scale).
    * Explainable AI reasoning (e.g., "Flagged due to 3 returns of high-value items within 24 hours").
    * Interactive dashboard to view behavioral clusters.

## 4. System Architecture
* **High-Level Flow:** Transaction Logs uploaded → Python Backend processes data → ML Model scores data & generates explanations → API sends JSON to Frontend → JavaScript Dashboard renders UI.
* **Architecture Description:** A lightweight vanilla JS frontend communicating via Fetch API to a FastAPI backend. The backend hosts a scikit-learn anomaly detection model and an explainer to generate the risk analysis.
* **Architecture Diagram:** *(To be added during development)*

## 5. Database Design
* **ER Diagram & Description:** *(Using a lightweight local structure for hackathon development; full ER diagram to be added if expanding to PostgreSQL/MySQL).*

## 6. Dataset Selected
* **Dataset Name:** Synthetic E-commerce Returns Log
* **Source:** Generated via custom Python script mimicking real-world behaviors.
* **Data Type:** Tabular (CSV) containing User ID, Purchase Date, Return Date, Item Category, Item Price, Return Reason.
* **Selection Reason:** Real-world fraud data is highly proprietary. We are generating a tailored dataset that accurately mimics "wardrobing" and "serial returner" behaviors to train the model properly.
* **Preprocessing Steps:** Encoding categorical variables, feature engineering (calculating days between purchase and return), and applying techniques to handle dataset imbalance.

## 7. Model Selected
* **Model Name:** Isolation Forest (with SHAP/Rule-based Explainability)
* **Selection Reasoning:** Isolation Forests are highly effective at isolating anomalies in large datasets without needing perfectly labeled training data. 
* **Alternatives Considered:** XGBoost (requires strictly labeled data), standard rule-based engine (too rigid).
* **Evaluation Metrics:** Precision (to minimize banning honest users), Recall (to catch as much fraud as possible), and F1-Score.

## 8. Technology Stack
* **Frontend:** HTML5, CSS3, Vanilla JavaScript.
* **Backend:** Python (FastAPI).
* **ML/AI:** scikit-learn, Pandas.
* **Database:** Local JSON/CSV / SQLite.
* **Deployment:** Localhost (TBD for final deployment).

## 9. API Documentation & Testing
**API Endpoints List (Draft):**
* `POST /api/upload_logs`: Ingests new CSV/JSON transaction data.
* `GET /api/risk_scores`: Returns a list of users and their calculated anomaly risk score.
* `GET /api/explain_flag/{user_id}`: Returns the specific text explanation of why a user was flagged.

## 10. Module-wise Development & Deliverables
* **Checkpoint 1: Research & Planning** - README creation, Architecture definition. *(Completed)*
* **Checkpoint 2: Backend Development** - Setup Python environment, create base API routes.
* **Checkpoint 3: Frontend Development** - Build UI layout, connect JS Fetch calls.
* **Checkpoint 4: Model Training** - Train Isolation Forest on dataset.
* **Checkpoint 5: Model Integration** - Link ML model to backend API.
* **Checkpoint 6: Deployment** - Final integration testing.

## 11. End-to-End Workflow
1. Admin uploads latest transaction logs.
2. Backend parses data and feeds it to the ML model.
3. Model scores each user and identifies anomalies.
4. Explainer module generates human-readable reasons for flagged users.
5. Dashboard updates to show High, Medium, and Low-risk customers.

## 12. Demo & Video
* **Live Demo Link:** *(TBD)*
* **Demo Video Link:** *(TBD)*
* **GitHub Repository:** *(Link will be added upon submission)*

## 13. Hackathon Deliverables Summary
* [x] Checkpoint 1 README
* [ ] Functional Backend
* [ ] Interactive Frontend Dashboard
* [ ] Integrated ML Model
* [ ] Final Demo

## 14. Team Roles & Responsibilities
* **Mehran Ansari** | ML/Backend Developer | Model training, API creation, Python logic.
* **Yashpal Singh** | Frontend Developer | UI/UX design, JavaScript integration.
* **Naman Katyal** | Frontend Developer | UI/UX design, JavaScript integration.

## 15. Future Scope & Scalability
* **Short-Term:** Integrate an LLM to generate highly conversational, plain-English summaries of the fraud risk.
* **Long-Term:** Connect directly to live payment gateways (Stripe/Shopify) for real-time transaction blocking.

## 16. Known Limitations
* The model may initially struggle with entirely new, unseen fraud patterns until the dataset is updated.

## 17. Impact
By shifting from rigid rules to explainable AI, e-commerce platforms can drastically reduce financial losses from serial returners while protecting honest customers, maintaining brand trust.