# src/reviewer/save_and_index_example.py
from src.utils.save_evidence import save_crop_and_meta
from src.ocr.plate_ocr import ocr_plate_from_crop
from src.reviewer.db import init_db, insert_or_update

def example_flow():
    # Suppose you have a detection frame (numpy BGR), camera_id, bbox, etc.
    # This is a pseudo-example. Replace frame_bgr and bbox with real values from your detector.
    import cv2
    frame_bgr = cv2.imread("examples/sample_frame.jpg")  # placeholder
    bbox = (100,100,400,200)
    meta = save_crop_and_meta(out_root="output/evidence", camera_id="cam_A", frame_index=1,
                              bbox=bbox, frame_bgr=frame_bgr, detection_conf=0.87, class_name="car")
    # OCR crop and update meta
    crop = cv2.imread(meta["crop_path"])
    plate_text, _ = ocr_plate_from_crop(crop)
    meta["plate_text"] = plate_text
    # Insert into DB
    init_db()
    insert_or_update(meta)
    print("Saved and indexed:", meta)

if __name__ == "__main__":
    example_flow()
