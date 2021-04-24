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
        logging.info(f"Checking if element: {element} is in list {self.scouted_elem_list}")
        if element in self.scouted_elem_list:
            self.scouted_elem_list.remove(element)
            logging.info(f"Element was removed from list {self.scouted_elem_list}")
            return True
        else:
            logging.info(f"Element was not found in list")
            return False

    def get_siblings(self, element):
        logging.info(f"Checking if element: {element} has siblings")
        if self.siblings_completed:
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

    def find_data(self):
        for elem in self.path_to_root:
            siblings = self.get_siblings(elem)
            if siblings:
                for sib in siblings:
                    tag = sib.tag
                    text = sib.text
                    if text:
                        duo = (tag, text)
                        logging.info(f"Siblings found {duo}, adding to data_elements {self.data_elements}")
                        self.add_to_data_elements(duo)
                        logging.info(f"Added to data elements{self.data_elements}")
        logging.info(f"Gathering data complete: {self.data_elements}")

    def write_data_to_file(self):
        with open('out.csv', 'a') as f:
            logging.info(f"Writing to file elements: {self.data_elements}")
            element = str(self.data_elements)
            f.write(element)
            f.write("\n")
            f.close()
        logging.info(f"Writing completed, purging data")
        self.purge_data_elements()

    def add_elements(self, tag_val):
        self.data_elements.append(tag_val)

    def get_siblings(self, element):
        logging.info(f"Checking if element: {element} has siblings")
        if self.siblings_completed:
            self.siblings_list = list()
            self.siblings_completed = False
        if element in self.siblings_list:
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
    scouted = obj.check_if_in_list(elem)
    if scouted:
        return
    children = elem.getchildren()
    if children:
        for child in children:
            perf_func(child, obj, level + 1)
        return
    elif not children:
        pass
        # Gather siblings
        generation = obj.get_siblings(elem)
        siblings = generation.remove(elem)
        logging.info(f"Generation gathered: {generation}")
        logging.info(f"Siblings gathered: {siblings}")
        # Start sibling sequence
        # if sibling.children, return 0
        # elif not sibling.children: continue
        # outside loop: no children found, deepest level
        deepest_branch = not obj.has_nephew(siblings)
        if deepest_branch:
            obj.add_to_scouted(siblings)
            obj.check_if_in_list(elem)
            logging.info(f"Upward climb can start for element {elem}")
            # Find root
            root_elem = elem.getroottree().getroot()
            # Start upward climb
            up_func(root_elem, elem, gathering_power)
            # Path to root
            # Gather (tag, text) for siblings with data
        elif not deepest_branch:
            return
        else:
            logging.info(f"Something weird happened: {elem}")


def up_func(root_element, elem, obj):
    parent = elem.getparent()
    if parent is root_element:
        obj.add_to_path(elem)
        logging.info(f"Root element: {root_element}")
        logging.info(f"Highest order found {elem}")
        logging.info(f"Current data elements are: {obj.data_elements}")
        logging.info(f"path to root is: {obj.get_path()}")
        # object must search path for siblings with data
        obj.find_data()
        obj.write_data_to_file()
        obj.purge_path()
        return
        # Send message that all data for single csv line has been gathered to obj.
        # Obj must start function to write data to csv
        # Obj must purge list of data and elements
    else:
        obj.add_to_path(elem)
        logging.info(f"Continuing up the ladder {elem}")
        up_func(root_element, parent, obj)


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
