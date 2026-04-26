import streamlit as st
import pandas as pd

from modules.parser import load_dataset
from modules.classifier import classify_dataset
from modules.governance import apply_governance_to_dataset
from modules.report_generator import save_text_report
from utils.masking import (
    mask_ssn,
    mask_credit_card,
    mask_email,
    mask_medical_note
)

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Data Governance System", layout="wide")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "df" not in st.session_state:
    st.session_state.df = None

if "processed" not in st.session_state:
    st.session_state.processed = False

# -------------------------------
# MASKING FUNCTION
# -------------------------------
def apply_masking(df):
    df = df.copy()

    if "ssn" in df.columns:
        df["ssn"] = df["ssn"].apply(mask_ssn)

    if "credit_card" in df.columns:
        df["credit_card"] = df["credit_card"].apply(mask_credit_card)

    if "email" in df.columns:
        df["email"] = df["email"].apply(mask_email)

    if "medical_note" in df.columns:
        df["medical_note"] = df["medical_note"].apply(mask_medical_note)

    return df

# -------------------------------
# NAVIGATION
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload", "Processing", "Report"])

# -------------------------------
# HOME PAGE
# -------------------------------
if page == "Home":
    st.title("Intelligent Data Classification & Governance System")

    st.write("""
    This system classifies data into sensitivity levels and applies governance rules such as retention policies and security controls.

    Workflow:
    1. Upload dataset
    2. Process classification
    3. View governance report
    """)

    if st.button("Start"):
        st.switch_page("Upload")

# -------------------------------
# UPLOAD PAGE
# -------------------------------
elif page == "Upload":
    st.title("Upload Dataset")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.processed = False

        st.success("Dataset uploaded successfully!")
        st.dataframe(df.head())

# -------------------------------
# PROCESSING PAGE
# -------------------------------
elif page == "Processing":
    st.title("Processing Dataset")

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")
    else:
        if st.button("Run Classification & Governance"):
            with st.spinner("Processing..."):
                df = st.session_state.df

                df = classify_dataset(df)
                df = apply_governance_to_dataset(df)
                df = apply_masking(df)

                st.session_state.df = df
                st.session_state.processed = True

            st.success("Processing complete!")

# -------------------------------
# REPORT PAGE
# -------------------------------
elif page == "Report":
    st.title("Governance Report")

    if not st.session_state.processed:
        st.warning("Please process the dataset first.")
    else:
        df = st.session_state.df

        # SUMMARY
        st.subheader("Classification Summary")
        summary = df["Classification"].value_counts()
        st.bar_chart(summary)

        # TABLE
        st.subheader("Detailed Results")
        st.dataframe(df)

        # DOWNLOAD CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="governance_report.csv",
            mime="text/csv"
        )

        # DOWNLOAD TEXT REPORT
        report_text = "\n".join([
            "DATA GOVERNANCE REPORT",
            "",
            "SUMMARY:",
            str(summary),
            "",
            "DETAILS:",
            df.to_string()
        ])

        st.download_button(
            label="Download Text Report",
            data=report_text,
            file_name="governance_report.txt",
            mime="text/plain"
        )

        # RESET BUTTON
        if st.button("Reset System"):
            st.session_state.df = None
            st.session_state.processed = False
            st.success("System reset. Go back to Upload.")