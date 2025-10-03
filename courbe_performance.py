#!/usr/bin/env python3
"""
Compare DFS classique and hybrid greedy-DFS (k=8) for computing connected component sizes.
Print sizes in the format [size1, size2, ..., sizeN] for each file and algorithm.
Optionally measure performance, visualize components, and plot execution times.
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from geo.point import Point


def lire_fichier_points(nom_fichier):
    """
    Lit un fichier de points au format : distance en première ligne, puis x, y par ligne.
    """
    try:
        with open(nom_fichier, 'r') as f:
            lignes = f.readlines()
        # Première ligne : distance
        distance = float(lignes[0].strip())
        points = []
        for ligne in lignes[1:]:
            ligne = ligne.strip()
            if not ligne:
                continue
            # Séparer sur ', ' pour gérer le format x, y
            try:
                x, y = map(float, ligne.split(', '))
                points.append(Point([x, y]))
            except ValueError as e:
                print(f"Erreur de format dans la ligne : {ligne} ({e})")
                continue
        return distance, points
    except Exception as e:
        print(f"Erreur lors de la lecture de {nom_fichier} : {e}")
        return None, []


def calcul_tailles_composantes_dfs_classique(distance, points):
    """
    Calcule les tailles des composantes connexes avec DFS classique.
    """
    if not points:
        print("[]")
        return []

    # Dictionnaire pour stocker les composantes connexes
    c_connexes = {}
    
    def connexe(p1, points, sommets=None):
        """
        Algorithme de parcours en profondeur.
        Détermine la composante connexe à laquelle appartient le point p1.
        """
        if sommets is None:
            # Si le point n'appartient à aucune composante connexe, on l'initialise
            sommets = [p1]
        for p2 in points:
            # On recherche les voisins de p1
            if p1.distance_to(p2) <= distance and p2 not in sommets:
                sommets.append(p2)
                connexe(p2, points, sommets)  # On recherche les voisins de voisins
        return sommets

    indice = 0
    copie = points.copy()
    # On construit chaque composante connexe
    while copie:  # Continue tant qu'il reste des points non traités
        p1 = copie[0]  # Prendre le premier point restant
        c_connexes[indice] = connexe(p1, points)  # Trouver sa composante connexe
        # Supprimer les points de cette composante de la copie
        for p2 in c_connexes[indice]:
            if p2 in copie:
                copie.remove(p2)
        indice += 1

    # Calculer les tailles des composantes
    tailles = []
    for composante in c_connexes.values():  # Utiliser .values() pour obtenir les listes de points
        tailles.append(len(composante))  # Ajouter la taille de la composante
    tailles.sort(reverse=True)  # Trier par ordre décroissant
    
    # Afficher au format [size1, size2, ..., sizeN]
    if not tailles:
        print("[]")
    else:
        sortie = "["  
        for i in range(len(tailles)):
            sortie += str(tailles[i]) 
            if i < len(tailles) - 1:
                sortie += ", "  
        sortie += "]"  
        print(sortie)
    return tailles


def calcul_tailles_composantes_hybride_dfs_glouton(distance, points, k=8):
    """
    Calcule les tailles des composantes avec un algorithme hybride (glouton + DFS).
    """
    if not points:
        print("[]")
        return []

    n = len(points)
    visites = [False] * n
    tailles = []

    def cluster_gourmand(depart):
        composante = [depart]
        visites[depart] = True
        pile = [depart]
        while pile:
            if len(composante) > k:
                return composante, True
            courant = pile.pop()
            for voisin in range(n):
                if not visites[voisin] and points[courant].distance_to(points[voisin]) <= distance:
                    composante.append(voisin)
                    pile.append(voisin)
                    visites[voisin] = True
        return composante, False

    def dfs(composante_initiale):
        # Continue l'exploration à partir des points déjà dans composante_initiale
        taille_composante = len(composante_initiale)
        pile = composante_initiale.copy()  # Commencer avec tous les points de la composante initiale
        while pile:
            courant = pile.pop()
            for voisin in range(n):
                if not visites[voisin] and points[courant].distance_to(points[voisin]) <= distance:
                    pile.append(voisin)
                    visites[voisin] = True
                    taille_composante += 1
        return taille_composante

    for i in range(n):
        if not visites[i]:
            composante, basculer = cluster_gourmand(i)
            if basculer:
                taille = dfs(composante)  # Passer la composante entière à dfs
            else:
                taille = len(composante)
            tailles.append(taille)

    tailles.sort(reverse=True)
    if not tailles:
        print("[]")
    else:
        sortie = "["  
        for i in range(len(tailles)):
            sortie += str(tailles[i]) 
            if i < len(tailles) - 1:
                sortie += ", "  
        sortie += "]"  
        print(sortie)
    return tailles


def visualiser_composantes(points, tailles, n, titre="Composantes"):
    """
    Visualise les composantes connexes avec des couleurs distinctes.
    """
    if not points or not tailles:
        print(f"Aucune composante à visualiser pour {titre}")
        return

    id_composante = [0] * len(points)
    id_courant = 1
    decalage = 0
    for taille in tailles:
        for i in range(decalage, decalage + taille):
            id_composante[i] = id_courant
        id_courant += 1
        decalage += taille

    plt.figure(figsize=(8, 8))
    couleurs = plt.colormaps['rainbow'](np.linspace(0, 1, max(id_composante) + 1))
    for i, p in enumerate(points):
        plt.scatter(p.coordinates[0], p.coordinates[1], c=[couleurs[id_composante[i]]], s=10)
    plt.title(titre)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


def mesurer_performance(nom_fichier, algorithme, k=None):
    """
    Mesure le temps d'exécution d'un algorithme sur un fichier.
    """
    distance, points = lire_fichier_points(nom_fichier)
    if not points:
        print(f"[]  # {nom_fichier} (0 points)")
        return float('inf'), [], points
    
    debut = time.time()
    if k is None:
        tailles = algorithme(distance, points)
    else:
        tailles = algorithme(distance, points, k)
    temps_ms = (time.time() - debut) * 1000
    
    nom_algo = algorithme.__name__.replace("calcul_tailles_composantes_", "")
    if k is not None:
        nom_algo += f" (k={k})"
    print(f"# {nom_algo} - {nom_fichier} ({len(points)} points) : {temps_ms:.2f} ms")
    return temps_ms, tailles, points


def principal():
    """
    Fonction principale pour tester DFS classique et DFS-glouton (k=8) sur exemple_*.pts.
    """
    fichiers = [f"exemple_{i}.pts" for i in range(1, 5)]
    algorithmes = [
        (calcul_tailles_composantes_dfs_classique, None),
        (calcul_tailles_composantes_hybride_dfs_glouton, 8)
    ]

    print("Comparaison DFS Classique vs DFS-Glouton (k=8) sur fichiers exemple_*.pts")
    donnees_performance = {f"{algo[0].__name__.replace('calcul_tailles_composantes_', '')}{f' (k={algo[1]})' if algo[1] is not None else ''}": [] for algo in algorithmes}
    nombres_points = []

    for fichier in fichiers:
        print(f"\nTest sur {fichier} :")
        nombres_points.append(0)
        for algo, k in algorithmes:
            temps_moyen, tailles, points = mesurer_performance(fichier, algo, k)
            if points:  # Only append if the file was successfully processed
                algo_nom = f"{algo.__name__.replace('calcul_tailles_composantes_', '')}{f' (k={k})' if k is not None else ''}"
                donnees_performance[algo_nom].append(temps_moyen)
                if nombres_points[-1] == 0:
                    nombres_points[-1] = len(points)
                # Comment out visualization to reduce clutter, uncomment if needed
                # visualiser_composantes(points, tailles, len(points), f"Composantes pour {fichier} ({algo_nom})")

    # Tracé des performances (commented out by default)

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
    principal()