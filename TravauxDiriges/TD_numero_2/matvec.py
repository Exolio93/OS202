# Produit matrice-vecteur v = A.u
import numpy as np
from mpi4py import MPI
import time as t
# Dimension du problème (peut-être changé)
dim = 4800
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])
# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])


#########################
# PRODUIT MATRICIEL CLASSIQUE
#########################

# t1 = t.time()
# v = A.dot(u)
# t2 = t.time()
# print(t2-t1)

#########################
# PARALELISATION 1
#########################

# t1 = t.time()
# comm = MPI.COMM_WORLD
# rank = comm.Get_rank()
# comm_size = comm.Get_size()

# chunk_size = dim // comm_size
# a = rank * chunk_size
# b = a + chunk_size if rank < comm_size - 1 else dim


# local = A[a:b,:].dot(u)
# results = comm.gather(local, root=0)

# if rank == 0:
#     v2 = np.hstack(results)
#     t2 = t.time()
#     print(t2-t1)
    
    
#########################
# PARALELISATION 2
#########################

t1 = t.time()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

chunk_size = dim // comm_size
a = rank * chunk_size
b = a + chunk_size if rank < comm_size - 1 else dim


local = A[:,a:b].dot(u[a:b])
results = comm.gather(local, root=0)

if rank == 0:
    v2 = results[0]
    for k in range(1,comm_size):
        v2 += results[k]
    t2 = t.time()
    print(t2-t1)
    