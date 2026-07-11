from data_loader import get_vertices


# Look for a negative cycle using Bellman-Ford.
# A negative cycle in the -log(rate) graph is an arbitrage opportunity.
# Returns the list of currencies in the cycle, or None.
def find_arbitrage(graph):
    vertices = get_vertices(graph)

    # Start every distance at 0 so the search can begin from any currency.
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

    # One more pass. If an edge can still relax, a negative cycle exists.
    for src in graph:
        for dst in graph[src]:
            weight = graph[src][dst]
            if distance[src] + weight < distance[dst]:
                return build_cycle(parent, dst)

    return None


# Walk backwards through the parents to rebuild the cycle.
def build_cycle(parent, start):
    # Step back V times to make sure we are inside the cycle.
    node = start
    for i in range(len(parent)):
        node = parent[node]

    # Collect the currencies until we come back to the start node.
    cycle = [node]
    current = parent[node]
    while current != node:
        cycle.append(current)
        current = parent[current]
    cycle.append(node)
    cycle.reverse()
    return cycle