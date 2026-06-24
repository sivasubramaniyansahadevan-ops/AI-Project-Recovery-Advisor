import streamlit as st
import pandas as pd
import plotly.express as px
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
color_map = {"Green": "#2ECC71", "Amber": "#F39C12", "Red": "#E74C3C"}
risk_color_map = {"High": "#E74C3C", "Medium": "#F39C12", "Low": "#2ECC71"}
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
        font_color="#F5F5F5",
        title_font_size=20,
        title_font_color="#FFFFFF",
        legend_title_font_color="#FFFFFF"
    )
    return fig

def calculate_risk_score(cost, schedule_pct, delay_days, spi, cpi, completed, risks, issues, scope, utilization, sentiment):
    """Balanced PMO scoring: mild SPI/CPI movement is watchlist, not automatic risk escalation."""
    score = 0
    score += max(cost, 0) * 0.8
    score += max(schedule_pct, 0) * 0.9
    score += risks * 1.5
    score += issues * 1.2
    score += scope * 1.6
    score += max(utilization - 85, 0) * 0.8
    score += max(3.8 - sentiment, 0) * 5

    if spi < 0.85:
        score += 14
    elif spi < 0.90:
        score += 8
    elif spi < 0.95:
        score += 4

    if cpi < 0.85:
        score += 14
    elif cpi < 0.90:
        score += 8
    elif cpi < 0.95:
        score += 4

    if completed > 80 and score > 40:
        score += 6

    return round(score, 2)

def classify_dimension(value, green_limit, amber_limit, reverse=False):
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
    return {
        "Schedule Health": classify_dimension(row["schedule_delay_percent"], 5, 15),
        "Cost Health": classify_dimension(row["cost_variance_percent"], 5, 15),
        "SPI Health": classify_dimension(row["spi"], 0.95, 0.85, reverse=True),
        "CPI Health": classify_dimension(row["cpi"], 0.95, 0.85, reverse=True),
        "Risk Health": classify_dimension(row["open_risks_count"], 3, 8),
        "Issue Health": classify_dimension(row["open_issues_count"], 3, 8),
        "Scope Health": classify_dimension(row["scope_changes_count"], 2, 5),
        "Resource Health": classify_dimension(row["resource_utilization_percent"], 85, 95),
        "Stakeholder Health": classify_dimension(row["stakeholder_sentiment_score"], 3.8, 2.8, reverse=True)
    }

def get_top_drivers(row):
    drivers = {
        "Cost Variance": row["cost_variance_percent"] * 0.8,
        "Schedule Delay %": row["schedule_delay_percent"] * 0.9,
        "Open Risks": row["open_risks_count"] * 1.5,
        "Open Issues": row["open_issues_count"] * 1.2,
        "Scope Changes": row["scope_changes_count"] * 1.6,
        "Resource Overload": max(row["resource_utilization_percent"] - 85, 0) * 0.8,
        "Stakeholder Concern": max(3.8 - row["stakeholder_sentiment_score"], 0) * 5,
        "SPI Impact": 14 if row["spi"] < 0.85 else 8 if row["spi"] < 0.90 else 4 if row["spi"] < 0.95 else 0,
        "CPI Impact": 14 if row["cpi"] < 0.85 else 8 if row["cpi"] < 0.90 else 4 if row["cpi"] < 0.95 else 0
    }
    return [(k, round(v, 2)) for k, v in sorted(drivers.items(), key=lambda x: x[1], reverse=True) if v > 0][:5]

def override_status(prediction, risk_score, spi, cpi, delay_percent, risks, issues, sentiment):
    """Final status logic. It keeps low-risk projects Green even when one or two KPIs are watchlist-level."""
    if risk_score >= 75 or spi < 0.80 or cpi < 0.80 or delay_percent >= 25 or risks >= 10 or issues >= 10 or sentiment < 2.5:
        return "Red"

    if risk_score >= 35 or spi < 0.90 or cpi < 0.90 or delay_percent >= 12 or risks >= 7 or issues >= 7 or sentiment < 3.0:
        return "Amber"

    if risk_score < 35 and delay_percent < 12 and risks < 7 and issues < 7 and sentiment >= 3.0:
        return "Green"

    return prediction

