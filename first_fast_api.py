import datetime as dt

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from predict_energy_generation.predict import Energy_Generation
from predict_energy_generation.test_data import get_test_data
from predict_energy_generation.weather import *

# run in your machine to test: from uvicorn first_fast_api.py 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return "The root default output"

@app.get("/predict")
def predict(target='wind', features='wind', loader='local'):
    # getting weather data from local files or remote weather files
    if loader == 'local':
        windspeed_df = pd.read_csv('predict_energy_generation/data/windspeed_df.csv', index_col='Date')
        temp_df = pd.read_csv('predict_energy_generation/data/temp_df.csv', index_col='Date')
        pressure_df = pd.read_csv('predict_energy_generation/data/pressure_df.csv', index_col='Date')
    elif loader == 'remote':
        weather_stations_df = get_weather_stations()
        station_ids = list(weather_stations_df['SDO_ID'])  # For testing purposes only
        weather_stations = fetch_longitudes(station_ids, weather_stations_df)
        windspeed_df, temp_df, pressure_df = fetch_weather_data(weather_stations)

    features = features.split(',')
    X_test = pd.DataFrame()
    if 'wind' in features:
        X_test['wind_speed'] = windspeed_df.mean(axis=1)
        X_test.index = windspeed_df.index
    if 'temp' in features:
        X_test['temperature'] = temp_df.mean(axis=1)
    if 'pressure' in features:
        X_test['air_pressure'] = pressure_df.mean(axis=1)

    # predicting generation from model
    generation = Energy_Generation()
    result = generation.predict(X_test)
    result = {date: pred for date, pred in zip(X_test.index, result.flatten().tolist())}

    return result
