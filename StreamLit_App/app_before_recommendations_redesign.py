
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
        "Compare mutual funds using historical returns, "
        "expense ratio, volatility and fund age."
    )

    available_funds = model_df["scheme_name"].dropna().tolist()

    selected_funds = st.multiselect(
        "Choose funds to compare",
        available_funds,
        default=available_funds[:2]
    )

    if selected_funds:

        comparison = model_df[
            model_df["scheme_name"].isin(selected_funds)
        ].copy()

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
            c for c in comparison_columns
            if c in comparison.columns
        ]

        st.dataframe(
            comparison[comparison_columns].rename(columns={
                "scheme_name": "Fund Name",
                "category": "Category",
                "returns_1yr": "1Y Return (%)",
                "returns_3yr": "3Y Return (%)",
                "returns_5yr": "5Y Return (%)",
                "expense_ratio": "Expense Ratio (%)",
                "fund_age_yr": "Fund Age (Years)",
                "sd": "Standard Deviation",
                "sharpe": "Sharpe Ratio",
                "fund_score_percentage": "Fund Score (%)"
            }),
            use_container_width=True,
            hide_index=True
        )

        if len(comparison) > 1:

            st.subheader("3-Year Return Comparison")

            fig = px.bar(
                comparison,
                x="scheme_name",
                y="returns_3yr",
                color="scheme_name",
                template="plotly_dark",
                labels={
                    "scheme_name": "Fund",
                    "returns_3yr": "3-Year Return (%)"
                }
            )

            fig.update_layout(showlegend=False)
            st.plotly_chart(
    style_chart(fig),
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True}
)

    else:
        st.info("Select at least one fund to compare.")


# --------------------------------------------------
# EXCEL REPORTS
# --------------------------------------------------

elif page == "Excel Reports":

    st.title("📥 Excel Reports")

    st.write(
        "Generate an Excel workbook containing investor profile, "
        "recommendations, fund comparison, risk analysis "
        "and methodology."
    )

    if "recommendations" not in st.session_state:

        st.info(
            "Generate recommendations from the Investor Profile "
            "page before downloading a report."
        )

    else:

        recommendations = st.session_state["recommendations"]
        profile = st.session_state["investor_profile"]

        if recommendations.empty:
            st.warning(
                "There are no recommendations to include in the report."
            )

        else:

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

            st.success("Excel report is ready.")

            st.download_button(
                label="Download Excel Report",
                data=excel_file,
                file_name=filename,
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True
            )

            st.write("**Workbook sheets**")

            for sheet in [
                "Investor Profile",
                "Top Recommendations",
                "Fund Comparison",
                "Suitability Assessment",
                "Risk Analysis",
                "Review Required",
                "All Ranked Funds",
                "Methodology"
            ]:
                st.write(f"✓ {sheet}")


# --------------------------------------------------
# ABOUT PROJECT
# --------------------------------------------------

elif page == "About Project":

    st.title("ℹ️ About the Project")

    st.subheader("Mutual Fund Recommendation System")

    st.write(
        """
        This project analyses mutual fund data and generates
        personalized fund recommendations based on investor
        risk appetite, investment amount, investment duration,
        investment mode and preferred category.
        """
    )

    st.subheader("Project Workflow")

    st.markdown("""
    1. Dataset loading
    2. Data cleaning and preprocessing
    3. Exploratory data analysis
    4. Fund scoring using MinMax scaling
    5. Dataset-relative volatility classification
    6. Investment eligibility filtering
    7. Personalized fund recommendations
    8. Excel report generation
    """)

    st.subheader("Fund Scoring Methodology")

    weights = pd.DataFrame({
        "Parameter": [
            "3-Year Returns",
            "Inverse Expense Ratio",
            "Fund Age",
            "1-Year Returns"
        ],
        "Weight": [40, 25, 20, 15]
    })

    fig = px.pie(
        weights,
        names="Parameter",
        values="Weight",
        hole=0.5,
        template="plotly_dark"
    )

    st.plotly_chart(
    style_chart(fig),
    use_container_width=True,
    config={"displayModeBar": False, "responsive": True}
)

    st.subheader("Important Limitations")

    st.markdown("""
    - Risk groups are based on dataset-relative standard deviation
      percentiles, not official SEBI Riskometer categories.
    - Historical returns do not guarantee future performance.
    - Scheme-specific recommended holding periods are not available
      in the dataset.
    - Suitability checks are preliminary screening only.
    - The scoring weights are experimental project assumptions,
      not an industry-standard investment formula.
    """)

    st.warning(
        "This application is an academic analytics project, "
        "not a SEBI-registered investment advisory service."
    )

    st.divider()

    st.caption("Mutual Fund Recommendation System | Academic Project")
