# src/reviewer/ingest_evidence.py
import os
import json
from datetime import datetime
from src.reviewer.db import init_db, insert_or_update

def ingest(folder_root=None):
    # Determine project root
    if folder_root is None:
        # Go two levels up from src/reviewer/ to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    else:
        project_root = folder_root
    print(f"[ingest_evidence] Project root fixed at: {project_root}")

    # Look for evidence meta files
    evidence_folder = os.path.join(project_root, "output", "evidence")
    print(f"[ingest_evidence] Looking for evidence meta files under: {evidence_folder}")

    if not os.path.exists(evidence_folder):
        print(f"[ingest_evidence] Folder not found: {evidence_folder}")
        return

    # Initialize DB
    init_db()

    # Walk through evidence folder
    meta_files = []
    for root, dirs, files in os.walk(evidence_folder):
        for file in files:
            if file.endswith(".json"):
                meta_files.append(os.path.join(root, file))

    if not meta_files:
        print(f"[ingest_evidence] No meta files found.")
        return

    # Ingest each meta file
    processed = 0
    errors = 0
    for meta_file in meta_files:
        try:
            with open(meta_file, 'r') as f:
                meta = json.load(f)

            # Convert timestamp string to datetime object for SQLite
            ts_str = meta.get("timestamp")
            if ts_str:
                meta["timestamp"] = datetime.fromisoformat(ts_str)

            # Insert into DB
            insert_or_update(meta)
            processed += 1
        except Exception as e:
            print(f"❌ Failed to ingest {meta_file} -> {e}")
            errors += 1

    print(f"[ingest_evidence] Done. Files processed: {processed}, errors: {errors}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest evidence JSON files into DB")
    parser.add_argument(
        "--folder", "-f", type=str, help="Optional root folder for the project"
    )
    args = parser.parse_args()

    ingest(folder_root=args.folder)
