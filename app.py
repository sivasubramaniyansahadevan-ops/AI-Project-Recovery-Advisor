import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="ProjectRescue AI",
    layout="wide"
)

st.title("🚀 ProjectRescue AI")
st.subheader("AI-Powered Project Recovery Advisor")

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
            title="Project Health Distribution"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        fig2 = px.histogram(
            df,
            x="risk_score",
            color="status",
            title="Risk Score Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    fig3 = px.scatter(
        df,
        x="schedule_variance_days",
        y="cost_variance_percent",
        color="status",
        hover_data=["project_name", "project_type"],
        title="Schedule Delay vs Cost Variance"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    st.subheader("Project Data Preview")
    st.dataframe(df.head(20))

else:
    st.info("Please upload the project CSV file to view dashboard.")
