# src/3_dashboard.py
import streamlit as st
import pandas as pd
import glob
import os

# Helper: Load Spark CSV output (which is in part-*.csv files)
def load_spark_output(folder):
    files = glob.glob(os.path.join(folder, "part-*.csv"))
    if not files:
        return pd.DataFrame()
    return pd.read_csv(files[0])

# Get project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hourly_path = os.path.join(project_root, "output", "hourly_patterns")
hotspots_path = os.path.join(project_root, "output", "hotspots")

# Load data
hourly_df = load_spark_output(hourly_path)
hotspots_df = load_spark_output(hotspots_path)

# Dashboard
st.set_page_config(page_title="🚦 Traffic Violation Dashboard", layout="wide")
st.title("🚦 Smart Traffic Violation Pattern Detector")

# Hourly Chart
if not hourly_df.empty:
    st.subheader("Violations by Hour of Day")
    st.bar_chart(hourly_df.set_index("hour")["count"])
else:
    st.warning("No hourly data found. Run ETL pipeline first.")

# Hotspot Map
if not hotspots_df.empty:
    st.subheader("Violation Hotspots")
    # Clean coordinates
    hotspots_df["lat_bin"] = pd.to_numeric(hotspots_df["lat_bin"], errors="coerce")
    hotspots_df["lon_bin"] = pd.to_numeric(hotspots_df["lon_bin"], errors="coerce")
    hotspots_df = hotspots_df.dropna(subset=["lat_bin", "lon_bin"])
    
    if not hotspots_df.empty:
        st.map(hotspots_df.rename(columns={"lat_bin": "lat", "lon_bin": "lon"}))
    else:
        st.warning("No valid hotspot coordinates.")
else:
    st.warning("No hotspot data found. Run ETL pipeline first.")