from face_free_cycle_cover.nonhamiltonians import *
from graphplotter import GraphPlotter
from instance_face_free_cycle_cover import FaceFreeCycleCoverInstance

"""
USAGE:
Left click:     placing new vertex/edge OR choosing existing vertex/edge
Right click:    (when a vertex being selected) moving the vertex to a new position
Delete:         deleting selected vertex/edge
Backspace:      clear worksheet
'i':            enter edges of a new graph
'j':            enter edges of a new graph (graph6 format)
'd':            [console] debug information
'l':            [console] prints whether the graph is planar (lowercase L)
'p':            generates a planar layout

'c':            fixing selected edge in solution
'v'             fixing specified face in solution

'x':            calculating a random face-free 2-factor (optionally using fixed edges)
'y':            calculating a random face-free and inclusion-free 2-factor (optionally using fixed edges)
'z':            calculating a random face-free and inclusion-containing 2-factor (optionally using fixed edges)
'm':            -
'n':            calculating a random 2-factor
"""


class GraphPlotterFaceFree(GraphPlotter):
    def __init__(self, points=None, edges=None, faces=None):
        super().__init__(points=points, edges=edges, faces=faces)
        self.instance = FaceFreeCycleCoverInstance(self.coordinates.keys(), edges, faces)


if __name__ == '__main__':
    faces, points = C5CP_52a()
    sandbox = GraphPlotterFaceFree(points=points, faces=faces)
    sandbox.start()
