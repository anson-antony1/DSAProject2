import csv
import math
import random


def load_rates(filename):
    graph = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row["from"].strip().upper()
            dst = row["to"].strip().upper()

            try:
                rate = float(row["rate"])
            except (ValueError, TypeError):
                continue
            if rate <= 0 or src == dst:
                continue

            add_edge(graph, src, dst, rate)
    return graph


def add_edge(graph, src, dst, rate):
    if src not in graph:
        graph[src] = {}
    # -log(rate) makes a profitable loop of trades a negative weight cycle.
    graph[src][dst] = -math.log(rate)


def get_vertices(graph):
    # Must include currencies that only appear as a destination, or
    # Floyd-Warshall crashes indexing them.
    vertices = set()
    for src in graph:
        vertices.add(src)
        for dst in graph[src]:
            vertices.add(dst)
    return sorted(vertices)


# Complete random graph for the benchmark. Rates near 1 keep arbitrage rare.
def make_random_graph(n, seed=1):
    rng = random.Random(seed)
    graph = {}
    names = ["C" + str(i) for i in range(n)]
    for src in names:
        for dst in names:
            if src != dst:
                add_edge(graph, src, dst, rng.uniform(0.9, 1.1))
    return graph
