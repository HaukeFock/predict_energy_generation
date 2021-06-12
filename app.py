import streamlit as st
import datetime
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from predict_energy_generation.data import get_weather_stations
from predict_energy_generation.weather import fetch_weather_data, build_datetime, fetch_longitudes

st.markdown('''
# Predict renewable energy in Germany

## Please pick your desired date and time up to 4 days from now.
''')

date = st.date_input('Date', datetime.date.today())
time = st.time_input('Time', datetime.time(9, 00))


params = {
        'XXX': 'XXX',
        }


API_URL = 'XXX'
if st.button('Submit'):
#    res = requests.get(URL, params).json()['prediction']
    date = build_datetime(date, time)
    weather_stations_df = get_weather_stations()
    station_ids = list(weather_stations_df['SDO_ID'])  # For testing purposes only
    weather_stations = fetch_longitudes(station_ids, weather_stations_df)
    windspeed_df, temp_df, pressure_df = fetch_weather_data(weather_stations)

    text = f"This is your result: **XXX**."

    st.markdown(text)

