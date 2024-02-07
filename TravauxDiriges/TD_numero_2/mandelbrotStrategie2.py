# Calcul de l'ensemble de Mandelbrot en python
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
import matplotlib.pyplot as plt
from mpi4py import MPI



comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()


@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations


# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024
result = np.zeros((width, height))

scaleX = 3./width
scaleY = 2.25/height
convergence = np.empty((width, height), dtype=np.double)
# Calcul de l'ensemble de mandelbrot :

def calculateLine(y):
    l = []
    for x in range(width):
        c = complex(-2. + scaleX*x, -1.125 + scaleY * y)
        l.append(mandelbrot_set.convergence(c, smooth=True))
    return l

def writeLine(y,l):
    for x in range (width):
        result[x,y] = l[x]

def master():
    y = 0
    for n in range(1,comm_size):
        comm.send(y, dest = n)
        y += 1
    while y< width:
        status = MPI.Status()
        data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        writeLine(data[0],data[1])
        comm.send(y, dest = source)
        y += 1
        
        
            
def slave():
    while True:
        y = comm.recv(source=0)
        l = calculateLine(y)
        
        if y is None:
            break

        comm.send((y,l), dest=0)



if rank == 0:
    deb = time()
    master()
    fin = time()
    print(f"Temps du calcul de l'ensemble de Mandelbrot : {fin-deb}")
    
    deb = time()
    plt.imshow(result)
    plt.show()
    plt.savefig('mon_image.png')
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
else :
    slave()

