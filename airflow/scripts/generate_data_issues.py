import os
import pandas as pd
import numpy as np
import random
import argparse

def generate_data_issues(dataset_path, output_path):
    os.makedirs(output_path, exist_ok=True)

    # Load the dataset
    df = pd.read_csv(dataset_path)

    # Make a copy to avoid modifying the original dataset
    corrupted_df = df.copy()

    ### 1. Missing Column (Drop the 'age' column if it exists)
    if 'age' in corrupted_df.columns:
        corrupted_df.drop(columns=['age'], inplace=True)

    ### 2. Missing Values in a Required Column (Set random 'gender' values to NaN)
    if 'gender' in corrupted_df.columns:
        missing_indices = corrupted_df.sample(frac=0.1, random_state=42).index
        corrupted_df.loc[missing_indices, 'gender'] = np.nan

    ### 3. Unknown Value in Categorical Column (Add unexpected 'France' value in 'country')
    if 'country' in corrupted_df.columns:
        unknown_indices = corrupted_df.sample(frac=0.05, random_state=42).index
        corrupted_df.loc[unknown_indices, 'country'] = 'France'

    ### 4. Wrong Value in Numeric Column (Set negative value in 'age' or other numeric fields)
    numeric_columns = corrupted_df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        wrong_indices = corrupted_df.sample(frac=0.05, random_state=42).index
        corrupted_df.loc[wrong_indices, col] = -12

    ### 5. Wrong Type in Numeric Column (Insert string into numeric column)
    if 'salary' in corrupted_df.columns:
        wrong_type_indices = corrupted_df.sample(frac=0.05, random_state=42).index
        corrupted_df.loc[wrong_type_indices, 'salary'] = 'not_a_number'

    ### 6. Duplicate Rows (Duplicate some rows)
    corrupted_df = pd.concat([corrupted_df, corrupted_df.sample(frac=0.05, random_state=42)], ignore_index=True)

    ### 7. Outlier Values (Set unrealistic values for numeric fields)
    if 'salary' in corrupted_df.columns:
        outlier_indices = corrupted_df.sample(frac=0.05, random_state=42).index
        corrupted_df.loc[outlier_indices, 'salary'] = corrupted_df['salary'].max() * 100

    # Save the final corrupted dataset
    final_path = os.path.join(output_path, 'corrupted_dataset.csv')
    corrupted_df.to_csv(final_path, index=False)
    print(f"Corrupted dataset saved to: {final_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate data issues for testing.")
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to the input dataset")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output directory")

    args = parser.parse_args()
    generate_data_issues(args.dataset_path, args.output_path)
