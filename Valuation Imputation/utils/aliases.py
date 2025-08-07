# utils/aliases.py

import pandas as pd
from config import USE_EXTERNAL_MAPPING, MAPPING_PATH


def get_field_mapping():
    if USE_EXTERNAL_MAPPING:
        try:
            df = pd.read_csv(MAPPING_PATH)
            return dict(zip(df["original"], df["new_name"]))
        except Exception as e:
            print(f"⚠️ Failed to load external mapping. Falling back to default. Error: {e}")

    from utils.field_mappings import FIELD_NAME_MAP
    return FIELD_NAME_MAP


def rename_columns(df):
    return df.rename(columns=get_field_mapping())
