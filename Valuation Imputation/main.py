from config import DATA_DIR, OUTPUT_DIR
from utils.aliases import rename_columns
from utils.io import load_data
from utils.transform import melt_pe_eps, pivot_to_matrix,generate_wide_custom_pe_sensitivity, generate_stacked_pe_sensitivity
from utils.valuation_analysis import calculate_price_impact, create_return_matrix
from utils.scenario_analysis import (
    generate_pe_scenario_tables,
    generate_eps_scenario_tables,
    generate_combined_long_format,
    generate_cross_basis_scenarios,
    generate_cross_basis_scenarios_with_rates
)
from utils.valuation_diagnostics import compute_pe_z_scores
import pandas as pd
import os
import logging

# --------------------------------------------
# 1. Setup working directory and logging
# --------------------------------------------
os.chdir(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info(f"Working directory set to: {os.getcwd()}")
def generate_and_save_cross_basis(df):
    all_scenarios = []
    for _, row in df.iterrows():
        scenarios = generate_cross_basis_scenarios(row)
        all_scenarios.extend(scenarios)
    result = pd.DataFrame(all_scenarios)
    result.to_csv(OUTPUT_DIR / "cross_basis_scenarios.csv", index=False)

def generate_and_save_cross_basis_with_rates(df):
    all_scenarios = []
    for _, row in df.iterrows():
        scenarios = generate_cross_basis_scenarios_with_rates(row)
        all_scenarios.extend(scenarios)
    result = pd.DataFrame(all_scenarios)
    result.to_csv(OUTPUT_DIR / "cross_basis_scenarios_with_rates.csv", index=False)

def main():
    # Either hardcode this or find the first CSV file in /data
    file_path = DATA_DIR / "sample_indices.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Raw Data
    df = load_data(file_path)

    # Raw Data with Clean Names
    df_clean = rename_columns(df)
    df_clean.to_csv(OUTPUT_DIR / "raw_clean_names.csv", index=False)

    for basis in ["trailing", "fwd_1y", "fwd_2y"]:
        prefix = f"scenario_{basis}"
        df_impact = calculate_price_impact(df, valuation_basis=basis)
        print(df_impact.columns)
        print(df_impact.head())

        df_impact.to_csv(OUTPUT_DIR / f"{prefix}_impact.csv", index=False)

        return_matrix = create_return_matrix(df_impact)
        return_matrix.to_csv(OUTPUT_DIR / f"{prefix}_return_matrix.csv")

        base = df.iloc[0]
        base_eps = base[f"eps_{basis}"]
        base_pe = base[f"pe_{basis}"]

        pe_pct, pe_abs = generate_pe_scenario_tables(base_pe)
        pe_pct.to_csv(OUTPUT_DIR / f"{prefix}_pe_pct.csv", index=False)
        pe_abs.to_csv(OUTPUT_DIR / f"{prefix}_pe_abs.csv")

        eps_tbl = generate_eps_scenario_tables(base_eps)
        eps_tbl.to_csv(OUTPUT_DIR / f"{prefix}_eps_scenarios.csv", index=False)

        combined = generate_combined_long_format(base_eps, base_pe)
        combined.to_csv(OUTPUT_DIR / f"{prefix}_combined.csv", index=False)

    generate_and_save_cross_basis(df)

    z_df = compute_pe_z_scores(df)
    z_df = rename_columns(z_df)
    z_df.to_csv(OUTPUT_DIR / "pe_z_scores.csv", index=False)

    # PowerBI Friendly Format
    long_df = melt_pe_eps(df_clean)
    long_df.to_csv(OUTPUT_DIR / "long_format_eps_pe.csv", index=False)

    # Generate Wide Custom PE Sensitivity
    custom_pe_sensitivity_return_df, custom_pe_sensitivity_price_df = generate_wide_custom_pe_sensitivity(df_clean)
    custom_pe_sensitivity_return_df.to_csv(OUTPUT_DIR / "wide_custom_pe_sensitivity_return.csv", index=False)
    custom_pe_sensitivity_price_df.to_csv(OUTPUT_DIR / "wide_custom_pe_sensitivity_price.csv", index=False)

    custom_pe_stacked_sensitivity_df = generate_stacked_pe_sensitivity(df_clean)
    custom_pe_stacked_sensitivity_df.to_csv(OUTPUT_DIR / "stacked_pe_sensitivity.csv", index=False)

    # Generate and save cross basis with rates
    generate_and_save_cross_basis_with_rates(df)

if __name__ == "__main__":
    main()
