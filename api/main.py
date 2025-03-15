from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Base, engine
from models import Prediction
import pickle
import os

# Load ML model
MODEL_PATH = "model.pkl"
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Initialize FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Pydantic schema for request validation
class EmployeeInput(BaseModel):
    age: int
    experience: int
    department: str
    education: str

# Prediction endpoint
@app.post("/predict")
def predict(employee: EmployeeInput, db: Session = Depends(get_db)):
    features = [[employee.age, employee.experience]]
    prediction = model.predict(features)[0]

    new_prediction = Prediction(
        age=employee.age,
        experience=employee.experience,
        department=employee.department,
        education=employee.education,
        performance_score=prediction
    )
    db.add(new_prediction)
    db.commit()
    return {"prediction": prediction}

# Fetch past predictions
@app.get("/past-predictions")
def get_past_predictions(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).all()
    return predictions
