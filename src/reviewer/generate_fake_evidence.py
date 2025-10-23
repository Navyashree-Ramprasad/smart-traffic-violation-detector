import os
import json
from datetime import datetime, timedelta
import random

# Project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
evidence_root = os.path.join(project_root, "output", "evidence")
os.makedirs(evidence_root, exist_ok=True)

# Parameters
cameras = ["cam_A", "cam_B", "cam_C"]
violation_classes = ["car", "motorbike", "truck", "bus"]
num_files_per_camera = 10

start_time = datetime.now() - timedelta(days=30)

# Generate fake data
for cam in cameras:
    cam_folder = os.path.join(evidence_root, cam)
    os.makedirs(cam_folder, exist_ok=True)

    for i in range(1, num_files_per_camera + 1):
        ts = start_time + timedelta(minutes=random.randint(0, 43200))  # 30 days in minutes
        meta = {
            "camera_id": cam,
            "frame_index": i,
            "timestamp": ts.isoformat(),
            "bbox": [
                random.randint(0, 500),
                random.randint(0, 500),
                random.randint(500, 1000),
                random.randint(500, 1000),
            ],
            "detection_confidence": round(random.uniform(0.5, 1.0), 2),
            "class": random.choice(violation_classes),
            "crop_path": ""  # Leave blank or add a dummy path
        }

        file_path = os.path.join(cam_folder, f"meta_{i}.json")
        with open(file_path, "w") as f:
            json.dump(meta, f, indent=2)

print(f"✅ Fake evidence generated under: {evidence_root}")
