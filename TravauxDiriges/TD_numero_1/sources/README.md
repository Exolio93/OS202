
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`





## lscpu

```
coller ici les infos *utiles* de lscpu. 
```
Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         48 bits physical, 48 bits vir
                         tual
  Byte Order:            Little Endian
CPU(s):                  6
  On-line CPU(s) list:   0-5
Vendor ID:               AuthenticAMD
  Model name:            AMD Ryzen 5 4500U with Radeon
                          Graphics
    CPU family:          23
    Model:               96
    Thread(s) per core:  1
    Core(s) per socket:  6
    Socket(s):           1
    Stepping:            1
    BogoMIPS:            4740.89

*Des infos utiles s'y trouvent : nb core, taille de cache*



## Produit matrice-matrice

./TestProductMatrix.exe 1023
Test passed
Temps CPU produit matrice-matrice naif : 2.43747 secondes
MFlops -> 1509.12

./TestProductMatrix.exe 1024
Test passed
Temps CPU produit matrice-matrice naif : 4.41423 secondes
MFlops -> 599.29

./TestProductMatrix.exe 1025
Test passed
Temps CPU produit matrice-matrice naif : 2.92728 secondes
MFlops -> 1388.55

### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlops  | MFlops(n=2048) 
------------------|---------|---------|----------------
i,j,k (origine)   | 3.72444 | 932.434 | -        
j,i,k             | 5.03849 | 632.421 | -
i,k,j             | 20.6498 | 219.35  | -
k,i,j             | 21.9223 | 157.435 | - 
j,k,i             | 1.738733| 2955.14 | 1877.43
k,j,i             | 1.992716| 2408.65 | 1730.74


*Discussion des résultats*



### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 |         |
2                 |         |
3                 |         |  
4                 |         |
5                 |         |
6                 |         |
7                 |         |  
8                 |         |




### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  |
64                |  |
128               |  |
256               |  |
512               |  | 
1024              |  |




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |         |                |                |               |
512            |  8      |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
