import pandas as pd
from pathlib import Path

def format_alias(name: str) -> str:
    name = name.replace("_", " ")
    name = name.replace("eps", "EPS").replace("pe", "P/E")
    name = name.replace("avg", "Avg").replace("std", "Std")
    return name.title()

def generate_alias_template(input_csv="sample_indices.csv", output_csv="column_aliases.csv"):
    # Load dataset
    df = pd.read_csv(input_csv)

    # Build alias dictionary
    aliases = {
        col: format_alias(col)
        for col in df.columns
    }

    # Create dataframe for editable CSV
    alias_df = pd.DataFrame(list(aliases.items()), columns=["original", "new_name"])

    # Save to file
    alias_df.to_csv(output_csv, index=False)
    print(f"✅ Alias file created: {output_csv}")

if __name__ == "__main__":
    generate_alias_template()
