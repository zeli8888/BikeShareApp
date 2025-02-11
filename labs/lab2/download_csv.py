from sqlalchemy import create_engine
import labs.lab2.db_config as db_config
import pandas as pd
import os
import db_config

tablename='your_table'
# read the parameters from a db_config.py file
engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(db_config.USER,
                                                                          db_config.PASSWORD,
                                                                          db_config.DB_URI,
                                                                          db_config.PORT,
                                                                          db_config.DB))

def get_csv(table_name):
	# if csv files exists, read csv and return df
	csv_fname = f"{tablename}.csv"

	if os.path.exists(csv_fname):
		df = pd.read_csv(csv_fname)
		return df
	else:
		df = pd.read_sql_table(table_name, engine)
		df.to_csv(csv_fname)
		return df