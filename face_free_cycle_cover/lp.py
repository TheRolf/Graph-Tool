from random import uniform

import gurobipy
from gurobipy import GRB

from tools import edge, pairs


def lp(faces, env=None, relaxQ=False, randomQ=False, faceFreeQ=True, fixEdges=()):
    faces = [tuple(face) for face in faces]
    edges = set()
    for face in faces:
        for e in pairs(face):
            edges.add(edge(e))
    points = set()
    for face in faces:
        for v in face:
            points.add(v)

    if env is None:
        env = gurobipy.Env(empty=True)
        env.setParam('LogToConsole', 0)
        env.start()

    model = gurobipy.Model("face_free", env=env)
    x = model.addVars([edge(e) for e in edges], vtype=GRB.CONTINUOUS if relaxQ else GRB.BINARY, lb=0, ub=1, name="x")
    c = {e: round(uniform(-1, 1), 3) for e in edges}
    model.setObjective(sum(x[e]*c[e] for e in edges) if randomQ else 0, GRB.MINIMIZE)

    # each vertex has to be covered exactly once
    model.addConstrs((sum(x[edge((u, v))] for u in points if edge((u, v)) in edges) == 2) for v in points)

    # one cannot cover all edges of a face
    if faceFreeQ:
        model.addConstrs((sum(x[edge(e)] for e in pairs(face)) <= len(face)-1) for face in faces)

    # fixed edges
    model.addConstrs(x[edge(e)] == 1 for e in fixEdges if fixEdges[e] is not None)

    model.optimize()
    res = {}
    if model.status == GRB.OPTIMAL:
        for e in edges:
            if round(float(x[edge(e)].X), 5) > 0:
                res[edge(e)] = round(float(x[edge(e)].X), 5)
    return res
