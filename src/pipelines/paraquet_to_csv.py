# parquet_to_csv.py

import pandas as pd
import sys
import os


def convert_parquet_to_csv(input_path, output_path=None):
    # If no output path provided, generate one
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}.csv"

    try:
        print(f"Reading Parquet file: {input_path}")
        # or "fastparquet" if installed
        df = pd.read_parquet(input_path, engine="pyarrow")
        print(f"File loaded successfully with shape: {df.shape}")

        print(f"Writing CSV file to: {output_path}")
        df.to_csv(output_path, index=False)
        print("Conversion completed successfully!")

    except Exception as e:
        print(f"Error during conversion: {e}")


if __name__ == "__main__":
    input_file = "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/data/processed/sales_pipeline_processed.parquet"
    output_file = "C:/Projects/React-Based AI-Driven Sales Intelligence/React-Based/src/data/processed"
    convert_parquet_to_csv(input_file, output_file)
