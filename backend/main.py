import os
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import Recommendation, ValidationWarning
from analytics.recommendations import generate_recommendations
from analytics.validation import validate_data

app = FastAPI(title="E-commerce Business Decision Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.normpath(os.path.join(BASE_DIR, 'data', 'sample_orders.csv'))

def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {CSV_PATH}. Run 'python data/generate_sample.py' first."
        )
    return pd.read_csv(CSV_PATH)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/recommendations", response_model=list[Recommendation])
def get_recommendations(priority: str = None):
    df = load_data()
    recs = generate_recommendations(df)
    if priority:
        recs = [r for r in recs if r['priority'].upper() == priority.upper()]
    return recs

@app.get("/data-quality", response_model=list[ValidationWarning])
def get_data_quality():
    df = load_data()
    return validate_data(df)