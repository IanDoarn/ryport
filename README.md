# ryport
Reporting tool for postgres

ryport allows you to run simple postgres quries with ease as well as manipluate the data it may return!

### Coming Soon!
Soon ryport will be able to automate queries, output to excel files, and re run / refresh data daily

### Requirments
- Python 3.6+
- psycopg2
- lxml
- XlsxWritter

### Usage
```python
"""
Connects to local database
Executes query
and formats returned data
"""
from ryport.pgsql.postgres import Postgres

# Create postgres connection
pg = Postgres(username='postgres',
              password='password',
              host='localhost',
              database='dvdrental')

# Test connection to server
pg.test_connection()

# Establish connection to server
pg.establish_connection()

# save sql query from file to variable
query = pg.open_sql_file(r'queries/movies.sql')

# Execute query, returning data and headers
data, headers = pg.execute(query)

# Terminate connection to server
pg.close_connection()

# Format data and headers to be readable,
# by default data is a list of tuples
# and headers are a psycopg2 Column object
data = pg.format_data(data, list)
headers = pg.format_headers(headers)
```
