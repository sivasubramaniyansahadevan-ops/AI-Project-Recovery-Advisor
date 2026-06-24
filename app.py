import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
from io import BytesIO
import matplotlib.pyplot as plt
import urllib.parse

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(
    page_title="ProjectRescue AI",
    page_icon="🟥",
    layout="wide"
)

# -----------------------------
# PREMIUM UI STYLE
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(229,9,20,0.18), transparent 30%),
        radial-gradient(circle at top right, rgba(255,255,255,0.05), transparent 25%),
        linear-gradient(135deg, #050505 0%, #0B0B0B 50%, #111111 100%);
    color: #FFFFFF;
}

.block-container {
    padding-top: 1.5rem;
    padding-left: 3.5rem;
    padding-right: 3.5rem;
    max-width: 1500px;
}

h1, h2, h3, h4, h5, h6, p, label, span {
    color: #F5F5F5 !important;
}

.hero {
    background: linear-gradient(135deg, rgba(20,20,20,0.95), rgba(8,8,8,0.95));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 28px;
    padding: 34px 38px;
    margin-bottom: 28px;
    box-shadow: 0 28px 80px rgba(0,0,0,0.6);
}

.hero-title {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: -1.5px;
    margin-bottom: 8px;
}

.hero-title span {
    color: #E50914 !important;
}

.hero-subtitle {
    font-size: 18px;
    color: #CCCCCC !important;
}

.hero-brand {
    font-size: 13px;
    color: #888888 !important;
    margin-top: 14px;
}

.panel {
    background: rgba(18,18,18,0.88);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 26px;
    margin-top: 18px;
    margin-bottom: 18px;
    box-shadow: 0 18px 50px rgba(0,0,0,0.45);
}

.result-card {
    padding: 32px;
    border-radius: 28px;
    margin: 28px 0;
    box-shadow: 0 28px 80px rgba(0,0,0,0.55);
}

