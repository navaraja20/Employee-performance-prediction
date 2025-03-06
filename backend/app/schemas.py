from pydantic import BaseModel

class EmployeeInput(BaseModel):
    name: str
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
    monthly_income: int
    hourly_rate: int
    stock_option_level: int
    percent_salary_hike: int
    job_satisfaction: int
    work_life_balance: int
    job_involvement: int
    environment_satisfaction: int
    performance_rating: int
    overtime: str

class EmployeePredictionResponse(BaseModel):
    performance_score: float
