import requests
import traceback
import datetime
import time
import os
import dbinfo
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display
from python_basic_db import new_engine_connection


def stations_to_db(text, in_engine):
    # let us load the stations from the text received from jcdecaux
    stations = json.loads(text)

    # print type of the stations object, and number of stations
    print(type(stations), len(stations))
    
    # let us print the type of the object stations (a dictionary) and load the content
    for station in stations:
        print(type(station))

        # let us load only the parts that we have included in our db:
        # address VARCHAR(256), 
        # banking INTEGER,
        # bikestands INTEGER,
        # name VARCHAR(256),
        # status VARCHAR(256))
        
        # let us extract the relevant info from the dictionary
        # vals = (station.get('address'), int(station.get('banking')), int(station.get('bike_stands')), 
        #         station.get('name'), station.get('status'))
        vals = {
            'address': station.get('address'),
            'banking': int(station.get('banking')),
            'bike_stands': int(station.get('bike_stands')),
            'name': station.get('name'),
            'status': station.get('status')
        }
        

        # now let us use the engine to insert into the stations
        # in_engine.execute("""
        #                   INSERT INTO station (address, banking, bikestands, name, status) 
        #                   VALUES (%s, %s, %s, %s, %s);
        #                   """, vals)
        new_engine_connection(in_engine, """
                          INSERT INTO station (address, banking, bike_stands, name, status) 
                          VALUES (:address, :banking, :bike_stands, :name, :status);
                          """, vals)


def main():
    USER = "root"
    PASSWORD = "as5071565"
    PORT = "3306"
    DB = "local_databasejcdecaux"
    URI = "127.0.0.1"

    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)

    engine = create_engine(connection_string, echo = True)
    new_engine_connection(engine, "USE {};".format(DB))

    try:
        r = requests.get(dbinfo.STATIONS_URI, params={"apiKey": dbinfo.JCKEY, "contract": dbinfo.NAME})
        stations_to_db(r.text, engine)
        time.sleep(5*60)
    except:
        print(traceback.format_exc())

# CTRL + Z or CTRL + C to stop it
main()   