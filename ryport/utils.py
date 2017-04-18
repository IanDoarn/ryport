"""
Created by: Ian Doarn

Utils for ryport
"""

__author__ = 'Ian Doarn'
__maintainer__ = __author__
__version__ = '1.0.0'


def soft_search(data, item):
    """
    Parses data and searches for matches
    based on given item

    :param item: Item to match
    :return: 
    """
    results = []
    for row in data:
        if row.__contains__(item):
            results.append(row)

    return results

def filter_data(data, filter_for):
    """
    Takes list of filters and sees if any 
    matches can be found in each row.

    Compares each cell in a row to each item in the 
    filter_for list using python lambdas

    :param filter_for: List of items to look for matches        
    :return: Returns filtered_data, newly formatted data, and count of rows
    """
    filter_data = {'rows': []}

    for i in range(len(data)):
        row = data[i]
        if any(map(lambda item: item in row, filter_for)):
            filter_data['rows'].append({'index': i, 'data': data[i]})

    if len(filter_data['rows']) is 0:
        return None, None

    _data = []
    for row in filter_data['rows']:
        _data.append(row['data'])

    return filter_data, _data, len(_data)


def format_data(data, sql_type='postgres', data_type=tuple):
    """
    Formats returned data.

    :param data: Data returned by sql database
    :param data_type: Type to convert the given data to. defaulted to tuple
    :return: Formatted data
    """

    if sql_type == 'postgres':
        for i in range(len(data)):
            row = data[i]
            if type(row) is not data_type:
                data[i] = data_type(row)
        return data
