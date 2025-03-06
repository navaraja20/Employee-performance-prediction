import os
import pickle
import pandas as pd
import psycopg2
import sqlalchemy
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (update with your .env file path)
load_dotenv()

# PostgreSQL connection details
DB_URL = os.getenv("DATABASE_URL", f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres:5432/{os.getenv('POSTGRES_DB')}")

# Load dataset
DATA_PATH = "data/raw/employees.csv"
df = pd.read_csv(DATA_PATH)

# Define features and target variable
features = [
    "Age", "Gender", "MaritalStatus", "JobRole", "Department",
    "BusinessTravel", "YearsAtCompany", "TotalWorkingYears",
    "YearsInCurrentRole", "YearsSinceLastPromotion",
    "MonthlyIncome", "HourlyRate", "StockOptionLevel",
    "PercentSalaryHike", "JobSatisfaction", "WorkLifeBalance",
    "JobInvolvement", "EnvironmentSatisfaction", "PerformanceRating", "OverTime"
]
target = "PerformanceRating"

# Convert categorical columns to numerical
df = pd.get_dummies(df, columns=["Gender", "MaritalStatus", "JobRole", "Department", "BusinessTravel", "OverTime"], drop_first=True)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Train Model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save Model
MODEL_PATH = "data/models/performance_model.pkl"
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

# Store metadata in PostgreSQL
try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS model_metadata (
                id SERIAL PRIMARY KEY,
                model_name TEXT,
                model_version TEXT,
                trained_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accuracy FLOAT
            )
        """)
        accuracy = model.score(X_test, y_test)
        conn.execute("""
            INSERT INTO model_metadata (model_name, model_version, accuracy)
            VALUES (%s, %s, %s)
        """, ("RandomForestRegressor", "1.0", accuracy))

    print(f"✅ Model trained and saved at {MODEL_PATH} with accuracy: {accuracy:.2f}")

except Exception as e:
    print(f"❌ Error storing model metadata: {e}")
