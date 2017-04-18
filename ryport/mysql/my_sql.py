"""
Written by: Ian Doarn

Simple MySQL connector
"""
import mysql.connector
from mysql.connector import connection
from mysql.connector import errorcode

# TODO: Test this on a real MySQL server
# TODO: Comment this

class MySQL:

    def __init__(self, username, password, host, port, database, raise_on_warnings=True, use_pure=False):
        self.config = {'user': username,
                       'password': password,
                       'host': host,
                       'port': port,
                       'database': database,
                       'raise_on_warnings': raise_on_warnings,
                       'use_pure': use_pure
                       }

        self.cnx = None
        self.cur = None

    def establish_connection(self, buffered=True):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cur = self.cnx.cursor(buffered=buffered)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def establish_connection_mysql(self, buffered=True):
        try:
            self.cnx = connection.MySQLConnection(**self.config)
            self.cur = self.cnx.cursor(buffered=buffered)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close_connection(self):
        try:
            self.cnx.close()
        except Exception as ex:
            print(ex)

    def execute(self, query, *args):
        try:
            self.cur.execute(query, *args)
            try:
                data = self.cur.fetchall()
                return data
            except Exception as ex:
                pass
            return self.cur
        except Exception as ex:
            print(ex)