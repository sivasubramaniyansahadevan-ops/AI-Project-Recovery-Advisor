import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ProjectRescue AI",
    layout="wide"
)

st.title("🚀 ProjectRescue AI")
st.subheader("AI-Powered Project Recovery Advisor")

color_map = {
    "Green": "#2ECC71",
    "Amber": "#F39C12",
    "Red": "#E74C3C"
}

uploaded_file = st.file_uploader(
    "Upload Project CSV",
    type=["csv"]
)

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
        fig1 = px.pie(
            df,
            names="status",
            title="Project Health Distribution",
            color="status",
            color_discrete_map=color_map
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        fig2 = px.histogram(
            df,
            x="risk_score",
            color="status",
            title="Risk Score Distribution",
            color_discrete_map=color_map
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

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
        cost_variance_percent = st.number_input("Cost Variance %", value=10.0)
        schedule_variance_days = st.number_input("Schedule Delay Days", value=15)
        spi = st.number_input("SPI", value=0.90, step=0.01)
        cpi = st.number_input("CPI", value=0.92, step=0.01)
        completed_tasks_percent = st.slider("Completed Tasks %", 0, 100, 65)

    with col_b:
        open_risks_count = st.number_input("Open Risks", value=5)
        open_issues_count = st.number_input("Open Issues", value=4)
        scope_changes_count = st.number_input("Scope Changes", value=2)
        resource_utilization_percent = st.slider("Resource Utilization %", 0, 100, 85)
        stakeholder_sentiment_score = st.slider(
            "Stakeholder Sentiment",
            1.0,
            5.0,
            3.5,
            step=0.1
        )

    if st.button("🔍 Analyze Project"):

        score = 0
        reasons = []

        if schedule_variance_days > 25:
            score += 3
            reasons.append("Schedule delay is very high.")
        elif schedule_variance_days > 10:
            score += 1
            reasons.append("Schedule delay needs attention.")

        if cost_variance_percent > 15:
            score += 3
            reasons.append("Cost variance is high.")
        elif cost_variance_percent > 5:
            score += 1
            reasons.append("Cost variance is moderate.")

        if spi < 0.85:
            score += 3
            reasons.append("SPI is low, meaning the project is progressing slower than planned.")
        elif spi < 0.95:
            score += 1
            reasons.append("SPI shows slight schedule performance concern.")

        if cpi < 0.85:
            score += 3
            reasons.append("CPI is low, meaning cost efficiency is poor.")
        elif cpi < 0.95:
            score += 1
            reasons.append("CPI shows moderate cost performance concern.")

        if open_risks_count > 8:
            score += 2
            reasons.append("There are many open risks.")
        elif open_risks_count > 4:
            score += 1
            reasons.append("Open risks should be monitored.")

        if open_issues_count > 8:
            score += 2
            reasons.append("There are many open issues blocking delivery.")
        elif open_issues_count > 4:
            score += 1
            reasons.append("Open issues need tracking.")

        if scope_changes_count > 5:
            score += 2
            reasons.append("Too many scope changes may affect delivery stability.")
        elif scope_changes_count > 2:
            score += 1
            reasons.append("Scope changes should be controlled.")

        if resource_utilization_percent > 92:
            score += 2
            reasons.append("Resource utilization is very high; team may be overloaded.")
        elif resource_utilization_percent > 85:
            score += 1
            reasons.append("Resource utilization is slightly high.")

        if stakeholder_sentiment_score < 2.5:
            score += 2
            reasons.append("Stakeholder sentiment is low.")
        elif stakeholder_sentiment_score < 3.5:
            score += 1
            reasons.append("Stakeholder sentiment needs improvement.")

        if score <= 4:
    status = "Green"
    status_display = "🟢 Green"
    box = st.success

    reasons = [
        "Project KPIs are within acceptable thresholds.",
        f"Cost performance is healthy with CPI at {cpi}.",
        f"Schedule performance is healthy with SPI at {spi}.",
        "Open risks and issues are low.",
        f"Stakeholder sentiment is positive at {stakeholder_sentiment_score}/5."
    ]

    if schedule_variance_days > 10:
        reasons.append(
            f"Observation: Schedule delay of {schedule_variance_days} days should be monitored, but it is not currently creating major delivery risk."
        )

    recommendation = """
The project appears stable. Continue monitoring schedule, cost, risks, and stakeholder communication.
Review milestone dependencies during weekly status meetings and maintain the current delivery rhythm.
"""
        elif score <= 9:
            status = "Amber"
            status_display = "🟠 Amber"
            box = st.warning
            recommendation = """
The project needs attention. Review the main risk areas, tighten change control, and conduct a project checkpoint meeting.
Focus on reducing delays, clearing issues, and improving stakeholder alignment.
"""
        else:
            status = "Red"
            status_display = "🔴 Red"
            box = st.error
            recommendation = """
The project is at high risk. Immediate recovery action is needed.
Escalate to leadership, rebaseline the schedule, review budget impact, freeze non-critical scope changes, and assign owners for major risks and issues.
"""

        st.subheader("Assessment Result")
        box(f"Predicted Project Health: {status_display}")

        st.markdown("### Key Reasons")
        if reasons:
            for reason in reasons:
                st.write(f"- {reason}")
        else:
            st.write("- No major risk indicators detected.")

        st.markdown("### Recovery Recommendation")
        st.write(recommendation)

        st.markdown("### Entered Project Metrics")
        manual_df = pd.DataFrame([{
            "project_name": project_name,
            "status": status,
            "score": score,
            "cost_variance_percent": cost_variance_percent,
            "schedule_variance_days": schedule_variance_days,
            "spi": spi,
            "cpi": cpi,
            "completed_tasks_percent": completed_tasks_percent,
            "open_risks_count": open_risks_count,
            "open_issues_count": open_issues_count,
            "scope_changes_count": scope_changes_count,
            "resource_utilization_percent": resource_utilization_percent,
            "stakeholder_sentiment_score": stakeholder_sentiment_score
        }])

        st.dataframe(manual_df)

    st.markdown("---")

    st.subheader("Project Data Preview")
    st.dataframe(df.head(20))

else:
    st.info("Please upload the project CSV file to view dashboard and use manual assessment.")
