import streamlit as st
import pandas as pd
import requests

API_URL = "http://api:8001"

def predict_single(data):
       response = requests.post(f"{API_URL}/predict", json=data)
       if response.status_code == 200:
           return response.json()
       else:
           st.error("Error making prediction")
           return None

def predict_multiple(file):
       df = pd.read_csv(file)
       data = df.to_dict(orient='records')
       response = requests.post(f"{API_URL}/predict", json=data)
       if response.status_code == 200:
           return response.json()
       else:
           st.error("Error making predictions")
           return None

st.header("Prediction")
st.subheader("Single Prediction")
with st.form("single_prediction"):
       age = st.number_input("Age", min_value=18, max_value=100, value=30)
       business_travel = st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
       department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
       education = st.selectbox("Education", [1, 2, 3, 4, 5])
       gender = st.selectbox("Gender", ["Male", "Female"])
       hourly_rate = st.number_input("Hourly Rate", min_value=0, value=50)
       job_involvement = st.selectbox("Job Involvement", [1, 2, 3, 4])
       job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])
       job_role = st.selectbox("Job Role", ["Sales Executive", "Research Scientist", "Laboratory Technician", "Manufacturing Director", "Healthcare Representative", "Manager", "Sales Representative", "Research Director", "Human Resources"])
       job_satisfaction = st.selectbox("Job Satisfaction", [1, 2, 3, 4])
       marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
       monthly_income = st.number_input("Monthly Income", min_value=0, value=5000)
       overtime = st.selectbox("Overtime", ["Yes", "No"])
       total_working_years = st.number_input("Total Working Years", min_value=0, value=10)
       work_life_balance = st.selectbox("Work Life Balance", [1, 2, 3, 4])
       years_at_company = st.number_input("Years at Company", min_value=0, value=5)
       years_in_current_role = st.number_input("Years in Current Role", min_value=0, value=3)
       years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, value=1)

       submitted = st.form_submit_button("Predict")
       if submitted:
           data = {
               "Age": age, "BusinessTravel": business_travel, "Department": department,
                "Education": education, "Gender": gender, "HourlyRate": hourly_rate,
               "JobInvolvement": job_involvement, "JobLevel": job_level, "JobRole": job_role,
               "JobSatisfaction": job_satisfaction, "MaritalStatus": marital_status, "MonthlyIncome": monthly_income,
               "OverTime": overtime, "TotalWorkingYears": total_working_years,
               "WorkLifeBalance": work_life_balance, "YearsAtCompany": years_at_company,
               "YearsInCurrentRole": years_in_current_role, "YearsSinceLastPromotion": years_since_last_promotion,
           }
           result = predict_single([data])
           if result:
               result_df = pd.DataFrame(result)
               st.write("Prediction Result:")
               st.dataframe(result_df)

st.subheader("Multiple Predictions")
uploaded_file = st.file_uploader("Upload CSV for Multiple Predictions", type=["csv"])
if uploaded_file:
       if st.button("Predict Multiple"):
           result = predict_multiple(uploaded_file)
           if result:
               result_df = pd.DataFrame(result)
               st.write("Prediction Results:")
               st.dataframe(result_df)