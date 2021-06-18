import pandas as pd
import datetime as dt

LOCAL_PATH = 'predict_energy_generation/data/weather_stations_df.csv'

def get_weather_stations():
    df = pd.read_csv(LOCAL_PATH)
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

def load_feature_df(path, date_as_index=True):
    ''' Returns the dataframe from the provided path and sets "Date" as index in
    the correct format. '''

    df = pd.read_csv(path)

    if date_as_index:
        #print(('Date' in list(df.columns)))
        if 'Date' in list(df.columns):
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)

    return df

def list_hourly_datetime(init_date=pd.Timestamp(2021,4,1), end_date=pd.Timestamp(2021,5,1)):
    ''' Returns a list of datetime timestamps from init_date to end_date '''

    dates = []
    date = init_date
    n_days = ((end_date-init_date).days) * 24
    for _ in range(n_days):
        dates.append(date)
        date += dt.timedelta(hours=1)

    return dates
