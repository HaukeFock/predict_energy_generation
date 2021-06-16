import warnings
import datetime as dt

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from predict_energy_generation.predict import Energy_Generation
from predict_energy_generation.test_data import get_test_data
from predict_energy_generation.weather import *
from predict_energy_generation.util import load_feature_df


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
def predict(target='wind', loader='local'):
    warnings.simplefilter(action='ignore', category=UserWarning)
    target = target.replace('both','wind,solar').split(',')
    print(target)
    # getting weather data from local files or remote weather files
    if loader == 'local':
        windspeed_df = load_feature_df('predict_energy_generation/data/windspeed_df.csv')
        print(windspeed_df.index[0])
        temp_df = load_feature_df('predict_energy_generation/data/temp_df.csv')
        pressure_df = load_feature_df('predict_energy_generation/data/pressure_df.csv')
        radiation_df = load_feature_df('predict_energy_generation/data/hourly_globalradiation_df.csv')
    elif loader == 'remote':
        weather_stations_df = get_weather_stations()
        station_ids = list(weather_stations_df['SDO_ID'])  # For testing purposes only
        weather_stations = fetch_longitudes(station_ids, weather_stations_df)
        windspeed_df, temp_df, pressure_df = fetch_weather_data(weather_stations)
        radiation_df = load_feature_df('predict_energy_generation/data/hourly_globalradiation_df.csv')

    # wind features
    X_wind = windspeed_df.mean(axis=1)

    # sun features
    best_sun_stations = ['13674', '4177', '3660', '15000', '4336','460','5100','5906',
                        '3098','2812','4928','2667','3287','2171','953','1639','5480',
                        '3761','1078','2485','5705','7374','2712','7368','282','1468',
                        '1766','3668','1443','5426','1270','198','3028','3231','3268',
                        '4887','2601','3167','2925','2638','867','5404','2014','232',
                        '5397','6197','1346','3366','3126','662','2559','2932','2261',
                        '5839','3631','1544','2044','691','1612','2115','2483','4393',
                        '3811','1691','342','2290','853','5856','7370','5629','3032',
                        '7367','4911','963','2907','704','5546','3730','3987','3086',
                        '4642','1001','3196','1358','427','4625','1048','1975','701',
                        '591','596','5779','856','430','4466','3015','433','5516',
                        '6163','880','4271','5109','1550','4745','164','891','183',
                        '1605','1684','7351','5792','1757','1503','4104','5142','3946']
    X_sun = radiation_df[best_sun_stations]['2021-04-26':]

    # predicting generation from model
    result = {}
    generation = Energy_Generation()
    if 'wind' in target:
        wind_result = generation.predict_wind(X_wind)
        wind_result = {date: pred for date, pred in zip(X_wind.index, wind_result.flatten().tolist())}
        result['wind'] = wind_result
    if 'solar' in target:
        sun_result = generation.predict_solar(X_sun)
        sun_result = {date: pred for date, pred in zip(X_sun.index, sun_result.flatten().tolist())}
        result['solar'] = sun_result

    return result
