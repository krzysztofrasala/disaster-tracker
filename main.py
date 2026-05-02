import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load configuration
load_dotenv()
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
EONET_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

def fetch_natural_events(status="open", days=20):
    """
    Fetches natural events from NASA EONET API.
    Args:
        status: 'open' or 'closed' events.
        days: How many days back to look.
    """
    params = {
        "status": status,
        "days": days,
        "api_key": API_KEY
    }
    
    print(f"LOG: Fetching active natural events from the last {days} days...")
    response = requests.get(EONET_URL, params=params)
    response.raise_for_status()
    return response.json().get("events", [])

def process_events(events):
    """
    Processes raw JSON events into a structured list of dictionaries.
    """
    processed_data = []
    
    for event in events:
        # Extract basic info
        event_id = event.get("id")
        title = event.get("title")
        category = event.get("categories")[0].get("title") if event.get("categories") else "Unknown"
        
        # Extract the latest coordinates (geometries)
        latest_geo = event.get("geometry")[-1]
        date = latest_geo.get("date")
        coordinates = latest_geo.get("coordinates") # [longitude, latitude]
        
        processed_data.append({
            "id": event_id,
            "title": title,
            "category": category,
            "date": date,
            "longitude": coordinates[0],
            "latitude": coordinates[1],
            "link": event.get("sources")[0].get("url") if event.get("sources") else "N/A"
        })
        
    return processed_data

def save_to_report(data):
    """
    Saves the processed data to a CSV file for analytical purposes.
    """
    if not data:
        print("LOG: No events to save.")
        return

    df = pd.DataFrame(data)
    filename = f"data/disaster_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    
    # Ensure directory exists
    os.makedirs("data", exist_ok=True)
    
    df.to_csv(filename, index=False)
    print(f"✅ SUCCESS: Report saved to {filename}")
    return df

if __name__ == "__main__":
    try:
        # 1. Get raw events
        raw_events = fetch_natural_events(days=30)
        
        # 2. Process to clean format
        clean_data = process_events(raw_events)
        
        # 3. Save and analyze with Pandas
        df = save_to_report(clean_data)
        
        if df is not None:
            print("\n--- Current Global Situation Summary ---")
            print(df['category'].value_counts())
            
            # Show top 5 most recent events
            print("\n--- Latest 5 Events ---")
            print(df[['title', 'category', 'date']].head())
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")