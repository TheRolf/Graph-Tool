from ast import literal_eval
from itertools import combinations

import networkx as nx

from tools import Env, graph6_to_edges


def isNormalizedQ(G):
    # degree-2 vertices
    for v in G.nodes:
        if G.degree[v] == 2:
            return False

    # multiple leaves at the same parent
    leaves = {v: [u for u in G[v] if G.degree[u]==1] for v in G.nodes}
    leaves = list({v: leaves[v] for v in leaves if len(leaves[v]) >= 2}.keys())
    if len(leaves) > 0:
        return False

    # simple cacti of size 1
    for u, v, w in combinations(G.nodes, 3):
        if (u, v) in G.edges and (v, w) in G.edges and (w, u) in G.edges:
            if (G.degree[u], G.degree[v], G.degree[w]) == (3, 3, 3):
                return False

    # simple cacti larger than 1
    if G.order() >= 9:
        triangle_graph = nx.Graph()
        simple_cacti = set()

        # find all triangles with vertex degrees from [3, 4]
        for u, v, w in combinations(G.nodes, 3):
            if (u, v) in G.edges and (v, w) in G.edges and (w, u) in G.edges:
                if G.degree[u] in (3, 4) and G.degree[v] in (3, 4) and G.degree[w] in (3, 4):
                    triangle_graph.add_node(str((u, v, w)))

        # add edges between compatible triangles
        for t1 in triangle_graph.nodes:
            triangle1 = literal_eval(t1)
            for t2 in triangle_graph.nodes:
                triangle2 = literal_eval(t2)
                if len(set(triangle1).intersection(triangle2)) == 1:
                    triangle_graph.add_edge(t1, t2)

        # keep only trees of compatible triangles
        nodes_to_remove = set()
        for comp in nx.connected_components(triangle_graph):
            if not nx.is_tree(nx.subgraph(triangle_graph, comp)):
                nodes_to_remove = nodes_to_remove.union(comp)
        triangle_graph.remove_nodes_from(nodes_to_remove)
        # print(list(triangle_graph.nodes), list(triangle_graph.edges), end=" ")

        # check needles of cacti
        for comp in nx.connected_components(triangle_graph):
            degree_four_vertices = {}
            for node in comp:
                triangle = literal_eval(node)
                for v in triangle:
                    if v in degree_four_vertices:
                        degree_four_vertices[v] = True
                    else:
                        degree_four_vertices[v] = False
            cactusQ = True
            for v in degree_four_vertices:
                if degree_four_vertices[v] is False and G.degree[v] == 4:
                    cactusQ = False
                    break
            if cactusQ:
                simple_cacti.add(tuple(comp))
        # print(f"simple cacti: {simple_cacti}")
        if len(simple_cacti) > 0:
            return False

    # isolated points (legacy)
    isolates = list(nx.isolates(G))
    if len(isolates):
        return False

    return True


def sparse_triangles(G):
    for u, v, w in combinations(G.nodes, 3):
        if (u, v) in G.edges and (v, w) in G.edges and (w, u) in G.edges:
            if (G.degree[u], G.degree[v], G.degree[w]) == (3, 3, 3):
                yield u, v, w


def split_deg_two(G):
    """
    Preprocessing step: splitting degree-2 vertices.
    """
    deg2 = {v: list(G[v]) for v in G.nodes if G.degree[v]==2}
    # print("degree-2", deg2)
    for v in deg2:
        u1, u2 = deg2[v]
        v1, v2 = f"{v}a", f"{v}b"
        G.remove_node(v)
        G.add_edges_from([[u1, v1], [u2, v2]])
        break
        # print(f"  replace {v} -> {[u1, v1], [u2, v2]}")
    return G


