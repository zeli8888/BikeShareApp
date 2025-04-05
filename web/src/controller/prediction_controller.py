from flask import Blueprint, request
from ..service import prediction_service

prediction_blueprint = Blueprint('prediction', __name__)

@prediction_blueprint.route('/prediction/<int:station_id>', methods=['GET'])
def get_prediction_by_station(station_id):
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    prediction = prediction_service.get_prediction_by_station_id(station_id, latitude, longitude)
    return prediction.to_json(orient='records'), 200