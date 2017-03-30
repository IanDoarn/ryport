from lxml import etree


class xmller:

    def __init__(self, root='root'):
        self.root = etree.Element(root)

    @staticmethod
    def write_file(root, file_name):
        xml_object = etree.tostring(root, pretty_print=True)
        with open(file_name, 'w')as xml_file:
            xml_file.write(xml_object.decode('utf-8'))
        xml_file.close()

    @staticmethod
    def create_root(name):
        return etree.Element(name)

    @staticmethod
    def create_child(name, text):
        child = etree.Element(name)
        child.text = text
        return child

    @staticmethod
    def add_child(root, child):
        root.append(child)


    def create_xml_data(self, file_name, query, server_information=[{}], information=[{}], use_default_root=True, custom_root=None):

        if use_default_root is False:
            root = self.create_root(custom_root)
        else:
            root = self.root

        children = []

        children.append(self.create_child('query', query))

        for object in server_information:
            for key, value in object.items():
                children.append(self.create_child(str(key), str(value)))

        for object in information:
            for key, value in object.items():
                children.append(self.create_child(str(key), str(value)))

        for child in children:
            self.add_child(root, child)

        self.write_file(self.root, file_name)
