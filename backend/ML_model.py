import numpy as np
import joblib  # For loading pre-trained models

# Load the pre-trained model (Ensure you have a trained model file)
MODEL_PATH = "../models/model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    model = None

def predict_performance(employee_data: dict) -> float:
    """
    Predicts the performance score based on employee details.

    Args:
        employee_data (dict): Dictionary containing employee details.

    Returns:
        float: Predicted performance score.
    """

    if not model:
        raise ValueError("Model is not loaded properly.")

    # Convert categorical variables to numerical (This should match model preprocessing)
    categorical_map = {
        "gender": {"Male": 0, "Female": 1, "Other": 2},
        "marital_status": {"Single": 0, "Married": 1, "Divorced": 2},
        "job_role": {"Manager": 0, "Engineer": 1, "Technician": 2, "HR": 3, "Sales": 4, "Other": 5},
        "department": {"IT": 0, "HR": 1, "Finance": 2, "Sales": 3, "Marketing": 4, "Operations": 5},
        "business_travel": {"Rarely": 0, "Frequently": 1, "Never": 2},
        "overtime": {"Yes": 1, "No": 0}
    }

    # Process input data
    features = [
        employee_data["age"],
        categorical_map["gender"][employee_data["gender"]],
        categorical_map["marital_status"][employee_data["marital_status"]],
        categorical_map["job_role"][employee_data["job_role"]],
        categorical_map["department"][employee_data["department"]],
        categorical_map["business_travel"][employee_data["business_travel"]],
        employee_data["years_at_company"],
        employee_data["total_working_years"],
        employee_data["years_in_current_role"],
        employee_data["years_since_last_promotion"],
        employee_data["monthly_income"],
        employee_data["hourly_rate"],
        employee_data["stock_option_level"],
        employee_data["percent_salary_hike"],
        employee_data["job_satisfaction"],
        employee_data["work_life_balance"],
        employee_data["job_involvement"],
        employee_data["environment_satisfaction"],
        employee_data["performance_rating"],
        categorical_map["overtime"][employee_data["overtime"]]
    ]

    # Convert to NumPy array and reshape for prediction
    input_array = np.array(features).reshape(1, -1)

    # Make prediction
    predicted_score = model.predict(input_array)[0]

    return round(predicted_score, 2)  # Round for readability
