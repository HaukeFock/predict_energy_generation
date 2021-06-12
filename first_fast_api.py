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
def predict(start_time, end_time):
    # call the model + predict
    start_time = f'{start_time[:10]} {start_time[11:]}'
    end_time = f'{end_time[:10]} {end_time[11:]}'

    if True:
        X_test, y_test = get_test_data(start_time, end_time)
    else:
        weather_stations_df = get_weather_stations()
        station_ids = list(weather_stations_df['SDO_ID'])  # For testing purposes only
        weather_stations = fetch_longitudes(station_ids, weather_stations_df)
        windspeed_df, temp_df, pressure_df = fetch_weather_data(weather_stations)
        X_test = windspeed_df.mean(axis=1)

    generation = Energy_Generation()

    result = generation.predict(X_test)

    # return str(type(result))
    return {date: round(pred, 4) for pred, date in zip(result.flatten().tolist(), X_test.index)}
