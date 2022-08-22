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
