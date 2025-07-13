import pandas as pd
import os

def clean_dataframe(df):
    """Clean dataframe by removing duplicate columns and handling missing Gender column"""
    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]
    
    # If Gender column is missing, add it with NaN values (for error simulation)
    if 'Gender' not in df.columns:
        print("⚠️ Gender column missing - adding with NaN values for error simulation")
        df['Gender'] = None
    
    return df

def split_by_num_files(df, output_base_dir, base_name, num_files):
    # Clean the dataframe first
    df = clean_dataframe(df)
    
    total_rows = len(df)
    base_chunk_size = total_rows // num_files
    remainder = total_rows % num_files

    start_idx = 0
    for chunk_num in range(num_files):
        current_chunk_size = base_chunk_size + (1 if chunk_num < remainder else 0)
        end_idx = start_idx + current_chunk_size
        chunk = df.iloc[start_idx:end_idx]

        output_file = os.path.join(output_base_dir, f'{base_name}_chunk_{chunk_num + 1}.csv')
        chunk.to_csv(output_file, index=False)
        print(f"✅ Saved: {output_file} with {len(chunk)} rows and columns: {list(chunk.columns)}")

        start_idx = end_idx

# Change these to match your employee corrupted data files with reasonable chunk sizes
input_files = [
    ('./airflow/data/generated_errors/employee_data_with_errors.csv', 5),  # Split into 5 chunks instead of 30
    ('./airflow/data/generated_errors/employee_data2_with_errors.csv', 20)  # Split into 20 chunks instead of 3500
]

output_base_dir = './airflow/data/raw_data'
os.makedirs(output_base_dir, exist_ok=True)

for input_file, num_files in input_files:
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    df = pd.read_csv(input_file)
    split_by_num_files(df, output_base_dir, base_name, num_files)
