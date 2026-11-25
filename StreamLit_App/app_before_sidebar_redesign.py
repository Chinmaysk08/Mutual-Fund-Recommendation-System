import html

import streamlit as st
import pandas as pd
import plotly.express as px

from engine import (
    prepare_fund_data,
    generate_personalized_recommendations,
    create_excel_report
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Mutual Fund Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

:root {
    --bg-main: #080e1a;
    --bg-card: #111c2e;
    --bg-card-hover: #17263c;
    --border: rgba(148, 163, 184, 0.15);
    --text-main: #edf4ff;
    --text-muted: #91a2ba;
    --accent: #6ee7b7;
    --accent-blue: #60a5fa;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, rgba(37, 99, 235, 0.15), transparent 35%),
        radial-gradient(ellipse at 95% 5%, rgba(16, 185, 129, 0.09), transparent 30%),
        var(--bg-main);
    color: var(--text-main);
    font-family: "Inter", "Segoe UI", sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: rgba(8, 14, 26, 0.75);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}

/* Main headings */

h1 {
    color: #f8fafc !important;
    font-size: 2.15rem !important;
    font-weight: 750 !important;
    letter-spacing: -1.2px;
    margin-bottom: 0.35rem !important;
}

h2 {
    color: #e2eaf7 !important;
    font-size: 1.42rem !important;
    font-weight: 650 !important;
    letter-spacing: -0.4px;
    margin-top: 1.2rem !important;
}

h3 {
    color: #d9e7f8 !important;
    font-size: 1.08rem !important;
    font-weight: 650 !important;
}

p, li, label {
    color: #bdcbe0;
}

[data-testid="stCaptionContainer"] {
    color: var(--text-muted);
}

/* Top application bar */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
    background: linear-gradient(
        110deg,
        rgba(20, 34, 55, 0.96),
        rgba(13, 26, 43, 0.92)
    );
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 15px 21px;
    margin-bottom: 28px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.16);
}

.topbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-mark {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 43px;
    height: 43px;
    border-radius: 13px;
    background: linear-gradient(135deg, #0d9488, #3b82f6);
    color: white;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: -1px;
    box-shadow: 0 5px 18px rgba(45, 212, 191, 0.2);
}

.brand-title {
    color: #f8fafc;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 1.1px;
}

.brand-subtitle {
    color: #8295b0;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 3px;
}

.topbar-status {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #a9bdd4;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 1px;
}

.status-pulse {
    width: 8px;
    height: 8px;
    background: #6ee7b7;
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(110, 231, 183, 0.75);
}

.topbar-divider {
    height: 17px;
    width: 1px;
    background: #334155;
    margin: 0 5px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101b2d, #0b1423);
    border-right: 1px solid rgba(148, 163, 184, 0.12);
}

[data-testid="stSidebar"] h1 {
    font-size: 1.45rem !important;
    letter-spacing: -0.5px;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #91a2ba;
    font-size: 12px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 10px;
    padding: 9px 11px;
    margin-bottom: 5px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(96, 165, 250, 0.10);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: rgba(45, 212, 191, 0.12);
    border: 1px solid rgba(45, 212, 191, 0.22);
}

/* KPI metric cards */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17263b, #101b2d);
    border: 1px solid rgba(148, 163, 184, 0.17);
    border-radius: 16px;
    padding: 19px 20px;
    box-shadow: 0 9px 25px rgba(0, 0, 0, 0.13);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(110, 231, 183, 0.45);
}

[data-testid="stMetricLabel"] {
    color: #9aadc5 !important;
    font-size: 12px !important;
    font-weight: 650 !important;
}

[data-testid="stMetricValue"] {
    color: #f4f8ff !important;
    font-size: 1.75rem !important;
    font-weight: 750 !important;
    letter-spacing: -0.7px;
}

[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}

/* Buttons */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: linear-gradient(110deg, #0d9488, #2563eb);
    color: white !important;
    border: 1px solid rgba(110, 231, 183, 0.28);
    border-radius: 11px;
    padding: 0.65rem 1.1rem;
    font-weight: 700;
    transition: all 0.2s ease;
    box-shadow: 0 5px 17px rgba(37, 99, 235, 0.17);
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    border-color: #6ee7b7;
    box-shadow: 0 8px 23px rgba(13, 148, 136, 0.25);
}

/* Input controls */

[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div {
    background: #111e31 !important;
    border: 1px solid #33445d !important;
    border-radius: 10px !important;
}

[data-baseweb="select"] > div:hover,
[data-baseweb="input"] > div:hover {
    border-color: #5eead4 !important;
}

input, textarea {
    color: #f1f5f9 !important;
}

[data-testid="stNumberInput"] button {
    background: #1c2d43 !important;
    color: #dce8f7 !important;
    border-color: #33445d !important;
}

/* Data tables */

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #111c2e;
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

[data-testid="stDataFrame"] iframe {
    border-radius: 12px;
}

/* Forms and content containers */

[data-testid="stForm"] {
    background: linear-gradient(145deg, #131f32, #101a2a);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 22px;
}

[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid var(--border);
}

[data-testid="stPlotlyChart"] {
    background: rgba(17, 28, 46, 0.65);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 8px;
}

hr {
    border-color: rgba(148, 163, 184, 0.16) !important;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Expanders */

[data-testid="stExpander"] {
    background: rgba(17, 28, 46, 0.65);
    border: 1px solid var(--border);
    border-radius: 12px;
}

/* Responsive layout */

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }

    .topbar {
        padding: 13px;
    }
}



/* Screenshot-matched chart panels */
[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, #111e32, #101a2b) !important;
    border: 1px solid rgba(105, 139, 180, 0.22) !important;
    border-radius: 17px !important;
    padding: 10px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.16);
    overflow: hidden;
}

