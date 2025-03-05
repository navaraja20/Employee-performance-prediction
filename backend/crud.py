from sqlalchemy.orm import Session
from models import EmployeePrediction
from schemas import EmployeeInput

def save_prediction(db: Session, employee_data: EmployeeInput, predicted_score: float):
    prediction = EmployeePrediction(
        name=employee_data.name,
        age=employee_data.age,
        gender=employee_data.gender,
        marital_status=employee_data.marital_status,
        job_role=employee_data.job_role,
        department=employee_data.department,
        business_travel=employee_data.business_travel,
        years_at_company=employee_data.years_at_company,
        total_working_years=employee_data.total_working_years,
        years_in_current_role=employee_data.years_in_current_role,
        years_since_last_promotion=employee_data.years_since_last_promotion,
        monthly_income=employee_data.monthly_income,
        hourly_rate=employee_data.hourly_rate,
        stock_option_level=employee_data.stock_option_level,
        percent_salary_hike=employee_data.percent_salary_hike,
        job_satisfaction=employee_data.job_satisfaction,
        work_life_balance=employee_data.work_life_balance,
        job_involvement=employee_data.job_involvement,
        environment_satisfaction=employee_data.environment_satisfaction,
        performance_rating=employee_data.performance_rating,
        overtime=employee_data.overtime,
        predicted_performance_score=predicted_score
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction

def get_past_predictions(db: Session):
    return db.query(EmployeePrediction).all()
