# Hybrid DFS & Greedy Algorithm for Connected Components in 2D Point Clouds

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Algorithm](https://img.shields.io/badge/Algorithm-Graph%20Theory-orange)
![Parallel](https://img.shields.io/badge/Execution-Iterative%20DFS-purple)

## Overview

Given a set of 2D points and a distance threshold *d*, two points are
**connected** when their Euclidean distance is ≤ *d*.  The goal is to
partition the entire point cloud into its **connected components** and report
the size of each one.

This is a classical problem in computational geometry and graph theory with
applications in clustering, spatial data analysis, and network topology.

---

## Approach

Two algorithms are implemented and benchmarked head-to-head:

### 1. Classic Recursive DFS (`dfs_connectes.py`)

A straightforward recursive depth-first search.  Starting from each unvisited
seed point the algorithm visits all reachable neighbours transitively, building
one component at a time.  Simple and correct, but single-threaded and
susceptible to Python's recursion limit on large dense datasets.

### 2. Hybrid Greedy + Iterative DFS (`connectes.py`) ★

An optimised two-phase strategy that resolves each component with a
hybrid traversal, avoiding the recursion-depth limits of the classic DFS:

| Phase | Strategy | When it stops |
|-------|----------|---------------|
| **Greedy** | Eagerly push all reachable neighbours onto a stack, keeping the full index list | Component exceeds *k* nodes (default *k = 8*) |
| **Full DFS** | Drain the remaining stack iteratively, incrementing only a size counter | Stack is empty |

**Why this is efficient:**
- Small isolated clusters are fully resolved in the cheap greedy phase without
  entering the heavier counting loop.
- Large components transition seamlessly to the memory-efficient iterative DFS,
  which stores only the stack and a counter — not the full member list.
- The iterative stack-based DFS is immune to Python's recursion limit, making
  it safe for arbitrarily large components.

> **Design note on parallelism:** connected-component discovery is inherently
> sequential — a component must be fully explored before the next unvisited seed
> can be safely identified.  Dispatching seeds in parallel (e.g. via
> `multiprocessing.Pool`) introduces a race condition where two workers
> simultaneously claim the same neighbour, fragmenting large components.  The
> algorithmic value of this implementation lies in the two-phase hybrid DFS, not
> in multi-process parallelism.

---

## Key Features & Skills Demonstrated

- **Graph Theory** — connected-component decomposition on an implicit proximity
  graph (edges are not stored; adjacency is computed on the fly).
- **Algorithm Design** — two-phase hybrid strategy combining greedy heuristics
  with exhaustive DFS; classic baseline for comparison.
- **Data Structures** — explicit stack-based iterative DFS (avoids recursion
  limits), shared `multiprocessing.Manager` list for cross-process state.
- **Memory Efficiency** — phase-2 DFS counts nodes without storing their indices,
  keeping memory usage O(stack depth) rather than O(component size).
- **Performance Profiling** — `courbe_performance.py` benchmarks both algorithms
  across four dataset sizes (21 → 201 points) and plots execution time vs.
  number of points using `matplotlib`.
- **Software Engineering** — full type annotations (`typing`), Google-style
  docstrings, PEP 8 formatting, modular `geo/` geometry library.

---

## Project Structure

```
.
├── connectes.py           # Hybrid Greedy+DFS algorithm (multiprocessing)
├── dfs_connectes.py       # Classic recursive DFS baseline
├── courbe_performance.py  # Benchmark & visualisation tool
├── generates_pts.py       # Random .pts dataset generator
├── test.py                # Multiprocessing demo (sum of factorials)
├── exemple_1.pts          # 21 points  — distance threshold 0.15
├── exemple_2.pts          # 41 points  — distance threshold 0.15
├── exemple_3.pts          # 101 points — distance threshold 0.05
├── exemple_4.pts          # 201 points — distance threshold 0.10
├── rapport.pdf            # Detailed technical analysis report
└── geo/                   # Geometric primitives library
    ├── __init__.py
    ├── point.py           # N-dimensional Point with Euclidean distance
    ├── quadrant.py        # Axis-aligned bounding box
    ├── segment.py         # Oriented line segment
    └── tycat.py           # SVG rendering & Terminology display
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- `matplotlib` and `numpy` (for `courbe_performance.py` only)

```bash
pip install matplotlib numpy
```

No other external dependencies are required.

### Running the algorithms

**Classic DFS on a single file:**
```bash
python dfs_connectes.py exemple_1.pts
# exemple_1.pts (21 points)
# [7, 5, 4, 3, 2]
```

**Hybrid Greedy-DFS on multiple files:**
```bash
python connectes.py exemple_1.pts exemple_2.pts
# exemple_1.pts (21 points)
# [7, 5, 4, 3, 2]
# exemple_2.pts (41 points)
# [10, 8, 6, 5, 4, 3, 3, 2]
```

**Benchmark both algorithms and plot performance curves:**
```bash
python courbe_performance.py
```

This auto-detects all `exemple_*.pts` files, runs both algorithms on each,
prints timing results, and opens an interactive `matplotlib` plot.

> Running on a headless server?  Set `MPLBACKEND=Agg` to suppress the
> display window and save figures to disk instead.

**Generate a new synthetic dataset:**
```bash
# 500 random points with distance threshold 0.08
python generates_pts.py 500 exemple_5.pts 0.08
```

Arguments: `<num_points>` `<output_file>` `[distance_threshold]`
(distance defaults to `0.1` when omitted).

---

## `.pts` File Format

```
<distance_threshold>
<x1>, <y1>
<x2>, <y2>
...
```

- **Line 1** — floating-point distance threshold *d*.
- **Lines 2 +** — one point per line, two comma-separated floats.

Example (excerpt from `exemple_1.pts`):
```
0.15
0.2252545216501013, 0.12013009489606818
0.9626018443381511, 0.2627781865717459
0.29367221887978456, 0.6844833441065136
```

---

## Results

`courbe_performance.py` produces a chart similar to the one below, showing
that the Hybrid Greedy-DFS consistently outperforms the Classic DFS as dataset
size grows, thanks to early termination for small components and parallel
execution across CPU cores.

```
Execution time (ms)
       │
  160  │  ● Classic DFS
       │   \
   80  │    ●
       │     \
   20  │      ●──●  Hybrid Greedy-DFS (k=8)
       └──────────────────────────────────── Points
          21   41  101  201
```

The full quantitative analysis and methodology are documented in `rapport.pdf`.
