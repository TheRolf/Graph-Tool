import easygui
import networkx as nx
import seaborn as sns

from instance import Instance
from max_edge_colour.lp import lp
from max_edge_colour.preprocess import isNormalizedQ


class MaxEdgeColourInstance(Instance):
    def __init__(self, vertices=None, edges=None, faces=None):
        super().__init__(vertices, edges, faces)
        self.colour_calc = {}

    def color_of_edge(self, u, v, textQ=False):
        if self.solvedQ:
            return (f"{self.input_parameter_edges[u, v]}*" if self.input_parameter_edges[u, v] else str(self.x_vec[u, v])) if textQ else self.colour_calc[self.x_vec[u, v]-1]
        else:
            return (f"{self.input_parameter_edges[u, v]}*" if self.input_parameter_edges[u, v] else '') if textQ else 'k'

    def update(self):
        super().update()
        self.colour_calc = {}

    def set_input_parameter_edge_dialog(self, e):
        text_gui = easygui.enterbox("", f"Set colour for edge {e}")
        c = None if text_gui in ['', '0', None] else int(text_gui)
        labels = [label for f, label in self.input_parameter_edges.items() if f != e and label]
        max_label = 0 if labels == [] else max(labels)
        if c <= max_label:
            self.input_parameter_edges[e] = c
        else:
            self.input_parameter_edges[e] = max_label + 1

    def solve(self, option='x'):
        if option == 'x':
            self.f_obj, self.x_vec = lp(self.input_parameter_edges, env=self.env)
            self.message = "Maximum Edge 2-Coloring: no constraints\n"
        elif option == 'y':
            self.f_obj, self.x_vec = lp(self.input_parameter_edges, env=self.env, leavesUniqueQ=True)
            self.message = "Maximum Edge 2-Coloring: unique pendant edge colours\n"
        elif option == 'z':
            self.f_obj, self.x_vec = lp(self.input_parameter_edges, env=self.env, fixedUniqueQ=True)
            self.message = "Maximum Edge 2-Coloring: unique fixed colours\n"
        elif option == 'm':
            self.f_obj, self.x_vec = lp(self.input_parameter_edges, env=self.env, leavesMonoQ=True, blockLeaveColourQ=False)
            self.message = "Maximum Edge 2-Coloring: monochromatic pendant edges\n"
        elif option == 'n':
            self.f_obj, self.x_vec = lp(self.input_parameter_edges, env=self.env, leavesMonoQ=True, blockLeaveColourQ=True)
            self.message = "Maximum Edge 2-Coloring: monochromatic pendant edges with unique colour\n"

        # Counts as solved if the solution is not empty
        self.solvedQ = self.x_vec != {}

        if self.solvedQ:
            self.message += f"OPT using {int(self.f_obj)} colours.\n"
            self.colour_calc = {i: c for i, c in enumerate(sns.color_palette("colorblind", max(self.x_vec.values())))}
        else:
            self.message += "No solution exists.\n"

        G = nx.Graph(self.edges)
        M = nx.max_weight_matching(G, maxcardinality=True)
        self.message += f"G is normalized: {isNormalizedQ(G)}\n"
        self.message += f"|V|={len(self.vertices)}, Max. matching is size {len(M)}\n({M})"

    def width_of_edge(self, u, v):
        return 3

    def print_debug_info(self):
        print(f"x_vec = {self.x_vec}")
        print(f"colour_calc = {self.colour_calc}")
        print(f"colour_pref = {self.input_parameter_edges}")
