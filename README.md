# Algorithme Hybride DFS-Glouton pour la Recherche de Composantes Connexes

Ce dépôt compare deux stratégies pour regrouper des points 2D en composantes connexes en fonction d'un seuil de distance. Il met face à face :

1. un parcours en profondeur (DFS) récursif classique ;
2. une variante hybride combinant une heuristique gloutonne et un DFS parallélisé via `multiprocessing`.

Les scripts permettent de charger des jeux de points, de calculer les composantes, de visualiser les regroupements et de mesurer les gains de performance.

## Fonctionnalités majeures
- Calcul des composantes connexes avec DFS classique ou approche hybride parallèle.
- Chargement de fichiers `.pts` et génération de jeux synthétiques.
- Comparaison de performances avec graphiques `matplotlib`.
- Visualisation optionnelle des composantes (coloration par cluster).
- Rapport PDF détaillant méthodologie et résultats.

## Structure du projet
```text
.
├── connectes.py              # Algorithme hybride DFS-Glouton (multiprocessing)
├── courbe_performance.py     # Benchmark et visualisations
├── dfs_connectes.py          # Implémentation DFS classique
├── generates_pts.py          # Générateur de fichiers .pts aléatoires
├── exemple_*.pts             # Jeux de test fournis
├── LeLabyrinthe/             # Générateur de labyrinthes et rendu PNG
├── geo/                      # Primitives géométriques (Point, Segment, ...)
├── rapport.pdf               # Analyse technique détaillée
└── README.md                 # Documentation
```

## Prise en main

### Prérequis
- Python 3.10 ou plus récent.
- `pip` ou `pipx` pour installer les dépendances.
- `matplotlib` et `numpy` pour les graphes et visualisations.
- (Optionnel) `Pillow` si vous utilisez le module `LeLabyrinthe`.


### Vérification rapide
```bash
python dfs_connectes.py exemple_1.pts
python connectes.py exemple_1.pts
```

## Format des fichiers `.pts`
```
distance_max
x1,y1
x2,y2
...
```
Exemple :
```
1.5
0.0,0.0
1.0,1.0
5.0,5.0
```
La première ligne fixe la distance maximale autorisée. Deux points appartiennent à la même composante si leur distance est inférieure ou égale à cette valeur.

## Utilisation des scripts

#### DFS classique
Calcule les tailles des composantes dans l'ordre décroissant.
```bash
python dfs_connectes.py exemple_1.pts exemple_2.pts
```

#### Algorithme hybride DFS-Glouton
Version parallèle reposant sur une croissance gloutonne initiale puis DFS. Affiche les tailles triées.
```bash
python connectes.py exemple_1.pts exemple_3.pts
```

#### Comparaison de performances
Exécute automatiquement les deux algorithmes sur tous les fichiers `exemple_*.pts`, mesure les temps et trace une courbe comparative.
```bash
python courbe_performance.py
```
> `matplotlib` ouvre une fenêtre interactive ; utilisez un backend non interactif (`MPLBACKEND=Agg`) si vous travaillez sur un serveur sans affichage.

#### Génération de jeux de données
Crée un fichier `.pts` de taille arbitraire afin d'alimenter les scripts de calcul.
```bash
python generates_pts.py 200 data/mon_jeu.pts 0.05
```
Arguments : nombre de points, chemin de sortie (relatif ou absolu) et seuil de distance (optionnel, 0.1 par défaut).

## Module LeLabyrinthe
Le dossier `LeLabyrinthe/` contient un générateur de labyrinthes basé sur une exploration DFS. Il produit une image `maze.png` représentant la grille.

- Dépendances : `Pillow` (installable via `pip install pillow`).
- Exécution :
  ```bash
  python LeLabyrinthe/Labyrinthe.py
  ```
- Le script vous demande la taille du labyrinthe ainsi que la case de départ, puis enregistre le résultat dans `LeLabyrinthe/maze.png`. Les classes utilitaires `cell.py` et `maze.py` peuvent servir d'exemple d'utilisation de DFS sur une structure quadrillée.

## Visualisation optionnelle
La fonction `visualiser_composantes` de `courbe_performance.py` peut être activée pour afficher les clusters colorés. Décommentez l'appel correspondant dans la boucle principale afin de générer un nuage de points pour chaque jeu de données et chaque algorithme.

## Résultats et rapport
- Les scripts affichent les tailles des composantes sous la forme `[taille1, taille2, ...]`.
- `courbe_performance.py` produit un graphique des temps d'exécution (en ms) en fonction du nombre de points.
- Le fichier `rapport.pdf` décrit l'approche, les paramètres retenus et les analyses expérimentales.

Bonnes explorations !
