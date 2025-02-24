from sqlalchemy import text
from sqlalchemy import create_engine
import traceback
# This is import from project directory, so any file import this should have project directory in its system path
from web.src.config import *
from math import radians, sin, cos, sqrt, atan2


def get_mysql_engine(database="LOCAL", no_echo=False):
    if database != "LOCAL" and database != "REMOTE":
        raise Exception("Invalid database choice, choose either LOCAL or REMOTE!")
    if no_echo != True and no_echo != False:
        raise Exception("Invalid echo option, choose either True or False!")
    
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(
        globals()[database+"_USER"], 
        globals()[database+"_PASSWORD"], 
        globals()[database+"_URI"], 
        globals()[database+"_PORT"], 
        globals()[database+"_DB"]
    )
    engine = create_engine(connection_string, echo = not no_echo)
    commit_sql(engine, "CREATE DATABASE IF NOT EXISTS {};".format(globals()[database+"_DB"]))
    commit_sql(engine, "USE {};".format(globals()[database+"_DB"]))
    return engine

def commit_sql(engine, sql, val=None):
    if val is None:
        with engine.connect() as connection:
            try:
                transaction = connection.begin()
                res = connection.execute(text(sql))
                transaction.commit()
                return res
            except Exception as e:
                traceback.print_exc()
                connection.rollback()
    else:
        with engine.connect() as connection:
            try:
                transaction = connection.begin()
                res = connection.execute(text(sql), val)
                transaction.commit()
                return res
            except Exception as e:
                traceback.print_exc()
                connection.rollback()
                
def get_distance(coord1, coord2):
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