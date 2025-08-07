
from utils.aliases import get_field_mapping
import numpy as np
import pandas as pd

def generate_stacked_pe_sensitivity(
    df: pd.DataFrame,
    valuation_basis: str = "trailing"
) -> pd.DataFrame:
    """
    Generate a stacked long-skinny format table of implied index levels and returns
    from P/E ratio scenarios using a specified EPS type (trailing, fwd_1y, fwd_2y).
    Adds columns: 'MetricType', 'Value', and 'Current Index Level'.
    """

    mapping = get_field_mapping()
    pe_col = mapping.get(f"pe_{valuation_basis}", f"pe_{valuation_basis}")
    eps_col = mapping.get(f"eps_{valuation_basis}", f"eps_{valuation_basis}")
    benchmark_col = mapping.get("benchmark_id", "benchmark_id")

    rows = []

    for _, row in df.iterrows():
        benchmark = row.get(benchmark_col)
        eps = row.get(eps_col)
        current_pe = row.get(pe_col)

        if pd.isna(eps) or pd.isna(current_pe):
            continue

        current_price = eps * current_pe
        pe_range = np.arange(int(current_pe) - 50, int(current_pe) + 51, 1)

        for pe in pe_range:
            if pe <= 0:
                continue  # skip invalid P/E values

            implied_price = eps * pe
            implied_return = (implied_price / current_price) - 1 if current_price else None

            rows.append({
                "Benchmark": benchmark,
                "EPS Type": valuation_basis,
                "Current EPS": eps,
                "Current PE": current_pe,
                "Current Index Level": current_price,
                "PE Scenario": pe,
                "Value": implied_price,
                "MetricType": "Implied Index Level"
            })

            rows.append({
                "Benchmark": benchmark,
                "EPS Type": valuation_basis,
                "Current EPS": eps,
                "Current PE": current_pe,
                "Current Index Level": current_price,
                "PE Scenario": pe,
                "Value": implied_return * 100 if implied_return is not None else None,
                "MetricType": "Implied Return (%)"
            })

    result = pd.DataFrame(rows)
    return result
def generate_wide_custom_pe_sensitivity(
    df: pd.DataFrame,
    valuation_basis: str = "trailing"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate long-format sensitivity matrices around each benchmark's current P/E ratio,
    using a dynamic valuation basis: 'trailing', 'fwd_1y', 'fwd_2y'.
    """
    result_returns = []
    result_prices = []

    mapping = get_field_mapping()
    pe_col = mapping.get(f"pe_{valuation_basis}", f"pe_{valuation_basis}")
    print(pe_col)
    eps_col = mapping.get(f"eps_{valuation_basis}", f"eps_{valuation_basis}")
    benchmark_col = mapping.get("benchmark_id", "benchmark_id")

    for _, row in df.iterrows():
        benchmark = row.get(benchmark_col)
        eps = row.get(eps_col)
        current_pe = row.get(pe_col)
        print(eps)
        if pd.isna(eps) or pd.isna(current_pe):
            continue

        current_price = eps * current_pe
        pe_range = np.arange(int(current_pe) - 50, int(current_pe) + 51, 1)
        print(current_price, pe_range)
        for pe in pe_range:
            if pe <= 0:
                continue  # Skip invalid P/E values

            implied_price = eps * pe
            implied_return = (implied_price / current_price) - 1 if current_price else None

            result_returns.append({
                "Benchmark": benchmark,
                "EPS Type": valuation_basis,
                "Current EPS": eps,
                "Current PE": current_pe,
                "PE Scenario": pe,
                "Implied Return (%)": implied_return * 100 if implied_return is not None else None
            })

            result_prices.append({
                "Benchmark": benchmark,
                "EPS Type": valuation_basis,
                "Current EPS": eps,
                "Current PE": current_pe,
                "PE Scenario": pe,
                "Implied Index Level": implied_price
            })

    df_returns = pd.DataFrame(result_returns)
    df_prices = pd.DataFrame(result_prices)

    return df_returns, df_prices


def melt_pe_eps(df):
    FIELD_NAME_MAP = get_field_mapping()

    id_vars = [
        FIELD_NAME_MAP.get("date", "date"),
        FIELD_NAME_MAP.get("benchmark_id", "benchmark_id")
    ]
    value_vars = [col for col in df.columns if any(p in col.lower() for p in ["pe", "eps"])]

    missing = [col for col in id_vars if col not in df.columns]
    if missing:
        raise ValueError(f"Missing ID columns in melt_pe_eps: {missing}")

    return df.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name="Metric",
        value_name="Value"
    )


def pivot_to_matrix(df: pd.DataFrame, value_type="eps", horizon="1y") -> pd.DataFrame:
    """
    Create a matrix of values for a given value type (EPS or PE) and horizon.
    For example, all `eps_fwd_1y` values by benchmark × date.
    """
    filtered = df[
        df["metric"].str.contains(value_type, case=False) &
        df["metric"].str.contains(horizon, case=False)
    ]
    return filtered.pivot(index="benchmark_id", columns="date", values="value")
