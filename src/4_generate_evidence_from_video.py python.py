# import os
# import random
# from datetime import datetime, timedelta
# import cv2
# import numpy as np

# # Simulate 100 "frames" from 3 cameras
# cameras = ["cam_A", "cam_B", "cam_C"]
# classes = ["car", "truck", "bus", "motorbike"]

# os.makedirs("output/images", exist_ok=True)

# records = []
# for i in range(100):
#     cam_id = random.choice(cameras)
#     frame_idx = random.randint(1, 50)
#     timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
    
#     # Generate fake bbox
#     x1, y1 = random.randint(100, 600), random.randint(100, 600)
#     w, h = random.randint(50, 200), random.randint(50, 200)
#     bbox = [x1, y1, x1+w, y1+h]
    
#     cls = random.choice(classes)
#     conf = round(random.uniform(0.6, 0.99), 2)
    
#     # Save fake image (black background with red rectangle)
#     img = np.zeros((720, 1280, 3), dtype=np.uint8)
#     cv2.rectangle(img, (x1, y1), (x1+w, y1+h), (0, 0, 255), 3)
#     cv2.putText(img, f"{cls} ({conf})", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
#     img_path = f"output/images/{cam_id}_frame_{frame_idx}.jpg"
#     cv2.imwrite(img_path, img)
    
#     records.append({
#         "id": i,
#         "camera_id": cam_id,
#         "frame_index": frame_idx,
#         "timestamp": str(timestamp),
#         "bbox": str(bbox),
#         "detection_confidence": conf,
#         "class": cls,
#         "crop_path": img_path
#     })

# # Save to CSV
# import pandas as pd
# df = pd.DataFrame(records)
# df.to_csv("output/evidence_records.csv", index=False)
# print("✅ Generated 100 simulated evidence records")


# src/4_generate_evidence_from_video.py
import cv2
import os
import random
from datetime import datetime, timedelta

video_path = "data/license-plate-recognition-for-red-light-violation/traffic_video_original.mp4"
output_dir = "output/images"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"Could not open video: {video_path}")

fps = int(cap.get(cv2.CAP_PROP_FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_step = max(1, total_frames // 50)
records = []

for i in range(0, total_frames, frame_step):
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    min_y = int(h * 0.5)
    max_y = int(h * 0.9)
    min_x = int(w * 0.2)
    max_x = int(w * 0.8)

    x1 = random.randint(min_x, max_x - 100)
    y1 = random.randint(min_y, max_y - 60)
    x2 = min(x1 + random.randint(80, 200), w - 10)
    y2 = min(y1 + random.randint(60, 150), h - 10)
    bbox = [x1, y1, x2, y2]

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
    cv2.putText(frame, "Red Light Violation", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    img_name = f"cam_redlight_01_frame_{i}.jpg"
    img_path = os.path.join(output_dir, img_name)
    cv2.imwrite(img_path, frame)

    timestamp = datetime.now() - timedelta(seconds=i // fps)
    records.append({
        "id": len(records),
        "camera_id": "cam_redlight_01",
        "frame_id": i,
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "violation_type": "Red Light Violation",
        "detection_confidence": round(random.uniform(0.85, 0.99), 2),
        "bbox": str(bbox),
        "image_path": img_path
    })

import pandas as pd
df = pd.DataFrame(records)
df.to_csv("output/evidence_records.csv", index=False)
print(f"✅ Generated {len(records)} evidence records with varied bounding boxes")
cap.release()