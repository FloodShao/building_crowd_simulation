from .behavior_file import *

    
class StateYAML:

    def __init__(self) :
        self._attributes = {}
        self._attributes['name'] = ''
        self._attributes['goal_set'] = ''
        self._attributes['navmesh_file_name'] = ''

    def load(self, yaml_node):
        keys = yaml_node.keys()

        B_state = BehaviorState()
        B_goal_selector = GoalSelector()
        B_vel_component = VelComponent()

        for key in keys :
            if key == "name" :
                self._attributes['name'] = yaml_node[key]
                B_state.setStateName(yaml_node[key])
            
            if key == "goal_set" :
                self._attributes['goal_set'] = yaml_node[key]
                B_goal_selector.setGoalSetId(yaml_node[key])

            if key == "navmesh_file_name" :
                self._attributes['navmesh_file_name'] = yaml_node[key]
                B_vel_component.setNavMeshFile(yaml_node[key])

        B_state.setGoalSelector(B_goal_selector)
        B_state.setVelComponent(B_vel_component)

        return B_state

    def getAttributes(self):
        return self._attributes

class TransitionYAML:

    def __init__(self) :
        self._attributes = {}
        self._attributes['from'] = ''
        self._attributes['to'] = ''
        self._attributes['condition_dist'] = 0.0
        # self._attributes['condition_type'] = 'goal_reached'

    def load(self, yaml_node) :
        keys = yaml_node.keys()

        B_transition = StateTransition()
        B_transition_condition = TransitionCondition()

        for key in keys :
            if key == "from" :
                self._attributes['from'] = yaml_node[key]
                B_transition.setFromStateName(yaml_node[key])
            if key == "to" :
                self._attributes['to'] = yaml_node[key]
                B_transition.setToStateName(yaml_node[key])
            if key == "condition_dist" :
                self._attributes['condition_dist'] = float(yaml_node[key])
                B_transition_condition.setConditionDistance( float(yaml_node[key]) )
        
        B_transition.setCondition(B_transition_condition)

        return B_transition

    def getAttributes(self):
        return self._attributes


class GoalSetYAML :
    
    def __init__(self) :
        self._attributes = {}
        self._attributes['set_id'] = ''
        self._attributes['set_area'] = set()
        self._attributes['capacity'] = 1

    def load(self, yaml_node) :
        keys = yaml_node.keys()
        
        B_goal_set = GoalSet()

        for key in keys :
            if key == "set_id" :
                self._attributes['set_id'] = yaml_node[key]
                B_goal_set.setId(yaml_node[key])
            if key == "set_area" :
                for area in yaml_node[key] :
                    self._attributes['set_area'].add(area)
                    B_goal_set.addGoalArea(area)
            if key == "capacity" :
                self._attributes['capacity'] = yaml_node[key]
                B_goal_set.setCapacity(yaml_node[key])

        # haven't initialize each goal
        return B_goal_set

    def getAttributes(self):
        return self._attributes

class GoalYAML :
    def __init__(self, x, y) :
        self._x = float(x)
        self._y = float(y)

class GoalsYAML :
    def __init__(self) :
        self._goals = {}

    def loadGoal(self, yaml_node) :
        for g in yaml_node :
            area = g[3]
            goal = GoalYAML(g[0], g[1])

            if not area in self._goals :
                self._goals[area] = []
            
            self._goals[area].append(goal)

    def getGoals(self, area):
        return self._goals[area]
