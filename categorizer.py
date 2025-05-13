import re
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# keyword -> category map
keyword_category_map = {
    'INDIAFORENSIC': 'Salary & Income', 'INDIAFORENS': 'Salary & Income', 'RMCPL': 'Salary & Income',
    'POS': 'Entertainment', 'SETTLEMENT': 'Payments', 'SETT': 'Payments',
    'NEFT': 'Transfers', 'RTGS': 'Transfers', 'IMPS': 'Transfers',
    'TRF FROM': 'Transfers', 'FTR FROM': 'Transfers', 'TRF TO': 'Transfers', 'SWEEP TRF TO': 'Transfers',
    'COMMISSION': 'Fees & Charges', 'SERVICE TAX': 'Fees & Charges', 'S TAX': 'Fees & Charges',
    'GROCERY': 'Entertainment', 'RENT': 'Salary & Income',
    'INSURANCE': 'Insurance', 'INDO GIBL': 'Insurance',
    'BBPS': 'Utilities & Telecom', 'FDRL': 'Transfers', 'INTERNAL FUND TRANSFER': 'Transfers',
    'MICRO ATM': 'Cash Handling', 'ATM': 'Cash Handling', 'CASHDEP': 'Cash Handling',
    'DSB CASH PICKP': 'Cash Handling', 'BEAT CASH PICKP': 'Cash Handling',
    'SHORT CSH': 'Cash Handling', 'LOAN RECOVERY': 'Loans & EMI',
    'AIRTEL': 'Utilities & Telecom', 'IRCTC': 'Entertainment',
    'CHQ DEPOSIT RETURN': 'Fees & Charges', 'INCOME': 'Salary & Income',
    'REMI': 'Salary & Income', 'INDFOR': 'Salary & Income', 'STL': 'Payments',
    'AEPS': 'Fees & Charges', 'ADJ': 'Fees & Charges',
    'CB': 'Payments', 'CR': 'Payments', 'DR': 'Payments', 'MAW': 'Fees & Charges',
    'Miscellaneous': 'Miscellaneous', 'CHQ DEP': 'Payments', 'CHEQUE DEPOSIT': 'Payments', 'CHQ': 'Payments',
    'SBI': 'Miscellaneous', 'VODAFONE': 'Utilities & Telecom', 'MOBILE SERVICES': 'Utilities & Telecom',
    'CASHPICKUP': 'Cash Handling', 'CASH PICKUP': 'Cash Handling',
    'RVSL DSB CSH PCKUP': 'Cash Handling', 'DSB CSH PCKUP': 'Cash Handling',
    'PICKUP CHARGE': 'Cash Handling', 'SER TAX': 'Fees & Charges',
    'NORTH DELHI POWER': 'Utilities & Telecom', 'RAJDHANI POWER': 'Utilities & Telecom', 'BSES': 'Utilities & Telecom',
    'INDIAIDEAS': 'Payments', 'BIGTREE': 'Entertainment', 'BOOKMYSHOW': 'Entertainment',
    'SONATA FINANCE': 'Loans & EMI', 'MANGALA FINANCE': 'Loans & EMI', 'SHETTY': 'Loans & EMI',
    'BY ': 'Transfers',
}

def categorize_transaction(description: str) -> str:
    """Categorizes a transaction based on description using keyword rules."""
    if description == 'Miscellaneous':
        return 'Miscellaneous'

    description_upper = str(description).upper()

    for keyword, category in keyword_category_map.items():
        if keyword in description_upper:
            return category

    if re.search(r'\b\d{16}\b', description_upper):
        return 'Card Reference'
    
    if re.search(r'\b\d{12}\b', description_upper):
        return 'Account'

    return 'Others'

def categorize_dataframe(df: pd.DataFrame, desc_col: str = 'TRANSACTION DETAILS') -> pd.DataFrame:
    df = df.copy()
    df['Category'] = df[desc_col].apply(categorize_transaction)
    return df

def plot_category_distribution(df: pd.DataFrame, min_threshold: float = 0.01):
    category_counts = df['Category'].value_counts().sort_values(ascending=False)

    c1, c2 = st.columns(2)
    with c1:
        # Bar Plot
        fig_bar, ax_bar = plt.subplots(figsize=(10, 10))
        category_counts.plot(kind='bar', color='green', ax=ax_bar)
        ax_bar.set_title('Number of Transactions by Category')
        ax_bar.set_xlabel('Category')
        ax_bar.set_ylabel('Transaction Count')
        ax_bar.tick_params(axis='x', rotation=45)
        st.pyplot(fig_bar)
    with c2:
        # Pie Chart
        total = category_counts.sum()
        category_percent = category_counts / total
        filtered = category_counts[category_percent >= min_threshold]
        others = category_counts[category_percent < min_threshold].sum()
        filtered['Others'] = others
        fig_pie, ax_pie = plt.subplots(figsize=(10, 10))
        filtered.plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax_pie)
        ax_pie.set_title('Simplified Transaction Count Distribution')
        ax_pie.set_ylabel('')
        st.pyplot(fig_pie)
