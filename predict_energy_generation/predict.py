import pandas as pd
import numpy as np
import joblib
import warnings

from predict_energy_generation.test_data import get_test_data

from tensorflow.keras.models import load_model


class Energy_Generation():

    def __init__(self, model_name='dummy_model.h5', pipe_name='pipeline.pkl'):
        self.model = load_model(model_name)
        self.pipeline = joblib.load(pipe_name)

    def predict(self, X_test):
        '''Predicts the energy production from an array of features X_test'''
        X_test = X_test.to_numpy().reshape(-1, 1)
        X_test = self.pipeline.transform(X_test)
        X_test = np.expand_dims(X_test, axis=0)
        print(X_test.shape)
        result = self.model.predict(X_test)
        return result


if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    # create loaded model instance
    generation = Energy_Generation()

    # get testing data
    X_test, y_test = get_test_data()

    #print(X_test.shape)
    # make prediction
    result = generation.predict(X_test)
    print('Made prediction from loaded model!')
    print(f"The result's shape is {result.shape}")
