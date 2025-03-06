from ..repository import StationRepository, AvailabilityRepository
from ..model import Station, Availability
from ..config import STATIONS_URI, JCKEY, NAME, AUTO_BIKES_UPDATE_INTERVAL, DAILY_DATA_DATE
import requests
import simplejson as json
from datetime import datetime, timedelta
from threading import Thread
from flask import current_app
class BikesService:
    @staticmethod
    def get_all_bikes():
        """
        Retrieve all stations' bikes.
        """
        availabilities = AvailabilityRepository.get_latest_availabilities()
        
        if availabilities and availabilities[0].last_update > (datetime.now() - timedelta(minutes=AUTO_BIKES_UPDATE_INTERVAL)):
            bikes = {}
            bikes['availabilities'] = [availability.as_dict() for availability in availabilities]
            bikes['stations'] = [station.as_dict() for station in StationRepository.get_all_stations()]
            return bikes
        else:
            return BikesService.get_all_current_bikes()

    @staticmethod
    def get_all_current_bikes():
        """
        Retrieve all stations' current bikes.
        Async Service!
        Will return data to frontend first, then store into database.
        """
        r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})
        stations = json.loads(r.text)
        
        bikes = {'stations': [], 'availabilities': []}
        stations_data = []
        availabilities_data = []

        for station in stations:
            station_obj = Station(
                number=station['number'],
                address=station['address'],
                banking=int(station['banking']),
                bike_stands=int(station['bike_stands']),
                name=station['name'],
                position_lat=station['position']['lat'],
                position_lng=station['position']['lng']
            )
            
            availability_obj = Availability(
                number=station.get('number'),
                last_update=datetime.fromtimestamp(station.get('last_update')/1000),
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
            with app.app_context():
                for station_obj, availability_obj in zip(stations_data, availabilities_data):
                    StationRepository.update_station(station_obj)
                    AvailabilityRepository.update_availability(availability_obj)
                AvailabilityRepository.delete_old_availabilities(DAILY_DATA_DATE)

        # Start the background thread
        Thread(target=update_database).start()

        return bikes