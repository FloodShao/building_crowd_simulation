import xml.etree.ElementTree as ET

class LeafElement:
    
    def __init__(self, name) :
        self._name = name
        self._attrib = {}
        self._text = None
        
    def addAttrib(self, key, value) :
        self._attrib[str(key)] = str(value)

    def setAttributes(self, attributes) :
        for key in attributes:
            self.addAttrib(key, attributes[key])

    def addText(self, text):
        self._text = str(text)

    def outputXmlElement(self):
        root = ET.Element(self._name, self._attrib)
        if self._text :
            root.text = self._text
        return root
