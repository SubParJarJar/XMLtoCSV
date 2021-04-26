# TODO: Request DTD or XSD schema
#   TODO: If not supplied generate DTD or XSD schema from XML
#   TODO: Generate CSV header plan from schema
#   TODO: Add ability to generate CSV headers on the fly if XML nests are simple.
#       TODO: Simple means: All headers are found in each branch of XML, no retroactivly creating new headers.
#       TODO: Add error check if extra header is found

import xmltodict

with open('try.xml') as fd:
    doc = xmltodict.parse(fd.read())