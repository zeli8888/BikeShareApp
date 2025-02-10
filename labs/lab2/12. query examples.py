'''
If done locally, remember to input mysql -u root -p in the terminal
If MySQL does not work, export PATH=${PATH}:/usr/local/mysql/bin
Let us do some queries on the database
'''
from sqlalchemy import create_engine
from python_basic_db import new_engine_connection

USER = "root"
PASSWORD = "as5071565"
PORT = "3306"
DB = "local_databasejcdecaux"
URI = "127.0.0.1"

connection_string = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)

engine = create_engine(connection_string, echo = True)

# QUERY 1 counts the total number of rows in the station table (count is count, and * is 'all')
sql = "select count(*) from station;"
# num_stations = engine.execute(sql).fetchall() # I need to use fetchall because execute does not return a list but an object ResultProxy that can be used to iterate over rows
num_stations = new_engine_connection(engine, sql).fetchall() # I need to use fetchall because execute does not return a list but an object ResultProxy that can be used to iterate over rows
print('the number of stations is {}'.format(num_stations[0][0]))

# QUERY 2 select the rows associated with station Smithfield North
sql = "select * from station where address = 'Smithfield North';"
# print(engine.execute(sql).fetchall())
print(new_engine_connection(engine, sql).fetchall())

# QUERY 3 remove the duplicates: first create a temporary table where I put only unique elements
# then remove the original table and rename the temporary one with the old name

# engine.execute("CREATE TABLE temp_station AS SELECT DISTINCT * FROM station;")
# engine.execute("DROP TABLE station;")
# engine.execute("RENAME TABLE temp_station TO station;")
new_engine_connection(engine, "CREATE TABLE temp_station AS SELECT DISTINCT * FROM station;")
new_engine_connection(engine, "DROP TABLE station;")
new_engine_connection(engine, "RENAME TABLE temp_station TO station;")

# print(engine.execute("select * from station where address = 'Smithfield North';").fetchall())
print(new_engine_connection(engine, "select * from station where address = 'Smithfield North';").fetchall())

# QUERY 4 

# print(engine.execute("select * from station where bikestands > 20").fetchall())
print(new_engine_connection(engine, "select * from station where bike_stands > 20").fetchall())