def thin_leaves(G):
    """
    Preprocessing step: at each non-leaf, removing all leaves but one.
    """
    leaves = {v: [u for u in G[v] if G.degree[u]==1] for v in G.nodes}
    leaves = {v: leaves[v] for v in leaves if len(leaves[v]) >= 2}
    # print("leaves", leaves)
    for v in leaves:
        # if v has an adjacent non-leaf -> remove all but 1 leaf
        # else v has only leaves adjacent -> remove all but 2 leaves
        remove_v = leaves[v][2:] if G.degree[v] == len(leaves[v]) else leaves[v][1:]
        G.remove_nodes_from(remove_v)
        # print(f"  remove {remove_v}")
    return G


def remove_sparse_triangles(G):
    """
    Preprocessing step: replacing 'sparse' triangles by a single edge.
    (sparse triangle: triangle with exactly 1 non-triangle edge adjacent to each of its vertices)
    """
    # print("triangles", end=" ")
    for u, v, w in sparse_triangles(G):
        # print((u, v, w), end=" ")
        G.remove_edges_from(((u, v), (v, w), (w, u)))
        G.add_edge(f"{{{u},{v},{w}}}a", f"{{{u},{v},{w}}}b")
    # print()
    return G


def preprocess(G):
    G = nx.relabel_nodes(G, {v: str(v) for v in G.nodes})
    # print(G.edges)
    old_edges = None
    edges = list(G.edges)
    # print("G", edges)
    # print()
    while edges != old_edges:
        split_deg_two(G)
        # print(G.edges)
        thin_leaves(G)
        # print(G.edges)
        remove_sparse_triangles(G)
        # print(G.edges)
        G.remove_nodes_from(list(nx.isolates(G)))
        # print(G.edges)
        old_edges = edges
        edges = list(G.edges)
        # print("G", edges)
        # print()
    return G


if __name__ == '__main__':
    # env = Env()
    G = nx.Graph([[1, 2], [2, 3], [1, 3], [3, 4], [3, 5], [4, 5], [1, 6], [2, 7], [4, 8], [5, 9]])
    print(isNormalizedQ(G))

    ifile = open("./graphs/normalized_db/normalized_n9.g6", 'r')
    for line in ifile:
        edges = graph6_to_edges(line.strip())
        H = nx.Graph(edges)
        if nx.is_isomorphic(G, H):
            print(isNormalizedQ(H))
            print(line)
    # while True:
    #     n = randint(4, 12)
    #     d = randint(2, 6)
    #     seed = randint(0, 2**20)
    #     print(f"G(n, p) random graph with p=d/n\nn={n}, d={d}, seed={seed}")
    #     G = nx.gnp_random_graph(n, d/n, seed=seed)

    # print(G.edges, end=" ")
    # G = preprocess(G)
    # print(G.edges)
    # comp_G = [comp for comp in nx.connected_components(G)]
    # largest = max((len(comp), i) for i, comp in enumerate(comp_G))[1]
    # G = G.subgraph(comp_G[largest])

    # n = 8
    # graphs = pickle.load(open(f"graphs/norm_combos_{n}.p", "rb"))
    # for edge_set in graphs:
    #     print(edge_set)
    #     continue
    #     G = nx.Graph(edge_set)
    #     # print(G.nodes)
    #     M = nx.max_weight_matching(G, maxcardinality=True)
    #     # print(M)
    #     opt, x_opt = lp(G.edges, env=env)
    #     opt = int(opt)
    #     apx = len(M)
    #     print(opt, apx, Fraction(opt/apx).limit_denominator(1000), round(opt/apx, 5))
    #     if opt/apx > 1.5:
    #         print(G.edges)
    #             # print(M)
    #             # # opt, x_opt = lp(G.edges, env=env)
    #             # print("OPT:", opt, x_opt)
    #             # pos = nx.planar_layout(G) if nx.check_planarity(G)[0] else nx.spectral_layout(G)
    #             # nx.draw(G, pos=pos, with_labels=True, node_color=['w' for v in G.nodes])
    #             # nx.draw_networkx_edge_labels(G, pos=pos, edge_labels={e: x_opt[e] for e in x_opt}, font_size=8)
    #             # plt.show()
    #             # break



