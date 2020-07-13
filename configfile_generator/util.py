import xml.etree.ElementTree as ET
import os

# use indent for '\t' and newline for '\n'
def prettyXml(element, indent, newline, level = 0) :
    # check whether the element has a child element
    if element :
        if element.text == None or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else :
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    
    temp = list(element)
    for subelement in temp :
        # not the last one
        if temp.index(subelement) < (len(temp) - 1) :
            subelement.tail = newline + indent * (level + 1)
        else:
            # finishing the current element, the indent becomes the previous element
            subelement.tail = newline + indent * level
        
        prettyXml(subelement, indent, newline, level = level + 1)


def writeXmlFile(root_element, output_dir = '', file_name = 'behavior_file.xml') :
    if not ET.iselement(root_element) :
        raise ValueError("Failed to write xml file. Invalid element provided!")

    prettyXml(root_element, '\t', '\n')
    
    ET.dump(root_element)
    tree = ElementTree(root_element)

    if len(output_dir) == 0:
        print("Warning: 'output_dir' is not specified. Write file to ", os.getcwd())
        output_dir = os.getcwd()
    else :
        print("Generat", file_name, "to ", output_dir)

    tree.write(output_dir + '/behavior_file.xml', encoding='utf-8')

    


