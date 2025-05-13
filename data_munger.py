import os
import pandas as pd
import numpy as np
import streamlit as st

# Path to store the fast-load parquet file
PARQUET_PATH = "transactions.parquet"

@st.cache_data
def load_raw_excel(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, dtype=str)
    return df

@st.cache_data
def load_raw_parquet(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)

@st.cache_data
def load_and_munge(path: str) -> pd.DataFrame:    
    if os.path.exists(PARQUET_PATH):
        df = load_raw_parquet(PARQUET_PATH)
    else:
        df = load_raw_excel(path)

        df = df.dropna(subset=['DATE'])

        df['TRANSACTION DETAILS'] = df['TRANSACTION DETAILS'].fillna('Miscellaneous')
        df['CHQ.NO.'] = df.get('chq_no', pd.Series(dtype=str)).fillna('NA')

        amt_cols = ['WITHDRAWAL AMT', 'DEPOSIT AMT', 'BALANCE AMT']
        for c in amt_cols:
            df[c] = (
                df[c]
                  .fillna('')             
                  .astype(str)
                  .str.replace(r'[\s,]', '', regex=True)
                  .replace({'': np.nan})
                  .astype(float)
            )

        
        df[['WITHDRAWAL AMT', 'DEPOSIT AMT']] = df[['WITHDRAWAL AMT', 'DEPOSIT AMT']].fillna(0.0)

        df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.date
        df['VALUE DATE'] = pd.to_datetime(df['VALUE DATE'], errors='coerce').dt.date
        df = df.sort_values('DATE').reset_index(drop=True)

        net = df['DEPOSIT AMT'] - df['WITHDRAWAL AMT']

        net = df['DEPOSIT AMT'] - df['WITHDRAWAL AMT']

        df['BALANCE AMT'] = net.cumsum()

        df.to_parquet(PARQUET_PATH, index=False)

    return df
