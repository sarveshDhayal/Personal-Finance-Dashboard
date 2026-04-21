"""
Data cleaning pipeline for transaction data.
Handles missing values, data validation, normalization, and feature engineering.
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
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df.dropna(subset=['Date'], inplace=True)
    logger.info("Dates converted and validated")
    
    # Convert amount to float - handle currency symbols
    df['Amount'] = df['Amount'].astype(str).str.replace(r'[₹$,]', '', regex=True)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df.dropna(subset=['Amount'], inplace=True)
    logger.info("Amounts converted and validated")
    
    # Normalize debit/credit to positive/negative
    df['Amount'] = df.apply(
        lambda r: -abs(r['Amount']) if str(r['Transaction Type']).lower() == 'debit'
        else abs(r['Amount']),
        axis=1
    )
    logger.info("Amounts normalized to positive/negative")
    
    # Remove duplicates
    df = df.drop_duplicates()
    logger.info(f"Removed duplicates. Remaining rows: {len(df)}")
    
    # Strip whitespace from string columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Create time-based features
    df['month'] = df['Date'].dt.to_period('M').astype(str)
    df['month_name'] = df['Date'].dt.strftime('%b %Y')
    df['year'] = df['Date'].dt.year
    df['week'] = df['Date'].dt.isocalendar().week
    df['day_of_week'] = df['Date'].dt.day_name()
    df['quarter'] = df['Date'].dt.to_period('Q').astype(str)
    logger.info("Time-based features created")
    
    # Create transaction type (Income/Expense)
    df['transaction_type'] = df['Amount'].apply(
        lambda x: 'Income' if x > 0 else 'Expense'
    )
    logger.info("Transaction types assigned")
    
    return df


def save_cleaned_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned data to CSV."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned data to {output_path}")


def main():
    """Main execution."""
    input_file = "data/raw/personal_transactions.csv"
    output_file = "data/cleaned/transactions_clean.csv"
    
    df = load_raw_data(input_file)
    df = clean_data(df)
    save_cleaned_data(df, output_file)
    
    logger.info("Data cleaning pipeline completed successfully!")
    print(df.head())


if __name__ == "__main__":
    main()
