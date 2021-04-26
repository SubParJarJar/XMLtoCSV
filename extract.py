# : Children are passed into function by master.
#   : Unless master is root, then .getchildren is run twice.
# : While looping over children, get data of all children.
#   : This data is saved into a list together with the list of grandchildren.
#   : If no grandchildren are found, that part of the recursive return 0.
#   : A tag is added called no_grandchildren which remains True until a grandchild is found.
#   : If master is at last child in list and no_grandchildren is True:
#       : Then the last branch is found and another tag is given, write_out.
#       : If write_out is true then all data is gathered and written to file, and the function exits.

# : Get XML, parse XML, get root, get list of children.
# : Create recursive function

from lxml import etree
import InitLogging
import logging

InitLogging.init_logging(log_level=0)


def add_to_header(d, dictionary, cnt):
    dictionary[d] = cnt


def unpack_xml(element, children_elements, children_data, no_grandchildren=True, counter=0):
    # Child: [grandchildren]
    children_parameters = dict()
    # pass to child if grandchildren: grandchildren, children_data,
    logging.info(f"Looping over children in {children_elements}")
    gathered_data = children_data.copy()
    for child in children_elements:
        logging.info(f"Processing {child}")
        child_data = (child.tag, child.text)
        logging.debug(f"Data found: {child_data}")
        # If child has text, add to data list
        if child_data[1]:
            counter += 1
            add_to_header(child.tag, header_dict, counter)
            gathered_data.append(child_data)
            logging.debug(f"Data added to data list")

        grandchildren = child.getchildren()
        logging.debug(f"Grandchildren returned: {grandchildren}")
        # If child has grandchildren: add child and list of children to dict. These are to be passed in when calling
        # this function again for the child.
        if grandchildren:
            no_grandchildren = False
            logging.debug(f"Grandchildren found, no_grandschildren set to: {no_grandchildren}")
            children_parameters[child] = grandchildren
            logging.debug(f"Grandchildren have been added to dictionary: {children_parameters}")
    logging.info(f"Information gathering for {element} has completed")

    logging.info(f"Checking if grandchildren were found.")
    if no_grandchildren:
        logging.info(f"No grandchildren were found, starting writeout.")
        with open('out.csv', 'a') as f:
            logging.info(f"{element} writing to file")
            for elem in gathered_data:
                f.write(elem[0])
                f.write(";")
                f.write(elem[1])
                f.write(",")
            f.write("\n")
            f.close()
    logging.info(f"Grandchildren were found, starting recursive chain")
    has_descendants = list(children_parameters.keys())
    # If child has grandchildren, then function is started for grandchildren. If no grandchildren: then write out
    while has_descendants:
        # Pop 0 to keep same order of loop above
        child = has_descendants.pop(0)
        grandchildren = children_parameters[child]

        logging.debug(f"Starting recursive for {child}")
        logging.debug(f"Inserting parameters:")
        logging.debug(f"Element: {child}")
        logging.debug(f"Children elements list: {grandchildren}")
        logging.debug(f"Data: {gathered_data}")
        unpack_xml(element=child, children_elements=grandchildren, children_data=gathered_data, counter=counter)
        # As long as children_elements has children, pop. If at last one and still no grandchildren, then last in branch
        # found, start writeout.


xml_file = 'try.xml'
parser = etree.XMLParser(encoding='UTF-8', )
parsed = etree.parse(xml_file, parser=parser)
root = parsed.getroot()
root_children = root.getchildren()
data = []
header_dict = dict()
unpack_xml(element=root, children_elements=root_children, children_data=data)


# TODO: Create dictionary with number:column_name. If key == dictionary[number] then keep writing.
#   TODO: If not, create new file.