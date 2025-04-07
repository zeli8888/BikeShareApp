from flask import Blueprint, jsonify
from ..service import BikesService

"""
Blueprint for handling bike-related API endpoints.

Endpoints:
    /bikes: Retrieve all stations' bikes condition, if it's too old, update it.
    /bikes/current: Retrieve all stations' bikes current condition from external API call.
    /bikes/oneday: Retrieve one day's availability of bikes for each station.
    /bikes/oneday/<int:station_id>: Retrieve one day's availability of bikes for a specific station.
"""

bikes_blueprint = Blueprint('bikes', __name__)

@bikes_blueprint.route('/bikes', methods=['GET'])
def get_all_bikes():
    """
    Retrieve all stations' bikes condition, if it's too old, update it.

    If data from database is older than time interval in config.py, then it will fetch data from website API calls.

    Returns:
        jsonify: A JSON response containing the bikes condition (200 OK).
    """
    
    return jsonify(BikesService.get_all_bikes()), 200

@bikes_blueprint.route('/bikes/current', methods=['GET'])
def get_all_current_bikes():
    """
    Retrieve all stations' bikes current condition, this method will be guaranteed to fetch data from website API calls.

    Returns:
        jsonify: A JSON response containing the current bikes condition (200 OK).
    """
    
    return jsonify(BikesService.get_all_current_bikes()), 200

@bikes_blueprint.route('/bikes/oneday', methods=['GET'])
def get_one_day_availability():
    """
    Retrieve one day's availability of bikes for each station.

    Returns:
        jsonify: A JSON response containing the one day's availability of bikes (200 OK).
    """
    return jsonify(BikesService.get_one_day_availability()), 200

@bikes_blueprint.route('/bikes/oneday/<int:station_id>', methods=['GET'])
def get_one_day_availability_for_station(station_id):
    """
    Retrieve one day's availability of bikes for a specific station.

    Args:
        station_id (int): The ID of the station.

    Returns:
        jsonify: A JSON response containing the one day's availability of bikes for the specified station (200 OK).
    """
    return jsonify(BikesService.get_one_day_availability_for_station(station_id)), 200