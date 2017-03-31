import psycopg2
from colorama import init, Fore

init(autoreset=True)


class Postgres:

    def __init___(self):
        self.conn = None
        self.cursor = None
        self.username = None
        self.password = None
        self.host = None

    def test_connection(self, retries=5, database="postgres"):
        if self.username is None or self.password is None or self.host is None:
            print(Fore.LIGHTRED_EX + 'No login and host information found.'.format())
            return False
        for i in range(0, retries):
            try:
                self.conn = psycopg2.connect("dbname=" + database + " user=" + self.username + " host=" + self.host + " password=" + self.password)
                self.cursor = self.conn.cursor()
                self.conn.close()
                return True
            except Exception as e:
                print(Fore.LIGHTRED_EX + 'Could not establish connection after [{}] tries. {}'.format(str(i + 1), e))
                return False

    def establish_connection(self):
        if self.test_connection():
            self.conn = psycopg2.connect("dbname=postgres user=" + self.username + " host=" + self.host + " password=" + self.password)
            self.cursor = self.conn.cursor()
        else:
            print(Fore.LIGHTRED_EX + 'Unable to connect to host: {}'.format(self.host))

    def close_connection(self):
        try:
            self.conn.close()
        except:
            print(Fore.LIGHTRED_EX + 'Unable to close connection to host: ' + self.host)

    def execute(self, query):
        if self.conn is None:
            print(Fore.LIGHTRED_EX + 'Unable to execute query. No connection has been established with the server.')
        else:
            try:
                self.cursor.execute(query)
                self.conn.commit()
                try:
                    data = self.cursor.fetchall()
                    return data
                except:
                    return None
            except Exception as e:
                print(Fore.LIGHTRED_EX + "{}".format(str(e)))
    def open_sql_file(self, file):
        with open(file, 'r')as f:
            query = f.read().replace('\n', ' ')
        f.close()
        return query

    def format_data(self, data, data_type=tuple):
        for i in range(len(data)):
            row = data[i]
            if type(row) is not data_type:
                data[i] = data_type(row)
        return data