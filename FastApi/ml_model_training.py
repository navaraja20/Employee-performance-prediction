import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from pathlib import Path

# Load dataset
project_root = Path(__file__).parent.parent
data_path = project_root / "airflow" / "data" / "employee_data.csv"
df = pd.read_csv(data_path)

# Keep only selected features and the target
selected_features = [
    "Age",
    "Gender", 
    "Job Role",
    "Monthly Income",
    "Job Satisfaction"
]
target_column = "Attrition"

# Standardize target labels first
df[target_column] = df[target_column].replace({
    'Left': 'Left',
    'Stayed': 'Stayed',
    'Yes': 'Left',
    'No': 'Stayed',
    1: 'Left',
    0: 'Stayed'
})

# Filter data
df = df[selected_features + [target_column]].dropna()

# Encode categorical features
categorical_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
if target_column in categorical_cols:
    categorical_cols.remove(target_column)

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Encode target
target_le = LabelEncoder()
df[target_column] = target_le.fit_transform(df[target_column])

# Print encoding for verification
print("Target encoding mapping:")
print(dict(zip(target_le.classes_, target_le.transform(target_le.classes_))))

# Train-test split
X = df[selected_features]
y = df[target_column]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save artifacts
joblib.dump(model, "ml_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(target_le, "target_encoder.pkl")

print("✅ Model training complete. Encodings:")
print(f"Target: {dict(zip(target_le.classes_, target_le.transform(target_le.classes_)))}")
for col, encoder in label_encoders.items():
    print(f"{col}: {dict(zip(encoder.classes_, encoder.transform(encoder.classes_)))}")