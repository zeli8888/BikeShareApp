from sqlalchemy import text
from sqlalchemy import create_engine
import traceback
from web.src.config import *
from math import radians, sin, cos, sqrt, atan2


def get_mysql_engine(database="LOCAL", no_echo=False):
    """
    Creates a MySQL engine instance based on the provided database name and echo option.

    Args:
        database (str): The database to use (default: 'LOCAL'). Options:
            - 'LOCAL': Use local database connection (LOCAL_DB_BIKES_URL).
            - 'REMOTE': Use local RDS database connection using SSH tunnel through EC2 (REMOTE_DB_BIKES_URL).
            - 'EC2': Use EC2 with RDS database connection (EC2_DB_BIKES_URL).
        no_echo (bool): Whether to suppress SQL echoing (default: False).

    Returns:
        engine: A SQLAlchemy engine instance.

    Raises:
        Exception: If the database choice is invalid or the echo option is not a boolean.
    """
    
    if os.getenv(f'{database}_DB_BIKES_URL') is None:
        raise Exception(f"Invalid database choice, check your system variable for {database}_DB_BIKES_URL!")
    if no_echo != True and no_echo != False:
        raise Exception("Invalid echo option, choose either True or False!")
    
    connection_string = os.getenv(f'{database}_DB_BIKES_URL')
    
    engine = create_engine(connection_string, echo = not no_echo)
    # commit_sql(engine, "CREATE DATABASE IF NOT EXISTS {};".format(globals()[database+"_DB"]))
    # commit_sql(engine, "USE {};".format(globals()[database+"_DB"]))
    return engine

def commit_sql(engine, sql, val=None):
    """
    Commits a SQL query to the database using the provided engine.

    Args:
        engine: A SQLAlchemy engine instance.
        sql (str): The SQL query to execute.
        val (tuple, optional): Values to bind to the SQL query (default: None).

    Returns:
        result: The result of the SQL query execution.

    Raises:
        Exception: If the SQL query execution fails.
    """
    
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