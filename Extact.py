import csv
import xml.etree.ElementTree as ET
from lxml import etree
import InitLogging
import logging


InitLogging.init_logging(log_level=0)



xml_file = 'try.xml'
parser = etree.XMLParser(encoding='UTF-8')
parsed = etree.parse(xml_file, parser=parser)
root = parsed.getroot()


class AlreadyGotIt:
    def __init__(self):
        self.scouted_elem_list = list()
        self.siblings_list = list()
        self.siblings_completed = False

    def add_to_scouted(self, elem_list):
        self.scouted_elem_list += elem_list

    def check_if_in_list(self, element):
        if element in self.scouted_elem_list:
            logging.debug(f"Element was found in list: {self.scouted_elem_list}")
            self.scouted_elem_list.remove(element)
            logging.debug(f"Element was removed from list: {self.scouted_elem_list}")
            return True
        else:
            logging.debug(f"Element was not found in list {self.scouted_elem_list}")
            return False

    def get_siblings(self, element):
        if self.siblings_completed:
            logging.debug(f"Previous siblings were found")
            self.siblings_list = list()
            self.siblings_completed = False
        # Causes recursion to loop.
        if element in self.siblings_list:
            logging.info(f"Element found in sibling list {element}")
            return
        self.siblings_list.append(element)
        nxt = element.getnext()
        prev = element.getprevious()
        if nxt:
            self.get_siblings(nxt)
        elif prev:
            self.get_siblings(prev)
        else:
            self.siblings_completed = True
            return self.siblings_list

    @staticmethod
    def has_nephew(siblings_list):
        # if has nephew, not deepest level
        # default siblings have no children
        logging.info(f"Finding deepest branch in {siblings_list}")
        nephew = False
        if siblings_list:
            logging.info(f"List approved: {siblings_list}")
            for sib in siblings_list:
                # if siblings do have children, not deepest level
                children = sib.getchildren()
                logging.info(f"Sibling {sib} has children: {children}")
                if children:
                    nephew = True
                    logging.info(f"Children found, returning true for not deepest branch: {nephew}")
                    return nephew
                else:
                    logging.info(f"Sibling {sib} has no children: {children}")
                    continue
            return nephew
        else:
            # Element has no siblings, so is deepest level
            return True


class GatheringData:
    def __init__(self):
        self.data_elements = list()
        self.siblings_list = list()
        self.siblings_completed = False
        self.path_to_root = list()

    def purge_path(self):
        self.path_to_root = list()

    def get_path(self):
        return self.path_to_root

    def add_to_path(self, elem):
        self.path_to_root.append(elem)

    def purge_data_elements(self):
        self.data_elements = list()

    def add_to_data_elements(self, item):
        self.data_elements.append(item)

    def find_data(self, siblings):
        r_list = list()
        if siblings:
            for sib in siblings:
                logging.debug(f"Searching sibling {sib} for text")
                tag = sib.tag
                text = sib.text
                logging.debug(f"Search resulted in: {tag, text}")
                if text:
                    duo = (tag, text)
                    logging.debug(f"Created duo of data: {duo}")
                    r_list.append(duo)
                    logging.info(f"Added to data elements: {r_list}")
        logging.info(f"Gathering data complete: {r_list}")
        return r_list

    @staticmethod
    def write_data_to_file(data_elements):
        with open('out.csv', 'a') as f:
            logging.info(f"Writing to file elements: {data_elements}")
            element = str(data_elements)
            logging.info(f"Writing elements: {element}")
            f.write(element)
            f.write("\n")
            f.close()

    def add_elements(self, tag_val):
        self.data_elements.append(tag_val)

    def get_siblings_up(self, element):
        logging.info(f"Checking if element: {element} has siblings")
        if self.siblings_completed:
            logging.debug(f"Previous siblings found: {self.siblings_list} purging list")
            logging.debug(f"Purging list")
            self.siblings_list = list()
            self.siblings_completed = False
        if element in self.siblings_list:
            logging.debug(f"Element was found in list of scouted siblings, quitting branch")
            return
        logging.debug(f"Adding element to scouted siblings list: {element}")
        self.siblings_list.append(element)
        nxt = element.getnext()
        prev = element.getprevious()
        logging.debug(f"Search for next element returned: {nxt}")
        logging.debug(f"Search for previous element returned: {prev}")
        if nxt:
            logging.debug(f"Next sibling found, continuing chain.")
            self.get_siblings_up(nxt)
        elif prev:
            logging.debug(f"Previous sibling found, continuing chain.")
            self.get_siblings_up(prev)
        else:
            logging.debug(f"Sibling list completed, returning list: {self.siblings_list}")
            self.siblings_completed = True
            return self.siblings_list


