import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def analyze_spending(df, weekly):
    st.title("Spending Analysis Dashboard")

    c1, c2 = st.columns(2)

    with c1:
        #Weekly Pattern
        st.header("Weekly Spending Pattern")

        latest_date = weekly.index.max()
        cutoff = latest_date - pd.Timedelta(days=365)
        recent = weekly.loc[cutoff:]

        st.subheader("Weekly Chart")
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        recent.plot(marker='o', color=['red', 'green'], ax=ax1)
        ax1.set_title('Weekly Spending Pattern (Last Year)')
        ax1.set_ylabel('Amount')
        ax1.set_xlabel('Week')
        ax1.grid(True)
        st.pyplot(fig1)

    with c2:
        # ----------- Monthly Withdrawals vs Deposits -----------
        st.header("Monthly Spending Pattern:")
        df_copy = df.copy()
        df_copy['DATE'] = pd.to_datetime(df_copy['DATE'], errors='coerce')
        monthly = df_copy.resample('ME', on='DATE')[['WITHDRAWAL AMT', 'DEPOSIT AMT']].sum()
        st.subheader("Monthly Chart")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        monthly.plot(marker='o', color=['red', 'green'], ax=ax2)
        ax2.set_title('Monthly Spending Pattern: Withdrawals vs Deposits')
        ax2.set_ylabel('Amount')
        ax2.set_xlabel('Month')
        ax2.grid(True)
        st.pyplot(fig2)

    c3,c4 = st.columns(2)
    with c3:
        #Histogram of Withdrawals by Category
        st.header("Withdrawal Amount Distribution by Category (Log-Scaled)")

        w = df[df['WITHDRAWAL AMT'] > 0].copy()
        w.rename(columns={'WITHDRAWAL AMT': 'amount'}, inplace=True)
        categories = w['Category'].unique()
        min_amt = w['amount'].min()
        max_amt = w['amount'].max()
        bins = np.logspace(np.log10(min_amt + 1), np.log10(max_amt), 25)

        fig3, ax3 = plt.subplots(figsize=(10, 6))
        for cat in categories:
            data = w[w['Category'] == cat]['amount']
            ax3.hist(data, bins=bins, alpha=0.5, label=cat, edgecolor='black')

        ax3.set_xscale('log')
        ax3.set_xlabel('Withdrawal Amount (₹)')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Withdrawal Amount Distribution by Category (Log-Scaled)')
        ax3.legend(title='Category')
        st.pyplot(fig3)

    with c4:
        #Boxplot by Category
        st.header("Boxplot of Withdrawals by Category (Log Scale)")

        fig4, ax4 = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=w, x='Category', y='amount', ax=ax4)
        ax4.set_yscale('log')
        ax4.set_title('Boxplot of Withdrawals by Category (Log Scale)')
        ax4.tick_params(axis='x', rotation=45)
        st.pyplot(fig4)
