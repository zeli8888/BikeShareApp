from flask import Blueprint, jsonify
from ..service import BikesService

bikes_blueprint = Blueprint('bikes', __name__)

@bikes_blueprint.route('/bikes', methods=['GET'])
def get_all_bikes():
    """
    Retrieve all stations' bikes condition.
    If data from database is older than time interval in config.py, then it will fetch data from website API calls.
    """
    
    return jsonify(BikesService.get_all_bikes())

@bikes_blueprint.route('/bikes/current', methods=['GET'])
def get_all_current_bikes():
    """
    Retrieve all stations' bikes current condition, this method will be guaranteed to fetch data from website API calls.
    """
    
    return jsonify(BikesService.get_all_current_bikes())