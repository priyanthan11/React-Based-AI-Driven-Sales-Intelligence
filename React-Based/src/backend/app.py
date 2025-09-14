from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load trained model
model_path = "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/models/xgb_sales_model.pkl"
model = joblib.load(model_path)

app = FastAPI(title="Sales Win Probablility API")

# Define request schema

FEATURE_COLUMNS = joblib.load(
    "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/models/feature_columns.pkl")


class DealRequest(BaseModel):
    opportunity_id: str
    features: dict  # expects keys = trained feature colums

# Predict endpoint


@app.post("/predict_deal")
def predict_deal(request: DealRequest):
    # Convert features dict to Dataframe
    X = pd.DataFrame([request.features])

    # Add missing column order as training
    for col in FEATURE_COLUMNS:
        if col not in X.columns:
            X[col] = 0

    # Ensure same column order as trainig
    X = X[FEATURE_COLUMNS]

    # Predict probability
    win_prob = model.predict_proba(X)[0, 1]

    return {
        "opportunity_id": request.opportunity_id,
        "win_probability": round(float(win_prob), 4)
    }

# Health check


@app.get("/health")
def health_check():
    return {"status": "ok"}
