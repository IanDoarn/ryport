"""
Written by: Ian Doarn

Example of using the mysql package to
work with MySQL databases
"""
from ryport.mysql import my_sql

# Create connect to database
mysql = my_sql.MySQL('anonymous', '', 'ensembldb.ensembl.org', 3306, '')

# Open the connection
mysql.establish_connection()

# Get the databases
databases = mysql.execute("SHOW DATABASES")

# Set our current database we want to use
mysql.execute("USE {};".format(databases[1][0]))

# Get a list of the tables from the database
tables = mysql.execute("SHOW TABLES")

# Choose the first table in out tables object,
# get the column headers and get 5 rows from the table
columns = mysql.execute("DESCRIBE {}".format(tables[1][0]))
data = mysql.execute("SELECT * from {} LIMIT 5;".format(tables[1][0]))

# Close the connection
mysql.close_connection()

# Print our column headers
# and the first row of results
print(list(columns[0]))
print(list(data[0]))

# Output:
# ['analysis_id', 'smallint(5) unsigned', 'NO', 'PRI', None, 'auto_increment']
# [1, datetime.datetime(2005, 10, 18, 20, 28, 11), 'vectorbase', None, None, None, None, None, None, None, 'GeneBuild', None, None, None]