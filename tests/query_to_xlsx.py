"""
Written by: Ian Doarn

Executes query and creates excel file from data
"""
from ryport.pgsql.postgres import Postgres
from ryport.xlsx_writer.writer import Writer

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
data, headers = pg.execute(query, format_data=True, format_headers=True)

# Terminate connection to server
pg.close_connection()

# Set file name
file_name = 'movies.xlsx_writer'

# Create writer and load in data and headers
writer = Writer(data, headers)

# Write report using the file_name and a basic sheet_name
writer.create_report(file_name=file_name ,sheet_names='sheet1')