def sanity_check_status(status, row):
    severe = []
    if row["cost_variance_percent"] >= 20:
        severe.append("Cost variance is severe")
    if row["schedule_delay_percent"] >= 25:
        severe.append("Schedule delay is severe compared to project duration")
    if row["spi"] < 0.85:
        severe.append("SPI is critically low")
    if row["cpi"] < 0.85:
        severe.append("CPI is critically low")
    if row["open_risks_count"] >= 10:
        severe.append("Open risk count is high")
    if row["open_issues_count"] >= 10:
        severe.append("Open issue count is high")
    if row["stakeholder_sentiment_score"] < 2.5:
        severe.append("Stakeholder sentiment is low")

    if status == "Red" and not severe:
        return "Amber", severe

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
    if row["risk_score"] >= 90 or row["schedule_delay_percent"] >= 25:
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
    """Create a summary phrase that stays consistent with the dimension cards."""
    dims = health_breakdown(row)
    red_dims = [name.replace(" Health", "") for name, value in dims.items() if value == "Red"]
    amber_dims = [name.replace(" Health", "") for name, value in dims.items() if value == "Amber"]

    if red_dims:
        return f"Critical concern areas: {', '.join(red_dims)}."
    if amber_dims:
        return f"Watchlist areas: {', '.join(amber_dims)}."
    return "All assessed dimensions are within acceptable PMO tolerance."

def generate_recovery_plan(row, status):
    reasons, actions = [], []

    if row["schedule_delay_percent"] >= 20 or row["schedule_variance_days"] >= 30:
        reasons.append(f"Schedule delay is significant at {row['schedule_variance_days']} days, equal to {row['schedule_delay_percent']}% of planned duration.")
        actions.append("Rebaseline the delivery plan and split remaining work into recovery milestones.")
    elif row["schedule_delay_percent"] >= 10 or row["schedule_variance_days"] >= 15:
        reasons.append(f"Schedule delay is moderate at {row['schedule_variance_days']} days and requires management attention.")
        actions.append("Review milestone dependencies and remove blockers affecting the critical path.")

    if row["spi"] < 0.85:
        reasons.append(f"SPI is {row['spi']}, indicating serious schedule performance risk.")
        actions.append("Increase delivery cadence reviews and track planned vs completed work weekly.")
    elif row["spi"] < 0.90:
        reasons.append(f"SPI is {row['spi']}, showing meaningful schedule slippage against plan.")
        actions.append("Review sprint velocity or milestone delivery performance.")
    elif row["spi"] < 0.95 and status != "Green":
        reasons.append(f"SPI is {row['spi']}, showing a watchlist-level schedule variance.")
        actions.append("Monitor milestone delivery trend in the next status review.")

    if row["cost_variance_percent"] >= 20:
        reasons.append(f"Cost variance is high at {row['cost_variance_percent']}%, which may require budget escalation.")
        actions.append("Perform budget impact analysis and stop non-essential spending.")
    elif row["cost_variance_percent"] >= 10:
        reasons.append(f"Cost variance is moderate at {row['cost_variance_percent']}% and should be reviewed.")
        actions.append("Review vendor/resource costs and validate remaining forecast.")

    if row["cpi"] < 0.85:
        reasons.append(f"CPI is {row['cpi']}, indicating poor cost efficiency.")
        actions.append("Review cost burn rate and identify low-value activities.")
    elif row["cpi"] < 0.90:
        reasons.append(f"CPI is {row['cpi']}, showing meaningful cost performance concern.")
        actions.append("Tighten budget tracking and review cost-to-complete.")
    elif row["cpi"] < 0.95 and status != "Green":
        reasons.append(f"CPI is {row['cpi']}, showing a watchlist-level cost variance.")
        actions.append("Monitor cost-to-complete and validate next forecast cycle.")

    if row["open_risks_count"] >= 10:
        reasons.append(f"There are {row['open_risks_count']} open risks, which may threaten delivery outcomes.")
        actions.append("Escalate top risks to steering committee with owners and due dates.")
    elif row["open_risks_count"] >= 5:
        reasons.append(f"There are {row['open_risks_count']} open risks requiring active mitigation.")
        actions.append("Update RAID log and assign mitigation owners.")

    if row["open_issues_count"] >= 10:
        reasons.append(f"There are {row['open_issues_count']} open issues, which may be blocking execution.")
        actions.append("Create an issue war-room and resolve high-impact blockers first.")
    elif row["open_issues_count"] >= 5:
        reasons.append(f"There are {row['open_issues_count']} open issues requiring faster resolution.")
        actions.append("Assign issue owners and review blockers every 48 hours.")

    if row["scope_changes_count"] >= 7:
        reasons.append(f"Scope volatility is high with {row['scope_changes_count']} scope changes.")
        actions.append("Freeze non-critical scope and enforce change control.")
    elif row["scope_changes_count"] >= 4:
        reasons.append(f"There are {row['scope_changes_count']} scope changes, which should be controlled.")
        actions.append("Prioritize only business-critical changes.")

    if row["resource_utilization_percent"] >= 95:
        reasons.append(f"Resource utilization is critically high at {row['resource_utilization_percent']}%.")
        actions.append("Add temporary support or rebalance workload to reduce burnout risk.")
    elif row["resource_utilization_percent"] >= 88:
        reasons.append(f"Resource utilization is high at {row['resource_utilization_percent']}%.")
        actions.append("Review workload distribution across the team.")

    if row["stakeholder_sentiment_score"] < 2.5:
        reasons.append(f"Stakeholder sentiment is low at {row['stakeholder_sentiment_score']}/5.")
        actions.append("Conduct stakeholder alignment meeting and reset communication cadence.")
    elif row["stakeholder_sentiment_score"] < 3.5:
        reasons.append(f"Stakeholder sentiment is neutral at {row['stakeholder_sentiment_score']}/5 and needs improvement.")
        actions.append("Increase stakeholder updates and clarify expectations.")

    if row["project_type"] == "Procurement Automation" and (row["cost_variance_percent"] >= 10 or row["cpi"] < 0.95):
        actions.extend([
            "Reforecast Estimate at Completion for procurement spend.",
            "Review vendor contracts, invoices, and approval delays.",
            "Freeze non-essential procurement requests until budget variance is controlled."
        ])

    if row["project_type"] == "Cloud Migration" and (row["schedule_delay_percent"] >= 10 or row["spi"] < 0.95):
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

    if status == "Red":
        priority = "High"
        summary = (
            f"This {row['project_type']} project is classified as Red with a risk score of {row['risk_score']}. "
            f"{dimension_note} Immediate recovery governance, leadership visibility, and owner-driven corrective actions are required. "
            f"Estimated recovery timeline is {timeline}."
        )
    elif status == "Amber":
        priority = "Medium"
        summary = (
            f"This {row['project_type']} project is classified as Amber with a risk score of {row['risk_score']}. "
            f"{dimension_note} The project appears recoverable within {timeline} if corrective actions are taken now."
        )
    else:
        priority = "Low"
        summary = (
            f"This {row['project_type']} project is classified as Green with a risk score of {row['risk_score']}. "
            f"{dimension_note} Continue standard PMO monitoring and review watchlist items during the next status cycle."
        )

    return summary, priority, reasons, actions, timeline, escalation

