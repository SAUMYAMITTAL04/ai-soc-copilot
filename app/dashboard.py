import streamlit as st
import sqlite3
import pandas as pd
import time
from app.database import engine



import os
import requests

# 1. Page Configuration
st.set_page_config(
    page_title="AI SOC Copilot",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Enterprise AI SOC Command Center")
# --- DIAGNOSTIC PROBE ---
db_url = os.getenv("DATABASE_URL", "sqlite")
if "postgres" in db_url:
    st.success("🔌 Connected to Neon Cloud Vault!")
else:
    st.error("⚠️ WARNING: Operating on Local SQLite Backup. Cloud key is missing.")
# ------------------------
st.markdown("Live Autonomous Threat Triage & Intelligence")

# 2. Database Connection Helper


def load_data():
    try:
        # Read from the exact same Cloud Engine that FastAPI uses
        df = pd.read_sql("SELECT * FROM security_logs", engine) 
        return df
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return pd.DataFrame()
# 3. Build the User Interface
try:
    df = load_data()
    
    # Create top-level metrics
    total_events = len(df)
    critical_threats = len(df[df['is_threat'] == True])
    safe_events = total_events - critical_threats

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logs Analyzed", total_events)
    col2.metric("Critical Threats Detected 🚨", critical_threats)
    col3.metric("Routine Events Cleared ✅", safe_events)

    st.divider()

    # Create the beautiful enterprise data table
    st.subheader("Live Threat Intelligence Feed")
    
    # We drop the 'id' column just to make the table look cleaner, 
    # and highlight the threat column!
    st.dataframe(
        df[['is_threat', 'raw_log', 'analysis']], 
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.warning("Database is empty or still initializing. Send a log through the API first!")

# 4. Auto-Refresh Button
if st.button("🔄 Refresh Data"):
    st.rerun()