/* Refined content background */
[data-testid="stMain"] {
    background: transparent;
}

/* Chart section headings */
[data-testid="stMain"] h2 {
    color: #e6eefb !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
    margin-bottom: 12px !important;
}

/* Keep charts responsive */
[data-testid="stPlotlyChart"] iframe {
    width: 100% !important;
    border: none !important;
}

/* Improved sidebar separators */
[data-testid="stSidebar"] hr {
    border-color: rgba(148, 163, 184, 0.15) !important;
}



/* Premium investor profile form */
[data-testid="stForm"] {
    background:
        radial-gradient(
            circle at 100% 0%,
            rgba(13, 148, 136, 0.07),
            transparent 35%
        ),
        linear-gradient(145deg, #142238, #101b2d) !important;
    border: 1px solid rgba(110, 231, 183, 0.17) !important;
    border-radius: 20px !important;
    padding: 27px !important;
    box-shadow: 0 14px 36px rgba(0, 0, 0, 0.19);
}

/* Form introduction */
.profile-form-heading {
    padding-bottom: 19px;
    margin-bottom: 23px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.17);
}

.profile-form-kicker {
    color: #6ee7b7;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.profile-form-title {
    color: #f1f6ff;
    font-size: 21px;
    font-weight: 750;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}

.profile-form-description {
    color: #92a6c1;
    font-size: 12px;
    line-height: 1.7;
}

/* Input labels */
[data-testid="stForm"] label {
    color: #c7d6e9 !important;
    font-size: 13px !important;
    font-weight: 650 !important;
}

/* Select boxes */
[data-testid="stForm"] div[data-baseweb="select"] > div {
    background-color: #172940 !important;
    border: 1px solid #354b65 !important;
    border-radius: 11px !important;
    min-height: 48px;
    box-shadow: none !important;
}

[data-testid="stForm"] div[data-baseweb="select"] > div:hover {
    border-color: #4e9b9a !important;
}

[data-testid="stForm"] div[data-baseweb="select"] [role="combobox"] {
    color: #f1f6ff !important;
}

/* Number input fields */
[data-testid="stForm"] div[data-baseweb="input"] > div {
    background-color: #172940 !important;
    border: 1px solid #354b65 !important;
    border-radius: 10px !important;
    min-height: 48px;
    box-shadow: none !important;
}

[data-testid="stForm"] div[data-baseweb="input"] input {
    background: transparent !important;
    color: #f1f6ff !important;
    font-size: 14px !important;
}

[data-testid="stForm"] div[data-baseweb="input"] > div:focus-within {
    border-color: #42c9ac !important;
    box-shadow: 0 0 0 2px rgba(66, 201, 172, 0.13) !important;
}

/* Number input controls */
[data-testid="stForm"] [data-testid="stNumberInput"] button {
    background: #203650 !important;
    color: #e2f2ff !important;
    border-color: #354b65 !important;
}

/* Column spacing */
[data-testid="stForm"] [data-testid="stHorizontalBlock"] {
    column-gap: 20px;
}

/* Generate button */
[data-testid="stFormSubmitButton"] > button {
    min-height: 53px;
    border-radius: 12px !important;
    font-size: 15px !important;
    font-weight: 750 !important;
    letter-spacing: 0.2px;
    margin-top: 9px;
    background: linear-gradient(105deg, #0d9488, #2563eb) !important;
    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.2);
}

[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 27px rgba(13, 148, 136, 0.28);
}

/* Mobile form padding */
@media (max-width: 768px) {
    [data-testid="stForm"] {
        padding: 17px !important;
    }
}



