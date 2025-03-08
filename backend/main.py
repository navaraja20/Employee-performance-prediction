from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Prediction
from schemas import PredictionRequest, BatchPredictionRequest
from datetime import datetime
from typing import List
import os

app = FastAPI()

# Load the trained model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This gets `/app`
MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.pkl")  # `/app/ml/model.pkl`

# Load model
model = joblib.load(MODEL_PATH)
# Database Configuration
DATABASE_URL = "postgresql+psycopg2://postgres:password@postgres_db:5432/employee_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Ensure tables exist
Base.metadata.create_all(bind=engine)

@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        df = pd.DataFrame([request.features])
        expected_features = ["Age", "MonthlyIncome", "JobSatisfaction", "JobRole", 
                             "YearsAtCompany", "WorkLifeBalance", "OverTime", "Education"]
        df = df[expected_features]

        prediction = model.predict(df)

        db = SessionLocal()
        db_prediction = Prediction(
            prediction=str(prediction[0]),
            features=str(request.features),
            source="webapp"
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        db.close()

        return {"prediction": prediction[0], "features": request.features}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict-batch")
async def predict_batch(request: BatchPredictionRequest):
    try:
        df = pd.DataFrame(request.data)
        expected_features = ["Age", "MonthlyIncome", "JobSatisfaction", "JobRole", 
                             "YearsAtCompany", "WorkLifeBalance", "OverTime", "Education"]
        df = df[expected_features]

        predictions = model.predict(df)

        db = SessionLocal()
        for i in range(len(df)):
            db_prediction = Prediction(
                prediction=str(predictions[i]),
                features=str(request.data[i]),
                source="webapp"
            )
            db.add(db_prediction)
        db.commit()
        db.close()

        return {"predictions": predictions.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/past-predictions")
async def past_predictions():
    try:
        db = SessionLocal()
        predictions = db.query(Prediction).all()
        db.close()
        return [
            {
                "id": p.id,
                "prediction": p.prediction,
                "features": p.features,
                "timestamp": p.timestamp,
                "source": p.source
            }
            for p in predictions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
