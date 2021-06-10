import numpy as np
import pandas as pd

TARGET_PATH = '/Users/R/code/HaukeFock/predict_energy_generation/raw_data//hourly/energy_generation_data/df_deutschland.csv'
WIND_PATH = '/Users/R/code/HaukeFock/predict_energy_generation/raw_data/hourly/features/wind_hourly_clean.csv'

def get_target_data(target='wind'):
    data_target = pd.read_csv(TARGET_PATH)
    data_target['Date'] = pd.to_datetime(data_target.Date)
    data_target = data_target.groupby(by=data_target['Date']).sum()
    if target == 'wind':
        target_df = data_target[['Wind offshore[MWh]','Wind onshore[MWh]']].sum(axis=1)
    if target == 'solar':
        target_df = data_target['Photovoltaics[MWh]']
    return target_df

def get_features_data(features=['wind_speed']):
    features_df = pd.DataFrame()
    if 'wind_speed' in features:
        wind_df = pd.read_csv(WIND_PATH, index_col=0)
        wind_df.index = pd.to_datetime(wind_df.index)
        wind_df = pd.DataFrame(wind_df.mean(axis=1), columns=['wind_speed'])
        features_df = pd.concat([features_df, wind_df], axis=1)
    return features_df

def get_test_data(test_days=4):
    target_df = get_target_data()
    features_df = get_features_data()
    complete_df = pd.concat([target_df, features_df], axis=1)
    complete_df.rename(columns={0:'energy_production'}, inplace=True)
    test_df = complete_df.iloc[-test_days*24:]
    X_test = test_df.wind_speed
    y_test = test_df.energy_production
    return X_test, y_test


if __name__ == '__main__':
    X_test, y_test = get_test_data(test_days=15)
    print(X_test.shape, y_test.shape)
