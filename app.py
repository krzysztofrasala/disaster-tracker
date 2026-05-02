import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv
import folium
from streamlit_folium import st_folium

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NASA Global Event Tracker", page_icon="🌍", layout="wide")

# Load environment variables
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

# --- DATA FETCHING LOGIC ---
@st.cache_data(ttl=3600)
def get_nasa_data(days=30, status="all"):
    """
    Fetches event data from NASA EONET API.
    Status 'all' helps to see events globally, not just currently 'open' ones.
    """
    try:
        # If status is 'all', we don't send the status parameter to get everything
        params = {"days": days, "api_key": API_KEY}
        if status == "open":
            params["status"] = "open"
            
        response = requests.get(EONET_URL, params=params, timeout=15)
        response.raise_for_status()
        events = response.json().get("events", [])
        
        processed_list = []
        for event in events:
            if event.get("geometry"):
                # Get the most recent geometry entry
                latest_geo = event["geometry"][-1]
                # Clean date for processing
                date_only = latest_geo["date"].split('T')[0]
                
                processed_list.append({
                    "title": event["title"],
                    "category": event["categories"][0]["title"],
                    "date": date_only,
                    "datetime": pd.to_datetime(date_only),
                    "latitude": float(latest_geo["coordinates"][1]),
                    "longitude": float(latest_geo["coordinates"][0]),
                    "link": event["sources"][0]["url"] if event["sources"] else ""
                })
        return pd.DataFrame(processed_list)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# --- SIDEBAR - CONTROL PANEL ---
st.sidebar.header("Global Filters")

# Status filter: 'all' shows more events worldwide
event_status = st.sidebar.radio(
    "Event Status",
    ["All Events (Global)", "Only Active (Open)"],
    help="NASA often marks US events as 'Open' longer. Choose 'All' for better global coverage."
)
status_param = "open" if "Only Active" in event_status else "all"

days_to_show = st.sidebar.slider("Time Range (Days)", 1, 90, 30)

map_theme = st.sidebar.selectbox(
    "Map Style",
    ["CartoDB Dark Matter", "OpenStreetMap", "CartoDB Positron"]
)

# --- MAIN CONTENT ---
st.title("🌍 NASA Global Natural Event Tracker")
st.markdown(f"Monitoring natural events across the globe for the last **{days_to_show}** days.")

# Fetch the data based on selection
df = get_nasa_data(days_to_show, status_param)

if not df.empty:
    # --- METRICS SECTION ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Events Found", len(df))
    m2.metric("Wildfires 🔥", len(df[df['category'] == 'Wildfires']))
    m3.metric("Volcanoes 🌋", len(df[df['category'] == 'Volcanoes']))

    st.divider()

    # --- MAP & BAR CHART SECTION ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Interactive Event Map")
        
        # Mapping tile names to Folium standards
        tiles = "openstreetmap"
        if "Dark" in map_theme: tiles = "cartodb dark_matter"
        if "Positron" in map_theme: tiles = "cartodb positron"
        
        # Initialize map
        m = folium.Map(location=[20, 0], zoom_start=2, tiles=tiles)
        
        # Add markers
        for _, row in df.iterrows():
            # Color logic: Red for fire, Blue for everything else
            color = "#FF4B4B" if row['category'] == 'Wildfires' else "#0072B2"
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=6,
                popup=f"<b>{row['title']}</b><br>Date: {row['date']}<br>Category: {row['category']}",
                color=color,
                fill=True,
                fill_opacity=0.7
            ).add_to(m)
        
        st_folium(m, width="100%", height=550, returned_objects=[])

    with col_right:
        st.subheader("Daily Activity")
        # Prepare time series data
        df_daily = df.groupby('date').size().reset_index(name='count')
        df_daily = df_daily.sort_values('date')
        
        fig_bar = px.bar(
            df_daily, x='date', y='count',
            labels={'date': 'Date', 'count': 'Events'},
            color_discrete_sequence=['#FF4B4B']
        )
        fig_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=550)
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- CATEGORY PIE CHART ---
    st.subheader("Distribution by Category")
    fig_pie = px.pie(
        df, names='category', 
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # --- DATA EXPLORER ---
    with st.expander("Explore Raw Data"):
        st.dataframe(df.sort_values('date', ascending=False), use_container_width=True)

else:
    st.warning("No data returned from NASA. Try selecting 'All Events' or a longer time range.")

# Footer
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC")