from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Database configuration
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/employee_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class EmployeePrediction(Base):
    __tablename__ = "employee_predictions"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    marital_status = Column(String)
    job_role = Column(String)
    department = Column(String)
    business_travel = Column(String)
    years_at_company = Column(Integer)
    total_working_years = Column(Integer)
    years_in_current_role = Column(Integer)
    years_since_last_promotion = Column(Integer)
    monthly_income = Column(Float)
    hourly_rate = Column(Float)
    stock_option_level = Column(Integer)
    percent_salary_hike = Column(Integer)
    job_satisfaction = Column(Integer)
    work_life_balance = Column(Integer)
    job_involvement = Column(Integer)
    environment_satisfaction = Column(Integer)
    performance_rating = Column(Integer)
    overtime = Column(String)
    performance_score = Column(Float)

Base.metadata.create_all(bind=engine)

# Pydantic model for API requests
class EmployeeInput(BaseModel):
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

# FastAPI app
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/predict")
def predict_performance(employee: EmployeeInput, db: Session = Depends(get_db)):
    # Dummy prediction logic (replace with actual model later)
    performance_score = (employee.job_satisfaction + employee.work_life_balance) * 10

    # Save prediction to database
    prediction = EmployeePrediction(
        **employee.dict(), performance_score=performance_score
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return {"performance_score": performance_score}

@app.get("/past-predictions")
def get_past_predictions(db: Session = Depends(get_db)):
    predictions = db.query(EmployeePrediction).all()
    return predictions