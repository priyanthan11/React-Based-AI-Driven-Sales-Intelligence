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

Future Improvements

- Batch prediction via CSV uploads
- Real-time model retraining with new sales data
- Advanced feature engineering (seasonality, agent trends)
- Dashboard analytics with charts for deals over time
