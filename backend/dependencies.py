from fastapi import HTTPException

def validate_input(data: dict):
    required_fields = [
        "age", "gender", "marital_status", "job_role", "department", "business_travel",
        "years_at_company", "total_working_years", "years_in_current_role", "years_since_last_promotion",
        "monthly_income", "hourly_rate", "stock_option_level", "percent_salary_hike",
        "job_satisfaction", "work_life_balance", "job_involvement", "environment_satisfaction",
        "performance_rating", "overtime"
    ]
    
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
