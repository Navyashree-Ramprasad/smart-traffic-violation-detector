# src/2_etl_pipeline.py
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_path = os.path.join(project_root, "data", "traffic_violations.csv")
output_hourly = os.path.join(project_root, "output", "hourly_patterns")
output_hotspots = os.path.join(project_root, "output", "hotspots")
output_violation_types = os.path.join(project_root, "output", "violation_types")

if not os.path.exists(data_path):
    raise FileNotFoundError(f"Input data not found at: {data_path}")

spark = SparkSession.builder \
    .appName("TrafficViolationETL") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

df = spark.read.csv(data_path, header=True, inferSchema=True)

df_clean = df.dropDuplicates().na.drop(subset=["timestamp", "latitude", "longitude"])
df_clean = df_clean.withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))

df_clean = df_clean \
    .withColumn("hour", hour(col("timestamp"))) \
    .withColumn("day_of_week", dayofweek(col("timestamp"))) \
    .withColumn("lat_bin", round(col("latitude"), 2)) \
    .withColumn("lon_bin", round(col("longitude"), 2))

hourly = df_clean.groupBy("hour").count().orderBy("hour")

# 🔥 CHANGE: Increase hotspot threshold to reduce density
# Hotspots with reduced density
hotspots = df_clean.groupBy("lat_bin", "lon_bin") \
    .agg(
        count("*").alias("violation_count"),
        first("location_name").alias("area")
    ) \
    .filter(col("violation_count") > 1000) \
    .orderBy(desc("violation_count"))
violation_types = df_clean.groupBy("violation_type").count().orderBy(desc("count"))

hourly.coalesce(1).write.mode("overwrite").csv(output_hourly, header=True)
hotspots.coalesce(1).write.mode("overwrite").csv(output_hotspots, header=True)
violation_types.coalesce(1).write.mode("overwrite").csv(output_violation_types, header=True)

print("✅ ETL complete!")
spark.stop()