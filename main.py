import math

import bellman_ford
import floyd_warshall
from data_loader import load_rates


# Turn a cycle of currencies into a profit percentage.
# Multiply the rates along the cycle. Anything above 1 is a profit.
def cycle_profit(graph, cycle):
    product = 1.0
    for i in range(len(cycle) - 1):
        src = cycle[i]
        dst = cycle[i + 1]
        weight = graph[src][dst]
        rate = math.exp(-weight)
        product = product * rate
    return (product - 1) * 100


# Print the result of one algorithm in a readable way.
def show_result(name, graph, cycle):
    print(name)
    if cycle is None:
        print("  No arbitrage cycle found.")
    else:
        path = " -> ".join(cycle)
        profit = cycle_profit(graph, cycle)
        print("  Cycle: " + path)
        print("  Profit: " + str(round(profit, 4)) + "%")
    print("")


def main():
    graph = load_rates("sample_rates.csv")

    bf_cycle = bellman_ford.find_arbitrage(graph)
    show_result("Bellman-Ford", graph, bf_cycle)

    fw_cycle = floyd_warshall.find_arbitrage(graph)
    show_result("Floyd-Warshall", graph, fw_cycle)


if __name__ == "__main__":
    main()
