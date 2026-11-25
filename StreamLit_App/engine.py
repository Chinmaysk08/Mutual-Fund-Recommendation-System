
from pathlib import Path
from io import BytesIO

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "Dataset" / "mutual_funds_data.csv"

NUMERIC_COLUMNS = [
    "min_sip", "min_lumpsum", "expense_ratio", "fund_size_cr",
    "fund_age_yr", "sortino", "alpha", "sd", "beta", "sharpe",
    "risk_level", "rating", "returns_1yr", "returns_3yr", "returns_5yr"
]

SCORING_COLUMNS = [
    "returns_3yr", "expense_ratio", "fund_age_yr", "returns_1yr"
]

RISK_COLUMNS = ["sortino", "alpha", "sd", "beta", "sharpe"]


def load_and_clean_data(csv_path=DATASET_PATH):
    """Load the original dataset and convert numeric columns."""
    df = pd.read_csv(csv_path)
    df_clean = df.copy()

    df_clean.replace("-", np.nan, inplace=True)

    for col in NUMERIC_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(
                df_clean[col], errors="coerce"
            )

    return df, df_clean


def prepare_fund_data(csv_path=DATASET_PATH):
    """Clean, score, rank and classify funds."""
    df, df_clean = load_and_clean_data(csv_path)

    missing_columns = [
        col for col in SCORING_COLUMNS + RISK_COLUMNS
        if col not in df_clean.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    # Retain funds with all required scoring inputs.
    df_model = df_clean.dropna(
        subset=SCORING_COLUMNS
    ).copy()

    if df_model.empty:
        raise ValueError("No funds have complete scoring data.")

    # Apply MinMax scaling.
    scaler = MinMaxScaler()

    scaled_values = scaler.fit_transform(
        df_model[SCORING_COLUMNS]
    )

    scaled_columns = [
        "return_3yr_scaled",
        "expense_scaled",
        "age_scaled",
        "return_1yr_scaled"
    ]

    df_model[scaled_columns] = scaled_values

    # Project scoring methodology.
    df_model["expense_score"] = (
        1 - df_model["expense_scaled"]
    )

    df_model["fund_score"] = (
        0.40 * df_model["return_3yr_scaled"]
        + 0.25 * df_model["expense_score"]
        + 0.20 * df_model["age_scaled"]
        + 0.15 * df_model["return_1yr_scaled"]
    )

    df_model["fund_score_percentage"] = (
        df_model["fund_score"] * 100
    )

    df_model = df_model.sort_values(
        "fund_score", ascending=False
    ).reset_index(drop=True)

    df_model["overall_rank"] = range(
        1, len(df_model) + 1
    )

    # Risk assessment requires all five risk metrics.
    risk_analysis = df_model.dropna(
        subset=RISK_COLUMNS
    ).copy()

    if risk_analysis.empty:
        raise ValueError(
            "No funds have complete risk assessment metrics."
        )

    # Dataset-relative volatility classification.
    low_threshold = risk_analysis["sd"].quantile(0.33)
    high_threshold = risk_analysis["sd"].quantile(0.66)

    def classify_volatility(sd):
        if sd <= low_threshold:
            return "Low"
        elif sd <= high_threshold:
            return "Moderate"
        return "High"

    risk_analysis["volatility_group"] = (
        risk_analysis["sd"].apply(classify_volatility)
    )

    return {
        "original": df,
        "cleaned": df_clean,
        "model": df_model,
        "risk_analysis": risk_analysis,
        "low_threshold": low_threshold,
        "high_threshold": high_threshold
    }


def generate_personalized_recommendations(
    investor_profile,
    risk_analysis,
    top_n=10
):
    """Generate recommendations using the project methodology."""

    funds = risk_analysis.copy()

    selected_risk = investor_profile["risk_appetite"]
    investment_amount = float(
        investor_profile["investment_amount"]
    )
    investment_duration = int(
        investor_profile["investment_duration"]
    )
    investment_mode = investor_profile["investment_mode"]
    preferred_category = investor_profile.get(
        "preferred_category", "Any"
    )

    # 1. Match investor risk appetite.
    funds = funds[
        funds["volatility_group"] == selected_risk
    ].copy()

    # 2. Check investment eligibility.
    if investment_mode == "SIP":
        monthly_budget = (
            investment_amount / (investment_duration * 12)
        )
        funds = funds[
            funds["min_sip"].notna()
            & (funds["min_sip"] <= monthly_budget)
        ].copy()

    elif investment_mode == "Lump Sum":
        funds = funds[
            funds["min_lumpsum"].notna()
            & (funds["min_lumpsum"] <= investment_amount)
        ].copy()

    else:
        raise ValueError(
            "Investment mode must be SIP or Lump Sum."
        )

    # 3. Apply preferred category.
    if preferred_category != "Any":
        funds = funds[
            funds["category"].astype(str).str.lower()
            == preferred_category.lower()
        ].copy()

    # 4. Rank by project fund score.
    funds = funds.sort_values(
        "fund_score", ascending=False
    ).head(top_n).copy()

    funds["recommendation_rank"] = range(
        1, len(funds) + 1
    )

    funds["recommendation_reason"] = (
        "Passed investment eligibility and risk-group filtering; "
        "ranked using the project's historical performance, "
        "expense and fund-age scoring model."
    )

    # Preliminary suitability screening.
    funds["investment_eligible"] = True
    funds["risk_compatible"] = (
        funds["volatility_group"] == selected_risk
    )
    funds["historical_data_available"] = (
        funds[["returns_3yr", "sd", "sharpe"]]
        .notna().all(axis=1)
    )
    funds["duration_assessment"] = (
        "Not assessed - scheme-specific holding period unavailable"
    )
    funds["suitability_status"] = np.where(
        funds[
            [
                "investment_eligible",
                "risk_compatible",
                "historical_data_available"
            ]
        ].all(axis=1),
        "Passed preliminary checks",
        "Review required"
    )

    return funds.reset_index(drop=True)


def create_excel_report(
    investor_profile,
    recommendations,
    all_funds,
    risk_analysis
):
    """Create a downloadable Excel report in memory."""

    profile_df = pd.DataFrame(
        [investor_profile]
    )

    comparison_columns = [
        col for col in [
            "scheme_name", "category", "returns_1yr",
            "returns_3yr", "returns_5yr", "expense_ratio",
            "fund_age_yr", "sd", "sharpe", "fund_score",
            "fund_score_percentage"
        ]
        if col in recommendations.columns
    ]

    fund_comparison = recommendations[
        comparison_columns
    ].copy()

    risk_summary = (
        risk_analysis["volatility_group"]
        .value_counts()
        .rename_axis("Volatility Group")
        .reset_index(name="Number of Funds")
    )

    review_required = recommendations[
        recommendations["suitability_status"] == "Review required"
    ].copy()

    methodology = pd.DataFrame([
        ["3-Year Returns Weight", "40%"],
        ["Inverse Expense Ratio Weight", "25%"],
        ["Fund Age Weight", "20%"],
        ["1-Year Returns Weight", "15%"],
        ["Risk Classification",
         "Dataset-relative standard deviation percentiles (33rd and 66th)"],
        ["Duration Limitation",
         "Scheme-specific holding period unavailable"],
        ["Suitability Status",
         "Preliminary screening only; not financial advice"],
        ["Performance Limitation",
         "Historical returns do not guarantee future performance"]
    ], columns=["Parameter", "Details"])

    all_ranked = all_funds.copy()

    output = BytesIO()

    with pd.ExcelWriter(
        output, engine="openpyxl"
    ) as writer:

        profile_df.to_excel(
            writer, sheet_name="Investor Profile", index=False
        )
        recommendations.to_excel(
            writer, sheet_name="Top Recommendations", index=False
        )
        fund_comparison.to_excel(
            writer, sheet_name="Fund Comparison", index=False
        )
        recommendations.to_excel(
            writer, sheet_name="Suitability Assessment", index=False
        )
        risk_summary.to_excel(
            writer, sheet_name="Risk Analysis", index=False
        )
        review_required.to_excel(
            writer, sheet_name="Review Required", index=False
        )
        all_ranked.to_excel(
            writer, sheet_name="All Ranked Funds", index=False
        )
        methodology.to_excel(
            writer, sheet_name="Methodology", index=False
        )

        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter

        for worksheet in writer.book.worksheets:
            for cell in worksheet[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill(
                    start_color="1F4E78",
                    end_color="1F4E78",
                    fill_type="solid"
                )
                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center",
                    wrap_text=True
                )

            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            for column_cells in worksheet.columns:
                max_length = max(
                    (len(str(cell.value))
                     for cell in column_cells
                     if cell.value is not None),
                    default=10
                )
                letter = get_column_letter(
                    column_cells[0].column
                )
                worksheet.column_dimensions[letter].width = min(
                    max_length + 3, 45
                )

            worksheet.row_dimensions[1].height = 30

    output.seek(0)
    return output
