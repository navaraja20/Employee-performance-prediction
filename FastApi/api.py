import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks, Response, Header
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import joblib
import logging
import os
from psycopg2 import pool, DatabaseError
from dotenv import load_dotenv
from datetime import date
import io
import pytz

app = FastAPI()

logging.basicConfig(level=logging.INFO)
load_dotenv()

@app.on_event("startup")
def load_model():
    global model, label_encoders, target_encoder
    try:
        model = joblib.load("ml_model.pkl")
        label_encoders = joblib.load("label_encoders.pkl")
        target_encoder = joblib.load("target_encoder.pkl")
        logging.info("Model and encoders loaded successfully")
    except FileNotFoundError as e:
        logging.error(f"Model or encoder file not found: {e}")
        raise HTTPException(status_code=500, detail="Model or encoder files not found. Please contact the administrator.")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")
connection_pool = pool.SimpleConnectionPool(1, 10, DATABASE_URL)

class PredictionRequest(BaseModel):
    data: List[dict]

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the input data to match training format"""
    # Create a copy to avoid modifying original
    processed_df = df.copy()
    
    # Standardize column names to match training data
    column_mapping = {
        'JobRole': 'Job Role',
        'MonthlyIncome': 'Monthly Income', 
        'JobSatisfaction': 'Job Satisfaction'
    }
    
    processed_df = processed_df.rename(columns=column_mapping)
    
    # Ensure columns are in the correct order as expected by the model
    expected_columns = ['Age', 'Gender', 'Job Role', 'Monthly Income', 'Job Satisfaction']
    processed_df = processed_df[expected_columns]
    
    # Apply label encoders to categorical columns
    for col in processed_df.columns:
        if col in label_encoders:
            le = label_encoders[col]
            try:
                processed_df[col] = le.transform(processed_df[col])
            except ValueError as e:
                # Handle unseen labels by mapping them to the most frequent class
                logging.warning(f"Unseen label in column {col}: {e}")
                most_frequent_class = le.classes_[0]  # Use first class as default
                processed_df[col] = processed_df[col].apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else le.transform([most_frequent_class])[0]
                )
                logging.info(f"Mapped unseen values in {col} to {most_frequent_class}")
    
    return processed_df

def get_db_connection():
    try:
        conn = connection_pool.getconn()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection pool exhausted.")
        conn.autocommit = False  # Ensure we can control transactions
        return conn
    except DatabaseError as e:
        logging.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

def insert_predictions_to_db(df: pd.DataFrame, predictions: List[str], confidences: List[float], source: str, actual_labels: List[str]):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        now = pd.Timestamp.now()
        confidences = [float(c) for c in confidences]
        df = df.reset_index(drop=True)

        # Handle both column name formats (with and without spaces)
        def get_column_value(row, col_options):
            for col in col_options:
                if col in row:
                    return row[col]
            raise KeyError(f"None of the expected columns found: {col_options}")

        data = [
            (
                row['Gender'], 
                row['Age'], 
                get_column_value(row, ['Job Role', 'JobRole']),
                get_column_value(row, ['Monthly Income', 'MonthlyIncome']),
                get_column_value(row, ['Job Satisfaction', 'JobSatisfaction']),
                predictions[i], confidences[i], source, now, actual_labels[i]
            )
            for i, row in df.iterrows()
        ]

        cursor.executemany(
            """
            INSERT INTO predictions
            (gender, age, job_role, monthly_income, job_satisfaction,
             performance_prediction, prediction_confidence, source, prediction_date, actual_label)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            data
        )

        # Explicitly commit the transaction
        conn.commit()
        logging.info(f"Successfully inserted {len(data)} predictions to database")
        
        # Verify the insert worked
        cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction_date >= %s", (now,))
        count = cursor.fetchone()[0]
        logging.info(f"Verification: {count} predictions found with timestamp >= {now}")
        
    except DatabaseError as e:
        logging.error(f"Database insertion error: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving predictions to the database: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error in database insertion: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            connection_pool.putconn(conn)

@app.post("/predict")
def predict(request: PredictionRequest, background_tasks: BackgroundTasks, x_request_source: Optional[str] = Header(default="Webapp Predictions")):
    try:
        df = pd.DataFrame(request.data)
        if df.empty:
            raise ValueError("No data provided for prediction.")

        # Check for required columns (both old and new formats are acceptable)
        required_columns = ["Gender", "Age"]
        job_role_cols = ["JobRole", "Job Role"]
        income_cols = ["MonthlyIncome", "Monthly Income"]
        satisfaction_cols = ["JobSatisfaction", "Job Satisfaction"]
        
        missing_required = [col for col in required_columns if col not in df.columns]
        if missing_required:
            raise ValueError(f"Missing required columns: {missing_required}")
            
        if not any(col in df.columns for col in job_role_cols):
            raise ValueError("Missing Job Role column (JobRole or 'Job Role')")
        if not any(col in df.columns for col in income_cols):
            raise ValueError("Missing Monthly Income column (MonthlyIncome or 'Monthly Income')")
        if not any(col in df.columns for col in satisfaction_cols):
            raise ValueError("Missing Job Satisfaction column (JobSatisfaction or 'Job Satisfaction')")

        # Preprocess the data (apply encoders and column mapping)
        processed_df = preprocess_data(df)
        
        # Make predictions on the processed data
        predictions = model.predict(processed_df)
        probabilities = model.predict_proba(processed_df)
        
        # Decode predictions using target encoder
        performance_prediction = target_encoder.inverse_transform(predictions)
        confidence_scores = probabilities.max(axis=1)
        confidence_scores = [float(c) for c in confidence_scores]

        # Add predictions to original dataframe (with original column names)
        df['performance_prediction'] = performance_prediction

        if 'actual_label' in df.columns:
            actual_labels = df['actual_label'].tolist()
        else:
            actual_labels = performance_prediction.tolist()  # fallback

        # Insert to database synchronously to catch errors
        try:
            insert_predictions_to_db(df, performance_prediction.tolist(), confidence_scores, x_request_source, actual_labels)
            db_status = "success"
        except Exception as e:
            logging.error(f"Failed to save predictions to database: {e}")
            db_status = f"failed: {e}"

        return {
            "predictions": performance_prediction.tolist(),
            "confidence_scores": confidence_scores,
            "database_status": db_status,
            "total_predictions": len(performance_prediction)
        }

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/past-predictions")
def get_past_predictions(start_date: date, end_date: date, source: str, page: int = 1, limit: int = None):
    if source not in ["All", "Scheduled Predictions", "Webapp Predictions"]:
        raise HTTPException(status_code=400, detail="Invalid source provided.")

    try:
        timezone = pytz.timezone('UTC')
        start_datetime = datetime.datetime.combine(start_date, datetime.datetime.min.time()).astimezone(timezone)
        end_datetime = datetime.datetime.combine(end_date, datetime.datetime.max.time()).astimezone(timezone)

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM predictions WHERE prediction_date BETWEEN %s AND %s"
        params = [start_datetime, end_datetime]

        if source == "Scheduled Predictions":
            query += " AND source = 'Scheduled Predictions' ORDER BY prediction_date DESC"
        elif source == "Webapp Predictions":
            query += " AND source = 'Webapp Predictions' ORDER BY prediction_date DESC"

        if limit and source != "Webapp Predictions":
            query += " LIMIT %s OFFSET %s"
            params.extend([limit, (page - 1) * limit])

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        past_predictions = []

        for row in rows:
            prediction_dict = dict(zip(columns, row))
            past_predictions.append(prediction_dict)

        if not past_predictions:
            raise HTTPException(status_code=404, detail="No past predictions found.")

        return {"past_predictions": past_predictions, "page": page, "limit": limit or "All"}

    except DatabaseError as e:
        logging.error(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail="Database query failed.")
    finally:
        cursor.close()
        connection_pool.putconn(conn)
