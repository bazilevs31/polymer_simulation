#!/home/vasiliy/anaconda/bin/python

import numpy as np
from MDAnalysis import *
import os
import matplotlib.pyplot as plt
from readparameters import read_traj
from numba import jit
# get the max length
# generate an array with 3 columns
# first column = n
# second column = sum of R2(n)
# third column = total number of segements of chains with n 
# 
# i.e if we have 100 polymers of the legth 100 then  thrid column, last element: there will be 100 (of n=100/2)
# if there are 50 of the length 100 and 50 of the length 50, then thrid column, last element will be 50  (of n=100/2)


# parser = argparse.ArgumentParser(description=__doc__,
#                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    

# simple_parser.add_argument("-d", "--data", dest="datafile", 
#                     default="./figures/lammps.data",
#                     type=lambda x: is_valid_file(parser, x),
#                     help="read datafile type ")
# simple_parser.add_argument("-s", 
#                 "--trajskip",
#                 dest="trajskip", 
#                 default=100, 
#                 type=int, 
#                 help="How many steps are to be skipped when trajectory \
#                                     file is being red\
#                                     (needs to be > 1, < number of frames) )")


# @jit
def max_chain(u):
    """ 
    input: MDAnalysis universe 
    output: maximum length of all of the chains present(integer)
    """
    maxlen=0
    for res in u.residues:
        reslen=len(res)
        print reslen
        if maxlen<reslen:
            maxlen=reslen
    print maxlen
    return  maxlen



def get_r2n(u):
    """
    input: MDAnalysis universe
    output: R2 - an array of N*2  (n R2(n)) 
    algorithm: 
    generate an array of N*3
    n  \Sigma R_i(n) \Sigma i 
    |   |               |
    then get an average by dividing Col2 / Col3
    This way it can handle polydisperse systems
    """ 
    chainlen=0
    maxlen = max_chain(u)
    # R = np.empty((maxlen/2,2))      # intermediate array which will be reduced after the calculation
    # R2 = np.empty((maxlen/2,2))     # final array 
    # for res in u.residues:
    #     chainlen = len(res)/2
    #     for i in range(chainlen):
    #         ag1, ag2 = res.atoms[i].pos, res.atoms[-i-1].pos
    #         # print ag1,ag2
    #         R[i,0] += np.linalg.norm(ag1-ag2)
    #         # print i, R[i,0]
    #         R[i,1] += 1
    # R2[::-1,0] = 2*np.arange(maxlen/2)+np.ones(maxlen/2)
    # R2[:,1] = R[:,0]/R[:,1]
    # # print R2
    # # R2[:,1] /= R2[:,0]
    # plt.plot(R2[:,0],R2[:,1])
    # plt.show()
    # return R2

def main():
    """
    main program input : psffile(no dimension), datafile(with dimension), dcdfile(with dimension), dcdskip(integer)
    """
    # s = []
    # time = []
    # u = Universe('poly_40.psf','traj_40.dcd')
    # u = Universe('./figures/lammps.data','trajectory_nve.dcd')
    u, args, psffile = read_traj()
    R2 = get_r2n(u)
    # print R2


if __name__ == '__main__':
    main()
