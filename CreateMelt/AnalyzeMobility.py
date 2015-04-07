#!/usr/bin/env python
import numpy as np
from MDAnalysis import *
from read_parameters import read_traj_vmd
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy import linalg as LA
from sklearn.metrics import mean_squared_error
from math import sqrt
from numba import jit

@jit
def calc_rmsd(a,b):
    """calculation of difference using numba"""
    N = a.shape[0]
    K = a.shape[1]
    for i in range(N):
      for k in range(K):
        tmp = a[i,k] - b[i,k]
        diff += tmp*tmp
    diff /= float(N)*float(K)
    diff = np.sqrt(diff)
    return diff

def main():
    args = read_traj_vmd()
    psffile = os.path.splitext(args.psffile)[0]
    u = Universe(psffile+'.psf', 'trajectory_nve.dcd')
    ref_atoms = u.selectAtoms("all")
    traj_atoms = u.selectAtoms("all")
    natoms = traj_atoms.numberOfAtoms()

  # if performing a mass-weighted alignment/rmsd calculation
  #masses = ref_atoms.masses()
  #weight = masses/numpy.mean(masses)



  # reference centre of mass system
    ref_com = ref_atoms.centerOfMass()
    ref_coordinates = ref_atoms.coordinates() - ref_com
  # diff_coordinates = ref_atoms.coordinates().copy

  # allocate the array for selection atom coords
    traj_coordinates = traj_atoms.coordinates().copy()

    for ts in u.trajectory[args.startframe:args.endframe:args.trajskip]:
      # shift coordinates for rotation fitting
      # selection is updated with the time frame
        x_com = traj_atoms.centerOfMass()
        traj_coordinates[:] = traj_atoms.coordinates() - x_com
        diff = calc_rmsd(traj_coordinates,ref_coordinates)
      
      # rms = sqrt(mean_squared_error(traj_coordinates,  ref_coordinates ))
      # diff_coordinates = traj_coordinates - ref_coordinates
      # mean = np.mean(LA.norm(diff_coordinates,axis=0))
      # difference = 
      # print diff_coordinates
      # print "%5d  %8.3f A" % (k, rmsd[k])
        print "frame " , ts.frame, " diff " , diff
      # print "frame " , ts.frame, " diff2 " , rms
if __name__ == '__main__':
  main()