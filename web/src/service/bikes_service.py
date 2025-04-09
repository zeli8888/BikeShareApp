from ..repository import StationRepository, AvailabilityRepository
from ..model import Station, Availability
from ..config import STATIONS_URI, JCKEY, NAME, AUTO_BIKES_UPDATE_INTERVAL, DAILY_DATA_DATE
import requests
import simplejson as json
from datetime import datetime, timedelta
from threading import Thread
from flask import current_app
class BikesService:
    """
    Represents a service for managing bike data involving stations and availability.

    Methods:
        get_all_bikes(): Retrieves all stations' bikes, if it's too old, update it.
        get_all_current_bikes(): Retrieves all stations' current bikes from external API call.
        get_one_day_availability(): Retrieves all availability data for the specified day.
        get_one_day_availability_for_station(station_id): Retrieves all availability data for the specified station and day.
    """
    
    @staticmethod
    def get_all_bikes():
        """
        Retrieves all stations' bikes, if it's too old, update it.

        Returns:
            dict: A dictionary containing the latest availability data and station information.
        """
        availabilities = AvailabilityRepository.get_latest_availabilities()
        
        # If data is recent enough, return it
        if availabilities and availabilities[0].last_update > (datetime.now() - timedelta(minutes=AUTO_BIKES_UPDATE_INTERVAL)):
            bikes = {}
            bikes['availabilities'] = [availability.as_dict() for availability in availabilities]
            bikes['stations'] = [station.as_dict() for station in StationRepository.get_all_stations()]
            return bikes
        else:
            # If data is not recent enough, update it with external API call
            return BikesService.get_all_current_bikes()

    @staticmethod
    def get_all_current_bikes():
        """
        Retrieves all stations' current bikes from external API call.

        Using Async Service, return data to frontend while starting a new thread to store data into database.

        Returns:
            dict: A dictionary containing the current availability data and station information.
        """
        r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})
        stations = json.loads(r.text)
        
        bikes = {'stations': [], 'availabilities': []}
        stations_data = []
        availabilities_data = []

        for station in stations:
            station_obj = Station(
                number=station.get('number'),
                address=station.get('address'),
                banking=int(station.get('banking', 0)),
                bike_stands=int(station.get('bike_stands', 0)),
                name=station.get('name'),
                position_lat=station.get('position', {}).get('lat'),
                position_lng=station.get('position', {}).get('lng')
            )
            
            availability_obj = Availability(
                number=station.get('number'),
                last_update=datetime.fromtimestamp(station.get('last_update')/1000) if 'last_update' in station else None,
                available_bikes=station.get('available_bikes'),
                available_bike_stands=station.get('available_bike_stands'),
                status=station.get('status')
            )
            
            # Add to response
            bikes['stations'].append(station_obj.as_dict())
            bikes['availabilities'].append(availability_obj.as_dict())
            stations_data.append(station_obj)
            availabilities_data.append(availability_obj)
            
        # Create background task for database updates
        app = current_app._get_current_object()
        def update_database():
            try:
                with app.app_context():
                    for station_obj, availability_obj in zip(stations_data, availabilities_data):
                        StationRepository.update_station(station_obj)
                        AvailabilityRepository.update_availability(availability_obj)
                    AvailabilityRepository.delete_old_availabilities(DAILY_DATA_DATE)
            except Exception as e:
                # with cases of multiple users, the database may already be updated.
                # in that case, the exception will happen due to the primary key constraint.
                # we can safely return because database is already updated by other process.
                return

        # Start the background thread
        Thread(target=update_database).start()

        return bikes
    
    @staticmethod
    def get_one_day_availability():
        """
        Retrieves all availability data for the specified day.

        Returns:
            list[dict]: A list of dictionaries representing the availability data for the specified day.
        """
        return [availability.as_dict() for availability in AvailabilityRepository.get_one_day_availability(DAILY_DATA_DATE)]
    
    @staticmethod
    def get_one_day_availability_for_station(station_id):
        """
        Retrieves all availability data for the specified station and day.

        Args:
            station_id (int): The ID of the station for which to retrieve availability data.

        Returns:
            list[dict]: A list of dictionaries representing the availability data for the specified station and day.
        """
        return [availability.as_dict() for availability in AvailabilityRepository.get_one_day_availability_for_station(DAILY_DATA_DATE, station_id)]