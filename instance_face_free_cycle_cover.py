from face_free_cycle_cover.lp import lp
from face_free_cycle_cover.planar_tools import isInclusionFree
from instance import Instance


class FaceFreeCycleCoverInstance(Instance):
    def __init__(self, vertices=None, edges=None, faces=None):
        super().__init__(vertices, edges, faces)

    def solve(self, option='x'):
        if option == 'x':
            self.x_vec = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            self.message = "Random face-free 2-factor\n"

        elif option == 'y':
            x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            while isInclusionFree(self.faces, x.keys()):
                x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            self.x_vec = x
            self.message = "Random inclusion-free face-free 2-factor\n"

        elif option == 'z':
            x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            while not isInclusionFree(self.faces, x.keys()):
                x = lp(self.faces, env=self.env, randomQ=True, fixEdges=self.input_parameter_edges)
            self.x_vec = x
            self.message = "Random inclusion-containing face-free 2-factor\n"

        elif option == 'n':
            self.x_vec = lp(self.faces, env=self.env, randomQ=True, faceFreeQ=False, fixEdges=self.input_parameter_edges)
            self.message = "Random 2-factor\n"

        # Counts as solved if the solution is not empty
        self.solvedQ = self.x_vec != {}

        if self.solvedQ:
            pass
        else:
            self.message += "No solution exists.\n"

    def color_of_edge(self, u, v, textQ=False):
        if textQ:
            return ''
        else:
            return 'k'

    def width_of_edge(self, u, v):
        return 4 if (u, v) in self.x_vec else 1.5
