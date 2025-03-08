import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from ml.preprocess import preprocess_data
from ml.config import MODEL_PATH, TEST_SIZE, RANDOM_STATE

def train_model(data_path: str):
    """Trains a RandomForest model on the dataset and saves it as a .pkl file."""
    
    # Load data
    df = pd.read_csv(data_path)

    # Separate features and target variable
    X = df.drop(columns=["Attrition"])  # Assuming "Attrition" is the target
    y = df["Attrition"]

    # Preprocess data
    X = preprocess_data(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")

    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

def load_model():
    """Loads the trained model from disk."""
    return joblib.load(MODEL_PATH)
