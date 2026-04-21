"""
Spending categorizer for transaction data.
Provides intelligent categorization based on description keywords.
"""

import pandas as pd
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Category keywords mapping - comprehensive rules
CATEGORY_RULES = {
    'Food & Dining': ['swiggy', 'zomato', 'restaurant', 'cafe', 'mcdonald',
                      'dominos', 'pizza', 'burger', 'starbucks', 'kfc', 'food'],
    'Groceries': ['bigbasket', 'grofers', 'blinkit', 'dmart', 'supermarket',
                  'zepto', 'reliance fresh', 'more supermarket', 'grocery'],
    'Transport': ['uber', 'ola', 'rapido', 'metro', 'petrol', 'fuel',
                  'irctc', 'redbus', 'makemytrip', 'goibibo', 'taxi'],
    'Shopping': ['amazon', 'flipkart', 'myntra', 'ajio', 'meesho',
                 'nykaa', 'snapdeal', 'tatacliq', 'mall', 'retail'],
    'Entertainment': ['netflix', 'spotify', 'hotstar', 'prime video', 'zee5',
                      'sonyliv', 'bookmyshow', 'pvr', 'inox', 'movie'],
    'Utilities': ['electricity', 'broadband', 'jio', 'airtel', 'vi ',
                  'water bill', 'gas bill', 'postpaid', 'prepaid', 'bill'],
    'Health': ['pharmacy', 'hospital', 'clinic', 'medplus', 'apollo',
               'netmeds', '1mg', 'healthians', 'diagnostic', 'doctor'],
    'Education': ['udemy', 'coursera', 'unacademy', 'byju', 'school fee',
                  'college fee', 'books', 'stationery', 'education'],
    'Finance & Banking': ['emi', 'loan', 'insurance', 'mutual fund', 'sip',
                          'credit card bill', 'fd', 'interest', 'bank'],
    'Rent & Housing': ['rent', 'maintenance', 'society', 'landlord', 'pg', 'housing'],
    'Income': ['salary', 'freelance', 'payment received', 'refund',
               'cashback', 'interest credit', 'dividend', 'income'],
}


def categorize(description: str) -> str:
    """Categorize a transaction based on description keywords."""
    desc = str(description).lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(re.search(kw, desc) for kw in keywords):
            return category
    return 'Other'


def apply_categorization(df: pd.DataFrame) -> pd.DataFrame:
    """Apply categorization rules to all transactions."""
    df = df.copy()
    df['category'] = df['Description'].apply(categorize)
    logger.info("Categorization applied to all transactions")
    return df


def get_uncategorized(df: pd.DataFrame) -> pd.DataFrame:
    """Get uncategorized transactions for review."""
    uncategorized = df[df['category'] == 'Other']
    logger.info(f"Uncategorized transactions: {len(uncategorized)}")
    return uncategorized


def main():
    """Main execution."""
    input_file = "data/cleaned/transactions_clean.csv"
    df = pd.read_csv(input_file)
    
    df = apply_categorization(df)
    uncategorized = get_uncategorized(df)
    
    print(f"\n⚠️  Uncategorized: {len(uncategorized)} rows")
    if len(uncategorized) > 0:
        print(uncategorized['Description'].value_counts().head(20))
    
    df.to_csv(input_file, index=False)
    logger.info("✅ Categories applied and saved")


if __name__ == "__main__":
    main()