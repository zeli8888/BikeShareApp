import os
import sys
# Append the project directory to the system path
sys.path.append(os.path.abspath(''))

import pandas as pd
import argparse
from web.src.config import *
from usage import *

def load_table_data(engine, table):
    """
    Loads data from a CSV file into a MySQL table.

    Args:
        engine: A SQLAlchemy engine instance.
        table (str): The name of the table to load data into.

    Returns:
        None
    """
    df = pd.read_csv(f'./database/{table}.csv')
    df.to_sql(f'{table}', engine, if_exists='append', index=False, method='multi', chunksize=1000)
    
def main(database="LOCAL"):
    """
    Loads data into MySQL tables for the specified database.
    Note: This function will not add constraints such as primary keys to the tables, so make sure to run the project first to create tables before loading data to database.

    Args:
        database (str): The database to use (default: 'LOCAL'). Options:
            - 'LOCAL': Use local database connection (LOCAL_DB_BIKES_URL).
            - 'REMOTE': Use local RDS database connection using SSH tunnel through EC2 (REMOTE_DB_BIKES_URL).
            - 'EC2': Use EC2 with RDS database connection (EC2_DB_BIKES_URL).

    Returns:
        None
    """
    engine = get_mysql_engine(database, True)
    try:
        for table in ['station', 'availability', 
                      'alerts', 'current', 'daily', 'hourly']:
            load_table_data(engine, table)
    except:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    """
    Entry point for the script.

    To run with SSH tunnel through EC2:
        python database_oneday_data/load_data.py --database 'REMOTE'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    args = parser.parse_args()
    main(args.database)