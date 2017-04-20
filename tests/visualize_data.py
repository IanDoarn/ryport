from ryport.pgsql.postgres import Postgres
import pprint

# Create postgres connection
pg = Postgres(username='postgres',
              password='password',
              host='localhost',
              database='dvdrental')

# Test connection to server
pg.test_connection()

# Establish connection to server
pg.establish_connection()

# Load query
query = pg.open_sql_file(r'queries/movies.sql')

# Execute query
# Automatically format data and headers
data, headers = pg.execute(query)

# Terminate connection to server
pg.close_connection()

pprint.pprint(data)
