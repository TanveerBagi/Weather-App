# Weather-App

A responsive weather forecast web app built using **Streamlit**, integrated with **OpenWeatherMap API** and **SQLite** for full CRUD (Create, Read, Update, Delete) operations and weather history storage.
The app allows users to search real-time weather conditions for any location worldwide and view detailed information like temperature, humidity, wind speed/direction, and sky conditions. It also includes a built-in system to save, view, update, and delete weather queries from history, giving users a persistent and editable weather log experience.

## 🚀 Features

- 🌍 **Real-Time Weather Search**: Enter any city/town name, Zip Code/Postal Code, GPS Coordinates, Landmarks, Current location to fetch and display current weather data including temperature, sky condition, humidity, and wind details.
- 📊 **Weather History Log**: Automatically saves every search with location, time, and corresponding weather details into a local SQLite database.
- 📋 **History Viewer**: Displays all past weather queries in a clean, scrollable tabular format.
- 🗑️ **Delete Records**: Allows users to delete specific entries from history by entering the record ID.
- ✏️ **Update Records**: Enables editing of a selected record’s location and time, with automatic weather update for the new values.
- 💾 **Persistent Storage**: Uses SQLite for durable data storage between sessions.
- 🧭 **Responsive and Intuitive UI**: Built using Streamlit’s modern UI components for fast and interactive experience.
- 🌐 **API Integrated**: Uses OpenWeatherMap API to fetch live and accurate weather data.


## 🧩 Tech Stack

- Streamlit
- SQLite
- OpenWeatherMap API
- Pandas
- Python Standard Libraries: `datetime`, `requests`, `os`

## ⚙️ How to Run

1. **Clone the repository:**
   git clone https://github.com/yourusername/weather-app.git
   cd weather-app
   
3. **Install dependencies:**
   pip install -r requirements.txt

4. **Run the app:**
   streamlit run weather_app_main.py


## 📁 Folder Structure

weather-app/
├── weather_app_main.py
├── history_storer.py
├── requirements.txt
├── weather.db        # will be created automatically by the weather app
└── README.md


