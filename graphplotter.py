from ast import literal_eval

import easygui
import matplotlib.pyplot as plt
import networkx as nx

from matplotlib.backend_bases import MouseButton

from tools import point_on_line, graph6_to_edges, spread_coords
from instance import Instance


class GraphPlotter:
    def __init__(self, points=None, edges=None):
        self.EPS = 0.15
        self.eps = 0.1
        self.X, self.Y = 8, 5

        self.coordinates = points or {}
        self.instance = Instance(self.coordinates.keys(), edges)

        self.i_sel, self.e_sel = None, None
        self.fig, self.ax = None, None

    def mouse_click(self, event):
        if event.inaxes is None:
            return

        elif event.button == MouseButton.LEFT:
            if self.e_sel is not None:
                self.e_sel = None
            else:
                self.select(event.xdata, event.ydata)

        elif event.button == MouseButton.RIGHT:
            if self.i_sel is not None:
                self.move_vertex(self.i_sel, event.xdata, event.ydata)
                self.i_sel = None
            elif self.e_sel is not None:
                self.e_sel = None

        self.draw()

    def key_press(self, event):
        if event.key == 'delete':
            if self.e_sel is not None:
                self.delete_edge(self.e_sel)
                self.e_sel = None
            elif self.i_sel is not None:
                self.delete_vertex(self.i_sel)
                self.i_sel = None

        elif event.key == 'backspace':
            self.reset()

        elif event.key == 'c' and self.e_sel is not None:
            text_gui = easygui.enterbox("", f"Set colour for edge {self.e_sel}")
            c = None if text_gui in ['', '0', None] else int(text_gui)
            self.instance.set_input_parameter_edge(self.e_sel, c)
            self.e_sel = None

        elif event.key == 'd':
            self.print_debug_info()
            self.instance.print_debug_info()

        elif event.key in ['l', 'p']:  # lowercase L and P
            self.planarity(repositionQ=(event.key=='p'))

        elif event.key in ['x', 'y', 'z', 'm', 'n']:
            self.instance.solve(option=event.key)

        if event.key in ['i', 'j']:
            input = easygui.enterbox("", f"Enter the list of edges" if event.key == 'i' else f"Enter the graph6 graph")
            if input:
                self.input_instance(input, graph6Q=(event.key=='j'))

        self.draw()

    def input_instance(self, input, graph6Q=False):
        edges = graph6_to_edges(input) if graph6Q else set(tuple(e) for e in literal_eval(input))
        vertices = {v for e in edges for v in e}
        G = nx.Graph(edges)
        planarity = nx.check_planarity(G)
        if planarity[0]:
            coordinates = nx.planar_layout(G, center=[self.X/2, self.Y/2], scale=3.5)
        else:
            points = spread_coords(len(vertices), [0, self.X], [0, self.Y])
            coordinates = {i: points[i] for i in range(len(points))}
        self.reset(coordinates, edges)

    def reset(self, points=None, edges=None):
        self.i_sel, self.e_sel = None, None
        self.coordinates = points or {}
        self.instance = Instance(self.coordinates.keys(), edges)

    def start(self):
        self.fig, self.ax = plt.subplots(figsize=(12, 9))
        self.fig.canvas.mpl_disconnect(self.fig.canvas.manager.key_press_handler_id)
        self.fig.canvas.mpl_connect('button_press_event', self.mouse_click)
        self.fig.canvas.mpl_connect('key_press_event', self.key_press)
        self.draw()
        plt.show()

    def draw(self):
        self.ax.cla()
        self.ax.set_aspect(1)
        plt.xlim([0, self.X])
        plt.ylim([0, self.Y])
        self.draw_vertices()
        self.draw_edges()
        self.draw_text()
        plt.draw()

    def draw_vertices(self):
        for i, (x, y) in self.coordinates.items():
            if i == self.i_sel:
                self.ax.scatter(x, y, s=40, c='k', zorder=2)
                self.ax.scatter(x, y, s=25, c='w', zorder=3)
            else:
                self.ax.scatter(x, y, s=40, c='k', zorder=3)
            tx, ty = x + 0.1, y + 0.1
            self.ax.add_patch(plt.Circle((tx, ty), 0.075, color='w', zorder=3))
            self.ax.annotate(f"[{i}]", (tx, ty), zorder=3, ha='center', va='center')

    def draw_edges(self):
        for i, j in self.instance.edges:
            x1, y1 = self.coordinates[i]
            x2, y2 = self.coordinates[j]
            if (i, j) == self.e_sel:
                self.ax.plot((x1, x2), (y1, y2), color=self.instance.color_of_edge(i, j), zorder=2, linewidth=4)
                self.ax.plot((x1, x2), (y1, y2), color='w', zorder=2, linewidth=1.5)
            else:
                self.ax.plot((x1, x2), (y1, y2), color=self.instance.color_of_edge(i, j), zorder=2, linewidth=3)

            e_text = self.instance.color_of_edge(i, j, textQ=True)
            if e_text != '':
                tx, ty = (x1 + 2 * x2) / 3 + 0.00, (y1 + 2 * y2) / 3 + 0.00
                self.ax.add_patch(plt.Circle((tx, ty), 0.075, color='w', zorder=3))
                self.ax.annotate(f"{e_text}", (tx, ty), zorder=3, ha='center', va='center')

    def draw_text(self):
        self.ax.annotate(self.instance.message, (0.4, 0.25))

    def select(self, x, y):
        self.e_sel = self.select_line(x, y)
        # If we clicked on an edge, select it
        if self.e_sel is None:
            i, x, y = self.select_vertex(x, y)
            # If we clicked on the selected vertex, de-select it
            if self.i_sel == i:
                self.i_sel = None
            elif self.i_sel is not None:
                self.instance.add_edge(self.i_sel, i)
                print(f"add: {(self.i_sel, i)}")
                self.i_sel = None

            else:
                self.i_sel = i

    def select_vertex(self, x, y):
        for i, (x0, y0) in self.coordinates.items():
            if abs(x - x0) < self.EPS and abs(y - y0) < self.EPS:
                return i, x0, y0
        else:
            i = 0
            while i in self.coordinates:
                i += 1
            self.coordinates[i] = [x, y]
            self.instance.add_vertex(i)
            print(f"add: {i}")
            self.draw()
            return i, x, y

    def select_line(self, x, y):
        for i, j in self.instance.edges:
            x1, y1 = self.coordinates[i]
            x2, y2 = self.coordinates[j]
            if point_on_line(x, y, x1, y1, x2, y2, self.eps, self.EPS):
                return i, j
        return None

    def move_vertex(self, i, x, y):
        self.coordinates[i] = [x, y]

    def delete_vertex(self, i):
        del self.coordinates[i]
        self.instance.delete_vertex(i)
        print(f"del: {i}")

    def delete_edge(self, e):
        self.instance.delete_edge(e)
        print(f"del: {e}")

    def planarity(self, repositionQ=False):
        G = nx.Graph(self.instance.edges)
        planarity = nx.check_planarity(G, counterexample=True)
        if planarity[0]:
            if repositionQ:
                self.coordinates = nx.planar_layout(G, center=[self.X/2, self.Y/2], scale=3.5)
            print("Planar.")
        else:
            print(f"Not planar: {planarity[1].edges}")

    def print_debug_info(self):
        print()
        print(f"i_sel = {self.i_sel}")
        print(f"e_sel = {self.e_sel}")

        coordinates = {i: [round(self.coordinates[i][0], 1), round(self.coordinates[i][1], 1)]
                       for i in self.coordinates}
        print(f"vertices = {coordinates}")
        print(f"edges = {self.instance.edges}")


class GraphPlotterMaxEdgeClr(GraphPlotter):
    def __init__(self, points=None, edges=None):
        super().__init__(points=points, edges=edges)
        self.instance = MaxEdgeColourInstance(self.coordinates.keys(), edges)
