from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
    percent_salary_hike = Column(Float)
    job_satisfaction = Column(Integer)
    work_life_balance = Column(Integer)
    job_involvement = Column(Integer)
    environment_satisfaction = Column(Integer)
    performance_rating = Column(Integer)
    overtime = Column(String)
    predicted_score = Column(Float)

