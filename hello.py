#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualisation avec matplotlib
"""
from math import cos, sin, pi
import matplotlib.pyplot as plt

def main():
    print("Affichage avec matplotlib")
    # Point à l'origine
    origine = [0.0, 0.0]
    # Points sur le cercle
    cercle = [[cos(c * pi / 10), sin(c * pi / 10)] for c in range(20)]
    # Segments reliant les points
    segments = [(p1, p2) for p1, p2 in zip(cercle, cercle[1:] + [cercle[0]])]

    # Tracé
    plt.scatter(*origine, color='red', label='Origine', s=50)
    plt.scatter([p[0] for p in cercle], [p[1] for p in cercle], color='green', label='Cercle', s=30)
    for seg in segments:
        plt.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], color='blue')
    
    plt.gca().set_aspect('equal')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()