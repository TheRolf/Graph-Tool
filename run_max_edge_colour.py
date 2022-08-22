from graphplotter import GraphPlotter
from instance_max_edge_colour import MaxEdgeColourInstance

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

'c':            set colour of edge

'x':            running the LP and showing an optimal colouring (requires Gurobi license)
'y':            running the LP and showing an optimal colouring with a unique colour for each pendant edge 
'z':            running the LP and showing an optimal colouring with a unique colour for each fixed-colour edge 
'm':            running the LP and showing an optimal colouring subject to all pendant edges having the same colour
'n':            running the LP and showing an optimal colouring subject to all pendant edges having the same unique colour

"""


class GraphPlotterMaxEdgeClr(GraphPlotter):
    def __init__(self, points=None, edges=None):
        super().__init__(points=points, edges=edges)
        self.instance = MaxEdgeColourInstance(self.coordinates.keys(), edges)


if __name__ == '__main__':
    # Small test example
    vertices = {0: [1.5, 1.8], 1: [3.0, 2.6], 2: [4.3, 1.1], 3: [4.7, 3.1], 4: [5.5, 1.1], 5: [4.2, 4.2], 6: [5.7, 3.1]}
    edges = {(0, 1), (2, 4), (1, 2), (2, 3), (3, 6), (1, 3), (3, 5)}

    # Tobias's evil matching counterexample
    # vertices = {0: [3.4, 3.6], 1: [0.3, 3.4], 2: [3.4, 3.1], 3: [0.3, 3.1], 4: [3.3, 2.3], 5: [0.3, 2.7], 6: [0.2, 2.2], 7: [5.0, 3.8], 8: [7.7, 4.0], 9: [7.7, 3.5], 10: [5.1, 2.4], 11: [7.6, 3.1], 12: [7.7, 2.6], 13: [5.0, 3.1], 14: [0.2, 3.8], 15: [7.7, 4.4], 16: [0.2, 1.6], 17: [7.7, 1.9]}
    # edges = [(0, 1), (2, 3), (4, 5), (4, 6), (2, 6), (1, 2), (1, 4), (0, 3), (0, 5), (3, 4), (2, 5), (0, 6), (0, 7), (2, 7), (4, 7), (7, 8), (7, 9), (8, 10), (0, 10), (2, 10), (4, 10), (9, 10), (10, 11), (7, 11), (12, 13), (8, 13), (9, 13), (11, 13), (10, 12), (7, 12), (0, 13), (2, 13), (4, 13), (0, 14), (2, 14), (4, 14), (7, 15), (10, 15), (13, 15), (0, 16), (2, 16), (4, 16), (13, 17), (10, 17), (7, 17)]

    # 4-cycles complementing matching edges
    # vertices = {0: [6.7, 2.5], 1: [5.9, 4.6], 2: [5.9, 4.1], 3: [0.9, 4.2], 4: [1.3, 4.7], 5: [5.7, 3.6], 6: [5.6, 3.0], 7: [1.4, 3.1], 8: [0.8, 3.6], 9: [0.4, 2.5], 10: [1.1, 1.8], 11: [6.6, 1.6]}
    # edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (0, 11), (1, 4), (3, 6), (5, 8), (7, 10), (0, 9), (2, 11)]

    # K_{3,3,3}
    # vertices = {0: [1.5, 3.9], 1: [3.9, 4.0], 2: [6.6, 4.0], 3: [1.7, 2.9], 4: [4.0, 3.0], 5: [6.7, 3.0], 6: [1.8, 2.0], 7: [3.9, 2.1], 8: [6.8, 2.0]}
    # edges = [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (0, 4), (2, 4), (2, 7), (0, 7), (4, 6), (4, 8), (1, 8), (1, 6), (1, 3), (1, 5), (3, 7), (5, 7)]

    # OPT = 3/2 * |M| example
    # vertices = {0: [1.0, 4.7], 1: [6.7, 4.6], 2: [0.9, 4.1], 3: [6.9, 2.9], 4: [1.1, 3.4], 5: [6.7, 3.4], 6: [0.9, 2.9], 7: [6.6, 4.2], 8: [1.0, 2.2], 9: [1.0, 1.7], 10: [6.6, 2.3], 11: [6.6, 1.8], 12: [6.7, 1.3], 13: [6.6, 0.9], 14: [1.0, 1.2], 15: [1.0, 0.9]}
    # edges = [(0, 1), (2, 3), (4, 5), (6, 7), (2, 5), (4, 7), (0, 3), (2, 7), (9, 11), (8, 11), (6, 10), (4, 10), (6, 11), (8, 10), (0, 5), (9, 12), (9, 13), (12, 14), (13, 14), (1, 14), (13, 15), (1, 15), (3, 15), (8, 12)]

    sandbox = GraphPlotterMaxEdgeClr(vertices, edges)
    sandbox.start()
