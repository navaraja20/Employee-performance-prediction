import pandas as pd
import random
import os

# Paths
DATASET_PATH = "D:\Employee-performance-prediction/employee_data.csv" 
OUTPUT_DIR = "D:\Employee-performance-prediction/"  
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Define error types
def introduce_missing_values(df):
    """Randomly remove values from required columns."""
    cols = random.sample(df.columns.tolist(), k=2) 
    df.loc[df.sample(frac=0.1).index, cols] = None
    return df

def remove_required_column(df):
    """Remove a required column from the dataset."""
    col_to_remove = random.choice(df.columns.tolist())
    return df.drop(columns=[col_to_remove])

def introduce_unknown_values(df):
    """Introduce unexpected values in categorical columns."""
    if "MaritalStatus" in df.columns:
        df.loc[df.sample(frac=0.05).index, "MaritalStatus"] = "Not Married"
    return df

def introduce_wrong_values(df):
    """Introduce wrong values (e.g., negative age)."""
    if "Age" in df.columns:
        df.loc[df.sample(frac=0.05).index, "Age"] = -12
    return df

def introduce_string_in_numeric(df):
    """Insert string values in a numeric column."""
    if "MonthlyIncome" in df.columns:
        df.loc[df.sample(frac=0.05).index, "MonthlyIncome"] = "unknown"
    return df

def introduce_wrong_category(df):
    """Insert an incorrect category (e.g., 'child' in gender)."""
    if "Gender" in df.columns:
        df.loc[df.sample(frac=0.05).index, "Gender"] = "child"
    return df

def shuffle_column_order(df):
    """Randomly shuffle column order to simulate unexpected format."""
    return df.sample(frac=1, axis=1)

# List of error functions
error_functions = [
    introduce_missing_values,
    remove_required_column,
    introduce_unknown_values,
    introduce_wrong_values,
    introduce_string_in_numeric,
    introduce_wrong_category,
    shuffle_column_order
]

# Generate multiple corrupted datasets
for i in range(1):  # Generate 5 different corrupted versions
    corrupted_df = df.copy()
    num_errors = random.randint(1, 3) 
    for _ in range(num_errors):
        corrupted_df = random.choice(error_functions)(corrupted_df)
    
    # Save the corrupted dataset
    corrupted_df.to_csv(f"{OUTPUT_DIR}/corrupted_data_{i+1}.csv", index=False)
    print(f"Saved: corrupted_data_{i+1}.csv")

print("Data issues generated successfully!")
