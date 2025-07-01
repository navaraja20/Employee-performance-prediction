# streamlit_app/app.py
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Employee Attrition Prediction", layout="wide")
st.title("Employee Attrition Predictor")

option = st.radio("Choose Prediction Mode:", ["Single Prediction", "Batch Prediction"])

if option == "Single Prediction":
    st.subheader("Enter Employee Information")
    input_data = {
        "Age": st.number_input("Age", 18, 65, 30),
        "BusinessTravel": st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"]),
        "DailyRate": st.number_input("Daily Rate", 100, 1500, 800),
        "Department": st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"]),
        "DistanceFromHome": st.slider("Distance From Home", 1, 30, 5),
        "Education": st.slider("Education Level", 1, 5, 3),
        "EducationField": st.selectbox("Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"]),
        "EnvironmentSatisfaction": st.slider("Environment Satisfaction", 1, 4, 3),
        "Gender": st.radio("Gender", ["Male", "Female"]),
        "HourlyRate": st.number_input("Hourly Rate", 30, 150, 60),
        "JobInvolvement": st.slider("Job Involvement", 1, 4, 3),
        "JobLevel": st.slider("Job Level", 1, 5, 2),
        "JobRole": st.selectbox("Job Role", ["Sales Executive", "Research Scientist", "Laboratory Technician", "Manufacturing Director", "Healthcare Representative", "Manager", "Sales Representative", "Research Director", "Human Resources"]),
        "JobSatisfaction": st.slider("Job Satisfaction", 1, 4, 3),
        "MaritalStatus": st.selectbox("Marital Status", ["Single", "Married", "Divorced"]),
        "MonthlyIncome": st.number_input("Monthly Income", 1000, 20000, 5000),
        "MonthlyRate": st.number_input("Monthly Rate", 100, 15000, 6000),
        "NumCompaniesWorked": st.slider("Number of Companies Worked", 0, 10, 1),
        "OverTime": st.radio("OverTime", ["Yes", "No"]),
        "PercentSalaryHike": st.slider("Percent Salary Hike", 10, 25, 15),
        "PerformanceRating": st.slider("Performance Rating", 1, 4, 3),
        "RelationshipSatisfaction": st.slider("Relationship Satisfaction", 1, 4, 3),
        "StockOptionLevel": st.slider("Stock Option Level", 0, 3, 1),
        "TotalWorkingYears": st.slider("Total Working Years", 0, 40, 10),
        "TrainingTimesLastYear": st.slider("Training Times Last Year", 0, 6, 3),
        "WorkLifeBalance": st.slider("Work Life Balance", 1, 4, 3),
        "YearsAtCompany": st.slider("Years At Company", 0, 40, 5),
        "YearsInCurrentRole": st.slider("Years In Current Role", 0, 18, 5),
        "YearsSinceLastPromotion": st.slider("Years Since Last Promotion", 0, 15, 1),
        "YearsWithCurrManager": st.slider("Years With Current Manager", 0, 17, 4),
    }

    if st.button("Predict"):
        response = requests.post("http://api:8000/predict", json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction: {'Attrition' if result['prediction'] == 1 else 'No Attrition'}")
            st.dataframe(pd.DataFrame(result['features']))
        else:
            st.error("Prediction failed.")

else:
    st.subheader("Upload CSV for Batch Prediction")
    file = st.file_uploader("Upload a CSV file", type=["csv"])

    if file and st.button("Predict Batch"):
        df = pd.read_csv(file)
        predictions = []
        for _, row in df.iterrows():
            response = requests.post("http://api:8000/predict", json=row.to_dict())
            if response.status_code == 200:
                result = response.json()
                row_result = row.to_dict()
                row_result["Prediction"] = result["prediction"]
                predictions.append(row_result)
        st.dataframe(pd.DataFrame(predictions))
