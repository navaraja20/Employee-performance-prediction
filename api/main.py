# api/main.py
from fastapi import FastAPI, HTTPException
from models.schemas import PredictionRequest
from database.db import SessionLocal, engine
from database import models, crud
from ml_model.preprocess import preprocess_input, load_model
import pandas as pd

app = FastAPI()

# Initialize DB
models.Base.metadata.create_all(bind=engine)
model, encoders, scaler = load_model()

@app.post("/predict")
def predict(data: PredictionRequest):
    try:
        df = pd.DataFrame([data.dict()])
        X = preprocess_input(df, encoders, scaler)
        prediction = model.predict(X)[0]
        crud.save_prediction(df, prediction)
        return {"prediction": prediction, "features": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/past-predictions")
def past_predictions():
    return crud.get_all_predictions()
