"""
Created by: Ian Doarn

Used to connect to postgres,
execute queries and retrieve data
"""
from ryport.utils import format_headers, format_data
import psycopg2

__author__ = 'Ian Doarn'
__maintainer__ = __author__
__version__ = '1.0.2'


class Postgres:
    """
    Connects to a postgres server using psycopg2
    """
    def __init__(self, username=None, password=None, host=None, database=None):
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.conn = None
        self.cursor = None

    def test_connection(self, retries=5):
        """
        Will test if a connection to the server is possible.
        If username, password, or the host is not set, it will
        automatically return False. Otherwise, a loop of range 0 to
        the number of given retires, defaulted at 5, will iterate until
        the limit is reached or a connection is made.

        :param retries: Number of times to retry a connection
        :return:
        """

        conn_info = {'username': self.username,
                     'password': self.password,
                     'host': self.host,
                     'database': self.database}

        if [v for k, v in conn_info.items() if v is None].__contains__(None):
            raise ConnectionError('Missing Information: [{}]'.format(
                str(', '.join([k for k, v in conn_info.items() if v is None]))))
        for i in range(0, retries):
            try:
                self.establish_connection()
                self.close_connection()
                return True
            except Exception as e:
                print('Could not establish connection after [{}] tries. {}'.format(str(i + 1), e))
                return False

    def establish_connection(self):
        """
        Opens connection to postgres and sets the
        self.conn object to the connection and sets the
        self.cursor the the connection cursor
        :return:
        """
        self.conn = psycopg2.connect("dbname=" + self.database +
                                     " user=" + self.username +
                                     " host=" + self.host +
                                     " password=" + self.password)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        """
        Closes the connection to postgres
        :return:
        """
        try:
            self.conn.close()
            self.conn = None
            self.cursor = None
        except Exception as e:
            print('Unable to close connection to host: {}\n{}'.format(self.host, str(e)))

    def execute(self, query, allow_format_data=True, allow_format_headers=True):
        """
        Executes a query to postgres

        If data is to be returned from the query,
        a tuple of the data and the data headers is returned.

        otherwise nothing is returned

        :param query: Given input to be executed
        :param format_data: Defaulted to True
        :param format_headers: Defaulted to True
        :return: Either data, data headers or None
        """
        if self.conn is None:
            print('Unable to execute query. No connection has been established with the server.')
        else:
            try:
                self.cursor.execute(query)
                self.conn.commit()
                try:
                    data = self.cursor.fetchall()
                    headers = self.cursor.description

                    if allow_format_data is not False:
                        data = format_data(data, data_type=list)
                    if allow_format_headers is not False:
                        headers = format_headers(headers)

                    return data, headers
                except Exception as e:
                    print(str(e))
                    return None, None
            except Exception as e:
                print("{}".format(str(e)))

    @staticmethod
    def open_sql_file(file):
        """
        Opens a sql file or other txt like file
        and formats it to be used by the execute() command

        :param file: File to be opened
        :return: Formatted query text
        """

        # TODO: Fix issues with multi sub-query files not loading properly

        with open(file, 'r')as f:
            query = f.read().replace('\n', ' ')
        f.close()
        return query

