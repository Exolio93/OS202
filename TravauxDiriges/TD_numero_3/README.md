# TD n°3 - parallélisation du Bucket Sort

Le bucket sort a ici été réalisé en 2 étapes : 
- Une première étape de parallelisation, où chaque unité de calcul trie une sous-liste avec un tri par insertion
- Une deuxième étape, ou on rassemble les listes triées en une seule.

Les temps de calculs sont indiqué ici :

Taille | Tri parallèle | Rassemblement | Total  |
1      |  6.959        |  0.017        |  6.976 |
2      |  1.833        |  0.017        |  1.850 |
3      |  0.773        |  0.017        |  0.791 |
4      |  0.519        |  0.018        |  0.536 |
5      |  0.412        |  0.018        |  0.430 |
6      |  0.312        |  0.022        |  0.334 |