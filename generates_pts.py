#!/usr/bin/env python3
"""
Generate a .pts dataset file with random points in [0,1] x [0,1].
Usage:
    python generate_pts.py <num_points> <output_file> [distance]
Example:
    python generate_pts.py 200 exemple_7.pts 0.05
"""

import random
import sys
import os


def generate_pts_file(filename, num_points, distance=0.1):
    """
    Génère un fichier .pts avec `num_points` points aléatoires.
    Chaque point est (x,y) avec x,y dans [0,1].
    """
    with open(filename, "w") as f:
        # Première ligne = distance
        f.write(f"{distance}\n")
        # Points aléatoires
        for _ in range(num_points):
            x = random.random()
            y = random.random()
            f.write(f"{x}, {y}\n")
    print(f" Fichier généré : {filename} ({num_points} points, distance={distance})")


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_pts.py <num_points> <output_file> [distance]")
        sys.exit(1)

    num_points = int(sys.argv[1])
    output_file = sys.argv[2]
    distance = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1

    # ensure file is created in the same directory as this script if relative path
    if not os.path.isabs(output_file):
        output_file = os.path.join(os.path.dirname(__file__), output_file)

    generate_pts_file(output_file, num_points, distance)


if __name__ == "__main__":
    main()