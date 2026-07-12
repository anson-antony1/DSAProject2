from data_loader import get_vertices


# Uses Bellman-Ford to look for a negative cycle, which means arbitrage.
def find_arbitrage(graph):
    vertices = get_vertices(graph)

    # Start every distance at 0 so any currency can be the start.
    distance = {}
    parent = {}
    for v in vertices:
        distance[v] = 0
        parent[v] = None

    # Relax all edges V-1 times.
    for i in range(len(vertices) - 1):
        for src in graph:
            for dst in graph[src]:
                weight = graph[src][dst]
                if distance[src] + weight < distance[dst]:
                    distance[dst] = distance[src] + weight
                    parent[dst] = src

    # One extra pass, if anything still improves there is a negative cycle.
    for src in graph:
        for dst in graph[src]:
            weight = graph[src][dst]
            if distance[src] + weight < distance[dst]:
                return build_cycle(parent, dst)

    return None


# Walks back through the parents to rebuild the cycle.
def build_cycle(parent, start):
    # Step back enough times to make sure we are inside the cycle.
    node = start
    for i in range(len(parent)):
        node = parent[node]

    # Collect currencies until we loop back to where we started.
    cycle = [node]
    current = parent[node]
    while current != node:
        cycle.append(current)
        current = parent[current]
    cycle.append(node)
    cycle.reverse()
    return cycle