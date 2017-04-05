"""
Created by: Ian Doarn

Parses psycopg2 data and edits it
"""

__author__ = 'Ian Doarn'
__maintainer__ = __author__
__version__ = '1.0.0'


class Parse:

    def __init__(self, data):
        """
        :param data: Data to parse
        """
        self.data = data

    def soft_search(self, item):
        """
        Parses data and searches for matches
        based on given item
        
        :param item: Item to match
        :return: 
        """
        results = []
        for row in self.data:
            if row.__contains__(item):
                results.append(row)

        return results

    def filter_data(self, filter_for):
        """
        Takes list of filters and sees if any 
        matches can be found in each row.
        
        Compares each cell in a row to each item in the 
        filter_for list using python lambdas
        
        :param filter_for: List of items to look for matches        
        :return: Returns filtered_data, newly formatted data, and count of rows
        """
        filter_data = {'rows': []}

        for i in range(len(self.data)):
            row = self.data[i]
            if any(map(lambda item: item in row, filter_for)):
                filter_data['rows'].append({'index': i, 'data': self.data[i]})

        if len(filter_data['rows']) is 0:
            return None, None

        self.data = []
        for row in filter_data['rows']:
            self.data.append(row['data'])

        return filter_data, self.data, len(self.data)
