import os
import sys
# Append the project directory to the system path
sys.path.append(os.path.abspath(''))

import pandas as pd
import argparse
from web.src.config import *
from usage import *

def save_table_data(engine, table):
    """
    Saves data from a MySQL table to a CSV file.

    Args:
        engine: A SQLAlchemy engine instance.
        table (str): The name of the table to save data from.

    Returns:
        None
    """
    
    sql = f'''SELECT * FROM {table}'''
    df = pd.read_sql_query(sql, engine)
    df.to_csv(f'./database/{table}.csv', index=False)
    
def main(database="LOCAL"):
    """
    Saves data from MySQL tables to CSV files for the specified database.

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
            save_table_data(engine, table)
    except:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    """
    Entry point for the script.

    To run with SSH tunnel through EC2:
        python database_oneday_data/save_data.py --database 'REMOTE'
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    args = parser.parse_args()
    main(args.database)