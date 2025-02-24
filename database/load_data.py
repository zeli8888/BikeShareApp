import os
import sys
# Append the project directory to the system path
sys.path.append(os.path.abspath(''))

import pandas as pd
import argparse
from web.config import *
from web.src.repository.usage import *

def load_table_data(engine, table):
    df = pd.read_csv(f'./database/{table}.csv')
    df.to_sql(f'{table}', engine, if_exists='append', index=False, method='multi', chunksize=1000)
    
def main(database="LOCAL"):
    engine = get_mysql_engine(database, True)
    try:
        for table in ['station', 'availability', 
                      'alerts', 'current', 'daily', 'hourly']:
            load_table_data(engine, table)
    except:
        print(traceback.format_exc())
        
if __name__ == "__main__":
    # to run: 
    # python load_data.py --database 'REMOTE'
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, action='store', default='LOCAL')
    args = parser.parse_args()
    main(args.database)