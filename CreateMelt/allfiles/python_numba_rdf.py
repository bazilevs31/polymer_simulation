#!/home/vasiliy/anaconda/bin/python

# Purpose: Calculate radial distribution function  using Python and Numba library
# Author:  Triandafilidi Vasiliy , MSc student at CHBE UBC, Vancouver
# e-mail:  vtriandafilidi(at)chbe(dot)ubc(dot)ca
# Syntax:  python  python_numba_rdf.py
# Requires: poly.psf poly.pdb, numba library 

# Theory:
# http://en.wikipedia.org/wiki/Radial_distribution_function
# 
# 
# Copyright (c) 2014 Vasiliy Triandafilidi
# Released under the GNU Public Licence, v2 or any higher version 

from numba import jit, autojit,njit
import math
from MDAnalysis import *
import numpy as np 
import os
import readparameters
from savenpz import save_arrays,append_arrays
from plotanimation import plotrdf



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




def del_endpsf(x):
    """
    delete npz dimension of the file
    """
    if x[-4:] == '.psf':
        return ''.join(x.split())[:-4]
    else:
        return x


def main():

	u, args = readparameters.read_parameters()
	smax, db, trajskip,startframe, endframe, psffile = args.smax, args.db, args.trajskip,args.startframe, args.endframe, args.psffile
	psffile = del_endpsf(psffile)
	print "psffile = %s" % psffile
	box = u.universe.dimensions[:3]
	L = box[0]
	nbins = int(smax/db)
	bins = np.linspace(0,smax,nbins)
	Resultarray = []	
	append_arrays(Resultarray,bins)

	for ts in u.trajectory[startframe:endframe:trajskip]:		
		print "frame = %d" % ts.frame
		D = np.zeros(nbins, dtype=np.float32)
		a = u.selectAtoms("all")
		aa = a.positions
		pairwise_python(aa, D, L, smax, db)
		normalise(D,L,db,aa.shape[0])
		append_arrays(Resultarray,D)
	save_arrays(Resultarray,'rdf'+psffile)
	plotrdf('rdf'+psffile+'.npz', 'animrdf'+psffile)


if __name__ == '__main__':
	main()