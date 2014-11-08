from numba import jit, autojit,njit
import matplotlib.pyplot as plt 

import math

from MDAnalysis import *

import numpy as np 



#get wrapped coordinates
#and get the nearest image distance
@jit('float32(float32,float32)',nopython=True)
def numbatrunc(a,l):
	a = abs(a)-l*int(abs(a)/l)
	if (a > l/2.0):
		return l - a
	else:
		return a

@jit('f8(f8)',nopython=True)
def CUB(x):
	return x**3.


#loop over all atoms 
#for ever atoms loop over the rest
#get the distance(consider pbc) histogramm it
@jit('void(float32[:,:],float32[:],float32,float32,float32)',nopython=True)
def pairwise_python(X,g,L,smax,db):
	M = X.shape[0]
	N = X.shape[1]
	nbins = int(smax/db)
	for i in range(M-1):
		# print " atom " , i
		for j in range(i+1,M):
			d = 0.0
			for k in range(N):
				tmp = X[i, k] - X[j, k]
				tmp = numbatrunc(tmp,L)
				d += tmp * tmp
			d = np.sqrt(d)
			if (d < smax):
				g[int(d/db)] += 2.0


#normalize the histogramm so the r->inf it -> 1.0
@jit('void(float32[:],float32,float32,int32)',nopython=True)
def normalise(A,L,db,N):
	n = A.shape[0]
	# pairs = float(N)*(float(N)-1.0)/float(2)
	pairs = float(N)*(float(N))
	factor = (4./3.)*np.pi*pairs/CUB(L)
	density = N/CUB(L)
	for i in range(n):
		A[i] /= factor*(CUB(i+1)-CUB(i))*CUB(db)


def plot_all(bins,D,r1,r2,smax):
	plt.axhline(y=1.0, xmin=0.0, xmax=smax, linewidth=1.0, color = 'k')
	plt.plot(bins,D, '-',linewidth=2,color='r',label='calc')
	plt.plot(r1,r2, '--',linewidth=2,color='g',label='vmd')
	plt.legend()
	plt.show()

# u = Universe("train_8atoms.psf","train_8atoms.pdb")
u = Universe("poly.psf","poly.pdb")
a = u.selectAtoms("all")
aa = a.positions
box = u.universe.dimensions[:3]
L = box[0]
smax = 10.0
db = 0.1
nbins = int(smax/db)
D = np.zeros(nbins, dtype=np.float32)

# g = calc_rdf(aa,L)
bins = np.linspace(0,smax,nbins)

#vmd 
vrdf = np.loadtxt('rdf.dat')
r2 = vrdf[:-1,1]
r1 = vrdf[:-1,0]
# denormalise(r2,L,db)


pairwise_python(aa,D,L,smax,db,len(aa))
normalise(D,L,db)
plot_all(bins,D,r1,r2,smax)
