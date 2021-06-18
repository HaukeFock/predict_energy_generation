import warnings
import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from predict_energy_generation.data import load_local_feature_df
from predict_energy_generation.predict import Energy_Generation
from predict_energy_generation.test_data import get_test_data
from predict_energy_generation.util import load_feature_df, list_hourly_datetime


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
    # print(target)
    # getting weather data from local files or remote weather files
    if loader == 'local':
       X_wind = load_local_feature_df(target='wind')
       X_sun = load_local_feature_df(target='solar')
    elif loader == 'remote':
        # HAS TO BE FINISHED
        weather_stations_df = get_weather_stations()
        station_ids = list(weather_stations_df['SDO_ID'])  # For testing purposes only
        weather_stations = fetch_longitudes(station_ids, weather_stations_df)
        windspeed_df, temp_df, pressure_df = fetch_weather_data(weather_stations)
        humidity = load_feature_df('predict_energy_generation/data/humidity_df.csv')
        radiation_df = load_feature_df('predict_energy_generation/data/radiation_df.csv')
    # predicting generation from model
    now = pd.Timestamp(datetime.datetime.now().date())
    final_index = list_hourly_datetime(init_date=now, end_date=now+(datetime.timedelta(30)))
    final_index = [pd.Timestamp(date) for date in final_index]
    result = {}
    generation = Energy_Generation()
    if 'wind' in target:
        wind_central, wind_lower, wind_upper = generation.predict_wind(X_wind)
        wind_central.index =  final_index
        wind_lower.index = final_index
        wind_upper.index = final_index
        result['wind'] = {'central': wind_central.to_dict(), 'lower': wind_lower.to_dict(), 'upper':wind_upper.to_dict()}
    if 'solar' in target:
        sun_central, sun_lower, sun_upper = generation.predict_solar(X_sun)
        sun_central.index =  final_index
        sun_lower.index = final_index
        sun_upper.index = final_index
        result['sun'] = {'central': sun_central.to_dict(), 'lower': sun_lower.to_dict(), 'upper':sun_upper.to_dict()}
    #print({idx.strftime('%Y-%m-%dT:%H:%M:%S'): value for value, idx in zip(wind_central.values, final_index)})
    return result
