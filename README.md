# ArbitrageX

Real-time crypto arbitrage detection using graph algorithms.

An arbitrage happens when a chain of trades across currency pairs comes back to
the starting currency with a profit. This project models exchange rates as a
graph and checks for that kind of profitable loop. It does this with two
shortest path algorithms built from scratch, Bellman-Ford and Floyd-Warshall,
and compares how fast they run as the graph grows.

## How it works

Each currency is a vertex. Each exchange rate is a directed edge. The edge
weight is set to `-log(rate)`. With that weight, a profitable loop of trades
turns into a negative weight cycle, so detecting arbitrage becomes detecting a
negative cycle.

- Bellman-Ford relaxes every edge and reports a negative cycle if an edge can
  still be relaxed after V-1 passes.
- Floyd-Warshall builds all-pairs shortest paths and reports a negative cycle if
  any currency ends up with a negative distance to itself.

## Files

- `data_loader.py` reads the exchange rates and builds the graph. Also makes
  random graphs for the benchmark.
- `bellman_ford.py` Bellman-Ford negative cycle detection and cycle path.
- `floyd_warshall.py` Floyd-Warshall negative cycle detection and cycle path.
- `main.py` loads the data, runs both algorithms, and prints the cycle and
  profit percentage.
- `benchmark.py` runs both algorithms on growing graph sizes and saves a runtime
  chart.
- `sample_rates.csv` small example with a known arbitrage loop.

## Setup

Install the one dependency used for the chart:

```
pip install -r requirements.txt
```

## Running

Detect arbitrage on the sample data:

```
python3 main.py
```

Example output:

```
Bellman-Ford
  Cycle: EUR -> BTC -> USD -> EUR
  Profit: 8.0%

Floyd-Warshall
  Cycle: BTC -> USD -> EUR -> BTC
  Profit: 8.0%
```

Run the runtime comparison and save the chart to `runtime_comparison.png`:

```
python3 benchmark.py
```

## Data format

`sample_rates.csv` has three columns: `from`, `to`, `rate`. To run on real data,
convert the Kaggle crypto price dataset into the same three column format using
one timestamp of close prices.
