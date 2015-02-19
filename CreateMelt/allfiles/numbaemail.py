#!/usr/bin/env python

from numba import jit, autojit,njit
import math
import numpy as np 



@jit('float32(float32,float32)',nopython=True)
def numbatrunc(a,l):
	"""
	get wrapped coordinates
	and get the nearest image distance
	"""
	a = abs(a)-l*int(abs(a)/l)
	if (a > l/2.0):
		return l - a
	else:
		return a

@jit('f8(f8)',nopython=True)
def CUB(x):
	return x**3.


@jit('void(float32[:,:],float32[:],float32,float32,float32)',nopython=True)
def pairwise_python(X,g,L,smax,db):
	""" 
	given array of Atom coordinates (Natoms*3) = X, empty array g, size of the box = L, cutoff = smax, size of the bin = db
	histogramm atom coordinates by the bins of size db, normalise the histogramm so in the infinity the function is 1.
	input X - array of atom positions, g(r), L(box), smax(cutoff), db(bins)
	output: none(output is stored in g)  
	
	1.loop over all atoms 
	2.for ever atoms loop over the rest
	3.get the distance(consider pbc) histogramm it
	"""
	M = X.shape[0]
	N = X.shape[1]
	nbins = int(smax/db)
	for i in range(M-1):
		# print " atom " , i
		for j in range(i+1,M):
			d = 0.0
			for k in range(N):
				tmp = X[i, k] - X[j, k]
				tmp = abs(tmp)-L*int(abs(tmp)/L)
				if (tmp > L/2.0):
					tmp = L - tmp
				d += tmp * tmp
			d = np.sqrt(d)
			if (d < smax):
				g[int(d/db)] += 2.0

@jit('void(float32[:],float32,float32,int32)',nopython=True)
def normalise(g,L,db,N):
	"""
	normalize the histogramm so the r->inf it -> 1.0
	input : g(r), L(box), db (bins), N(atoms)
	output : nothing(but g[:] is normalized)
	"""
	n = g.shape[0]
	# pairs = float(N)*(float(N)-1.0)/float(2)
	pairs = float(N)*(float(N))
	factor = (4./3.)*np.pi*pairs/CUB(L)
	density = N/CUB(L)
	for i in range(n):
		g[i] /= factor*(CUB(i+1)-CUB(i))*CUB(db)

L = 15.0
smax = 8.0
db = 0.1
nbins = int(smax/db)
coords = L*np.random.rand(10000,3)
coords = np.asarray(coords,dtype=np.float32)

g = np.zeros(nbins, dtype=np.float32)
pairwise_python(coords, g, L, smax, db)
normalise(g,L,db,coords.shape[0])
