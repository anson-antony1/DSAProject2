from data_loader import get_vertices

# Stands in for "no edge yet".
INF = float("inf")


# Uses Floyd-Warshall to look for a negative cycle, which means arbitrage.
def find_arbitrage(graph):
    vertices = get_vertices(graph)
    n = len(vertices)

    # Give each currency a number so we can use simple grids.
    index = {}
    for i in range(n):
        index[vertices[i]] = i

    # dist holds the best distances and nxt remembers the path taken.
    dist = [[INF] * n for i in range(n)]
    nxt = [[None] * n for i in range(n)]

    # Distance from a currency to itself starts at 0.
    for i in range(n):
        dist[i][i] = 0

    # Fill in the starting edges from the graph.
    for src in graph:
        for dst in graph[src]:
            i = index[src]
            j = index[dst]
            dist[i][j] = graph[src][dst]
            nxt[i][j] = j

    # Try every currency k as a stop between i and j.
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    # A negative distance from a currency back to itself means arbitrage.
    for i in range(n):
        if dist[i][i] < 0:
            return build_cycle(nxt, vertices, i)

    return None


# Follows the next hops to rebuild the cycle.
def build_cycle(nxt, vertices, start):
    order = []
    node = start

    # Keep walking until we land on a currency we already visited.
    while node not in order:
        order.append(node)
        node = nxt[node][start]

    # The repeated currency marks the loop, so cut off anything before it.
    loop_start = order.index(node)
    cycle = order[loop_start:]
    cycle.append(node)

    return [vertices[i] for i in cycle]
