# api/ml_model/preprocess.py
import pandas as pd
import joblib
import os

def load_model():
    model = joblib.load("ml_model/model.pkl")
    encoders = joblib.load("ml_model/encoders.pkl")
    scaler = joblib.load("ml_model/scaler.pkl")
    return model, encoders, scaler

def preprocess_input(df, encoders, scaler):
    cat_cols = encoders.keys()
    for col in cat_cols:
        df[col] = encoders[col].transform(df[col])
    df_scaled = scaler.transform(df)
    return df_scaled
