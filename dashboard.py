import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import time
import random

# --- 1. SETUP & REAL WEATHER ---
st.set_page_config(page_title="Antwerp Digital Twin", layout="wide")
st.title("🚢 Port of Antwerp: Digital Twin Simulator")

# Fetch Live Weather (Real Data)
try:
    url = "https://api.open-meteo.com/v1/forecast?latitude=51.2194&longitude=4.4025&current=wind_speed_10m"
    weather_data = requests.get(url).json()
    wind_speed = weather_data['current']['wind_speed_10m']
except:
    wind_speed = 25 # Fallback if API fails

# --- 2. THE RIVER PATH (Geography) ---
# These are real coordinates tracing the Scheldt River approach to Antwerp
river_path = [
    [51.45, 3.60], # North Sea Start
    [51.40, 3.80], # Vlissingen
    [51.35, 4.00], # Terneuzen
    [51.30, 4.15], # Western Scheldt
    [51.28, 4.25], # Doel
    [51.26, 4.30], # Kieldrecht Lock (Destination)
]

# --- 3. THE SIMULATION LOGIC ---
# We use Streamlit's "Session State" to remember where ships are between refreshes
if 'ships' not in st.session_state:
    st.session_state.ships = [
        {"name": "MSC Belgium", "type": "Container", "progress": 0, "color": "blue"},
        {"name": "Barge Albert", "type": "Barge",     "progress": 1, "color": "green"},
        {"name": "Tanker One",   "type": "Tanker",    "progress": 2, "color": "red"},
    ]

def move_ships(wind):
    for ship in st.session_state.ships:
        # LOGIC: How fast does this ship move?
        speed = 1 # Default speed
        
        # Rule 1: Barges stop in high wind
        if ship["type"] == "Barge" and wind > 45:
            speed = 0
            ship["status"] = "🔴 HALTED (Wind)"
        
        # Rule 2: Everyone slows down in medium wind
        elif wind > 30:
            speed = 0.5
            ship["status"] = "🟡 SLOW (Safety)"
            
        else:
            speed = 1
            ship["status"] = "🟢 MOVING"

        # Update Position along the path
        # We add 'speed' to 'progress' (index in the coordinate list)
        ship["progress"] += speed
        
        # Loop back to start if they reach the port (Infinite simulation)
        if ship["progress"] >= len(river_path) - 1:
            ship["progress"] = 0

# Button to Advance Time
if st.button("⏳ Simulate Next Hour"):
    move_ships(wind_speed)

# --- 4. THE DASHBOARD ---
# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Live Wind Speed", f"{wind_speed} km/h")
col2.metric("Active Ships", len(st.session_state.ships))

# The Map
m = folium.Map(location=[51.35, 4.00], zoom_start=10)

# Draw the River Path (Line)
folium.PolyLine(river_path, color="gray", weight=2, opacity=0.5).add_to(m)

# Draw the Ships
for ship in st.session_state.ships:
    # Find current lat/lon based on 'progress'
    # We use 'int' because progress might be 1.5 (between two points)
    current_index = int(ship["progress"])
    location = river_path[current_index]
    
    folium.Marker(
        location,
        popup=f"{ship['name']}: {ship['status']}",
        tooltip=ship["name"],
        icon=folium.Icon(color=ship['color'], icon="ship", prefix='fa')
    ).add_to(m)

st_folium(m, width=1200, height=500)

# Explanation for the Recruiter
st.markdown("""
### 🧠 How this works (The Logic)
1. **Live Data:** We fetch real-time wind speeds from *Open-Meteo*.
2. **Simulation:** We model ship traffic on the *Scheldt River* path.
3. **Safety Logic:**
    * If Wind > **45 km/h**, Barges automatically **STOP**.
    * If Wind > **30 km/h**, Heavy Traffic **SLOWS**.
""")