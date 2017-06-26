"""
Written by: Ian Doarn

Executes multiple queries and creates excel file from data
that contains multiple sheets
"""
from ryport.pgsql.postgres import Postgres
from ryport.report.xlsxw import Writer

# Create postgres connection
pg = Postgres(username='user',
              password='password',
              host='host',
              database='postgres')

# Test connection to server
pg.test_connection()

# Establish connection to server
pg.establish_connection()

# Load queries from files
mutation_bins_query = pg.open_sql_file(r'queries\mutation_bins.sql')
mutation_loans_query = pg.open_sql_file(r'queries\mutation_loans.sql')

# Execute queries
bin_data, bin_headers = pg.execute(mutation_bins_query)
loan_data, loan_headers = pg.execute(mutation_loans_query)

# Terminate connection to server
pg.close_connection()

# Set file name
file_name = 'mutation.xlsx'

# Create dict for input to writer
# sheet1 and sheet4 are filler sheets and will be empty
data = {'sheets': [{'name': 'sheet1',
                    'data': None,
                    'headers': None},
                   {'name': 'Loans Transferred',
                    'data': loan_data,
                    'headers': loan_headers},
                   {'name': 'Bin Transferred',
                    'data': bin_data,
                    'headers': bin_headers},
                   {'name': 'sheet4',
                    'data': None,
                    'headers': None}],
        'file_name': file_name}


# Create writer and load in data and headers
writer = Writer(pg_data=data, headers=None, multi_sheet=True)

# Write multi sheet report
writer.create_multi_sheet_simple()
