import pandas as pd


GC_BUCKET_PATH = "gs://wagon-ml-kuntz-566/data/weather_stations_df.csv"


def get_weather_stations():
    df = pd.read_csv(GC_BUCKET_PATH)
    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df


if __name__ == "__main__":
    df = get_weather_stations()
