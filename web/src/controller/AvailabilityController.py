from flask import Blueprint, jsonify
from ..service import AvailabilityService

availability_blueprint = Blueprint('availabilities', __name__)

@availability_blueprint.route('/availabilities', methods=['GET'])
def get_all_availabilities():
    """
    Retrieve all availabilities.
    """
    availabilities = AvailabilityService.get_all_availabilities()
    
    return jsonify([availability.as_dict() for availability in availabilities])

@availability_blueprint.route('/availabilities/<int:number>', methods=['GET'])
def get_availability(number):

    availabilities = AvailabilityService.get_availability(number)

    return jsonify([availability.as_dict() for availability in availabilities])

@availability_blueprint.route('/availabilities/latest', methods=['GET'])
def get_latest_availabilities():
    
    availabilities = AvailabilityService.get_latest_availabilities()

    return jsonify([availability.as_dict() for availability in availabilities])

@availability_blueprint.route('/availabilities/latest/<int:number>', methods=['GET'])
def get_latest_availability(number):
    
    availability = AvailabilityService.get_latest_availability(number)
    if not availability:
        return jsonify({'error': 'Availability not found'}), 404

    return jsonify(availability.as_dict()), 200