from flask import Blueprint, request
from ..service import PredictionService

"""
Blueprint for handling prediction-related API endpoints.

Endpoints:
    /prediction/<int:station_id>: Retrieve prediction data for a specific station.
"""

prediction_blueprint = Blueprint('prediction', __name__)

@prediction_blueprint.route('/prediction/<int:station_id>', methods=['GET'])
def get_prediction_by_station(station_id):
    """
    Retrieve prediction data for a specific station.

    Args:
        station_id (int): The ID of the station (path parameter).
        latitude (str): The latitude of the station (query parameter).
        longitude (str): The longitude of the station (query parameter).

    Returns:
        jsonify: A JSON response containing the prediction data (200 OK).
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    prediction = PredictionService.get_prediction_by_station_id(station_id, latitude, longitude)
    return prediction.to_json(orient='records'), 200