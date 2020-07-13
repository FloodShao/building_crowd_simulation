class ConfigureYAML:

    def __init__(self) :
        self._states = []
        self._transitions = []
        self._goalSet = []

    
class StateYAML:

    def __init__(self) :
        self._attributes = {}
        self._attributes['name'] = ''
        self._attributes['goal_set'] = ''
        self._attributes['navmesh_file_name'] = ''

    def getAttributes(self):
        return self._attributes

class TransitionYAML:

    def __init__(self) :
        self._attributes = {}
        self._attributes['from'] = ''
        self._attributes['to'] = ''
        self._attributes['condition_dist'] = 0.0

    def getAttributes(self):
        return self._attributes


class GoalSetYAML :
    
    def __init__(self) :
        self._attributes = {}
        self._attributes['set_id'] = ''
        self._attributes['set_area'] = {}
        self._attributes['capacity'] = 1

    def getAttributes(self):
        return self._attributes
