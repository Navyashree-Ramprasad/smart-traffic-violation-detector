# src/1_generate_data.py
from faker import Faker
import random
import pandas as pd
import os

fake = Faker()
violation_types = ["Speeding", "Red Light", "Illegal Parking", "No Seatbelt", "DUI"]
locations = [
    (40.7128, -74.0060, "NYC Downtown"),
    (40.7589, -73.9851, "Times Square"),
    (40.7505, -73.9934, "Empire State"),
    (40.7061, -74.0088, "Wall Street"),
    (40.7812, -73.9665, "Central Park South"),
]

data = []
for _ in range(100000):
    lat, lon, name = random.choice(locations)
    ts = fake.date_time_between(start_date="-2y", end_date="now")
    data.append({
        "violation_id": fake.uuid4(),
        "timestamp": ts,
        "latitude": round(lat + random.uniform(-0.005, 0.005), 6),
        "longitude": round(lon + random.uniform(-0.005, 0.005), 6),
        "location_name": name,
        "violation_type": random.choice(violation_types),
        "fine_amount": round(random.uniform(50, 500), 2)
    })

df = pd.DataFrame(data)

# --- Save safely ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_dir = os.path.join(project_root, "data")
os.makedirs(data_dir, exist_ok=True)
output_path = os.path.join(data_dir, "traffic_violations.csv")
df.to_csv(output_path, index=False)
print(f"✅ Simulated data saved to {output_path}")