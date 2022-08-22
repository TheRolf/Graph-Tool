import gurobipy
from gurobipy.gurobipy import GRB

from tools import edge


def pendant_edges(V, E):
    """
    Returns a dict where
    - keys: pendant parent v
    - values: list of pendant edges adjacent to v, in sorted edge format
    """
    delta = {w: [(w, v) for e in E for v in e if w in e and v != w] for w in V}
    pendant_dict = {}
    for w in V:
        if len(delta[w]) == 1:
            u, v = delta[w][0]
            w_parent = u if v == w else v
            if w_parent not in pendant_dict:
                pendant_dict[w_parent] = []
            pendant_dict[w_parent].append(edge((w_parent, w)))
    return pendant_dict


def lp(E, q=2, k=0, env=None, relaxQ=False, leavesUniqueQ=False, leavesNonUniqueQ=False, leavesMonoQ=False, blockLeaveColourQ=False, fixedUniqueQ=False):
    if len(E)==1:
        return 1, {list(E)[0]: 1}
    if env is None:
        env = gurobipy.Env(empty=True)
        env.setParam('LogToConsole', 0)
        env.start()
    V = set([v for e in E for v in e])
    if k == 0:
        k = len(V)
    C = range(1, k+1)

    delta = {w: [(w, v) for e in E for v in e if w in e and v != w] for w in V}
    pendant_dict = pendant_edges(V, E)

    model = gurobipy.Model(f"max_edge_{q}-colour", env=env)

    y = model.addVars([edge(e) for e in E], C, vtype=GRB.CONTINUOUS if relaxQ else GRB.BINARY, lb=0, ub=1, name="y")
    z = model.addVars(C, vtype=GRB.CONTINUOUS if relaxQ else GRB.BINARY, lb=0, ub=1, name="z")
    model.setObjective(sum((z[c]) for c in C), GRB.MAXIMIZE)

    for u, v in E.keys():
        if E[u, v] is not None:
            u, v = edge((u, v))
            m = E[u, v]
            model.addConstr(y[u, v, m] == 1, f"colour of {(u, v)} is {m}")
            if fixedUniqueQ:
                for u0, v0 in E:
                    u0, v0 = edge((u0, v0))
                    if u0 != u or v0 != v:
                        model.addConstr(y[u0, v0, m] == 0, f"colour of {(u0, v0)} not {m}")

    # colour 'c' is used (z[c]) if there is an edge coloured 'c' (y[e, c])
    model.addConstrs((z[c] <= sum(y[u, v, c] for u, v in E)) for c in C)
    # every edge has one color
    model.addConstrs((sum(y[u, v, c] for c in C) == 1) for u, v in E)
    # use the first opt colors from the color list
    model.addConstrs(z[c] >= z[c+1] for c in C[:-1])

    if leavesUniqueQ:
        m = 1
        for w_parent in pendant_dict:
            for u, v in pendant_dict[w_parent]:
                model.addConstr(y[u, v, m] == 1, f"pendant edge {(u, v)} with colour {m}")
                model.addConstrs(y[u0, v0, m] == 0 for u0, v0 in E if u != u0 or v != v0)
            m += 1

    elif leavesMonoQ:
        model.addConstrs(
            y[u, v, 1] == 1
            for w_parent in pendant_dict for u, v in pendant_dict[w_parent])
        if blockLeaveColourQ:
            model.addConstrs(
             y[u, v, 1] == 0
             for u, v in E if len(delta[u]) > 1 and len(delta[v]) > 1)

    elif leavesNonUniqueQ:
        model.addConstrs(
            y[delta[w][0][0], delta[w][0][1], c] <= sum(y[u, v, c] for u, v in E if len(delta[u]) > 1 and len(delta[v]) > 1)
            for w in V if len(delta[w])==1 for c in C)

    x = model.addVars(V, C, vtype=GRB.CONTINUOUS if relaxQ else GRB.BINARY, lb=0, ub=1, name="x")
    model.addConstrs((y[u, v, c] <= x[w, c]) for c in C for u, v in E for w in [u, v])
    model.addConstrs((sum(x[v, c] for c in C) <= q) for v in V)

    model.optimize()
    res, obj_val = {}, -float("inf")
    if model.status == GRB.OPTIMAL:
        for u, v in E:
            for c in C:
                if round(float(y[u, v, c].X), 5) > 0:
                    if relaxQ:
                        print(f"{(u, v)}, {c}: {y[u, v, c].X}")
                    res[u, v] = c
        obj_val = round(model.getObjective().getValue(), 5)
    return obj_val, res
