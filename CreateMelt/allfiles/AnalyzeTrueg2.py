#!/usr/bin/env python
from __future__ import print_function
import numpy as np
# from numba import jit,autojit,njit
# from numbapro import jit,njit
from parakeet import jit as par_jit
from numbapro import double, long_, int_, jit, autojit
from MDAnalysis import *
# import matplotlib.pyplot as plt   # side-stepping mpl's backend
# import os
import readparameters
# import objgraph

def get_angles(u):
    """
    given universe return chords of the (i+1-i-1) atoms(central ith atom) and angles
    input: universe
    output: atoms(coordinates), angles(angle_values)
    """
    angles = u.angles
    angle_values = angles.angles()
    atoms = angles.atom2.positions
    # atoms = np.ascontiguousarray(atoms, dtype=np.float32), 
    # angle_values = np.ascontiguousarray(angle_values, dtype=np.float32)
    atoms = np.asarray(atoms,dtype=np.float32)
    angle_values = np.asarray(angle_values,dtype=np.float32)
    return atoms, angle_values

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


# Nangles = angles.shape[0]
# assert Natoms==Nangles, " number of atoms %d should equal nuber of anngles %d " % (Natoms,Nangles)

# @jit('float32(float32[:,:],float32[:])',nopython=True, locals={'i':long_,'j':long_,'cos2':double,'d':double,'tmp':double, 'dPhi':double, 'dist_around':double,'n':long_, 'Natoms':long_, 'M':long_, 'k':long_})
@jit('float32(float32[:,::1],float32[:],float32)',nopython=True)
def Calcg2(atoms, angles,L):
    """
    calculate g2 parameter
    input: atoms Natoms*3 array, angles Natoms*1 array of angles
    here Natoms is not number of atoms in the system, is number of angle vertices
    """
    # d local distance parameter , tmp needed to calculate d
    # dPhi - local angle difference, dist_around = cutoff
    # cos2 - local g2 parameter , n - counter of neighbours
    # g2 - the result of our program 
    Natoms = atoms.shape[0]
    M = atoms.shape[1]
    cos2 = 0.0; g2 = 0.0; d = 0.0; tmp = 0.0; dPhi = 0.0;dist_around = 8.0 ; n = 0
    for i in range(Natoms):
        n = 0
        cos2 = 0.0
        for j in range(Natoms):
            if i!=j:
                d = 0.0
                tmp = 0.0
                for k in range(M):
                    tmp = atoms[i,k] - atoms[j,k]
                    tmp = numbatrunc(tmp,L)
                    d += tmp*tmp
                d = np.sqrt(d)
                if d<dist_around:
                    dPhi = 2.0*(angles[i]-angles[j])
                    cos2 += np.cos(dPhi)
                    n += 1 #number of neighbours
        g2 += cos2/float(n)
        # print cos2/float(n)
    g2 /= Natoms
    return g2

def main():
    u, args, psffile = readparameters.read_parameters()
    trajskip = args.trajskip
    box = u.universe.dimensions[:3]
    L = box[0]
    print (L)
    for ts in u.trajectory[1:-1:trajskip]:
        atoms,angles = get_angles(u)
        g2 = 0.0
        # print (atoms,angles)
        g2 = Calcg2(atoms,angles,L)
        print ("frame %d , g2 = %f" %(ts.frame, g2))
        # objgraph.show_refs([atoms], filename='atoms-graph.png')
        # objgraph.show_refs([angles], filename='angles-graph.png')




if __name__ == '__main__':
    main()