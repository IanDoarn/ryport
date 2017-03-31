"""
Created by: Ian Doarn

Uses lxml to create xml files
"""
from lxml import etree

__author__ = 'Ian Doarn'
__maintainer__ = __author__
__version__ = '1.0.0'


class XML:

    def __init__(self, root='root'):
        """
        Instantiated wit the name of the root node
        :param root: Root node name
        """
        self.root = etree.Element(root)

    @staticmethod
    def write_file(root, file_name):
        """
        Writes XML file
        
        :param root: root node
        :param file_name: name of the xml file
        :return: None
        """
        doc = etree.ElementTree(root)
        doc.write(file_name, pretty_print=True)

    @staticmethod
    def create_root(name):
        """
        Create a new root node if you need one
        
        :param name: Name of root node
        :return: etree.Element object
        """
        return etree.Element(name)

    @staticmethod
    def create_child(node_name, text=None, **kwargs):
        """
        Creates a new child node and adds additional
        attributes to it using given **kwargs
        
        Example:
        
            Given:  
                create_child('name', type='string', value='Bob')
            Result: 
                <name type="string" value="Bob"/>
        
        :param node_name: Name of node
        :param text: Text inside node
        :param kwargs: Additional keywords for the node
        :return: etree.Element object
        """
        child = etree.Element(node_name, kwargs)
        child.text = text if text is not None else None
        return child

    @staticmethod
    def create_sub_child(root, node_name, text=None, **kwargs):
        """
        Works the same as the create_child method except
        it requires the root node to add the sub child to
        Example:
        
            Given:  
                hobbies = xml.create_child('hobbies', type='Hobbies')
                languages = xml.create_sub_child(hobbies, 'programming_languages', type='languages', value='3')
                python = xml.create_sub_child(languages, 'python', language_name='python')
           
            Result: 
            
                <hobbies type="Hobbies">
                    <programming_languages type="languages" value="3">
                      <python language_name="python"/>
                      
        :param root: Parent node
        :param node_name: name of the node
        :param text: Text inside node
        :param kwargs: Additional keywords for the node
        :return: etree.SubElement object
        """
        sub_child = etree.SubElement(root, node_name, **kwargs)
        sub_child.text = text if text is not None else None
        return sub_child

    @staticmethod
    def add_child(root, child):
        """
        Adds child node to its parent
        
        :param root: Parent node
        :param child: child node
        :return: 
        """
        root.append(child)


# Example Usage
# ===========================================================================================================================
# file_name = 'ian.xml'
# xml = XML('Ian')
#
# name = xml.create_child('name', type='string', value='Ian')
# age = xml.create_child('age', type='integer', value='20')
# hobbies = xml.create_child('hobbies', type='Hobbies')
# video_games = xml.create_child('games', type='Games')
#
# languages = xml.create_sub_child(hobbies, 'programming_languages', type='languages', value='3')
# python = xml.create_sub_child(languages, 'python', language_name='python')
# java = xml.create_sub_child(languages, 'java', language_name='java')
# c_sharp = xml.create_sub_child(languages, 'c_Sharp', language_name='c_sharp')
#
# computer_games = xml.create_sub_child(video_games, 'computer_games', type='PC')
# team_fortress_2 = xml.create_sub_child(computer_games, 'tf2', name='Team_Fortress_2', abbreviation='TF2', hours='4000')
# counter_strike = xml.create_sub_child(computer_games, 'csgo', name='Counter_Strike_Global_Offensive', abbreviation='CSGO', hours='600')
#
#
# xml.add_child(xml.root, name)
# xml.add_child(xml.root, age)
# xml.add_child(xml.root, hobbies)
# xml.add_child(xml.root, video_games)
#
# xml.write_file(xml.root, file_name)
#
# Output:
# <Ian>
#   <name type="string" value="Ian"/>
#   <age type="integer" value="20"/>
#   <hobbies type="Hobbies">
#     <programming_languages type="languages" value="3">
#       <python language_name="python"/>
#       <java language_name="java"/>
#       <c_Sharp language_name="c_sharp"/>
#     </programming_languages>
#   </hobbies>
#   <games type="Games">
#     <computer_games type="PC">
#       <tf2 abbreviation="TF2" hours="4000" name="Team_Fortress_2"/>
#       <csgo abbreviation="CSGO" hours="600" name="Counter_Strike_Global_Offensive"/>
#     </computer_games>
#   </games>
# </Ian>
# ===========================================================================================================================
