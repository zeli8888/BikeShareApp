from flask import Blueprint, jsonify

weather_blueprint = Blueprint('weather', __name__)

@weather_blueprint.route('/weather', methods=['GET'])
def get_all_weather():
    return jsonify({'weather': []})