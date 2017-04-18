"""
Written by: Ian Doarn

Writes and excel (xlsx) file from given data and headers
"""
import xlsxwriter

__author__ = 'Ian Doarn'
__file__ = 'xlsx.py'

#TODO: Add support for multi sheet data
#TODO: Add support for formatting on excel file tables, such as
#TODO: cell color, text color, ect.
#TODO: Auto format file names to check for .xlsx extension if it isn't present

class Writer:
    """
    Writer class 
    """
    def __init__(self, pg_data=None, headers=None):
        """
        Takes input of data and headers
        
        checks if pg_data is a list or is not None and
        checks if headers is a dict or is not None. Raises
        a TypeError in response, data and headers should be formatted
        before being passed in
        
        :param pg_data: Query data
        :param headers: Query headers
        """
        if type(pg_data) is not list or type(pg_data) is None:
            raise TypeError('pg_data must be list not {}'.format(str(type(pg_data))))
        if type(headers) is not dict or type(headers) is None:
            raise TypeError('headers must be dict not {}'.format(str(type(pg_data))))

        self.data = pg_data
        self.headers = headers

    @classmethod
    def get_column_range(cls, height, width, start_index=0):
        """get_column_range
        Gets the range for the table to be used when writing the excel file.
        
        Height corresponds to the number of rows in the table
        Width refers to the number of columns in the table
        start_index is the column to start at, which is A
        
        the initial and final letters are found by index a string of letters
        of the alphabet.
        
        Example:
            height = 7, width = 3, start_index = 0
            
            initial column letter will be A
            initial column cell will be 1
            
            final column letter will be C
            final column cell will be 7
            
            resulting pair for column range is A1:C7
        
        :param height: 
        :param width: 
        :param start_index: 
        :return: Initial column letter, initial column cell index, final letter, final index
        """
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        init_letter = letters[start_index]
        init_pos = init_letter + str(start_index + 1)
        final_letter = letters[width - 1]
        final_pos = final_letter + str(height)

        return init_letter, init_pos, final_letter, final_pos

    def create_report(self, file_name='untitled.xlsx', sheet_names=None):
        """create_report
        Creates excel(xlsx) report from given data and headers
        
        Process:
        1. We check if if the user gave a sheet_name, raise an error if not
        2. Create workbook and give it the name from file_name, defaulted as untitled.xlsx
        3. Create workbook sheet with sheet_names given
        4. Create list of each rows data
        5. Create column_data dict which is used from worksheet.add_table()
        6. Create list of header dicts for column_data, these correspond to each column
           that will be in the table
        7. Get the column range
        8. Set the column range and add the table to the sheet
        9. Close the workbook
        
        This method currently only supports single sheet excel files but soon
        will handle multiple sheets.
        
        
        
        :param file_name: 
        :param sheet_names: 
        :return: 
        """
        if sheet_names is None or type(sheet_names) is not str:
            raise TypeError('sheet_names must be a str not {}'.format(str(type(sheet_names))))
        if len(sheet_names) is 0:
            raise ValueError('sheet_names can not be empty')

        data = self.data
        headers = self.headers

        # Create workbook
        workbook = xlsxwriter.Workbook(file_name)

        # Add sheet
        worksheet = workbook.add_worksheet(sheet_names)

        # Set up row and column data
        row_data = [row for row in data]
        column_data = {'data': row_data, 'columns': []}

        # Get tables height and width
        table_width = len(data[0])
        table_height = len(data)

        # Create list of column headers
        # Format: {'header': 'example_header'}
        for header in headers['data']:
            column_data['columns'].append({'header': header['name']})

        # Get table ranges for columns
        init_l, init_p, final_l, final_p = self.get_column_range(table_height, table_width)

        # Set column range
        worksheet.set_column('{}:{}'.format(init_l, final_l))

        # Create and add table to worksheet
        worksheet.add_table('{}:{}'.format(init_p, final_p),
                            column_data)

        # Close workbook
        workbook.close()
