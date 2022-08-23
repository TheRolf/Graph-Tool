from ast import literal_eval

import easygui

from face_free_cycle_cover.lp import lp
from face_free_cycle_cover.planar_tools import isInclusionFree, edges_of_cycle
from instance import Instance


class FaceFreeCycleCoverInstance(Instance):
    def __init__(self, vertices=None, edges=None, faces=None):
        super().__init__(vertices, edges, faces)
        self.fixed_faces = set()

    def solve(self, option='x'):
        if option == 'x':
            self.x_vec = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            self.title = "Random face-free 2-factor\n"

        elif option == 'y':
            x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            while isInclusionFree(self.faces, x.keys()):
                x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            self.x_vec = x
            self.title = "Random inclusion-free face-free 2-factor\n"

        elif option == 'z':
            x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            while not isInclusionFree(self.faces, x.keys()):
                x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            self.x_vec = x
            self.title = "Random inclusion-containing face-free 2-factor\n"

        elif option == 'n':
            self.x_vec = lp(self.faces, env=self.env, randomQ=True, faceFreeQ=False, fixEdges=self.input_parameter_edges)
            self.title = "Random 2-factor\n"

        # Counts as solved if the solution is not empty
        self.solvedQ = self.x_vec != {}

        if self.solvedQ:
            pass
        else:
            self.title += "No solution exists.\n"

    def set_input_parameter_edge_dialog(self, e):
        if self.input_parameter_edges[e] is None:
            self.input_parameter_edges[e] = True
        else:
            self.input_parameter_edges[e] = None

    def set_other_parameter_dialog(self):
        text_gui = easygui.enterbox("", f"Specify which face(s) to fix/release:")
        if text_gui:
            face_indices = literal_eval(f"[{text_gui}]")
            self.fixed_faces = self.fixed_faces.symmetric_difference(face_indices)
            edges_to_fix = edges_of_cycle([self.faces[int(i)] for i in self.fixed_faces])
            self.input_parameter_edges = {e: e in edges_to_fix for e in self.edges}

    def color_of_edge(self, u, v, textQ=False):
        if textQ:
            return ''  # '*' if self.input_parameter_edges[u, v] else ''
        else:
            return 'k' if self.input_parameter_edges[u, v] or self.solvedQ else 'gray'

    def width_of_edge(self, u, v):
        if (u, v) in self.x_vec:
            return 4
        elif self.input_parameter_edges[u, v]:
            return 2.5
        else:
            return 1.5

    def print_debug_info(self):
        print(f"x_vec = {self.x_vec}")
        print(f"fixed_faces = {self.fixed_faces}")
        print(f"input_parameter_edges = {[e for e in self.input_parameter_edges if self.input_parameter_edges[e]]}")
