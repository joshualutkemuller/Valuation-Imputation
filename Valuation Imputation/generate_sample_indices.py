import pandas as pd
from pathlib import Path
import os


def generate_sample_indices_csv(filename="sample_indices.csv",relative_dir = None,verbose=False):
    # Write to the current working directory
    if relative_dir is None:
        output_path = Path(os.getcwd())  / filename
    else:
        output_path = Path(os.getcwd()) / 'data' / filename

    if verbose:
        print(f"Output path: {output_path}")

    horizons = [1, 3, 5, 7, 10, 15, 20]

    data = {
        "date": ["2025-08-05"] * 3,
        "benchmark_id": ["S&P 500", "Russell 2000", "FTSE All‑World"],
        "eps_trailing": [225.0, 145.0, 14.0],
        "pe_trailing": [27.8, 20.0, 18.0],
        "eps_fwd_1y": [312.0, 164.0, 18.0],
        "pe_fwd_1y": [22.56, 17.92, 16.5],
        "eps_fwd_2y": [340.0, 180.0, 20.0],
        "pe_fwd_2y": [21.5, 16.7, 15.8],
        "current_interest_rate":[4.25,4.25,4.25]
    }

    for pe_type, avg_vals, std_vals in [
        ("pe_trailing", [25.0, 18.0, 17.0], [2.0, 1.5, 1.2]),
        ("pe_fwd_1y", [20.0, 17.0, 16.0], [1.8, 1.2, 1.0]),
        ("pe_fwd_2y", [19.0, 16.5, 15.5], [1.7, 1.1, 0.9]),
    ]:
        for h in horizons:
            data[f"{pe_type}_avg_{h}y"] = avg_vals
            data[f"{pe_type}_std_{h}y"] = std_vals

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Sample CSV written to {output_path}")

if __name__ == "__main__":
    generate_sample_indices_csv(relative_dir="data",verbose=True)
