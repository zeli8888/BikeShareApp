import dbinfo
import requests
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine, text
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import time
from IPython.display import display

def new_engine_connection(engine, sql, val=None):
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

if __name__ == "__main__":
    USER = "root"
    PASSWORD = "as5071565"
    PORT = "3306"
    DB = "local_databasejcdecaux"
    URI = "127.0.0.1"

    connection_string = "mysql+pymysql://{}:{}@{}:{}".format(USER, PASSWORD, URI, PORT)

    engine = create_engine(connection_string, echo = True)

    sql = """
    CREATE DATABASE IF NOT EXISTS {};
    """.format(DB)

    # engine.execute(sql)
    new_engine_connection(engine, sql)
    new_engine_connection(engine, "USE {};".format(DB))

    # for res in engine.execute("SHOW VARIABLES;"):
    #     print(res)

    for res in new_engine_connection(engine, sql="SHOW VARIABLES;"):
        print(res)
