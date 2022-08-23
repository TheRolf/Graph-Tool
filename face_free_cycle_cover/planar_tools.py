import networkx as nx

from tools import pairs, edge


def dual_graph2(faces):
    D = nx.Graph()
    for face1 in faces:
        for edge1 in pairs(face1):
            for face2 in faces:
                if face1 != face2:
                    if edge(edge1) in pairs(face2):
                        D.add_edge(str(face1), str(face2))
    return D


def isInclusionFree(faces, cycle_cover):
    D = dual_graph2(faces)
    bordering_faces = {}
    for e in cycle_cover:
        bordering_faces[e] = []
        for face in faces:
            for f in pairs(face):
                if edge(e) == edge(f):
                    bordering_faces[e].append(face)
                    break
        if D.has_edge(str(bordering_faces[e][0]), str(bordering_faces[e][1])):
            D.remove_edge(str(bordering_faces[e][0]), str(bordering_faces[e][1]))

    for e in cycle_cover:
        if not nx.has_path(D, str(faces[-1]), str(bordering_faces[e][0])) and not nx.has_path(D, str(faces[-1]), str(bordering_faces[e][1])):
            return False
    return True


def edges_of_cycle(faces):
    G = nx.Graph()
    for face1 in faces:
        for face2 in faces:
            if set(face1).intersection(face2) != set():
                G.add_edge(str(face1), str(face2))

    if G.order() == 0 or not nx.is_connected(G):
        return ()

    edges_of_faces = []
    for face in faces:
        edges_of_faces.append(list(pairs(face)))

    i, j, d = 0, 0, 1
    start_edge = edges_of_faces[i][j]
    uniqueEdgeQ = True
    for i0 in range(len(faces)):
        if i0 != i:
            if start_edge in edges_of_faces[i0]:
                uniqueEdgeQ = False
                break

    while not uniqueEdgeQ:
        j = j+1
        if j >= len(faces[i]):
            i, j = i+1, 0
        start_edge = edges_of_faces[i][j]
        uniqueEdgeQ = True
        for i0 in range(len(faces)):
            if i0 != i:
                if start_edge in edges_of_faces[i0]:
                    uniqueEdgeQ = False
                    break

    j = (j+1)%len(faces[i])
    cycle = [start_edge]
    current_edge = (edges_of_faces[i][j])
    prev_edge = start_edge
    # pprint(edges_of_faces)
    while current_edge != start_edge and current_edge != reversed(start_edge):
        # print(f"current edge: {current_edge}")
        for i0 in range(len(faces)):
            if i0 != i:
                if current_edge in edges_of_faces[i0]:
                    i = i0
                    j = edges_of_faces[i].index(current_edge)
                    # print(f"{edges_of_faces[i][j]}")
                    d = 1 if set(prev_edge).intersection(edges_of_faces[i][(j+1)%len(faces[i])]) != set() else -1
                    j = (j+d)%len(faces[i])
                    break
        else:
            cycle.append(current_edge)
            j = (j+d)%len(faces[i])
        prev_edge = current_edge
        current_edge = edges_of_faces[i][j]
    return cycle
