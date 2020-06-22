from vertex import Vertex
from lane_vertex import LaneVertex, LaneVertexManager
from lane import Lane, LaneManager
from vector import Vector2d
import util

class Polygon:
    
    def __init__(self):
        self.vertices = [] # store the actual vertices
        self.verticesIdSet = set()
        self.edges = set()
        self.obstacles = set()
        self.gradient = [0, 0, 0] # equations for plane Ax+By+C = 0
        # one node(convex polygon) can be either one intersection vertex or one lane
        self.intersect_vertex_id = -1
        self.intersect_lanes = [] # empty set
        self.lane_id = -1 

    def setID(self, id):
        self.id = id
    
    def getId(self):
        return self.id

    def addVertex(self, vertex):
        if(vertex.getId() in self.verticesIdSet):
            return
        self.verticesIdSet.add(vertex.getId())
        self.vertices.append(vertex)

    def getVertexSize(self):
        return len(self.vertices)

    def getVertex(self):
        return list(self.vertices)

    def addEdge(self, id):
        self.edges.add(id)

    def addEdges(self, edge_ids):
        for id in edge_ids:
            self.edges.add(id)
    
    def getEdge(self):
        return list(self.edges)
    
    def addObstacle(self, id):
        self.obstacles.add(id)

    def addObstacles(self, obstacle_ids):
        for id in obstacle_ids:
            self.obstacles.add(id)

    def setIntersectVertexId(self, lane_vertex_id):
        self.intersect_vertex_id = lane_vertex_id
    
    def getIntersectVertexId(self):
        return self.intersect_vertex_id

    def addIntersectLanes(self, lane_ids):
        for id in lane_ids:
            self.intersect_lanes.append(id)

    def setLaneId(self, lane_id):
        self.lane_id = lane_id

    def getLaneId(self):
        return self.lane_id
    

    def calCenter(self):
        num = len(self.vertices)
        if(num < 3):
            print("Is not a polygon")
        assert(num >= 3)
        X = 0.0
        Y = 0.0
        for vtx in self.vertices:
            X += vtx.x
            Y += vtx.y
        self.center = Vertex([X/num, Y/num])

    def getVar(self):
        result = []
        self.calCenter()
        result.append(self.center.getCoords())
        vertices_id = []
        for v in self.vertices:
            vertices_id.append(v.getId())
        result.append(vertices_id)
        result.append(self.gradient)
        result.append(self.edges)
        result.append(self.obstacles)
        return result


class PolygonManager:
    def __init__(self):
        self.polygons = []
        self.polygon_map = dict()

    def getSize(self):
        return len(self.polygons)

    def addPolygon(self, polygon):
        id = self.getSize()
        polygon.setID(id)
        self.polygons.append(polygon)

    def getPolygon(self, id):
        assert(id < self.getSize())
        return self.polygons[id]

    def updatePolygonSet(self, polygon):
        # if the polygon is an intersection node, should find the node by the intersection vertex
        if(polygon.getIntersectVertexId() != -1 and polygon.getLaneId() == -1):
            self.polygon_map[polygon.getIntersectVertexId()] = polygon.getId()
            ## debug purpose
            # print("update polygon set for polygon[ ", polygon.getId(), " ]")
        
    def getPolygonIdFromIntersectVertexId(self, intersect_vertex_id):
        if(intersect_vertex_id not in self.polygon_map):
            # did not find map key, might be a dead end vertex
            # print("Intersect_vertex_id:", intersect_vertex_id, " is not found in polygon map. Check function updatePolygonSet().")
            return -1
        
        return self.polygon_map[intersect_vertex_id]

    

    
            
