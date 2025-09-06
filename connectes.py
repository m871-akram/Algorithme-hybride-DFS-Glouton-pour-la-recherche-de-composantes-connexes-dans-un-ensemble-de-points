#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from timeit import timeit
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


def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    n = len(points)
    visites = [False] * n
    tailles = []
    k=8 # on a choisi k=8 car c est suppose etre le plus optimal ( voir pdf )

    def glouton(depart):
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

    def dfs(composante_initiale): # pour ce dfs on adopte une approche iterative pour eviter les recurssions limit errors 
        # Continue l exploration a partir des points deja dans composante initiale
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
            composante, basculer = glouton(i)
            if basculer:
                taille = dfs(composante)  # Passer la composante entiere a dfs
            else:
                taille = len(composante)
            tailles.append(taille)

    tailles.sort(reverse=True)

    sortie = "["  
    for i in range(len(tailles)):
        sortie += str(tailles[i]) 
        if i < len(tailles) - 1:
            sortie += ", "  
    sortie += "]"  
    print(sortie)
    return tailles
def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()
