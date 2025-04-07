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
    """
    Initialize the database by creating the necessary tables.

    Args:
        engine: The database engine to use.

    Returns:
        None
    """
    
    sql = '''
    CREATE TABLE IF NOT EXISTS current(
    district VARCHAR(32),
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
    PRIMARY KEY (district, dt)
    );
    '''
    commit_sql(engine, sql)
    
    sql = '''
    CREATE TABLE IF NOT EXISTS hourly (
    district VARCHAR(32),
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
    PRIMARY KEY (district, dt, future_dt)
    );
    '''
    commit_sql(engine, sql)
    
    sql = '''
    CREATE TABLE IF NOT EXISTS daily (
    district VARCHAR(32),
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
    PRIMARY KEY (district, dt, future_dt)
    );
    '''
    commit_sql(engine, sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS alerts (
        district VARCHAR(32),
        sender_name VARCHAR(128),
        event VARCHAR(128),
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        description TEXT,
        tags VARCHAR(128),
        PRIMARY KEY (district, sender_name, event, start_time, end_time)
    );
    '''
    commit_sql(engine, sql)

def weather_data_scraper(engine):
    """
    Scrape weather data from the API and insert it into the database.

    Args:
        engine: The database engine to use.

    Returns:
        None
    """
    
    for district in OPEN_WEATHER_DUBLIN_LOC:
        params = {
            "lat": OPEN_WEATHER_DUBLIN_LOC[district][0],
            "lon": OPEN_WEATHER_DUBLIN_LOC[district][1],
            "appid": OPEN_WEATHER_KEY,
            "exclude": "minutely"
            # "exclude": "minutely, hourly, daily"
        }
        r = requests.get(OPEN_WEATHER_URI, params=params)
        weather_information = json.loads(r.text)
        current_info = weather_information.get("current")
        hourly_info = weather_information.get("hourly")
        daily_info = weather_information.get("daily")
        alerts_info = weather_information.get("alerts")
        if alerts_info is not None:
            for alerts_data in alerts_info:
                vals = {
                    'district': district,
                    'sender_name': alerts_data.get('sender_name'),
                    'event': alerts_data.get('event'),
                    'start_time': datetime.datetime.fromtimestamp(alerts_data.get('start')),
                    'end_time': datetime.datetime.fromtimestamp(alerts_data.get('end')),
                    'description': alerts_data.get('description'),
                    'tags': alerts_data.get('tags')[0] if alerts_data.get('tags') else None
                }
                sql = '''
                INSERT INTO alerts (
                    district,
                    sender_name,
                    event,
                    start_time,
                    end_time,
                    description,
                    tags
                ) VALUES (
                    :district,
                    :sender_name,
                    :event,
                    :start_time,
                    :end_time,
                    :description,
                    :tags
                ) ON DUPLICATE KEY UPDATE
                    description = VALUES(description),
                    tags = VALUES(tags);
                '''
                commit_sql(engine, sql, vals)
                
        
        vals = {
            'district': district,
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
            'visibility': current_info.get('visibility'),
            'wind_speed': current_info.get('wind_speed'),
            'wind_gust': current_info.get('wind_gust'),
            'wind_deg': current_info.get('wind_deg'),
            'rain_1h': current_info.get('rain',{}).get('1h'),
            'snow_1h': current_info.get('snow',{}).get('1h'),
            'weather_id': current_info.get('weather')[0].get('id') if current_info.get('weather') else None,
            'weather_main': current_info.get('weather')[0].get('main') if current_info.get('weather') else None,
            'weather_description': current_info.get('weather')[0].get('description') if current_info.get('weather') else None,
            'weather_icon': current_info.get('weather')[0].get('icon') if current_info.get('weather') else None
        }
        sql = """
        INSERT INTO current (district, dt, feels_like, humidity, pressure, sunrise, sunset, temp, uvi, weather_id, wind_gust, wind_speed, rain_1h, snow_1h, weather_main, weather_description, 
                clouds, weather_icon)
        VALUES (:district, :dt, :feels_like, :humidity, :pressure, :sunrise, :sunset, :temp, :uvi, :weather_id, :wind_gust, :wind_speed, :rain_1h, :snow_1h, :weather_main, :weather_description, 
                :clouds, :weather_icon)
        ON DUPLICATE KEY UPDATE
            feels_like = VALUES(feels_like), humidity = VALUES(humidity), pressure = VALUES(pressure),
            sunrise = VALUES(sunrise), sunset = VALUES(sunset), temp = VALUES(temp), uvi = VALUES(uvi),
            weather_id = VALUES(weather_id), wind_gust = VALUES(wind_gust), wind_speed = VALUES(wind_speed),
            rain_1h = VALUES(rain_1h), snow_1h = VALUES(snow_1h), weather_main = VALUES(weather_main),
            weather_description = VALUES(weather_description), clouds = VALUES(clouds), weather_icon = VALUES(weather_icon);
        """
        commit_sql(engine, sql, vals)
        
        for hourly_data in hourly_info:
            vals = {
                'district': district,
                'dt': datetime.datetime.fromtimestamp(current_info.get('dt')),
                'future_dt': datetime.datetime.fromtimestamp(hourly_data.get('dt')),
                'temp': hourly_data.get('temp'),
                'feels_like': hourly_data.get('feels_like'),
                'pressure': hourly_data.get('pressure'),
                'humidity': hourly_data.get('humidity'),
                'dew_point': hourly_data.get('dew_point'),
                'clouds': hourly_data.get('clouds'),
                'uvi': hourly_data.get('uvi'),
                'visibility': hourly_data.get('visibility'),
                'wind_speed': hourly_data.get('wind_speed'),
                'wind_gust': hourly_data.get('wind_gust'),
                'wind_deg': hourly_data.get('wind_deg'),
                'pop': hourly_data.get('pop'),
                'rain_1h': current_info.get('rain',{}).get('1h'),
                'snow_1h': current_info.get('snow',{}).get('1h'),
                'weather_id': hourly_data.get('weather')[0].get('id') if hourly_data.get('weather') else None,
                'weather_main': hourly_data.get('weather')[0].get('main') if hourly_data.get('weather') else None,
                'weather_description': hourly_data.get('weather')[0].get('description') if hourly_data.get('weather') else None,
                'weather_icon': hourly_data.get('weather')[0].get('icon') if hourly_data.get('weather') else None
            }
            sql = """
            INSERT INTO hourly (
                district, dt, future_dt, temp, feels_like, pressure, humidity, dew_point,
                clouds, uvi, visibility, wind_speed, wind_gust, wind_deg, pop, rain_1h,
                snow_1h, weather_id, weather_main, weather_description, weather_icon
            ) VALUES (
                :district, :dt, :future_dt, :temp, :feels_like, :pressure, :humidity, :dew_point,
                :clouds, :uvi, :visibility, :wind_speed, :wind_gust, :wind_deg, :pop, :rain_1h,
                :snow_1h, :weather_id, :weather_main, :weather_description, :weather_icon
            )
            ON DUPLICATE KEY UPDATE
                temp = VALUES(temp),
                feels_like = VALUES(feels_like),
                pressure = VALUES(pressure),
                humidity = VALUES(humidity),
                dew_point = VALUES(dew_point),
                clouds = VALUES(clouds),
                uvi = VALUES(uvi),
                visibility = VALUES(visibility),
                wind_speed = VALUES(wind_speed),
                wind_gust = VALUES(wind_gust),
                wind_deg = VALUES(wind_deg),
                pop = VALUES(pop),
                rain_1h = VALUES(rain_1h),
                snow_1h = VALUES(snow_1h),
                weather_id = VALUES(weather_id),
                weather_main = VALUES(weather_main),
                weather_description = VALUES(weather_description),
                weather_icon = VALUES(weather_icon);
            """
            commit_sql(engine, sql, vals)
        
        for daily_data in daily_info:
            vals = {
                'district': district,
                'dt': datetime.datetime.fromtimestamp(current_info.get('dt')),
                'future_dt': datetime.datetime.fromtimestamp(daily_data.get('dt')),
                'sunrise': datetime.datetime.fromtimestamp(daily_data.get('sunrise')),
                'sunset': datetime.datetime.fromtimestamp(daily_data.get('sunset')),
                'moonrise': datetime.datetime.fromtimestamp(daily_data.get('moonrise')),
                'moonset': datetime.datetime.fromtimestamp(daily_data.get('moonrise')),
                'moon_phase': daily_data.get('moon_phase'),
                'summary': daily_data.get('summary'),
                'temp_morn': daily_data.get('temp',{}).get('morn'),
                'temp_day': daily_data.get('temp',{}).get('day'),
                'temp_eve': daily_data.get('temp',{}).get('eve'),
                'temp_night': daily_data.get('temp',{}).get('night'),
                'temp_min': daily_data.get('temp',{}).get('min'),
                'temp_max': daily_data.get('temp',{}).get('max'),
                'feels_like_morn': daily_data.get('feels_like',{}).get('morn'),
                'feels_like_day': daily_data.get('feels_like',{}).get('day'),
                'feels_like_eve': daily_data.get('feels_like',{}).get('eve'),
                'feels_like_night': daily_data.get('feels_like',{}).get('night'),
                'pressure': daily_data.get('pressure'),
                'humidity': daily_data.get('humidity'),
                'dew_point': daily_data.get('dew_point'),
                'wind_speed': daily_data.get('wind_speed'),
                'wind_gust': daily_data.get('wind_gust'),
                'wind_deg': daily_data.get('wind_deg'),
                'clouds': daily_data.get('clouds'),
                'uvi': daily_data.get('uvi'),
                'pop': daily_data.get('pop'),
                'rain': daily_data.get('rain'),
                'snow': daily_data.get('snow'),
                'weather_id': daily_data.get('weather')[0].get('id') if daily_data.get('weather') else None,
                'weather_main': daily_data.get('weather')[0].get('main') if daily_data.get('weather') else None,
                'weather_description': daily_data.get('weather')[0].get('description') if daily_data.get('weather') else None,
                'weather_icon': daily_data.get('weather')[0].get('icon') if daily_data.get('weather') else None
            }
            
            sql = """
            INSERT INTO daily (
                district, dt, future_dt, sunrise, sunset, moonrise, moonset,
                moon_phase, summary, temp_morn, temp_day, temp_eve, temp_night,
                temp_min, temp_max, feels_like_morn, feels_like_day, feels_like_eve,
                feels_like_night, pressure, humidity, dew_point, wind_speed, wind_gust,
                wind_deg, clouds, uvi, pop, rain, snow, weather_id, weather_main,
                weather_description, weather_icon
            ) VALUES (
                :district, :dt, :future_dt, :sunrise, :sunset, :moonrise, :moonset,
                :moon_phase, :summary, :temp_morn, :temp_day, :temp_eve, :temp_night,
                :temp_min, :temp_max, :feels_like_morn, :feels_like_day, :feels_like_eve,
                :feels_like_night, :pressure, :humidity, :dew_point, :wind_speed, :wind_gust,
                :wind_deg, :clouds, :uvi, :pop, :rain, :snow, :weather_id, :weather_main,
                :weather_description, :weather_icon
            ) ON DUPLICATE KEY UPDATE
                sunrise = VALUES(sunrise),
                sunset = VALUES(sunset),
                moonrise = VALUES(moonrise),
                moonset = VALUES(moonset),
                moon_phase = VALUES(moon_phase),
                summary = VALUES(summary),
                temp_morn = VALUES(temp_morn),
                temp_day = VALUES(temp_day),
                temp_eve = VALUES(temp_eve),
                temp_night = VALUES(temp_night),
                temp_min = VALUES(temp_min),
                temp_max = VALUES(temp_max),
                feels_like_morn = VALUES(feels_like_morn),
                feels_like_day = VALUES(feels_like_day),
                feels_like_eve = VALUES(feels_like_eve),
                feels_like_night = VALUES(feels_like_night),
                pressure = VALUES(pressure),
                humidity = VALUES(humidity),
                dew_point = VALUES(dew_point),
                wind_speed = VALUES(wind_speed),
                wind_gust = VALUES(wind_gust),
                wind_deg = VALUES(wind_deg),
                clouds = VALUES(clouds),
                uvi = VALUES(uvi),
                pop = VALUES(pop),
                rain = VALUES(rain),
                snow = VALUES(snow),
                weather_id = VALUES(weather_id),
                weather_main = VALUES(weather_main),
                weather_description = VALUES(weather_description),
                weather_icon = VALUES(weather_icon);
            """
            commit_sql(engine, sql, vals)
        
        # wait for 2 seconds to avoid DoS, it should be fine
        time.sleep(2)
    
    

def main(database="LOCAL", no_echo=True, loop=False, scraper_interval=60*60):
    """
    Initialize the database connection and start the weather data scraper.

    Args:
        database (str): The database to use (default: 'LOCAL'). Options:
            - 'LOCAL': Use local database connection (LOCAL_DB_BIKES_URL).
            - 'REMOTE': Use local RDS database connection using SSH tunnel through EC2 (REMOTE_DB_BIKES_URL).
            - 'EC2': Use EC2 with RDS database connection (EC2_DB_BIKES_URL).
        no_echo (bool): Suppress SQL echo output (default: True).
        loop (bool): Continuously scrape data in a loop (default: False).
        scraper_interval (int): Interval between scrapes in seconds (default: 3600).

    Returns:
        None
    """
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
    """
    Run the weather data scraper.

    To run with SSH tunnel through EC2:
        python database_oneday_data/weather_scraper.py --database 'REMOTE' --scraper_interval 3600 --no_echo --loop
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    parser.add_argument('--scraper_interval', type=int, action='store', default=60*60)
    parser.add_argument('--no_echo', action='store_true')
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()
    main(args.database, args.no_echo, args.loop, args.scraper_interval)