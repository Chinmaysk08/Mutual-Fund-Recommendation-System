
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# Project paths
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
DATASET_PATH = PROJECT_DIR / "Dataset" / "mutual_funds_data.csv"


def load_and_clean_data():
    """Load the original mutual fund dataset and clean its columns."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    df_clean = df.copy()

    # Replace hyphens with missing values
    df_clean.replace("-", np.nan, inplace=True)

    # Convert numerical columns
    numeric_columns = [
        "min_sip",
        "min_lumpsum",
        "expense_ratio",
        "fund_size_cr",
        "fund_age_yr",
        "sortino",
        "alpha",
        "sd",
        "beta",
        "sharpe",
        "risk_level",
        "rating",
        "returns_1yr",
        "returns_3yr",
        "returns_5yr"
    ]

    for col in numeric_columns:
        df_clean[col] = pd.to_numeric(
            df_clean[col],
            errors="coerce"
        )

    return df, df_clean
