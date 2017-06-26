"""
Written by: Ian Doarn

Writes and excel (xlsx) file from given data and headers
"""
import xlsxwriter

__author__ = 'Ian Doarn'

DEFAULT_EXTENSION = '.xlsx'
DEFAULT_FILE_NAME = 'untitled{}'.format(DEFAULT_EXTENSION)
DEFAULT_SHEET_NAME = 'sheet'


# TODO: Fix create_single_sheet_simple not working on create_table

class Writer:
    """
    Writer class 
    """
    def __init__(self, pg_data=None, headers=None, multi_sheet=False):
        """
        Takes input of data and headers
        
        checks if pg_data is a list or is not None and
        checks if headers is a dict or is not None. Raises
        a TypeError in response, data and headers should be formatted
        before being passed in
        
        if multi_sheet is True, headers must be None, pg_data must be
        a dict in the following format:
            
            {'sheets': 
                [{'name': 'sheet1',
                  'data': data,
                  'headers': headers},
                 {'name': 'sheet2',
                  'data': data,
                  'headers': headers}],
             'file_name': 'untitled.xlsx'}
        
            for empty / filler sheets, make the values of the keys
            data and headers None and make sure to include a sheet name
            
        :param pg_data: Query data
        :param headers: Query headers
        :param multi_sheet: Weather to query will need to be written to multiple sheets
        """

        if type(multi_sheet) is not bool:
            raise TypeError('multi_sheet must be bool not {}'.format(str(type(bool))))

        if multi_sheet is True:
            if type(pg_data) is not dict or type(pg_data) is None:
                raise TypeError('pg_data must be dict not {}'.format(str(type(pg_data))))

            self.pg_data = pg_data

        else:
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

        if width > 26:
            raise ValueError('width can not exceed 26 columns. [VALUE {}]'.format(str(width)))

        init_letter = letters[start_index]
        init_pos = init_letter + str(start_index + 1)
        final_letter = letters[width - 1]
        final_pos = final_letter + str(height)

        return init_letter, init_pos, final_letter, final_pos

    def create_single_sheet_simple(self, file_name=DEFAULT_FILE_NAME, sheet_name=DEFAULT_SHEET_NAME + '1'):
        """create_single_sheet
        Creates single sheet excel(xlsx) report from given data and headers
        
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
        
        
        :param file_name: Default: untitled.xlsx
        :param sheet_names: name of sheet, Default: sheet1
        """

        if sheet_name is None or type(sheet_name) is not str:
            raise TypeError('sheet_names must be str not {}'.format(str(type(sheet_name))))

        data = self.data
        headers = self.headers

        # Create workbook

        # check if .xlsx is at the end, if not add it
        if file_name.endswith(DEFAULT_EXTENSION):
            workbook = xlsxwriter.Workbook(file_name)
        else:
            workbook = xlsxwriter.Workbook(file_name + DEFAULT_EXTENSION)

        # Add sheet
        worksheet = workbook.add_worksheet(sheet_name)

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
        worksheet.add_table('{}:{}'.format(init_p, final_p), column_data)

        # Close workbook
        workbook.close()

    def create_multi_sheet_simple(self):
        """create_multi_sheet_simple
        Creates a multi sheet excel(xlsx) report from given data and headers

        Process:
        1. Create workbook and give it the name from file_name, defaulted as untitled.xlsx
        2. Iterate each sheet in data dict
        3. Create workbook sheet with sheet_names given
        4. Create list of each rows data
        5. Create column_data dict which is used from worksheet.add_table()
        6. Create list of header dicts for column_data, these correspond to each column
           that will be in the table
        7. Get the column range
        8. Set the column range and add the table to the sheet
        9. Close the workbook after all data has been iterated

        If data or headers contains the value None, the sheet will automatically be assumed as a filler
        sheet and be ignored but will still be added in the order it occurs in the dictionary
        """

        data = self.pg_data

        # Create workbook, use default file name if one is not given
        if 'file_name' not in data.keys():
            file_name = DEFAULT_FILE_NAME
        else:
            file_name = data['file_name']

        # check if .xlsx is at the end, if not add it
        if file_name.endswith(DEFAULT_EXTENSION):
            workbook = xlsxwriter.Workbook(file_name)
        else:
            workbook = xlsxwriter.Workbook(file_name + DEFAULT_EXTENSION)

        sheet_count = 0

        # Begin iterating each item in the list of sheets
        for sheet in data['sheets']:

            sheet_count += 1
            q_data = sheet['data']
            headers = sheet['headers']

            # Set sheet name to default if one is not present
            if 'name' not in sheet.keys() or sheet['name'] is None:
                sheet_name = DEFAULT_SHEET_NAME + str(sheet_count)
            else:
                sheet_name = sheet['name']

            # Determine if sheet is a filler sheet
            if q_data is not None or headers is not None:
                # Add sheet
                worksheet = workbook.add_worksheet(sheet_name)

                # Set up row and column data
                row_data = [row for row in q_data]
                column_data = {'data': row_data, 'columns': []}

                # Get tables height and width
                table_width = len(q_data[0])
                table_height = len(q_data)

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

            # if it is, add it to the worksheet
            else:
                worksheet = workbook.add_worksheet(sheet_name)

        # Close workbook
        workbook.close()
