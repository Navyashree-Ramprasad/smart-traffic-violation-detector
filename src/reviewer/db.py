# src/reviewer/db.py
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.exc import SQLAlchemyError

# -----------------------------
# Project root & DB path
# -----------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "output", "reviewer.db")

# Ensure parent folder exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# -----------------------------
# SQLAlchemy engine & metadata
# -----------------------------
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
metadata = MetaData()

# -----------------------------
# Evidence table definition
# -----------------------------
evidence_table = Table(
    "evidence",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("camera_id", String, nullable=False),
    Column("frame_index", Integer, nullable=False),
    Column("timestamp", DateTime, nullable=False),
    Column("bbox", JSON, nullable=False),
    Column("detection_confidence", Float, nullable=False),
    Column("class", String, nullable=False),
    Column("crop_path", String, nullable=True)
)

# -----------------------------
# Initialize DB
# -----------------------------
def init_db():
    """Create the database and tables if they don't exist."""
    try:
        metadata.create_all(engine)
        print(f"✅ Database initialized at: {DB_PATH}")
    except SQLAlchemyError as e:
        print(f"❌ Failed to initialize DB: {e}")
        raise e

# -----------------------------
# Insert or update evidence
# -----------------------------
def insert_or_update(evidence_data):
    """
    Insert a new evidence record into the table.
    `evidence_data` should be a dict with keys:
    camera_id, frame_index, timestamp, bbox, detection_confidence, class, crop_path
    """
    from sqlalchemy import insert
    try:
        stmt = insert(evidence_table).values(**evidence_data)
        with engine.begin() as conn:
            conn.execute(stmt)
    except SQLAlchemyError as e:
        print(f"❌ Failed to insert evidence: {e}")
        raise e

# -----------------------------
# Optional: simple fetch all
# -----------------------------
def fetch_all():
    """Fetch all records from the evidence table."""
    from sqlalchemy import select
    try:
        with engine.connect() as conn:
            result = conn.execute(select(evidence_table))
            return [dict(row) for row in result]
    except SQLAlchemyError as e:
        print(f"❌ Failed to fetch evidence: {e}")
        return []
