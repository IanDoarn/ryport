import psycopg2
from colorama import init, Fore

init(autoreset=True)


class Postgres:

    def __init___(self, username, password, host):
        self.con = None
        self.cur = None
        self.username = username
        self.password = password
        self.host = host

    def test_connection(self, retries=5, database="postgres"):
        if self.username is None or self.password is None or self.host is None:
            print(Fore.LIGHTRED_EX + 'No login and host information found.'.format())
            return False
        for i in range(0, retries):
            try:
                self.con = psycopg2.connect("dbname=" + database + " user=" + self.username + " host=" + self.host + " password=" + self.password)
                self.cur = self.con.cursor()
                self.con.close()
                return True
            except Exception as e:
                print(Fore.LIGHTRED_EX + 'Could not establish connection after [{}] tries. {}'.format(str(i + 1), e))
                return False

    def establish_connection(self):
        if self.test_connection():
            self.con = psycopg2.connect("dbname=postgres user=" + self.username + " host=" + self.host + " password=" + self.password)
            self.cur = self.con.cursor()
        else:
            print(Fore.LIGHTRED_EX + 'Unable to connect to host: {}'.format(self.host))

    def close_connection(self):
        try:
            self.con.close()
        except:
            print(Fore.LIGHTRED_EX + 'Unable to close connection to host: ' + self.host)

    def execute(self, query):
        if self.con is None:
            print(Fore.LIGHTRED_EX + 'Unable to execute query. No connection has been established with the server.')
        else:
            try:
                self.cur.execute(query)
                self.con.commit()
                try:
                    data = self.cur.fetchall()
                    return data
                except:
                    return None
            except Exception as e:
                print(Fore.LIGHTRED_EX + "{}".format(str(e)))