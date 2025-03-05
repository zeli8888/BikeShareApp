from flask import Blueprint, jsonify, request
from ..service import WeatherService

weather_blueprint = Blueprint('weather', __name__)

@weather_blueprint.route('/weather', methods=['GET'])
def get_weather_by_district():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    weather = WeatherService.get_weather_by_coordinate(latitude, longitude)
    return jsonify(weather), 200