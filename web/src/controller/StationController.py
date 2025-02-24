from flask import Blueprint, jsonify
from ..service import StationService

station_blueprint = Blueprint('stations', __name__)

@station_blueprint.route('/stations/<int:number>', methods=['GET'])
def get_station(number):
    station = StationService.get_station(number)
    if not station:
        return jsonify({'error': 'Station not found'}), 404

    return jsonify(station.as_dict()), 200
    
@station_blueprint.route('/stations', methods=['GET'])
def get_all_stations():
    """
    Retrieve all stations.
    """
    stations = StationService.get_all_stations()
    
    return jsonify([station.as_dict() for station in stations])