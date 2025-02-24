import os
import sys
# Append the project directory to the system path
sys.path.append(os.path.abspath(''))
    
from web.src.config import *
from usage import *
import requests
import argparse
import time
import simplejson as json
import datetime

def database_initialization(engine):
    sql = '''
    CREATE TABLE IF NOT EXISTS station (
    number INTEGER NOT NULL, 
    address VARCHAR(128), 
    banking INTEGER, 
    bike_stands INTEGER, 
    name VARCHAR(128), 
    position_lat FLOAT, 
    position_lng FLOAT, 
    PRIMARY KEY (number)
    );
    '''
    # bonus INTEGER
    commit_sql(engine, sql)
    
    sql = """
    CREATE TABLE IF NOT EXISTS availability (
        number INTEGER NOT NULL,
        last_update DATETIME NOT NULL,
        available_bikes INTEGER,
        available_bike_stands INTEGER,
        status VARCHAR(128),
        PRIMARY KEY (number, last_update),
        FOREIGN KEY (number) REFERENCES station(number)
    );
    """
    commit_sql(engine, sql)
    

def bike_data_scraper(engine, non_static=True):
    r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})
    stations = json.loads(r.text)
    for station in stations:
        if not non_static:
            vals = {
                'number': station.get('number'),
                'address': station.get('address'),
                'banking': int(station.get('banking')),
                'bike_stands': int(station.get('bike_stands')),
                'name': station.get('name'),
                'position_lat': station.get('position').get('lat'),
                'position_lng': station.get('position').get('lng')
            }
            sql = """
            INSERT INTO station (number, address, banking, bike_stands, name, position_lat, position_lng)
            VALUES (:number, :address, :banking, :bike_stands, :name, :position_lat, :position_lng)
            ON DUPLICATE KEY UPDATE
                address = VALUES(address),
                banking = VALUES(banking),
                bike_stands = VALUES(bike_stands),
                name = VALUES(name),
                position_lat = VALUES(position_lat),
                position_lng = VALUES(position_lng);
            """
            commit_sql(engine, sql, vals)
        
        vals = {
            'number': station.get('number'),
            'last_update': datetime.datetime.fromtimestamp(station.get('last_update')/1000),
            'available_bikes': station.get('available_bikes'),
            'available_bike_stands': station.get('available_bike_stands'),
            'status': station.get('status')
        }
        sql = """
        INSERT INTO availability (number, last_update, available_bikes, available_bike_stands, status)
        VALUES (:number, :last_update, :available_bikes, :available_bike_stands, :status)
        ON DUPLICATE KEY UPDATE
            available_bikes = VALUES(available_bikes),
            available_bike_stands = VALUES(available_bike_stands),
            status = VALUES(status);
        """
        commit_sql(engine, sql, vals)

def main(database="LOCAL", no_echo=True, loop=False, scraper_interval=5*60):
    engine = get_mysql_engine(database, no_echo)
    database_initialization(engine)

    try:
        bike_data_scraper(engine, non_static=False)
        while loop:
            time.sleep(scraper_interval)
            bike_data_scraper(engine)
    except:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    # to run: 
    # python database/bike_scraper.py --database 'REMOTE' --scraper_interval 300 --no_echo --loop
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    parser.add_argument('--scraper_interval', type=int, action='store', default=5*60)
    parser.add_argument('--no_echo', action='store_true')
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()
    main(args.database, args.no_echo, args.loop, args.scraper_interval)