#!/usr/bin/env python3
"""
Compare DFS classique and hybrid greedy-DFS (k=8) for computing connected component sizes.
Print sizes in the format [size1, size2, ..., sizeN] for each file and algorithm.
Optionally measure performance, visualize components, and plot execution times.
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from connectes import print_components_sizes
from dfs_connectes import lire_fichier_points, calcul_tailles_composantes_dfs_classique


# ----------- UTILS -----------

def algo_name(algo, k):
    """Retourne le nom affiché d’un algorithme"""
    name = algo.__name__.replace("calcul_tailles_composantes_", "").replace("print_components_sizes", "hybride")
    return f"{name} (k={k})" if k is not None else name


def visualiser_composantes(points, tailles, titre="Composantes"):
    """Visualise les composantes connexes avec des couleurs distinctes."""
    if not points or not tailles:
        print(f"Aucune composante à visualiser pour {titre}")
        return

    id_composante = []
    for idx, taille in enumerate(tailles, start=1):
        id_composante.extend([idx] * taille)

    plt.figure(figsize=(8, 8))
    couleurs = plt.colormaps['rainbow'](np.linspace(0, 1, max(id_composante) + 1))
    for i, p in enumerate(points):
        plt.scatter(p.coordinates[0], p.coordinates[1], c=[couleurs[id_composante[i]]], s=10)

    plt.title(titre)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


def mesurer_performance(nom_fichier, algo, k=None):
    """Mesure le temps d'exécution d'un algorithme sur un fichier."""
    distance, points = lire_fichier_points(nom_fichier)
    if not points:
        print(f"[]  # {nom_fichier} (0 points)")
        return float('inf'), [], points

    debut = time.time()
    tailles = algo(distance, points) if k is None else algo(distance, points, k)
    temps_ms = (time.time() - debut) * 1000

    nom_algo = algo_name(algo, k)
    print(f"# {nom_algo} - {nom_fichier} ({len(points)} points) : {temps_ms:.2f} ms")
    return temps_ms, tailles, points


# ----------- MAIN -----------

def main():
    import glob, os

    # détecter tous les fichiers exemple_*.pts
    repo_dir = os.path.dirname(__file__)
    fichiers = sorted(glob.glob(os.path.join(repo_dir, "exemple_*.pts")))

    if not fichiers:
        print("⚠️ Aucun fichier exemple_*.pts trouvé dans le répertoire.")
        return

    algorithmes = [
        # (calcul_tailles_composantes_dfs_classique, None),
        (print_components_sizes, 8)   # directly use the imported function
    ]

    print("Comparaison DFS Classique vs DFS-Glouton (k=8) sur fichiers exemple_*.pts")

    donnees_performance = {algo_name(a, k): [] for a, k in algorithmes}
    nombres_points = []

    for fichier in fichiers:
        print(f"\nTest sur {os.path.basename(fichier)} :")
        nombres_points.append(0)

        for algo, k in algorithmes:
            temps, tailles, points = mesurer_performance(fichier, algo, k)
            if not points:
                continue

            nom_algo = algo_name(algo, k)
            donnees_performance[nom_algo].append(temps)
            if nombres_points[-1] == 0:
                nombres_points[-1] = len(points)

            # Visualisation (décommenter si nécessaire)
            visualiser_composantes(points, tailles, f"Composantes pour {os.path.basename(fichier)} ({nom_algo})")

    # Tracé des performances
    plt.figure(figsize=(10, 6))
    for nom_algo, temps in donnees_performance.items():
        plt.plot(nombres_points[:len(temps)], temps, marker='o', label=nom_algo)
    plt.xlabel("Nombre de points")
    plt.ylabel("Temps d'exécution (ms)")
    plt.title("Comparaison DFS Classique vs DFS-Glouton (k=8)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()