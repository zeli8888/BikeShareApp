from flask import Blueprint, jsonify
from ..service import AvailabilityService

availability_blueprint = Blueprint('availabilities', __name__)

@availability_blueprint.route('/availabilities/<int:number>', methods=['GET'])
def get_availability(number):
    availability = AvailabilityService.get_availability(number)
    if not availability:
        return jsonify({'error': 'availability not found'}), 404

    return jsonify(availability.as_dict()), 200
    
@availability_blueprint.route('/availabilities', methods=['GET'])
def get_all_availabilities():
    """
    Retrieve all availabilities.
    """
    availabilities = AvailabilityService.get_all_availabilities()
    
    return jsonify([availability.as_dict() for availability in availabilities])