from config import *
import requests
from usage import *
import argparse
import time
import simplejson as json

def database_initialization(engine):
    sql = '''
    CREATE TABLE IF NOT EXISTS station (
    address VARCHAR(256), 
    banking INTEGER,
    bike_stands INTEGER,
    bonus INTEGER,
    contract_name VARCHAR(256),
    name VARCHAR(256),
    number INTEGER,
    position_lat REAL,
    position_lng REAL,
    status VARCHAR(256));
    '''
    res = commit_sql(engine, sql)
    
    sql = """
    CREATE TABLE IF NOT EXISTS availability (
    number INTEGER,
    available_bikes INTEGER,
    available_bike_stands INTEGER,
    last_update DATETIME
    );
    """
    res = commit_sql(engine, sql)
    

def bike_data_scraper(engine):
    r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})
    stations = json.loads(r.text)
    for station in stations:
        vals = {
            'address': station.get('address'),
            'banking': int(station.get('banking')),
            'bike_stands': int(station.get('bike_stands')),
            'name': station.get('name'),
            'status': station.get('status')
        }
        sql = """
        INSERT INTO station (address, banking, bike_stands, name, status) 
        VALUES (:address, :banking, :bike_stands, :name, :status);
        """
        commit_sql(engine, sql, vals)

def main(database="LOCAL", no_echo=True, loop=False, scraper_interval=5*60):
    engine = get_mysql_engine(database, no_echo)
    database_initialization(engine)
    
    try:
        bike_data_scraper(engine)
        while loop:
            time.sleep(scraper_interval)
            bike_data_scraper(engine)
    except:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    # to run: 
    # python bike_scraper.py --database 'REMOTE' --scraper_interval 300 --no_echo --loop
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    parser.add_argument('--scraper_interval', type=int, action='store', default=5*60)
    parser.add_argument('--no_echo', action='store_true')
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()
    main(args.database, args.no_echo, args.loop, args.scraper_interval)