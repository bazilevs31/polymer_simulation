from numba import jit,autojit
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


# @jit('void(float32[:,:],float32[:,:],float32[:,:])',nopython=True)
# def numba_get_qab(coor,out,dij):
#     #gets the Qab for all atoms and averages it
#     nq = coor.shape[0]

#     for i in xrange(0, nq):
#         out += np.outer(coor[i], coor[i])

#     out = 1.5*(out - 0.3*dij) / float(nq)

coords = np.random.rand(1000,3)
A = coords

out = np.zeros((3,3))
dij = np.eye(3)

out1 = np.einsum('ij,ik->jk', A, A)
out1 = 1.5*(out1 - 0.3*dij)
out2 = get_qab(A)
# get_qab(coords)

