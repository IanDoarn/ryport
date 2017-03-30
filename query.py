from pgsql.postgres import Postgres

pg = Postgres()

pg.username = 'reader'
pg.password = 'ZimmerBiomet'
pg.host = 'vsbslgprd01.zmr.zimmer.com'

with open('test.sql', 'r')as f:
    query = f.read().replace('\n', ' ')
f.close()

pg.establish_connection()

data = pg.execute(query)

pg.close_connection()

print('Query complete. Total rows: {}'.format(str(len(data))))