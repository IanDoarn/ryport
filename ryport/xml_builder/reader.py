"""
Written by: Ian Doarn

Readers / Parses XML files and returns 
the data they contain making it readable
and iterable

==============
Example Usage:
==============
import pprint
r = Reader('ian.xml')
r.set_root('//Ian')

root_children = r.get_children(r.root)
root_children_attributes = r.get_attributes_from_children(root_children)

print(r.base)
pprint.pprint(root_children_attributes, indent=4)

Output:

# Base object, a.k.a. the file name
'ian.xml'

# Attributes and sub-attributes of each element of root //Ian in ian.xml
[   {   'attributes': {'type': 'languages', 'value': '3'},
        'children': [   {   'attribute': {'language_name': 'python'},
                            'element': <Element programming_languages at 0x17c5b48>,
                            'keys': ['language_name'],
                            'tag': 'python'},
                        {   'attribute': {'language_name': 'java'},
                            'element': <Element programming_languages at 0x17c5b48>,
                            'keys': ['language_name'],
                            'tag': 'java'},
                        {   'attribute': {'language_name': 'c_sharp'},
                            'element': <Element programming_languages at 0x17c5b48>,
                            'keys': ['language_name'],
                            'tag': 'c_Sharp'}],
        'element': <Element programming_languages at 0x17c5b48>,
        'keys': ['type', 'value'],
        'tag': 'programming_languages'},
    {   'attributes': {'type': 'PC'},
        'children': [   {   'attribute': {'name': 'Team_Fortress_2', 'abbreviation': 'TF2', 'hours': '4000'},
                            'element': <Element computer_games at 0x17c5dc8>,
                            'keys': ['abbreviation', 'hours', 'name'],
                            'tag': 'tf2'},
                        {   'attribute': {'name': 'Counter_Strike_Global_Offensive', 'abbreviation': 'CSGO', 'hours': '600'},
                            'element': <Element computer_games at 0x17c5dc8>,
                            'keys': ['abbreviation', 'hours', 'name'],
                            'tag': 'csgo'}],
        'element': <Element computer_games at 0x17c5dc8>,
        'keys': ['type'],
        'tag': 'computer_games'}]
"""
from lxml import etree

__author__ = 'Ian Doarn'
__maintainer__ = __author__


class Reader:
    """
    Reader class for reading XML files
    """

    def __init__(self, file):
        """
        Opens file and parses using lxml.etree parser
        Will raise TypeError if the file cannot be parsed
        
        root is the initial node at the top of the tree
        base is the file name associated with the tree
        
        :param file: must be an xml file of an xml like file
        """

        try:
            self.tree = etree.parse(file)
        except Exception as lxml_ex:
            raise TypeError("File could not be opened: Must be .xml or encoded"
                            " like .xml. LXML ERROR: {}".format(str(lxml_ex)))
        self.root = None
        self.base = None

    def check_for_root(self):
        """
        Determine if the root node has been loaded.
        """
        if self.root is None:
            raise ValueError("root is NoneType")

    def set_root(self, xpath):
        """
        Finds the root node in the xml tree
        xpath argument should be str and should have
        '//' at the beginning.
        
        Sets the root value and the base value
        
        :param xpath: xpath to the root node
        :return: root node string
        """
        if xpath[:2] is not '//':
            # Add the // to the front of the string if it isn't there
            self.root = self.tree.xpath('//{}'.format(xpath))
            self.base = self.root[0].base
            return self.root
        self.root = self.tree.xpath(xpath)
        self.base = self.root[0].base
        return self.root

    def get_element(self, xpath):
        """
        Finds the element at the given xpath from the root node
        If the root node is not set, then raise an error
        
        :param xpath: str xpath to the element
        :return: list of elements at the xpath given
        """
        self.check_for_root()
        if xpath[:2] is not '//':
            # Add the // to the front of the string if it isn't there
            return [element for element in self.tree.xpath('{}//{}'.format(self.root, xpath))]
        return [element for element in self.tree.xpath('{}{}'.format(self.root, xpath))]

    @staticmethod
    def get_attributes_from_child(child):
        """
        Gets the attributes of a given element
        
        :param child: Element to return attributes from
        :return: List of dictionaries with the keys: element, attribute, tag, and keys
        """
        return [{'element': child,
                 'attribute': x.attrib,
                 'tag': x.tag,
                 'keys': x.keys()} for x in child]

    @staticmethod
    def get_children(parent, default_index=0):
        """
        Get the child nodes of a given element parent
        
        If a list with a list inside is passed as an argument,
        default_index is used only id the length of the parent list is 
        1 else, iterate each sub list and create dictionary of elements
        and thiar sub children
        
        :param parent: Element node to parse for children 
        :param default_index: default parent list index
        :return: list of children of parent or dictionary of children for each parent in list
        """
        # See if parent  is a list
        if type(parent) is list:
            # If its has 1 item in it
            if len(parent) < 2:
                return [child for child in parent[default_index].getchildren()]
            # Else, iterate each sub list
            else:
                data = []
                for parents in parent:
                    data.append({'element': parents, 'children': [child for child in parents.getchildren()]})
        else:
            # parent isn't a list, so iterate each child
            return [child for child in parent.getchildren()]


    @staticmethod
    def get_items_from_element(element):
        """
        Get element items from given element
        
        returns a dictionary of data about each element.
        The returned dictionary has a list of each items
        items, tag, and keys
        
        :param element: Node to parse
        :return: dictionary of data about given element
        """
        data = {'element': element,
                'items': []}
        for item in element[len(element)-1]:
            item_info = {'data': item.items(),
                         'tag': item.tag,
                         'keys': item.keys()}
            data['items'].append(item_info)
        return data

    def get_attributes_from_children(self, children):
        """
        Iterates a list of elements for each elements sub children and 
        returns the attributes of each child and sub child in the given list
        
        :param children: list of elements to parse
        :return: dictionary of children and their attributes and sub children's attributes
        """
        # Make sure the root is set
        self.check_for_root()
        child_attributes = []
        # for each element_list in the given list of element lists
        for element_list in children:
            # for each element in the current element_list
            for element in element_list:
                # Create dictionary of data
                sub_element = {'element': element,
                               'attributes': element.attrib,
                               'tag': element.tag,
                               'keys': element.keys()}
                # check if element has children
                if element.getchildren() is not []:
                    # get information about each sub-child
                    sub_element['children'] = self.get_attributes_from_child(element)
                child_attributes.append(sub_element)
        return child_attributes
