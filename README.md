

# Algorithme Hybride DFS-Glouton pour la Recherche de Composantes Connexes

## 📋 Description

Ce projet implémente et compare deux algorithmes pour identifier les composantes connexes dans un ensemble de points 2D basés sur un seuil de distance :

1. **DFS Classique** : Parcours en profondeur récursif standard
2. **Algorithme Hybride DFS-Glouton** : Approche optimisée combinant une phase gloutonne avec DFS, utilisant le multiprocessing pour améliorer les performances

Dans l'analyse de réseaux et l'apprentissage automatique (comme K-means), il est crucial d'identifier les groupes d'éléments qui partagent une proximité géométrique. Ce projet explore différentes approches pour résoudre ce problème efficacement.

## 🚀 Fonctionnalités

- **Calcul de composantes connexes** avec deux algorithmes différents
- **Parallélisation** via multiprocessing pour l'algorithme hybride
- **Visualisation** des composantes avec des couleurs distinctes
- **Comparaison de performance** entre les deux approches
- **Support de fichiers `.pts`** contenant des ensembles de points
- **Génération de graphiques** comparatifs des temps d'exécution

## 📦 Prérequis

- Python 3.13.7
- Packages Python : `matplotlib`, `numpy`

Les dépendances sont déjà installées dans l'environnement conda du projet.

## 📁 Structure du Projet
```

.
├── connectes.py              # Algorithme hybride DFS-Glouton (parallélisé)
├── dfs_connectes.py          # Algorithme DFS classique
├── courbe_performance.py     # Script de comparaison et visualisation
├── generates_pts.py          # Générateur de fichiers de test
├── exemple_*.pts             # Fichiers de test avec points 2D
├── geo/                      # Module géométrique (Point, Segment, etc.)
└── README.md                 # Ce fichier
```
## 🎯 Utilisation

### Calcul avec DFS Classique

```bash
python dfs_connectes.py exemple_1.pts exemple_2.pts
```
```


### Calcul avec Algorithme Hybride

```shell script
python connectes.py exemple_1.pts exemple_2.pts
```


### Comparaison de Performance

```shell script
python courbe_performance.py
```


Ce script :
- Teste automatiquement tous les fichiers `exemple_*.pts`
- Affiche les tailles des composantes connexes
- Mesure les temps d'exécution
- Génère un graphique comparatif

## 📊 Format des Fichiers `.pts`

```
distance_limite
x1,y1
x2,y2
x3,y3
...
```


**Exemple :**
```
1.5
0.0,0.0
1.0,1.0
5.0,5.0
```


La première ligne définit le seuil de distance. Deux points appartiennent à la même composante connexe s'ils sont à une distance ≤ `distance_limite`.

## 🔬 Algorithmes

### DFS Classique
- Parcours en profondeur récursif
- Complexité : O(n²) où n est le nombre de points
- Simple mais peut être lent sur de grands ensembles

### Hybride DFS-Glouton (k=8)
- **Phase gloutonne** : Croissance rapide jusqu'à k voisins
- **Phase DFS** : Parcours complet pour les composantes > k
- **Parallélisation** : Utilise tous les cœurs CPU disponibles
- Optimisé pour de grands ensembles de points

## 📈 Résultats

Le script de comparaison affiche :
- Tailles des composantes triées par ordre décroissant : `[10, 5, 3, 1]`
- Temps d'exécution en millisecondes
- Graphique comparatif des performances

## 📄 Rapport

Le fichier `rapport.pdf` contient l'analyse détaillée des algorithmes, les résultats expérimentaux et les conclusions.

## 👥 Note

J'avais modifie le fichier `connectes.py' avec le paradigme du parallelism (multiprocessing) pour le rendre plus rapide.

