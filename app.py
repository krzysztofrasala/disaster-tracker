import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NASA Disaster Tracker", page_icon="🌍", layout="wide")

load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

@st.cache_data(ttl=3600)
def get_nasa_data(days=30):
    try:
        params = {"status": "open", "days": days, "api_key": API_KEY}
        response = requests.get(EONET_URL, params=params, timeout=10)
        events = response.json().get("events", [])
        
        processed_list = []
        for event in events:
            if event.get("geometry"):
                geo = event["geometry"][-1]
                processed_list.append({
                    "title": event["title"],
                    "category": event["categories"][0]["title"],
                    "date": geo["date"],
                    "lat": float(geo["coordinates"][1]),
                    "lon": float(geo["coordinates"][0])
                })
        return pd.DataFrame(processed_list)
    except Exception as e:
        return pd.DataFrame()

# --- UI ---
st.title("🌍 NASA Disaster Tracker (Folium Edition)")

days = st.sidebar.slider("Days to look back", 1, 90, 30)
df = get_nasa_data(days)

if not df.empty:
    st.metric("Events Found", len(df))

    # --- FOLIUM MAP (PLAN B) ---
    st.subheader("Global Event Map")
    
    # Tworzymy bazową mapę
    m = folium.Map(location=[20, 0], zoom_start=2)
    
    # Dodajemy punkty do mapy
    for idx, row in df.iterrows():
        color = "red" if row['category'] == 'Wildfires' else "blue"
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            popup=f"{row['title']} ({row['category']})",
            color=color,
            fill=True
        ).add_to(m)
    
    # Wyświetlamy mapę Folium
    st_folium(m, width=1200, height=500)

    st.subheader("Data Table")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found. Please check your API Key or increase day range.")