# 1. Parent searches for data in child (child.text)
#   a. If data, save to list
# 2. At the same time checks for grandchildren
#   a. If grandchildren, add to dict {child_elem: [grandchildren]}.
#   b. Tag: no_grandchildren is set to False.
# 3. If no grandchildren, write to file
# 4. If grandchildren, restard function for child

from lxml import etree
import InitLogging
import logging

InitLogging.init_logging(log_level=0)


def unpack_xml(element, children_elements, children_data, no_grandchildren=True):
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
            gathered_data.append(child_data)
            logging.debug(f"Data added to data list")

        grandchildren = child.getchildren()
        logging.debug(f"Grandchildren returned: {grandchildren}")
        # If child has grandchildren: add child and list of children to dict.
        # These are to be passed in when calling this function again for the child.
        if grandchildren:
            no_grandchildren = False
            logging.debug(f"Grandchildren found, no_grandchildren set to: {no_grandchildren}")
            children_parameters[child] = grandchildren
            logging.debug(f"Grandchildren have been added to dictionary: {children_parameters}")
    logging.info(f"Information gathering for {element} has completed")

    logging.info(f"Checking if grandchildren were found.")
    if no_grandchildren:
        logging.info(f"No grandchildren were found, starting write-out.")
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
        unpack_xml(element=child, children_elements=grandchildren, children_data=gathered_data)
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
