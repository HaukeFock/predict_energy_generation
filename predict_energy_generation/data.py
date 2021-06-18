import pandas as pd

from predict_energy_generation.util import load_feature_df, list_hourly_datetime
from predict_energy_generation.weather import fetch_longitudes, fetch_weather_data
from predict_energy_generation.util import get_weather_stations

def load_local_feature_df(target='wind'):
    ''' Loads and returns the features (X_test) for a specified target'''
    df = pd.DataFrame(index=list_hourly_datetime())
    if target == 'wind':
        df = df.join(pd.Series(load_feature_df(f'{DATA_PATH}/windspeed_df.csv').mean(axis=1), name='wind_speed'))
        df = df.join(pd.Series(load_feature_df(f'{DATA_PATH}/pressure_df.csv').mean(axis=1), name='air_pressure'))
        df = df.join(pd.Series(load_feature_df(f'{DATA_PATH}/humidity_df.csv').mean(axis=1), name='humidity'))
        df = df.join(pd.Series(load_feature_df(f'{DATA_PATH}/temp_df.csv').mean(axis=1), name='temperature'))
        #print('Wind features Loaded!')

    if target == 'solar':
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
        radiation_df = load_feature_df(f'{DATA_PATH}/radiation_df.csv')[best_sun_stations]
        df = df.join(radiation_df, how='left')

    return df

def load_remote_feature_df(target='wind'):
    df = pd.DataFrame(index=list_hourly_datetime())
    if target == 'wind':
        weather_stations_df = get_weather_stations()
        station_ids = list(weather_stations_df['SDO_ID'])
        weather_stations = fetch_longitudes(station_ids, weather_stations_df)
        windspeed_df, temp_df, pressure_df, humidity_df, cloudiness_df = fetch_weather_data(weather_stations)
        df['wind_speed'] = windspeed_df.mean(axis=1)
        df['air_pressure'] = pressure_df.mean(axis=1)
        df['humidity'] = humidity_df.mean(axis=1)
        df['temperature'] = temp_df.mean(axis=1)
    if target == 'solar':
        # TO BE DEVELOPED...
        pass
    return df


if __name__ == "__main__":
    df = load_remote_feature_df()
    print(df.shape)
    print(df.head())
