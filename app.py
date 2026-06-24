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

    st.dataframe(df.head())

    st.write("Total Projects:", len(df))
