
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

LOG_FILE = "results_log.txt"

def load_data():
    try:
        df = pd.read_csv(
            LOG_FILE,
            names=["timestamp", "result", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "platform"],
            header=None,
            skiprows=1 if "timestamp" in open(LOG_FILE).readline() else 0
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%S.%fZ", errors="coerce")
        df = df.dropna(subset=["timestamp"])
        return df
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()


def main():
    st.set_page_config(page_title="AI Fault Detection Dashboard", layout="wide")
    st.title("🔍 AI Fault Detection Dashboard")

    if not os.path.exists(LOG_FILE):
        st.warning(f"Log file '{LOG_FILE}' not found.")
        return

    refresh_rate = st.sidebar.slider("⏱️ Auto-Refresh Every (sec)", 0, 60, 0)
    show_faults_only = st.sidebar.checkbox("🚨 Show Only Faults", value=False)

    df = load_data()
    if df.empty:
        st.warning("No data available.")
        return

    if show_faults_only:
        df = df[df["result"] == "Fault Detected"]

    latest = df.iloc[-1]

    st.subheader("🧠 Latest Inference")
    st.metric("Result", latest["result"])
    st.metric("Timestamp", latest["timestamp"].strftime("%b %d, %I:%M %p UTC"))
    st.metric("Platform", f"{'🌍 GCP' if latest['platform'] == 'GCP' else '☁️ Azure'}")

    st.markdown("---")
    st.subheader("📈 Metric Trends")

    df_plot = df[["timestamp", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9"]].copy()
    df_plot = df_plot.rename(columns={
        "m1": "Duration",
        "m2": "MaxMemoryUsed",
        "m3": "Invocations",
        "m4": "Errors",
        "m5": "Throttles",
        "m6": "ConcurrentExecutions",
        "m7": "DurationP90",
        "m8": "DurationP99",
        "m9": "ProvisionedConcurrencyUtilization"
    })
    df_melt = df_plot.melt(id_vars=["timestamp"], var_name="Metric", value_name="Value")

    fig = px.line(df_melt, x="timestamp", y="Value", color="Metric", title="Metric Over Time")
    st.plotly_chart(fig, use_container_width=True)

    if refresh_rate > 0:
        time.sleep(refresh_rate)
        st.rerun()

if __name__ == "__main__":
    main()
