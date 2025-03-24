from flask import Blueprint, jsonify
from ..repository import HourlyRepository

# Create a Blueprint for this API
hourly_blueprint = Blueprint('hourly', __name__)

# Fetch hourly data for a district
@hourly_blueprint.route('/hourly/<district>', methods=['GET'])
def get_hourly_data(district):
    try:
        # Get the latest hourly data for the district from the database
        hourly_data = HourlyRepository.get_by_district(district)
        
        if not hourly_data:
            return jsonify({'message': 'No hourly data available for this district'}), 404
        
        # Convert the data to a dictionary format to return it as JSON
        data = [hourly.as_dict() for hourly in hourly_data]
        
        # Return the data as a JSON response
        return jsonify(data), 200
    except Exception as e:
        # If something goes wrong, return an error message
        return jsonify({'error': str(e)}), 500
