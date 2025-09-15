from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np

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


@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
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


@app.post("/recommend_action")
def recommend_action(request: DealRequest):
    try:
        X = pd.DataFrame([request.features])

        # Align features
        for col in FEATURE_COLUMNS:
            if col not in X.columns:
                X[col] = 0
        X = X[FEATURE_COLUMNS]

        # Predict next-best-action
        action_score = model.predict_proba(X)[0]  # multi-class classifer
        best_idx = int(np.argmax(action_score))
        best_action = model.classes_[best_idx]
        confidence = float(action_score[best_idx])

        return {
            "opportunity_id": request.opportunity_id,
            "recommended_action": str(best_action),
            "confidence": round(confidence, 3)
        }
    except Exception as e:
        return {"error": str(e)}

# Health check


@app.get("/health")
def health_check():
    return {"status": "ok"}
