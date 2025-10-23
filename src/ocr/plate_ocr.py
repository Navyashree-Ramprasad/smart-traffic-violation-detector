# src/ocr/plate_ocr.py
import easyocr
import re
import numpy as np
import cv2

_reader = None

def get_reader(lang_list=None):
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(lang_list if lang_list else ['en'], gpu=False)  # set gpu=True if available
    return _reader

def preprocess_for_ocr(image_bgr):
    """Return grayscale, denoised, and resized image good for EasyOCR/Tesseract"""
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    # CLAHE to improve contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(gray)
    # Resize to improve OCR accuracy (preserve aspect)
    h, w = cl.shape
    scale = 300 / max(h, w)
    new = cv2.resize(cl, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_CUBIC)
    # slight bilateral filter
    filtered = cv2.bilateralFilter(new, 5, 75, 75)
    return filtered

def postprocess_plate(raw_text: str) -> str:
    """
    Basic normalization: uppercase, remove spaces & symbols except alphanumerics,
    common OCR corrections (O->0, I->1 when likely numeric)
    """
    if not raw_text:
        return ""
    s = raw_text.upper()
    s = re.sub(r'[^A-Z0-9]', '', s)
    # heuristic fixes: if mostly digits, convert common misreads
    digits_ratio = sum(c.isdigit() for c in s) / max(1, len(s))
    if digits_ratio > 0.5:
        s = s.replace('O', '0').replace('I', '1').replace('L','1')
    return s

def ocr_plate_from_crop(crop_bgr):
    """
    Input: crop_bgr (BGR numpy array of the plate region or whole vehicle crop)
    Returns: best_text (string), full EasyOCR result (list)
    """
    reader = get_reader()
    img = preprocess_for_ocr(crop_bgr)
    results = reader.readtext(img, detail=1)  # returns list of tuples (bbox, text, prob)
    if not results:
        return "", []
    # choose highest prob result
    best = max(results, key=lambda x: x[2])
    text = best[1]
    prob = best[2]
    text_clean = postprocess_plate(text)
    return text_clean, results
