# # src/1_generate_data.py
# from faker import Faker
# import random
# import pandas as pd
# import os

# fake = Faker()
# violation_types = ["Speeding", "Red Light", "Illegal Parking", "No Seatbelt", "DUI"]
# locations = [
#     (40.7128, -74.0060, "NYC Downtown"),
#     (40.7589, -73.9851, "Times Square"),
#     (40.7505, -73.9934, "Empire State"),
#     (40.7061, -74.0088, "Wall Street"),
#     (40.7812, -73.9665, "Central Park South"),
# ]

# data = []
# for _ in range(100000):
#     lat, lon, name = random.choice(locations)
#     ts = fake.date_time_between(start_date="-2y", end_date="now")
#     data.append({
#         "violation_id": fake.uuid4(),
#         "timestamp": ts,
#         "latitude": round(lat + random.uniform(-0.005, 0.005), 6),
#         "longitude": round(lon + random.uniform(-0.005, 0.005), 6),
#         "location_name": name,
#         "violation_type": random.choice(violation_types),
#         "fine_amount": round(random.uniform(50, 500), 2)
#     })

# df = pd.DataFrame(data)

# # --- Save safely ---
# script_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(script_dir)
# data_dir = os.path.join(project_root, "data")
# os.makedirs(data_dir, exist_ok=True)
# output_path = os.path.join(data_dir, "traffic_violations.csv")
# df.to_csv(output_path, index=False)
# print(f"✅ Simulated data saved to {output_path}")


# # src/1_generate_data.py
# import os
# import pandas as pd
# from faker import Faker
# import random
# import numpy as np

# fake = Faker()
# violation_types = ["Speeding", "Red Light", "Illegal Parking", "No Seatbelt", "DUI"]
# locations = [
#     (40.7128, -74.0060, "NYC Downtown"),
#     (40.7589, -73.9851, "Times Square"),
#     (40.7505, -73.9934, "Empire State"),
#     (40.7061, -74.0088, "Wall Street"),
#     (40.7812, -73.9665, "Central Park South"),
# ]

# # Realistic hour weights (peak at 7-9 AM and 4-7 PM)
# hour_weights = [
#     0.5,  # 0 AM
#     0.4,  # 1 AM
#     0.3,  # 2 AM
#     0.3,  # 3 AM
#     0.4,  # 4 AM
#     0.7,  # 5 AM
#     1.0,  # 6 AM
#     2.5,  # 7 AM ← Peak 1
#     3.0,  # 8 AM ← Peak 1
#     2.8,  # 9 AM
#     2.0,  # 10 AM
#     2.2,  # 11 AM
#     2.5,  # 12 PM
#     2.3,  # 1 PM
#     2.6,  # 2 PM
#     3.0,  # 3 PM
#     4.0,  # 4 PM ← Peak 2
#     4.5,  # 5 PM ← Peak 2
#     4.0,  # 6 PM
#     3.5,  # 7 PM
#     2.8,  # 8 PM
#     2.0,  # 9 PM
#     1.5,  # 10 PM
#     1.0,  # 11 PM
# ]

# data = []
# for _ in range(100000):
#     lat, lon, name = random.choice(locations)
    
#     # Generate timestamp with realistic hour distribution
#     hour = np.random.choice(range(24), p=np.array(hour_weights) / sum(hour_weights))
#     date = fake.date_time_between(start_date="-2y", end_date="now")
#     ts = date.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))
    
#     # Simulate location noise
#     lat_noisy = round(lat + random.uniform(-0.005, 0.005), 6)
#     lon_noisy = round(lon + random.uniform(-0.005, 0.005), 6)
    
#     data.append({
#         "violation_id": fake.uuid4(),
#         "timestamp": ts,
#         "latitude": lat_noisy,
#         "longitude": lon_noisy,
#         "location_name": name,
#         "violation_type": random.choice(violation_types),
#         "fine_amount": round(random.uniform(50, 500), 2)
#     })

# df = pd.DataFrame(data)

# # --- Save safely ---
# script_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(script_dir)
# data_dir = os.path.join(project_root, "data")
# os.makedirs(data_dir, exist_ok=True)
# output_path = os.path.join(data_dir, "traffic_violations.csv")
# df.to_csv(output_path, index=False)
# print(f"✅ Simulated data saved to {output_path}")

# src/1_generate_data.py
import os
import pandas as pd
from faker import Faker
import random
import numpy as np

fake = Faker()
locations = [
    (40.7128, -74.0060, "NYC Downtown", ["Illegal Parking", "No Seatbelt"]),
    (40.7589, -73.9851, "Times Square", ["Speeding", "Red Light"]),
    (40.7505, -73.9934, "Empire State", ["Speeding", "Red Light"]),
    (40.7061, -74.0088, "Wall Street", ["Illegal Parking", "DUI"]),
    (40.7812, -73.9665, "Central Park South", ["Speeding", "Red Light"]),
]

hour_weights = [
    0.5, 0.4, 0.3, 0.3, 0.4, 0.7, 1.0, 2.5, 3.0, 2.8, 2.0, 2.2,
    2.5, 2.3, 2.6, 3.0, 4.0, 4.5, 4.0, 3.5, 2.8, 2.0, 1.5, 1.0
]
hour_probs = np.array(hour_weights) / sum(hour_weights)

data = []
num_records = 200000

for _ in range(num_records):
    lat, lon, name, common_violations = random.choice(locations)
    
    # 80% weekdays
    if random.random() < 0.8:
        date = fake.date_time_between(start_date="-2y", end_date="now")
        while date.weekday() >= 5:
            date = fake.date_time_between(start_date="-2y", end_date="now")
    else:
        date = fake.date_time_between(start_date="-2y", end_date="now")
        while date.weekday() < 5:
            date = fake.date_time_between(start_date="-2y", end_date="now")
    
    hour = np.random.choice(range(24), p=hour_probs)
    ts = date.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))
    
    lat_noisy = round(lat + random.uniform(-0.005, 0.005), 6)
    lon_noisy = round(lon + random.uniform(-0.005, 0.005), 6)
    
    violation_type = random.choice(common_violations) if random.random() < 0.7 else random.choice(
        ["Speeding", "Red Light", "Illegal Parking", "No Seatbelt", "DUI"]
    )
    
    data.append({
        "violation_id": fake.uuid4(),
        "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
        "latitude": lat_noisy,
        "longitude": lon_noisy,
        "location_name": name,
        "violation_type": violation_type,
        "fine_amount": round(random.uniform(50, 500), 2)
    })

df = pd.DataFrame(data)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_dir = os.path.join(project_root, "data")
os.makedirs(data_dir, exist_ok=True)
output_path = os.path.join(data_dir, "traffic_violations.csv")
df.to_csv(output_path, index=False)
print(f"✅ Generated {len(df)} realistic synthetic records → {output_path}")