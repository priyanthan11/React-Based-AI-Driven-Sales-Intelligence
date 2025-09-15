# 🚀 Sales Win Probability Predictor

A full-stack AI-driven application that predicts the probability of closing a sales deal based on historical data.  
The backend uses **FastAPI** to serve a trained machine learning model (XGBoost / LightGBM), and the frontend is built with **React** for an interactive deals dashboard.

---

## 🔹 Features

- Predict sales deal win probability in real-time
- Interactive React dashboard showing deals, sales agents, and products
- Color-coded risk bars for quick visualization
- Easily extensible backend for additional predictive models
- Batch prediction via CSV upload (planned)

---

## 🛠 Tech Stack

**Frontend:**

- React
- TypeScript
- Tailwind CSS

**Backend:**

- Python
- FastAPI
- Joblib (model serialization)

**Machine Learning:**

- XGBoost / LightGBM
- Pandas, NumPy
- Scikit-learn

---

## ⚡ Setup

### Backend

```bash
git clone <repo-url>
cd <repo-folder>/backend
pip install -r requirements.txt
```

Place the trained model in the models/ folder (e.g., xgb_sales_model.pkl)

Start FastAPI server:

```
uvicorn main:app --reload
```

React - based

```
cd ../frontend
npm install
npm start

```

- Open your browser at http://localhost:3000 to view the dashboard

📊 Usage

Each deal row shows: sales agent, product, account, deal stage, close value, and predicted win probability

Color-coded bars indicate high, medium, or low chances of winning a deal

🧠 Model Training

Features used:

- deal_stage, close_value, deal_duration_days
- Sales agent performance metrics
- Product categories

Pipeline:

- Clean and preprocess data with pandas
- Train XGBoost or LightGBM classifier
- Evaluate with accuracy, F1 score, ROC-AUC
- Serialize model with joblib for deployment

🔗 API Endpoints:
POST `/predict_deal` – Returns deal ID and predicted win probability

Request example:

```
{
  "opportunity_id": "12345",
  "sales_agent": "John Doe",
  "product": "GTX Basic",
  "account": "Acme Corp",
  "deal_stage": "Negotiation",
  "close_value": 50000
}
```

Response example:

```
{
  "opportunity_id": "12345",
  "win_probability": 0.72
}
```

![Dashboard Screenshot]("C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/assets/predction.png")
2️⃣ Recommend Next Best Action

POST /recommend_action – Returns the recommended action for the deal based on the model's prediction scores.

Request example:

```
{
  "opportunity_id": "12345",
  "features": {
    "deal_duration_days": 45,
    "engage_month": 10,
    "agent_total_deals": 20,
    "agent_win_rate": 0.75,
    "sales_agent_JohnDoe": 1,
    "product_XYZ": 1,
    "account_AcmeCorp": 1
  }
}

```

Response example:

```
{
  "opportunity_id": "12345",
  "recommended_action": "Follow-Up",
  "confidence": 0.83
}
```

- recommended_action: The next-best action to increase chances of winning the deal.
- confidence: The model’s confidence in this recommendation (0–1).
  Future Improvements

- Batch prediction via CSV uploads
- Real-time model retraining with new sales data
- Advanced feature engineering (seasonality, agent trends)
- Dashboard analytics with charts for deals over time

```

```
