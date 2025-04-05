import streamlit as st
import pandas as pd
import requests
from io import StringIO

# API endpoint
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Employee Performance Prediction", layout="wide")

# Custom styling with background image
st.markdown(
    """
    <style>
    body {
        background-image: url('https://source.unsplash.com/1600x900/?office,work');
        background-size: cover;
    }
    .stApp {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 10px;
    }
    .stTextInput, .stSelectbox, .stNumberInput {
        border-radius: 10px;
        padding: 10px;
    }
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and tabs
st.title("🏆 Employee Performance Prediction")
tab1, tab2 = st.tabs(["📈 Make Predictions", "🗃️ Past Predictions"])

# -------------------------
# 🚀 Prediction Tab
# -------------------------
with tab1:
    st.header("Make Predictions")

    # Single Prediction Form
    st.subheader("SINGLE")
    with st.form("single_prediction_form"):
        st.markdown("### Employee Information")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=18, max_value=65)
            gender = st.selectbox("Gender", ["Male", "Female"])
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
            department = st.selectbox("Department", ["Sales", "HR", "R&D", "Finance", "Marketing"])
            job_role = st.selectbox("Job Role", ["Manager", "Developer", "Sales Executive", "HR", "Research Scientist"])
            education = st.selectbox("Education Level", [1, 2, 3, 4, 5])
        with col2:
            job_level = st.number_input("Job Level", min_value=1, max_value=5)
            total_working_years = st.number_input("Total Working Years", min_value=0)
            years_at_company = st.number_input("Years at Company", min_value=0)
            years_in_current_role = st.number_input("Years in Current Role", min_value=0)
            years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0)
            num_companies_worked = st.number_input("Number of Companies Worked", min_value=0)
        
        st.markdown("### Compensation & Benefits")
        col3, col4 = st.columns(2)
        with col3:
            monthly_income = st.number_input("Monthly Income", min_value=1000)
            hourly_rate = st.number_input("Hourly Rate", min_value=10)
            stock_option_level = st.number_input("Stock Option Level", min_value=0, max_value=3)
        with col4:
            percent_salary_hike = st.number_input("Percent Salary Hike", min_value=0)
            performance_rating = st.number_input("Performance Rating", min_value=1, max_value=5)
            overtime = st.selectbox("OverTime", ["Yes", "No"])
        
        submit_single = st.form_submit_button("Predict", use_container_width=True)
        
        if submit_single:
            input_data = {
                "age": age, "gender": gender, "marital_status": marital_status,
                "department": department, "job_role": job_role, "education": education,
                "job_level": job_level, "total_working_years": total_working_years,
                "years_at_company": years_at_company, "years_in_current_role": years_in_current_role,
                "years_since_last_promotion": years_since_last_promotion,
                "num_companies_worked": num_companies_worked,
                "monthly_income": monthly_income, "hourly_rate": hourly_rate,
                "stock_option_level": stock_option_level,
                "percent_salary_hike": percent_salary_hike, "performance_rating": performance_rating,
                "overtime": overtime
            }
            try:
                response = requests.post(f"{API_URL}/predict", json=input_data)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Predicted Performance Rating: **{result['prediction']}**")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
    
    # -------------------------
    # 🔥 Multi Prediction (CSV Upload)
    # -------------------------
    st.subheader("BATCH PREDICTIONS")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        file_content = StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = pd.read_csv(file_content)
        st.write("📊 Uploaded Data:")
        st.dataframe(data)

        if st.button("Predict for Uploaded Data", use_container_width=True):
            try:
                response = requests.post(f"{API_URL}/predict", json=data.to_dict(orient="records"))
                if response.status_code == 200:
                    results = response.json()
                    df = pd.DataFrame(results)
                    st.success("Batch Prediction Completed!")
                    st.write(df)
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")

# -------------------------
# 🗃️ Past Predictions Tab
# -------------------------
with tab2:
    st.header("PAST PREDICTIONS")
    
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    source = st.selectbox("Source", ["all", "webapp", "scheduled"])
    
    if st.button("Get Past Predictions", use_container_width=True):
        params = {"start_date": start_date, "end_date": end_date, "source": source}
        try:
            response = requests.get(f"{API_URL}/past-predictions", params=params)
            if response.status_code == 200:
                results = response.json()
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
