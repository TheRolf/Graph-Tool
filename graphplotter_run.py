from graphplotter import GraphPlotter

"""
USAGE:
Left click:     placing new vertex/edge OR choosing existing vertex/edge
Right click:    (when a vertex being selected) moving the vertex to a new position
Delete:         deleting selected vertex/edge
Backspace:      clear worksheet
'c':            set input parameter of edge
'i':            enter edges of a new graph
'j':            enter edges of a new graph (graph6 format)
'd':            [console] debug information
'l':            [console] prints whether the graph is planar (lowercase L)
'p':            generates a planar layout
"""

if __name__ == '__main__':
    # Small test example
    vertices = {0: [1.5, 1.8], 1: [3.0, 2.6], 2: [4.3, 1.1], 3: [4.7, 3.1], 4: [5.5, 1.1], 5: [4.2, 4.2], 6: [5.7, 3.1]}
    edges = {(0, 1), (2, 4), (1, 2), (2, 3), (3, 6), (1, 3), (3, 5)}

    sandbox = GraphPlotter(vertices, edges)
    sandbox.start()
