import os
import warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Set to 3 to hide all logs, warnings, and errors
import pickle
import pandas as pd
import numpy as np
import holidays
from .WeatherService import WeatherService
# Ignore UserWarnings from Keras
warnings.filterwarnings("ignore", category=UserWarning)

class prediction_service:
    @staticmethod
    def get_prediction_by_station_id(station_id, latitude, longitude):
        path_for_model = os.path.join(os.path.dirname(__file__), f'../../../machine_learning/trained_model/station_{station_id}_model.pkl')
        path_for_scaler = os.path.join(os.path.dirname(__file__), f'../../../machine_learning/trained_model/scaler_station_{station_id}.pkl')

        if not os.path.isfile(path_for_model) or not os.path.isfile(path_for_scaler):
            return []

        hourly_data = WeatherService.get_weather_by_coordinate(latitude, longitude)['hourly'][0:24]
        df = pd.DataFrame(hourly_data)[['future_dt', 'temp', 'pressure', 'humidity']]
        df['future_dt'] = pd.to_datetime(df['future_dt'])
        df['hour'] = df['future_dt'].dt.hour
        # add is_holiday and is_weekend
        ireland_holidays = holidays.country_holidays('IE')
        df['is_holiday'] = df['future_dt'].apply(lambda x: x in ireland_holidays)
        df['is_weekend'] = df['future_dt'].apply(lambda x: x.weekday() in [5, 6])
        # Cyclical Encoding for hour feature
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 23.0).round(6)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 23.0).round(6)
        # convert temperature from Kelvin to Celsius
        df['temp'] = df['temp'] - 273.15
        # keep hour info for the prediction result
        hour_prediction = pd.DataFrame(df['future_dt'].dt.strftime('%Y-%m-%dT%H:%M:%S%z'))
        # drop unnecessary columns, rearrange columns to match training data
        df = df[['temp', 'humidity', 'pressure', 'is_holiday', 'is_weekend', 'hour_sin', 'hour_cos']]

        with open(path_for_model, 'rb') as f:
            model = pickle.load(f)
        with open(path_for_scaler, 'rb') as f:
            scaler = pickle.load(f)
        transformed_data = scaler.transform(df.values)
        prediction = np.round(model.predict(transformed_data, verbose=False))
        hour_prediction[['available_bikes', 'available_stands']] = prediction
        return hour_prediction