import streamlit as st
import pandas as pd
import requests
import datetime

API_URL = "http://api:8000"

def get_past_predictions(start_date, end_date, source):
       response = requests.get(f"{API_URL}/past-predictions", params={"start_date": start_date, "end_date": end_date, "source": source})
       if response.status_code == 200:
           return pd.DataFrame(response.json())
       else:
           st.error("Error fetching past predictions")
           return pd.DataFrame()

st.header("Past Predictions")
start_date = st.date_input("Start Date", datetime.date.today() - datetime.timedelta(days=7))
end_date = st.date_input("End Date", datetime.date.today())
source = st.selectbox("Prediction Source", ["all", "webapp", "scheduled"])
if st.button("Fetch Predictions"):
       predictions = get_past_predictions(start_date, end_date, source)
       if not predictions.empty:
           st.write("Past Predictions:")
           st.dataframe(predictions)
       else:
           st.write("No predictions found for the selected criteria.")