from ..repository import CurrentRepository, HourlyRepository, DailyRepository, AlertsRepository
from ..model import Current, Hourly, Daily, Alerts
from ..config import OPEN_WEATHER_DUBLIN_LOC, OPEN_WEATHER_KEY, OPEN_WEATHER_URI, AUTO_WEATHER_UPDATE_INTERVAL
import requests
from datetime import datetime, timedelta
import simplejson as json
from threading import Thread
from flask import current_app
from math import radians, sin, cos, sqrt, atan2

class WeatherService:
    """
    Represents a service for managing weather data involving current, hourly, daily, and alerts.

    Methods:
        get_weather_by_coordinate(latitude, longitude): Retrieves the weather data for the specified coordinates, if it's too old, update it.
        get_current_weather_by_coordinate(latitude, longitude, district=None): Retrieves the current weather data for the specified coordinates from external API call.
    """
    
    @staticmethod
    def get_weather_by_coordinate(latitude, longitude):
        """
        Retrieves the weather data for the specified coordinates, if it's too old, update it.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.

        Returns:
            dict: A dictionary containing the weather data.
        """
        
        # Find the nearest district, by default Dublin 1
        if latitude is None or longitude is None:
            district = 'Dublin 1'
        else:
            district = find_nearest_district((float(latitude), float(longitude)))
            
        current = CurrentRepository.get_by_district(district)
        # If data is recent enough, return it
        if current and current.dt > (datetime.now() - timedelta(minutes=AUTO_WEATHER_UPDATE_INTERVAL)):
            weather = {}
            weather['current'] = current.as_dict()
            weather['hourly'] = [hourly.as_dict() for hourly in HourlyRepository.get_by_district(district)]
            weather['daily'] = [daily.as_dict() for daily in DailyRepository.get_by_district(district)]
            weather['alerts'] = [alerts.as_dict() for alerts in AlertsRepository.get_by_district(district)]
            return weather
        else:
            # If data is not recent enough, update it with external API call
            return WeatherService.get_current_weather_by_coordinate(latitude, longitude, district)
    
    @staticmethod
    def get_current_weather_by_coordinate(latitude, longitude, district=None):
        """
        Retrieves the current weather data for the specified coordinates from external API call.

        Args:
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
            district (str, optional): The district of the location, superior to latitude and longitude. Defaults to None.

        Returns:
            dict: A dictionary containing the current weather data.
        """
        
        if district is None:
            # If district is not provided, find the nearest district, by default Dublin 1
            if latitude is None or longitude is None:
                district = 'Dublin 1'
            else:
                district = find_nearest_district((float(latitude), float(longitude)))
        
        params = {
            "lat": OPEN_WEATHER_DUBLIN_LOC[district][0],
            "lon": OPEN_WEATHER_DUBLIN_LOC[district][1],
            "appid": OPEN_WEATHER_KEY,
            "exclude": "minutely"
        }
        r = requests.get(OPEN_WEATHER_URI, params=params)
        weather_information = json.loads(r.text)
        current_info = weather_information.get("current")
        hourly_info = weather_information.get("hourly")
        daily_info = weather_information.get("daily")
        alerts_info = weather_information.get("alerts")
        weather = {
            'hourly':[],
            'daily':[],
            'alerts':[]
        }
        hourly_data = []
        daily_data = []
        alerts_data = []
        
        if alerts_info is not None:
            for alerts_info_data in alerts_info:
                alerts_obj = Alerts(
                    district=district,
                    sender_name=alerts_info_data.get('sender_name'),
                    event=alerts_info_data.get('event'),
                    start_time=datetime.fromtimestamp(alerts_info_data.get('start')),
                    end_time=datetime.fromtimestamp(alerts_info_data.get('end')),
                    description=alerts_info_data.get('description'),
                    tags=alerts_info_data.get('tags')[0] if alerts_info_data.get('tags') else None
                )
                
                # Add to response
                weather['alerts'].append(alerts_obj.as_dict())
                alerts_data.append(alerts_obj)
                
        current_obj = Current(
            district=district,
            dt=datetime.fromtimestamp(current_info.get('dt')),
            sunrise=datetime.fromtimestamp(current_info.get('sunrise')),
            sunset=datetime.fromtimestamp(current_info.get('sunset')),
            temp=current_info.get('temp'),
            feels_like=current_info.get('feels_like'),
            pressure=current_info.get('pressure'),
            humidity=current_info.get('humidity'),
            dew_point=current_info.get('dew_point'),
            clouds=current_info.get('clouds'),
            uvi=current_info.get('uvi'),
            visibility=current_info.get('visibility'),
            wind_speed=current_info.get('wind_speed'),
            wind_gust=current_info.get('wind_gust'),
            wind_deg=current_info.get('wind_deg'),
            rain_1h=current_info.get('rain', {}).get('1h'),
            snow_1h=current_info.get('snow', {}).get('1h'),
            weather_id=current_info.get('weather')[0].get('id') if current_info.get('weather') else None,
            weather_main=current_info.get('weather')[0].get('main') if current_info.get('weather') else None,
            weather_description=current_info.get('weather')[0].get('description') if current_info.get('weather') else None,
            weather_icon=current_info.get('weather')[0].get('icon') if current_info.get('weather') else None
        )
        # Add to response
        weather['current'] = current_obj.as_dict()
        
        for hourly_info_data in hourly_info:
            hourly_obj = Hourly(
                district=district,
                dt=datetime.fromtimestamp(current_info.get('dt')),
                future_dt=datetime.fromtimestamp(hourly_info_data.get('dt')),
                temp=hourly_info_data.get('temp'),
                feels_like=hourly_info_data.get('feels_like'),
                pressure=hourly_info_data.get('pressure'),
                humidity=hourly_info_data.get('humidity'),
                dew_point=hourly_info_data.get('dew_point'),
                clouds=hourly_info_data.get('clouds'),
                uvi=hourly_info_data.get('uvi'),
                visibility=hourly_info_data.get('visibility'),
                wind_speed=hourly_info_data.get('wind_speed'),
                wind_gust=hourly_info_data.get('wind_gust'),
                wind_deg=hourly_info_data.get('wind_deg'),
                pop=hourly_info_data.get('pop'),
                rain_1h=current_info.get('rain', {}).get('1h'),
                snow_1h=current_info.get('snow', {}).get('1h'),
                weather_id=hourly_info_data.get('weather')[0].get('id') if hourly_info_data.get('weather') else None,
                weather_main=hourly_info_data.get('weather')[0].get('main') if hourly_info_data.get('weather') else None,
                weather_description=hourly_info_data.get('weather')[0].get('description') if hourly_info_data.get('weather') else None,
                weather_icon=hourly_info_data.get('weather')[0].get('icon') if hourly_info_data.get('weather') else None
            )
            
            # Add to response
            weather['hourly'].append(hourly_obj.as_dict())
            hourly_data.append(hourly_obj)
            
        for daily_info_data in daily_info:
            daily_obj = Daily(
                district=district,
                dt=datetime.fromtimestamp(current_info.get('dt')),
                future_dt=datetime.fromtimestamp(daily_info_data.get('dt')),
                sunrise=datetime.fromtimestamp(daily_info_data.get('sunrise')),
                sunset=datetime.fromtimestamp(daily_info_data.get('sunset')),
                moonrise=datetime.fromtimestamp(daily_info_data.get('moonrise')),
                moonset=datetime.fromtimestamp(daily_info_data.get('moonset')),
                moon_phase=daily_info_data.get('moon_phase'),
                summary=daily_info_data.get('summary'),
                temp_morn=daily_info_data.get('temp', {}).get('morn'),
                temp_day=daily_info_data.get('temp', {}).get('day'),
                temp_eve=daily_info_data.get('temp', {}).get('eve'),
                temp_night=daily_info_data.get('temp', {}).get('night'),
                temp_min=daily_info_data.get('temp', {}).get('min'),
                temp_max=daily_info_data.get('temp', {}).get('max'),
                feels_like_morn=daily_info_data.get('feels_like', {}).get('morn'),
                feels_like_day=daily_info_data.get('feels_like', {}).get('day'),
                feels_like_eve=daily_info_data.get('feels_like', {}).get('eve'),
                feels_like_night=daily_info_data.get('feels_like', {}).get('night'),
                pressure=daily_info_data.get('pressure'),
                humidity=daily_info_data.get('humidity'),
                dew_point=daily_info_data.get('dew_point'),
                wind_speed=daily_info_data.get('wind_speed'),
                wind_gust=daily_info_data.get('wind_gust'),
                wind_deg=daily_info_data.get('wind_deg'),
                clouds=daily_info_data.get('clouds'),
                uvi=daily_info_data.get('uvi'),
                pop=daily_info_data.get('pop'),
                rain=daily_info_data.get('rain'),
                snow=daily_info_data.get('snow'),
                weather_id=daily_info_data.get('weather')[0].get('id') if daily_info_data.get('weather') else None,
                weather_main=daily_info_data.get('weather')[0].get('main') if daily_info_data.get('weather') else None,
                weather_description=daily_info_data.get('weather')[0].get('description') if daily_info_data.get('weather') else None,
                weather_icon=daily_info_data.get('weather')[0].get('icon') if daily_info_data.get('weather') else None
            )
            
            # Add to response
            weather['daily'].append(daily_obj.as_dict())
            daily_data.append(daily_obj)
        
        # Create background task for database updates
        app = current_app._get_current_object()
        def update_database():
            with app.app_context():
                CurrentRepository.update_current(current_obj)
                for alerts_obj in alerts_data:
                    AlertsRepository.update_alerts(alerts_obj)
                for hourly_obj in hourly_data:
                    HourlyRepository.update_hourly(hourly_obj)
                for daily_obj in daily_data:
                    DailyRepository.update_daily(daily_obj)
                CurrentRepository.delete_old_current()
                AlertsRepository.delete_old_alerts()
                HourlyRepository.delete_old_hourly()
                DailyRepository.delete_old_daily()

        # Start the background thread
        Thread(target=update_database).start()

        return weather
    
def get_distance(coord1, coord2):
    """
    Calculates the distance between two coordinates using the Haversine formula.

    Args:
        coord1 (tuple): The first coordinate.
        coord2 (tuple): The second coordinate.

    Returns:
        float: The distance between the two coordinates in kilometers.
    """
    
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
    """
    Finds the nearest district to the specified coordinate.

    Args:
        coord1 (tuple): The coordinate.

    Returns:
        str: The nearest district.
    """
    
    min_distance = float('inf')
    nearest_district = None

    for district, coord2 in OPEN_WEATHER_DUBLIN_LOC.items():
        distance = get_distance(coord1, coord2)
        if distance < min_distance:
            min_distance = distance
            nearest_district = district

    return nearest_district