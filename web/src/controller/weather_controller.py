from flask import Blueprint, jsonify, request
from ..service import WeatherService

"""
Blueprint for handling weather-related API endpoints.

Endpoints:
    /weather: Retrieve weather data by district, if it's too old, update it.
    /weather/current: Retrieve current weather data by district from external API call.
"""

weather_blueprint = Blueprint('weather', __name__)

@weather_blueprint.route('/weather', methods=['GET'])
def get_weather_by_district():
    """
    Retrieve weather data by district, if it's too old, update it.

    Args:
        latitude (str): The latitude of the district (query parameter).
        longitude (str): The longitude of the district (query parameter).

    Returns:
        jsonify: A JSON response containing the weather data (200 OK).
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    weather = WeatherService.get_weather_by_coordinate(latitude, longitude)
    return jsonify(weather), 200

@weather_blueprint.route('/weather/current', methods=['GET'])
def get_current_weather_by_district():
    """
    Retrieve current weather data by district from external API call.

    Args:
        latitude (str): The latitude of the district (query parameter).
        longitude (str): The longitude of the district (query parameter).

    Returns:
        jsonify: A JSON response containing the current weather data (200 OK).
    """
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    weather = WeatherService.get_current_weather_by_coordinate(latitude, longitude)
    return jsonify(weather), 200