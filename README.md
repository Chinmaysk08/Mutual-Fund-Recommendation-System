<div align="center">
# Mutual Fund Recommendation System
 
**A rule-based, explainable decision-support dashboard for screening and ranking Indian mutual funds**
 
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243?logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualisation-3F4F75?logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-MinMaxScaler-F7931E?logo=scikitlearn&logoColor=white)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel%20Reports-217346?logo=microsoftexcel&logoColor=white)
 
[Live Application](https://mutual-fund-intelligence-chinmay.streamlit.app/) · [Methodology](#9-recommendation-methodology) · [Installation](#11-installation-and-setup) · [Disclaimer](#18-disclaimer)
 
</div>
> **Educational project.** This application is an academic decision-support tool built on historical data. It is not certified financial advice and does not guarantee returns. See the [Disclaimer](#18-disclaimer).
 
---
 
## Table of Contents
 
1. [Project Title and Overview](#1-project-title-and-overview)
2. [Project Introduction](#2-project-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Project Objectives](#4-project-objectives)
5. [Key Features](#5-key-features)
6. [Technology Stack](#6-technology-stack)
7. [Dataset Description](#7-dataset-description)
8. [System Architecture](#8-system-architecture)
9. [Recommendation Methodology](#9-recommendation-methodology)
10. [Project Folder Structure](#10-project-folder-structure)
11. [Installation and Setup](#11-installation-and-setup)
12. [Running the Streamlit Application](#12-running-the-streamlit-application)
13. [Application Screenshots](#13-application-screenshots)
14. [Excel Report Outputs](#14-excel-report-outputs)
15. [Project Results and Outcomes](#15-project-results-and-outcomes)
16. [Limitations](#16-limitations)
17. [Future Enhancements](#17-future-enhancements)
18. [Disclaimer](#18-disclaimer)
19. [Author Information](#19-author-information)
20. [Acknowledgements](#20-acknowledgements)
---
 
## 1. Project Title and Overview
 
**Mutual Fund Recommendation System** (branded in the app as *Fund Intelligence*) is a Python and Streamlit web application that analyses a dataset of 814 mutual fund schemes, scores and ranks them with a transparent weighted formula, groups them by volatility, and produces a personalised shortlist based on an investor's stated preferences. Results can be exported as a multi-sheet Excel workbook.
 
| Item | Detail |
|---|---|
| Type | Data analytics and decision-support web application |
| Approach | Rule-based filtering plus weighted scoring (no trained ML model) |
| Interface | Streamlit multi-page dashboard (6 pages) |
| Data | 814 schemes, 20 columns (`Dataset/mutual_funds_data.csv`) |
| Output | Interactive ranked recommendations and a downloadable `.xlsx` report |
| Live demo | https://mutual-fund-intelligence-chinmay.streamlit.app/ |
 
---
 
## 2. Project Introduction
 
Choosing a mutual fund usually means comparing many schemes across returns, costs, fund age and volatility. This project turns a structured fund dataset into an interactive workflow: explore the market, enter an investor profile, receive a ranked shortlist, compare funds side by side and download the analysis.
 
All logic is deliberately simple and inspectable. Every number shown in the app can be traced to a formula in `engine.py`.
 
---
 
## 3. Problem Statement
 
Retail investors face a large universe of schemes with many overlapping metrics. Raw tables are hard to interpret, and rankings published elsewhere often do not explain how they were produced.
 
This project addresses that gap by building a system that:
 
- cleans and standardises raw fund data,
- ranks funds with an explicit, documented scoring formula,
- classifies funds into Low, Moderate and High volatility groups,
- filters funds by an investor's risk appetite, budget, investment mode and preferred category, and
- presents the output in a form that can be reviewed, compared and exported.
---
 
## 4. Project Objectives
 
- Load and clean the mutual fund dataset, handling placeholder and missing values.
- Design a transparent weighted scoring model using returns, cost and fund age.
- Classify funds by volatility using dataset-relative percentile thresholds.
- Match funds to an investor profile (risk appetite, amount, duration, mode, category).
- Provide an interactive dashboard with charts, comparisons and ranked tables.
- Generate a structured Excel report documenting the profile, results and methodology.
- State assumptions and limitations clearly.
---
 
## 5. Key Features
 
The application has six pages, selected from the sidebar.
 
### Interactive Dashboard
- Four summary metrics: total funds, eligible scored funds, average 3-year return and average expense ratio.
- Bar chart of fund category distribution.
- Donut chart of the volatility group distribution.
- Table of the top 10 funds by project score.
### Investor Profile Management
- Form capturing risk appetite (Low / Moderate / High), investment amount (₹), duration (1 to 40 years), investment mode (SIP or Lump Sum) and preferred fund category (or *Any*).
- Profile is stored in the Streamlit session and shown as a summary.
- For SIP, an estimated monthly budget is displayed.
### Personalized Mutual Fund Recommendations
- Up to 10 funds ranked by project score after eligibility and risk filtering.
- Highlight cards for the top three funds.
- Full ranked table and a per-fund detail view with the recommendation reason and a preliminary suitability status.
### Fund Comparison
- Multi-select any funds from the scored set (the first two are pre-selected).
- Summary cards, a grouped bar chart of 1-year, 3-year and 5-year returns, an expense ratio chart and a detailed comparison table.
### Excel Report Generation
- One-click download of an 8-sheet formatted workbook built from the current profile and recommendations (see [Excel Report Outputs](#14-excel-report-outputs)).
### About Project
- In-app summary of the workflow, scoring weights (with chart), dataset counts and technology stack.
---
 
## 6. Technology Stack
 
| Layer | Technology | Role in this project |
|---|---|---|
| Language | Python | Core implementation |
| Web framework | Streamlit | Multi-page interactive UI, forms, downloads |
| Data processing | Pandas, NumPy | Loading, cleaning, filtering, ranking |
| Preprocessing | scikit-learn (`MinMaxScaler` only) | Normalising scoring inputs to a 0–1 range |
| Visualisation | Plotly Express | Bar, grouped-bar and donut charts |
| Reporting | OpenPyXL (via `pandas.ExcelWriter`) | Formatted Excel workbook |
 
> scikit-learn is used solely for min-max scaling. The project does not train or use any machine learning model.
 
Dependencies are listed in `StreamLit_App/requirements.txt` (unpinned): `streamlit`, `pandas`, `numpy`, `plotly`, `openpyxl`, `scikit-learn`.
 
---
 
## 7. Dataset Description
 
**File:** `Dataset/mutual_funds_data.csv` · **814 records × 20 columns**
 
| Column | Type | Description |
|---|---|---|
| `scheme_name` | Text | Name of the mutual fund scheme |
| `min_sip` | Integer | Minimum SIP amount (₹) |
| `min_lumpsum` | Integer | Minimum lump-sum investment (₹) |
| `expense_ratio` | Float | Annual expense ratio (%) |
| `fund_size_cr` | Float | Fund size (₹ crore) |
| `fund_age_yr` | Integer | Fund age in years |
| `fund_manager` | Text | Fund manager name |
| `sortino` | Numeric (stored as text) | Sortino ratio |
| `alpha` | Numeric (stored as text) | Alpha |
| `sd` | Numeric (stored as text) | Standard deviation of returns (volatility) |
| `beta` | Numeric (stored as text) | Beta |
| `sharpe` | Numeric (stored as text) | Sharpe ratio |
| `risk_level` | Integer | Source-provided risk level (values 1 to 6) |
| `amc_name` | Text | Asset management company (39 distinct) |
| `rating` | Integer | Source-provided rating (0 to 5) |
| `category` | Text | Equity, Debt, Hybrid, Solution Oriented, Other |
| `sub_category` | Text | Finer classification (38 distinct) |
| `returns_1yr` | Float | 1-year return (%) |
| `returns_3yr` | Float | 3-year return (%) |
| `returns_5yr` | Float | 5-year return (%) |
 
**Category mix**
 
| Category | Funds |
|---|---|
| Equity | 308 |
| Debt | 282 |
| Hybrid | 116 |
| Other | 80 |
| Solution Oriented | 28 |
 
**Data quality notes (from inspection of the CSV)**
 
- The five risk metrics (`sortino`, `alpha`, `sd`, `beta`, `sharpe`) contain `-` placeholders (23 to 42 per column), which is why they are read as text and converted during cleaning.
- `returns_3yr` has 21 missing values and `returns_5yr` has 167, as newer funds lack longer histories.
- The source `risk_level` and `rating` columns are present but are not used by the scoring or recommendation logic.
---
 
## 8. System Architecture
 
```text
┌────────────────────────────┐
│ Dataset/mutual_funds_data  │   814 schemes, 20 columns
└─────────────┬──────────────┘
              │  load_and_clean_data()
              ▼
┌────────────────────────────┐
│ Cleaning                   │   "-" → NaN, numeric conversion
└─────────────┬──────────────┘
              │  prepare_fund_data()
              ▼
┌────────────────────────────┐
│ Scoring and ranking        │   MinMax scaling + weighted score
│ → 793 scored funds         │   → overall_rank
└─────────────┬──────────────┘
              ▼
┌────────────────────────────┐
│ Risk classification        │   sd percentiles → Low/Moderate/High
│ → 770 risk-assessed funds  │
└─────────────┬──────────────┘
              │  generate_personalized_recommendations()
              ▼
┌────────────────────────────┐
│ Investor-profile filtering │   risk → eligibility → category → top 10
└─────────────┬──────────────┘
              ▼
┌────────────────────────────┐        ┌──────────────────────────┐
│ Streamlit UI (app.py)      │ ─────► │ create_excel_report()    │
│ Dashboard · Profile · Recs │        │ 8-sheet .xlsx download   │
│ Comparison · Reports · About│       └──────────────────────────┘
└────────────────────────────┘
```
 
| File | Responsibility |
|---|---|
| `StreamLit_App/engine.py` | Data loading, cleaning, scoring, risk grouping, recommendation filtering, Excel generation |
| `StreamLit_App/app.py` | Streamlit interface, navigation, charts, session state; calls the engine |
 
The dataset is loaded once through `@st.cache_data`, and the investor profile and recommendations are held in `st.session_state` so they persist across pages.
 
---
 
## 9. Recommendation Methodology
 
All logic below is implemented in `StreamLit_App/engine.py`.
 
### Data preprocessing
 
1. Read the CSV with Pandas.
2. Replace `-` placeholders with `NaN`.
3. Convert the 15 numeric columns with `pd.to_numeric(errors="coerce")`.
4. Keep only funds that have all four scoring inputs (`returns_3yr`, `expense_ratio`, `fund_age_yr`, `returns_1yr`). This leaves **793 of 814** funds.
### Fund scoring and evaluation
 
The four scoring inputs are scaled to 0–1 with `MinMaxScaler`. Expense ratio is inverted (`1 − scaled value`) so that lower costs score higher. The score is a weighted sum:
 
```text
fund_score = 0.40 × scaled 3-year return
           + 0.25 × (1 − scaled expense ratio)
           + 0.20 × scaled fund age
           + 0.15 × scaled 1-year return
```
 
| Component | Weight | Direction |
|---|---|---|
| 3-year return | 40% | Higher is better |
| Expense ratio | 25% | Lower is better |
| Fund age | 20% | Older is better |
| 1-year return | 15% | Higher is better |
 
The score is multiplied by 100 for display (`fund_score_percentage`), and funds receive an `overall_rank` in descending score order. Scaling is relative to this dataset, so scores are comparative and not absolute measures of quality.
 
### Risk assessment
 
Among funds that also have all five risk metrics (`sortino`, `alpha`, `sd`, `beta`, `sharpe`), **770 funds**, volatility groups are assigned from the standard deviation (`sd`):
 
| Group | Rule |
|---|---|
| Low | `sd` ≤ 33rd percentile (≈ 3.05) |
| Moderate | `sd` between the 33rd and 66th percentile (≈ 3.05 to 15.69) |
| High | `sd` above the 66th percentile (≈ 15.69) |
 
Thresholds are dataset-relative, not regulatory risk categories. Of the 770 funds, 254 are Low, 257 Moderate and 259 High.
 
### Investor preference matching
 
`generate_personalized_recommendations()` applies the following filters in order:
 
| Step | Rule |
|---|---|
| 1. Risk | Keep funds whose volatility group equals the selected risk appetite |
| 2. Eligibility (SIP) | Monthly budget = `investment_amount ÷ (duration_years × 12)`; keep funds with `min_sip` ≤ budget |
| 2. Eligibility (Lump Sum) | Keep funds with `min_lumpsum` ≤ `investment_amount` |
| 3. Category | If a category other than *Any* is chosen, keep only that category |
 
Note that for SIP, the amount entered is treated as the **total** amount to invest over the chosen duration, which is converted to a monthly figure.
 
### Recommendation generation
 
- Remaining funds are sorted by `fund_score` and the top 10 are returned with a `recommendation_rank`.
- Each result carries a fixed recommendation reason, a `suitability_status` ("Passed preliminary checks" or "Review required") and a `duration_assessment` that is explicitly marked *Not assessed*, because the dataset has no scheme-specific holding period.
- If no fund passes all filters, the app shows a message suggesting a different risk level, category or amount.
---
 
## 10. Project Folder Structure
 
Folder and file names below match the repository exactly, including the capitalisation of `StreamLit_App`.
 
```text
Mutual-Fund-Recommendation-System/
├── Dataset/
│   └── mutual_funds_data.csv        # 814 records, 20 columns
├── StreamLit_App/
│   ├── app.py                       # Streamlit application (entry point)
│   ├── engine.py                    # Scoring, risk and recommendation engine
│   ├── requirements.txt             # Python dependencies
│   └── ...                          # Earlier development snapshots and backups
└── README.md
```
 
The `StreamLit_App/` folder also contains earlier development snapshots (for example `app_before_*.py`, `app.py.backup`, `engine.py.py`, `requirements.txt.txt`). They are not used by the running application.
 
---
 
## 11. Installation and Setup
 
**Prerequisites:** Python 3.11 or later and Git.
 
Commands below are for Windows (Command Prompt or PowerShell).
 
**1. Clone the repository**
 
```bash
git clone https://github.com/Chinmaysk08/Mutual-Fund-Recommendation-System.git
cd Mutual-Fund-Recommendation-System
```
 
**2. Create and activate a virtual environment**
 
```bash
python -m venv venv
```
 
Command Prompt:
 
```bat
venv\Scripts\activate
```
 
PowerShell:
 
```powershell
venv\Scripts\Activate.ps1
```
 
> If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and retry.
 
**3. Install dependencies**
 
```bash
pip install -r StreamLit_App/requirements.txt
```
 
---
 
## 12. Running the Streamlit Application
 
From the repository root, with the virtual environment active:
 
```bash
streamlit run StreamLit_App/app.py
```
 
Streamlit prints a local address (normally `http://localhost:8501`); open it in a browser.
 
**Suggested walkthrough**
 
1. Open **Dashboard** to see dataset-level charts.
2. Open **Investor Profile**, enter preferences and select *Generate Recommendations*.
3. Review results under **Recommendations**.
4. Use **Fund Comparison** to compare selected funds.
5. Download the workbook from **Excel Reports**.
**Deployed version:** https://mutual-fund-intelligence-chinmay.streamlit.app/
 
> Availability of the hosted app depends on Streamlit Community Cloud. Apps there can go to sleep after inactivity and may need a moment to wake up.
 
---
 
## 13. Application Screenshots
 
Screenshots are not yet included in the repository. To add them, save images under `docs/screenshots/` and reference them here, for example:
 
```markdown
![Dashboard](docs/screenshots/dashboard.png)
```
 
| Page | What it shows |
|---|---|
| Dashboard | KPI metrics, category distribution, volatility donut, top 10 funds |
| Investor Profile | Preference form and profile summary |
| Recommendations | Top-three cards, ranked table, fund detail view |
| Fund Comparison | Return and expense charts, detailed comparison table |
| Excel Reports | Profile summary, workbook details, download button |
| About Project | Workflow, scoring weights, technology stack |
 
---
 
## 14. Excel Report Outputs
 
The report is generated in memory by `create_excel_report()` and downloaded as `Mutual_Fund_Report_<Risk>_<Mode>.xlsx` (for example, `Mutual_Fund_Report_Moderate_SIP.xlsx`). Every sheet has a styled header row, frozen top row, auto-filter and auto-sized columns.
 
| # | Sheet | Contents |
|---|---|---|
| 1 | Investor Profile | The submitted investor preferences |
| 2 | Top Recommendations | Ranked recommendations with all computed fields |
| 3 | Fund Comparison | Selected metrics (returns, expense, age, `sd`, Sharpe, score) for recommended funds |
| 4 | Suitability Assessment | Recommendations with the preliminary suitability fields |
| 5 | Risk Analysis | Number of funds in each volatility group |
| 6 | Review Required | Recommended funds flagged "Review required" (may be empty) |
| 7 | All Ranked Funds | All 793 scored funds with scores and ranks |
| 8 | Methodology | Scoring weights, risk-classification rule and stated limitations |
 
---
 
## 15. Project Results and Outcomes
 
This project does not report model accuracy or investment returns, because it uses a rule-based scoring system rather than a predictive model. The outcomes below were verified by running the engine on the repository dataset.
 
| Outcome | Value |
|---|---|
| Funds in the original dataset | 814 |
| Funds with complete scoring data | 793 |
| Funds with complete risk-assessment data | 770 |
| Volatility groups (Low / Moderate / High) | 254 / 257 / 259 |
| Recommendations returned with default inputs (₹12,000, 5 years, any category) | 10 for every combination of risk level and investment mode |
 
What the project demonstrates:
 
- an end-to-end data pipeline from raw CSV to interactive application,
- a documented, reproducible scoring and filtering method,
- separation of analytical logic (`engine.py`) from presentation (`app.py`), and
- automated, structured Excel reporting.
---
 
## 16. Limitations
 
- **Historical data only.** Past returns do not predict future performance.
- **Simple scoring model.** Only four variables feed the score; alpha, beta, Sharpe, Sortino, fund size, rating and 5-year returns are not part of the score.
- **Fund age is rewarded.** Older funds receive a higher score by construction, which may favour established schemes regardless of current quality.
- **Dataset-relative scaling and risk groups.** Scores and Low/Moderate/High labels depend on this dataset and are not absolute or regulatory measures.
- **Risk matching uses volatility only.** The investor's risk appetite is mapped to the `sd`-based group; no questionnaire or risk-capacity assessment is performed.
- **Duration is not assessed against fund suitability.** It only affects the SIP monthly-budget calculation.
- **Preliminary suitability checks are limited.** They largely restate the filters already applied and do not constitute a suitability assessment.
- **Static dataset.** Data is a snapshot, with no live NAV or market feed, and its original source date is not recorded in the repository.
- **No tax, exit load or goal planning.**
- **Unpinned dependencies.** `requirements.txt` has no version pins, so future library releases could change behaviour.
---
 
## 17. Future Enhancements
 
- Add live or periodically refreshed fund data.
- Pin dependency versions and add automated tests for the engine.
- Allow adjustable scoring weights in the interface.
- Include additional metrics (Sharpe, alpha, fund size) in the score, with a sensitivity analysis.
- Add a risk-profiling questionnaire.
- Add rolling returns, drawdown and benchmark comparison.
- Add a goal-based projection tool with clear assumptions.
- Remove superseded backup files and add a `.gitignore` for `__pycache__`.
---
 
## 18. Disclaimer
 
This project is an **educational decision-support application** developed for academic and portfolio purposes. It is **not** certified financial advice, an investment recommendation, or a solicitation to buy or sell any security. The rankings reflect only the scoring methodology described in this document and historical data. Past performance does not guarantee future results, and mutual fund investments are subject to market risk. Consult a qualified, SEBI-registered financial adviser before making investment decisions.
 
---
 
## 19. Author Information
 
**Chinmay**
GitHub: [@Chinmaysk08](https://github.com/Chinmaysk08)
 
<!-- Add before publishing: full name, institution / department, LinkedIn, email. -->
 
---
 
## 20. Acknowledgements
 
- [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [Plotly](https://plotly.com/python/), [scikit-learn](https://scikit-learn.org/) and [OpenPyXL](https://openpyxl.readthedocs.io/) for the open-source tooling.
- Streamlit Community Cloud for hosting the demo application.
