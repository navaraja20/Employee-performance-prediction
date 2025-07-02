# streamlit_app/utils.py

import requests
import pandas as pd

API_URL = "http://api:8000"

def predict_single(data: dict) -> dict:
    """Send a single prediction request to the FastAPI backend."""
    response = requests.post(f"{API_URL}/predict", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Prediction failed: {response.text}")

def predict_batch(df: pd.DataFrame) -> pd.DataFrame:
    """Send batch prediction requests row by row to FastAPI."""
    results = []
    for _, row in df.iterrows():
        try:
            result = predict_single(row.to_dict())
            row_result = row.to_dict()
            row_result["Prediction"] = result["prediction"]
            results.append(row_result)
        except Exception as e:
            print(f"Failed to predict row: {e}")
    return pd.DataFrame(results)

def fetch_past_predictions() -> pd.DataFrame:
    """Fetch stored predictions from FastAPI (served from PostgreSQL)."""
    response = requests.get(f"{API_URL}/predictions")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print("Failed to fetch predictions")
        return pd.DataFrame([])
