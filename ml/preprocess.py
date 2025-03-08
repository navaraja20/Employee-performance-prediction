import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(df: pd.DataFrame):
    """Preprocesses the dataset by handling missing values and scaling numeric features."""
    
    # Fill missing values with median
    df.fillna(df.median(), inplace=True)

    # Select numerical columns for scaling
    numeric_features = df.select_dtypes(include=["number"]).columns
    scaler = StandardScaler()
    df[numeric_features] = scaler.fit_transform(df[numeric_features])

    return df