def assess_project(row):
    duration = max(float(row.get("project_duration_days", 180)), 1)
    schedule_days = float(row["schedule_variance_days"])
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
    names = [x[0] for x in top_drivers]
    scores = [x[1] for x in top_drivers]
    levels = ["High" if s >= 15 else "Medium" if s >= 8 else "Low" for s in scores]
    colors_list = [risk_color_map[level] for level in levels]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(names, scores, color=colors_list)
    ax.set_title("Top Risk Drivers")
    ax.set_ylabel("Impact Score")
    ax.tick_params(axis="x", rotation=25)
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
        story.append(Paragraph("Top Risk Drivers Chart", styles["Heading2"]))
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
            <div class="result-metric"><div class="result-label">Risk Score</div><div class="result-value">{result_row["risk_score"]}</div></div>
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
    st.markdown("### Health Breakdown by Dimension")
    health_html = '<div class="health-grid">'
    for k, v in dimensions.items():
        health_html += f'<div class="health-tile health-{v.lower()}"><div class="health-name">{k}</div><div class="health-value">{health_icons[v]}</div></div>'
    health_html += '</div>'
    st.markdown(health_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Top Risk Drivers")
    if top_drivers:
        driver_df = pd.DataFrame(top_drivers, columns=["Driver", "Impact Score"])
        driver_df["Risk Level"] = driver_df["Impact Score"].apply(lambda x: "High" if x >= 20 else "Medium" if x >= 8 else "Low")
        table_html = '<table class="driver-table"><tr><th>Driver</th><th>Impact Score</th><th>Risk Level</th></tr>'
        for _, rr in driver_df.iterrows():
            level = rr["Risk Level"]
            table_html += f'<tr><td>{rr["Driver"]}</td><td>{rr["Impact Score"]}</td><td><span class="driver-badge driver-{level.lower()}">{level}</span></td></tr>'
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)
        fig_driver = px.bar(
    driver_df,
    x="Driver",
    y="Impact Score",
    color="Risk Level",
    title="Risk Driver Impact",
    color_discrete_map=risk_color_map,
    text="Impact Score"
)

