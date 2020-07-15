from .behavior_file import *
from .scene_file import *


class PointYAML :
    def __init__(self, x, y) :
        self._x = float(x)
        self._y = float(y)
        # for agent point
        self._name = 'GroupId' 

    def params(self, key, value) :
        self._params[key] = value

    def get(self, key) :
        if self._params and key in self._params :
            return self._params[key]
        raise ValueError("Invalid key provided")

class BasicYAML :
    def __init__(self):
        self._attributes = {}

    def getAttributes(self):
        return self._attributes

    def load(self, yaml_node):
        for key in yaml_node :
            self._attributes[key] = yaml_node[key]

class StateYAML:

    def __init__(self) :
        self._attributes = {}
        self._attributes['name'] = ''
        self._attributes['goal_set'] = ''
        self._attributes['navmesh_file_name'] = ''
        self._attributes['final'] = 0

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

            if key == "final" :
                self._attributes['final'] = yaml_node[key]
        
        if not self._attributes['final'] : 
            B_state.setUnFinalState()
            B_state.setGoalSelector(B_goal_selector)
            B_state.setVelComponent(B_vel_component)
        else :
            B_state.setFinalState()

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



class GoalsYAML :
    def __init__(self) :
        self._goals = {}

    def loadGoal(self, yaml_node) :
        for g in yaml_node :
            area = g[3]
            goal = PointYAML(g[0], g[1])

            if not area in self._goals :
                self._goals[area] = []
            
            self._goals[area].append(goal)

    def getGoals(self, area):
        return self._goals[area]


class AgentProfileYAML (BasicYAML):
    def __init__(self):
        BasicYAML.__init__(self)
        self._attributes['name'] = None

        self._attributes['class'] = 'agentClassId'
        self._attributes['max_accel'] = 5
        self._attributes['max_angle_vel'] = 360
        self._attributes['max_neighbors'] = 10
        self._attributes['max_speed'] = 0
        self._attributes['neighbor_dist'] = 5
        self._attributes['obstacleSet'] = 'obstacleSetId'
        self._attributes['pref_speed'] = 0
        self._attributes['r'] = 0.2

        self._attributes['ORCA_tau'] = 1.0
        self._attributes['ORCA_tauObst'] = 0.4

    def load(self, yaml_node):
        keys = yaml_node.keys()

        if len(keys) < len(self.getAttributes()) :
            raise ValueError("There are unspecified parameters for AgentProfile")
        
        if len(yaml_node['name']) == 0:
            raise ValueError("Invalid AgentProfile name provided")
        
        self._attributes['name'] = yaml_node['name']
        agent_profile = AgentProfile(yaml_node['name'])

        # verify the parent method is working
        BasicYAML.load(self, yaml_node)
        
        for key in keys:
            if key == 'class' or \
                key == 'max_accel' or \
                key == 'max_angle_vel' or \
                key == 'max_neighbors' or \
                key == 'max_speed' or \
                key == 'neighbor_dist' or \
                key == 'obstacleSet' or \
                key == 'pref_speed' or \
                key == 'r'  :
                agent_profile.setProfileCommon(key, yaml_node[key])
            if key == 'ORCA_tau' or \
                key == 'ORCA_tauObst' :
                agent_profile.setProfileORCA(key[5:], yaml_node[key])

        return agent_profile

class AgentGroupYAML (BasicYAML):
    def __init__(self):
        BasicYAML.__init__(self)
        self._attributes['GroupId'] = None
        self._attributes['profile_selector'] = None
        self._attributes['state_selector'] = None
        self._agent_group = None

    def load(self, yaml_node):
        keys = yaml_node.keys()

        if not 'GroupId' in keys or not 'profile_selector' in keys or not 'state_selector' in keys :
            raise ValueError("Invalid AgentGroup YAML provided.")

        BasicYAML.load(self, yaml_node)

        self._agent_group = AgentGroup(self._attributes['profile_selector'], self._attributes['state_selector'])
        return self._agent_group

    def loadAgents(self, agents_list_yaml) :
        agents_list = agents_list_yaml.getAgentsGroup(self._attributes['GroupId'])
        if not agents_list or not self._agent_group:
            print("No agents are loaded.")
            return 

        for agent in agents_list :
            # agent is type of PointXML
            self._agent_group.addAgent(agent._x, agent._y)

        return self._agent_group


class AgentsListYAML:
    # not needed in generating the template YAML list
    def __init__(self):
        self._agents = {}

    def load(self, yaml_node):
        for agent in yaml_node :
            group_id = str(agent[2])
            if not group_id in self._agents :
                self._agents[group_id] = []
            self._agents[group_id].append(PointYAML(agent[0], agent[1]))

    def allGroupId(self):
        return self._agents.keys()

    def getAgentsGroup(self, group_id):
        if not str(group_id) in self.allGroupId() :
            print("No agent for [", group_id, "] listed in conf_yaml")
            return None
        
        return self._agents[str(group_id)]


class ObstacleSetYAML (BasicYAML) :
    def __init__(self) :
        BasicYAML.__init__(self)
        self._attributes['class'] = 'obstacleSetId'
        self._attributes['file_name'] = None
        self._attributes['type'] = 'nav_mesh'
        self._obstacle_set = None

    def load(self, yaml_node) :
        BasicYAML.load(self, yaml_node)

        if not self._attributes['file_name']:
            raise ValueError("Invalid file_name provided for obstacle set.")

        self._obstacle_set = ObstacleSet()
        self._obstacle_set.setNavMeshFile(self._attributes['file_name'])
        self._obstacle_set.setClassId(self._attributes['class'])
        return self._obstacle_set        
        
