import streamlit as st
import pandas as pd
import os
from database import engine

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
    
    if not df.empty:
        # --- TOP METRICS ---
        total_events = len(df)
        critical_threats = len(df[df['is_threat'] == True])
        safe_events = total_events - critical_threats

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Logs Analyzed", total_events)
        col2.metric("Critical Threats Detected 🚨", critical_threats)
        col3.metric("Routine Events Cleared ✅", safe_events)

        st.divider()

        # --- UPGRADE 3: VISUAL ANALYTICS & SOAR ---
        st.markdown("### 📊 Threat Intelligence Analytics")
        col_chart, col_soar = st.columns(2)
        
        with col_chart:
            st.markdown("**Log Classification Volume**")
            # Creates a live bar chart comparing Threats vs Safe logs
            st.bar_chart(df['is_threat'].value_counts())
            
        with col_soar:
            st.markdown("**🛡️ Active SOAR Countermeasures**")
            threats_only = df[df['is_threat'] == True]
            
            # Display the 3 most recent actions the AI took to defend the network
            if 'soar_action' in threats_only.columns:
                recent_actions = threats_only['soar_action'].dropna().tail(3)
                for action in recent_actions:
                    st.warning(action)
            else:
                st.info("No active countermeasures deployed yet.")

        st.divider()

        # --- THE LIVE FEED ---
        st.subheader("📡 Raw Intelligence Feed")
        
        # Show the table, dropping 'id' if it exists to keep it clean
        columns_to_show = [col for col in df.columns if col != 'id']
        st.dataframe(
            df[columns_to_show], 
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("Database is empty or still initializing. Send a log through the API first!")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")

# 4. Auto-Refresh Button
if st.button("🔄 Refresh Data"):
    st.rerun()