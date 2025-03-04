from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Allow frontend (Streamlit) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the frontend URL if deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database simulation (Replace with actual PostgreSQL connection later)
past_predictions = []

# Define the request data model
class EmployeeData(BaseModel):
    age: int
    gender: str
    marital_status: str
    job_role: str
    department: str
    business_travel: str
    years_at_company: int
    total_working_years: int
    years_in_current_role: int
    years_since_last_promotion: int
    monthly_income: float
    hourly_rate: float
    stock_option_level: int
    percent_salary_hike: int
    job_satisfaction: int
    work_life_balance: int
    job_involvement: int
    environment_satisfaction: int
    performance_rating: int
    overtime: str

# Dummy prediction function (Replace with ML model later)
def predict_performance(data: EmployeeData):
    return round(random.uniform(1, 5), 2)  # Simulated performance score between 1 and 5

# Prediction endpoint
@app.post("/predict")
def predict(data: EmployeeData):
    try:
        # Get prediction from the ML model (or dummy function for now)
        performance_score = predict_performance(data)

        # Save prediction to the database (simulated)
        prediction_record = {
            "employee_data": data.dict(),
            "performance_score": performance_score
        }
        past_predictions.append(prediction_record)

        return {"performance_score": performance_score}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retrieve past predictions
@app.get("/past-predictions")
def get_past_predictions():
    return past_predictions
