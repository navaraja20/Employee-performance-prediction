# streamlit_app/app.py

import streamlit as st
import pandas as pd
from utils import predict_single, predict_batch, fetch_past_predictions

st.set_page_config(page_title="Employee Performance Predictor", layout="wide")
st.title("Employee Attrition Prediction System")

option = st.radio("Choose Mode:", ["Single Prediction", "Batch Prediction", "Past Predictions"])

if option == "Single Prediction":
    st.subheader("🧍 Enter Employee Details")
    with st.form("single_form"):
        age = st.number_input("Age", min_value=18, max_value=65, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        job_role = st.text_input("Job Role")
        job_satisfaction = st.slider("Job Satisfaction", 1, 4, 3)
        income = st.number_input("Monthly Income", min_value=1000, value=5000)
        submit = st.form_submit_button("Predict")

    if submit:
        data = {
            "Age": age,
            "Gender": gender,
            "JobRole": job_role,
            "JobSatisfaction": job_satisfaction,
            "MonthlyIncome": income
        }
        try:
            result = predict_single(data)
            prediction = result["prediction"]
            st.success(f"Prediction: {'Yes' if prediction == 1 else 'No'}")
        except Exception as e:
            st.error(f"Error: {e}")

elif option == "Batch Prediction":
    st.subheader("Upload CSV File")
    file = st.file_uploader("Choose a file", type="csv")
    if file:
        df = pd.read_csv(file)
        st.write("Input Preview:", df.head())
        if st.button("Run Batch Prediction"):
            try:
                results_df = predict_batch(df)
                st.success("Batch prediction complete!")
                st.dataframe(results_df)
            except Exception as e:
                st.error(f"Error: {e}")

elif option == "Past Predictions":
    st.subheader("Historical Predictions")
    df = fetch_past_predictions()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No predictions logged yet.")
