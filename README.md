````markdown
# 📊 Personal Finance Dashboard

**A Streamlit application that transforms your raw transaction data into actionable insights, visualizations, and budget recommendations.**

---

## 🔍 Overview
This tool ingests your banking transactions (from Excel), categorizes each entry, analyzes spending patterns, and suggests budget adjustments.

- **Transaction Categorization**: Automatic keyword-based tagging (e.g., Utilities, Entertainment, Salary).
- **Spending Analysis**: Weekly and monthly trends, histograms (log scale), boxplots by category.
- **Budget Recommendations**: Tailored advice on discretionary categories.
- **Interactive Dashboard**: Date-range filters, dynamic metrics, and drill-down on raw data.

---

## 🛠️ Tech Stack

- **Python** 3.8+
- **Streamlit** (UI & dashboard)
- **Pandas & NumPy** (data processing)
- **Matplotlib & Seaborn** (charting)
- **Parquet** (optimized data caching)

---

## 🗂️ Project Structure

```bash
personal-finance-dashboard/
├── transactions.xlsx        # Raw transaction data (Excel)
├── transactions.parquet     # Cached Parquet for faster reloads
├── dashboard.py             # Streamlit app entrypoint
├── data_munger.py           # Data loading & cleaning utilities
├── categorizer.py           # Transaction categorization logic
├── spending_pattern.py      # Charts & spending analysis functions
├── recommendations.py       # Discretionary-spend recommendations
├── utils.py                 # Helper functions (e.g., date filtering)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🚀 Installation & Setup

1. **Clone the repo**

   ```bash
   git clone https://github.com/<your-username>/personal-finance-dashboard.git
   cd personal-finance-dashboard
   ```

2. **(Optional) Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate.bat   # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your data**

   * Place `transactions.xlsx` in the project root or update the path in `dashboard.py`.

---

## ▶️ Usage

Launch the dashboard:

```bash
streamlit run dashboard.py
```

Visit `http://localhost:8501` in your browser.

---

## 📐 Methodology

1. **Data Munging** (`data_munger.py`)

   * Reads Excel or Parquet cache
   * Cleans/normalizes columns, computes running balances

2. **Categorization** (`categorizer.py`)

   * Applies keyword-map to transaction details
   * Fallback to `Others` for uncategorized entries

3. **Spending Analysis** (`spending_pattern.py`)

   * Aggregates weekly/monthly spend vs. deposit
   * Generates time-series plots, histograms (log-scaled), boxplots

4. **Recommendations** (`recommendations.py`)

   * Filters non-essential categories
   * Computes each category’s share of discretionary spending
   * Produces tiered suggestions (strict cap, small reduction, maintain)

5. **Dashboard Layout** (`dashboard.py`)

   * Sidebar: date-picker + recommendation count slider
   * Overview metrics: total transactions, total spent/received, avg. spend
   * Tabs: Categories, Spending Pattern, Suggestions, Raw Data

---

## ⭐ Future Enhancements

* OCR integration for receipt parsing
* Multi-user support & authentication
* Machine Learning–driven categorization
* Exportable reports (PDF, CSV)

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request.

---

## 📬 Contact

Questions? Reach me at [your.email@domain.com](mailto:your.email@domain.com).

```
```
"# personal-finance-dashboard" 
