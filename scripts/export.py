"""
Export and aggregate data for Tableau visualization.
Prepares KPI summaries and category breakdowns for BI tools.
"""

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_cleaned_data(input_file: str) -> pd.DataFrame:
    """Load cleaned transaction data."""
    df = pd.read_csv(input_file)
    df['Date'] = pd.to_datetime(df['Date'])
    logger.info(f"Loaded {len(df)} transactions from {input_file}")
    return df


def create_monthly_kpi(df: pd.DataFrame) -> pd.DataFrame:
    """Create monthly KPI summary (income, expenses, savings)."""
    expenses = df[df['transaction_type'] == 'Expense'].copy()
    income = df[df['transaction_type'] == 'Income'].copy()
    
    monthly_income = income.groupby('month')['Amount'].sum().rename('total_income')
    monthly_expense = expenses.groupby('month')['Amount'].apply(
        lambda x: abs(x.sum())
    ).rename('total_expense')
    
    monthly_kpi = pd.concat([monthly_income, monthly_expense], axis=1).fillna(0)
    monthly_kpi['savings'] = monthly_kpi['total_income'] - monthly_kpi['total_expense']
    monthly_kpi['savings_rate'] = (
        monthly_kpi['savings'] / monthly_kpi['total_income'] * 100
    ).round(2).replace([float('inf'), float('-inf')], 0)
    
    monthly_kpi.reset_index(inplace=True)
    logger.info("Monthly KPI summary created")
    return monthly_kpi


def create_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create category-based spending breakdown."""
    expenses = df[df['transaction_type'] == 'Expense'].copy()
    
    category_summary = (
        expenses.groupby(['month', 'category'])['Amount']
        .apply(lambda x: abs(x.sum()))
        .reset_index()
        .rename(columns={'Amount': 'spent'})
    )
    logger.info("Category summary created")
    return category_summary


def create_daily_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create daily spending summary."""
    daily_summary = df.groupby('Date')['Amount'].sum().reset_index()
    daily_summary.columns = ['Date', 'Daily_Total']
    logger.info("Daily summary created")
    return daily_summary


def export_summaries(df: pd.DataFrame, output_dir: str = "data/cleaned") -> None:
    """Export all summary tables for Tableau."""
    monthly_kpi = create_monthly_kpi(df)
    category_summary = create_category_summary(df)
    daily_summary = create_daily_summary(df)
    
    monthly_kpi.to_csv(f"{output_dir}/monthly_kpi.csv", index=False)
    category_summary.to_csv(f"{output_dir}/category_summary.csv", index=False)
    daily_summary.to_csv(f"{output_dir}/daily_summary.csv", index=False)
    
    logger.info(f"All summaries exported to {output_dir}")
    print("\n✅ Exported files:")
    print(f"  - monthly_kpi.csv")
    print(f"  - category_summary.csv")
    print(f"  - daily_summary.csv")


def main():
    """Main execution."""
    input_file = "data/cleaned/transactions_clean.csv"
    df = load_cleaned_data(input_file)
    export_summaries(df)
    logger.info("Export pipeline completed successfully!")


if __name__ == "__main__":
    main()