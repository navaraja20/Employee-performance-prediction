import numpy as np
import pickle

# Load trained model (Ensure model.pkl exists in 'data/models/')
MODEL_PATH = "data/models/model.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# ✅ Predict Function
def predict_employee_performance(employee_data: dict) -> float:
    try:
        input_data = np.array([list(employee_data.values())]).astype(float)
        prediction = model.predict(input_data)[0]
        return float(prediction)
    except Exception as e:
        return -1  # Return error code for failed prediction
