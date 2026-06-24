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

st.set_page_config(page_title="ProjectRescue AI", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #050505 0%, #0B0B0B 45%, #111111 100%);
    color: #F5F5F5;
}

.block-container {
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
    max-width: 1400px;
}

h1, h2, h3 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

p, label, span {
    color: #E5E5E5 !important;
}

.hero-card {
    background: linear-gradient(135deg, #141414, #090909);
    border: 1px solid #2A2A2A;
    border-radius: 22px;
    padding: 32px;
    margin-bottom: 28px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.45);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 8px;
}

.hero-title span {
    color: #E50914 !important;
}

.hero-subtitle {
    font-size: 18px;
    color: #BDBDBD !important;
    margin-bottom: 14px;
}

.hero-brand {
    font-size: 14px;
    color: #8E8E8E !important;
}

[data-testid="stTabs"] button {
    background-color: #141414 !important;
    border-radius: 12px 12px 0 0 !important;
    color: #E5E5E5 !important;
    font-weight: 600 !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FFFFFF !important;
    border-bottom: 3px solid #E50914 !important;
}

.stNumberInput input, .stTextInput input {
    background-color: #1C1C1C !important;
    color: #FFFFFF !important;
    border: 1px solid #333333 !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #1C1C1C !important;
    color: #FFFFFF !important;
}

.result-card {
    padding: 28px;
    border-radius: 24px;
    margin-top: 28px;
    margin-bottom: 28px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.45);
}

.green-card {
    background: linear-gradient(135deg, #082E1D, #0F6B3A);
    border: 1px solid #2ECC71;
}

.amber-card {
    background: linear-gradient(135deg, #3A2600, #9A6500);
    border: 1px solid #F39C12;
}

.red-card {
    background: linear-gradient(135deg, #320000, #8B0000);
    border: 1px solid #E50914;
}

.result-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 18px;
    margin-top: 22px;
}

.result-metric {
    background: rgba(0,0,0,0.28);
    padding: 18px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.12);
}

.result-metric-label {
    font-size: 13px;
    color: #BDBDBD !important;
    margin-bottom: 8px;
}

.result-metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF !important;
}

