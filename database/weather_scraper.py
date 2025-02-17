from config import *
import requests
from usage import *
import argparse
import time
import simplejson as json
import datetime

def database_initialization(engine):
    sql = '''
    CREATE TABLE IF NOT EXISTS weather (
    dt DATETIME,
    temp DECIMAL(10, 2),
    feels_like DECIMAL(10, 2),
    pressure INT,
    humidity INT,
    uvi DECIMAL(10, 2),
    clouds INT,
    visibility INT,
    wind_speed DECIMAL(10, 2),
    wind_deg INT,
    main_weather VARCHAR(255),
    description VARCHAR(255)
    );
    '''
    res = commit_sql(engine, sql)
    

def weather_data_scraper(engine):
    params = {
        "lat": OPEN_WEATHER_DUBLIN_LOC[0],
        "lon": OPEN_WEATHER_DUBLIN_LOC[1],
        "appid": OPEN_WEATHER_KEY,
        "exclude": "minutely, hourly, daily"
    }
    r = requests.get(OPEN_WEATHER_URI, params=params)
    weather_info = json.loads(r.text)["current"]
    # dt, temp, feels_like, pressure, humidity, uvi, clouds, visibility, wind_speed, wind_deg, weather
    # weather: main, description
    weather_info['dt'] = datetime.datetime.fromtimestamp(weather_info['dt'])
    weather_info['main_weather'] = weather_info['weather'][0]['main']
    weather_info['description'] = weather_info['weather'][0]['description']
    sql = """
    INSERT INTO weather (dt, temp, feels_like, pressure, humidity, uvi, clouds, visibility, wind_speed, wind_deg, main_weather, description) 
    VALUES (:dt, :temp, :feels_like, :pressure, :humidity, :uvi, :clouds, :visibility, :wind_speed, :wind_deg, :main_weather, :description);
    """
    commit_sql(engine, sql, weather_info)

def main(database="LOCAL", no_echo=True, loop=False, scraper_interval=60*60):
    engine = get_mysql_engine(database, no_echo)
    database_initialization(engine)
    
    try:
        weather_data_scraper(engine)
        while loop:
            time.sleep(scraper_interval)
            weather_data_scraper(engine)
    except:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    # to run: 
    # python weather_scraper.py --database 'REMOTE' --scraper_interval 3600 --no_echo --loop
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    parser.add_argument('--scraper_interval', type=int, action='store', default=60*60)
    parser.add_argument('--no_echo', action='store_true')
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()
    main(args.database, args.no_echo, args.loop, args.scraper_interval)