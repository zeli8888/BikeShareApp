from datetime import datetime
import os
import pandas as pd
import numpy as np
import holidays
from sklearn.metrics import mean_absolute_error, r2_score
from tensorflow.keras.models import load_model
import warnings
import joblib
# Ignore UserWarnings from Keras
warnings.filterwarnings("ignore", category=UserWarning, module="keras")
def train_model(station_id, visualize=False):
    # Load the data
    data = pd.read_csv(f'training_data/station_{station_id}.csv')
    X = data.drop(['available_bikes', 'available_docks'], axis=1)
    y = data[['available_bikes', 'available_docks']]

    # Predict using the model
    model = load_model(f'trained_model/station_{station_id}_model.keras')
    scaler = joblib.load(f'trained_model/scaler_station_{station_id}.joblib')
    X_test = scaler.transform(X)
    y_pred = model.predict(X_test, verbose=visualize)

    # Evaluate each target separately
    mae_bikes = mean_absolute_error(y[:, 0], y_pred[:, 0])
    mae_docks = mean_absolute_error(y[:, 1], y_pred[:, 1])

    r2_score_bikes = r2_score(y[:, 0], y_pred[:, 0])
    r2_score_docks = r2_score(y[:, 1], y_pred[:, 1])
        
    return mae_bikes, r2_score_bikes, mae_docks, r2_score_docks

if __name__ == '__main__':
    train_model(1)