/* Recommendation cards */
.rec-card {
    background: linear-gradient(145deg, #172a42, #101d30);
    border: 1px solid rgba(148, 163, 184, 0.20);
    border-radius: 16px;
    padding: 19px;
    min-height: 180px;
    height: 100%;
    box-shadow: 0 9px 24px rgba(0, 0, 0, 0.16);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.rec-card:hover {
    transform: translateY(-4px);
    border-color: rgba(110, 231, 183, 0.55);
}

.rec-card.rank-1 {
    border-top: 3px solid #6ee7b7;
}

.rec-card.rank-2 {
    border-top: 3px solid #60a5fa;
}

.rec-card.rank-3 {
    border-top: 3px solid #a78bfa;
}

.rec-rank {
    color: #6ee7b7;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 13px;
}

.rec-name {
    color: #f1f6ff;
    font-size: 15px;
    line-height: 1.5;
    font-weight: 750;
    min-height: 47px;
    margin-bottom: 13px;
}

.rec-score {
    color: #6ee7b7;
    font-size: 23px;
    font-weight: 800;
}

.rec-meta {
    color: #91a7c0;
    font-size: 11px;
    margin-top: 8px;
}

.rec-section-label {
    color: #8fa5c0;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 13px;
}

.rec-table-heading {
    color: #e8f0fb;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 12px;
}



/* Premium fund comparison cards */
.comparison-card {
    background: linear-gradient(145deg, #172a42, #101d30);
    border: 1px solid rgba(148, 163, 184, 0.20);
    border-radius: 16px;
    padding: 20px;
    min-height: 185px;
    height: 100%;
    box-shadow: 0 9px 24px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
}

.comparison-card:hover {
    transform: translateY(-4px);
    border-color: rgba(110, 231, 183, 0.48);
}

.comparison-rank {
    color: #6ee7b7;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.4px;
    margin-bottom: 12px;
}

.comparison-name {
    color: #f1f6ff;
    font-size: 14px;
    line-height: 1.5;
    font-weight: 750;
    min-height: 43px;
    margin-bottom: 14px;
}

.comparison-return {
    color: #6ee7b7;
    font-size: 23px;
    font-weight: 800;
}

.comparison-label {
    color: #91a7c0;
    font-size: 10px;
    margin-top: 5px;
}

.comparison-metric {
    color: #dce8f7;
    font-size: 13px;
    font-weight: 650;
    margin-top: 11px;
}

.comparison-section-label {
    color: #8fa5c0;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.7px;
    margin-bottom: 14px;
}



/* Premium Excel report interface */

.report-hero {
    background: linear-gradient(125deg, #142b43, #102036);
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-radius: 20px;
    padding: 28px;
    margin: 18px 0;
}

.report-eyebrow {
    color: #6ee7b7;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.report-heading {
    color: #f1f6ff;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 8px;
}

.report-description {
    color: #a9bbd1;
    font-size: 14px;
    line-height: 1.7;
}

.report-stat {
    background: linear-gradient(145deg, #172a42, #101d30);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 15px;
    padding: 19px;
    min-height: 105px;
}

.report-stat-label {
    color: #91a7c0;
    font-size: 11px;
    font-weight: 650;
}

.report-stat-value {
    color: #e6f0ff;
    font-size: 21px;
    font-weight: 800;
    margin-top: 9px;
}

.sheet-card {
    background: linear-gradient(145deg, #172a42, #101d30);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 10px;
    color: #dce8f7;
    font-size: 13px;
    font-weight: 650;
}

.sheet-check {
    color: #6ee7b7;
    font-weight: 900;
    margin-right: 9px;
}

</style>
""", unsafe_allow_html=True)



def style_chart(fig):
    """Apply consistent navy fintech styling to Plotly charts."""

    is_pie = any(
        getattr(trace, "type", "") == "pie"
        for trace in fig.data
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color="#DCE7F5",
            size=12
        ),
        height=400,
        autosize=True,
        margin=dict(
            l=35,
            r=25,
            t=35,
            b=65 if is_pie else 125
        ),
        hoverlabel=dict(
            bgcolor="#17263B",
            bordercolor="#3C536E",
            font=dict(color="#F8FAFC", size=12)
        ),
        legend=dict(
            orientation="h" if is_pie else "v",
            x=0.5 if is_pie else 1,
            xanchor="center" if is_pie else "left",
            y=-0.12 if is_pie else 0.5,
            yanchor="top" if is_pie else "middle",
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#C8D7E8", size=11)
        )
    )

    fig.update_xaxes(
        showgrid=False,
        automargin=True,
        tickangle=-35,
        tickfont=dict(color="#B8C8DC", size=11),
        title_font=dict(color="#DCE7F5", size=12),
        linecolor="rgba(148,163,184,0.20)"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,0.13)",
        zerolinecolor="rgba(148,163,184,0.18)",
        automargin=True,
        tickfont=dict(color="#B8C8DC", size=11),
        title_font=dict(color="#DCE7F5", size=12)
    )

    if is_pie:
        fig.update_traces(
            textfont=dict(
                color="#F8FAFC",
                size=12
            ),
            marker=dict(
                line=dict(
                    color="#111C2E",
                    width=2
                )
            )
        )

    return fig


# --------------------------------------------------
# LOAD PROJECT DATA
# --------------------------------------------------

@st.cache_data
def load_project():
    return prepare_fund_data()


try:
    project_data = load_project()

    original_df = project_data["original"]
    cleaned_df = project_data["cleaned"]
    model_df = project_data["model"]
    risk_df = project_data["risk_analysis"]

except Exception as error:
    st.error(f"Unable to load project data: {error}")
    st.stop()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("📈 Fund Intelligence")
st.sidebar.caption("Mutual Fund Recommendation System")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Investor Profile",
        "Recommendations",
        "Fund Comparison",
        "Excel Reports",
        "About Project"
    ]
)


st.markdown("""
<div class="topbar">
    <div class="topbar-brand">
        <div class="brand-mark">MF</div>
        <div>
            <div class="brand-title">FUND INTELLIGENCE</div>
            <div class="brand-subtitle">MUTUAL FUND ANALYTICS WORKSPACE</div>
        </div>
    </div>
    <div class="topbar-status">
        <span class="status-pulse"></span>
        DATASET CONNECTED
        <span class="topbar-divider"></span>
        LOCAL ANALYTICS
    </div>
</div>
""", unsafe_allow_html=True)


st.sidebar.divider()
st.sidebar.caption("Academic Project | Mutual Fund Analytics")


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def format_percentage(value):
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f}%"


def display_fund_table(data):
    columns = [
        "recommendation_rank",
        "scheme_name",
        "category",
        "volatility_group",
        "returns_1yr",
        "returns_3yr",
        "expense_ratio",
        "fund_score_percentage"
    ]

    available = [c for c in columns if c in data.columns]

    display_data = data[available].copy()

    rename = {
        "recommendation_rank": "Rank",
        "scheme_name": "Fund Name",
        "category": "Category",
        "volatility_group": "Risk Group",
        "returns_1yr": "1Y Return (%)",
        "returns_3yr": "3Y Return (%)",
        "expense_ratio": "Expense Ratio (%)",
        "fund_score_percentage": "Fund Score (%)"
    }

    return display_data.rename(columns=rename)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("📊 Mutual Fund Analytics Dashboard")

    st.write(
        "Explore mutual fund performance, risk distribution "
        "and historical investment metrics."
    )

    total_funds = len(original_df)
    average_return = model_df["returns_3yr"].mean()
    average_expense = model_df["expense_ratio"].mean()
    average_rating = (
        cleaned_df["rating"].mean()
        if "rating" in cleaned_df.columns else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Funds", f"{total_funds:,}")
    col2.metric("Eligible Scored Funds", f"{len(model_df):,}")
    col3.metric("Average 3Y Return", format_percentage(average_return))
    col4.metric("Average Expense Ratio", format_percentage(average_expense))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Fund Category Distribution")

        category_data = (
            cleaned_df["category"]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        category_data.columns = ["Category", "Count"]

        category_colors = {
            "Equity": "#6366F1",
            "Debt": "#F0523A",
            "Hybrid": "#00C99A",
            "Other": "#A855F7",
            "Solution Oriented": "#FB923C"
        }

        fig = px.bar(
            category_data,
            x="Category",
            y="Count",
            color="Category",
            color_discrete_map=category_colors,
            color_discrete_sequence=[
                "#6366F1", "#F0523A", "#00C99A",
                "#A855F7", "#FB923C"
            ],
            template="plotly_dark",
            text="Count"
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(color="#E2E8F0", size=11),
            cliponaxis=False
        )

        fig.update_layout(showlegend=False)
        st.plotly_chart(
    style_chart(fig),
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True}
)

    with right:
        st.subheader("Volatility Distribution")

        risk_distribution = (
            risk_df["volatility_group"]
            .value_counts()
            .reset_index()
        )

        risk_distribution.columns = ["Risk Group", "Funds"]

        risk_colors = {
            "High": "#6366F1",
            "Moderate": "#F0523A",
            "Low": "#00C99A"
        }

        fig = px.pie(
            risk_distribution,
            names="Risk Group",
            values="Funds",
            hole=0.58,
            color="Risk Group",
            color_discrete_map=risk_colors,
            template="plotly_dark"
        )

        fig.update_traces(
            textinfo="percent",
            textposition="inside",
            insidetextfont=dict(
                color="#FFFFFF",
                size=12
            ),
            hovertemplate="%{label}<br>Funds: %{value}<br>Share: %{percent}<extra></extra>"
        )

        fig.add_annotation(
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            text=f"<b>{len(risk_df)}</b><br>FUNDS",
            showarrow=False,
            font=dict(size=18, color="#F8FAFC")
        )

        st.plotly_chart(
    style_chart(fig),
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True}
)

    st.divider()

    st.subheader("Top 10 Funds by Project Score")

    top_funds = model_df.head(10).copy()

    top_columns = [
        "scheme_name",
        "category",
        "returns_3yr",
        "expense_ratio",
        "fund_score_percentage"
    ]

    st.dataframe(
        top_funds[top_columns].rename(columns={
            "scheme_name": "Fund Name",
            "category": "Category",
            "returns_3yr": "3Y Return (%)",
            "expense_ratio": "Expense Ratio (%)",
            "fund_score_percentage": "Fund Score (%)"
        }),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# INVESTOR PROFILE
# --------------------------------------------------

elif page == "Investor Profile":

    st.title("👤 Investor Profile")

    st.write(
        "Enter your investment preferences to generate "
        "risk-based mutual fund recommendations."
    )

    with st.form("investor_form"):

        st.markdown("""
        <div class="profile-form-heading">
            <div class="profile-form-kicker">
                INVESTMENT CONFIGURATION
            </div>
            <div class="profile-form-title">
                Build Your Investor Profile
            </div>
            <div class="profile-form-description">
                Configure your risk appetite, investment budget,
                investment duration and preferred fund category.
                These preferences will be used to filter your recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            risk_appetite = st.selectbox(
                "Risk Appetite",
                ["Low", "Moderate", "High"]
            )

            investment_amount = st.number_input(
                "Investment Amount (₹)",
                min_value=1000,
                max_value=100000000,
                value=12000,
                step=1000
            )

            investment_duration = st.number_input(
                "Investment Duration (Years)",
                min_value=1,
                max_value=40,
                value=5
            )

        with col2:
            investment_mode = st.selectbox(
                "Investment Mode",
                ["SIP", "Lump Sum"]
            )

            categories = ["Any"] + sorted(
                cleaned_df["category"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            preferred_category = st.selectbox(
                "Preferred Fund Category",
                categories
            )

        submitted = st.form_submit_button(
            "Generate Recommendations",
            use_container_width=True
        )

    if submitted:

        profile = {
            "risk_appetite": risk_appetite,
            "investment_amount": investment_amount,
            "investment_duration": investment_duration,
            "investment_mode": investment_mode,
            "preferred_category": preferred_category
        }

        st.session_state["investor_profile"] = profile

        recommendations = generate_personalized_recommendations(
            profile,
            risk_df
        )

        st.session_state["recommendations"] = recommendations

        st.success("Investor profile saved and recommendations generated.")

        st.subheader("Investor Profile Summary")

        summary1, summary2, summary3 = st.columns(3)

        summary1.metric("Risk Appetite", risk_appetite)
        summary2.metric("Investment Mode", investment_mode)
        summary3.metric("Investment Amount", f"₹{investment_amount:,.0f}")

        if investment_mode == "SIP":
            monthly_budget = (
                investment_amount / (investment_duration * 12)
            )
            st.info(
                f"Estimated monthly budget: ₹{monthly_budget:,.2f}"
            )

        st.write(
            f"Investment duration: {investment_duration} years"
        )

        st.write(
            f"Preferred category: {preferred_category}"
        )

        if recommendations.empty:
            st.warning(
                "No funds match all selected filters. "
                "Try another risk appetite, category or investment amount."
            )


# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

elif page == "Recommendations":

    st.title("🎯 Personalized Recommendations")

    if "recommendations" not in st.session_state:

        st.info(
            "Please complete the Investor Profile page first "
            "to generate recommendations."
        )

    else:

        recommendations = st.session_state["recommendations"]

        if recommendations.empty:
            st.warning("No recommendations are currently available.")

        else:

            profile = st.session_state["investor_profile"]

            st.write(
                f"Recommendations for a **{profile['risk_appetite']} "
                f"risk** investor using **{profile['investment_mode']}**."
            )

            st.metric(
                "Recommended Funds",
                len(recommendations)
            )

            # Highlight the top three ranked funds
            st.markdown(
                '<div class="rec-section-label">TOP RECOMMENDED FUNDS</div>',
                unsafe_allow_html=True
            )

            top_three = recommendations.head(3)
            recommendation_columns = st.columns(3)

            for index, (_, fund_row) in enumerate(top_three.iterrows()):

                with recommendation_columns[index]:

                    fund_name = html.escape(
                        str(fund_row.get("scheme_name", "Fund"))
                    )

                    category = html.escape(
                        str(fund_row.get("category", "N/A"))
                    )

                    risk_group = html.escape(
                        str(fund_row.get("volatility_group", "N/A"))
                    )

                    rank = int(
                        fund_row.get("recommendation_rank", index + 1)
                    )

                    score = pd.to_numeric(
                        fund_row.get("fund_score_percentage"),
                        errors="coerce"
                    )

                    returns = pd.to_numeric(
                        fund_row.get("returns_3yr"),
                        errors="coerce"
                    )

                    score_text = (
                        f"{score:.2f}%" if pd.notna(score) else "N/A"
                    )

                    returns_text = (
                        f"{returns:.2f}%" if pd.notna(returns) else "N/A"
                    )

                    st.markdown(f"""
                    <div class="rec-card rank-{rank}">
                        <div class="rec-rank">RANK #{rank}</div>
                        <div class="rec-name">{fund_name}</div>
                        <div class="rec-score">{score_text}</div>
                        <div class="rec-meta">
                            PROJECT SCORE
                        </div>
                        <div class="rec-meta">
                            3Y Return: {returns_text}
                        </div>
                        <div class="rec-meta">
                            {category} · {risk_group} Risk
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()

            st.markdown(
                '<div class="rec-table-heading">Complete Ranked Recommendations</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                display_fund_table(recommendations),
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("Recommendation Details")

            selected_fund = st.selectbox(
                "Select a fund",
                recommendations["scheme_name"].tolist()
            )

            fund = recommendations[
                recommendations["scheme_name"] == selected_fund
            ].iloc[0]

            st.markdown(f"### {fund['scheme_name']}")

            a, b, c = st.columns(3)

            a.metric(
                "3-Year Return",
                format_percentage(fund["returns_3yr"])
            )

            b.metric(
                "Expense Ratio",
                format_percentage(fund["expense_ratio"])
            )

            c.metric(
                "Project Fund Score",
                format_percentage(fund["fund_score_percentage"])
            )

            st.write("**Recommendation Reason**")
            st.write(fund["recommendation_reason"])

            st.write("**Preliminary Suitability Status**")
            st.write(fund["suitability_status"])

            st.caption(
                "Project ranking is based on historical data and "
                "the specified scoring methodology. It is not "
                "a guarantee of future returns."
            )


# --------------------------------------------------
# FUND COMPARISON
# --------------------------------------------------

elif page == "Fund Comparison":

    st.title("⚖️ Fund Comparison")

    st.write(
        "Compare mutual funds across historical returns, "
        "expense ratios, fund age and project scoring."
    )

    st.markdown(
        '<div class="comparison-section-label">'
        'SELECT FUNDS TO ANALYSE'
        '</div>',
        unsafe_allow_html=True
    )

    available_funds = (
        model_df["scheme_name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_funds = st.multiselect(
        "Choose mutual funds",
        available_funds,
        default=available_funds[:2],
        help="Select multiple funds to compare their performance."
    )

    if selected_funds:

        comparison = model_df[
            model_df["scheme_name"].isin(selected_funds)
        ].copy()

        comparison = comparison.drop_duplicates(
            subset=["scheme_name"]
        )

        comparison = comparison.sort_values(
            "fund_score", ascending=False
        )

        # ------------------------------------------
        # FUND COMPARISON CARDS
        # ------------------------------------------

        st.divider()

        st.markdown(
            '<div class="comparison-section-label">'
            'FUND PERFORMANCE OVERVIEW'
            '</div>',
            unsafe_allow_html=True
        )

        for batch_start in range(0, len(comparison), 3):

            batch = comparison.iloc[
                batch_start:batch_start + 3
            ]

            card_columns = st.columns(len(batch))

            for column, (_, fund_row) in zip(
                card_columns, batch.iterrows()
            ):

                with column:

                    fund_name = html.escape(
                        str(fund_row["scheme_name"])
                    )

                    category = html.escape(
                        str(fund_row.get("category", "N/A"))
                    )

                    rank = int(
                        fund_row.get("overall_rank", 0)
                    )

                    return_3yr = pd.to_numeric(
                        fund_row.get("returns_3yr"),
                        errors="coerce"
                    )

                    expense = pd.to_numeric(
                        fund_row.get("expense_ratio"),
                        errors="coerce"
                    )

                    score = pd.to_numeric(
                        fund_row.get("fund_score_percentage"),
                        errors="coerce"
                    )

                    return_text = (
                        f"{return_3yr:.2f}%"
                        if pd.notna(return_3yr) else "N/A"
                    )

                    expense_text = (
                        f"{expense:.2f}%"
                        if pd.notna(expense) else "N/A"
                    )

                    score_text = (
                        f"{score:.2f}%"
                        if pd.notna(score) else "N/A"
                    )

                    st.markdown(f"""
                    <div class="comparison-card">
                        <div class="comparison-rank">
                            OVERALL RANK #{rank}
                        </div>
                        <div class="comparison-name">
                            {fund_name}
                        </div>
                        <div class="comparison-return">
                            {return_text}
                        </div>
                        <div class="comparison-label">
                            3-YEAR HISTORICAL RETURN
                        </div>
                        <div class="comparison-metric">
                            Expense Ratio: {expense_text}
                        </div>
                        <div class="comparison-metric">
                            Project Score: {score_text}
                        </div>
                        <div class="comparison-label">
                            {category}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()

        # ------------------------------------------
        # HISTORICAL RETURN COMPARISON
        # ------------------------------------------

        st.subheader("Historical Return Comparison")

        return_columns = [
            col for col in [
                "returns_1yr",
                "returns_3yr",
                "returns_5yr"
            ]
            if col in comparison.columns
        ]

        if return_columns:

            return_data = comparison[
                ["scheme_name"] + return_columns
            ].melt(
                id_vars=["scheme_name"],
                value_vars=return_columns,
                var_name="Period",
                value_name="Return (%)"
            ).dropna()

            period_labels = {
                "returns_1yr": "1 Year",
                "returns_3yr": "3 Years",
                "returns_5yr": "5 Years"
            }

            return_data["Period"] = (
                return_data["Period"].map(period_labels)
            )

            fig = px.bar(
                return_data,
                x="scheme_name",
                y="Return (%)",
                color="Period",
                barmode="group",
                color_discrete_map={
                    "1 Year": "#6366F1",
                    "3 Years": "#00C99A",
                    "5 Years": "#F59E0B"
                },
                template="plotly_dark",
                labels={
                    "scheme_name": "Mutual Fund",
                    "Return (%)": "Historical Return (%)"
                }
            )

            fig.update_layout(
                legend_title_text="Investment Period"
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True
                }
            )

        # ------------------------------------------
        # EXPENSE RATIO COMPARISON
        # ------------------------------------------

        st.subheader("Expense Ratio Comparison")

        if "expense_ratio" in comparison.columns:

            expense_data = comparison.dropna(
                subset=["expense_ratio"]
            )

            if not expense_data.empty:

                fig = px.bar(
                    expense_data,
                    x="scheme_name",
                    y="expense_ratio",
                    color="scheme_name",
                    text="expense_ratio",
                    color_discrete_sequence=[
                        "#6366F1", "#F0523A",
                        "#00C99A", "#A855F7",
                        "#FB923C"
                    ],
                    template="plotly_dark",
                    labels={
                        "scheme_name": "Mutual Fund",
                        "expense_ratio": "Expense Ratio (%)"
                    }
                )

                fig.update_traces(
                    texttemplate="%{text:.2f}%",
                    textposition="outside",
                    cliponaxis=False
                )

                fig.update_layout(showlegend=False)

                st.plotly_chart(
                    style_chart(fig),
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True
                    }
                )

        # ------------------------------------------
        # DETAILED COMPARISON TABLE
        # ------------------------------------------

        st.divider()

        st.subheader("Detailed Fund Comparison")

        comparison_columns = [
            "scheme_name",
            "category",
            "returns_1yr",
            "returns_3yr",
            "returns_5yr",
            "expense_ratio",
            "fund_age_yr",
            "sd",
            "sharpe",
            "fund_score_percentage"
        ]

        comparison_columns = [
            col for col in comparison_columns
            if col in comparison.columns
        ]

        comparison_display = comparison[
            comparison_columns
        ].rename(columns={
            "scheme_name": "Fund Name",
            "category": "Category",
            "returns_1yr": "1Y Return (%)",
            "returns_3yr": "3Y Return (%)",
            "returns_5yr": "5Y Return (%)",
            "expense_ratio": "Expense Ratio (%)",
            "fund_age_yr": "Fund Age (Years)",
            "sd": "Standard Deviation",
            "sharpe": "Sharpe Ratio",
            "fund_score_percentage": "Project Score (%)"
        })

        st.dataframe(
            comparison_display,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Historical returns and project scores are analytical "
            "indicators, not predictions of future performance."
        )

    else:
        st.info("Select at least one mutual fund to begin comparison.")


# --------------------------------------------------
# EXCEL REPORTS
# --------------------------------------------------

elif page == "Excel Reports":

    st.title("📥 Excel Reports")

    st.write(
        "Generate and download a comprehensive Excel workbook "
        "containing personalized mutual fund analytics."
    )

    if "recommendations" not in st.session_state:

        st.info(
            "Please generate recommendations from the "
            "Investor Profile page before downloading a report."
        )

    else:

        recommendations = st.session_state["recommendations"]
        profile = st.session_state["investor_profile"]

        if recommendations.empty:

            st.warning(
                "There are no recommendations to include in the report."
            )

        else:

            # Generate the original Excel workbook
            excel_file = create_excel_report(
                profile,
                recommendations,
                model_df,
                risk_df
            )

            filename = (
                f"Mutual_Fund_Report_"
                f"{profile['risk_appetite']}_"
                f"{profile['investment_mode'].replace(' ', '_')}.xlsx"
            )

            file_size_kb = len(excel_file.getvalue()) / 1024

            # --------------------------------------
            # REPORT HERO
            # --------------------------------------

            st.markdown("""
            <div class="report-hero">
                <div class="report-eyebrow">
                    FUND INTELLIGENCE / REPORT CENTER
                </div>
                <div class="report-heading">
                    Your Investment Analytics Report
                </div>
                <div class="report-description">
                    A personalized Excel workbook containing
                    your investor profile, ranked fund recommendations,
                    comparison analysis, risk assessment and methodology.
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --------------------------------------
            # INVESTOR PROFILE SUMMARY
            # --------------------------------------

            st.markdown(
                '<div class="report-eyebrow">INVESTOR PROFILE SUMMARY</div>',
                unsafe_allow_html=True
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="report-stat">
                    <div class="report-stat-label">RISK APPETITE</div>
                    <div class="report-stat-value">
                        {profile['risk_appetite']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="report-stat">
                    <div class="report-stat-label">INVESTMENT MODE</div>
                    <div class="report-stat-value">
                        {profile['investment_mode']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="report-stat">
                    <div class="report-stat-label">INVESTMENT AMOUNT</div>
                    <div class="report-stat-value">
                        ₹{profile['investment_amount']:,.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="report-stat">
                    <div class="report-stat-label">DURATION</div>
                    <div class="report-stat-value">
                        {profile['investment_duration']} Years
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.write("")

            # --------------------------------------
            # WORKBOOK DETAILS
            # --------------------------------------

            st.markdown(
                '<div class="report-eyebrow">GENERATED WORKBOOK</div>',
                unsafe_allow_html=True
            )

            st.markdown(f"""
            <div class="report-hero">
                <div class="report-heading">
                    📊 Excel Analytics Workbook
                </div>
                <div class="report-description">
                    {filename}
                </div>
                <div class="report-description">
                    File format: XLSX &nbsp; | &nbsp;
                    File size: {file_size_kb:.1f} KB &nbsp; | &nbsp;
                    Recommendations: {len(recommendations)}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --------------------------------------
            # DOWNLOAD BUTTON
            # --------------------------------------

            st.download_button(
                label="⬇  DOWNLOAD EXCEL REPORT",
                data=excel_file,
                file_name=filename,
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True,
                type="primary"
            )

            st.caption(
                "Your workbook is generated using the existing "
                "recommendation and risk analysis engine."
            )

            # --------------------------------------
            # WORKBOOK CONTENTS
            # --------------------------------------

            st.divider()

            st.subheader("📑 Workbook Contents")

            st.write(
                "Your report contains the following analytical sheets:"
            )

            sheets = [
                ("01", "Investor Profile",
                 "Investor preferences and investment details"),

                ("02", "Top Recommendations",
                 "Personalized ranked mutual fund recommendations"),

                ("03", "Fund Comparison",
                 "Performance and fund metric comparison"),

                ("04", "Suitability Assessment",
                 "Preliminary investment suitability checks"),

                ("05", "Risk Analysis",
                 "Fund volatility and risk classification"),

                ("06", "Review Required",
                 "Funds requiring additional suitability review"),

                ("07", "All Ranked Funds",
                 "Ranked fund dataset and project scores"),

                ("08", "Methodology",
                 "Scoring weights, methodology and limitations")
            ]

            for batch_start in range(0, len(sheets), 2):

                batch = sheets[batch_start:batch_start + 2]
                sheet_columns = st.columns(2)

                for column, (number, name, description) in zip(
                    sheet_columns, batch
                ):

                    with column:

                        st.markdown(f"""
                        <div class="sheet-card">
                            <span class="sheet-check">✓</span>
                            {number} &nbsp; {name}
                            <div style="
                                color:#91a7c0;
                                font-size:11px;
                                font-weight:400;
                                margin-top:7px;
                            ">
                                {description}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            st.success(
                "Your Excel report is ready for download."
            )


# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------


elif page == "About Project":

    st.title("ℹ️ About Fund Intelligence")

    st.markdown(
        "Understand the system, its analytical workflow, "
        "recommendation methodology and project scope."
    )

    st.divider()

    # PROJECT OVERVIEW
    st.subheader("Project Overview")

    st.markdown("""
    This **Mutual Fund Recommendation System** is an academic
    analytics application that analyses mutual fund data and
    generates personalized fund recommendations.

    Recommendations are generated using investor risk appetite,
    investment amount, investment duration, investment mode
    and preferred fund category.
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Original Dataset", "814 Funds")

    with c2:
        st.metric("Scored Funds", "793 Funds")

    with c3:
        st.metric("Risk-Assessed Funds", "770 Funds")

    st.divider()

    # PROJECT WORKFLOW
    st.subheader("⚙️ Project Workflow")

    workflow = [
        ("01", "Dataset Loading", "Import mutual fund dataset."),
        ("02", "Data Preprocessing", "Clean missing and invalid values."),
        ("03", "Exploratory Analysis", "Analyse fund characteristics."),
        ("04", "Fund Scoring", "Apply MinMax scaling and weighted scoring."),
        ("05", "Risk Classification", "Group funds using volatility percentiles."),
        ("06", "Eligibility Filtering", "Check investment amount and risk compatibility."),
        ("07", "Recommendations", "Generate personalized ranked fund suggestions."),
        ("08", "Excel Reporting", "Export analysis and recommendations.")
    ]

    for i in range(0, len(workflow), 2):
        col1, col2 = st.columns(2)

        for col, item in zip(
            [col1, col2],
            workflow[i:i + 2]
        ):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{item[0]} · {item[1]}**")
                    st.caption(item[2])

    st.divider()

    # SCORING METHODOLOGY
    st.subheader("📊 Fund Scoring Methodology")

    st.write(
        "The system calculates a weighted fund score using "
        "four selected performance and cost parameters."
    )

    weights = pd.DataFrame({
        "Parameter": [
            "3-Year Returns",
            "Inverse Expense Ratio",
            "Fund Age",
            "1-Year Returns"
        ],
        "Weight": [40, 25, 20, 15]
    })

    col1, col2 = st.columns([1.2, 1])

    with col1:
        fig = px.pie(
            weights,
            names="Parameter",
            values="Weight",
            hole=0.58,
            template="plotly_dark",
            color_discrete_sequence=[
                "#6366F1",
                "#F05A43",
                "#00C99A",
                "#A855F7"
            ]
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#DCE6F5",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5
            ),
            margin=dict(t=20, b=50, l=10, r=10)
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:
        st.markdown("#### Scoring Weights")

        for _, row in weights.iterrows():
            st.markdown(
                f"**{row['Parameter']}** — {row['Weight']}%"
            )
            st.progress(int(row["Weight"]))

        st.info(
            "Expense ratio is inversely scored: lower expense "
            "ratios receive a higher score."
        )

    st.caption(
        "Final fund score = 40% (3Y Returns) + 25% "
        "(Inverse Expense Ratio) + 20% (Fund Age) + "
        "15% (1Y Returns), using normalized values."
    )

    st.divider()

    # TECHNOLOGY STACK
    st.subheader("💻 Technology Stack")

    tech = [
        ("Python", "Core programming language"),
        ("Pandas & NumPy", "Data processing and numerical analysis"),
        ("Scikit-learn", "MinMax scaling"),
        ("Plotly", "Interactive visualizations"),
        ("Streamlit", "Web application interface"),
        ("OpenPyXL", "Excel report generation")
    ]

    for i in range(0, len(tech), 3):
        cols = st.columns(3)

        for col, item in zip(cols, tech[i:i + 3]):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{item[0]}**")
                    st.caption(item[1])

    st.divider()

    st.caption(
        "Fund Intelligence | Mutual Fund Recommendation System | "
        "Academic Project"
    )
