# src/3_dashboard.py
import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

# ----------------------------
# Custom CSS for Modern Look
# ----------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0e0e0e;
        color: white;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .stSidebar {
        background-color: #1a1a1a;
    }
    h1, h2, h3 {
        color: #00D4FF;
    }
    .stDataFrame {
        background-color: #1e1e1e;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Helper: Load Spark CSV Output
# ----------------------------
def load_spark_csv(folder):
    files = glob.glob(os.path.join(folder, "part-*.csv"))
    return pd.read_csv(files[0]) if files else pd.DataFrame()

# ----------------------------
# Paths
# ----------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hourly_path = os.path.join(project_root, "output", "hourly_patterns")
hotspots_path = os.path.join(project_root, "output", "hotspots")
violation_types_path = os.path.join(project_root, "output", "violation_types")
evidence_path = os.path.join(project_root, "output", "evidence_records.csv")

# ----------------------------
# Load Data
# ----------------------------
hourly_df = load_spark_csv(hourly_path)
hotspots_df = load_spark_csv(hotspots_path)
violation_df = load_spark_csv(violation_types_path)

evidence_df = None
if os.path.exists(evidence_path):
    evidence_df = pd.read_csv(evidence_path)

# ----------------------------
# Dashboard UI
# ----------------------------
st.set_page_config(page_title="🚦 Smart Traffic Violation Dashboard", layout="wide")
st.title("🚦 Smart Traffic Violation Pattern Detector")

# ----------------------------
# KPIs at Top
# ----------------------------
total_violations = hourly_df['count'].sum() if not hourly_df.empty else 0
peak_hour = hourly_df.loc[hourly_df['count'].idxmax(), 'hour'] if not hourly_df.empty else "N/A"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Violations", f"{total_violations:,}")
with col2:
    st.metric("Peak Hour", peak_hour)
with col3:
    st.metric("Hotspot Zones", len(hotspots_df) if not hotspots_df.empty else 0)

# ----------------------------
# Tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Hourly Trends",
    "Hotspots",
    "Top Violations",
    "Visual Evidence"
])

# ----------------------------
# Tab 1: Hourly Trends
# ----------------------------
with tab1:
    if not hourly_df.empty:
        st.subheader("Violations by Hour of Day")
        fig = px.bar(
            hourly_df,
            x="hour",
            y="count",
            labels={"hour": "Hour of Day", "count": "Number of Violations"},
            height=400
        )
        fig.update_xaxes(tickmode='linear')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hourly data. Run ETL pipeline.")

# ----------------------------
# Tab 2: Hotspots
# ----------------------------
with tab2:
    if not hotspots_df.empty:
        st.subheader("Violation Hotspots")
        hotspots_df["lat_bin"] = pd.to_numeric(hotspots_df["lat_bin"], errors="coerce")
        hotspots_df["lon_bin"] = pd.to_numeric(hotspots_df["lon_bin"], errors="coerce")
        hotspots_df = hotspots_df.dropna(subset=["lat_bin", "lon_bin"])
        if not hotspots_df.empty:
            fig_map = px.scatter_mapbox(
                hotspots_df,
                lat="lat_bin",
                lon="lon_bin",
                size="violation_count",
                color="violation_count",
                hover_name="area",
                zoom=10,
                height=500,
                mapbox_style="carto-darkmatter"
            )
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("No valid coordinates.")
    else:
        st.warning("No hotspot data. Run ETL pipeline.")

# ----------------------------
# Tab 3: Top Violations
# ----------------------------
with tab3:
    if not violation_df.empty:
        st.subheader("Top Violation Types")
        st.dataframe(violation_df, use_container_width=True)
        
        fig_donut = px.pie(
            violation_df,
            names="violation_type",
            values="count",
            title="Violation Type Distribution",
            hole=0.4
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.warning("No violation type data. Run ETL pipeline.")

# ----------------------------
# Tab 4: Visual Evidence + Video at Bottom
# ----------------------------
with tab4:
    if evidence_df is not None and not evidence_df.empty:
        st.subheader("Traffic Violation Evidence Reviewer")
        
        cam_options = evidence_df['camera_id'].unique().tolist()
        cam_filter = st.sidebar.multiselect("Filter by Camera", options=cam_options, default=cam_options)
        filtered_df = evidence_df[evidence_df['camera_id'].isin(cam_filter)]
        
        st.write(f"Showing {len(filtered_df)} records")
        
        for _, row in filtered_df.iterrows():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row['image_path'], caption=f"{row['violation_type']} @ {row['camera_id']}")
            with col2:
                st.write(f"**Timestamp**: {row['timestamp']}")
                st.write(f"**Confidence**: {row['detection_confidence']:.2f}")
                st.write(f"**Bounding Box**: {row['bbox']}")
                st.markdown("---")
        
        # 🎥 VIDEO AT BOTTOM OF THIS TAB
        st.subheader("Original Traffic Video")
        video_path = os.path.join(
            project_root,
            "data",
            "license-plate-recognition-for-red-light-violation",
            "traffic_video_original.mp4"
        )
        if os.path.exists(video_path):
            with open(video_path, "rb") as f:
                st.video(f.read())
        else:
            st.warning("Video not found. Ensure `traffic_video_original.mp4` is in the correct folder.")
    else:
        st.warning("No visual evidence. Run `src/4_generate_evidence_from_video.py`.")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("Smart Traffic Violation Pattern Detector • Powered by PySpark + Streamlit")