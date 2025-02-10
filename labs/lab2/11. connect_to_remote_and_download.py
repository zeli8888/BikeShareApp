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
import traceback
import datetime
import time
import os
import dbinfo
from python_basic_db import new_engine_connection

##############Function to import from JCDecaux API##########

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
        
        

######################Let us connect to the DB

USER = "..."
PASSWORD = "..."
PORT = "3306"
DB = "...db name..."
URI = "...remote uri..."

connection_string = "mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)

engine = create_engine(connection_string, echo = True)

sql = """
CREATE DATABASE IF NOT EXISTS databasejc;
"""
# engine.execute(sql)
new_engine_connection(engine, sql)
new_engine_connection(engine, "databasejc")

#############Let us create the table############

# sql = '''
# CREATE TABLE IF NOT EXISTS station (
# address VARCHAR(256), 
# banking INTEGER,
# bikestands INTEGER,
# name VARCHAR(256),
# status VARCHAR(256));
# '''

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

# Execute the query
# res = engine.execute(sql)
res = new_engine_connection(engine, sql)

# Use the engine to execute the DESCRIBE command to inspect the table schema
# tab_structure = engine.execute("SHOW COLUMNS FROM station;")
tab_structure = new_engine_connection(engine, "SHOW COLUMNS FROM station;")

# Fetch and print the result to see the columns of the table
columns = tab_structure.fetchall()
print(columns)

##############Let us Run the request

try:
    r = requests.get(dbinfo.STATIONS_URI, params={"apiKey": dbinfo.JCKEY, "contract": dbinfo.NAME})
    stations_to_db(r.text, engine)
    
    # let us see if we have stuff
    # res = engine.execute("SELECT * FROM station")
    res = new_engine_connection(engine, "SELECT * FROM station")
    rows = res.fetchall()
    print(rows) 
except:
    print(traceback.format_exc())


        
    

    

 