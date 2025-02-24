from flask import Blueprint, jsonify

station_blueprint = Blueprint('stations', __name__)

@station_blueprint.route('/stations', methods=['GET'])
def get_all_stations():
    return jsonify({'stations': []})