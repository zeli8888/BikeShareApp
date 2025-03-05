from flask import Blueprint, jsonify
from ..service import BikesService

bikes_blueprint = Blueprint('bikes', __name__)

@bikes_blueprint.route('/bikes', methods=['GET'])
def get_all_bikes():
    """
    Retrieve all stations' bikes condition.
    """
    
    return jsonify(BikesService.get_all_bikes())

@bikes_blueprint.route('/bikes/<int:number>', methods=['GET'])
def get_bikes(number):
    """
    Retrieve one station's bikes condition.
    """
    
    return jsonify(BikesService.get_bikes(number))