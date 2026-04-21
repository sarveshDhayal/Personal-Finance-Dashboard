"""
Export and aggregate data for Tableau visualization.
Prepares data in formats suitable for BI tools.
"""

import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_cleaned_data(input_file: str) -> pd.DataFrame:
    """Load cleaned transaction data."""
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    return df


def create_monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create monthly spending summary."""
    df['year_month'] = df['date'].dt.to_period('M')
    monthly_summary = df.groupby(['year_month', 'category'])['amount'].sum().reset_index()
    monthly_summary.columns = ['Month', 'Category', 'Amount']
    monthly_summary['Month'] = monthly_summary['Month'].astype(str)
    logger.info("Monthly summary created")
    return monthly_summary


def create_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create daily spending summary."""
    daily_summary = df.groupby('date')['amount'].sum().reset_index()
    daily_summary.columns = ['Date', 'Daily_Total']
    logger.info("Daily summary created")
    return daily_summary


def create_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create category-based summary."""
    category_summary = df.groupby('category').agg({
        'amount': ['sum', 'mean', 'count', 'min', 'max']
    }).reset_index()
    category_summary.columns = ['Category', 'Total', 'Average', 'Count', 'Min', 'Max']
    logger.info("Category summary created")
    return category_summary


def export_summaries(df: pd.DataFrame, output_dir: str = "data/cleaned") -> None:
    """Export all summary tables."""
    monthly = create_monthly_summary(df)
    daily = create_daily_summary(df)
    category = create_category_summary(df)
    
    monthly.to_csv(f"{output_dir}/monthly_summary.csv", index=False)
    daily.to_csv(f"{output_dir}/daily_summary.csv", index=False)
    category.to_csv(f"{output_dir}/category_summary.csv", index=False)
    
    logger.info(f"All summaries exported to {output_dir}")


def main():
    """Main execution."""
    input_file = "data/cleaned/transactions_clean.csv"
    df = load_cleaned_data(input_file)
    export_summaries(df)
    logger.info("Export pipeline completed successfully!")


if __name__ == "__main__":
    main()
