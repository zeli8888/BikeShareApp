from sqlalchemy import text
from sqlalchemy import create_engine
import traceback
from config import *


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