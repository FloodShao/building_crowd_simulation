class Vertex:

    def __init__(self, yaml_node):
        self.x = float(yaml_node[0])
        self.y = float(-yaml_node[1]) # oppsite direction of y, following the design of traffic editor
        self.z = float(yaml_node[2]) # currently keep z = 0
        self.name = yaml_node[3]

    def xy(self):
        return (self.x, self.y)
