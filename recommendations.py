import streamlit as st
import pandas as pd

# Your essential categories set
ESSENTIAL_CATEGORIES = {
    "Transfers", "Loans & EMI", "Fees & Charges",
    "Utilities & Telecom", "Salary & Income", "Insurance",
    "Payments", "Miscellaneous"
}

def generate_category_recs(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each discretionary category, computes total spend,
    its % of total discretionary, and attaches a tailored recommendation.
    Returns a DataFrame with:
      ['Category', 'Total Spend', 'Pct of Discretionary', 'Recommendation']
    """
    # 1) Clean and filter discretionary
    df = df.copy()
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    df = df.dropna(subset=['DATE'])
    mask = (~df['Category'].isin(ESSENTIAL_CATEGORIES)) & (df['WITHDRAWAL AMT'] > 0)
    disc = df.loc[mask].copy()
    if disc.empty:
        return pd.DataFrame(columns=[
            'Category','Total Spend','Pct of Discretionary','Recommendation'
        ])

    # 2) Compute totals
    summary = (
        disc.groupby('Category')['WITHDRAWAL AMT']
            .sum()
            .reset_index(name='Total Spend')
    )
    total_disc = summary['Total Spend'].sum()
    summary['Pct of Discretionary'] = (summary['Total Spend'] / total_disc * 100)

    # 3) Build smart rec per category
    def make_rec(row):
        pct = row['Pct of Discretionary']
        total = row['Total Spend']
        cat = row['Category']

        # high-burn if > 30% of discretionary
        if pct > 30:
            return (
                f"You’re spending **{pct:.0f}%** of all discretionary in **{cat}** "
                f"(₹{total:,.0f}). Consider setting a strict cap here."
            )
        # above-average if > mean%
        mean_pct = 100.0 / len(summary)
        if pct > mean_pct:
            cap = total * 0.9
            return (
                f"**{cat}** is above average at **{pct:.0f}%** of discretionary. "
                f"Try reducing by 10% (cap at ₹{cap:,.0f})."
            )
        # well-controlled if small slice
        return (
            f"**{cat}** is well-controlled at just **{pct:.0f}%** (~₹{total:,.0f}). "
            "Keep it up!"
        )

    summary['Recommendation'] = summary.apply(make_rec, axis=1)

    # 4) Sort by Total Spend descending
    return summary.sort_values('Total Spend', ascending=False)

def show_category_recommendations(df: pd.DataFrame, max_recs: int = 3) -> None:
    """
    Displays the top `max_recs` discretionary categories with styled cards.
    """
    st.header("🧠 Category-Level Insights")
    cat_recs = generate_category_recs(df)
    if cat_recs.empty:
        st.info("No discretionary spending found in this period.")
        return

    # Build a grid container
    st.markdown("<div class='category-cards'>", unsafe_allow_html=True)

    # Top N cards
    for _, row in cat_recs.head(max_recs).iterrows():
        pct = row['Pct of Discretionary']
        total = row['Total Spend']
        cat = row['Category']
        rec = row['Recommendation']

        # Choose icon by recommendation type
        icon = "🔥" if pct > 30 else ("⚠️" if pct > (100.0/len(cat_recs)) else "✅")

        card_html = f"""
        <div class='rec-card'>
          <div class='rec-icon'>{icon}</div>
          <div class='rec-body'>{rec}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # “Show more” expander with same grid logic
    if len(cat_recs) > max_recs:
        with st.expander("🔍 Show more category insights"):
            st.markdown("<div class='category-cards'>", unsafe_allow_html=True)
            for _, row in cat_recs.iloc[max_recs:].iterrows():
                pct = row['Pct of Discretionary']
                rec = row['Recommendation']
                icon = "🔥" if pct > 30 else ("⚠️" if pct > (100.0/len(cat_recs)) else "✅")
                st.markdown(f"""
                  <div class='rec-card'>
                    <div class='rec-icon'>{icon}</div>
                    <div class='rec-body'>{rec}</div>
                  </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)