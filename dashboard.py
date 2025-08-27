import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "runs_log.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM runs", conn)
    conn.close()
    return df

st.set_page_config(page_title="Automation Dashboard", layout="wide")
st.title("📊 Automation Monitoring Dashboard")

df = load_data()

if df.empty:
    st.warning("No logs found yet.")
else:
    # Metrics
    total_runs = len(df)
    success_count = len(df[df["status"] == "success"])
    fail_count = len(df[df["status"] == "fail"])
    total_processed = df["records_processed"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Runs", total_runs)
    col2.metric("✅ Successful", success_count)
    col3.metric("❌ Failed", fail_count)
    col4.metric("📦 Records Processed", total_processed)

    # Show table of last 10 runs
    st.subheader("Latest Runs")
    st.dataframe(df.tail(10))

    # Chart: Runs over time
    st.subheader("Runs Over Time")
    runs_per_day = df.groupby(df["timestamp"].str[:10]).size()
    st.line_chart(runs_per_day)