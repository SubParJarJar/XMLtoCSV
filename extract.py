# TODO: Children are passed into function by master.
#   TODO: Unless master is root, then .getchildren is run twice.
# TODO: While looping over children, get data of all children.
#   TODO: This data is saved into a list together with the list of grandchildren.
#   TODO: If no grandchildren are found, that part of the recursive return 0.
#   TODO: A tag is added called no_grandchildren which remains True until a grandchild is found.
#   TODO: If master is at last child in list and no_grandchildren is True:
#       TODO: Then the last branch is found and another tag is given, write_out.
#       TODO: If write_out is true then all data is gathered and written to file, and the function exits.

# TODO: Get XML, parse XML, get root, get list of children.
# TODO: Create recursive function

from lxml import etree
import InitLogging
import logging


InitLogging.init_logging(log_level=0)

xml_file = 'try.xml'
parser = etree.XMLParser(encoding='UTF-8')
parsed = etree.parse(xml_file, parser=parser)
root = parsed.getroot()
root_children = root.getchildren()


def unpack_xml (element, children_elements, sibling_data, no_grandchildren=True, write_out=False):
    pass



