import time

import matplotlib.pyplot as plt

import bellman_ford
import floyd_warshall
from data_loader import make_random_graph


# Time how long one algorithm takes on a single graph.
def time_run(algorithm, graph):
    start = time.perf_counter()
    algorithm(graph)
    end = time.perf_counter()
    return end - start


# Run both algorithms on graphs of growing size and collect the times.
def run_benchmark(sizes):
    bf_times = []
    fw_times = []

    for n in sizes:
        graph = make_random_graph(n)

        bf_time = time_run(bellman_ford.find_arbitrage, graph)
        fw_time = time_run(floyd_warshall.find_arbitrage, graph)

        bf_times.append(bf_time)
        fw_times.append(fw_time)

        print("Size " + str(n) + ": Bellman-Ford " + str(round(bf_time, 4))
              + "s, Floyd-Warshall " + str(round(fw_time, 4)) + "s")

    return bf_times, fw_times


# Draw the runtime comparison chart and save it to a file.
def make_chart(sizes, bf_times, fw_times):
    plt.plot(sizes, bf_times, marker="o", label="Bellman-Ford")
    plt.plot(sizes, fw_times, marker="o", label="Floyd-Warshall")
    plt.xlabel("Number of currencies")
    plt.ylabel("Runtime (seconds)")
    plt.title("Arbitrage Detection Runtime Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("runtime_comparison.png")
    print("Saved chart to runtime_comparison.png")


def main():
    sizes = [10, 25, 50, 75, 100]
    bf_times, fw_times = run_benchmark(sizes)
    make_chart(sizes, bf_times, fw_times)


if __name__ == "__main__":
    main()
