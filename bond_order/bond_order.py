
# Program: bond_order.py
# Purpose: get the P2(cos\theta) parameter using Python
# Author:  Triandafilidi Vasiliy , MSc student at CHBE UBC, Vancouver
# e-mail:  vtriandafilidi(at)chbe(dot)ubc(dot)ca
# Syntax:  python bond_order.py
# Requires: polymer.psf, trajectory.xtc

# Theory:
#Order parameter P2 - is a way of measuring alignment of polymers along certain matrix
# P2 =def= 3/2<cos^2 \theta -1>, where averaging is performed over all atoms
# \theta =def=  angle(z_axis_of alignment, b_i)
# b_i =def= r_i - r_{i-2} - mean arithmetic of two bond vectors
# C1===C2===C3, i.e vec{C3 - C1}
# z_axis_of_alignment vector that corresponds to highest eigenvalue of tensor Qab
# Qab = 3/2 <<b_i**b_i>a - 1/3>f where averaging is performed over all atoms
# In our case we average Qab over last 400 frames where structure is crystalline
# The parameter P2 is : -1/2 < P2 < 1,
#P2 = 1 - perfect alignment, P2 = 0 amorphous, P2 = -1/2 is perpendicular to the z_axis 

# Copyright (c) 2014 Vasiliy Triandafilidi
# Released under the GNU Public Licence, v2 or any higher version 

from MDAnalysis import *
import numpy as np
# from numpy import linalg  as LA
from pylab import *


def get_qab(coor):
    #gets the Qab for all atoms and averages it
    nq = coor.shape[0]
    out = np.zeros((3, 3))
    # print "nq = ", nq
    out = np.zeros((3, 3))
    dij = np.eye(3)

    for i in xrange(0, nq):
        out += np.outer(coor[i], coor[i])

    return 1.5*(out - 0.3*dij) / float(nq)


def get_bond_list(bondlist):
    #gets the universe creates a normalized bonds list
    # Make two atomgroups, each containing one atom from each bond
    ag1 = u.atoms[[b[0] for b in bondlist]]
    ag2 = u.atoms[[b[1] for b in bondlist]]
    vecs = ag1.positions - ag2.positions # so this gives the vectors between bonds as np array
    norm = np.sqrt((vecs*vecs).sum(axis=1)) # normalise to unit vectors
    vecs /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    vecs  = 0.5*(vecs[1:] + vecs[:-1]) # this is the average of every two neigbour bonds
    return vecs


def get_eigen_vector(u):
    #gets the universe and loops over the trajector
    print "getting the eigen_values and eigen_vectors"
    Qab = np.zeros((3, 3))
    count = 0.
    nframes = len(u.trajectory)
    for ts in u.trajectory[nframes - 10:-1]:
        # print "frame is = ", ts.frame
        bondlist = u.bonds
        Qab += get_qab(get_bond_list(bondlist))
        count += 1.
    Qab = Qab/count
    print Qab
    print np.trace(Qab)
    vals, vecs = np.linalg.eig(Qab)
    print vals[0], vecs[:, 0]
    return vecs[:, 0]


def get_p2(coor, principal_vector):
    nq = coor.shape[0]
    p2 = 0.
    pv2 = np.linalg.norm(principal_vector)
    for i in xrange(0, nq):
        v1 = np.linalg.norm(coor[i])
        some = np.dot(coor[i], principal_vector)/(v1*pv2)
        p2 += (3.*some*some - 1.)/2.
    p2 /= float(nq)
    return p2


def get_order_param(u):
    #this function gets the universe
    #uses the get_eigen_vector(universe) to get the eigen_vector
    #then uses the get_bond_list(bondlist) to get the vectorized coor
    #then uses the get_p2(coor, principal_vector) to get the p2
    print "running the get_order_param"
    principal_vector = get_eigen_vector(u)
    print "the principal vector is = ", principal_vector
    Order_array = np.zeros((len(u.trajectory), 2))
    for ts in u.trajectory[1:-1]:
        bondlist = u.bonds
        vecs = get_bond_list(bondlist)
        order = get_p2(vecs, principal_vector)
        # Order_array.append((ts.frame, order))
        Order_array[ts.frame, 0] = ts.frame
        Order_array[ts.frame, 1] = order
        print "frame is = ", ts.frame, "order = ", order
    return Order_array


# u = Universe("shortchain_polymer.psf", "trajectory_shortchain.xtc")
# u = Universe("poly_without_long.psf", "trajectory_shortchain.xtc")
u = Universe("../coor_files/poly.psf", "../coor_files/traj_skip10.dcd")

Order_array = get_order_param(u)

plot(Order_array[:, 0], Order_array[:, 1], 'r--', lw=2, label=r"$P_2 = \dfrac{3 cos^2 \theta - 1}{2}$")
xlabel("time (ps)")
ylabel(r"order parameter $P_2$ ($\AA$)")

savefig('shortchain.pdf')