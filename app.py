import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(page_title="ProjectRescue AI", layout="wide")

st.title("🚀 ProjectRescue AI")
st.subheader("ML-Powered Project Health & Recovery Advisor")

color_map = {
    "Green": "#2ECC71",
    "Amber": "#F39C12",
    "Red": "#E74C3C"
}

features = [
    "cost_variance_percent",
    "schedule_variance_percent",
    "schedule_variance_days",
    "spi",
    "cpi",
    "completed_tasks_percent",
    "open_risks_count",
    "open_issues_count",
    "scope_changes_count",
    "resource_utilization_percent",
    "stakeholder_sentiment_score",
    "risk_score"
]

@st.cache_resource
def load_model():
    return joblib.load("project_rescue_model.pkl")

model = load_model()


def calculate_risk_score(
    cost_variance_percent,
    schedule_variance_percent,
    schedule_variance_days,
    spi,
    cpi,
    completed_tasks_percent,
    open_risks_count,
    open_issues_count,
    scope_changes_count,
    resource_utilization_percent,
    stakeholder_sentiment_score
):
    score = 0
    score += max(cost_variance_percent, 0) * 1.2
    score += max(schedule_variance_percent, 0) * 1.3
    score += open_risks_count * 2.5
    score += open_issues_count * 2.0
    score += scope_changes_count * 3.0
    score += max(resource_utilization_percent - 80, 0) * 1.1
    score += (5 - stakeholder_sentiment_score) * 8

    if spi < 0.85:
        score += 15
    elif spi < 0.95:
        score += 8

    if cpi < 0.85:
        score += 15
    elif cpi < 0.95:
        score += 8

    if completed_tasks_percent > 75 and score > 40:
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

    sorted_drivers = sorted(drivers.items(), key=lambda x: x[1], reverse=True)
    return [(name, round(score, 2)) for name, score in sorted_drivers if score > 0][:5]


def sanity_check_status(status, row):
    severe_drivers = []

    if row["cost_variance_percent"] >= 20:
        severe_drivers.append("Cost variance is severe")
    if row["schedule_delay_percent"] >= 25:
        severe_drivers.append("Schedule delay is severe compared to project duration")
    if row["spi"] < 0.85:
        severe_drivers.append("SPI is critically low")
    if row["cpi"] < 0.85:
        severe_drivers.append("CPI is critically low")
    if row["open_risks_count"] >= 10:
        severe_drivers.append("Open risk count is high")
    if row["open_issues_count"] >= 10:
        severe_drivers.append("Open issue count is high")
    if row["stakeholder_sentiment_score"] < 2.5:
        severe_drivers.append("Stakeholder sentiment is low")

    if status == "Red" and len(severe_drivers) == 0:
        return "Amber", severe_drivers

    return status, severe_drivers


def override_status(prediction, risk_score, spi, cpi, delay_percent, open_risks, open_issues, sentiment):
    if risk_score >= 90 or spi < 0.75 or cpi < 0.75 or delay_percent >= 25:
        return "Red"

    if (
        risk_score >= 45
        or spi < 0.92
        or cpi < 0.92
        or delay_percent >= 12
        or open_risks >= 7
        or open_issues >= 7
        or sentiment < 3
    ):
        if prediction == "Green":
            return "Amber"

    if (
        risk_score <= 25
        and spi >= 0.95
        and cpi >= 0.95
        and sentiment >= 3.8
        and open_risks <= 3
        and open_issues <= 3
    ):
        return "Green"

    return prediction


def recovery_timeline(status, row):
    if status == "Green":
        return "No recovery required"

    if status == "Amber":
        if row["cost_variance_percent"] >= 10 or row["cpi"] < 0.95:
            return "4–6 weeks"
        if row["schedule_delay_percent"] >= 10 or row["spi"] < 0.95:
            return "3–5 weeks"
        return "2–4 weeks"

    if status == "Red":
        if row["risk_score"] >= 90 or row["schedule_delay_percent"] >= 25:
            return "8–12 weeks"
        return "6–8 weeks"


def escalation_required(status, row):
    if status == "Red":
        return "Yes"
    if row["cost_variance_percent"] >= 20 or row["open_risks_count"] >= 10 or row["stakeholder_sentiment_score"] < 2.5:
        return "Yes"
    if status == "Amber":
        return "Monitor"
    return "No"


def generate_recovery_plan(row, status):
    reasons = []
    actions = []

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
        reasons.append(f"Stakeholder sentiment is low at {row['stakeholder_sentiment_score']}/5, indicating confidence or alignment issues.")
        actions.append("Conduct stakeholder alignment meeting and reset communication cadence.")
    elif row["stakeholder_sentiment_score"] < 3.5:
        reasons.append(f"Stakeholder sentiment is neutral at {row['stakeholder_sentiment_score']}/5 and needs improvement.")
        actions.append("Increase stakeholder updates and clarify expectations.")

    if row["project_type"] == "Procurement Automation" and (row["cost_variance_percent"] >= 10 or row["cpi"] < 0.95):
        actions.append("Reforecast Estimate at Completion for procurement spend.")
        actions.append("Review vendor contracts, invoices, and approval delays.")
        actions.append("Freeze non-essential procurement requests until budget variance is controlled.")

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
        summary = (
            f"This {row['project_type']} project is classified as Red due to a risk score of {row['risk_score']}. "
            f"The project needs immediate recovery action, leadership visibility, and a structured recovery plan. "
            f"Estimated recovery timeline is {timeline}."
        )
    elif status == "Amber":
        priority = "Medium"
        summary = (
            f"This {row['project_type']} project is classified as Amber due to emerging delivery concerns. "
            f"Primary drivers include cost, schedule, risk, stakeholder, or execution indicators that require management attention. "
            f"The project appears recoverable within {timeline} if corrective actions are taken now."
        )
    else:
        priority = "Low"
        summary = (
            f"This {row['project_type']} project is classified as Green. "
            f"Cost, schedule, risk, issue, resource, and stakeholder indicators are currently within acceptable PMO tolerance. "
            f"No recovery plan is required beyond standard monitoring."
        )

    return summary, priority, reasons, actions, timeline, escalation