fig_driver.update_traces(
    textposition="outside",
    marker_line_color="rgba(255,255,255,0.9)",
    marker_line_width=2,
    opacity=0.95
)

fig_driver.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0B0B0B",
    plot_bgcolor="#0B0B0B",
    font=dict(
        color="#FFFFFF",
        size=15,
        family="Inter"
    ),
    title=dict(
        text="<b>Risk Driver Impact</b>",
        font=dict(size=28, color="#FFFFFF")
    ),
    xaxis=dict(
        title="<b>Driver</b>",
        title_font=dict(size=18, color="#FFFFFF"),
        tickfont=dict(size=15, color="#FFFFFF", family="Inter"),
        showgrid=False
    ),
    yaxis=dict(
        title="<b>Impact Score</b>",
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

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Key Reasons")
    for reason in reasons:
        st.write(f"- {reason}")

    st.markdown("### Recommended Recovery Actions")
    for action in actions:
        st.write(f"- {action}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### Export & Share")
    pdf_buffer = create_pdf_report(
        result_row["project_name"], final_status, confidence, result_row["risk_score"],
        priority, timeline, escalation, summary, dimensions, top_drivers, reasons, actions, result_row
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=f"{result_row['project_name'].replace(' ', '_')}_assessment_report.pdf",
        mime="application/pdf"
    )

    reasons_text = "\n".join([f"- {r}" for r in reasons])
    actions_text = "\n".join([f"- {a}" for a in actions])
    top_drivers_text = "\n".join([f"- {driver}: {score}" for driver, score in top_drivers]) if top_drivers else "No major risk drivers detected."

    share_text = f"""
ProjectRescue AI Assessment Report

Project: {result_row['project_name']}
Project Type: {result_row['project_type']}
Health Status: {final_status}
Confidence: {confidence}%
Risk Score: {result_row['risk_score']}
Recovery Priority: {priority}
Recovery Timeline: {timeline}
Executive Escalation: {escalation}

Executive Summary:
{summary}

Top Risk Drivers:
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
            st.markdown('<div class="panel">', unsafe_allow_html=True)

            header_col, clear_col = st.columns([4, 1])
            with header_col:
                st.subheader("Portfolio Results")
                if st.session_state.portfolio_file_name:
                    st.caption(f"Analyzed file: {st.session_state.portfolio_file_name}")
            with clear_col:
                clear_portfolio = st.button("Clear Results", key="clear_portfolio_results")

            if clear_portfolio:
                st.session_state.portfolio_results = None
                st.session_state.portfolio_file_name = None
                st.rerun()

            c1, c2, c3 = st.columns(3)

            c1.metric("Total Projects", len(assessed_df))
            c2.metric("Average Risk Score", round(assessed_df["risk_score"].mean(), 2))
            c3.metric(
                "High Priority Projects",
                len(assessed_df[assessed_df["recovery_priority"] == "High"])
            )

            col1, col2 = st.columns(2)

            with col1:
                fig1 = px.pie(
                    assessed_df,
                    names="final_status",
                    title="Portfolio Health Distribution",
                    color="final_status",
                    color_discrete_map=color_map,
                    hole=0.45
                )
                st.plotly_chart(dark_plot(fig1), use_container_width=True)

            with col2:
                fig2 = px.scatter_3d(
                    assessed_df,
                    x="schedule_variance_days",
                    y="cost_variance_percent",
                    z="risk_score",
                    color="final_status",
                    hover_name="project_name",
                    title="3D Portfolio Risk View",
                    color_discrete_map=color_map
                )
                st.plotly_chart(dark_plot(fig2), use_container_width=True)

            st.subheader("Assessed Project Results")
            st.dataframe(assessed_df, use_container_width=True)

            st.download_button(
                "Download Assessed CSV",
                data=assessed_df.to_csv(index=False).encode("utf-8"),
                file_name="project_rescue_assessed_results.csv",
                mime="text/csv",
                key="download_portfolio_csv"
            )

            st.markdown("</div>", unsafe_allow_html=True)

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
