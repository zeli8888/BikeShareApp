import os
import pickle
from .WeatherService import WeatherService

class prediction_service:
    @staticmethod
    def get_prediction_by_station_id(station_id, latitude, longitude):
        path_for_model = os.path.join(os.path.dirname(__file__), f'../../../machine_learning/trained_model/station_{station_id}_model.pkl')
        path_for_scaler = os.path.join(os.path.dirname(__file__), f'../../../machine_learning/training_data/scaler_station_{station_id}.pkl')

        if not os.path.exists(path_for_model) or not os.path.exists(path_for_scaler):
            return []
        with open(path_for_model, 'rb') as f:
            model = pickle.load(f)
        with open(path_for_scaler, 'rb') as f:
            scaler = pickle.load(f)

        hourly_data = WeatherService.get_current_weather_by_coordinate(latitude, longitude)['hourly'][0:24]
        debug = True