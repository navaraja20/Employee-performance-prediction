import pandas as pd
import os
import random
import argparse
from datetime import datetime

def introduce_errors(df):
    """Introduce synthetic data errors"""
    if random.random() < 0.3:  # 30% chance to add errors
        error_type = random.choice([
            'missing_column',
            'missing_values',
            'invalid_values',
            'wrong_type'
        ])
        
        if error_type == 'missing_column' and len(df.columns) > 1:
            df.drop(random.choice(df.columns), axis=1, inplace=True)
            
        elif error_type == 'missing_values':
            col = random.choice(df.columns)
            df.loc[df.sample(frac=0.2).index, col] = None
            
        elif error_type == 'invalid_values':
            if 'age' in df.columns:
                df.loc[df.sample(frac=0.1).index, 'age'] = -abs(df['age'])
                
        elif error_type == 'wrong_type':
            col = random.choice(df.select_dtypes(include='number').columns)
            df.loc[df.sample(frac=0.1).index, col] = 'invalid'
    
    return df

def split_dataset(input_path, output_dir, n_files):
    """Split dataset into multiple files with potential errors"""
    df = pd.read_csv(input_path)
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(n_files):
        file_df = df.sample(frac=0.2) 
        file_df = introduce_errors(file_df)
        file_df.to_csv(f"{output_dir}/data_{i}.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split dataset into multiple files with synthetic errors')
    parser.add_argument('--input', required=True, help='Path to input CSV file')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--n_files', type=int, required=True, help='Number of files to create')
    args = parser.parse_args()
    
    split_dataset(args.input, args.output, args.n_files)