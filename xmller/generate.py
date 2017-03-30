from lxml import etree

# create XML
root = etree.Element('root')
root.append(etree.Element('child'))
# another child with text
child = etree.Element('child')
child.text = 'some text'
root.append(child)

# pretty string
s = etree.tostring(root, pretty_print=True)

with open('test.xml', 'w')as f:
    f.write(s.decode("utf-8"))