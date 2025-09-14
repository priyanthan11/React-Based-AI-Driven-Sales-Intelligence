# backend/main.py
from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/deals")
def get_deals():
    df = pd.read_csv("./data/raw/sales_pipeline.csv")
    return df.to_dict(orient="records")
