import streamlit as st
from streamlit_js_eval import get_geolocation
from collections import defaultdict
from datetime import datetime

from history_storer import init_db , read_records, create_record, delete_record, update_record
from helper import get_coordinates, get_weather, validate_coordinates, deg_to_compass

st.set_page_config(layout="wide")

init_db()

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.markdown("""
    <style>
    .stButton > button {
        width: 200px;  /* Change width as needed */
        height: 40px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.write("### Go to:")

if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("History"):
    st.session_state.page = "History"

if st.session_state.page == "Home":

    st.markdown("<h1 style='text-align: center;'>Weather App</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("**Developed by Tanveer Bagi**")

    with col2:
        if st.button("About PM Accelerator"):
            st.info(
                "PM Accelerator helps aspiring product managers become industry-ready by offering real-world training, mentorship, and job-focused guidance. Learn more at [LinkedIn Page](https://www.linkedin.com/school/pmaccelerator/)"
            )

    input_type = st.selectbox("Choose how you want to enter the location:",["City/Town", "Zip Code/Postal Code", "GPS Coordinates", "Landmarks", "Current location"])


    if input_type in ["City/Town", "Zip Code/Postal Code", "Landmarks"]:
        user_input = st.text_input(f"### Enter the {input_type}")

        if user_input:
            lat, lon = get_coordinates(user_input)
            if lat is None or lon is None:
                st.error("Location not found. Please check the spelling or try a more specific name.")
            else:
                st.success(f"Coordinates: ({lat}, {lon})")
                weather_data = get_weather(lat, lon, "current")
                if weather_data:
                    st.subheader(" Current Weather: ")

                    st.write("Temp:", weather_data["main"]["temp"], "°C")
                    avg_temp = weather_data["main"]["temp"], "°C"

                    st.write("Sky Condition:", weather_data["weather"][0]["description"])
                    sky_condition = weather_data["weather"][0]["description"]

                    st.write("Humidity:", weather_data["main"]["humidity"], "%")
                    humidity =  weather_data["main"]["humidity"], "%"

                    wind_speed = weather_data["wind"]["speed"]
                    wind_deg = weather_data["wind"]["deg"]

                    wind_dir = deg_to_compass(wind_deg)

                    st.write(f"Wind Speed: {wind_speed} m/s")

                    st.write(f"Wind Direction: {wind_dir} ({wind_deg}°)")

                    create_record(user_input, avg_temp, sky_condition, humidity, wind_speed, wind_dir)

                    forecast_data = get_weather(lat, lon, mode="forecast")
                    if forecast_data:
                        daily_forecast = defaultdict(list)

                        for entry in forecast_data["list"]:
                            date = entry["dt_txt"].split(" ")[0]
                            daily_forecast[date].append(entry)

                        st.subheader("5-Day Forecast")
                        for date, entries in list(daily_forecast.items())[:5]:
                            temps = [e["main"]["temp"] for e in entries]
                            descriptions = [e["weather"][0]["description"] for e in entries]
                            avg_temp = round(sum(temps) / len(temps), 2)
                            common_desc = max(set(descriptions), key=descriptions.count)

                            readable_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %b %d")
                            st.write(f"{readable_date} — Average temp.:  {avg_temp}°C — Sky Condition: {common_desc}")

                else:
                    st.error("Failed to fetch weather. Try again later.")


    elif input_type in "GPS Coordinates":
        coordinates_of_location_direct = st.text_input(f"### Enter the GPS Coordinates in this format: (latitude, longitude) ")

        if coordinates_of_location_direct:
            lat_validated, lon_validated = validate_coordinates(coordinates_of_location_direct)
            if lat_validated is None or lon_validated is None:
                st.error("Invalid coordinates. Please provide a valid coordinate or check the format, it should be in the format (lat, lon) e.g.( 28.61, 77.20)")
            else:
                st.success(f"Coordinates: ({lat_validated}, {lon_validated})")
                weather_data = get_weather(lat_validated, lon_validated,"current")
                if weather_data:
                    st.write("### Current Weather")
                    st.write("Temp:", weather_data["main"]["temp"], "°C")
                    avg_temp = weather_data["main"]["temp"], "°C"

                    st.write("Sky Condition:", weather_data["weather"][0]["description"])
                    sky_condition = weather_data["weather"][0]["description"]

                    st.write("Humidity:", weather_data["main"]["humidity"], "%")
                    humidity = weather_data["main"]["humidity"], "%"

                    wind_speed = weather_data["wind"]["speed"]
                    wind_deg = weather_data["wind"]["deg"]

                    wind_dir = deg_to_compass(wind_deg)

                    st.write(f"Wind Speed: {wind_speed} m/s")
                    st.write(f"Wind Direction: {wind_dir} ({wind_deg}°)")

                    create_record(coordinates_of_location_direct, avg_temp, sky_condition, humidity, wind_speed, wind_dir)

                    forecast_data = get_weather(lat_validated, lon_validated, mode="forecast")
                    if forecast_data:
                        daily_forecast = defaultdict(list)

                        for entry in forecast_data["list"]:
                            date = entry["dt_txt"].split(" ")[0]
                            daily_forecast[date].append(entry)

                        st.subheader("5-Day Forecast")
                        for date, entries in list(daily_forecast.items())[:5]:
                            temps = [e["main"]["temp"] for e in entries]
                            descriptions = [e["weather"][0]["description"] for e in entries]
                            avg_temp = round(sum(temps) / len(temps), 2)
                            common_desc = max(set(descriptions), key=descriptions.count)

                            readable_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %b %d")
                            st.write(f"{readable_date} — Average temp.:  {avg_temp}°C — Sky Condition: {common_desc}")
                else:
                    st.error("Failed to fetch weather. Try again later.")


    else:
        location = get_geolocation()
        if location is None:
            st.info("Requesting location access...")
        elif "coords" in location:
            lat_current = location["coords"]["latitude"]
            lon_current = location["coords"]["longitude"]
            st.success(f"Location acquired: Latitude {lat_current}, Longitude {lon_current}")

            weather_data = get_weather(lat_current,lon_current,"current")
            if weather_data:
                st.write("### Current Weather: ")
                st.write("Temp:", weather_data["main"]["temp"], "°C")
                avg_temp = weather_data["main"]["temp"], "°C"

                st.write("Sky Condition:", weather_data["weather"][0]["description"])
                sky_condition = weather_data["weather"][0]["description"]

                st.write("Humidity:", weather_data["main"]["humidity"], "%")
                humidity = weather_data["main"]["humidity"], "%"

                wind_speed = weather_data["wind"]["speed"]
                wind_deg = weather_data["wind"]["deg"]

                wind_dir = deg_to_compass(wind_deg)

                st.write(f"Wind Speed: {wind_speed} m/s")
                st.write(f"Wind Direction: {wind_dir} ({wind_deg}°)")

                location_current = "Current Location"

                create_record(location_current, avg_temp, sky_condition, humidity, wind_speed, wind_dir)

                forecast_data = get_weather(lat_current, lon_current, mode="forecast")
                if forecast_data:
                    daily_forecast = defaultdict(list)

                    for entry in forecast_data["list"]:
                        date = entry["dt_txt"].split(" ")[0]
                        daily_forecast[date].append(entry)

                    st.subheader("5-Day Forecast")
                    for date, entries in list(daily_forecast.items())[:5]:
                        temps = [e["main"]["temp"] for e in entries]
                        descriptions = [e["weather"][0]["description"] for e in entries]
                        avg_temp = round(sum(temps) / len(temps), 2)
                        common_desc = max(set(descriptions), key=descriptions.count)

                        readable_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %b %d")
                        st.write(f"{readable_date} — Average temp.:  {avg_temp}°C — Sky Condition: {common_desc}")
            else:
                st.warning("something is wrong")
        else:
            st.warning("Please allow location access in your browser and reload the app.")

elif st.session_state.page == "History":
    from helper import get_coordinates, get_weather, validate_coordinates, deg_to_compass

    st.title("Weather History")

    record_id = st.text_input("Enter the ID of the record")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Delete Record"):
            delete_record(record_id)
            st.success("Record deleted successfully!")

    with col2:
        new_location = st.text_input("New Location")
        new_time = st.time_input("New Time")

        if st.button("Update Record"):

            if new_location and new_time:

                full_datetime = datetime.combine(datetime.today(), new_time)
                lat, lon = get_coordinates(new_location)

                if lat is None or lon is None:
                    st.error("Location not found. Please check the spelling or try a more specific name.")

                else:
                    weather = get_weather(lat, lon, mode="current")
                    wind_deg = weather["wind"]["deg"]

                    wind_dir = deg_to_compass(wind_deg)

                    if weather:
                        update_record(record_id, new_location, full_datetime, weather['main']['temp'],
                                      weather["weather"][0]["description"], weather["main"]["humidity"],
                                      weather["wind"]["speed"], wind_dir)
                        st.success("Record updated successfully!")

    history = read_records()

    st.dataframe(history, use_container_width=True)