.stButton button, .stDownloadButton button {
    background: linear-gradient(135deg, #E50914, #B00610) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.2rem !important;
    font-weight: 700 !important;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: linear-gradient(135deg, #FF1E2D, #E50914) !important;
}

.brand-footer {
    color: #777777;
    font-size: 13px;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 1px solid #222222;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">ProjectRescue <span>AI</span></div>
    <div class="hero-subtitle">Project Health & Recovery Advisor</div>
    <div class="hero-brand">Powered by ThinkLab.pm · Built by Sivasubramaniyan Sahadevan</div>
</div>
""", unsafe_allow_html=True)

color_map = {"Green": "#2ECC71", "Amber": "#F39C12", "Red": "#E74C3C"}
risk_color_map = {"High": "#E74C3C", "Medium": "#F39C12", "Low": "#2ECC71"}
health_icons = {"Green": "🟢 Green", "Amber": "🟠 Amber", "Red": "🔴 Red"}

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
        font_color="#F5F5F5"
    )
    return fig


def calculate_risk_score(cost, schedule_pct, delay_days, spi, cpi, completed, risks, issues, scope, utilization, sentiment):
    score = 0
    score += max(cost, 0) * 1.2
    score += max(schedule_pct, 0) * 1.3
    score += risks * 2.5
    score += issues * 2.0
    score += scope * 3.0
    score += max(utilization - 80, 0) * 1.1
    score += (5 - sentiment) * 8

    if spi < 0.85:
        score += 15
    elif spi < 0.95:
        score += 8

    if cpi < 0.85:
        score += 15
    elif cpi < 0.95:
        score += 8

    if completed > 75 and score > 40:
        score += 8

    return round(score, 2)


def classify_dimension(value, green_limit, amber_limit, reverse=False):
    if reverse:
        if value >= green_limit:
            return "Green"
        elif value >= amber_limit:
            return "Amber"
        return "Red"
    else:
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
        "Cost Variance": row["cost_variance_percent"] * 1.2,
        "Schedule Delay %": row["schedule_delay_percent"] * 1.3,
        "Open Risks": row["open_risks_count"] * 2.5,
        "Open Issues": row["open_issues_count"] * 2.0,
        "Scope Changes": row["scope_changes_count"] * 3.0,
        "Resource Overload": max(row["resource_utilization_percent"] - 80, 0) * 1.1,
        "Stakeholder Concern": (5 - row["stakeholder_sentiment_score"]) * 8,
        "SPI Impact": 15 if row["spi"] < 0.85 else 8 if row["spi"] < 0.95 else 0,
        "CPI Impact": 15 if row["cpi"] < 0.85 else 8 if row["cpi"] < 0.95 else 0
    }
    return [(k, round(v, 2)) for k, v in sorted(drivers.items(), key=lambda x: x[1], reverse=True) if v > 0][:5]


def override_status(prediction, risk_score, spi, cpi, delay_percent, risks, issues, sentiment):
    if risk_score >= 90 or spi < 0.75 or cpi < 0.75 or delay_percent >= 25:
        return "Red"

    if risk_score >= 45 or spi < 0.92 or cpi < 0.92 or delay_percent >= 12 or risks >= 7 or issues >= 7 or sentiment < 3:
        if prediction == "Green":
            return "Amber"

    if risk_score <= 25 and spi >= 0.95 and cpi >= 0.95 and sentiment >= 3.8 and risks <= 3 and issues <= 3:
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

    if status == "Red" and len(severe) == 0:
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
    elif row["spi"] < 0.95:
        reasons.append(f"SPI is {row['spi']}, showing schedule slippage against plan.")
        actions.append("Review sprint velocity or milestone delivery performance.")

    if row["cost_variance_percent"] >= 20:
        reasons.append(f"Cost variance is high at {row['cost_variance_percent']}%, which may require budget escalation.")
        actions.append("Perform budget impact analysis and stop non-essential spending.")
    elif row["cost_variance_percent"] >= 10:
        reasons.append(f"Cost variance is moderate at {row['cost_variance_percent']}% and should be reviewed.")
        actions.append("Review vendor/resource costs and validate remaining forecast.")

    if row["cpi"] < 0.85:
        reasons.append(f"CPI is {row['cpi']}, indicating poor cost efficiency.")
        actions.append("Review cost burn rate and identify low-value activities.")
    elif row["cpi"] < 0.95:
        reasons.append(f"CPI is {row['cpi']}, showing cost performance concern.")
        actions.append("Tighten budget tracking and review cost-to-complete.")

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

    if status == "Red":
        priority = "High"
        summary = f"This {row['project_type']} project is classified as Red due to a risk score of {row['risk_score']}. Immediate recovery action, leadership visibility, and structured recovery governance are required. Estimated recovery timeline is {timeline}."
    elif status == "Amber":
        priority = "Medium"
        summary = f"This {row['project_type']} project is classified as Amber. The project appears recoverable within {timeline}, but cost, schedule, risk, stakeholder, or execution indicators require management attention."
    else:
        priority = "Low"
        summary = f"This {row['project_type']} project is classified as Green. Cost, schedule, risk, issue, resource, and stakeholder indicators are within acceptable PMO tolerance."

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

    input_df = pd.DataFrame([{
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


def chart_to_buffer(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=160)
    plt.close(fig)
    buf.seek(0)
    return buf


def create_health_chart(dimensions):
    labels = list(dimensions.keys())
    values = [1] * len(labels)
    colors_list = [color_map[dimensions[label]] for label in labels]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, values, color=colors_list)
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
        <h2 style="margin-bottom: 8px;">Assessment Result</h2>
        <h1 style="margin-top: 0;">{health_icons[final_status]}</h1>
        <div class="result-grid">
            <div class="result-metric"><div class="result-metric-label">Confidence</div><div class="result-metric-value">{confidence}%</div></div>
            <div class="result-metric"><div class="result-metric-label">Risk Score</div><div class="result-metric-value">{result_row["risk_score"]}</div></div>
            <div class="result-metric"><div class="result-metric-label">Recovery Priority</div><div class="result-metric-value">{priority}</div></div>
            <div class="result-metric"><div class="result-metric-label">Recovery Timeline</div><div class="result-metric-value">{timeline}</div></div>
            <div class="result-metric"><div class="result-metric-label">Executive Escalation</div><div class="result-metric-value">{escalation}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Executive Summary")
    st.write(summary)

    st.markdown("### Health Breakdown by Dimension")
    health_df = pd.DataFrame([{"Dimension": k, "Health": health_icons[v]} for k, v in dimensions.items()])
    st.dataframe(health_df, use_container_width=True)

    st.markdown("### Top Risk Drivers / Feature Importance")
    if top_drivers:
        driver_df = pd.DataFrame(top_drivers, columns=["Driver", "Impact Score"])
        driver_df["Risk Level"] = driver_df["Impact Score"].apply(lambda x: "High" if x >= 15 else "Medium" if x >= 8 else "Low")
        st.dataframe(driver_df, use_container_width=True)

        fig_driver = px.bar(
            driver_df,
            x="Driver",
            y="Impact Score",
            color="Risk Level",
            title="Top Risk Drivers",
            color_discrete_map=risk_color_map,
            text="Impact Score"
        )
        fig_driver.update_traces(textposition="outside", marker_line_color="white", marker_line_width=1.5)
        st.plotly_chart(dark_plot(fig_driver), use_container_width=True)

    if severe_drivers:
        st.markdown("### Severe Drivers")
        for driver in severe_drivers:
            st.write(f"- {driver}")

    st.markdown("### Key Reasons")
    for reason in reasons:
        st.write(f"- {reason}")

    st.markdown("### Recommended Recovery Actions")
    for action in actions:
        st.write(f"- {action}")

    st.markdown("### Export Assessment Report")
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

    share_text = f"""
ProjectRescue AI Report
Project: {result_row['project_name']}
Status: {final_status}
Risk Score: {result_row['risk_score']}
Recovery Priority: {priority}
Timeline: {timeline}
Generated by ProjectRescue AI | ThinkLab.pm
"""
    encoded_text = urllib.parse.quote(share_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su=ProjectRescue AI Report - {result_row['project_name']}&body={encoded_text}"

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("Share Summary on WhatsApp", whatsapp_url)
    with c2:
        st.link_button("Share Summary via Gmail", gmail_url)

    st.markdown("### Entered Project Metrics")
    output_df = pd.DataFrame([{**result_row, "model_prediction": prediction, "final_status": final_status, "confidence_percent": confidence}])
    st.dataframe(output_df, use_container_width=True)


tab_csv, tab_manual = st.tabs([
    "Portfolio Assessment",
    "Single Project Assessment"
])

with tab_csv:
    uploaded_file = st.file_uploader("Upload Project CSV", type=["csv"], key="csv_upload")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully")

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
                st.warning(f"Skipped one row due to missing or invalid data: {e}")

        assessed_df = pd.DataFrame(assessed_rows)

        if not assessed_df.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Projects", len(assessed_df))
            col2.metric("Average Risk Score", round(assessed_df["risk_score"].mean(), 2))
            col3.metric("High Priority Projects", len(assessed_df[assessed_df["recovery_priority"] == "High"]))

            c1, c2 = st.columns(2)

            with c1:
                fig1 = px.pie(
                    assessed_df,
                    names="final_status",
                    title="Predicted Project Health Distribution",
                    color="final_status",
                    color_discrete_map=color_map
                )
                st.plotly_chart(dark_plot(fig1), use_container_width=True)

            with c2:
                fig2 = px.histogram(
                    assessed_df,
                    x="risk_score",
                    color="final_status",
                    title="Risk Score Distribution",
                    color_discrete_map=color_map
                )
                st.plotly_chart(dark_plot(fig2), use_container_width=True)

            fig3 = px.scatter(
                assessed_df,
                x="schedule_variance_days",
                y="cost_variance_percent",
                color="final_status",
                hover_data=["project_name", "project_type"],
                title="Schedule Delay vs Cost Variance",
                color_discrete_map=color_map
            )
            st.plotly_chart(dark_plot(fig3), use_container_width=True)

            st.subheader("Assessed Project Results")
            st.dataframe(assessed_df, use_container_width=True)

            csv_export = assessed_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Assessed CSV",
                data=csv_export,
                file_name="project_rescue_assessed_results.csv",
                mime="text/csv"
            )
    else:
        st.info("Upload a CSV file to assess multiple projects at once.")


with tab_manual:
    st.header("Single Project Assessment")

    col_a, col_b = st.columns(2)

    with col_a:
        project_name = st.text_input("Project Name", "Cloud Migration Program")
        project_type = st.selectbox(
            "Project Type",
            [
                "Cloud Migration", "ERP Implementation", "CRM Modernization",
                "Data Warehouse Migration", "Cybersecurity Program", "ITSM Transformation",
                "Procurement Automation", "License Optimization", "Infrastructure Refresh",
                "Mobile App Development", "AI Adoption Program"
            ]
        )
        project_duration_days = st.number_input("Planned Project Duration Days", min_value=1, value=180)
        completed_tasks_percent = st.slider("Completed Tasks %", 0, 100, 65)
        cost_variance_percent = st.number_input("Cost Variance %", value=8.0)
        schedule_variance_days = st.number_input("Schedule Delay Days", value=10)
        spi = st.number_input("SPI", value=0.95, step=0.01)
        cpi = st.number_input("CPI", value=0.96, step=0.01)

    with col_b:
        open_risks_count = st.number_input("Open Risks", min_value=0, value=4)
        open_issues_count = st.number_input("Open Issues", min_value=0, value=3)
        scope_changes_count = st.number_input("Scope Changes", min_value=0, value=2)
        resource_utilization_percent = st.slider("Resource Utilization %", 0, 100, 85)
        stakeholder_sentiment_score = st.slider("Stakeholder Sentiment", 1.0, 5.0, 3.5, step=0.1)

    if st.button("Analyze Project"):
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

        result = assess_project(manual_row)
        render_result(*result)

st.markdown("""
<div class="brand-footer">
    ProjectRescue AI | ThinkLab.pm | Built by Sivasubramaniyan Sahadevan PMP®, CAPM®, CSM®, CSPO®
</div>
""", unsafe_allow_html=True)
