from lxml import etree


class XML:

    def __init__(self, root='root'):
        self.root = etree.Element(root)


    @staticmethod
    def write_file(root, file_name):
        doc = etree.ElementTree(root)
        doc.write(file_name, pretty_print=True)

    @staticmethod
    def create_root(name):
        return etree.Element(name)

    @staticmethod
    def create_child(node_name, text=None, **kwargs):
        child = etree.Element(node_name, kwargs)
        child.text = text if text is not None else None
        return child

    @staticmethod
    def create_sub_child(root, node_name, text=None, **kwargs):
        sub_child = etree.SubElement(root, node_name, **kwargs)
        sub_child.text = text if text is not None else None
        return sub_child

    @staticmethod
    def add_child(root, child):
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
# team_fortess_2 = xml.create_sub_child(computer_games, 'tf2', name='Team_Fortress_2', abbreviation='TF2', hours='4000')
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
