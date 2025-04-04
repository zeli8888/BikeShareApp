import os
import warnings
# Set environment variable to ignore CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Set to 3 to hide all logs, warnings, and errors
from datetime import datetime
import holidays
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
# Import TensorFlow after setting the environment variable
import tensorflow as tf
from tensorflow.keras.models import load_model
# Ignore UserWarnings from Keras and other warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="sklearn.utils.validation")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
def train_model(station_id, visualize=False):
    # Load the data
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), f'training_data/station_{station_id}.csv'))
    X = data.drop(['available_bikes', 'available_docks'], axis=1)
    y = data[['available_bikes', 'available_docks']].values

    # Predict using the model
    model = load_model(os.path.join(os.path.dirname(__file__), f'trained_model/station_{station_id}_model.keras'))
    scaler = joblib.load(os.path.join(os.path.dirname(__file__), f'trained_model/scaler_station_{station_id}.joblib'))
    X_test = scaler.transform(X)
    y_pred = model.predict(X_test, verbose=visualize)

    # Evaluate each target separately
    mae_bikes = mean_absolute_error(y[:, 0], y_pred[:, 0])
    mae_docks = mean_absolute_error(y[:, 1], y_pred[:, 1])

    r2_score_bikes = r2_score(y[:, 0], y_pred[:, 0])
    r2_score_docks = r2_score(y[:, 1], y_pred[:, 1])
        
    return mae_bikes, r2_score_bikes, mae_docks, r2_score_docks

if __name__ == '__main__':
    mae_bikes, r2_score_bikes, mae_docks, r2_score_docks = train_model(1)
    print(f"MAE bikes: {mae_bikes}, R2 score bikes: {r2_score_bikes}, MAE docks: {mae_docks}, R2 score docks: {r2_score_docks}")

