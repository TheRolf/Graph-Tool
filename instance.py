import gurobipy

from tools import edge, pairs


class Instance:
    env = gurobipy.Env(empty=True)
    env.setParam('LogToConsole', 0)
    env.start()

    def __init__(self, vertices=None, edges=None, faces=None):
        self.vertices = set(vertices or [])
        self.edges = set(edges or [])
        self.faces = faces or [(), ]

        self.f_obj = 0
        self.x_vec = {}
        self.solvedQ = False
        self.message = ""

        self.input_parameter_edges = {e: None for e in self.edges}
        self.input_parameter_vertices = {v: None for v in self.vertices}

    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.add(v)
            self.input_parameter_vertices[v] = None

    def add_edge(self, u, v):
        e = edge([u, v])
        if e not in self.edges:
            self.vertices.add(u)
            self.vertices.add(v)
            self.edges.add(e)
            self.input_parameter_edges[e] = None
            self.update()

    def set_input_parameter_edge(self, e, c):
        self.input_parameter_edges[e] = c

    def color_of_edge(self, u, v, textQ=False):
        return '' if textQ else 'k'

    def update(self):
        self.f_obj = 0
        self.x_vec = {}
        self.solvedQ = False
        self.message = ""

    def delete_vertex(self, v):
        self.vertices.remove(v)
        del self.input_parameter_vertices[v]
        self.edges = set(e for e in self.edges if v not in e)
        self.faces = [face for face in self.faces if v not in face]
        self.update()

    def delete_edge(self, e):
        e = edge(e)
        self.edges.remove(e)
        del self.input_parameter_edges[e]
        self.faces = [face for face in self.faces if e not in pairs(face)]
        self.update()

    def solve(self, option='x'):
        pass

    def print_debug_info(self):
        print(f"x_vec = {self.x_vec}")
