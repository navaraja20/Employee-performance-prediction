# api/ml_model/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

output_dir = os.path.join(os.path.dirname(__file__), ".")  # Save in same dir
os.makedirs(output_dir, exist_ok=True)


# Load dataset
df = pd.read_csv("airflow/data/employee_data.csv")
selected_features = ['Age', 'Gender', 'JobRole', 'JobSatisfaction', 'MonthlyIncome']

# Target variable
y = df["Attrition"].map({"Yes": 1, "No": 0})

# Drop unused or non-informative columns
X = df[selected_features].copy()

# Encode categorical variables
encoders = {}
for col in X.select_dtypes(include="object").columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

# Scale numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and preprocessors
output_dir = os.path.dirname(__file__)
joblib.dump(model, os.path.join(output_dir, "model.pkl"))
joblib.dump(encoders, os.path.join(output_dir, "encoders.pkl"))
joblib.dump(scaler, os.path.join(output_dir, "scaler.pkl"))

print("✅ Model training completed and files saved.")
