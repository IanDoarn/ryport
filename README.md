# ryport
Reporting tool for postgres

ryport allows you to run simple postgres queries with ease as well as
manipulate the data and build / reader xml files!

### Coming Soon!
 - Automated refresh of queries
 - Re run any report
 - Save reports to be run again

### Requirments
- Python 3.6+
- psycopg2
- lxml
- XlsxWritter

# Usage

### Basic example of executing a query.
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

# Format data and headers to be readable,
# by default data is a list of tuples
# and headers are a psycopg2 Column object
data = pg.format_data(data, list)
headers = pg.format_headers(headers)
```


### Execute a query then create simple excel file from data
-------------------------------------------------------
```python
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
file_name = 'movies.xlsx'

# Create writer and load in data and headers
writer = Writer(data, headers)

# Write report using the file_name and a basic sheet_name
writer.create_report(file_name=file_name ,sheet_names='sheet1')
```

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
```python
# Base object, a.k.a. the file name
'ian.xml'

# Attributes and sub-attributes of each element of root //Ian in ian.xml
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
