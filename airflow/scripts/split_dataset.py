# airflow/scripts/split_dataset.py
import pandas as pd
import os
import sys
import numpy as np
from pathlib import Path

def split_csv(input_path, output_folder, num_files, rows_per_file=10):
    # Convert to Path objects for robust handling
    input_path = Path(input_path)
    output_folder = Path(output_folder)

    # Debug: Check file and folder existence
    print(f"Input file: {input_path}")
    print(f"Input file exists: {input_path.exists()}")
    print(f"Output folder: {output_folder}")
    print(f"Output folder exists: {output_folder.exists()}")

    # Read input CSV
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: Input file {input_path} not found.")
        sys.exit(1)

    # Check if dataset has enough rows
    total_rows = len(df)
    print(f"Total rows in dataset: {total_rows}")
    max_possible_files = total_rows // rows_per_file
    if num_files > max_possible_files:
        print(f"Warning: Requested {num_files} files, but only {max_possible_files} files possible with {rows_per_file} rows each.")
        num_files = min(num_files, max_possible_files)

    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Split dataset into chunks of rows_per_file
    for i in range(num_files):
        start_idx = i * rows_per_file
        end_idx = min(start_idx + rows_per_file, total_rows)  # Ensure we don't go beyond dataset
        split_df = df.iloc[start_idx:end_idx]
        
        if not split_df.empty:  # Only save non-empty DataFrames
            output_path = output_folder / f"part_{i+1}.csv"
            split_df.to_csv(output_path, index=False)
            print(f"Saved: {output_path} with {len(split_df)} rows")
        else:
            print(f"Skipping empty split for file {i+1}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python split_dataset.py <input_csv> <output_folder> <num_files>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_folder = sys.argv[2]
    try:
        num_files = int(sys.argv[3])
    except ValueError:
        print("Error: num_files must be an integer.")
        sys.exit(1)

    split_csv(input_csv, output_folder, num_files, rows_per_file=10)