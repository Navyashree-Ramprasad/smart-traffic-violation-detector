# src/2_etl_pipeline.py
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql import functions as F

# Get project root (works no matter where script is run from)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_path = os.path.join(project_root, "data", "traffic_violations.csv")
output_hourly = os.path.join(project_root, "output", "hourly_patterns")
output_hotspots = os.path.join(project_root, "output", "hotspots")

# Ensure output directories can be written (Spark handles folder creation, but good to validate input)
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Input data not found at: {data_path}")

spark = SparkSession.builder \
    .appName("TrafficViolationETL") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Load data
df = spark.read.csv(data_path, header=True, inferSchema=True)

# Clean & transform
df_clean = df.dropDuplicates().na.drop(subset=["timestamp", "latitude", "longitude"])
df_clean = df_clean.withColumn("timestamp", to_timestamp(col("timestamp")))

df_clean = df_clean \
    .withColumn("hour", hour(col("timestamp"))) \
    .withColumn("day_of_week", dayofweek(col("timestamp"))) \
    .withColumn("lat_bin", round(col("latitude"), 2)) \
    .withColumn("lon_bin", round(col("longitude"), 2))

# Time patterns
hourly = df_clean.groupBy("hour").count().orderBy("hour")
daily = df_clean.groupBy("day_of_week").count().orderBy("day_of_week")

# Hotspots
hotspots = df_clean.groupBy("lat_bin", "lon_bin") \
    .agg(
        count("*").alias("violation_count"),
        first("location_name").alias("area")
    ) \
    .filter(col("violation_count") > 50) \
    .orderBy(desc("violation_count"))

# Save results
hourly.coalesce(1).write.mode("overwrite").csv(output_hourly, header=True)
hotspots.coalesce(1).write.mode("overwrite").csv(output_hotspots, header=True)

print(f"✅ ETL complete!")
print(f"   Hourly patterns saved to: {output_hourly}")
print(f"   Hotspots saved to: {output_hotspots}")

spark.stop()