did_i_get_it = AlreadyGotIt()
gathering_power = GatheringData()
gathering_power.add_elements(1)


def perf_func(elem, obj, level=0):
    # func(elem,level)
    # + kunnen we ter efficientie de elementen uit de lijst poppen zodra ze herkend worden?
    #         ++ i.e. siblings zijn toegevoegd aan lijst van verkende elementen, volgende recursive komt bij sibling terecht:
    #            checkt of hij herkent is, en als dat zo is popt het element uit de lijst.
    #         + een lijst die zich buiten de recursive functie bevindt, en wordt geupdate met de lijst van verkende elementen
    #             + vraagt lijst op met benaderde elementen vanuit ander object.
    #             + deze verkende elementen mogen alleen elementen van de laatste tak zijn.
    #                 + hoe zorgen we ervoor dat een eerdere afgesloten branch geen terugloop functie start?
    #                 + hoe herkent het programma dat dit element de langste tak is, en niet een afgebroken tak hoger in de XML?
    #                     ++ als branch einde heeft siblings, maar siblings hebben geen children, start terugloop.
    #                     ++ als branch einde heeft siblings, en siblings hebben children, return 0
    #                     ++ als branch einde heeft geen siblings, start terugloop.
    #     + hoe zorgen we ervoor dat de csv file de juiste headers in de juist volgorde krijgt?
    #     ++ als terugloopfunctie is gestart, zoek siblings met text, add element.tag en element.text. start parent.
    logging.debug(f"Checking if element is in list")
    logging.debug(f"Parameters: {elem}")
    scouted = obj.check_if_in_list(elem)
    logging.debug(f"Function returned: {scouted}")
    if scouted:
        logging.debug(f"Element was found, exiting this part of recursive function")
        return
    logging.debug(f"Element was not scouted, getting element children")
    logging.debug(f"No parameters passed")
    children = elem.getchildren()
    logging.debug(f"Element returned children: {children}")
    if children:
        logging.debug(f"Children were found, looping over list of children and starting new recursive function")
        for child in children:
            logging.debug(f"Starting new function for child: {child, child.tag}")
            logging.debug(f"Parameters: {child, obj, level + 1}")
            perf_func(child, obj, level + 1)
        logging.debug(f"Looping is done for element: {elem}, exiting branch.")
        return
    elif not children:
        logging.debug(f"No children found for element {elem}")
        # Gather siblings
        logging.debug(f"Searching for siblings of element: {elem}")
        logging.debug(f"Parameters: {elem}")
        generation = obj.get_siblings(elem)
        logging.debug(f"Generation gathered: {generation}")
        if generation:
            siblings = generation.remove(elem)
            logging.debug(f"Element: {elem} siblings gathered: {siblings}")
        # Start sibling sequence
        # if sibling.children, return 0
        # elif not sibling.children: continue
        # outside loop: no children found, deepest level
        logging.debug(f"Checking if {elem} is deepest branch")
        logging.debug(f"Parameters: {generation}")
        deepest_branch = not obj.has_nephew(generation)
        logging.debug(f"Is element {elem} deemed the deepest branch? {deepest_branch}")
        if deepest_branch:
            logging.debug(f"Element {elem} has started deepest_branch execution.")
            logging.debug(f"Adding all siblings to scouted list")
            logging.debug(f"Parameters: {siblings}")
            obj.add_to_scouted(siblings)
            logging.debug(f"Checking if element has been scouted already, to remove element from list.")
            logging.debug(f"Parameters: {siblings}")
            scouted = obj.check_if_in_list(elem)
            logging.debug(f"Upward climb can start for element {elem}")
            # Find root
            logging.debug(f"Getting root for starting recursive up function")
            root_elem = elem.getroottree().getroot()
            logging.debug(f"Root element set: {root_elem}")
            # Start upward climb
            logging.debug(f"Starting recursive up function")
            logging.debug(f"Parameters: {root_elem, elem, gathering_power}")
            up_func(root_elem, elem, gathering_power)
            logging.debug(f"Recursive up function has been completed. Cleaning up gatherer object")
            logging.debug(f"Purging path: {gathering_power.path_to_root}")
            gathering_power.purge_path()
            logging.debug(f"Purging data elements: {gathering_power.purge_data_elements}")
            gathering_power.purge_data_elements()
            logging.debug(f"Purging done, exiting this branch of function")
            return
            # Path to root
            # Gather (tag, text) for siblings with data
        elif not deepest_branch:
            logging.debug(f"Not deepest branch, exiting this branch of function")
            return
        else:
            logging.info(f"Something weird happened: {elem}")


