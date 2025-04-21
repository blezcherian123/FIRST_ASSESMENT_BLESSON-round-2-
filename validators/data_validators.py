import pandas as pd

def required_columns_present(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    return missing

def validate_date_column(df, date_col):
    try:
        pd.to_datetime(df[date_col])
        return True
    except:
        return False

def high_value_transactions(df, amount_col='amount', threshold=10000):
    if amount_col in df.columns:
        return df[df[amount_col] > threshold]
    return pd.DataFrame()
