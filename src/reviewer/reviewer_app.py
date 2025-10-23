# src/reviewer/reviewer_app.py
import streamlit as st
from src.reviewer.db import init_db, fetch_pending, update_review
import os
from PIL import Image
import io

st.set_page_config(page_title="Violation Reviewer", layout="wide")

init_db()

st.title("📋 Violation Reviewer")

cols = st.columns([1, 3])
with cols[0]:
    limit = st.number_input("Load pending", min_value=1, max_value=500, value=25)
    refresh = st.button("Refresh")
    st.markdown("**Actions:** Accept / Reject / Edit plate text and add notes.")

if refresh:
    st.experimental_rerun()

pending = fetch_pending(limit=int(limit))

if not pending:
    st.info("No pending violations. Ingest evidence or produce violations to review.")
    st.stop()

# Display items one-by-one
idx = st.number_input("Select index", min_value=0, max_value=max(0, len(pending)-1), value=0)
item = pending[idx]

left, right = st.columns([1,2])

with left:
    st.subheader("Evidence")
    if item.get("crop_path") and os.path.exists(item["crop_path"]):
        img = Image.open(item["crop_path"])
        st.image(img, caption=f"Crop: {os.path.basename(item['crop_path'])}", use_column_width=True)
    else:
        st.warning("Crop image missing: " + str(item.get("crop_path")))

    if item.get("clip_path") and os.path.exists(item["clip_path"]):
        st.video(item["clip_path"])
    else:
        st.info("No clip found")

with right:
    st.subheader("Metadata & Review")
    st.write("**ID:**", item["id"])
    st.write("**Camera:**", item.get("camera_id"))
    st.write("**Timestamp:**", item.get("timestamp"))
    st.write("**Detection confidence:**", item.get("detection_confidence"))
    st.write("**BBox:**", item.get("bbox"))
    current_plate = item.get("plate_text") or ""
    new_plate = st.text_input("Plate text (edit)", value=current_plate)
    notes = st.text_area("Reviewer notes")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Accept"):
            update_review(item["id"], "accepted", notes=notes, plate_text=new_plate)
            st.success("Accepted")
    with col_b:
        if st.button("Reject"):
            update_review(item["id"], "rejected", notes=notes, plate_text=new_plate)
            st.error("Rejected")

st.markdown("---")
st.markdown("**Pending list (preview):**")
for i, it in enumerate(pending[:10]):
    st.write(f"{i}. {it['id']} — {it.get('camera_id')} — {it.get('timestamp')} — {it.get('plate_text')}")
