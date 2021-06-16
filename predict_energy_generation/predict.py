import pandas as pd
import numpy as np
import joblib
import warnings

from predict_energy_generation.test_data import get_test_data

from tensorflow.keras.models import load_model
from statsmodels.iolib.smpickle import load_pickle


class Energy_Generation():

    def __init__(self, wind_model_path='predict_energy_generation/data/models/wind_model_2.h5',
                 wind_feature_pipe_path='predict_energy_generation/data/models/wind_feat_pipe.pkl',
                 wind_target_pipe_path='predict_energy_generation/data/models/wind_target_pipe.pkl',
                 sun_model_path='predict_energy_generation/data/models/sun_model.pkl',
                 sun_feat_pipe_path='predict_energy_generation/data/models/sun_feat_pipeline.pkl',
                 sun_target_pipe_path='predict_energy_generation/data/models/scaler_y_pipeline.pkl'):
        self.wind_model = load_model(wind_model_path)
        self.wind_feat_pipe = joblib.load(wind_feature_pipe_path)
        self.wind_target_pipe = joblib.load(wind_target_pipe_path)
        self.sun_model = load_pickle(sun_model_path)
        self.sun_feat_pipe = joblib.load(wind_feature_pipe_path)
        self.sun_target_pipe = joblib.load(wind_target_pipe_path)

    def predict_wind(self, X_test):
        '''Predicts the energy production from an array of features X_test'''
        X_test = X_test.to_numpy().reshape(-1, 1)
        X_test = self.wind_feat_pipe.transform(X_test)
        X_test = np.expand_dims(X_test, axis=0)
        # print(X_test.shape)
        result = self.wind_model.predict(X_test)
        result = self.wind_target_pipe.inverse_transform(result.flatten().reshape(-1,1))
        return result

    def predict_solar(self, X_test):
        '''Predicts the energy production from an array of features X_test'''
        X_test = self.sun_feat_pipe.transform(X_test)
        result = self.sun_model.forecast(steps=len(X_test), exog=X_test, alpha=0.05)
        result = self.sun_target_pipe.inverse_transform(result.to_numpy().flatten().reshape(1,-1))
        return result

if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    # create loaded model instance
    generation = Energy_Generation()

    # get wind testing data
    X_test, y_test = get_test_data()

    # make prediction
    result = generation.predict(X_test)
    print('Made prediction from loaded model!')
    print(f"The result's shape is {result.shape}")
