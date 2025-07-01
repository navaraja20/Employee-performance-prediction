# airflow/scripts/generate_data_issues.py
import pandas as pd
import random
import os
from pathlib import Path

def inject_errors(df):
    # Error 1: Missing required column
    df.drop(columns=["Gender"], inplace=True, errors='ignore')

    # Error 2: Null values
    df.loc[random.sample(range(len(df)), 5), "Age"] = None

    # Error 3: Out-of-range value
    df.loc[0, "Age"] = -10

    # Error 4: Unknown category
    df.loc[1, "BusinessTravel"] = "Teleport"

    # Error 5: String in numeric column
    df.loc[2, "DailyRate"] = "OneThousand"

    # Error 6: Wrong data type
    df["EnvironmentSatisfaction"] = df["EnvironmentSatisfaction"].astype(str)

    # Error 7: Duplicate rows
    df = pd.concat([df, df.iloc[:2]], ignore_index=True)

    return df

def main():
    # Define paths using pathlib
    data_path = Path(__file__).parent.parent / "data" / "employee_data.csv"
    output_path = Path(__file__).parent.parent / "data" / "employee_data_with_errors.csv"

    # Debug: Check path and file existence
    print(f"Looking for file at: {data_path}")
    print(f"File exists: {data_path.exists()}")
    if data_path.parent.exists():
        print(f"Files in data folder: {os.listdir(data_path.parent)}")
    else:
        print("Data folder not found")

    # Load dataset
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Cannot find {data_path}. Ensure 'employee_data.csv' is in the 'data' folder.")

    # Process and save
    df_error = inject_errors(df.copy())
    df_error.to_csv(output_path, index=False)
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()