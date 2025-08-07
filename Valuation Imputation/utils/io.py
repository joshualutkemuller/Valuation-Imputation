import pandas as pd
from config import SUPPORTED_FORMATS

def load_data(filepath):
    """
    Load data from a file based on its extension.
    Supported formats: .csv, .xlsx, .xls, .parquet
    """
    ext = str(filepath).lower().split(".")[-1]

    if ext == "csv":
        return pd.read_csv(filepath, parse_dates=["date"])
    elif ext in ["xlsx", "xls"]:
        return pd.read_excel(filepath, parse_dates=["date"])
    elif ext == "parquet":
        return pd.read_parquet(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}")