----------------------
ENSEMBLE DE MANDELBROT
----------------------

En adoptant la stratégie 1, qui est de répartir les lignes sur différentes unités de calcul, on obtient le temps de calcul total suivant :

   n   Temps de calcul
   1        6.61
   2        3.16
   3        2.22
   4        1.80
   5        1.56
   6        1.17

Avec une approche maitre esclave, on a les résultats suivant :

   n   Temps de calcul
   2        6.66
   3        3.40
   4        2.26
   5        1.71
   6        1.63

On constate que l'algorithme maitre-esclave marche aussi très bien, mais il ne se démarque pas spéciallement de la première méthode.

----------------------
PRODUIT MATRICIEL
----------------------

Nous allons faire des tests sur un produit matriciel avec ndim = 4800.
Dans ce cas, un produit matricielle classique nous donne un temps de calcul d'environ 0.010 secondes.

Pour la première méthode de paralélisation, en divisant les lignes par unité de calcul, on obtient ces résultats en fonction du nombre de coeur :

   n   Temps de calcul
   1        0.013
   2        0.006
   3        0.701
   4        0.591

On se rend compte que ca ne marche pas trop pour les cas n = 3 et n = 4, pour des raisons que j'ignore. Le temps de calcul est aussi multiplié pour l'initialisation de la matrice, car elle est redéfinit pour chaque processus.

Pour la deuxième méthode de paralélisation, et on a un problème similaire au cas précédent.