def up_func(root_element, elem, obj, data_element=None):
    logging.debug(f"Checking if list of data elements is passed for {elem}")
    if data_element is None:
        logging.debug(f"No data element found, setting data element to: {obj.data_elements}")
        data_element = obj.data_elements
    logging.debug(f"Element {elem} moving towards root {root_element}")
    logging.debug(f"Searching for parent of element {elem}")
    parent = elem.getparent()
    logging.debug(f"Function returned {parent}")
    if parent is root_element:
        logging.debug(f"Root element found: {parent}, adding element {elem} to path to root")
        obj.add_to_path(elem)
        logging.debug(f"Element {elem} was added to path to root")
        logging.debug(f"Current data elements are: {obj.data_elements}")
        logging.debug(f"Current path to root is: {obj.path_to_root}")
        # object must search path for siblings with data
        logging.debug(f"Starting walk up to root, searching for siblings")
        logging.debug(f"Parameters: {elem}")
        siblings = obj.get_siblings_up(elem)
        logging.debug(f"Siblings search returned: {siblings}")
        logging.debug(f"Searching for data in siblings list")
        found_data = obj.find_data(siblings)
        data_element += found_data
        logging.debug(f"Writing data full element list: {data_element}")
        obj.write_data_to_file(data_element)
        logging.debug(f"Write completed, ending this sequence of recursive function")
        return
        # Send message that all data for single csv line has been gathered to obj.
        # Obj must start function to write data to csv
        # Obj must purge list of data and elements
    else:
        logging.debug(f"No root found: {parent}, adding element {elem} to path to root")
        obj.add_to_path(elem)
        logging.debug(f"Element {elem} was added to path to root")
        logging.debug(f"Current data elements are: {obj.data_elements}")
        logging.debug(f"Current path to root is: {obj.path_to_root}")
        # object must search path for siblings with data
        logging.debug(f"Starting walk up to root, searching for siblings")
        logging.debug(f"Parameters: {elem}")
        siblings = obj.get_siblings_up(elem)
        logging.debug(f"Siblings search returned: {siblings}")
        logging.debug(f"Searching for data in siblings list")
        found_data = obj.find_data(siblings)
        data_element += found_data
        logging.debug(f"Writing data full element list: {data_element}")
        logging.info(f"Continuing up the ladder {elem}")
        logging.debug(f"Parameters: {root_element, parent, obj, data_element}")
        up_func(root_element, parent, obj, data_element=data_element)


# def up_func(root_element, elem, obj):
#     # Get parent of element
#     parent = elem.getparent()
#     # Get siblings of element
#     siblings = obj.get_siblings(elem)
#     logging.info(f"{elem} siblings found for upwards function {siblings}")
#     # Get data of siblings
#     if siblings:
#         for sib in siblings:
#             sib_tag = sib.tag
#             sib_text = sib.text
#             logging.info(f"Data gathered for sibling: {sib, sib_tag, sib_text}")
#             if sib_text:
#                 sib_duo = (sib_tag, sib_text)
#                 logging.info(f"Text was found for sibling {sib_duo}")
#                 obj.add_to_data_elements(sib_duo)
#             else:
#                 logging.info(f"No text found for {sib}")
#                 continue
#     if parent is root_element:
#         logging.info(f"Highest order found {elem}")
#         obj.write_data_to_file()
#         # Send message that all data for single csv line has been gathered to obj.
#         # Obj must start function to write data to csv
#         # Obj must purge list of data and elements
#     else:
#         logging.info(f"Continuing up the ladder {elem}")
#         up_func(root_element, parent, obj)


xml_file = 'try.xml'
parser = etree.XMLParser(encoding='UTF-8')
parsed = etree.parse(xml_file, parser=parser)
root = parsed.getroot()
x = perf_func(root, did_i_get_it)
