# src/utils/save_evidence.py
import os
import json
import datetime
import cv2
import ffmpeg  # ffmpeg-python wrapper; requires ffmpeg binary installed
from pathlib import Path
from typing import Tuple, Dict, Optional

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def save_crop_and_meta(out_root: str,
                       camera_id: str,
                       frame_index: int,
                       bbox: Tuple[int,int,int,int],
                       frame_bgr,                      # numpy array (BGR)
                       detection_conf: float,
                       class_name: str,
                       timestamp: Optional[str]=None,
                       clip_source_video: Optional[str]=None,
                       clip_seconds: int = 2) -> Dict:
    """
    Save cropped image, write JSON metadata, optionally extract a short clip using ffmpeg.
    Returns metadata dict.
    bbox = (x1,y1,x2,y2)
    frame_bgr is BGR OpenCV image for the frame containing detection.
    """
    if timestamp is None:
        timestamp = datetime.datetime.utcnow().isoformat()

    out_dir = os.path.join(out_root, camera_id, timestamp.replace(":", "-"))
    ensure_dir(out_dir)

    # Save crop
    x1,y1,x2,y2 = bbox
    crop = frame_bgr[y1:y2, x1:x2]
    img_name = f"crop_{frame_index}.jpg"
    img_path = os.path.join(out_dir, img_name)
    cv2.imwrite(img_path, crop)

    meta = {
        "camera_id": camera_id,
        "frame_index": int(frame_index),
        "timestamp": timestamp,
        "bbox": [int(x1), int(y1), int(x2), int(y2)],
        "detection_confidence": float(detection_conf),
        "class": class_name,
        "crop_path": img_path,
        "evidence_dir": out_dir
    }

    # Optionally extract a short clip (requires clip_source_video and ffmpeg installed)
    if clip_source_video:
        try:
            clip_name = f"clip_{frame_index}.mp4"
            clip_path = os.path.join(out_dir, clip_name)

            # Estimate middle timestamp: assume frame_index and fps known by caller OR provide start time in timestamp
            # Caller should provide accurate clip start time if precise clip is required.
            # Here we attempt to extract around timestamp if timestamp includes time and ffmpeg can parse it.
            (
                ffmpeg
                .input(clip_source_video, ss=timestamp, t=clip_seconds)
                .output(clip_path, vcodec='libx264', acodec='aac', strict='experimental', loglevel='error')
                .overwrite_output()
                .run()
            )
            meta["clip_path"] = clip_path
        except Exception as e:
            meta["clip_error"] = str(e)

    # Save JSON meta
    meta_path = os.path.join(out_dir, f"meta_{frame_index}.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    return meta
