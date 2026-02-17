# 🚢 Antwerp Logistics Digital Twin

### 🎯 The Problem
Barge transport in the **Port of Antwerp** is highly sensitive to weather conditions. High winds on the Scheldt River often cause unexpected delays.

### 💡 The Solution
I built a **Digital Twin Simulator** that acts as an intelligent control tower. It combines:
1.  **Live Weather Data:** Real-time wind speed API (Open-Meteo).
2.  **Geospatial Logic:** A mapped path of the Scheldt River approach.
3.  **Automated Safety Rules:** A simulation engine that automatically halts specific vessel types (Barges) when wind speeds exceed safety thresholds (>45 km/h).

### 🛠️ Tech Stack
* **Language:** Python
* **Interface:** Streamlit (Web Dashboard)
* **Geospatial:** Folium (Interactive Mapping)

### 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run dashboard.py`