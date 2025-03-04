import streamlit as st
import requests

# FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"

# Title
st.title("Employee Performance Prediction")

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ["Predict", "Past Predictions"])

# ------------------- PREDICTION PAGE -------------------
if page == "Predict":
    st.header("Enter Employee Details")

    # Personal information
    st.subheader("Demographics")
    name = st.text_input("Employee Name")  
    age = st.number_input("Age", min_value=18, max_value=65, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])

    # Job & Work Experience
    st.subheader("Job & Work Experience")
    job_role = st.selectbox("Job Role", ["Manager", "Engineer", "Technician", "HR", "Sales", "Other"])
    department = st.selectbox("Department", ["IT", "HR", "Finance", "Sales", "Marketing", "Operations"])
    business_travel = st.selectbox("Business Travel", ["Rarely", "Frequently", "Never"])
    years_at_company = st.number_input("Years at Company", min_value=0, max_value=50, value=5)
    total_working_years = st.number_input("Total Working Years", min_value=0, max_value=50, value=10)
    years_in_current_role = st.number_input("Years in Current Role", min_value=0, max_value=30, value=3)
    years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, max_value=20, value=1)

    # Compensation & Benefits
    st.subheader("Compensation & Benefits")
    monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=50000, value=5000)
    hourly_rate = st.number_input("Hourly Rate ($)", min_value=10, max_value=500, value=50)
    stock_option_level = st.selectbox("Stock Option Level", [0, 1, 2, 3])
    percent_salary_hike = st.number_input("Percent Salary Hike", min_value=0, max_value=100, value=10)

    # Work-Life Balance & Satisfaction
    st.subheader("Work-Life Balance & Satisfaction")
    job_satisfaction = st.slider("Job Satisfaction", 1, 5, 3)
    work_life_balance = st.slider("Work-Life Balance", 1, 5, 3)
    job_involvement = st.slider("Job Involvement", 1, 5, 3)
    environment_satisfaction = st.slider("Environment Satisfaction", 1, 5, 3)

    # Performance & Attrition
    st.subheader("Performance & Attrition")
    performance_rating = st.selectbox("Performance Rating", [1, 2, 3, 4, 5])
    overtime = st.selectbox("OverTime", ["Yes", "No"])

    # Submit Button
    if st.button("Predict"):
        # Prepare request payload
        data = {
            "age": age,
            "gender": gender,
            "marital_status": marital_status,
            "job_role": job_role,
            "department": department,
            "business_travel": business_travel,
            "years_at_company": years_at_company,
            "total_working_years": total_working_years,
            "years_in_current_role": years_in_current_role,
            "years_since_last_promotion": years_since_last_promotion,
            "monthly_income": monthly_income,
            "hourly_rate": hourly_rate,
            "stock_option_level": stock_option_level,
            "percent_salary_hike": percent_salary_hike,
            "job_satisfaction": job_satisfaction,
            "work_life_balance": work_life_balance,
            "job_involvement": job_involvement,
            "environment_satisfaction": environment_satisfaction,
            "performance_rating": performance_rating,
            "overtime": overtime
        }

        # Send POST request to FastAPI
        response = requests.post(f"{FASTAPI_URL}/predict", json=data)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Performance Score: {result['performance_score']}")
        else:
            st.error("Error: Could not fetch prediction. Please try again.")

# ------------------- PAST PREDICTIONS PAGE -------------------
elif page == "Past Predictions":
    st.header("Past Predictions")

    # Fetch past predictions from FastAPI
    response = requests.get(f"{FASTAPI_URL}/past-predictions")

    if response.status_code == 200:
        predictions = response.json()
        if predictions:
            st.write(predictions)
        else:
            st.warning("No past predictions found.")
    else:
        st.error("Error fetching past predictions. Please try again.")
