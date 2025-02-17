from sqlalchemy import text
from sqlalchemy import create_engine
import traceback

def get_mysql_engine(database="LOCAL", echo=True):
    if database != "LOCAL" | database != "REMOTE":
        raise Exception("Invalid database choice, choose either LOCAL or REMOTE!")
    if echo != True | echo != False:
        raise Exception("Invalid echo option, choose either True or False!")
    
    connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(
        database+"_USER", database+"_PASSWORD", database+"_URI", database+"_PORT", database+"_DB")
    engine = create_engine(connection_string, echo = echo)
    commit_sql(engine, "USE {};".format(database+"_DB"))
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