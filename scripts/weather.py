import pandas as pd
import time
from datetime import datetime as dt
import requests
from data import generate_dataframe


# Global variables
API_KEY = 'b1b15e88fa797225412429c1c50c122a1'


''' Function to fetch geo data for a list of station ids '''

def fetch_longitudes(station_ids, raw_data):
    df = pd.DataFrame(station_ids).merge(raw_data, left_on = 0, right_on = 'SDO_ID')
    df.drop([0,'SDO_Name','Height_above_NN', 'Metadata_Link'], axis=1,inplace = True)
    return df


''' Function to build a datetime object from user inputs for "date" and "time" '''

def build_datetime(date, time):
    format = "%Y-%m-%d %H:%M:%S"
    date_time = f'{date} {time}'
    return dt.strptime(date_time, format)


''' Function to convert a UNIX timestamp to a datetime object '''

def datetime_converter(timestamp):
    return dt.fromtimestamp(timestamp)


''' Function to convert a datetime object to an UNIX timestamp '''

def unix_converter(date):
    date = (time.mktime(date.timetuple()))
    return date


''' Function to convert a temperature from Kelvin to Celsius '''

def celsius_converter(temp):
    return round(float(temp)-273.15,2)


''' Function to create pivoted dataframes for specific weather forecast data '''

def create_dataframe(dates,stations, feature, feature_name):
    data = list(zip(dates, stations, feature))
    data_df = pd.DataFrame(data, columns=['Date', 'Station_ID', str(feature_name)])
    data_df.set_index('Date', inplace=True)
    return data_df.pivot(columns="Station_ID", values=str(feature_name))


''' Function to featch weather forecast data from openweather API '''

def fetch_weather_data(stations):
    dates = []
    station_id = []
    windspeed = []
    temp = []
    pressure = []
    i = 0
    for index in range(stations.shape[0]):
        latitude = stations['Latitude'][index]
        longitude = stations['Longitude'][index]
        API_LINK = f'http://pro.openweathermap.org/data/2.5/forecast/hourly?lat={latitude}&lon={longitude}&appid={API_KEY}'
        response = requests.get(url=API_LINK).json()
        for predictions in range(len(response['list'])):
            dates.append(datetime_converter(response['list'][predictions]['dt']))
            station_id.append(stations['SDO_ID'][index])
            windspeed.append(response['list'][predictions]['wind']['speed'])
            temp.append(celsius_converter(response['list'][predictions]['main']['temp']))
            pressure.append(response['list'][predictions]['main']['pressure'])
            i+=1
    return create_dataframe(dates, station_id, windspeed, 'Wind_speed'), create_dataframe(dates, station_id, temp, 'Temperature'), create_dataframe(dates, station_id, pressure, 'Air_pressure')


if __name__ == "__main__":
    df, sdo_df = generate_dataframe('/Users/michael.kuntz/code/HaukeFock/predict_energy_generation/raw_data/Features/Humidity','daily','Humidity')
    station_ids = list(sdo_df['SDO_ID'])  # For testing purposes only
    weather_stations = fetch_longitudes(station_ids, sdo_df)  # For testing purposes only
    windspeed_df, temp_df, pressure_df = fetch_weather_data(weather_stations)
    print(windspeed_df.head())
