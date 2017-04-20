"""
Written by: Ian Doarn

simple CSV wrapper
"""

import ryport.utils as util
import csv
# TODO: Test with multiple queries

class Writer:
    """
    Writer class for creating CSV files
    """

    def __init__(self, data, headers, file_name, delimiter=',', register_new_dialect=False, new_dialect=None):
        """
        Writer
        
        Creates csv files from sql data
            
        :param data: Data from the query
        :param headers: Headers for the column names
        :param file_name: name of csv file
        :param delimiter: what to put in between each cell, defaults at ',', change if using a new dialect
        :param register_new_dialect: add a new type of file
        :param new_dialect: set to true if to using something other than a .csv file
        """
        if register_new_dialect:
            csv.register_dialect(new_dialect, delimiter=delimiter)
        if type(headers) is dict:
            # check if headers are properly formatted
            self.headers = util.format_header_data(headers)
        elif type(headers) is list:
            self.headers = headers

        # Determine if data is correctly formatted
        if type(data) is not list:
            raise TypeError('data must be list not {}'.format(str(type(data))))

        self.data = data
        self.delimiter = delimiter
        self.file_name = file_name
        self.file = None
        self.writer = None

    def create_writer(self, file_name, quote_char = '"', newline='', quoting=csv.QUOTE_ALL):
        """
        Create csv writer object
        
        :param file_name: File name
        :param quote_char: what to encapsulate chars and strings with
        :param newline: defaulted at '', prevents blank lines between rows
        :param quoting: default csv.QUOTE_ALL, quotes all data types in file
        :return: self.writer
        """
        self.file = open(file_name,  'w', newline=newline)
        self.writer = csv.writer(self.file,
                                 delimiter=self.delimiter,
                                 quotechar=quote_char,
                                 quoting=quoting)

    def write_csv(self):
        """
        Writes csv file
        :return: None
        """
        # Write headers first
        self.writer.writerow(self.headers)

        # Write rest of the rows
        for row in self.data:
            self.writer.writerow(row)
        self.file.close()

