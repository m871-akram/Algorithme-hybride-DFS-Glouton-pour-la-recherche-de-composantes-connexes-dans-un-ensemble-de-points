#!/usr/bin/env python3
"""
Compute sizes of all connected components using hybrid greedy+DFS.
Parallelize the computation of clusters with multiprocessing.
"""

import multiprocessing as mp
from sys import argv
from geo.point import Point


def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]

    return distance, points


def compute_cluster(start_index, distance, points, visites, k=8):
    """
    Calcule la taille d'une composante connexe en partant du point start_index.
    On suppose que start_index n'a pas encore été visité.
    """
    n = len(points)

    if visites[start_index]:
        return 0

    visites[start_index] = True
    composante = [start_index]
    pile = [start_index]

    # phase glouton
    while pile:
        if len(composante) > k:
            break  # bascule en DFS classique
        courant = pile.pop()
        for voisin in range(n):
            if not visites[voisin] and points[courant].distance_to(points[voisin]) <= distance:
                visites[voisin] = True
                composante.append(voisin)
                pile.append(voisin)

    # DFS complet si nécessaire
    taille_composante = len(composante)
    while pile:
        courant = pile.pop()
        for voisin in range(n):
            if not visites[voisin] and points[courant].distance_to(points[voisin]) <= distance:
                visites[voisin] = True
                taille_composante += 1
                pile.append(voisin)

    return taille_composante


def print_components_sizes(distance, points, verbose=True):
    """
    Calcule et affiche les tailles triees des composantes en parallèle.
    """
    n = len(points)
    if n == 0:
        return []

    manager = mp.Manager()
    visites = manager.list([False] * n)  # shared list for visited flags

    tailles = []
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = []
        for i in range(n):
            if not visites[i]:
                results.append(pool.apply_async(compute_cluster, (i, distance, points, visites)))

        tailles = [res.get() for res in results if res.get() > 0]

    tailles.sort(reverse=True)

    if verbose:
        print("[" + ", ".join(map(str, tailles)) + "]")

    return tailles


def process_instance(filename):
    """
    Charge et traite un fichier .pts
    """
    try:
        distance, points = load_instance(filename)
        print(f"# {filename} ({len(points)} points)")
        return filename, print_components_sizes(distance, points)
    except Exception as e:
        print(f"Erreur lors du traitement de {filename} : {e}")
        return filename, []


def main():
    """
    Traite les fichiers donnés en ligne de commande
    """
    instances = argv[1:]
    if not instances:
        print("Usage: python connectes.py fichier1.pts fichier2.pts ...")
        return

    for instance in instances:
        process_instance(instance)


if __name__ == "__main__":
    main()