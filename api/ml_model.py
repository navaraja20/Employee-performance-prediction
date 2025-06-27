import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def preprocess_data(data):
    df = pd.DataFrame(data)
    
  
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
 
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    
    return df

def train_model():
  
    df = pd.read_csv('./employee_data.csv') 
    

    df = preprocess_data(df)
    

    X = df.drop(['PerformanceRating', 'EmployeeNumber'], axis=1, errors='ignore')
    y = df['PerformanceRating']
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
   
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    

    os.makedirs('models', exist_ok=True)
    joblib.dump(model, '../api/models/performance_model.pkl')
    print(f"Model trained and saved to models/performance_model.pkl")
    print(f"Test accuracy: {model.score(X_test, y_test)}")

def load_model():
    return joblib.load("../api/models/performance_model.pkl")

if __name__ == "__main__":
    train_model()