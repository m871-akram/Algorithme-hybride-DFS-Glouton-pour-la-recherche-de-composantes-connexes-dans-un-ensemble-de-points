#!/usr/bin/env python3
"""
Compute the sizes of all connected components using a Hybrid Greedy + DFS strategy.

The algorithm seeds each component from an unvisited point and uses a two-phase
traversal:

1. **Greedy phase** – eagerly expands neighbours until the component exceeds *k*
   nodes.  Small isolated clusters are fully handled here without entering the
   heavier counting loop.
2. **Full DFS phase** – drains the remaining stack iteratively, incrementing only
   a counter (no index list kept), which is memory-efficient for large components.

Seeds are evaluated sequentially to guarantee correctness: a component must be
fully explored before the next unvisited seed can be safely identified.
"""

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
    visited: List[bool],
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

    # Caller guarantees start_index is unvisited, but guard defensively.
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

    Iterates sequentially over unvisited seed points, calling
    :func:`compute_cluster` for each one.  Sequential seed evaluation is
    required for correctness: only after one component is fully explored can we
    be sure that the next unvisited point is a genuine new seed.

    Note:
        Parallelising seed dispatch (e.g. with ``multiprocessing.Pool``) is
        unsound for this problem because workers race to claim the same
        neighbours, fragmenting components that should be large.  The algorithmic
        value here lies in the two-phase hybrid DFS inside
        :func:`compute_cluster`, not in multi-process parallelism.

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

    # Plain list: visited flags shared within a single process (no IPC overhead)
    visited: List[bool] = [False] * n

    sizes: List[int] = []
    for i in range(n):
        if not visited[i]:
            # Each seed is fully explored before advancing — this guarantees
            # no two calls ever race over the same point.
            size = compute_cluster(i, distance, points, visited)
            if size > 0:
                sizes.append(size)

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
