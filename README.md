# NASA Global Disaster Dashboard 🌍🔥

An interactive web application built with **Streamlit** to monitor and analyze global natural disasters using **NASA's EONET (Earth Observatory Natural Event Tracker) API**.

## 🚀 Key Features
- **Global Monitoring:** Access real-time and historical data for wildfires, volcanoes, and more.
- **Interactive Maps:** Built with **Folium**, featuring event popups and multiple map styles (Dark, Satellite, Standard).
- **Advanced Analytics:** Dynamic charts using **Plotly** to track event distribution and daily activity.
- **Flexible Filters:** Toggle between "Only Active" and "All Events" to get a truly global perspective.
- **Secure Integration:** Uses `.env` for safe API key management.

## 🛠️ Tech Stack
- **Python 3.12+**
- **Streamlit:** Web dashboard framework.
- **Folium:** Interactive map rendering.
- **Plotly:** Data visualization (Bar & Pie charts).
- **Pandas:** Data manipulation and analysis.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/krzysztofrasala/disaster-tracker.git
   cd disaster-tracker
   \`\`\`

2. **Set up virtual environment:**
   \`\`\`bash
   python3 -m venv .venv
   source .venv/bin/activate
   \`\`\`

3. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **API Configuration:**
   Create a \`.env\` file and add your NASA API key:
   \`\`\`text
   NASA_API_KEY=your_key_here
   \`\`\`

## 📈 Running the App
Start the dashboard locally:
\`\`\`bash
streamlit run app.py
\`\`\`

## 🔒 Security
The project is configured with a \`.gitignore\` file to ensure that sensitive files like \`.env\` and local caches are never uploaded to the public repository.
