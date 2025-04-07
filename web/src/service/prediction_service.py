import os
import pickle
import pandas as pd
import numpy as np
import holidays
from .weather_service import WeatherService

class prediction_service:
    """
    Represents a service for making predictions about bike availability.

    Methods:
        get_prediction_by_station_id(station_id, latitude, longitude): Retrieves a prediction for the specified station. The latitude and longitude are used to fetch weather data.
    """
    
    @staticmethod
    def get_prediction_by_station_id(station_id, latitude, longitude):
        """
        Retrieves a prediction for the specified station.

        Args:
            station_id (int): The ID of the station.
            latitude (float): The latitude of the station.
            longitude (float): The longitude of the station.

        Returns:
            pd.DataFrame: A DataFrame containing the predicted availability of bikes and stands for the next 24 hours.
        """
        
        # check if the model exists
        path_for_model = os.path.join(os.path.dirname(__file__), f'../../../machine_learning/trained_model/station_{station_id}_model.pkl')
        path_for_scaler = os.path.join(os.path.dirname(__file__), f'../../../machine_learning/trained_model/scaler_station_{station_id}.pkl')

        # if the model does not exist, return an empty DataFrame
        if not os.path.isfile(path_for_model) or not os.path.isfile(path_for_scaler):
            return pd.DataFrame()

        # fetch weather data
        hourly_data = WeatherService.get_weather_by_coordinate(latitude, longitude)['hourly'][1:25]
        # preprocess features data
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

        # load model
        with open(path_for_model, 'rb') as f:
            model = pickle.load(f)
        # load scaler, transform features data
        with open(path_for_scaler, 'rb') as f:
            scaler = pickle.load(f)
        transformed_data = scaler.transform(df.values)
        # make prediction
        prediction = np.round(model.predict(transformed_data, verbose=False))
        # combine prediction with hour info
        hour_prediction[['available_bikes', 'available_stands']] = prediction
        return hour_prediction