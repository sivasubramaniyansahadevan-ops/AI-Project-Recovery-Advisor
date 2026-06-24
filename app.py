import streamlit as st
import pandas as pd

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

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Projects",
        len(df)
    )

    col2.metric(
        "Average Risk Score",
        round(df["risk_score"].mean(),2)
    )

    col3.metric(
        "Average Delay",
        round(df["schedule_variance_days"].mean(),2)
    )

    st.dataframe(df.head())
