#!/usr/bin/env python3
"""
Module contenant :
- lecture d'un fichier de points .pts (via load_instance)
- calcul des composantes connexes avec DFS classique
"""

from geo.point import Point


def load_instance(filename):
    """
    Charge un fichier .pts :
    Première ligne = distance limite,
    puis les coordonnées x,y séparées par des virgules.
    Retourne (distance, points)
    """
    try:
        with open(filename, "r") as instance_file:
            lines = iter(instance_file)
            distance = float(next(lines).strip())
            points = [Point([float(f) for f in line.split(",")]) for line in lines if line.strip()]
        return distance, points
    except Exception as e:
        print(f"Erreur lors de la lecture de {filename} : {e}")
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
        print("[" + ", ".join(map(str, tailles)) + "]")

    return tailles


def main():
    """
    Permet de lancer le calcul sur un fichier donné en argument.
    """
    from sys import argv
    if len(argv) < 2:
        print("Usage: python dfs_connectes.py fichier.pts")
        return

    for filename in argv[1:]:
        distance, points = load_instance(filename)
        if distance is not None:
            print(f"# {filename} ({len(points)} points)")
            calcul_tailles_composantes_dfs_classique(distance, points)


if __name__ == "__main__":
    main()