import pandas as pd

def compute_pe_z_scores(df: pd.DataFrame) -> pd.DataFrame:
    horizons = ["1", "3", "5", "7", "10", "15", "20"]
    pe_types = ["pe_trailing", "pe_fwd_1y", "pe_fwd_2y"]

    output = []

    for _, row in df.iterrows():
        for pe_type in pe_types:
            current_val = row[pe_type]
            for h in horizons:
                avg_col = f"{pe_type}_avg_{h}y"
                std_col = f"{pe_type}_std_{h}y"

                if avg_col in row and std_col in row and pd.notna(row[avg_col]) and pd.notna(row[std_col]):
                    z = (current_val - row[avg_col]) / row[std_col] if row[std_col] != 0 else None
                    output.append({
                        "Benchmark": row["benchmark_id"],
                        "Date": row["date"],
                        "PE_Type": pe_type,
                        "Horizon": h,
                        "Current_Value": current_val,
                        "Avg_Value": row[avg_col],
                        "Std_Dev": row[std_col],
                        "Z_Score": z
                    })

    return pd.DataFrame(output)
