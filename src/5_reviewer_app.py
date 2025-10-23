# # src/5_reviewer_app.py
# import streamlit as st
# import pandas as pd
# import cv2
# import numpy as np
# from PIL import Image

# st.set_page_config(page_title="🚦 Evidence Reviewer", layout="wide")
# st.title("📸 Traffic Violation Evidence Reviewer")

# # Load records
# df = pd.read_csv("output/evidence_records.csv")

# # Filter by camera
# cam_filter = st.sidebar.multiselect("Camera ID", df['camera_id'].unique(), default=df['camera_id'].unique())
# df_filtered = df[df['camera_id'].isin(cam_filter)]

# st.subheader(f"Showing {len(df_filtered)} records")

# for _, row in df_filtered.iterrows():
#     col1, col2 = st.columns([1, 3])
#     with col1:
#         st.image(row['crop_path'], caption=f"{row['class']} @ {row['camera_id']}")
#     with col2:
#         st.write(f"**Timestamp**: {row['timestamp']}")
#         st.write(f"**Confidence**: {row['detection_confidence']:.2f}")
#         st.write(f"**Bounding Box**: {row['bbox']}")
#         st.markdown("---")

# src/5_reviewer_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="🚦 Evidence Reviewer", layout="wide")
st.title("📸 Traffic Violation Evidence Reviewer")

# Load records
df = pd.read_csv("output/evidence_records.csv")

# Filter by camera
cam_filter = st.sidebar.multiselect("Camera ID", df['camera_id'].unique(), default=df['camera_id'].unique())
df_filtered = df[df['camera_id'].isin(cam_filter)]

st.subheader(f"Showing {len(df_filtered)} records")

for _, row in df_filtered.iterrows():
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(row['image_path'], caption=f"{row['violation_type']} @ {row['camera_id']}")
    with col2:
        st.write(f"**Timestamp**: {row['timestamp']}")
        st.write(f"**Confidence**: {row['detection_confidence']:.2f}")
        st.write(f"**Bounding Box**: {row['bbox']}")
        st.markdown("---")