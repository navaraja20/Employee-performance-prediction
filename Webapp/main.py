import streamlit as st
import pandas as pd
import requests
import datetime
import os
from io import StringIO

# API URLs from environment variables
PREDICTION_API_URL = os.getenv("PREDICTION_API_URL", "http://localhost:8000/predict")
PAST_PREDICTIONS_API_URL = os.getenv("PAST_PREDICTIONS_API_URL", "http://localhost:8000/past-predictions")

st.title("Employee Performance Prediction App")

# Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Go to", ["Prediction", "Past Predictions"])

def get_feature_inputs():
    st.subheader("Enter Employee Info for Prediction:")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=70, step=1)
    job_role = st.selectbox("Job Role", ["Education", "Media", "Healthcare", "Technology", "Finance"])
    monthly_income = st.number_input("Monthly Income", min_value=1000, max_value=20000, step=100)
    job_satisfaction = st.selectbox("Job Satisfaction", ["Low", "Medium", "High", "Very High"])

    features = {
        "Gender": gender,
        "Age": age,
        "JobRole": job_role,
        "MonthlyIncome": monthly_income,
        "JobSatisfaction": job_satisfaction
    }
    return features

if page == "Prediction":
    st.subheader("Prediction")

    tab1, tab2 = st.tabs(["Single Prediction", "Multiple Predictions"])

    with tab1:
        features = get_feature_inputs()
        if st.button("Predict"):
            try:
                headers = {"X-Request-Source": "Webapp Predictions"}
                response = requests.post(
                    PREDICTION_API_URL,
                    json={"data": [features]},
                    headers=headers
                )

                if not response.text.strip():
                    st.error("The response from the API is empty.")
                    st.stop()

                if response.status_code == 200:
                    try:
                        result = response.json()
                        if "predictions" in result:
                            # Create a DataFrame with the original features and predictions
                            result_df = pd.DataFrame([features])
                            result_df['Performance_Prediction'] = result["predictions"][0]
                            result_df['Confidence_Score'] = f"{result['confidence_scores'][0]:.2%}"
                            result_df['Database_Status'] = result.get("database_status", "unknown")
                            
                            st.success("Prediction completed successfully!")
                            st.write("Prediction Result:")
                            st.dataframe(result_df)
                            st.download_button(
                                label="Download Prediction as CSV",
                                data=result_df.to_csv(index=False).encode('utf-8'),
                                file_name='single_prediction_result.csv',
                                mime='text/csv'
                            )
                        else:
                            st.error("Unexpected response format")
                            st.error(f"Response keys: {list(result.keys())}")
                            st.error(f"Full response: {result}")
                    except Exception as json_error:
                        st.error(f"Error parsing response: {json_error}")
                        st.error(f"Raw response: {response.text}")
                else:
                    st.error(f"Failed to get a valid response from the API. Status code: {response.status_code}")
                    st.error(f"Response: {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    with tab2:
        uploaded_file = st.file_uploader("Upload a CSV file for Multiple Predictions", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of Uploaded Data:")
            st.dataframe(df)

            required_columns = ["Gender", "Age", "JobRole", "MonthlyIncome", "JobSatisfaction"]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
            else:
                data_payload = df.to_dict(orient="records")
                if st.button("Predict Multiple"):
                    try:
                        headers = {"X-Request-Source": "Webapp Predictions"}
                        response = requests.post(PREDICTION_API_URL, json={"data": data_payload}, headers=headers)

                        if not response.text.strip():
                            st.error("The response from the API is empty.")
                            st.stop()

                        if response.status_code == 200:
                            try:
                                result = response.json()
                                if "predictions" in result:
                                    # Create a DataFrame with the original data and predictions
                                    result_df = df.copy()
                                    result_df['Performance_Prediction'] = result["predictions"]
                                    result_df['Confidence_Score'] = [f"{score:.2%}" for score in result['confidence_scores']]
                                    result_df['Database_Status'] = result.get("database_status", "unknown")
                                    
                                    st.success("Predictions Completed!")
                                    st.write("Results:")
                                    st.dataframe(result_df)
                                    st.download_button(
                                        label="Download Predictions as CSV",
                                        data=result_df.to_csv(index=False).encode('utf-8'),
                                        file_name='multiple_prediction_results.csv',
                                        mime='text/csv'
                                    )
                                else:
                                    st.error("Invalid response format from API")
                            except Exception as json_error:
                                st.error(f"Error parsing response: {json_error}")
                                st.error(f"Raw response: {response.text}")
                        else:
                            st.error(f"Failed to get a valid response from the API. Status code: {response.status_code}")
                            st.error(f"Response: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

else:
    st.subheader("Past Predictions")
    start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=30))
    end_date = st.date_input("End Date", datetime.date.today())
    source = st.selectbox("Prediction Source", ["All", "Scheduled Predictions", "Webapp Predictions"])

    if st.button("Get Past Predictions"):
        try:
            response = requests.get(PAST_PREDICTIONS_API_URL, params={
                "start_date": start_date,
                "end_date": end_date,
                "source": source
            })

            if not response.text.strip():
                st.error("The response from the API is empty.")
                st.stop()

            if response.status_code == 200:
                data = response.json()
                if "past_predictions" in data and isinstance(data["past_predictions"], list):
                    past_predictions_df = pd.DataFrame(data["past_predictions"])
                    if not past_predictions_df.empty:
                        st.write("Past Predictions:")
                        st.dataframe(past_predictions_df)
                        st.download_button(
                            label="Download Past Predictions as CSV",
                            data=past_predictions_df.to_csv(index=False).encode('utf-8'),
                            file_name='past_predictions.csv',
                            mime='text/csv'
                        )
                    else:
                        st.warning("No past predictions found.")
                else:
                    st.error("Unexpected response format.")
            else:
                st.warning("No past predictions found for the selected date range and source.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
