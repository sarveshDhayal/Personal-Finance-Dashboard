# Tableau Finance Dashboard Workbook

This directory should contain the Tableau workbook file: `finance_dashboard.twbx`

## To Create the Dashboard:

1. Open Tableau Desktop
2. Connect to the cleaned data files in `../data/cleaned/`:
   - `transactions_clean.csv` - Full transaction details
   - `monthly_summary.csv` - Monthly aggregations
   - `daily_summary.csv` - Daily totals
   - `category_summary.csv` - Category statistics

3. Create visualizations:
   - **Daily Spending Trend**: Time series line chart using daily_summary.csv
   - **Category Breakdown**: Pie/donut chart of spending distribution
   - **Monthly Comparison**: Stacked bar chart by category
   - **Payment Method Analysis**: Box plot showing transaction distributions
   - **Category Statistics**: Table view with sum, mean, count, min, max

4. Create a Dashboard combining these sheets for comprehensive financial overview

5. Save as `finance_dashboard.twbx` in this directory

## Dashboard Features:
- Interactive filters by date range
- Drill-down capability by category
- Payment method breakdown
- Comparative analysis across time periods
- Spending alerts and thresholds
