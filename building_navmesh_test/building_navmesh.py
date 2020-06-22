import yaml
import os

from param_value import ParamValue
from lane_vertex import LaneVertex
from lane import Lane

yaml_data = {}
lane_vertices = []
lanes = []

def main():
    current_path = os.path.abspath(os.path.dirname(__file__))
    print(current_path)
    resource_path = current_path + "/../test/load_yaml_test"
    print(resource_path)
    file_name = "yaml_test.yaml"

    with open(resource_path + '/' + file_name) as file:
        temp = yaml.load(file.read())
        for yaml_value in temp.items():
            tmp_param = ParamValue(yaml_value)
            yaml_data[tmp_param.type] = tmp_param.value

if __name__ == "__main__":
    main()
    for it in yaml_data:
        if(it == "Vertex"):
            for idx, vtx in enumerate(yaml_data[it]):
                tmp = LaneVertex(vtx)
                lane_vertices.append(tmp)
                print(len(lane_vertices)-1) # get the insert id
                print(tmp.x, tmp.y)
        if(it == "Lanes"):
            for idx, l in enumerate(yaml_data[it]):
                tmp = Lane(l)
                lanes.append(l)
                lane_vertices[l[0]].setLanes(idx)
                lane_vertices[l[1]].setLanes(idx)
        
    for idx, vtx in enumerate(lane_vertices):
        print(idx)
        print(vtx.lanes)
