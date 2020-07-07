import yaml
import sys
import os

from building_navmesh.build_navmesh import BuildNavmesh

class NavmeshGenerator:
    def __init__(self, vertices, lanes, graph_idx):
        self._vertices_raw = vertices
        self._lanes_raw = lanes
        self._graph_idx = graph_idx
        self._navmeshManager = BuildNavmesh()

        lane_vertices_number = self.LoadLaneVertices()
        print("Load lane vertices of ", lane_vertices_number)
        
        lane_number = self.LoadLanes()        
        if lane_number <= 0:
            print("Error loading human lanes")
            return
        print("Load human lanes of", lane_number)

    
    # wrap up building_navmesh api
    def AddLaneVertex(self, px, py):
        self._navmeshManager.AddLaneVertex(px, py)

    def AddLane(self, idx0, idx1, width):
        self._navmeshManager.AddLane(idx0, idx1, width)

    def Generate(self):
        self._navmeshManager.Process()

    def Output(self, output_file_path):
        self._navmeshManager.Output(output_file_path)
    
    # add all lane vertices  
    def LoadLaneVertices(self):
        count = 0
        for v in self._vertices_raw:
            if v[2] != self._graph_idx:
                continue
            self.AddLaneVertex(v[0], v[1])
            count += 1
        self._lane_vertices_number = count
        return count

    def LoadLanes(self):
        count = 0
        for l in self._lanes_raw:
            if l[2]['graph_idx'][1] != self._graph_idx:
                continue
            # make sure the width is double
            width = l[2]['width'][1] / 1.0
            
            if l[0] > self._lane_vertices_number or l[1] > self._lane_vertices_number :
                print("Error load lanes for lane, [vertices_idx over stored vertices_number]", l)
                return -1
                        
            self.AddLane(l[0], l[1], width)
            count += 1
        self._lane_number = count
        return count


class BuildingYamlParse:
    
    def __init__(self, map_path):
        self._building_file = map_path
        with open(self._building_file) as f :
            _yaml_raw = yaml.load(f, yaml.SafeLoader)
            self._level_raw = _yaml_raw['levels']
        
        if not self._level_raw:
            print("Error loading map file: ", map_path)
            return
        
        self._level_number = len(self._level_raw)
        self._level_keys = list(self._level_raw.keys())

    def GetLevelRawData(self, level_id):
        if level_id > self._level_number :
            print("Error finding level id for ", level_id, ". Total level number is ", self._level_number)
            return
        key = self._level_keys[level_id]
        return self.GetLevelRawDataFromKey(key)
        
    def GetLevelRawDataFromKey(self, key):
        if not key in self._level_keys:
            print("Invalid level name: ", key)
            return
        return self._level_raw[key]
    

def main():
    if len(sys.argv) > 1 :
        map_path = sys.argv[1]
    elif 'RMF_MAP_PATH' in os.environ:
        map_path = os.environ['RMF_MAP_PATH']
    else:
        print('map path must be provided in command line or RMF_MAP_PATH env')
        sys.exit(1)
        raise ValueError('Map path not provided')

    if not os.path.exists(map_path) :
        print('map path does not exist!')
        sys.exit(1)
        raise ValueError('Map path not exist!')

    if len(sys.argv) > 2:
        output_folder_path = sys.argv[2]
        if not os.path.exists(output_folder_path) :
            print("Invalid output folder path: ", output_folder_path)
            sys.exit(1)
            raise ValueError('output folder path not exist!')
    else:
        output_folder_path = "navmesh_output/"
        if not os.path.exists(output_folder_path) :
            os.mkdir(output_folder_path)

    yaml_parse = BuildingYamlParse(map_path)

    for level_name in yaml_parse._level_keys :
        output_file = output_folder_path + level_name + "_navmesh.nav"
        vertices = yaml_parse.GetLevelRawDataFromKey(level_name)['vertices']
        human_lanes = yaml_parse.GetLevelRawDataFromKey(level_name)['human_lanes']
        
        # TODO, add graph_id support
        navmesh_generator = NavmeshGenerator(vertices, human_lanes, 0)
        navmesh_generator.Generate()
        navmesh_generator.Output(output_file)


if __name__ == "__main__":
    sys.exit(main())