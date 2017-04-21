# ryport
Softwrapper and reporting tool for Postgres

Ryport can run queries and write the data straight to readable formats
such as Excel and CSV. 

__!!Currently only PostgreSQL data can be converted to Excel and CSV files!!__

### Coming Soon!
 - Full support for MySQL, MongoDB, Apex SQL
 - Automated refresh of queries
 - Re run any report
 - Save reports to be run again

### Requirements
- Python 3.5+
- psycopg2
- mysql-connector-python
- lxml
- XlsxWriter

# Usage

### Postgres basic query example
----------------------------------
```python
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
```

### MySQL basic query example
---
__Currently MySQL is supported but only as a soft wrapper for executing queries.__
```python
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
```

### Execute a query then create simple excel file from data
-------------------------------------------------------
```python
from ryport.pgsql.postgres import Postgres
from ryport.report.xlsxw import Writer

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
# Set file name
file_name = 'movies.xlsx'
# Create writer and load in data and headers
writer = Writer(data, headers)
# Write report using the file_name and a basic sheet_name
writer.create_single_sheet_simple(file_name=file_name)
```

### Multi query to multi sheet excel file
------------------------------------------
```python
from ryport.pgsql.postgres import Postgres
from ryport.report.xlsxw import Writer

# Create postgres connection
pg = Postgres(username='user',
              password='password',
              host='localhost',
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
```

### Writing CSV Files!
----------------------
```python
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
```

# Data Structures

With ryport you are able to crate xml files and parse them, this will eventually
be used to create and save automated reporting for queries so that users can store
connection information, query settings, reports and locations. This will allow for refreshing
and re running of queries!

### Building XML files
----------------------
Use the XML class in ryport.xml_builder.builder
to create XML files!

```python
from ryport.xml_builder.builder import XML

file_name = 'ian.xml'
xml = XML('Ian')
name = xml.create_child('name', type='string', value='Ian')
age = xml.create_child('age', type='integer', value='20')
hobbies = xml.create_child('hobbies', type='Hobbies')
video_games = xml.create_child('games', type='Games')

languages = xml.create_sub_child(hobbies, 'programming_languages', type='languages', value='3')
python = xml.create_sub_child(languages, 'python', language_name='python')
java = xml.create_sub_child(languages, 'java', language_name='java')
c_sharp = xml.create_sub_child(languages, 'c_Sharp', language_name='c_sharp')

computer_games = xml.create_sub_child(video_games, 'computer_games', type='PC')
team_fortress_2 = xml.create_sub_child(computer_games, 'tf2', name='Team_Fortress_2', abbreviation='TF2', hours='4000')
counter_strike = xml.create_sub_child(computer_games, 'csgo', name='Counter_Strike_Global_Offensive', abbreviation='CSGO', hours='600')


xml.add_child(xml.root, name)
xml.add_child(xml.root, age)
xml.add_child(xml.root, hobbies)
xml.add_child(xml.root, video_games)

xml.write_file(xml.root, file_name)
```

Output:
```xml
<Ian>
  <name type="string" value="Ian"/>
  <age type="integer" value="20"/>
  <hobbies type="Hobbies">
    <programming_languages type="languages" value="3">
      <python language_name="python"/>
      <java language_name="java"/>
      <c_Sharp language_name="c_sharp"/>
    </programming_languages>
  </hobbies>
  <games type="Games">
    <computer_games type="PC">
      <tf2 abbreviation="TF2" hours="4000" name="Team_Fortress_2"/>
      <csgo abbreviation="CSGO" hours="600" name="Counter_Strike_Global_Offensive"/>
    </computer_games>
  </games>
</Ian>
```

### Reading / Parsing XML files
----------------------
Use the Reader class in ryport.xml_builder.reader
to parse and read data from XML and XML-like files!

```python
from ryport.xml_builder.reader import Reader
import pprint


r = Reader('ian.xml')
r.set_root('//Ian')

root_children = r.get_children(r.root)
root_children_attributes = r.get_attributes_from_children(root_children)

print(r.base)
pprint.pprint(root_children_attributes, indent=4)
```
Output:
```json
[   {   'attributes': {'type': 'languages', 'value': '3'},
        'children': [   {   'attribute': {'language_name': 'python'},
                            'element': <Element programming_languages at 0x17c5b48>,
                            'keys': ['language_name'],
                            'tag': 'python'},
                        {   'attribute': {'language_name': 'java'},
                            'element': <Element programming_languages at 0x17c5b48>,
                            'keys': ['language_name'],
                            'tag': 'java'},
                        {   'attribute': {'language_name': 'c_sharp'},
                            'element': <Element programming_languages at 0x17c5b48>,
                            'keys': ['language_name'],
                            'tag': 'c_Sharp'}],
        'element': <Element programming_languages at 0x17c5b48>,
        'keys': ['type', 'value'],
        'tag': 'programming_languages'},
    {   'attributes': {'type': 'PC'},
        'children': [   {   'attribute': {'name': 'Team_Fortress_2', 'abbreviation': 'TF2', 'hours': '4000'},
                            'element': <Element computer_games at 0x17c5dc8>,
                            'keys': ['abbreviation', 'hours', 'name'],
                            'tag': 'tf2'},
                        {   'attribute': {'name': 'Counter_Strike_Global_Offensive', 'abbreviation': 'CSGO', 'hours': '600'},
                            'element': <Element computer_games at 0x17c5dc8>,
                            'keys': ['abbreviation', 'hours', 'name'],
                            'tag': 'csgo'}],
        'element': <Element computer_games at 0x17c5dc8>,
        'keys': ['type'],
        'tag': 'computer_games'}]
```
