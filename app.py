import streamlit as st
import datetime
from data_munger import load_and_munge
from utils import filter_by_date
from categorizer import categorize_dataframe, plot_category_distribution
import pandas as pd
from spending_pattern import analyze_spending
from recommendations import show_category_recommendations

st.set_page_config(
    page_title="Personal Finance Dashboard",
    layout="wide",     
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Grid container stays the same */
.category-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 1rem;
}

/* Dark-mode cards */
.rec-card {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-radius: 12px;
  background-color: #1e1e1e;      /* dark grey */
  border: 1px solid #333333;      /* slightly lighter grey */
  color: #e0e0e0;                 /* light text */
  margin-bottom: 5px;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.rec-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  transform: translateY(-3px);
}

/* Icon styling */
.rec-icon {
  font-size: 1.6rem;
  margin-right: 0.75rem;
  line-height: 1;
  color: #ffd700;                 /* gold/yellow accent */
}

/* Text block */
.rec-body {
  flex: 1;
  font-size: 0.95rem;
  line-height: 1.4;
}

/* Expander header */
.stExpander > .streamlit-expanderHeader {
  font-weight: 600;
  color: #ffffff;
  background-color: #2b2b2b;
  border: 1px solid #444444;
  border-radius: 6px;
  padding: 0.5rem 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("Personal Finance Dashboard")

dff = load_and_munge(path="transactions.xlsx")



min_date = datetime.date(2015, 1, 1)
max_date = datetime.date(2019, 3, 5)
start_date, end_date = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)
if start_date > end_date:
    st.sidebar.error("Start date must be ≤ end date")
    st.stop()
max_recs = st.sidebar.slider(
    label="How many top suggestions to show?",
    min_value=1,
    max_value=10,
    value=2,
    help="Use this slider to adjust how many cards you see before you have to expand."
)
df = filter_by_date(dff, start_date, end_date)



st.markdown("## Overview")
col1, col2, col3, col4 = st.columns(4, gap="large")

total_txn = len(df)
total_spent = df['WITHDRAWAL AMT'].sum()
total_received = df['DEPOSIT AMT'].sum()
avg_txn     = df['WITHDRAWAL AMT'].mean()

col1.metric("Total Transitions:", f"{total_txn:,}")
col2.metric("Total Spent:", f"₹{total_spent:,.0f}")
col3.metric("Total Received:", f"₹{total_received:,.0f}")
col4.metric("Avg. Spent per transition:", f"₹{avg_txn:,.0f}")



df = categorize_dataframe(df)

tab1, tab2,tab3 = st.tabs(["📊 Categories", "📈 Spending Pattern","Suggestions"])

with tab1:
    st.markdown("### Transactions by Category")
    plot_category_distribution(df)

with tab2:
    df_copy = df.copy()
    df_copy['DATE'] = pd.to_datetime(df_copy['DATE'], errors='coerce')
    weekly = df_copy.resample('W-MON', on='DATE')[['WITHDRAWAL AMT', 'DEPOSIT AMT']].sum()
    analyze_spending(df, weekly)


with tab3:
    show_category_recommendations(df, max_recs)



with st.expander("Show raw transactions data"):
    st.dataframe(df)

