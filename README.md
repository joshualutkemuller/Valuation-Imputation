
# Valuation Imputation Project

This project generates sensitivity matrices for equity valuation based on different Price-to-Earnings (P/E) scenarios and optionally adjusts for changes in interest rates.

## Key Features

- Calculates **implied index price and return** using static EPS and varying P/E levels.
- Generates long-form DataFrames for both **price and return sensitivity** under different valuation bases (Trailing, NTM, 2Y Fwd).
- Supports **interest rate scenario analysis** by incorporating basis point shifts.
- Stack both return and price matrices into a single tidy DataFrame.
- Tracks and records baseline EPS, PE, and index values for clarity in interpretation.

## Functions

### `generate_pe_scenarios(row)`
Generates different implied prices and returns assuming EPS stays constant and P/E changes ±50 in steps of 1.

### `generate_stacked_pe_sensitivity(df)`
Combines the return and price sensitivity matrices into one long, skinny DataFrame with an additional column identifying the type (`Implied Return (%)` or `Implied Index Level`).

### `generate_cross_basis_scenarios(row)`
Creates a matrix for EPS × PE interactions (±50% in steps of 10%) and calculates the resulting implied return and price.

### `generate_cross_basis_scenarios_with_rates(row)`
Same as above, but adds another dimension—**interest rate shocks** (from -200 to +200 bps). Includes metadata for current EPS, PE, price, and rate.

## Usage

Prepare your input DataFrame with the following columns:

- `benchmark_id`
- `eps_trailing`, `pe_trailing`
- `eps_fwd_1y`, `pe_fwd_1y`
- `eps_fwd_2y`, `pe_fwd_2y`
- `current_interest_rate` (if running rate-sensitive scenarios)

Then apply:

```python
df.apply(generate_pe_scenarios, axis=1)
df.apply(generate_cross_basis_scenarios, axis=1)
df.apply(generate_cross_basis_scenarios_with_rates, axis=1)
```

## Output

All outputs are tidy `pd.DataFrame`s that can be saved as CSVs or visualized. Return and price matrices are stacked for easy plotting with fields like:

- `EPS Type`
- `PE Type`
- `Implied Index Level`
- `Implied Return (%)`
- `Current PE`, `Current EPS`, `Current Index Level`
- `Interest Rate Change (bps)` (if applicable)

## Requirements

See `requirements.txt` for dependencies.
