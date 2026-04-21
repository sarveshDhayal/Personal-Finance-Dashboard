"""
Data cleaning pipeline for transaction data.
Handles missing values, data validation, and normalization.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_raw_data(input_path: str) -> pd.DataFrame:
    """Load raw transaction data from CSV."""
    try:
        df = pd.read_csv(input_path)
        logger.info(f"Loaded {len(df)} transactions from {input_path}")
        return df
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_path}")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply cleaning transformations to the dataframe."""
    df = df.copy()
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Convert amount to float
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Remove duplicates
    df = df.drop_duplicates()
    logger.info(f"Removed duplicates. Remaining rows: {len(df)}")
    
    # Handle missing values
    df = df.dropna(subset=['date', 'amount', 'description'])
    logger.info(f"Removed rows with missing critical values. Remaining rows: {len(df)}")
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    
    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)
    
    return df


def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned data to CSV."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned data to {output_path}")


def main():
    """Main execution."""
    input_file = "data/raw/transactions.csv"
    output_file = "data/cleaned/transactions_clean.csv"
    
    df = load_raw_data(input_file)
    df = clean_data(df)
    save_cleaned_data(df, output_file)
    
    logger.info("Data cleaning pipeline completed successfully!")


if __name__ == "__main__":
    main()
