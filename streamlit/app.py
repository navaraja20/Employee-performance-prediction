import streamlit as st
import pandas as pd
import requests

# FastAPI endpoint
API_URL = "http://api:8000"

st.set_page_config(page_title="Employee Performance Prediction", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Make Prediction", "Past Predictions"])

# Prediction Page
if page == "Make Prediction":
    st.title("Employee Performance Prediction")

    # Input form for single prediction
    st.header("Single Prediction")
    with st.form("prediction_form"):
        age = st.number_input("Age", min_value=18, max_value=65, step=1)
        experience = st.number_input("Experience (Years)", min_value=0, max_value=40, step=1)
        department = st.selectbox("Department", ["HR", "Engineering", "Sales", "Marketing", "Finance"])
        education = st.selectbox("Education", ["High School", "Bachelors", "Masters", "PhD"])
        submitted = st.form_submit_button("Predict")

    if submitted:
        data = {
            "age": age,
            "experience": experience,
            "department": department,
            "education": education
        }
        response = requests.post(f"{API_URL}/predict", json=data)

        if response.status_code == 200:
            prediction = response.json()["prediction"]
            st.success(f"Predicted Performance Score: {prediction:.2f}")
        else:
            st.error("Error in prediction. Please try again.")

    # File upload for bulk prediction
    st.header("Bulk Prediction")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if {"age", "experience", "department", "education"}.issubset(df.columns):
            st.write("Uploaded Data Preview:")
            st.dataframe(df)

            if st.button("Predict for File"):
                predictions = []
                for _, row in df.iterrows():
                    response = requests.post(f"{API_URL}/predict", json=row.to_dict())
                    if response.status_code == 200:
                        prediction = response.json()["prediction"]
                        predictions.append(prediction)
                    else:
                        predictions.append("Error")

                df["Predicted Performance Score"] = predictions
                st.write("Predictions:")
                st.dataframe(df)
        else:
            st.error("CSV file must contain columns: age, experience, department, education")

# Past Predictions Page
elif page == "Past Predictions":
    st.title("Past Predictions")
    
    # Fetch past predictions from API
    response = requests.get(f"{API_URL}/past-predictions")

    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            st.write("Past Predictions Data:")
            st.dataframe(df)
        else:
            st.warning("No past predictions found.")
    else:
        st.error("Error fetching past predictions. Please try again.")
