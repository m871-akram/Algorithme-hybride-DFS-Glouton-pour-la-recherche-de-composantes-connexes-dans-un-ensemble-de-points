#!/usr/bin/env python3
"""
Classic recursive DFS implementation for computing connected-component sizes.

This module provides the baseline algorithm against which the Hybrid Greedy+DFS
approach in ``connectes.py`` is benchmarked.  Two points belong to the same
component when their Euclidean distance is at most the threshold stored in the
``.pts`` file.
"""

from sys import argv
from typing import Dict, List, Optional, Tuple

from geo.point import Point


def load_instance(filename: str) -> Tuple[Optional[float], List[Point]]:
    """Load a ``.pts`` dataset file.

    The file format is::

        <distance_threshold>
        <x1>, <y1>
        <x2>, <y2>
        ...

    Args:
        filename: Path to the ``.pts`` file.

    Returns:
        A tuple ``(distance, points)`` on success.  Returns ``(None, [])``
        when the file cannot be read so callers can detect failures without
        catching exceptions.
    """
    try:
        with open(filename, "r") as instance_file:
            lines = iter(instance_file)
            distance = float(next(lines).strip())
            points = [
                Point([float(f) for f in line.split(",")])
                for line in lines
                if line.strip()
            ]
        return distance, points
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None, []


def compute_component_sizes_dfs(distance: float, points: List[Point]) -> List[int]:
    """Compute connected-component sizes with a classic recursive DFS.

    Starting from each unvisited point a depth-first traversal explores all
    reachable neighbours (i.e. those within *distance*) and collects them into
    a component.  Visited points are removed from the working copy so they are
    never seeded again.

    Note:
        Python's default recursion limit (``sys.setrecursionlimit``) may be
        exceeded on large, densely connected datasets.  For those cases use the
        iterative hybrid implementation in :mod:`connectes`.

    Args:
        distance: Maximum Euclidean distance that defines an edge between two
            points.
        points: Complete list of points in the dataset.

    Returns:
        List of component sizes sorted in descending order.
    """
    if not points:
        print("[]")
        return []

    components: Dict[int, List[Point]] = {}

    def _dfs(
        seed: Point,
        all_points: List[Point],
        visited: Optional[List[Point]] = None,
    ) -> List[Point]:
        """Recursively collect all points reachable from *seed*.

        Args:
            seed: The point currently being explored.
            all_points: Complete point list used for neighbour lookup.
            visited: Accumulator of points already confirmed in this component.
                Initialised to ``[seed]`` on the first call.

        Returns:
            Final list of every point in the component that contains *seed*.
        """
        if visited is None:
            visited = [seed]
        for candidate in all_points:
            # A candidate joins this component if it is within reach and not
            # yet assigned — checking membership via ``not in`` is O(n) but
            # acceptable for the dataset sizes targeted here.
            if seed.distance_to(candidate) <= distance and candidate not in visited:
                visited.append(candidate)
                _dfs(candidate, all_points, visited)
        return visited

    component_id = 0
    remaining = points.copy()  # working copy — shrinks as components are found
    while remaining:
        seed = remaining[0]
        components[component_id] = _dfs(seed, points)
        # Remove every discovered point from the unvisited pool
        for point in components[component_id]:
            if point in remaining:
                remaining.remove(point)
        component_id += 1

    sizes = sorted((len(comp) for comp in components.values()), reverse=True)

    if not sizes:
        print("[]")
    else:
        print("[" + ", ".join(map(str, sizes)) + "]")

    return sizes


def main() -> None:
    """Entry point: process one or more ``.pts`` files passed on the command line."""
    if len(argv) < 2:
        print("Usage: python dfs_connectes.py file.pts")
        return

    for filename in argv[1:]:
        distance, points = load_instance(filename)
        if distance is not None:
            print(f"# {filename} ({len(points)} points)")
            compute_component_sizes_dfs(distance, points)


if __name__ == "__main__":
    main()
