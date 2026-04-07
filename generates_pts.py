#!/usr/bin/env python3
"""
Generate synthetic ``.pts`` dataset files with uniformly random 2D points.

Each point is drawn independently from [0, 1] × [0, 1].  The output file
starts with the distance threshold on the first line, followed by one
``x, y`` coordinate pair per line.

Usage::

    python generates_pts.py <num_points> <output_file> [distance]

Example::

    python generates_pts.py 200 exemple_5.pts 0.05
"""

import os
import random
import sys


def generate_pts_file(filename: str, num_points: int, distance: float = 0.1) -> None:
    """Write a ``.pts`` file containing random 2D points.

    Args:
        filename: Output file path (absolute or relative to the script directory).
        num_points: Number of random points to generate.
        distance: Distance threshold written to the first line of the file.
            Two points whose Euclidean distance is ≤ this value will be
            considered connected.  Defaults to ``0.1``.
    """
    with open(filename, "w") as f:
        # First line: the distance threshold consumed by the algorithm scripts
        f.write(f"{distance}\n")
        for _ in range(num_points):
            x = random.random()
            y = random.random()
            f.write(f"{x}, {y}\n")

    print(f"Generated: {filename} ({num_points} points, distance={distance})")


def main() -> None:
    """Parse command-line arguments and generate the ``.pts`` file."""
    if len(sys.argv) < 3:
        print("Usage: python generates_pts.py <num_points> <output_file> [distance]")
        sys.exit(1)

    num_points = int(sys.argv[1])
    output_file = sys.argv[2]
    distance = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1

    # Resolve relative paths against the script's own directory so the file
    # lands next to the other example datasets regardless of the working directory.
    if not os.path.isabs(output_file):
        output_file = os.path.join(os.path.dirname(__file__), output_file)

    generate_pts_file(output_file, num_points, distance)


if __name__ == "__main__":
    main()
