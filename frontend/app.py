import streamlit as st
import requests
import pandas as pd

API_URL = "http://backend:8000"

st.title("🏢 Employee Performance Prediction")

# Sidebar Navigation
page = st.sidebar.radio("📌 Select Page", ["📊 Make Predictions", "📜 Past Predictions"])

if page == "📊 Make Predictions":
    st.header("🎯 Make a Prediction")

    # Form for single sample prediction
    with st.form("single_prediction_form"):
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=20000, value=5000)
        job_satisfaction = st.selectbox("Job Satisfaction (1-4)", [1, 2, 3, 4])
        job_role = st.selectbox("Job Role", ["Sales Executive", "Manager", "Laboratory Technician", "Research Scientist", "Human Resources"])
        years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5)
        work_life_balance = st.selectbox("Work-Life Balance (1-4)", [1, 2, 3, 4])
        overtime = st.selectbox("Overtime", ["Yes", "No"])
        education_level = st.selectbox("Education Level", [1, 2, 3, 4, 5])  # 1 = Below College, 5 = Doctorate
        
        submit = st.form_submit_button("🚀 Predict")

    # Handle single prediction request
    if submit:
        input_data = {
            "features": {
                "Age": age,
                "MonthlyIncome": monthly_income,
                "JobSatisfaction": job_satisfaction,
                "JobRole": job_role,
                "YearsAtCompany": years_at_company,
                "WorkLifeBalance": work_life_balance,
                "OverTime": 1 if overtime == "Yes" else 0,  # Convert Yes/No to binary
                "Education": education_level
            }
        }

        response = requests.post(f"{API_URL}/predict", json=input_data)
        
        if response.status_code == 200:
            st.success(f"🎉 Prediction: {response.json()['prediction']}")
        else:
            st.error("❌ Prediction failed")

    # CSV Upload for Batch Predictions
    st.header("📂 Upload CSV for Bulk Prediction")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        response = requests.post(f"{API_URL}/predict-batch", json={"data": df.to_dict(orient="records")})
        
        if response.status_code == 200:
            st.write("✅ Predictions:", pd.DataFrame(response.json()["predictions"], columns=["Predictions"]))
        else:
            st.error("❌ Batch prediction failed")

elif page == "📜 Past Predictions":
    st.header("📊 Past Predictions")
    
    # Filters for past predictions
    start_date = st.date_input("📅 Start Date")
    end_date = st.date_input("📅 End Date")
    source = st.selectbox("📂 Prediction Source", ["All", "Webapp", "Scheduled Predictions"])
    
    response = requests.get(f"{API_URL}/past-predictions")
    
    if response.status_code == 200:
        predictions = response.json()
        df = pd.DataFrame(predictions)
        
        # Apply filtering
        if source != "All":
            df = df[df["source"] == source.lower()]
        
        st.write(df)
    else:
        st.error("❌ Failed to fetch past predictions")