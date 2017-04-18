"""
Written by: Ian Doarn

Write a csv file from postgres data
"""
from ryport.pgsql.postgres import Postgres
from ryport.report.csvw import Writer

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

# Create csv writer, pass in the data, headers, and give it a file name
csvf = Writer(data, headers, 'movies.csv')

# Create a csv writer and pass in the file name
csvf.create_writer(csvf.file_name)

# Write the csv file!
csvf.write_csv()
