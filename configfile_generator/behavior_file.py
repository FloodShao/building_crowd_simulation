import xml.etree.ElementTree as ET

from .leaf_element import LeafElement, Element

class BehaviorFile (Element):
    
    def __init__(self) :
        Element.__init__(self, 'BFSM')

    def addState(self, state) :
        if not hasattr(state, "outputXmlElement"):
            raise ValueError("state provided is not an Element")
        self.addSubElement(state)

    def addTransition(self, transition) :
        if not hasattr(transition, "outputXmlElement"):
            raise ValueError("transition provided is not an Element")
        self.addSubElement(transition)

    def addGoalSet(self, goal_set) :
        if not hasattr(goal_set, "outputXmlElement"):
            raise ValueError("transition provided is not an Element")
        self.addSubElement(goal_set)


class BehaviorState (Element):
    def __init__(self) :
        Element.__init__(self, 'State')
        self.addAttribute('name', '')
        self.addAttribute('final', 0)
        self._goalSelector = GoalSelector()
        self._velComponent = VelComponent()

    def setStateName(self, name) :
        if len(name) != 0 :
            self.addAttribute('name', name)
        else :
            raise ValueError("invalid name provided for state name")

    def getStateName(self) :
        # from LeafElement
        return self._attrib['name']

    def setGoalSelector(self, goal_selector) :
        if not hasattr(goal_selector, "outputXmlElement"):
            raise ValueError("goal_selector provided is not an element!")
        self._goalSelector = goal_selector
        self.addSubElement(self._goalSelector)

    def setVelComponent(self, vel_component) :
        if not hasattr(vel_component, "outputXmlElement"):
            raise ValueError("vel_component provided is not an element!")
        self._velComponent = vel_component
        self.addSubElement(self._velComponent)
            
    def setFinalState(self) : 
        self.addAttribute('final', 1)
    
    def setUnFinalState(self) :
        self.addAttribute('final', 0)
    

class GoalSelector (LeafElement):

    def __init__(self) : 
        LeafElement.__init__(self, 'GoalSelector')
        self.addAttribute('dist', 'u')
        self.addAttribute('type', 'weighted')
        self.addAttribute('goal_set', -1) # not set
    
    def setGoalSetId(self, goal_set_id) :
        self.addAttribute('goal_set', goal_set_id)


class VelComponent (LeafElement): 

    def __init__(self) : 
        LeafElement.__init__(self, 'VelComponent')
        self.addAttribute('type', 'nav_mesh')
        self.addAttribute('heading_threshold', 15)
        self.addAttribute('file_name', '') # not set

    def setNavMeshFile(self, file_name) : 
        self.addAttribute('file_name', file_name)


class StateTransition (Element):

    def __init__(self) :
        Element.__init__(self, 'Transition')
        self.addAttribute('from', '')
        self.addAttribute('to', '')
        self._condition = TransitionCondition() 
    
    def setFromState(self, state) :
        if state.getStateName() != None :
            self.addAttribute('from', state.getStateName())
        else :
            raise ValueError("The transition FromState provided is not a xml element")

    def setFromStateName(self, state_name) :
        if len( state_name ) > 0 :
            self.addAttribute('from', state_name)
        else :
            raise ValueError("Invalid state name for state transition")

    def setToState(self, state):
        if state.getStateName() != None :
            self.addAttribute('to', state.getStateName())
        else :
            raise ValueError("The transition ToState provided is not a xml element")
    
    def setToStateName(self, state_name) :
        # to state can be None, as there might be a Target
        if not state_name:
            return
        if len( state_name ) > 0 :
            self.addAttribute('to', state_name)
        else :
            raise ValueError("Invalid state name for state transition")

    def setCondition(self, condition) :
        if not hasattr(condition, "outputXmlElement") :
            raise ValueError("Invalid transition condition provided!")
        self._condition = condition
        self.addSubElement(self._condition)


class TransitionCondition (LeafElement):

    def __init__(self) :
        LeafElement.__init__(self, 'Condition')
        self.addAttribute('distance', 0.0)
        self.addAttribute('type', 'goal_reached')
    
    def setConditionDistance(self, dist) :
        if(float(dist) > 0) :
            self.addAttribute('distance', dist)
        else :
            raise ValueError('invalid condition distance provided for TransitionCondition')


class GoalSet (Element): 

    def __init__(self) :
        Element.__init__(self, 'GoalSet')
        self.addAttribute('id', -1)
        self._goalList = []
        self._goal_area = set()
        self._capacity = 1

    def setId(self, id) :
        self.addAttribute('id', str(id))
    
    def addGoalArea(self, area) :
        self._goal_area.add(area)

    def setCapacity(self, capacity) :
        self._capacity = capacity

    def addGoal(self, goal) :
        goal.setId( len(self._goalList) )
        self._goalList.append(goal)
        self.addSubElement(goal)

    
class Goal (LeafElement):
    def __init__(self, id = -1) :
        # default id = -1, need to initialize
        LeafElement.__init__(self, 'Goal')
        self.addAttribute('id', -1)
        self.addAttribute('type', 'point')
        self.addAttribute('x', 0.0)
        self.addAttribute('y', 0.0)
        self.addAttribute('weight', 1.0)
        self.addAttribute('capacity', 1)

    def setCoord(self, x, y) :
        self.addAttribute('x', float(x))
        self.addAttribute('y', float(y))

    def setWeight(self, weight) :
        self.addAttribute('weight', float(weight))

    def setId(self, id) :
        self.addAttribute('id', int(id))

    def setCapacity(self, capacity) : 
        self.addAttribute('capacity', capacity)
