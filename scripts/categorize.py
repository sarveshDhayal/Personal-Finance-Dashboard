"""
Spending categorizer for transaction data.
Provides additional categorization and analysis utilities.
"""

import pandas as pd
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Category keywords mapping
CATEGORY_KEYWORDS = {
    'Groceries': ['grocery', 'whole foods', 'trader joe', 'safeway', 'food store'],
    'Transportation': ['gas', 'uber', 'lyft', 'taxi', 'parking', 'transit'],
    'Dining': ['restaurant', 'cafe', 'pizza', 'burger', 'sushi', 'coffee'],
    'Entertainment': ['movie', 'netflix', 'spotify', 'game', 'concert'],
    'Utilities': ['electric', 'water', 'internet', 'phone', 'gas bill'],
    'Health': ['pharmacy', 'doctor', 'hospital', 'gym', 'health'],
    'Shopping': ['amazon', 'mall', 'store', 'retail', 'shop'],
    'Books': ['bookstore', 'kindle', 'book', 'library'],
}


def categorize_transaction(description: str, existing_category: str) -> str:
    """
    Categorize a transaction based on description keywords.
    Falls back to existing category if no match found.
    """
    description_lower = description.lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in description_lower for keyword in keywords):
            return category
    
    return existing_category


def apply_categorization(df: pd.DataFrame) -> pd.DataFrame:
    """Apply categorization rules to all transactions."""
    df = df.copy()
    df['category'] = df.apply(
        lambda row: categorize_transaction(row['description'], row['category']),
        axis=1
    )
    logger.info("Categorization applied to all transactions")
    return df


def get_spending_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate spending summary by category."""
    summary = df.groupby('category')['amount'].agg(['sum', 'count', 'mean'])
    summary.columns = ['Total', 'Count', 'Average']
    summary = summary.sort_values('Total', ascending=False)
    logger.info("Spending summary generated")
    return summary


def main():
    """Main execution."""
    input_file = "data/cleaned/transactions_clean.csv"
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    
    df = apply_categorization(df)
    df.to_csv(input_file, index=False)
    
    summary = get_spending_summary(df)
    logger.info(f"\nSpending Summary:\n{summary}")
    
    logger.info("Categorization complete!")


if __name__ == "__main__":
    main()
