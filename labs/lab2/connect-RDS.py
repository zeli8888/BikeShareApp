from sqlalchemy import create_engine
import pandas as pd

# Define database connection URL (SQLAlchemy format)
DB_USER = "admin"  # Your RDS username
DB_PASSWORD = "as5071565"  # Your RDS password
DB_HOST = "127.0.0.1"  # Localhost because of SSH tunnel
DB_PORT = "3333"  # Must match your tunnel port
DB_NAME = "dbbikes"  # Change to your database name

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Fetch data into a DataFrame
query = "SELECT * FROM your_table"
df = pd.read_sql(query, engine)

# Print the data
print(df)

# Close the connection
engine.dispose()