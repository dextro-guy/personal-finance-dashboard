import pandas as pd
import datetime

def filter_by_date(df: pd.DataFrame,
                   start_date: datetime.date,
                   end_date: datetime.date,
                   date_col: str = 'DATE'
                  ) -> pd.DataFrame:

    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
    
    mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
    return df.loc[mask].reset_index(drop=True)
