#!/usr/bin/env python3
"""
Module contenant :
- lecture d'un fichier de points .pts
- calcul des composantes connexes avec DFS classique
"""

from geo.point import Point


def lire_fichier_points(nom_fichier):
    """
    Lit un fichier de points au format : distance en première ligne, puis x, y par ligne.
    Retourne (distance, points).
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

    c_connexes = {}

    def connexe(p1, points, sommets=None):
        """
        Parcours en profondeur récursif.
        Détermine la composante connexe à laquelle appartient le point p1.
        """
        if sommets is None:
            sommets = [p1]
        for p2 in points:
            if p1.distance_to(p2) <= distance and p2 not in sommets:
                sommets.append(p2)
                connexe(p2, points, sommets)
        return sommets

    indice = 0
    copie = points.copy()
    while copie:
        p1 = copie[0]
        c_connexes[indice] = connexe(p1, points)
        for p2 in c_connexes[indice]:
            if p2 in copie:
                copie.remove(p2)
        indice += 1

    tailles = [len(composante) for composante in c_connexes.values()]
    tailles.sort(reverse=True)

    if not tailles:
        print("[]")
    else:
        sortie = "[" + ", ".join(map(str, tailles)) + "]"
        print(sortie)

    return tailles