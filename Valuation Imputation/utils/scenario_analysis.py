import pandas as pd
import numpy as np

def generate_pe_scenario_tables(base_pe, change_range=np.linspace(-0.2, 0.2, 9)):
    pct_labels = [f"{int(c*100)}%" for c in change_range]
    abs_vals = [base_pe * (1 + c) for c in change_range]
    df_pct = pd.DataFrame({"PE Change (%)": pct_labels, "PE Value": abs_vals})
    df_abs = pd.DataFrame({"PE Value": abs_vals}, index=pct_labels)
    return df_pct, df_abs

def generate_eps_scenario_tables(base_eps, change_range=np.linspace(-0.2, 0.2, 9)):
    data = []
    for c in change_range:
        eps_val = base_eps * (1 + c)
        flag = "Current" if np.isclose(c, 0.0) else "What-if"
        data.append({"EPS Change (%)": f"{int(c*100)}%", "EPS Value": eps_val, "Scenario": flag})
    return pd.DataFrame(data)

def generate_combined_long_format(base_eps, base_pe,
                                  eps_changes=np.linspace(-0.2, 0.2, 5),
                                  pe_changes=np.linspace(-0.2, 0.2, 5)):
    base_price = base_eps * base_pe
    scenarios = []
    for e in eps_changes:
        for p in pe_changes:
            eps = base_eps * (1 + e)
            pe = base_pe * (1 + p)
            price = eps * pe
            ret = (price / base_price) - 1
            flag = "Current" if (np.isclose(e, 0.0) and np.isclose(p, 0.0)) else "What-if"
            scenarios.append({
                "EPS Change (%)": f"{int(e*100)}%",
                "PE Change (%)": f"{int(p*100)}%",
                "EPS Value": eps,
                "PE Value": pe,
                "Implied Price": price,
                "Implied Return": ret,
                "Scenario": flag
            })
    return pd.DataFrame(scenarios)

def generate_cross_basis_scenarios(row: pd.Series) -> list[dict]:
    """
    Generate combined EPS × PE scenarios for a single benchmark row.
    Includes original EPS, PE, Index, and type metadata for each basis.
    """
    benchmark = row.get("benchmark_id") or row.get("Benchmark")
    scenarios = []

    for basis in ["trailing", "fwd_1y", "fwd_2y"]:
        eps_key = f"eps_{basis}"
        pe_key = f"pe_{basis}"

        eps = row.get(eps_key)
        pe = row.get(pe_key)

        if pd.isna(eps) or pd.isna(pe) or eps <= 0 or pe <= 0:
            continue

        base_price = eps * pe
        eps_change_range = np.arange(-0.5, 0.55, 0.1)   # -50% to +50%
        pe_change_range = np.arange(-0.5, 0.55, 0.1)

        for eps_chg in eps_change_range:
            for pe_chg in pe_change_range:
                adj_eps = eps * (1 + eps_chg)
                adj_pe = pe * (1 + pe_chg)
                implied_price = adj_eps * adj_pe
                implied_return = (implied_price / base_price) - 1 if base_price else None

                scenarios.append({
                    "Benchmark": benchmark,
                    "EPS Type": basis,
                    "PE Type": basis,
                    "EPS Change (%)": eps_chg * 100,
                    "PE Change (%)": pe_chg * 100,
                    "Adjusted EPS": adj_eps,
                    "Adjusted PE": adj_pe,
                    "Implied Index Level": implied_price,
                    "Implied Return (%)": implied_return * 100 if implied_return is not None else None,

                    # Actual Current Levels
                    "Current EPS": eps,
                    "Current PE": pe,
                    "Current Index Level": base_price
                })

    return scenarios


def generate_cross_basis_scenarios_with_rates(row: pd.Series) -> list[dict]:
    """
    Generate combined EPS × PE × Interest Rate scenarios for a single benchmark row.
    Includes metadata like type, current EPS/PE/Price, and interest rate.
    """
    benchmark = row.get("benchmark_id") or row.get("Benchmark")
    current_rate = row.get("current_interest_rate") or row.get("Current Interest Rate") # Make sure this field is in your data
    print(current_rate)
    if pd.isna(current_rate):
        return []  # Skip if no current interest rate

    scenarios = []

    # Iterate over each valuation basis
    for basis in ["trailing", "fwd_1y", "fwd_2y"]:
        eps_key = f"eps_{basis}"
        pe_key = f"pe_{basis}"

        eps = row.get(eps_key)
        pe = row.get(pe_key)
        print(eps,pe)
        if pd.isna(eps) or pd.isna(pe) or eps <= 0 or pe <= 0:
            continue

        base_price = eps * pe

        # EPS and PE changes
        eps_change_range = np.arange(-0.5, 0.55, 0.1)   # -50% to +50%
        pe_change_range = np.arange(-0.5, 0.55, 0.1)

        # Interest rate changes in basis points
        rate_change_range = np.arange(-200, 225, 25)  # -200 to +200 bps in 25 bps steps

        for eps_chg in eps_change_range:
            for pe_chg in pe_change_range:
                for rate_chg in rate_change_range:
                    adj_eps = eps * (1 + eps_chg)
                    adj_pe = pe * (1 + pe_chg)
                    implied_price = adj_eps * adj_pe
                    implied_return = (implied_price / base_price) - 1 if base_price else None

                    scenarios.append({
                        "Benchmark": benchmark,
                        "EPS Type": basis,
                        "PE Type": basis,

                        # Scenario deltas
                        "EPS Change (%)": eps_chg * 100,
                        "PE Change (%)": pe_chg * 100,
                        "Interest Rate Change (bps)": rate_chg,

                        # Adjusted values
                        "Adjusted EPS": adj_eps,
                        "Adjusted PE": adj_pe,
                        "Adjusted Interest Rate": current_rate + rate_chg / 100.0,  # convert bps to %
                        "Implied Index Level": implied_price,
                        "Implied Return (%)": implied_return * 100 if implied_return is not None else None,

                        # Current baseline values
                        "Current EPS": eps,
                        "Current PE": pe,
                        "Current Index Level": base_price,
                        "Current Interest Rate": current_rate
                    })

    return scenarios
