from .lane import Lane, LaneManager
from .lane_vertex import LaneVertex, LaneVertexManager
from .util import ConnectionManager, PolygonFactory
from .polygon import Polygon, PolygonManager
from .vertex import Vertex, VertexManager
from .edge import Edge, EdgeManager
from .util import FileWriter
from .obstacle import Obstacle, ObstacleManager

file_name = "test_navmesh.nav"

if __name__ == "__main__":

    laneVertexManager = LaneVertexManager()
    laneManager = LaneManager()
    polygonManager = PolygonManager()
    vertexManager = VertexManager()
    edgeManager = EdgeManager()
    obstacleManager = ObstacleManager()

    polygonFactory = PolygonFactory(polygonManager, laneVertexManager, laneManager, vertexManager, edgeManager, obstacleManager)

    laneVertexManager.addLaneVertex(LaneVertex([18.83, -3.85]))
    laneVertexManager.addLaneVertex(LaneVertex([18.79, -6.92]))
    laneVertexManager.addLaneVertex(LaneVertex([18.81, -10.92]))
    laneVertexManager.addLaneVertex(LaneVertex([15.22, -11.02]))
    laneVertexManager.addLaneVertex(LaneVertex([11.47, -10.92]))
    laneVertexManager.addLaneVertex(LaneVertex([11.37, -7.07]))
    laneVertexManager.addLaneVertex(LaneVertex([15.06, -6.96]))
    laneVertexManager.addLaneVertex(LaneVertex([10.02, -3.85]))
    laneVertexManager.addLaneVertex(LaneVertex([9.07, -5.48]))
    laneVertexManager.addLaneVertex(LaneVertex([7.05, -10.86]))
    laneVertexManager.addLaneVertex(LaneVertex([6.88, -2.03]))


    laneManager.addLane(Lane([0, 1, 1.0]))
    laneManager.addLane(Lane([1, 2, 1.0]))
    laneManager.addLane(Lane([2, 3, 1.0]))
    laneManager.addLane(Lane([1, 6, 1.0]))
    laneManager.addLane(Lane([3, 6, 1.0]))
    laneManager.addLane(Lane([3, 4, 1.5]))
    laneManager.addLane(Lane([6, 5, 1.0]))
    laneManager.addLane(Lane([4, 5, 1.0]))
    laneManager.addLane(Lane([4, 9, 0.8]))
    laneManager.addLane(Lane([5, 8, 2.0]))
    laneManager.addLane(Lane([8, 9, 1.5]))
    laneManager.addLane(Lane([7, 8, 1.5]))
    laneManager.addLane(Lane([0, 7, 1.5]))
    laneManager.addLane(Lane([7, 10, 1.0]))

    connectionManager = ConnectionManager(laneVertexManager, laneManager)
    connectionManager.buildConnection()

    ## add intersection vertices as node, only intersection node generates polygon vertices
    for lane_vertex_id in range(laneVertexManager.getSize()):
        lane_vertex = laneVertexManager.getLaneVertex(lane_vertex_id)
        if(len(lane_vertex.getLanes()) < 2):
            continue

        polygon = Polygon()
        polygon.setIntersectVertexId( lane_vertex_id )
        polygon.addIntersectLanes(lane_vertex.getLanes())
        polygonFactory.intersectionPolygonUpdate(polygon)

    ## add lane as node
    for lane_id in range(laneManager.getSize()):
        polygon = Polygon()
        polygon.setLaneId(lane_id)
        polygonFactory.lanePolygonUpdate(polygon)

    
    ## Python write file
    navmesh_file = FileWriter(file_name)
    navmesh_file.setDataManager(vertexManager=vertexManager, edgeManager=edgeManager, obstacleManager=obstacleManager, polygonManager=polygonManager)
    navmesh_file.openFile()
    navmesh_file.generateNavMesh()
    navmesh_file.closeFile()
