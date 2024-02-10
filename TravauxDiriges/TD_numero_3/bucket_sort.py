# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI
import time
import random

# Dimension du problème (peut-être changé)
dim = 10000
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()
t1 = time.time()

tab = [random.randint(1,dim) for _ in range(dim)]


n = dim // comm_size
a = rank * n
b = a + n if rank < comm_size - 1 else dim


t = tab[a:b]
for i in range(1, len(t)):
    key = t[i]
    j = i - 1
    while j >= 0 and t[j] > key:
        t[j + 1] = t[j]
        j -= 1
    t[j + 1] = key


result = comm.gather(t,root = 0)
t2 = time.time()

if (rank ==0):
    print("Temps de calcul des tris parallèles : ", t2-t1)
    sorted = []
    sorting_ind = []
    for k in range(comm_size):
        pos = 0
        while pos<len(sorting_ind) and result[k][0] > result[sorting_ind[pos]][0]:
            pos += 1    
        sorting_ind.insert(pos,k)
        
    while(sorting_ind !=[]):
        i = sorting_ind[0]
        sorted.append(result[i][0])
        result[i].pop(0)
        sorting_ind.pop(0)
        if result[i] !=[]:
            pos = 0
            while pos<len(sorting_ind) and result[i][0] > result[sorting_ind[pos]][0]:
                pos += 1    
            sorting_ind.insert(pos,i)

    t3 = time.time()
    print("Temps du rassemblement des listes triées : ", t3-t2)
    print("Temps du tri complet : ", t3-t1)

    print(comm_size,"     |"," {:.3f}        |".format(t2-t1)," {:.3f}        |".format(t3-t2)," {:.3f} |".format(t3-t1))

#     v2 = results[0]
#     for k in range(1,comm_size):
#         v2 += results[k]
#     t2 = t.time()
#     print(t2-t1)
    