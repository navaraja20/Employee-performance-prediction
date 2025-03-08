import joblib
import pandas as pd
import os

# Load the trained model
MODEL_PATH = os.getenv("MODEL_PATH", "/ml/model.pkl")
model = joblib.load(MODEL_PATH)

def make_prediction(features: dict):
    """Takes input features as a dictionary and returns model prediction."""
    df = pd.DataFrame([features])
    prediction = model.predict(df)
    return prediction[0]
