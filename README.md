🚦 Smart Traffic Violation Pattern Detector

A scalable big data analytics system that detects spatiotemporal patterns in traffic violations using Apache PySpark, processes synthetic traffic data, and delivers actionable insights via an **interactive Streamlit dashboard** — all built for **Windows** with real-world engineering challenges solved.

---

 🎯 Project Overview

This project simulates and analyzes traffic violation data to answer key questions for urban planners and traffic authorities:

- **When** do violations most frequently occur?  
- **Where** are high-risk "hotspot" zones?  
- **What** types of violations dominate?  
- **How** can visual evidence support enforcement?

Built entirely with **open-source tools**, it demonstrates end-to-end data engineering: from synthetic data generation → distributed processing → visual analytics.

---

🧩 Features

📊 **Analytics Engine**
- **Realistic synthetic data**: 200K+ records with rush-hour peaks (7–9 AM, 4–7 PM)
- **PySpark ETL pipeline**: Cleans, enriches, and aggregates data at scale
- **Hotspot detection**: Spatial clustering with configurable thresholds
- **Violation type analysis**: Top offenses ranked by frequency

🖼️ **Visual Evidence System**
- **Simulated detections**: Bounding boxes overlaid on real traffic video frames
- **Evidence metadata**: Camera ID, timestamp, confidence, violation type
- **Original traffic video**: Embedded directly in the dashboard

### 📈 **Interactive Dashboard**
- **4-tab interface**: Hourly Trends, Hotspots, Top Violations, Visual Evidence
- **Professional UI**: Dark theme, labeled Plotly charts, KPIs
- **Responsive design**: Works on desktop and tablet

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Core Engine** | Apache Spark 4.0.1 (via PySpark) |
| **JVM** | Java 17 (Temurin JDK) |
| **Windows Native Binaries** | `winutils.exe` + `hadoop.dll` (Hadoop 3.3.4) |
| **Language** | Python 3.9+ |
| **Data Generation** | `faker`, `pandas`, `numpy` |
| **Visualization** | Streamlit, Plotly |
| **Computer Vision** | OpenCV |
| **Environment** | `venv`, VS Code |

---

## 📁 Project Structure

```
smart-traffic-violation-detector/
├── data/
│   └── license-plate-recognition-for-red-light-violation/
│       └── traffic_video_original.mp4      # Evidence source video
├── output/
│   ├── evidence_records.csv                # Evidence metadata
│   ├── hourly_patterns/                    # Hourly violation counts
│   ├── hotspots/                           # Spatial hotspots (>1000 violations)
│   └── violation_types/                    # Top violation types
├── src/
│   ├── 1_generate_data.py                  # Realistic synthetic data generator
│   ├── 2_etl_pipeline.py                   # PySpark ETL pipeline
│   ├── 4_generate_evidence_from_video.py   # Evidence image generator
│   └── 3_dashboard.py                      # Unified Streamlit dashboard
└── venv/                                   # Python virtual environment
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Windows 10/11
- Python 3.9+
- Java 17 (Temurin JDK)

### Step 1: Clone & Setup Environment

### Step 2: Add Traffic Video
Place your downloaded video in:
```
data/license-plate-recognition-for-red-light-violation/traffic_video_original.mp4
```

### Step 3: Run the Pipeline
```powershell
# Generate synthetic data
python src/1_generate_data.py

# Run PySpark ETL
python src/2_etl_pipeline.py

# Generate visual evidence
python src/4_generate_evidence_from_video.py

# Launch dashboard
streamlit run src/3_dashboard.py
```

Open `http://localhost:8501` to explore insights!

---

## 🪟 Windows Setup Guide

PySpark on Windows requires **native Hadoop binaries**. Follow these steps:

### 1. Install Java 17
- Download [Eclipse Temurin JDK 17](https://adoptium.net/)
- Install to `C:\java\jdk-17`
- Set `JAVA_HOME = C:\java\jdk-17`

### 2. Install Hadoop Native Binaries
- Create folder: `C:\hadoop\bin`
- Download:
  - [`winutils.exe`](https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.4/bin/winutils.exe)
  - [`hadoop.dll`](https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.4/bin/hadoop.dll)
- Place both in `C:\hadoop\bin`
- Set `HADOOP_HOME = C:\hadoop`
- Add `C:\hadoop\bin` to system `PATH`

### 3. Fix PowerShell Execution Policy (if needed)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 Sample Insights

- **Peak Violations**: 5–7 PM on weekdays (rush hour)
- **Top Hotspot**: Times Square area (40.7589, -73.9851)
- **Most Common Violation**: Speeding (42%), Illegal Parking (28%)
- **Evidence**: 52+ frames with simulated red-light detections

---

## 📄 Documentation

- **Agile Tracking**: [`Agile_Template_v0.1.xls`](Agile_Template_v0.1.xls)
- **Unit Tests**: [`Unit_Test_Plan_v0.1.xlsx`](Unit_Test_Plan_v0.1.xlsx)
- **Defect Log**: [`Defect_Tracker Template_v0.1.xlsx`](Defect_Tracker Template_v0.1.xlsx)

---

## 🚀 Future Enhancements

- [ ] Export insights to PDF/Excel
- [ ] Integrate real NYC Parking Violations data (Kaggle)
- [ ] Add license plate OCR with Tesseract


