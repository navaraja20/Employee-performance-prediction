import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os

# Load dataset
DATA_PATH = "employees.csv"
MODEL_PATH = "model.pkl"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Handle categorical variables
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# Split data
X = df.drop(columns=['Attrition'])  # Assuming 'Attrition' is the target variable
y = df['Attrition']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, MODEL_PATH)
print(f"Model saved at {MODEL_PATH}")
