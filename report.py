from xmller.generate import XML

xml = XML()

information = [{'autorun': False},
               {'refresh': False}]

server_information = [{'username': 'reader'},
                      {'password': 'password'},
                      {'host': 'host_url'}]

query = "select * from sms.enum"

file = 'test.xml'

xml.create_xml_data(file, query, server_information=server_information, information=information)