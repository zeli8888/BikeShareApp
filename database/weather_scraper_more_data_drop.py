from config import *
import requests
from usage import *
import argparse
import time
import simplejson as json
import datetime

def database_initialization(engine):
    sql = '''
    CREATE TABLE IF NOT EXISTS current(
    dt DATETIME NOT NULL, 
    sunrise DATETIME, 
    sunset DATETIME, 
    temp FLOAT, 
    feels_like FLOAT, 
    pressure INTEGER, 
    humidity INTEGER, 
    dew_point FLOAT,
    clouds INTEGER,
    uvi FLOAT, 
    visibility INTEGER,
    wind_speed FLOAT, 
    wind_gust FLOAT, 
    wind_deg INTEGER,
    rain_1h FLOAT, 
    snow_1h FLOAT, 
    weather_id INTEGER, 
    weather_main VARCHAR(128),
    weather_description VARCHAR(128),
    weather_icon VARCHAR(32),
    PRIMARY KEY (dt)
    );
    '''
    res = commit_sql(engine, sql)
    
    sql = '''
    CREATE TABLE hourly (
    dt DATETIME NOT NULL, 
    future_dt DATETIME NOT NULL, 
    temp FLOAT, 
    feels_like FLOAT, 
    pressure INTEGER, 
    humidity INTEGER, 
    dew_point FLOAT,
    clouds INTEGER,
    uvi FLOAT, 
    visibility INTEGER,
    wind_speed FLOAT, 
    wind_gust FLOAT, 
    wind_deg INTEGER,
    pop FLOAT,
    rain_1h FLOAT, 
    snow_1h FLOAT, 
    weather_id INTEGER, 
    weather_main VARCHAR(128),
    weather_description VARCHAR(128),
    weather_icon VARCHAR(32),
    PRIMARY KEY (dt, future_dt)
    );
    '''
    res = commit_sql(engine, sql)
    
    sql = '''
    CREATE TABLE IF NOT EXISTS daily (
    dt DATETIME NOT NULL, 
    future_dt DATETIME NOT NULL, 
    sunrise DATETIME, 
    sunset DATETIME, 
    moonrise DATETIME,
    moonset DATETIME,
    moon_phase FLOAT,
    summary VARCHAR(256),
    temp_morn FLOAT, 
    temp_day FLOAT, 
    temp_eve FLOAT, 
    temp_night FLOAT, 
    temp_min FLOAT, 
    temp_max FLOAT, 
    feels_like_morn FLOAT, 
    feels_like_day FLOAT, 
    feels_like_eve FLOAT, 
    feels_like_night FLOAT, 
    pressure INTEGER, 
    humidity INTEGER, 
    dew_point FLOAT,
    wind_speed FLOAT, 
    wind_gust FLOAT, 
    wind_deg INTEGER,
    clouds INTEGER,
    uvi FLOAT, 
    pop FLOAT,
    rain FLOAT, 
    snow FLOAT, 
    weather_id INTEGER, 
    weather_main VARCHAR(128),
    weather_description VARCHAR(128),
    weather_icon VARCHAR(32),
    PRIMARY KEY (dt, future_dt)
    );
    '''
    res = commit_sql(engine, sql)


def weather_data_scraper(engine):
    params = {
        "lat": OPEN_WEATHER_DUBLIN_LOC[0],
        "lon": OPEN_WEATHER_DUBLIN_LOC[1],
        "appid": OPEN_WEATHER_KEY,
        "exclude": "minutely"
        # "exclude": "minutely, hourly, daily"
    }
    r = requests.get(OPEN_WEATHER_URI, params=params)
    weather_information = json.loads(r.text)
    current_info = weather_information["current"]
    hourly_info = weather_information["hourly"]
    daily_info = weather_information["daily"]
    vals = {
        'dt': datetime.datetime.fromtimestamp(current_info.get('dt')),
        'sunrise': datetime.datetime.fromtimestamp(current_info.get('sunrise')),
        'sunset': datetime.datetime.fromtimestamp(current_info.get('sunset')),
        'temp': current_info.get('temp'),
        'feels_like': current_info.get('feels_like'),
        'pressure': current_info.get('pressure'),
        'humidity': current_info.get('humidity'),
        'dew_point': current_info.get('dew_point'),
        'clouds': current_info.get('clouds'),
        'uvi': current_info.get('uvi'),
        'visibility': 1,
        # some attributes are based on position, for example, visibility, this actually wont work
        'weather_id': current_info.get('weather')[0].get('id'),
        'wind_gust': current_info.get('wind_gust'),
        'wind_speed': current_info.get('wind_speed'),
        'rain_1h': current_info.get('rain_1h'),
        'snow_1h': current_info.get('snow_1h'),
        'main': current_info.get('weather')[0].get('main'),
        'description': current_info.get('weather')[0].get('description'),
        'icon': current_info.get('weather')[0].get('icon')
    }
    sql = """
    INSERT INTO current (dt, feels_like, humidity, pressure, sunrise, sunset, temp, uvi, weather_id, wind_gust, wind_speed, rain_1h, snow_1h, main, description, 
            clouds, icon)
    VALUES (:dt, :feels_like, :humidity, :pressure, :sunrise, :sunset, :temp, :uvi, :weather_id, :wind_gust, :wind_speed, :rain_1h, :snow_1h, :main, :description, 
            :clouds, :icon)
    ON DUPLICATE KEY UPDATE
        feels_like = VALUES(feels_like), humidity = VALUES(humidity), pressure = VALUES(pressure),
        sunrise = VALUES(sunrise), sunset = VALUES(sunset), temp = VALUES(temp), uvi = VALUES(uvi),
        weather_id = VALUES(weather_id), wind_gust = VALUES(wind_gust), wind_speed = VALUES(wind_speed),
        rain_1h = VALUES(rain_1h), snow_1h = VALUES(snow_1h), main = VALUES(main),
        description = VALUES(description), clouds = VALUES(clouds), icon = VALUES(icon);
    """
    commit_sql(engine, sql, vals)
    
    

def main(database="LOCAL", no_echo=True, loop=False, scraper_interval=60*60):
    engine = get_mysql_engine(database, no_echo)
    database_initialization(engine)
    
    try:
        weather_data_scraper(engine)
    except:
        print(traceback.format_exc())
    while loop:
        try:
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