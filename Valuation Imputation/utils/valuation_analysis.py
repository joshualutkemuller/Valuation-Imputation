import pandas as pd

def calculate_price_impact(df: pd.DataFrame, valuation_basis: str = "trailing") -> pd.DataFrame:
    eps_col = f"eps_{valuation_basis}"
    pe_col = f"pe_{valuation_basis}"

    if eps_col not in df.columns or pe_col not in df.columns:
        raise KeyError(f"Missing required columns: {eps_col} or {pe_col}")

    df = df.copy()
    df["Implied_Price"] = df[eps_col] * df[pe_col]

    if df["Implied_Price"].notna().any():
        base_price = df["Implied_Price"].dropna().iloc[0]
        df["Base_Price"] = base_price
        df["Implied_Return"] = df["Implied_Price"] / base_price - 1
    else:
        df["Base_Price"] = None
        df["Implied_Return"] = None

    return df


def create_return_matrix(df):
    """
    Pivot implied return into a matrix: benchmark_id × date
    """
    return df.pivot(index="benchmark_id", columns="date", values="Implied_Return")
