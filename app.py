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

from utils.pdf_report import create_pdf_report


# Page Configuration
st.set_page_config(page_title="Data Governance System", layout="wide")


if "df" not in st.session_state:
    st.session_state.df = None

if "processed" not in st.session_state:
    st.session_state.processed = False

if "page" not in st.session_state:
    st.session_state.page = "Home"


# Masking
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



# Navigation
st.sidebar.title("Navigation")
pages = ["Home", "Upload", "Processing", "Report"]

selected = st.sidebar.radio(
    "Go to",
    pages,
    index=pages.index(st.session_state.page)
)

st.session_state.page = selected
page = st.session_state.page



# HOME PAGE
if page == "Home":
    st.title(" Data Classification & Governance System")

    st.write("""
    This system classifies data into sensitivity levels and applies governance rules such as retention policies and security controls.

    Workflow:
    1. Upload dataset
    2. Process classification
    3. View governance report
    """)

    st.info("""
    Security Model:
            
    • Data is processed in-memory (session-based)
            
    • No permanent storage of uploaded datasets
            
    • Data is cleared on reset or session end
    """)

    if st.button("Start"):
        st.session_state.page = "Upload"
        st.rerun()

# UPLOAD PAGE
elif page == "Upload":
    st.title("Upload Dataset")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.processed = False

        st.success("Dataset uploaded successfully!")
        st.dataframe(df.head())

        st.session_state.page = "Processing"
        st.rerun()


# PROCESSING PAGE
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

            st.session_state.page = "Report"
            st.rerun()


# REPORT PAGE
elif page == "Report":
    st.title("Governance Report")

    if not st.session_state.processed:
        st.warning("Please process the dataset first.")
    else:
        df = st.session_state.df

        # SUMMARY
        import matplotlib.pyplot as plt

        st.subheader("Classification Summary")

        summary = df["Classification"].value_counts()

        fig, ax = plt.subplots(figsize=(4, 3)) 

        ax.bar(summary.index.astype(str), summary.values)

        ax.set_xlabel("Classification")
        ax.set_ylabel("Count")
        ax.set_title("Data Classification Distribution")

        plt.xticks(rotation=30, ha='right')

        plt.tight_layout()
        plt.savefig("chart.png", bbox_inches='tight', dpi=150)


        st.pyplot(fig, use_container_width=False)


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
            "===================================",
            "DATA GOVERNANCE REPORT",
            "===================================",
            "",
            "CLASSIFICATION SUMMARY:",
            str(summary),
            "",
            "-----------------------------------",
            "DETAILED RECORDS",
            "-----------------------------------",
            df[["id", "description", "Classification", "Retention", "Action"]].to_string(index=False),
            "",
            "==================================="
        ])

        st.download_button(
            label="Download Text Report",
            data=report_text,
            file_name="governance_report.txt",
            mime="text/plain"
        )

        # GENERATE PDF REPORT

        if st.button("Generate PDF Report"):
            summary = df["Classification"].value_counts()
            create_pdf_report(df, summary)
            
            with open("governance_report.pdf", "rb") as f:
                pdf_bytes = f.read()

                st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="governance_report.pdf",
                mime="application/pdf"
            )


        # RESET BUTTON
        if "confirm_reset" not in st.session_state:
            st.session_state.confirm_reset = False

        if st.button("Reset System", key="reset_btn"):
            st.session_state.confirm_reset = True

        if st.session_state.confirm_reset:
            st.warning("WARNING: You will lose your data. Download report first.")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Yes, Reset"):
                    st.session_state.df = None
                    st.session_state.processed = False
                    st.session_state.confirm_reset = False
                    st.success("System reset.")
                    st.session_state.page = "Home" 
                    st.rerun()

            with col2:
                if st.button("Cancel"):
                    st.session_state.confirm_reset = False
        

        st.markdown("""
        <div style="padding:15px; background-color: #87CEEB; color: black; border-radius:8px; border-left:5px solid #3366cc;">
        <b>Security & Data Handling</b><br><br>
        The system uses a session-based processing model. Uploaded datasets are stored temporarily in memory and are not persisted to disk.
        Data is automatically cleared when the session ends or when the user resets the system.
        </div>
        """, unsafe_allow_html=True)