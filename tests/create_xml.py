from ryport.xml_builder.builder import XML


file_name = 'ian.xml'
xml = XML('Ian')

name = xml.create_child('name', type='string', value='Ian')
age = xml.create_child('age', type='integer', value='20')
hobbies = xml.create_child('hobbies', type='Hobbies')
video_games = xml.create_child('games', type='Games')

languages = xml.create_sub_child(hobbies, 'programming_languages', type='languages', value='3')
python = xml.create_sub_child(languages, 'python', language_name='python')
java = xml.create_sub_child(languages, 'java', language_name='java')
c_sharp = xml.create_sub_child(languages, 'c_Sharp', language_name='c_sharp')

computer_games = xml.create_sub_child(video_games, 'computer_games', type='PC')
team_fortress_2 = xml.create_sub_child(computer_games, 'tf2', name='Team_Fortress_2', abbreviation='TF2', hours='4000')
counter_strike = xml.create_sub_child(computer_games, 'csgo', name='Counter_Strike_Global_Offensive', abbreviation='CSGO', hours='600')


xml.add_child(xml.root, name)
xml.add_child(xml.root, age)
xml.add_child(xml.root, hobbies)
xml.add_child(xml.root, video_games)

xml.write_file(xml.root, file_name)