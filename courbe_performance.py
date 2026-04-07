#!/usr/bin/env python3
"""
Benchmark and visualise Classic DFS vs. Hybrid Greedy-DFS performance.

Scans the project directory for all ``exemple_*.pts`` files, runs both
algorithms on each dataset, records wall-clock execution times, and produces a
comparative performance curve (execution time vs. number of points).
"""

import glob
import os
import time
from typing import Callable, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

from connectes import print_components_sizes
from dfs_connectes import compute_component_sizes_dfs, load_instance


def visualize_components(
    points: List,
    sizes: List[int],
    title: str = "Connected Components",
) -> None:
    """Display a colour-coded scatter plot of the 2D point cloud.

    Each component is assigned a distinct colour from the ``rainbow`` colormap.
    Points are coloured in the same order they appear in *points*, assuming
    *sizes* was produced by the same algorithm on the same dataset.

    Args:
        points: List of :class:`~geo.point.Point` objects to plot.
        sizes: Component sizes in descending order.  Used to build the
            colour-index mapping: first ``sizes[0]`` points → colour 1, next
            ``sizes[1]`` → colour 2, and so on.
        title: Plot window title.
    """
    if not points or not sizes:
        print(f"Nothing to visualise for '{title}'.")
        return

    # Assign a colour index to every point based on which component it belongs to
    colour_ids: List[int] = []
    for component_id, size in enumerate(sizes, start=1):
        colour_ids.extend([component_id] * size)

    colours = plt.colormaps["rainbow"](np.linspace(0, 1, max(colour_ids) + 1))

    plt.figure(figsize=(8, 8))
    for i, point in enumerate(points):
        plt.scatter(
            point.coordinates[0],
            point.coordinates[1],
            c=[colours[colour_ids[i]]],
            s=10,
        )

    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


def measure_performance(
    filename: str,
    algo: Callable,
    algo_name: str,
    k: Optional[int] = None,
) -> Tuple[float, List[int], List]:
    """Run one algorithm on one file and return its wall-clock execution time.

    Args:
        filename: Path to the ``.pts`` dataset file.
        algo: Algorithm callable.  Must accept ``(distance, points)`` or, when
            *k* is provided, ``(distance, points, k)``.
        algo_name: Human-readable label printed in the console summary.
        k: Optional greedy-phase threshold forwarded to the hybrid algorithm.
            Pass ``None`` for the classic DFS.

    Returns:
        A tuple ``(elapsed_ms, sizes, points)`` where *elapsed_ms* is the
        measured wall-clock time in milliseconds, *sizes* is the list of
        component sizes returned by *algo*, and *points* is the parsed dataset.
    """
    distance, points = load_instance(filename)
    if not points:
        print(f"[]  # {filename} (0 points)")
        return float("inf"), [], points

    start = time.time()
    sizes = algo(distance, points) if k is None else algo(distance, points, k)
    elapsed_ms = (time.time() - start) * 1000

    print(f"# {algo_name} — {filename} ({len(points)} points): {elapsed_ms:.2f} ms")
    return elapsed_ms, sizes, points


def main() -> None:
    """Auto-detect example files, benchmark both algorithms, and plot results."""
    repo_dir = os.path.dirname(__file__)
    files = sorted(glob.glob(os.path.join(repo_dir, "exemple_*.pts")))

    if not files:
        print("No exemple_*.pts files found in the project directory.")
        return

    algorithms = [
        ("Classic DFS", compute_component_sizes_dfs, None),
        ("Hybrid Greedy-DFS (k=8)", print_components_sizes, 8),
    ]

    print("Benchmarking Classic DFS vs. Hybrid Greedy-DFS (k=8)\n")

    performance_data: Dict[str, List[float]] = {name: [] for name, _, _ in algorithms}
    point_counts: List[int] = []

    for filepath in files:
        print(f"--- {os.path.basename(filepath)} ---")
        point_counts.append(0)

        for algo_name, algo, k in algorithms:
            elapsed, sizes, points = measure_performance(filepath, algo, algo_name, k)
            if not points:
                continue

            performance_data[algo_name].append(elapsed)
            if point_counts[-1] == 0:
                point_counts[-1] = len(points)

            # Uncomment to render a colour-coded scatter plot for each run:
            # visualize_components(
            #     points, sizes,
            #     f"{os.path.basename(filepath)} — {algo_name}"
            # )

        print()

    # --- Performance curve ---
    plt.figure(figsize=(10, 6))
    for algo_name, times in performance_data.items():
        plt.plot(point_counts[: len(times)], times, marker="o", label=algo_name)

    plt.xlabel("Number of points")
    plt.ylabel("Execution time (ms)")
    plt.title("Classic DFS vs. Hybrid Greedy-DFS (k=8) — Performance Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
