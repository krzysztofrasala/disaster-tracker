# NASA EONET Disaster Tracker 🌍🔥

A specialized Python tool designed to monitor and analyze real-time natural events such as wildfires, volcanic eruptions, and icebergs using NASA's **Earth Observatory Natural Event Tracker (EONET)** API.

## 📌 Project Overview
This project serves as a practical application for data acquisition and environmental monitoring. It fetches active event data from NASA, processes geographic coordinates, and generates structured analytical reports. It's built with a focus on clean code, modularity, and professional data handling.

## 🚀 Features
- **Real-time Monitoring:** Accesses NASA's live database of global natural disasters.
- **Data Processing:** Uses Pandas to clean and structure complex JSON responses into readable DataFrames.
- **Automated Reporting:** Generates timestamped CSV reports for further analysis in tools like Excel or Tableau.
- **Global Statistics:** Provides a summary of event categories (e.g., how many wildfires are active vs. volcanoes).
- **Secure Integration:** Fully compatible with .env files to protect sensitive API credentials.

## 🛠️ Technologies
- **Python 3.12+**
- **Requests:** For API communication.
- **Pandas:** For high-level data manipulation and CSV generation.
- **Python-dotenv:** For secure environment variable management.

## ⚙️ Setup & Installation

1. **Clone the repository:**
   git clone https://github.com/krzysztofrasala/disaster-tracker.git
   cd disaster-tracker

2. **Create and activate a virtual environment:**
   python3 -m venv .venv
   source .venv/bin/activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Set up your API Key:**
   - Create a .env file in the root directory.
   - Add your NASA API Key (get it from api.nasa.gov):
     NASA_API_KEY=your_actual_api_key_here

## 📈 Usage
Run the main script to fetch the latest 30 days of global events and generate a report:
python main.py

The script will output a summary to the console and save a detailed CSV file in the data/ directory.

## 🔒 Security Note
This project is configured with a .gitignore file to ensure that:
- Your .env file (API Keys) is **never** uploaded to GitHub.
- Local data reports and virtual environments are kept out of the repository.

## 📄 License
This project is open-source and available for educational purposes.
