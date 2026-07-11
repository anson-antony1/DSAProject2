from data_loader import get_vertices

# A big number used to stand in for "no edge yet".
INF = float("inf")


# Look for a negative cycle using Floyd-Warshall.
# It builds the shortest path between every pair of currencies.
# If any currency ends up with a negative distance to itself, that is arbitrage.
# Returns the list of currencies in the cycle, or None if there is none.
def find_arbitrage(graph):
    vertices = get_vertices(graph)
    n = len(vertices)

    # Give each currency a number so we can use simple grids.
    index = {}
    for i in range(n):
        index[vertices[i]] = i

    # dist[i][j] is the best known distance from currency i to currency j.
    # nxt[i][j] remembers the next currency on that path so we can rebuild it.
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

    # Main Floyd-Warshall triple loop.
    # Try using currency k as a stop between i and j.
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

    # Check the diagonal. A negative value means a currency can reach
    # itself for a profit, so a negative cycle exists there.
    for i in range(n):
        if dist[i][i] < 0:
            return build_cycle(nxt, vertices, i)

    return None


# Follow the next-hop grid to rebuild the cycle.
# Under a negative cycle the path can loop before reaching the start,
# so we stop at the first currency we visit twice and keep that loop.
def build_cycle(nxt, vertices, start):
    order = []
    node = start

    # Walk the next hops until we land on a currency we already visited.
    while node not in order:
        order.append(node)
        node = nxt[node][start]

    # The repeated currency marks the loop. Cut off anything before it.
    loop_start = order.index(node)
    cycle = order[loop_start:]
    cycle.append(node)

    return [vertices[i] for i in cycle]
