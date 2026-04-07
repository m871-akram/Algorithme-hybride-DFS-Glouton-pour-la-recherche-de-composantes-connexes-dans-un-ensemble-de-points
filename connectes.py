#!/usr/bin/env python3
"""
Compute the sizes of all connected components using a Hybrid Greedy + DFS strategy.

The algorithm seeds each component from an unvisited point and uses a two-phase
traversal:

1. **Greedy phase** – eagerly expands neighbours until the component exceeds *k*
   nodes, which filters out small isolated clusters cheaply.
2. **Full DFS phase** – drains the remaining stack with a classic iterative DFS,
   counting every reachable node without storing indices in memory.

Component discovery across different seed points is parallelised via
``multiprocessing.Pool``, distributing work over all available CPU cores.
"""

import multiprocessing as mp
from sys import argv
from typing import List, Tuple

from geo.point import Point


def load_instance(filename: str) -> Tuple[float, List[Point]]:
    """Load a ``.pts`` dataset file.

    The file format is::

        <distance_threshold>
        <x1>, <y1>
        <x2>, <y2>
        ...

    Args:
        filename: Path to the ``.pts`` file.

    Returns:
        A tuple ``(distance, points)`` where *distance* is the maximum
        Euclidean distance that connects two points into the same component,
        and *points* is the list of parsed :class:`~geo.point.Point` objects.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in line.split(",")]) for line in lines]

    return distance, points


def compute_cluster(
    start_index: int,
    distance: float,
    points: List[Point],
    visited: "mp.managers.ListProxy",
    k: int = 8,
) -> int:
    """Compute the size of one connected component from a seed point.

    Uses a two-phase hybrid strategy:

    * **Phase 1 — Greedy expansion**: pop nodes from a stack and mark all
      reachable neighbours as visited.  Stop as soon as the component has more
      than *k* nodes — tiny isolated clusters are handled entirely here.
    * **Phase 2 — Full iterative DFS**: for larger components, drain the
      remaining stack while only incrementing a counter (no index list kept in
      memory), which is more memory-efficient at scale.

    Args:
        start_index: Index of the seed point in *points*.
        distance: Maximum Euclidean distance that defines an edge.
        points: Complete list of points in the dataset.
        visited: Shared boolean list managed across worker processes; ``True``
            means the point has already been claimed by a component.
        k: Greedy-phase threshold.  When the component grows beyond *k* nodes
            the algorithm switches to the pure counting DFS.

    Returns:
        Size of the discovered component, or ``0`` if *start_index* was already
        visited by another worker process before this call began.
    """
    n = len(points)

    # Guard: another process may have claimed this seed between the caller's
    # unvisited check and this function actually executing.
    if visited[start_index]:
        return 0

    visited[start_index] = True
    component: List[int] = [start_index]  # index accumulator for phase 1
    stack: List[int] = [start_index]

    # --- Phase 1: Greedy expansion ---
    # Keep a full index list so we can restart DFS from any already-visited node.
    while stack:
        if len(component) > k:
            break  # hand off to full DFS — component is large enough
        current = stack.pop()
        for neighbour in range(n):
            if (
                not visited[neighbour]
                and points[current].distance_to(points[neighbour]) <= distance
            ):
                visited[neighbour] = True
                component.append(neighbour)
                stack.append(neighbour)

    # --- Phase 2: Full iterative DFS ---
    # Only the running count is maintained; individual indices are discarded.
    component_size = len(component)
    while stack:
        current = stack.pop()
        for neighbour in range(n):
            if (
                not visited[neighbour]
                and points[current].distance_to(points[neighbour]) <= distance
            ):
                visited[neighbour] = True
                component_size += 1
                stack.append(neighbour)

    return component_size


def print_components_sizes(
    distance: float,
    points: List[Point],
    verbose: bool = True,
) -> List[int]:
    """Discover all connected components and (optionally) print their sizes.

    Iterates over unvisited seed points and dispatches each
    :func:`compute_cluster` call to a worker in a ``multiprocessing.Pool``,
    enabling parallel execution across all available CPU cores.

    A :class:`~multiprocessing.managers.SyncManager` list is used for the
    *visited* flags so that worker processes share a single consistent view of
    which points have been claimed.

    Args:
        distance: Maximum Euclidean distance that connects two points.
        points: Complete list of points in the dataset.
        verbose: When ``True``, print the sorted sizes to stdout in the form
            ``[size1, size2, ...]``.

    Returns:
        Component sizes sorted in descending order.
    """
    n = len(points)
    if n == 0:
        return []

    # Manager provides a shared list visible to all worker processes
    manager = mp.Manager()
    visited = manager.list([False] * n)

    sizes: List[int] = []
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pending = []
        for i in range(n):
            if not visited[i]:
                # Submit one async task per unvisited seed point
                pending.append(
                    pool.apply_async(compute_cluster, (i, distance, points, visited))
                )

        # Collect results; zero means the seed was already taken by another worker
        for async_result in pending:
            value = async_result.get()
            if value > 0:
                sizes.append(value)

    sizes.sort(reverse=True)

    if verbose:
        print("[" + ", ".join(map(str, sizes)) + "]")

    return sizes


def main() -> None:
    """Entry point: process one or more ``.pts`` files passed on the command line."""
    instances = argv[1:]
    if not instances:
        print("Usage: python connectes.py file1.pts file2.pts ...")
        return

    for filename in instances:
        try:
            distance, points = load_instance(filename)
            print(f"# {filename} ({len(points)} points)")
            print_components_sizes(distance, points)
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    main()