.green-card {
    background: linear-gradient(135deg, #062C1B, #0E6B3A);
    border: 1px solid #2ECC71;
}

.amber-card {
    background: linear-gradient(135deg, #2D1C00, #A96A00);
    border: 1px solid #F39C12;
}

.red-card {
    background: linear-gradient(135deg, #2B0000, #990000);
    border: 1px solid #E50914;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 18px;
    margin-top: 26px;
}

.result-metric {
    background: rgba(0,0,0,0.32);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 18px;
}

.result-label {
    font-size: 12px;
    color: #BBBBBB !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.result-value {
    font-size: 30px;
    font-weight: 900;
    margin-top: 8px;
}

[data-testid="stTabs"] button {
    background: #151515 !important;
    border-radius: 14px 14px 0 0 !important;
    color: #BBBBBB !important;
    font-weight: 700 !important;
    padding: 14px 20px !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 3px solid #E50914 !important;
}

/* Primary Streamlit buttons */
.stButton button {
    background: #181818 !important;
    color: #F5F5F5 !important;
    border: 1px solid #333333 !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.4rem !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}

.stButton button:hover {
    background: #242424 !important;
    color: #FFFFFF !important;
    border: 1px solid #E50914 !important;
    box-shadow: 0 0 18px rgba(229,9,20,0.28);
}

.stLinkButton a {
    background: #181818 !important;
    color: #F5F5F5 !important;
    border: 1px solid #333333 !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.4rem !important;
    text-decoration: none !important;
    box-shadow: 0 12px 30px rgba(0,0,0,0.30);
}

.stLinkButton a:hover {
    background: #242424 !important;
    color: #FFFFFF !important;
    border: 1px solid #E50914 !important;
    box-shadow: 0 0 18px rgba(229,9,20,0.28);
}

.stDownloadButton button {
    background: linear-gradient(135deg, #E50914, #B00610) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    padding: 0.75rem 1.4rem !important;
    box-shadow: 0 12px 30px rgba(229,9,20,0.25);
}

.stDownloadButton button:hover {
    background: linear-gradient(135deg, #FF2333, #E50914) !important;
}

[data-testid="stFileUploader"] section {
    background: #181818 !important;
    border: 1px solid #333333 !important;
    border-radius: 14px !important;
}

[data-testid="stFileUploader"] section * {
    color: #F5F5F5 !important;
}

.stNumberInput input, .stTextInput input {
    background-color: #181818 !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #181818 !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] {
    background: #121212 !important;
    border: 1px dashed #444444 !important;
    border-radius: 18px !important;
    padding: 18px !important;
}

[data-testid="stFileUploader"] section {
    background: #181818 !important;
    border: 1px solid #2A2A2A !important;
    border-radius: 16px !important;
}

[data-testid="stFileUploader"] button {
    background: #151515 !important;
    color: #F5F5F5 !important;
    border: 1px solid #333333 !important;
    border-radius: 12px !important;
}

[data-testid="stFileUploader"] button:hover {
    border: 1px solid #E50914 !important;
    color: #FFFFFF !important;
}

.badge {
    padding: 6px 12px;
    border-radius: 999px;
    font-weight: 800;
    font-size: 13px;
}

.badge-green { background:#0E6B3A; color:#FFFFFF; }
.badge-amber { background:#A96A00; color:#FFFFFF; }
.badge-red { background:#990000; color:#FFFFFF; }

.footer {
    color: #777777;
    margin-top: 50px;
    padding-top: 22px;
    border-top: 1px solid #222222;
    font-size: 13px;
}

.health-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 16px;
}
.health-tile {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 16px;
}
.health-name {
    font-size: 13px;
    color: #BDBDBD !important;
    margin-bottom: 8px;
}
.health-value {
    font-size: 18px;
    font-weight: 900;
}
.health-green { border-left: 5px solid #2ECC71; }
.health-amber { border-left: 5px solid #F39C12; }
.health-red { border-left: 5px solid #E74C3C; }
.driver-table {
    width:100%;
    border-collapse: collapse;
    margin-top: 14px;
    margin-bottom: 20px;
}
.driver-table th, .driver-table td {
    border-bottom: 1px solid rgba(255,255,255,0.10);
    padding: 12px;
    text-align: left;
}
.driver-table th { color:#BDBDBD !important; font-size:12px; text-transform:uppercase; }
.driver-badge { padding: 5px 10px; border-radius: 999px; font-weight: 800; font-size: 12px; }
.driver-high { background:#8B0000; color:white; }
.driver-medium { background:#9A6500; color:white; }
.driver-low { background:#0E6B3A; color:white; }
.driver-critical { background:#8B0000; color:white; }
.driver-watchlist { background:#9A6500; color:white; }



/* =============================
   FINAL INPUT BORDER FIX
   Removes white Streamlit/BaseWeb outlines
   ============================= */

.stTextInput input,
.stNumberInput input{
    background: linear-gradient(180deg, #161616 0%, #111111 100%) !important;
    color:#F5F5F5 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
    outline:none !important;
}

.stTextInput input:hover,
.stNumberInput input:hover{
    border:1px solid #3A3A3A !important;
    box-shadow:none !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextInput input:focus-visible,
.stNumberInput input:focus-visible{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.35) !important;
    outline:none !important;
}

[data-baseweb="input"],
[data-baseweb="input"] > div{
    background:#141414 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
    outline:none !important;
}

[data-baseweb="input"]:focus-within,
[data-baseweb="input"] > div:focus-within{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.35) !important;
    outline:none !important;
}

.stNumberInput button,
.stNumberInput [data-testid="stNumberInputStepUp"],
.stNumberInput [data-testid="stNumberInputStepDown"]{
    background:#181818 !important;
    border:1px solid #2A2A2A !important;
    color:#E5E5E5 !important;
    box-shadow:none !important;
}

.stNumberInput button:hover,
.stNumberInput [data-testid="stNumberInputStepUp"]:hover,
.stNumberInput [data-testid="stNumberInputStepDown"]:hover{
    background:#252525 !important;
    border:1px solid #E50914 !important;
    color:#FFFFFF !important;
}

.stSelectbox div[data-baseweb="select"],
.stSelectbox div[data-baseweb="select"] > div{
    background:#141414 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
    outline:none !important;
}

.stSelectbox div[data-baseweb="select"]:hover,
.stSelectbox div[data-baseweb="select"]:focus-within{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.28) !important;
}

[data-testid="stFileUploader"] section{
    background:#141414 !important;
    border:1px solid #2A2A2A !important;
    border-radius:14px !important;
    box-shadow:none !important;
}

[data-testid="stFileUploader"] section:hover{
    border:1px solid #E50914 !important;
    box-shadow:0 0 12px rgba(229,9,20,.20) !important;
}

/* Remove browser autofill white flash */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus{
    -webkit-text-fill-color:#F5F5F5 !important;
    transition: background-color 9999s ease-in-out 0s !important;
    box-shadow:0 0 0px 1000px #141414 inset !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# BRAND HEADER
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">ProjectRescue <span>AI</span></div>
    <div class="hero-subtitle">Enterprise Project Health & Recovery Advisor</div>
    <div class="hero-brand">Powered by ThinkLab.pm · Built by Sivasubramaniyan Sahadevan</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# CONFIG
# -----------------------------
# Executive PMO traffic-light palette.
# Critical and Watchlist are intentionally red/amber instead of blue so urgency is clear.
color_map = {
    "Green": "#52C41A", "Amber": "#FFC53D", "Red": "#FF4D4F",
    "On Track": "#52C41A", "Watchlist": "#FFC53D", "Critical": "#FF4D4F",
    "Critical Projects": "#FF4D4F", "Watchlist Projects": "#FFC53D"
}
risk_color_map = {
    "Critical": "#FF4D4F",
    "Watchlist": "#FFC53D",
    "Low": "#52C41A",
    "High": "#FF4D4F",
    "Medium": "#FFC53D"
}
health_icons = {"Green": "🟢 On Track", "Amber": "🟠 Watchlist", "Red": "🔴 Critical"}

features = [
    "cost_variance_percent", "schedule_variance_percent", "schedule_variance_days",
    "spi", "cpi", "completed_tasks_percent", "open_risks_count", "open_issues_count",
    "scope_changes_count", "resource_utilization_percent", "stakeholder_sentiment_score",
    "risk_score"
]

@st.cache_resource
def load_model():
    return joblib.load("project_rescue_model.pkl")

model = load_model()

def dark_plot(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B0B0B",
        plot_bgcolor="#0B0B0B",
        font=dict(color="#F5F5F5", size=15, family="Inter"),
        title=dict(font=dict(size=24, color="#FFFFFF", family="Inter")),
        legend=dict(
            title=dict(text="<b>Project Health</b>", font=dict(size=18, color="#FFFFFF", family="Inter")),
            font=dict(size=16, color="#FFFFFF", family="Inter"),
            bgcolor="rgba(20,20,20,0.88)",
            bordercolor="rgba(255,255,255,0.25)",
            borderwidth=1
        )
    )
    return fig


def polish_3d_portfolio_chart(fig):
    """Make the 3D portfolio chart executive-readable with bold titles and clear legends."""
    fig.update_traces(marker=dict(size=5, opacity=0.9))
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(text="<b>Schedule Delay (Days)</b>", font=dict(size=16, color="#FFFFFF")),
                tickfont=dict(size=12, color="#FFFFFF"),
                gridcolor="rgba(255,255,255,0.20)"
            ),
            yaxis=dict(
                title=dict(text="<b>Cost Variance (%)</b>", font=dict(size=16, color="#FFFFFF")),
                tickfont=dict(size=12, color="#FFFFFF"),
                gridcolor="rgba(255,255,255,0.20)"
            ),
            zaxis=dict(
                title=dict(text="<b>Risk Score</b>", font=dict(size=16, color="#FFFFFF")),
                tickfont=dict(size=12, color="#FFFFFF"),
                gridcolor="rgba(255,255,255,0.20)"
            )
        ),
        legend=dict(
            title=dict(text="<b>Project Health</b>", font=dict(size=18, color="#FFFFFF", family="Inter")),
            font=dict(size=16, color="#FFFFFF", family="Inter"),
            bgcolor="rgba(20,20,20,0.90)",
            bordercolor="rgba(255,255,255,0.35)",
            borderwidth=1
        ),
        title=dict(text="<b>3D Portfolio Risk View</b>", font=dict(size=24, color="#FFFFFF", family="Inter"))
    )
    return fig


# -----------------------------
# PMI / PMBOK-ALIGNED RULE ENGINE
# -----------------------------
# The ML model is retained as a secondary signal, but final health is governed by
# transparent PMO/EVM rules. This avoids contradictions such as Schedule = On Track
# while SPI is Critical.

SEVERITY_ORDER = {"Green": 0, "Amber": 1, "Red": 2}
STATUS_ORDER = {"Green": 0, "Amber": 1, "Red": 2}


def worst_health(*values):
    """Return the worst health value among Green/Amber/Red dimensions."""
    return max(values, key=lambda v: SEVERITY_ORDER.get(v, 0))


def status_label(status):
    """User-facing status labels."""
    return {"Green": "On Track", "Amber": "Watchlist", "Red": "Critical"}.get(status, status)


def evm_health(index_value):
    """PMI/EVM-aligned SPI/CPI health.

    SPI/CPI >= 0.95: within PMO tolerance
    0.85 - 0.94: management watchlist
    < 0.85: critical performance variance
    """
    if index_value >= 0.95:
        return "Green"
    if index_value >= 0.85:
        return "Amber"
    return "Red"


def variance_health(percent_value, green_limit=5, amber_limit=15):
    """Variance health for cost/schedule percentage variance."""
    if percent_value <= green_limit:
        return "Green"
    if percent_value <= amber_limit:
        return "Amber"
    return "Red"


def count_health(count_value, green_limit, amber_limit):
    if count_value <= green_limit:
        return "Green"
    if count_value <= amber_limit:
        return "Amber"
    return "Red"


def utilization_health(utilization):
    """Resource utilization aligned to overload risk.

    0-85%: sustainable
    86-95%: watchlist / potential overload
    >95%: critical overload risk
    """
    if utilization <= 85:
        return "Green"
    if utilization <= 95:
        return "Amber"
    return "Red"


def sentiment_health(sentiment):
    """Stakeholder alignment threshold.

    In real PMO reporting, 3.5/5 is usually managed/acceptable unless there are
    active escalations. 3.0-3.49 is watchlist; below 3.0 needs recovery action.
    """
    if sentiment >= 3.5:
        return "Green"
    if sentiment >= 3.0:
        return "Amber"
    return "Red"


def calculate_risk_score(cost, schedule_pct, delay_days, spi, cpi, completed, risks, issues, scope, utilization, sentiment):
    """0-100 PMO risk score.

    The score is weighted toward Earned Value Management because PMI EVM practice
    treats SPI and CPI as leading indicators of schedule and cost performance.
    """
    score = 0.0

    # Direct variance exposure
    score += max(cost, 0) * 0.80
    score += max(schedule_pct, 0) * 0.70

    # RAID/change exposure
    score += max(risks, 0) * 1.50
    score += max(issues, 0) * 1.20
    score += max(scope, 0) * 1.50

    # Resource and stakeholder exposure
    score += max(utilization - 85, 0) * 0.90
    score += max(3.5 - sentiment, 0) * 6.00

    # EVM performance penalties. Severe SPI/CPI should materially influence final score.
    if spi < 0.80:
        score += 25
    elif spi < 0.85:
        score += 20
    elif spi < 0.90:
        score += 12
    elif spi < 0.95:
        score += 6

    if cpi < 0.80:
        score += 27
    elif cpi < 0.85:
        score += 22
    elif cpi < 0.90:
        score += 14
    elif cpi < 0.95:
        score += 7

    # Late-stage projects with poor EVM performance have less room to recover.
    if completed >= 70 and (spi < 0.90 or cpi < 0.90):
        score += 5
    if completed >= 85 and (spi < 0.95 or cpi < 0.95):
        score += 5

    return round(min(score, 100), 2)


def classify_dimension(value, green_limit, amber_limit, reverse=False):
    """Backward-compatible helper for charts/legacy calls."""
    if reverse:
        if value >= green_limit:
            return "Green"
        elif value >= amber_limit:
            return "Amber"
        return "Red"
    if value <= green_limit:
        return "Green"
    elif value <= amber_limit:
        return "Amber"
    return "Red"


def health_breakdown(row):
    """Non-duplicated PMO dimension cards.

    SPI is embedded inside Schedule Performance.
    CPI is embedded inside Cost Performance.
    This removes duplicate Schedule/SPI and Cost/CPI cards while keeping the logic EVM-aligned.
    """
    spi_h = evm_health(float(row["spi"]))
    cpi_h = evm_health(float(row["cpi"]))
    schedule_delay_h = variance_health(float(row["schedule_delay_percent"]), 5, 15)
    cost_variance_h = variance_health(float(row["cost_variance_percent"]), 5, 15)

    schedule_h = worst_health(schedule_delay_h, spi_h)
    cost_h = worst_health(cost_variance_h, cpi_h)

    risk_h = count_health(int(row["open_risks_count"]), 4, 8)
    issue_h = count_health(int(row["open_issues_count"]), 4, 8)
    scope_h = count_health(int(row["scope_changes_count"]), 2, 5)
    raid_h = raid_maturity_health(row)

    return {
        "Schedule Performance": schedule_h,
        "Cost Performance": cost_h,
        "RAID Governance": raid_h,
        "Scope Control": scope_h,
        "Resource Capacity": utilization_health(float(row["resource_utilization_percent"])),
        "Stakeholder Alignment": sentiment_health(float(row["stakeholder_sentiment_score"])),
        "Delivery Progress": progress_health(row)
    }


def progress_health(row):
    """Progress view used as a soft indicator, not a hard override.

    A completed-task percentage alone should not make a project critical because it depends
    on where the project is in its lifecycle. This only flags very low progress when EVM
    signals are also poor.
    """
    completed = float(row["completed_tasks_percent"])
    spi = float(row["spi"])
    if completed < 40 and spi < 0.85:
        return "Red"
    if completed < 60 and spi < 0.95:
        return "Amber"
    return "Green"


def calculate_evm_forecast(bac, cpi):
    """PMBOK/EVM forecasting.

    EAC = BAC / CPI assumes future cost performance continues at the current CPI.
    VAC = BAC - EAC. Negative VAC means expected budget overrun.
    """
    bac = max(float(bac), 0)
    cpi = max(float(cpi), 0.01)
    eac = bac / cpi
    vac = bac - eac
    vac_percent = (vac / bac) * 100 if bac > 0 else 0
    return round(eac, 2), round(vac, 2), round(vac_percent, 2)


def raid_maturity_score(row):
    """Proxy RAID maturity score from available inputs.

    This is intentionally conservative: a few open risks/issues should not make
    governance look fully mature. The score represents control discipline, not
    the absence of all risks.
    """
    risks = int(row["open_risks_count"])
    issues = int(row["open_issues_count"])
    scope = int(row["scope_changes_count"])
    sentiment = float(row["stakeholder_sentiment_score"])

    score = 100.0
    score -= max(risks - 2, 0) * 5.0
    score -= max(issues - 2, 0) * 6.0
    score -= max(scope - 1, 0) * 5.0
    score -= max(4.0 - sentiment, 0) * 12.0

    if risks >= 9:
        score -= 12
    if issues >= 9:
        score -= 14
    if scope >= 6:
        score -= 10

    return round(max(min(score, 100), 0), 1)

def raid_maturity_health(row):
    score = float(row.get("raid_maturity_score", raid_maturity_score(row)))
    if score >= 75:
        return "Green"
    if score >= 60:
        return "Amber"
    return "Red"


def raid_maturity_label(score):
    if score >= 90:
        return "Mature"
    if score >= 75:
        return "Managed"
    if score >= 60:
        return "Developing"
    return "Weak"


def kpi_severity_level(status):
    return {"Green": "Low", "Amber": "Watchlist", "Red": "Critical"}[status]


def kpi_severity_score(status):
    return {"Green": 1, "Amber": 2, "Red": 3}[status]


def get_top_kpis(row):
    """Executive-friendly drivers using actual KPI values, not arbitrary impact points."""
    kpis = []

    def add(driver, value, health, signal):
        kpis.append({
            "Driver": driver,
            "KPI Value": value,
            "Risk Level": kpi_severity_level(health),
            "PMO Signal": signal,
            "Severity Score": kpi_severity_score(health)
        })

    add("CPI", f"{float(row['cpi']):.2f}", evm_health(float(row["cpi"])), "Cost efficiency / earned value")
    add("SPI", f"{float(row['spi']):.2f}", evm_health(float(row["spi"])), "Schedule efficiency / earned value")
    add("Cost Variance", f"{float(row['cost_variance_percent']):.1f}%", variance_health(float(row["cost_variance_percent"]), 5, 15), "Budget variance")
    add("Schedule Delay", f"{float(row['schedule_delay_percent']):.1f}% / {float(row['schedule_variance_days']):.0f} days", variance_health(float(row["schedule_delay_percent"]), 5, 15), "Time variance")
    add("Open Risks", f"{int(row['open_risks_count'])}", count_health(int(row["open_risks_count"]), 4, 8), "RAID exposure")
    add("Open Issues", f"{int(row['open_issues_count'])}", count_health(int(row["open_issues_count"]), 4, 8), "Execution blockers")
    add("Scope Changes", f"{int(row['scope_changes_count'])}", count_health(int(row["scope_changes_count"]), 2, 5), "Change control")
    add("Resource Utilization", f"{float(row['resource_utilization_percent']):.0f}%", utilization_health(float(row["resource_utilization_percent"])), "Capacity / overload")
    add("Stakeholder Sentiment", f"{float(row['stakeholder_sentiment_score']):.1f}/5", sentiment_health(float(row["stakeholder_sentiment_score"])), "Stakeholder alignment")
    add("RAID Maturity", f"{float(row['raid_maturity_score']):.1f}/100", raid_maturity_health(row), "Governance discipline")

    return sorted(kpis, key=lambda x: x["Severity Score"], reverse=True)[:6]


# Backward-compatible name used by existing render/export code.
def get_top_drivers(row):
    return get_top_kpis(row)


def risk_driver_level(level_or_score):
    """Compatibility helper. Accepts either a severity score or a Risk Level string."""
    if isinstance(level_or_score, str):
        return level_or_score
    if level_or_score >= 3:
        return "Critical"
    if level_or_score >= 2:
        return "Watchlist"
    return "Low"

def override_status(prediction, risk_score, spi, cpi, delay_percent, risks, issues, sentiment):
    """Final project health rule.

    Rule-based PMO governance is the source of truth. The ML model is retained
    for confidence/explainability, but it must not collapse the portfolio into
    only Green/Red. Amber should remain the normal management-watch category.
    """
    dimension_statuses = [
        variance_health(delay_percent, 5, 15),
        evm_health(spi),
        evm_health(cpi),
        count_health(risks, 4, 8),
        count_health(issues, 4, 8),
        sentiment_health(sentiment),
        "Red" if risk_score >= 70 else "Amber" if risk_score >= 35 else "Green"
    ]

    return worst_health(*dimension_statuses)

def sanity_check_status(status, row):
    severe = []
    dims = health_breakdown(row)

    # These names must match the non-duplicated real-life PMO dimensions
    # returned by health_breakdown(). This fixes the KeyError caused by
    # old labels such as "Schedule Health" and "Cost Health".
    if dims.get("Schedule Performance") == "Red":
        severe.append("Schedule performance is critical")
    if dims.get("Cost Performance") == "Red":
        severe.append("Cost performance is critical")
    if dims.get("RAID Governance") == "Red":
        severe.append("RAID governance maturity is weak")
    if dims.get("Scope Control") == "Red":
        severe.append("Scope control is critical")
    if dims.get("Resource Capacity") == "Red":
        severe.append("Resource capacity is critical")
    if dims.get("Stakeholder Alignment") == "Red":
        severe.append("Stakeholder alignment is low")

    # Never allow the final status to be lower than the worst health card.
    worst_dim = worst_health(*dims.values())
    if STATUS_ORDER[worst_dim] > STATUS_ORDER[status]:
        status = worst_dim

    return status, severe


def recovery_timeline(status, row):
    if status == "Green":
        return "No recovery required"
    if status == "Amber":
        if row["cost_variance_percent"] >= 10 or row["cpi"] < 0.95:
            return "4-6 weeks"
        if row["schedule_delay_percent"] >= 10 or row["spi"] < 0.95:
            return "3-5 weeks"
        return "2-4 weeks"
    if row["risk_score"] >= 85 or row["schedule_delay_percent"] >= 25 or row["cpi"] < 0.75:
        return "8-12 weeks"
    return "6-8 weeks"


def escalation_required(status, row):
    if status == "Red":
        return "Yes"
    if row["cost_variance_percent"] >= 20 or row["open_risks_count"] >= 10 or row["stakeholder_sentiment_score"] < 2.5:
        return "Yes"
    if status == "Amber":
        return "Monitor"
    return "No"


def summarize_dimension_watchlist(row, status):
    dims = health_breakdown(row)
    red_dims = [name for name, value in dims.items() if value == "Red"]
    amber_dims = [name for name, value in dims.items() if value == "Amber"]

    if red_dims:
        return f"Critical concern areas: {', '.join(red_dims)}."
    if amber_dims:
        return f"Watchlist areas: {', '.join(amber_dims)}."
    return "All assessed dimensions are within acceptable PMO tolerance."


def generate_recovery_plan(row, status):
    reasons, actions = [], []

    if row["schedule_delay_percent"] > 15 or row["schedule_variance_days"] >= 30:
        reasons.append(f"Schedule delay is significant at {row['schedule_variance_days']} days, equal to {row['schedule_delay_percent']}% of planned duration.")
        actions.append("Rebaseline the delivery plan and split remaining work into recovery milestones.")
    elif row["schedule_delay_percent"] > 5 or row["schedule_variance_days"] >= 15:
        reasons.append(f"Schedule delay is moderate at {row['schedule_variance_days']} days and requires management attention.")
        actions.append("Review milestone dependencies and remove blockers affecting the critical path.")

    if row["spi"] < 0.85:
        reasons.append(f"SPI is {row['spi']}, indicating critical schedule performance variance.")
        actions.append("Increase delivery cadence reviews, validate earned value, and recover critical-path work packages.")
    elif row["spi"] < 0.95:
        reasons.append(f"SPI is {row['spi']}, showing schedule performance below PMO tolerance.")
        actions.append("Review milestone delivery performance and correct planned-vs-earned work gaps.")

    if row["cost_variance_percent"] > 15:
        reasons.append(f"Cost variance is high at {row['cost_variance_percent']}%, which may require budget escalation.")
        actions.append("Perform budget impact analysis and stop or defer non-essential spend.")
    elif row["cost_variance_percent"] > 5:
        reasons.append(f"Cost variance is moderate at {row['cost_variance_percent']}% and should be reviewed.")
        actions.append("Review vendor/resource costs and validate Estimate at Completion.")

    if row["cpi"] < 0.85:
        reasons.append(f"CPI is {row['cpi']}, indicating critical cost efficiency variance.")
        actions.append("Review cost burn rate, remove low-value activities, and reset cost-to-complete controls.")
        actions.append("Recalculate EAC/VAC and confirm whether contingency or change approval is required.")
    elif row["cpi"] < 0.95:
        reasons.append(f"CPI is {row['cpi']}, showing cost performance below PMO tolerance.")
        actions.append("Tighten budget tracking and review cost-to-complete.")

    if row["open_risks_count"] > 8:
        reasons.append(f"There are {row['open_risks_count']} open risks, which may threaten delivery outcomes.")
        actions.append("Escalate top risks to steering committee with owners and due dates.")
    elif row["open_risks_count"] > 3:
        reasons.append(f"There are {row['open_risks_count']} open risks requiring active mitigation.")
        actions.append("Update RAID log and assign mitigation owners.")

    if row["open_issues_count"] > 8:
        reasons.append(f"There are {row['open_issues_count']} open issues, which may be blocking execution.")
        actions.append("Create an issue war-room and resolve high-impact blockers first.")
    elif row["open_issues_count"] > 3:
        reasons.append(f"There are {row['open_issues_count']} open issues requiring faster resolution.")
        actions.append("Assign issue owners and review blockers every 48 hours.")

    if row["scope_changes_count"] > 5:
        reasons.append(f"Scope volatility is high with {row['scope_changes_count']} scope changes.")
        actions.append("Freeze non-critical scope and enforce formal change control.")
    elif row["scope_changes_count"] > 2:
        reasons.append(f"There are {row['scope_changes_count']} scope changes, which should be controlled.")
        actions.append("Prioritize only business-critical changes through change control.")

    if row["resource_utilization_percent"] > 95:
        reasons.append(f"Resource utilization is critically high at {row['resource_utilization_percent']}%.")
        actions.append("Add temporary support or rebalance workload to reduce burnout risk.")
    elif row["resource_utilization_percent"] > 85:
        reasons.append(f"Resource utilization is high at {row['resource_utilization_percent']}%.")
        actions.append("Review workload distribution across the team.")

    if row["stakeholder_sentiment_score"] < 3.0:
        reasons.append(f"Stakeholder sentiment is low at {row['stakeholder_sentiment_score']}/5.")
        actions.append("Conduct stakeholder alignment meeting and reset communication cadence.")
    elif row["stakeholder_sentiment_score"] < 3.5:
        reasons.append(f"Stakeholder sentiment is watchlist-level at {row['stakeholder_sentiment_score']}/5.")
        actions.append("Increase stakeholder updates and clarify expectations.")

    if row["project_type"] == "Procurement Automation" and (row["cost_variance_percent"] > 5 or row["cpi"] < 0.95):
        actions.extend([
            "Reforecast Estimate at Completion for procurement spend.",
            "Review vendor contracts, invoices, and approval delays.",
            "Freeze non-essential procurement requests until budget variance is controlled."
        ])

    if row["project_type"] == "Cloud Migration" and (row["schedule_delay_percent"] > 5 or row["spi"] < 0.95):
        actions.append("Review migration wave plan, cutover readiness, and rollback strategy.")

    if row["project_type"] == "ERP Implementation" and status in ["Amber", "Red"]:
        actions.append("Validate data migration readiness, testing completion, and go-live criteria.")

    if row["project_type"] == "Cybersecurity Program" and status in ["Amber", "Red"]:
        actions.append("Review unresolved vulnerabilities, compliance gaps, and executive risk exposure.")

    if not reasons:
        reasons = [
            "Project KPIs are within acceptable PMO thresholds.",
            f"SPI is {row['spi']} and CPI is {row['cpi']}, indicating stable schedule and cost performance.",
            f"Open risks ({row['open_risks_count']}) and issues ({row['open_issues_count']}) are manageable.",
            f"Stakeholder sentiment is positive at {row['stakeholder_sentiment_score']}/5."
        ]

    if not actions:
        actions = [
            "Continue weekly KPI monitoring.",
            "Maintain current delivery rhythm.",
            "Track risks, issues, and stakeholder communication."
        ]

    timeline = recovery_timeline(status, row)
    escalation = escalation_required(status, row)
    dimension_note = summarize_dimension_watchlist(row, status)
    readable_status = status_label(status)
    forecast_note = (
        f" EAC is {row['eac']:,.0f} against BAC {row['budget_at_completion']:,.0f}; "
        f"VAC is {row['vac']:,.0f} ({row['vac_percent']:.1f}%). "
        f"RAID maturity is {row['raid_maturity_score']}/100 ({row['raid_maturity_label']})."
    )

    if status == "Red":
        priority = "High"
        summary = (
            f"This {row['project_type']} project is classified as {readable_status} with a risk score of {row['risk_score']}. "
            f"{dimension_note}{forecast_note} Immediate recovery governance, leadership visibility, and owner-driven corrective actions are required. "
            f"Estimated recovery timeline is {timeline}."
        )
    elif status == "Amber":
        priority = "Medium"
        summary = (
            f"This {row['project_type']} project is classified as {readable_status} with a risk score of {row['risk_score']}. "
            f"{dimension_note}{forecast_note} The project appears recoverable within {timeline} if corrective actions are taken now."
        )
    else:
        priority = "Low"
        summary = (
            f"This {row['project_type']} project is classified as {readable_status} with a risk score of {row['risk_score']}. "
            f"{dimension_note}{forecast_note} Continue standard PMO monitoring and review watchlist items during the next status cycle."
        )

    return summary, priority, reasons, actions, timeline, escalation


def assess_project(row):
    duration = max(float(row.get("project_duration_days", 180)), 1)
    schedule_days = max(float(row["schedule_variance_days"]), 0)
    schedule_pct = float(row.get("schedule_variance_percent", round((schedule_days / duration) * 100, 2)))

    risk_score = calculate_risk_score(
        float(row["cost_variance_percent"]), schedule_pct, schedule_days,
        float(row["spi"]), float(row["cpi"]), float(row["completed_tasks_percent"]),
        int(row["open_risks_count"]), int(row["open_issues_count"]), int(row["scope_changes_count"]),
        float(row["resource_utilization_percent"]), float(row["stakeholder_sentiment_score"])
    )

    input_df = pd.DataFrame([{**{f: None for f in features},
        "cost_variance_percent": float(row["cost_variance_percent"]),
        "schedule_variance_percent": schedule_pct,
        "schedule_variance_days": schedule_days,
        "spi": float(row["spi"]),
        "cpi": float(row["cpi"]),
        "completed_tasks_percent": float(row["completed_tasks_percent"]),
        "open_risks_count": int(row["open_risks_count"]),
        "open_issues_count": int(row["open_issues_count"]),
        "scope_changes_count": int(row["scope_changes_count"]),
        "resource_utilization_percent": float(row["resource_utilization_percent"]),
        "stakeholder_sentiment_score": float(row["stakeholder_sentiment_score"]),
        "risk_score": risk_score
    }])

    prediction = model.predict(input_df[features])[0]
    confidence = round(max(model.predict_proba(input_df[features])[0]) * 100, 2)

    final_status = override_status(
        prediction, risk_score, float(row["spi"]), float(row["cpi"]),
        schedule_pct, int(row["open_risks_count"]), int(row["open_issues_count"]),
        float(row["stakeholder_sentiment_score"])
    )

    result_row = {
        "project_name": row.get("project_name", "Manual Project"),
        "project_type": row.get("project_type", "General Project"),
        "project_duration_days": duration,
        "budget_at_completion": float(row.get("budget_at_completion", 100000)),
        "completed_tasks_percent": float(row["completed_tasks_percent"]),
        "cost_variance_percent": float(row["cost_variance_percent"]),
        "schedule_variance_days": schedule_days,
        "schedule_delay_percent": schedule_pct,
        "spi": float(row["spi"]),
        "cpi": float(row["cpi"]),
        "open_risks_count": int(row["open_risks_count"]),
        "open_issues_count": int(row["open_issues_count"]),
        "scope_changes_count": int(row["scope_changes_count"]),
        "resource_utilization_percent": float(row["resource_utilization_percent"]),
        "stakeholder_sentiment_score": float(row["stakeholder_sentiment_score"]),
        "risk_score": risk_score
    }

    result_row["eac"], result_row["vac"], result_row["vac_percent"] = calculate_evm_forecast(
        result_row["budget_at_completion"], result_row["cpi"]
    )
    result_row["raid_maturity_score"] = raid_maturity_score(result_row)
    result_row["raid_maturity_label"] = raid_maturity_label(result_row["raid_maturity_score"])

    final_status, severe_drivers = sanity_check_status(final_status, result_row)
    summary, priority, reasons, actions, timeline, escalation = generate_recovery_plan(result_row, final_status)

    return result_row, prediction, final_status, confidence, severe_drivers, summary, priority, reasons, actions, timeline, escalation

# PDF functions
def chart_to_buffer(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)
    buf.seek(0)
    return buf

def create_health_chart(dimensions):
    labels = list(dimensions.keys())
    colors_list = [color_map[dimensions[label]] for label in labels]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, [1] * len(labels), color=colors_list)
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_title("Health Breakdown by Dimension")
    return chart_to_buffer(fig)

def create_driver_chart(top_drivers):
    names = [x["Driver"] for x in top_drivers]
    scores = [x["Severity Score"] for x in top_drivers]
    labels = [x["KPI Value"] for x in top_drivers]
    colors_list = [risk_color_map[x["Risk Level"]] for x in top_drivers]
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(names, scores, color=colors_list)
    ax.set_title("KPI Severity View")
    ax.set_ylabel("Severity")
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Low", "Watchlist", "Critical"])
    ax.tick_params(axis="x", rotation=25)
    for bar, label in zip(bars, labels):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03, label, ha="center", va="bottom", fontsize=8)
    return chart_to_buffer(fig)

def create_pdf_report(project_name, final_status, confidence, risk_score, priority, timeline, escalation,
                      summary, dimensions, top_drivers, reasons, actions, result_row):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("ProjectRescue AI - Project Health Assessment Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Project Name:</b> {project_name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Project Type:</b> {result_row['project_type']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Final Health Status:</b> {final_status}", styles["Normal"]))
    story.append(Paragraph(f"<b>Confidence:</b> {confidence}%", styles["Normal"]))
    story.append(Paragraph(f"<b>Risk Score:</b> {risk_score}", styles["Normal"]))
    story.append(Paragraph(f"<b>BAC:</b> {result_row['budget_at_completion']:,.2f}", styles["Normal"]))
    story.append(Paragraph(f"<b>EAC:</b> {result_row['eac']:,.2f}", styles["Normal"]))
    story.append(Paragraph(f"<b>VAC:</b> {result_row['vac']:,.2f} ({result_row['vac_percent']:.1f}%)", styles["Normal"]))
    story.append(Paragraph(f"<b>RAID Maturity:</b> {result_row['raid_maturity_score']}/100 - {result_row['raid_maturity_label']}", styles["Normal"]))
    story.append(Paragraph(f"<b>Recovery Priority:</b> {priority}", styles["Normal"]))
    story.append(Paragraph(f"<b>Recovery Timeline:</b> {timeline}", styles["Normal"]))
    story.append(Paragraph(f"<b>Executive Escalation:</b> {escalation}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    story.append(Paragraph(summary, styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Health Breakdown Chart", styles["Heading2"]))
    story.append(Image(create_health_chart(dimensions), width=470, height=240))
    story.append(Spacer(1, 12))

    if top_drivers:
        story.append(Paragraph("Top KPI Risk Drivers Chart", styles["Heading2"]))
        story.append(Image(create_driver_chart(top_drivers), width=470, height=240))
        story.append(Spacer(1, 12))

    story.append(Paragraph("Key Reasons", styles["Heading2"]))
    for reason in reasons:
        story.append(Paragraph(f"- {reason}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Recommended Recovery Actions", styles["Heading2"]))
    for action in actions:
        story.append(Paragraph(f"- {action}", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

def render_result(result_row, prediction, final_status, confidence, severe_drivers, summary, priority, reasons, actions, timeline, escalation):
    dimensions = health_breakdown(result_row)
    top_drivers = get_top_drivers(result_row)
    card_class = {"Green": "green-card", "Amber": "amber-card", "Red": "red-card"}[final_status]

    st.markdown(f"""
    <div class="result-card {card_class}">
        <div style="font-size:18px;font-weight:700;opacity:.85;">Assessment Result</div>
        <div style="font-size:42px;font-weight:900;margin-top:6px;">{health_icons[final_status]}</div>
        <div class="result-grid">
            <div class="result-metric"><div class="result-label">Confidence</div><div class="result-value">{confidence}%</div></div>
            <div class="result-metric"><div class="result-label">Risk Score</div><div class="result-value">{result_row['risk_score']}</div></div>
            <div class="result-metric"><div class="result-label">Recovery Priority</div><div class="result-value">{priority}</div></div>
            <div class="result-metric"><div class="result-label">Timeline</div><div class="result-value">{timeline}</div></div>
            <div class="result-metric"><div class="result-label">Escalation</div><div class="result-value">{escalation}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Executive Summary")
    st.write(summary)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### EVM Forecast & RAID Maturity")
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("BAC", f"{result_row['budget_at_completion']:,.0f}")
    f2.metric("EAC", f"{result_row['eac']:,.0f}")
    f3.metric("VAC", f"{result_row['vac']:,.0f}", f"{result_row['vac_percent']:.1f}%")
    f4.metric("RAID Maturity", f"{result_row['raid_maturity_score']}/100", result_row['raid_maturity_label'])
    st.caption("EAC = BAC / CPI. VAC = BAC - EAC. Negative VAC indicates a forecast budget overrun.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Health Breakdown by Dimension")
    health_html = '<div class="health-grid">'
    for dimension_name, health_value in dimensions.items():
        health_html += (
            f'<div class="health-tile health-{health_value.lower()}">'
            f'<div class="health-name">{dimension_name}</div>'
            f'<div class="health-value">{health_icons[health_value]}</div>'
            '</div>'
        )
    health_html += '</div>'
    st.markdown(health_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Top KPI Risk Drivers")

    if top_drivers:
        driver_df = pd.DataFrame(top_drivers)

        table_html = '<table class="driver-table"><tr><th>Driver</th><th>KPI Value</th><th>Risk Level</th><th>PMO Signal</th></tr>'
        for _, rr in driver_df.iterrows():
            level = rr["Risk Level"]
            table_html += (
                f'<tr><td>{rr["Driver"]}</td>'
                f'<td>{rr["KPI Value"]}</td>'
                f'<td><span class="driver-badge driver-{level.lower()}">{level}</span></td>'
                f'<td>{rr["PMO Signal"]}</td></tr>'
            )
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)

        fig_driver = px.bar(
            driver_df,
            x="Driver",
            y="Severity Score",
            color="Risk Level",
            title="KPI Severity View",
            color_discrete_map=risk_color_map,
            text="KPI Value"
        )

        fig_driver.update_traces(
            textposition="outside",
            marker_line_color="rgba(255,255,255,0.9)",
            marker_line_width=2,
            opacity=0.96
        )

        fig_driver.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0B0B0B",
            plot_bgcolor="#0B0B0B",
            font=dict(color="#FFFFFF", size=15, family="Inter"),
            title=dict(text="<b>KPI Severity View</b>", font=dict(size=28, color="#FFFFFF")),
            xaxis=dict(
                title="<b>Driver</b>",
                title_font=dict(size=18, color="#FFFFFF"),
                tickfont=dict(size=15, color="#FFFFFF", family="Inter"),
                showgrid=False
            ),
            yaxis=dict(
                title="<b>Severity</b>",
                title_font=dict(size=18, color="#FFFFFF"),
                tickfont=dict(size=15, color="#FFFFFF", family="Inter"),
                gridcolor="rgba(255,255,255,0.18)"
            ),
            legend=dict(
                title=dict(text="<b>Risk Level</b>", font=dict(size=16, color="#FFFFFF")),
                font=dict(size=15, color="#FFFFFF"),
                bgcolor="rgba(20,20,20,0.85)",
                bordercolor="rgba(255,255,255,0.25)",
                borderwidth=1
            ),
            bargap=0.35
        )

        st.plotly_chart(fig_driver, use_container_width=True)
    else:
        st.write("No major risk drivers detected.")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Key Reasons")
    for reason in reasons:
        st.write(f"• {reason}")

    st.markdown("### Recommended Recovery Actions")
    for action in actions:
        st.write(f"• {action}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Export & Share")

    pdf_buffer = create_pdf_report(
        result_row["project_name"],
        final_status,
        confidence,
        result_row["risk_score"],
        priority,
        timeline,
        escalation,
        summary,
        dimensions,
        top_drivers,
        reasons,
        actions,
        result_row
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=f"{result_row['project_name'].replace(' ', '_')}_assessment_report.pdf",
        mime="application/pdf",
        key=f"download_pdf_{result_row['project_name']}_{result_row['risk_score']}"
    )

    reasons_text = "\n".join([f"- {r}" for r in reasons])
    actions_text = "\n".join([f"- {a}" for a in actions])
    top_drivers_text = (
        "\n".join([
            f"- {item['Driver']}: {item['KPI Value']} ({item['Risk Level']}) - {item['PMO Signal']}"
            for item in top_drivers
        ])
        if top_drivers else "No major risk drivers detected."
    )

    share_text = f"""
ProjectRescue AI Assessment Report

Project: {result_row['project_name']}
Project Type: {result_row['project_type']}
Health Status: {final_status}
Confidence: {confidence}%
Risk Score: {result_row['risk_score']}
BAC: {result_row['budget_at_completion']:,.0f}
EAC: {result_row['eac']:,.0f}
VAC: {result_row['vac']:,.0f} ({result_row['vac_percent']:.1f}%)
RAID Maturity: {result_row['raid_maturity_score']}/100 - {result_row['raid_maturity_label']}
Recovery Priority: {priority}
Recovery Timeline: {timeline}
Executive Escalation: {escalation}

Executive Summary:
{summary}

Top KPI Risk Drivers:
{top_drivers_text}

Key Reasons:
{reasons_text}

Recommended Recovery Actions:
{actions_text}

Note: The full PDF report includes visual charts. Download the PDF from ProjectRescue AI and attach it if required.

Generated by ProjectRescue AI | ThinkLab.pm
""".strip()

    encoded_text = urllib.parse.quote(share_text)
    encoded_subject = urllib.parse.quote(f"ProjectRescue AI Report - {result_row['project_name']}")
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_text}"

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("Share Summary on WhatsApp", whatsapp_url)
    with c2:
        st.link_button("Share Summary via Gmail", gmail_url)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# PORTFOLIO EXECUTIVE INSIGHTS
# -----------------------------
def portfolio_dimension_dataframe(assessed_df):
    """Build dimension-level portfolio distribution from the same logic used in Single Project Assessment."""
    records = []
    for _, row in assessed_df.iterrows():
        dims = health_breakdown(row)
        for dimension, health in dims.items():
            records.append({
                "Dimension": dimension,
                "Health": status_label(health),
                "Raw Health": health,
                "Project": row.get("project_name", "Project")
            })
    return pd.DataFrame(records)


def portfolio_kpi_driver_summary(assessed_df):
    """Aggregate KPI risk signals across the full portfolio using actual KPI values."""
    rows = []

    def add(driver, value, critical_count, watchlist_count, pmo_signal):
        total = len(assessed_df)
        exposure_count = int(critical_count + watchlist_count)
        exposure_pct = round((exposure_count / total) * 100, 1) if total else 0
        rows.append({
            "Driver": driver,
            "Portfolio KPI": value,
            "Critical Projects": int(critical_count),
            "Watchlist Projects": int(watchlist_count),
            "Exposure %": f"{exposure_pct}%",
            "PMO Signal": pmo_signal
        })

    total = max(len(assessed_df), 1)
    spi_health = assessed_df["spi"].apply(evm_health)
    cpi_health = assessed_df["cpi"].apply(evm_health)
    cost_health = assessed_df["cost_variance_percent"].apply(lambda x: variance_health(float(x), 5, 15))
    schedule_health = assessed_df["schedule_delay_percent"].apply(lambda x: variance_health(float(x), 5, 15))
    risk_health = assessed_df["open_risks_count"].apply(lambda x: count_health(int(x), 4, 8))
    issue_health = assessed_df["open_issues_count"].apply(lambda x: count_health(int(x), 4, 8))
    scope_health = assessed_df["scope_changes_count"].apply(lambda x: count_health(int(x), 2, 5))
    stakeholder_health = assessed_df["stakeholder_sentiment_score"].apply(lambda x: sentiment_health(float(x)))
    raid_health = assessed_df.apply(lambda r: raid_maturity_health(r), axis=1)

    add("Cost Performance / CPI", f"Avg CPI {assessed_df['cpi'].mean():.2f}", (cpi_health == "Red").sum(), (cpi_health == "Amber").sum(), "Earned value cost efficiency")
    add("Schedule Performance / SPI", f"Avg SPI {assessed_df['spi'].mean():.2f}", (spi_health == "Red").sum(), (spi_health == "Amber").sum(), "Earned value schedule efficiency")
    add("Cost Variance", f"Avg {assessed_df['cost_variance_percent'].mean():.1f}%", (cost_health == "Red").sum(), (cost_health == "Amber").sum(), "Budget variance exposure")
    add("Schedule Delay", f"Avg {assessed_df['schedule_delay_percent'].mean():.1f}%", (schedule_health == "Red").sum(), (schedule_health == "Amber").sum(), "Time variance exposure")
    add("Open Risks", f"Avg {assessed_df['open_risks_count'].mean():.1f}", (risk_health == "Red").sum(), (risk_health == "Amber").sum(), "RAID risk exposure")
    add("Open Issues", f"Avg {assessed_df['open_issues_count'].mean():.1f}", (issue_health == "Red").sum(), (issue_health == "Amber").sum(), "Execution blockers")
    add("Scope Changes", f"Avg {assessed_df['scope_changes_count'].mean():.1f}", (scope_health == "Red").sum(), (scope_health == "Amber").sum(), "Change control discipline")
    add("Stakeholder Sentiment", f"Avg {assessed_df['stakeholder_sentiment_score'].mean():.1f}/5", (stakeholder_health == "Red").sum(), (stakeholder_health == "Amber").sum(), "Stakeholder alignment")
    add("RAID Maturity", f"Avg {assessed_df['raid_maturity_score'].mean():.1f}/100", (raid_health == "Red").sum(), (raid_health == "Amber").sum(), "Governance maturity")

    out = pd.DataFrame(rows)
    out["Exposure Sort"] = out["Critical Projects"] * 3 + out["Watchlist Projects"]
    return out.sort_values("Exposure Sort", ascending=False).drop(columns=["Exposure Sort"])


def portfolio_health_matrix(assessed_df):
    """Create a practical PMO matrix: Schedule Performance vs Cost Performance.

    Rows = schedule health; columns = cost health. This shows where the portfolio
    needs governance focus: schedule-only, cost-only, or combined recovery.
    """
    records = []
    for _, row in assessed_df.iterrows():
        dims = health_breakdown(row)
        records.append({
            "Schedule Performance": status_label(dims["Schedule Performance"]),
            "Cost Performance": status_label(dims["Cost Performance"]),
            "Project": row.get("project_name", "Project")
        })

    matrix = pd.DataFrame(records)
    order = ["On Track", "Watchlist", "Critical"]
    matrix_counts = (
        matrix.groupby(["Schedule Performance", "Cost Performance"])
        .size()
        .reset_index(name="Project Count")
        .pivot(index="Schedule Performance", columns="Cost Performance", values="Project Count")
        .reindex(index=order, columns=order)
        .fillna(0)
        .astype(int)
    )
    return matrix_counts


def portfolio_priority_matrix(assessed_df):
    """Portfolio prioritization matrix: Risk Score band vs RAID Maturity band."""
    def risk_band(score):
        score = float(score)
        if score >= 70:
            return "High Risk"
        if score >= 35:
            return "Medium Risk"
        return "Low Risk"

    def raid_band(score):
        score = float(score)
        if score >= 75:
            return "Managed/Mature"
        if score >= 60:
            return "Developing"
        return "Weak"

    tmp = assessed_df.copy()
    tmp["Risk Band"] = tmp["risk_score"].apply(risk_band)
    tmp["RAID Band"] = tmp["raid_maturity_score"].apply(raid_band)

    risk_order = ["Low Risk", "Medium Risk", "High Risk"]
    raid_order = ["Managed/Mature", "Developing", "Weak"]
    matrix_counts = (
        tmp.groupby(["Risk Band", "RAID Band"])
        .size()
        .reset_index(name="Project Count")
        .pivot(index="Risk Band", columns="RAID Band", values="Project Count")
        .reindex(index=risk_order, columns=raid_order)
        .fillna(0)
        .astype(int)
    )
    return matrix_counts


def portfolio_recovery_actions(assessed_df):
    actions = []
    critical_count = int((assessed_df["final_status"] == "Red").sum())
    watchlist_count = int((assessed_df["final_status"] == "Amber").sum())
    cpi_critical = int((assessed_df["cpi"].apply(evm_health) == "Red").sum())
    spi_critical = int((assessed_df["spi"].apply(evm_health) == "Red").sum())
    overrun_total = float(abs(assessed_df.loc[assessed_df["vac"] < 0, "vac"].sum())) if "vac" in assessed_df else 0

    if critical_count:
        actions.append(f"Create a recovery command center for {critical_count} Critical projects with named owners, weekly executive review, and decision log tracking.")
    if watchlist_count:
        actions.append(f"Move {watchlist_count} Watchlist projects into preventive-control cadence before they become Critical.")
    if cpi_critical:
        actions.append(f"Run cost-to-complete and vendor/resource burn-rate review for {cpi_critical} projects with critical CPI.")
    if spi_critical:
        actions.append(f"Run critical-path and milestone recovery planning for {spi_critical} projects with critical SPI.")
    if overrun_total > 0:
        actions.append(f"Review portfolio forecast overrun exposure of {overrun_total:,.0f} based on negative VAC.")
    if assessed_df["raid_maturity_score"].mean() < 75:
        actions.append("Improve RAID governance: owner, due date, mitigation, aging, and escalation discipline for weak/developing projects.")
    if not actions:
        actions.append("Portfolio is within PMO tolerance. Continue standard governance, KPI trend review, and monthly steering reporting.")
    return actions


def render_portfolio_results(assessed_df, portfolio_file_name=None):
    """Detailed portfolio view matching the depth of Single Project Assessment."""
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    header_col, clear_col = st.columns([4, 1])
    with header_col:
        st.subheader("Portfolio Results")
        if portfolio_file_name:
            st.caption(f"Analyzed file: {portfolio_file_name}")
    with clear_col:
        clear_portfolio = st.button("Clear Results", key="clear_portfolio_results")

    if clear_portfolio:
        st.session_state.portfolio_results = None
        st.session_state.portfolio_file_name = None
        st.rerun()

    total_projects = len(assessed_df)
    critical_projects = int((assessed_df["final_status"] == "Red").sum())
    watchlist_projects = int((assessed_df["final_status"] == "Amber").sum())
    ontrack_projects = int((assessed_df["final_status"] == "Green").sum())
    avg_risk = round(assessed_df["risk_score"].mean(), 2)
    avg_raid = round(assessed_df["raid_maturity_score"].mean(), 1)
    total_bac = float(assessed_df["budget_at_completion"].sum()) if "budget_at_completion" in assessed_df else 0
    total_eac = float(assessed_df["eac"].sum()) if "eac" in assessed_df else 0
    total_vac = float(assessed_df["vac"].sum()) if "vac" in assessed_df else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Projects", total_projects)
    c2.metric("Critical Projects", critical_projects)
    c3.metric("Watchlist Projects", watchlist_projects)
    c4.metric("On Track Projects", ontrack_projects)

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Average Risk Score", avg_risk)
    c6.metric("Average RAID Maturity", f"{avg_raid}/100")
    c7.metric("Total BAC", f"{total_bac:,.0f}")
    c8.metric("Total Forecast VAC", f"{total_vac:,.0f}")

    st.markdown("### Portfolio Executive Summary")
    st.write(
        f"This portfolio contains {total_projects} projects: {ontrack_projects} On Track, "
        f"{watchlist_projects} Watchlist, and {critical_projects} Critical. "
        f"Average risk score is {avg_risk}, average RAID maturity is {avg_raid}/100, "
        f"and total forecast variance at completion is {total_vac:,.0f}."
    )

    st.markdown("### Portfolio EVM Forecast & RAID Maturity")
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Total BAC", f"{total_bac:,.0f}")
    e2.metric("Total EAC", f"{total_eac:,.0f}")
    e3.metric("Total VAC", f"{total_vac:,.0f}")
    e4.metric("Avg RAID Maturity", f"{avg_raid}/100")
    st.caption("EAC = BAC / CPI at project level. VAC = BAC - EAC. Negative VAC indicates forecast budget overrun.")

    col1, col2 = st.columns(2)
    with col1:
        status_order = ["On Track", "Watchlist", "Critical"]
        fig1 = px.pie(
            assessed_df,
            names="portfolio_health",
            title="<b>Portfolio Health Distribution</b>",
            color="portfolio_health",
            category_orders={"portfolio_health": status_order},
            color_discrete_map=color_map,
            hole=0.45
        )
        fig1.update_traces(textinfo="percent+label", marker=dict(line=dict(color="#111111", width=2)))
        st.plotly_chart(dark_plot(fig1), use_container_width=True)

    with col2:
        fig2 = px.scatter_3d(
            assessed_df,
            x="schedule_variance_days",
            y="cost_variance_percent",
            z="risk_score",
            color="portfolio_health",
            hover_name="project_name",
            title="<b>3D Portfolio Risk View</b>",
            category_orders={"portfolio_health": status_order},
            color_discrete_map=color_map
        )
        st.plotly_chart(polish_3d_portfolio_chart(dark_plot(fig2)), use_container_width=True)

    st.markdown("### Health Breakdown by Dimension")
    dim_df = portfolio_dimension_dataframe(assessed_df)
    dim_counts = dim_df.groupby(["Dimension", "Health"]).size().reset_index(name="Project Count")
    fig_dim = px.bar(
        dim_counts,
        x="Dimension",
        y="Project Count",
        color="Health",
        title="<b>Portfolio Dimension Health Distribution</b>",
        category_orders={"Health": ["On Track", "Watchlist", "Critical"]},
        color_discrete_map=color_map,
        text="Project Count"
    )
    fig_dim.update_traces(textposition="outside")
    fig_dim.update_layout(
        barmode="group",
        xaxis=dict(title="<b>PMO Dimension</b>", tickangle=-20, title_font=dict(size=16), tickfont=dict(size=13)),
        yaxis=dict(title="<b>Project Count</b>", title_font=dict(size=16)),
        legend=dict(title=dict(text="<b>Health</b>"), font=dict(size=15))
    )
    st.plotly_chart(dark_plot(fig_dim), use_container_width=True)

    st.markdown("### Top Portfolio KPI Risk Drivers")
    driver_summary = portfolio_kpi_driver_summary(assessed_df)
    st.dataframe(driver_summary, use_container_width=True, hide_index=True)

    fig_driver = px.bar(
        driver_summary.head(8),
        x="Driver",
        y=["Critical Projects", "Watchlist Projects"],
        title="<b>Critical & Watchlist Exposure by KPI</b>",
        barmode="group",
        text_auto=True,
        color_discrete_map={
            "Critical Projects": color_map["Critical Projects"],
            "Watchlist Projects": color_map["Watchlist Projects"]
        }
    )
    fig_driver.update_traces(marker_line_color="rgba(255,255,255,0.85)", marker_line_width=1.5)
    fig_driver.update_layout(
        xaxis=dict(title="<b>KPI Driver</b>", tickangle=-20, title_font=dict(size=16), tickfont=dict(size=14, color="#FFFFFF")),
        yaxis=dict(title="<b>Number of Projects</b>", title_font=dict(size=16), tickfont=dict(size=14, color="#FFFFFF")),
        legend=dict(title=dict(text="<b>Exposure Level</b>", font=dict(size=17, color="#FFFFFF")), font=dict(size=15, color="#FFFFFF"))
    )
    st.plotly_chart(dark_plot(fig_driver), use_container_width=True)

    st.markdown("### Portfolio Matrix View")
    m1, m2 = st.columns(2)
    schedule_cost_matrix = portfolio_health_matrix(assessed_df)
    priority_matrix = portfolio_priority_matrix(assessed_df)

    # Heatmap color is based on risk severity, not count volume.
    # This prevents healthy high-volume cells from appearing red.
    matrix_colorscale = [
        [0.0, "#173D25"], [0.49, "#173D25"],
        [0.50, "#7A5200"], [0.74, "#7A5200"],
        [0.75, "#8B0000"], [1.0, "#8B0000"]
    ]

    with m1:
        st.markdown("#### Schedule vs Cost Performance Matrix")
        status_risk = {"On Track": 0, "Watchlist": 1, "Critical": 2}
        schedule_cost_severity = pd.DataFrame(
            [[max(status_risk.get(row_label, 0), status_risk.get(col_label, 0)) for col_label in schedule_cost_matrix.columns] for row_label in schedule_cost_matrix.index],
            index=schedule_cost_matrix.index,
            columns=schedule_cost_matrix.columns
        )
        fig_matrix = go.Figure(data=go.Heatmap(
            z=schedule_cost_severity.values,
            x=list(schedule_cost_matrix.columns),
            y=list(schedule_cost_matrix.index),
            zmin=0,
            zmax=2,
            colorscale=matrix_colorscale,
            showscale=False,
            text=schedule_cost_matrix.values,
            customdata=schedule_cost_matrix.values,
            texttemplate="<b>%{text}</b>",
            textfont={"size": 18, "color": "#FFFFFF"},
            hovertemplate="Schedule: %{y}<br>Cost: %{x}<br>Projects: %{customdata}<extra></extra>"
        ))
        fig_matrix.update_layout(
            title="<b>Schedule-Cost Exposure Matrix</b>",
            xaxis_title="<b>Cost Performance</b>",
            yaxis_title="<b>Schedule Performance</b>",
            paper_bgcolor="#0B0B0B",
            plot_bgcolor="#0B0B0B",
            font=dict(color="#FFFFFF", family="Inter"),
            height=430
        )
        st.plotly_chart(fig_matrix, use_container_width=True)
        st.dataframe(schedule_cost_matrix, use_container_width=True)

    with m2:
        st.markdown("#### Risk Score vs RAID Governance Matrix")
        risk_band_score = {"Low Risk": 0, "Medium Risk": 1, "High Risk": 2}
        raid_band_score = {"Managed/Mature": 0, "Developing": 1, "Weak": 2}
        priority_severity = pd.DataFrame(
            [[max(risk_band_score.get(row_label, 0), raid_band_score.get(col_label, 0)) for col_label in priority_matrix.columns] for row_label in priority_matrix.index],
            index=priority_matrix.index,
            columns=priority_matrix.columns
        )
        fig_priority = go.Figure(data=go.Heatmap(
            z=priority_severity.values,
            x=list(priority_matrix.columns),
            y=list(priority_matrix.index),
            zmin=0,
            zmax=2,
            colorscale=matrix_colorscale,
            showscale=False,
            text=priority_matrix.values,
            customdata=priority_matrix.values,
            texttemplate="<b>%{text}</b>",
            textfont={"size": 18, "color": "#FFFFFF"},
            hovertemplate="Risk Band: %{y}<br>RAID Band: %{x}<br>Projects: %{customdata}<extra></extra>"
        ))
        fig_priority.update_layout(
            title="<b>Recovery Priority Matrix</b>",
            xaxis_title="<b>RAID Maturity</b>",
            yaxis_title="<b>Risk Score Band</b>",
            paper_bgcolor="#0B0B0B",
            plot_bgcolor="#0B0B0B",
            font=dict(color="#FFFFFF", family="Inter"),
            height=430
        )
        st.plotly_chart(fig_priority, use_container_width=True)
        st.dataframe(priority_matrix, use_container_width=True)

    st.caption("Matrix colors show severity: green = healthy/managed, amber = watchlist, red = critical. Cell numbers show project count.")

    st.markdown("### Portfolio Bubble Matrix")
    bubble_df = assessed_df.copy()
    bubble_df["Portfolio Health"] = bubble_df["final_status"].apply(status_label)
    bubble_df["Bubble Size"] = bubble_df.get("budget_at_completion", pd.Series([100000] * len(bubble_df))).astype(float).clip(lower=1)
    fig_bubble = px.scatter(
        bubble_df,
        x="schedule_delay_percent",
        y="cost_variance_percent",
        size="Bubble Size",
        color="Portfolio Health",
        hover_name="project_name",
        hover_data={
            "project_type": True,
            "spi": ":.2f",
            "cpi": ":.2f",
            "risk_score": ":.1f",
            "raid_maturity_score": ":.1f",
            "Bubble Size": False
        },
        title="<b>Schedule Delay vs Cost Variance Bubble Matrix</b>",
        category_orders={"Portfolio Health": ["On Track", "Watchlist", "Critical"]},
        color_discrete_map=color_map,
        size_max=28
    )
    fig_bubble.update_layout(
        xaxis=dict(title="<b>Schedule Delay %</b>", title_font=dict(size=16), tickfont=dict(size=13)),
        yaxis=dict(title="<b>Cost Variance %</b>", title_font=dict(size=16), tickfont=dict(size=13)),
        legend=dict(title=dict(text="<b>Project Health</b>", font=dict(size=17, color="#FFFFFF")), font=dict(size=15, color="#FFFFFF")),
        height=520
    )
    fig_bubble.add_vline(x=5, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    fig_bubble.add_vline(x=15, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    fig_bubble.add_hline(y=5, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    fig_bubble.add_hline(y=15, line_dash="dash", line_color="rgba(255,255,255,0.35)")
    st.plotly_chart(dark_plot(fig_bubble), use_container_width=True)

    st.markdown("### Portfolio Recovery Actions")
    for action in portfolio_recovery_actions(assessed_df):
        st.write(f"• {action}")

    st.markdown("### Critical Project Watchlist")
    watch_cols = [
        "project_name", "project_type", "final_status", "risk_score", "recovery_priority",
        "executive_escalation", "spi", "cpi", "cost_variance_percent", "schedule_delay_percent",
        "eac", "vac", "raid_maturity_score", "open_risks_count", "open_issues_count"
    ]
    available_cols = [c for c in watch_cols if c in assessed_df.columns]
    priority_df = assessed_df.sort_values(["final_status", "risk_score"], ascending=[False, False])[available_cols]
    st.dataframe(priority_df.head(25), use_container_width=True, hide_index=True)

    st.markdown("### Assessed Project Results")
    st.dataframe(assessed_df, use_container_width=True)

    st.download_button(
        "Download Detailed Assessed CSV",
        data=assessed_df.to_csv(index=False).encode("utf-8"),
        file_name="project_rescue_detailed_portfolio_results.csv",
        mime="text/csv",
        key="download_portfolio_csv"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# MAIN UI
# -----------------------------

# Session-state containers keep Portfolio and Single Project workflows independent.
if "portfolio_results" not in st.session_state:
    st.session_state.portfolio_results = None

if "portfolio_file_name" not in st.session_state:
    st.session_state.portfolio_file_name = None

if "manual_result" not in st.session_state:
    st.session_state.manual_result = None


tab_csv, tab_manual = st.tabs([
    "Portfolio Assessment",
    "Single Project Assessment"
])


with tab_csv:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Portfolio Assessment")

    with st.form("portfolio_form"):
        uploaded_file = st.file_uploader(
            "Upload project portfolio CSV",
            type=["csv"],
            key="portfolio_csv_upload"
        )

        st.caption("Upload your CSV, then click Analyze Portfolio. The app will not analyze automatically.")

        analyze_portfolio = st.form_submit_button("Analyze Portfolio")

    st.markdown("</div>", unsafe_allow_html=True)

    # If the uploaded file is removed, clear only the portfolio result output area.
    # This prevents old portfolio results from remaining visible after file removal.
    if uploaded_file is None:
        st.session_state.portfolio_results = None
        st.session_state.portfolio_file_name = None

    if analyze_portfolio:
        if uploaded_file is None:
            st.warning("Please upload a CSV file first.")
        else:
            df = pd.read_csv(uploaded_file)
            assessed_rows = []

            for _, r in df.iterrows():
                try:
                    result_row, prediction, final_status, confidence, severe, summary, priority, reasons, actions, timeline, escalation = assess_project(r)

                    assessed_rows.append({
                        **result_row,
                        "model_prediction": prediction,
                        "final_status": final_status,
                        "portfolio_health": status_label(final_status),
                        "confidence_percent": confidence,
                        "recovery_priority": priority,
                        "recovery_timeline": timeline,
                        "executive_escalation": escalation
                    })

                except Exception as e:
                    st.warning(f"Skipped one row due to invalid data: {e}")

            st.session_state.portfolio_results = pd.DataFrame(assessed_rows)
            st.session_state.portfolio_file_name = uploaded_file.name

    if st.session_state.portfolio_results is not None:
        assessed_df = st.session_state.portfolio_results

        if not assessed_df.empty:
            render_portfolio_results(assessed_df, st.session_state.portfolio_file_name)

    else:
        st.info("Upload a CSV file and click Analyze Portfolio.")


with tab_manual:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Single Project Assessment")

    with st.form("manual_project_form"):
        col_a, col_b = st.columns(2)

        with col_a:
            project_name = st.text_input(
                "Project Name",
                "Cloud Migration Program"
            )

            project_type = st.selectbox(
                "Project Type",
                [
                    "Cloud Migration",
                    "ERP Implementation",
                    "CRM Modernization",
                    "Data Warehouse Migration",
                    "Cybersecurity Program",
                    "ITSM Transformation",
                    "Procurement Automation",
                    "License Optimization",
                    "Infrastructure Refresh",
                    "Mobile App Development",
                    "AI Adoption Program"
                ]
            )

            project_duration_days = st.number_input(
                "Planned Project Duration Days",
                min_value=1,
                value=180
            )

            budget_at_completion = st.number_input(
                "Budget at Completion / BAC",
                min_value=0.0,
                value=100000.0,
                step=1000.0
            )

            completed_tasks_percent = st.slider(
                "Completed Tasks %",
                0,
                100,
                65
            )

            cost_variance_percent = st.number_input(
                "Cost Variance %",
                value=8.0
            )

            schedule_variance_days = st.number_input(
                "Schedule Delay Days",
                value=10
            )

            spi = st.number_input(
                "SPI",
                value=0.95,
                step=0.01
            )

            cpi = st.number_input(
                "CPI",
                value=0.96,
                step=0.01
            )

        with col_b:
            open_risks_count = st.number_input(
                "Open Risks",
                min_value=0,
                value=4
            )

            open_issues_count = st.number_input(
                "Open Issues",
                min_value=0,
                value=3
            )

            scope_changes_count = st.number_input(
                "Scope Changes",
                min_value=0,
                value=2
            )

            resource_utilization_percent = st.slider(
                "Resource Utilization %",
                0,
                100,
                85
            )

            stakeholder_sentiment_score = st.slider(
                "Stakeholder Sentiment",
                1.0,
                5.0,
                3.5,
                step=0.1
            )

        analyze_manual = st.form_submit_button("Analyze Project")

    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_manual:
        manual_row = {
            "project_name": project_name,
            "project_type": project_type,
            "project_duration_days": project_duration_days,
            "budget_at_completion": budget_at_completion,
            "completed_tasks_percent": completed_tasks_percent,
            "cost_variance_percent": cost_variance_percent,
            "schedule_variance_days": schedule_variance_days,
            "spi": spi,
            "cpi": cpi,
            "open_risks_count": open_risks_count,
            "open_issues_count": open_issues_count,
            "scope_changes_count": scope_changes_count,
            "resource_utilization_percent": resource_utilization_percent,
            "stakeholder_sentiment_score": stakeholder_sentiment_score
        }

        st.session_state.manual_result = assess_project(manual_row)

    if st.session_state.manual_result is not None:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        _, clear_col = st.columns([4, 1])
        with clear_col:
            clear_manual = st.button("Clear Result", key="clear_manual_result")

        if clear_manual:
            st.session_state.manual_result = None
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        render_result(*st.session_state.manual_result)


st.markdown("""
<div class="footer">
    ProjectRescue AI · ThinkLab.pm · Built by Sivasubramaniyan Sahadevan
</div>
""", unsafe_allow_html=True)
