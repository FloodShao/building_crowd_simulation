class Vertex:

    def __init__(self, yaml_node):
        self.x = float(yaml_node[0])
        self.y = float(-yaml_node[1]) # oppsite direction of y, following the design of traffic editor
        self.z = float(yaml_node[2]) # currently keep z = 0
        self.name = str(yaml_node[3]) # indicate the goal area
        self.params = None
        # some vertices do not have the 5th param
        if len(yaml_node) >= 5 :
            self.params = yaml_node[4]

    def xy(self):
        return (self.x, self.y)

    def getName(self):
        return self.name
    
    def getParams(self):
        return self.params
