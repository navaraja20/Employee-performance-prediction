import pandas as pd
import os
import argparse
import random

def split_csv(input_csv, output_folder, num_files=10):
    df = pd.read_csv(input_csv)
    
    os.makedirs(output_folder, exist_ok=True)
    chunk_size = len(df) // num_files
    
    for i in range(num_files):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_files - 1 else len(df)
        chunk = df.iloc[start:end]
        
        file_path = os.path.join(output_folder, f"data_part_{i+1}.csv")
        chunk.to_csv(file_path, index=False)
        print(f"Saved {file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to the input CSV file")
    parser.add_argument("--output", type=str, required=True, help="Path to the output folder")
    parser.add_argument("--num_files", type=int, default=10, help="Number of files to generate")

    args = parser.parse_args()
    split_csv(args.input, args.output, args.num_files)
