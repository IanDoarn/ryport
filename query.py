from pgsql.postgres import Postgres
from pgsql.parse import Parse

pg = Postgres()

pg.username = 'reader'
pg.password = 'ZimmerBiomet'
pg.host = 'vsbslgprd01.zmr.zimmer.com'

query = pg.open_sql_file('test.sql')

pg.establish_connection()

data = pg.execute(query)
data = pg.format_data(data, data_type=list)

pg.close_connection()

parse = Parse(data)

filter = []
_, filtered_data, total = parse.filter_data(filter)


if filtered_data is not None:
    print("Total items matching the filter(s): [{}]\nFilter(s): {}".format(str(total), ', '.join(filter)))
    for row in filtered_data:
        print(row)
else:
    print("No items matching given filter(s): {}".format(', '.join(filter)))