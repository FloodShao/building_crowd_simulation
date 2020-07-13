import xml.etree.ElementTree as ET

from .leaf_element import LeafElement

class BehaviorState :

    def __init__(self) :
        self._name = None
        self._final = False
        self._goalSelector = None
        self._velComponent = None

    def setStateName(self, name) :
        if len(name) != 0 :
            self._name = str(name)
        else :
            raise ValueError("invalid name provided for state name")

    def getStateName(self) :
        return self._name

    def setGoalSelector(self, goal_selector) :
        if  goal_selector.getGoalSetId() != None :
            self._goalSelector = goal_selector
        else :
            raise ValueError("goal_selector provided does not configure a goal set!")

    def setVelComponent(self, vel_component) :
        if vel_component.getNavMeshFile() != None :
            self._velComponent = vel_component
        else :
            raise ValueError("vel_component provided does not configure a navmesh file!")
    
    def setFinalState(self) : 
        self._final = True
    
    def setUnFinalState(self) :
        self._final = False
    
    def outputXmlElement(self) :
        if(not self._name or self._goalSelector or self._velComponent) :
            raise ValueError("Incomplete element for State.")
        
        root = Element('State')
        
        # attribute
        if self._final : 
            root.set('final', '1')
        else :
            root.set('final', '0')
        root.set('name', self._name)

        goal_selector_xml = LeafElement('GoalSelector')
        goal_selector_xml.setAttributes(self._goalSelector.getAttributes())
        root.append(goal_selector_xml)

        vel_component_xml = LeafElement('VelComponent')
        vel_component_xml.setAttributes(self._velComponent.getAttributes())
        root.append(vel_component_xml)
        
        return root

class GoalSelector :

    def __init__(self) : 
        self._attributes = {}
        self._attributes['dist'] = 'u'
        self._attributes['type'] = 'weighted'
        self._attributes['goal_set'] = None
    
    def setGoalSetId(self, goal_set_id) :
        self._attributes['goal_set'] = str(goal_set_id)

    def getGoalSetId(self) :
        return self._attributes['goal_set']

    def getAttributes(self):
        return self._attributes


class VelComponent : 

    def __init__(self) : 
        self._attributes = {}
        self._attributes['type'] = 'nav_mesh'
        self._attributes['heading_threshold'] = str(15)
        self._attributes['file_name'] = None

    def setNavMeshFile(self, file_name) : 
        self._attributes['file_name'] = file_name

    def getNavMeshFile(self) :
        return self._attributes['file_name']
    
    def getAttributes(self) :
        return self._attributes


class StateTransition :
    def __init__(self) : 
        self._fromStateName = None
        self._toStateName = None
        self._condition = None
    
    def setFromState(self, state) :
        if state.getStateName() != None :
            self._fromStateName = state.getStateName()
        else :
            raise ValueError("The transition FromState provided is not a xml element")

    def setToState(self, state):
        if state.getStateName() != None :
            self._toStateName = state.getStateName()
        else :
            raise ValueError("The transition ToState provided is not a xml element")

    def setCondition(self, condition) :
        if condition.getConditionDistance() != None :
            self._condition = condition
        else :
            raise ValueError("Invalid transition condition provided!")

    def outputXmlElement(self) :
        if not self._fromStateName or not self._toStateName or not self._condition :
            raise ValueError("Incomplete element for transition.")
        
        root = ET.Element('Transition')
        root.set('from', self._fromStateName)
        root.set('to', self._toStateName)

        condition_xml = LeafElement('Condition')
        condition_xml.setAttributes(self._condition.getAttributes())
        root.append(condition_xml)
        return root


class TransitionCondition:

    def __init__(self) :
        self._attributes = {}
        self._attributes['distance'] = None
        self._attributes['type'] = 'goal_reached'
    
    def setConditionDistance(self, dist) :
        if(float(dist) > 0) :
            self._attributes['distance'] = str(dist)
        else :
            raise ValueError('invalid condition distance provided for TransitionCondition')

    def getConditionDistance(self) :
        return self._attributes['distance']

    def getAttributes(self):
        return self._attributes


class GoalSet : 

    def __init__(self, id) :
        self._id = id
        self._goalList = []
    
    def addGoal(self, goal) :
        goal.setId( len(self._goalList) )

    def outputXmlElement(self) :
        root = ET.Element('GoalSet', {'id' : self._id})

        for goal in self._goalList :
            goal_attributes = goal.getAttributes()
            goal_element = LeafElement('Goal')
            goal_element.setAttributes(goal_attributes)
            root.append(goal_element.outputXmlElement())
        return root

    
class Goal :
    
    def __init__(self, id = -1) :
        # default id = -1, need to initialize
        self._id = id
        self._type = 'point'
        self._x = 0.0
        self._y = 0.0
        self._capacity = 1
        self._weight = 1.0

    def setCoord(self, x, y) :
        self._x = float(x)
        self._y = float(y)

    def setWeight(self, weight) :
        self._weight = float(weight)

    def setId(self, id) :
        self._id = int(id)

    def setCapacity(self, capacity) : 
        self._capacity = int(capacity)

    def getAttributes(self):
        if self._id < 0 : 
            raise ValueError("The Goal id is ", self._id, ". Please initialize the goal first!")
        
        result = {}
        result['id'] = str(self._id)
        result['capacity'] = str(self._capacity)
        result['type'] = str(self._type)
        result['weight'] = str(self._weight)
        result['x'] = str(self._x)
        result['y'] = str(self._y)

        return result


class BehaviorFile :
    
    def __init__(self) :
        self._states = []
        self._transitions = []
        self._goalSets = []

    def addState(self, State) :
        self._states.append(State)

    def addTransitions(self, Transition) :
        self._transitions.append(Transition)

    def addGoalSet(self, GoalSet) :
        self._goalSets.append(GoalSet)

    def outputXmlElement(self):
        root = ET.Element('BFSM')

        for state in self._states :
            root.append(state.outputXmlElement())

        for transition in self._transitions :
            root.append(transition.outputXmlElement())

        for goalset in self._goalSets :
            root.append(goalset.outputXmlElement())
        
        return root

        
