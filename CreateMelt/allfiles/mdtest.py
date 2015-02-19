#!/home/vasiliy/anaconda/bin/python

import numpy as np
import fortnew as ft  #f2py module for analyzing the traj(it should be in the path)
from MDAnalysis import *
from numba import jit
import matplotlib.pyplot as plt   # side-stepping mpl's backend
import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import subprocess


u = Universe("../data/poly_40.psf", "../data/wraptraj_40.dcd")
atoms = u.atoms
i=10
Natoms = len(u.atoms)
cutoff = 2.0

def get_bondlist_coords(u):
    """
    use universe of a domain
    generate normalized coordinates of bond vectors
    get universe , return bonds(coordinates)
    generate coor of all bonds(bond = chord i-1 - i+1 ), normalize it
    """
    angles = u.angles
    bonds = angles.atom3.positions - angles.atom1.positions 
    # coords = angles.atom2.positions
    norm = np.linalg.norm(bonds,axis=1)
    bonds /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    return bonds

@jit('float32(float32[:,:],float32[:])',nopython=True)
def calc_g2(B,b):
	"""
	get atoms_around_bonds, atom_bond
	produce for every bond in the atoms_around_bonds calcualte dot produce with the atom_bond
	"""
	N = B.shape[0]
	K = B.shape[1]
	# assert K==b.shape[1], "the shapes don't much k=%d, K=%d" %(b.shape,K)
	cos2=0.0
	for i in range(N):
		tmp=0.0
		for k in range(K):
			tmp+=B[i,k]*b[k]
			# assert hasattr(tmp, "__len__")==False , "tmp isn't a scalar "
		# tmp = np.dot(B[i,:], b[:])
		# assert tmp<=1.0 , "tmp = %f" % tmp
		cos2+=tmp
	cos2 /= float(N)
	return cos2

g2 = 0
for i in xrange(1,Natoms):
	atom = u.selectAtoms("bynum %d" % i)
	b = atom.bonds
	b1 = b.atom1.positions
	b2 = b.atom2.positions
	atom_bond = (b1[0,:] - b2[-1,:])
	norm1 = np.linalg.norm(atom_bond)
	assert norm1>0.0 , "norm1 = %f" % norm1
	atom_bond /= norm1
	atoms_around = u.selectAtoms("around %f (bynum %d)" % (cutoff,i))
	atoms_around_bonds = get_bondlist_coords(atoms_around)
	g2 += calc_g2(atoms_around_bonds,atom_bond)
	# print "atom is %d and order is %f" % (i,g2)
	print "atom is %d" % (i)

print g2/Natoms