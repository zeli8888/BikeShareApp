from ..repository import CurrentRepository
from ..repository import HourlyRepository
from ..repository import DailyRepository
from ..repository import AlertsRepository
from ..config import OPEN_WEATHER_DUBLIN_LOC
from math import radians, sin, cos, sqrt, atan2
def get_distance(coord1, coord2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    
    # Difference between coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Distance in kilometers
    distance = R * c
    
    return distance

def find_nearest_district(coord1):
    min_distance = float('inf')
    nearest_district = None

    for district, coord2 in OPEN_WEATHER_DUBLIN_LOC.items():
        distance = get_distance(coord1, coord2)
        if distance < min_distance:
            min_distance = distance
            nearest_district = district

    return nearest_district

class WeatherService:

    @staticmethod
    def get_by_coordinate(latitude, longitude):
        if latitude is None or longitude is None:
            district = 'Dublin 1'
        else:
            district = find_nearest_district((float(latitude), float(longitude)))
        weather = {}
        weather['current'] = CurrentRepository.get_by_district(district).as_dict()
        weather['hourly'] = [hourly.as_dict() for hourly in HourlyRepository.get_by_district(district)]
        weather['daily'] = [daily.as_dict() for daily in DailyRepository.get_by_district(district)]
        weather['alerts'] = [alerts.as_dict() for alerts in AlertsRepository.get_by_district(district)]
        return weather