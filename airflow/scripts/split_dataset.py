import os
import pandas as pd
import numpy as np
import argparse

def split_dataset(dataset_path, output_path, num_files):
    os.makedirs(output_path, exist_ok=True)
    
    # Load the dataset
    df = pd.read_csv(dataset_path)
    
    # Shuffle the data to make the split more random
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split the data into chunks
    chunks = np.array_split(df, num_files)
    
    # Save each chunk as a separate file
    for i, chunk in enumerate(chunks):
        file_path = os.path.join(output_path, f'part_{i + 1}.csv')
        chunk.to_csv(file_path, index=False)
        print(f"Saved: {file_path} ({len(chunk)} rows)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split dataset into multiple files.")
    parser.add_argument("--dataset_path", type=str, required=True, help="Path to the input dataset")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output directory")
    parser.add_argument("--num_files", type=int, required=True, help="Number of files to generate")

    args = parser.parse_args()
    split_dataset(args.dataset_path, args.output_path, args.num_files)
