from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    response = client.post("/predict", json={
        "age": 30, "gender": "Male", "marital_status": "Single",
        "job_role": "Engineer", "department": "IT", "business_travel": "Rarely",
        "years_at_company": 5, "total_working_years": 10, "years_in_current_role": 3,
        "years_since_last_promotion": 1, "monthly_income": 5000, "hourly_rate": 50,
        "stock_option_level": 2, "percent_salary_hike": 10, "job_satisfaction": 3,
        "work_life_balance": 3, "job_involvement": 3, "environment_satisfaction": 3,
        "performance_rating": 4, "overtime": "No"
    })
    assert response.status_code == 200
    assert "performance_score" in response.json()
