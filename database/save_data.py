import pandas as pd
import argparse
from config import *
from usage import *

def save_bike_data(engine, table):
    sql = f'''SELECT * FROM {table}'''
    df = pd.read_sql_query(sql, engine)
    df.to_csv(f'./database/{table}.csv')
    
def main(database="LOCAL"):
    engine = get_mysql_engine(database, True)
    try:
        for table in ['station', 'availability', 
                      'alerts', 'current', 'daily', 'hourly']:
            save_bike_data(engine, table)
    except:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    # to run: 
    # python save_data.py --database 'REMOTE'
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    args = parser.parse_args()
    main(args.database)