# api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from ml_model.preprocess import preprocess_input
from ml_model.preprocess import load_model 
from database import crud
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow Streamlit to call FastAPI
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model and preprocessors
model, encoders, scaler = load_model()

class PredictionRequest(BaseModel):
    Age: int
    Gender: str
    JobRole: str
    JobSatisfaction: int
    MonthlyIncome: float

@app.post("/predict")
def predict(request: PredictionRequest):
    df = pd.DataFrame([request.dict()])
    X = preprocess_input(df, encoders, scaler)
    prediction = model.predict(X)[0]
    crud.save_prediction(df, prediction)
    return {"prediction": int(prediction)}

@app.get("/predictions")
def get_past_predictions():
    predictions = crud.get_predictions()
    result = [p.__dict__ for p in predictions]
    for item in result:
        item.pop("_sa_instance_state", None)
    return JSONResponse(content=result)
