from ryport.xml_builder.reader import Reader
import pprint


r = Reader('ian.xml')
r.set_root('//Ian')

root_children = r.get_children(r.root)
root_children_attributes = r.get_attributes_from_children(root_children)

print(r.base)
pprint.pprint(root_children_attributes, indent=4)
