import random
from itertools import islice

import gurobipy
from networkx import NetworkXError
from networkx.readwrite.graph6 import data_to_n, n_to_data
from scipy.spatial.distance import euclidean


def Env(LogToConsole=0):
    env = gurobipy.Env(empty=True)
    env.setParam('LogToConsole', LogToConsole)
    env.start()
    return env


def edge(e):
    return tuple(e) if e[0] < e[1] else tuple(reversed(e))


def pairs(circle):
    return (edge(e) for e in zip(circle, circle[1:]+circle[0:1]))


def triplets(circle):
    return zip(circle, circle[1:]+circle[0:1], circle[2:]+circle[0:2])

def graph6_to_edges(string):
    """
    From networkx 2.8.2, modified slightly
    """
    def bits():
        """Returns sequence of individual bits from 6-bit-per-value
        list of data values."""
        for d in data:
            for i in [5, 4, 3, 2, 1, 0]:
                yield (d >> i) & 1

    bytes_in = bytearray(string, "ascii")
    data = [c-63 for c in bytes_in]
    if any(c > 63 for c in data):
        raise ValueError("each input character must be in range(63, 127)")

    n, data = data_to_n(data)
    nd = (n * (n - 1) // 2 + 5) // 6
    if len(data) != nd:
        raise NetworkXError(
            f"Expected {n * (n - 1) // 2} bits but got {len(data) * 6} in graph6"
        )

    edges = []
    for (i, j), b in zip([(i, j) for j in range(1, n) for i in range(j)], bits()):
        if b:
            edges.append((i, j))

    return edges


def edges_to_graph6(G):
    g_bytes = b""
    n = len(G)
    nodes = list(G.nodes)
    for d in n_to_data(n):
        g_bytes += str.encode(chr(d + 63))
    # This generates the same as `(v in G[u] for u, v in combinations(G, 2))`,
    # but in "column-major" order instead of "row-major" order.
    bits = (nodes[j] in G[nodes[i]] for j in range(1, n) for i in range(j))
    chunk = list(islice(bits, 6))
    while chunk:
        d = sum(b << 5 - i for i, b in enumerate(chunk))
        g_bytes += str.encode(chr(d + 63))
        chunk = list(islice(bits, 6))
    return g_bytes


def spread_coords(N, xrange=(0, 1), yrange=(0, 1), margin=0.1, K=10):
    # Generates 'N' spread out points in the Euclidean plane in 'xrange' and 'yrange' ranges.
    # Leaves a margin (0.05 corresponds to 5%), uses 'K' candidates for each new point (Mitchell's algorithm)
    x_size = xrange[1] - xrange[0]
    y_size = yrange[1] - yrange[0]

    def candidate():
        return [random.uniform(xrange[0] + margin*x_size, xrange[1] - margin*x_size),
                random.uniform(yrange[0] + margin*y_size, yrange[1] - margin*y_size)]

    def closestDistance(p):
        min_dist = float("inf")
        for s in points:
            dist = euclidean(p, s)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    points = [candidate()]
    for n in range(N-1):
        best_distance, best_candidate = 0, None
        for k in range(K):
            point = candidate()
            distance = closestDistance(point)
            if distance > best_distance:
                best_distance = distance
                best_candidate = point
        points.append(best_candidate)
    return points


def point_on_line(x, y, x1, y1, x2, y2, eps, EPS):
    if (abs(x - x1) < EPS and abs(y - y1) < EPS) or (abs(x - x2) < EPS and abs(y - y2) < EPS):
        return False

    crossproduct = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > eps:
        return False

    dotproduct = (x - x1) * (x2 - x1) + (y - y1)*(y2 - y1)
    if dotproduct < 0:
        return False

    squaredlengthba = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
    if dotproduct > squaredlengthba:
        return False

    return True
