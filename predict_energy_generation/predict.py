import pandas as pd
import numpy as np
import joblib
import warnings

from statsmodels.iolib.smpickle import load_pickle


class Energy_Generation():

    def __init__(self, wind_model_path='predict_energy_generation/data/models/wind_model_4.pkl',
                 #wind_feature_pipe_path='predict_energy_generation/data/models/wind_feat_pipe.pkl',
                 #wind_target_pipe_path='predict_energy_generation/data/models/wind_target_pipe.pkl',
                 sun_model_path='predict_energy_generation/data/models/sun_model.pkl',
                 sun_feat_pipe_path='predict_energy_generation/data/models/sun_feat_pipeline.pkl',
                 sun_target_pipe_path='predict_energy_generation/data/models/sun_target_pipeline.pkl'):
        self.wind_model = load_pickle(wind_model_path)
        #self.wind_feat_pipe = joblib.load(wind_feature_pipe_path)
        #self.wind_target_pipe = joblib.load(wind_target_pipe_path)
        self.sun_model = load_pickle(sun_model_path)
        self.sun_feat_pipe = joblib.load(sun_feat_pipe_path)
        self.sun_target_pipe = joblib.load(sun_target_pipe_path)

    def predict_wind(self, X_test, rnn=False, sarimax=True):
        '''Predicts the energy production from an array of features X_test'''

        if sarimax:
            results = self.wind_model.get_prediction(start=0, end=X_test.shape[0]-1, exog=X_test)
            central = results.predicted_mean
            confint = results.conf_int(alpha=0.05)
            lower = confint['lower y']
            upper = confint['upper y']

            return central, lower, upper

        if rnn:
            X_test = X_test.to_numpy().reshape(-1, 1)
            X_test = self.wind_feat_pipe.transform(X_test)
            X_test = np.expand_dims(X_test, axis=0)
            # print(X_test.shape)
            result = self.wind_model.predict(X_test)
            result = self.wind_target_pipe.inverse_transform(result.flatten().reshape(-1,1))

            return result

    def predict_solar(self, X_test):
        '''Predicts the energy production from an array of features X_test'''

        # scaling features
        X_test = pd.DataFrame(self.sun_feat_pipe.transform(X_test), columns=X_test.columns, index=X_test.index)

        # make predictions and calculate confidence interval
        results = self.sun_model.get_prediction(start=X_test.index[0], end=X_test.index[-1], exog=X_test)
        central = results.predicted_mean
        confint = results.conf_int(alpha=0.05)
        lower = confint['lower y']
        upper = confint['upper y']

        # re-scaling to original scale
        central = pd.Series(self.sun_target_pipe.inverse_transform(central.to_numpy().reshape(-1,1)).squeeze(), index=central.index)
        lower = pd.Series(self.sun_target_pipe.inverse_transform(lower.to_numpy().reshape(-1,1)).squeeze(), index=central.index)
        upper = pd.Series(self.sun_target_pipe.inverse_transform(upper.to_numpy().reshape(-1,1)).squeeze(), index=central.index)

        return central, lower, upper


if __name__ == "__main__":
    # warnings.simplefilter(action='ignore', category=FutureWarning)
    # # create loaded model instance
    # generation = Energy_Generation()

    # # make prediction
    # result = generation.predict(X_test)
    # print('Made prediction from loaded model!')
    # print(f"The result's shape is {result.shape}")
    pass