uploaded_file = st.file_uploader("Upload Project CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("File Uploaded Successfully")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Projects", len(df))
    col2.metric("Average Risk Score", round(df["risk_score"].mean(), 2))
    col3.metric("Average Delay Days", round(df["schedule_variance_days"].mean(), 2))

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        fig1 = px.pie(df, names="status", title="Project Health Distribution", color="status", color_discrete_map=color_map)
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        fig2 = px.histogram(df, x="risk_score", color="status", title="Risk Score Distribution", color_discrete_map=color_map)
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.scatter(
        df,
        x="schedule_variance_days",
        y="cost_variance_percent",
        color="status",
        hover_data=["project_name", "project_type"],
        title="Schedule Delay vs Cost Variance",
        color_discrete_map=color_map
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.header("📝 Manual Project Assessment")

    col_a, col_b = st.columns(2)

    with col_a:
        project_name = st.text_input("Project Name", "Cloud Migration Program")
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

    if st.button("🔍 Analyze Project"):
        schedule_variance_percent = round((schedule_variance_days / project_duration_days) * 100, 2)

        risk_score = calculate_risk_score(
            cost_variance_percent,
            schedule_variance_percent,
            schedule_variance_days,
            spi,
            cpi,
            completed_tasks_percent,
            open_risks_count,
            open_issues_count,
            scope_changes_count,
            resource_utilization_percent,
            stakeholder_sentiment_score
        )

        input_df = pd.DataFrame([{
            "cost_variance_percent": cost_variance_percent,
            "schedule_variance_percent": schedule_variance_percent,
            "schedule_variance_days": schedule_variance_days,
            "spi": spi,
            "cpi": cpi,
            "completed_tasks_percent": completed_tasks_percent,
            "open_risks_count": open_risks_count,
            "open_issues_count": open_issues_count,
            "scope_changes_count": scope_changes_count,
            "resource_utilization_percent": resource_utilization_percent,
            "stakeholder_sentiment_score": stakeholder_sentiment_score,
            "risk_score": risk_score
        }])

        prediction = model.predict(input_df[features])[0]
        probabilities = model.predict_proba(input_df[features])[0]
        confidence = round(max(probabilities) * 100, 2)

        final_status = override_status(
            prediction,
            risk_score,
            spi,
            cpi,
            schedule_variance_percent,
            open_risks_count,
            open_issues_count,
            stakeholder_sentiment_score
        )

        result_row = {
            "project_name": project_name,
            "project_type": project_type,
            "project_duration_days": project_duration_days,
            "completed_tasks_percent": completed_tasks_percent,
            "cost_variance_percent": cost_variance_percent,
            "schedule_variance_days": schedule_variance_days,
            "schedule_delay_percent": schedule_variance_percent,
            "spi": spi,
            "cpi": cpi,
            "open_risks_count": open_risks_count,
            "open_issues_count": open_issues_count,
            "scope_changes_count": scope_changes_count,
            "resource_utilization_percent": resource_utilization_percent,
            "stakeholder_sentiment_score": stakeholder_sentiment_score,
            "risk_score": risk_score
        }

        final_status, severe_drivers = sanity_check_status(final_status, result_row)
        summary, priority, reasons, actions, timeline, escalation = generate_recovery_plan(result_row, final_status)
        dimensions = health_breakdown(result_row)
        top_drivers = get_top_drivers(result_row)

        st.subheader("Assessment Result")

        if final_status == "Green":
            st.success("Predicted Project Health: 🟢 Green")
        elif final_status == "Amber":
            st.warning("Predicted Project Health: 🟠 Amber")
        else:
            st.error("Predicted Project Health: 🔴 Red")

        col_x, col_y, col_z, col_w, col_v = st.columns(5)
        col_x.metric("ML Confidence", f"{confidence}%")
        col_y.metric("Risk Score", risk_score)
        col_z.metric("Recovery Priority", priority)
        col_w.metric("Recovery Timeline", timeline)
        col_v.metric("Executive Escalation", escalation)

        st.markdown("### Executive Summary")
        st.write(summary)

        st.markdown("### Health Breakdown by Dimension")
        health_df = pd.DataFrame([
            {"Dimension": key, "Health": value} for key, value in dimensions.items()
        ])
        st.dataframe(health_df, use_container_width=True)

        st.markdown("### Top Risk Drivers / Feature Importance")
        if top_drivers:
            driver_df = pd.DataFrame(top_drivers, columns=["Driver", "Impact Score"])
            st.dataframe(driver_df, use_container_width=True)

            fig_driver = px.bar(
                driver_df,
                x="Driver",
                y="Impact Score",
                title="Top Risk Drivers",
            )
            st.plotly_chart(fig_driver, use_container_width=True)
        else:
            st.write("No major risk drivers detected.")

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

        st.markdown("### Entered Project Metrics")
        output_df = pd.DataFrame([{
            **result_row,
            "ml_prediction": prediction,
            "final_status": final_status,
            "ml_confidence_percent": confidence,
            "recovery_priority": priority,
            "recovery_timeline": timeline,
            "executive_escalation": escalation
        }])
        st.dataframe(output_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Project Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

else:
    st.info("Please upload the project CSV file to view dashboard and use manual assessment.")
