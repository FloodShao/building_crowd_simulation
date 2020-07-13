import yaml

class Goal:
    def __init__(self, cood):
        self.cood = cood

    def __repr(self):
        return "%s(%r)" % (self.__class__.__name__, self.cood)

f = open("test.yaml", "w+")

yaml.dump(Goal([1,2]), f)