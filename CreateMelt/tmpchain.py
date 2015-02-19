import numpy as np
from MDAnalysis import *
# check how does it work?


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

def moving_average(a, n=3) :
    ret = np.cumsum(a, axis=0, dtype=float)
    ret[n:,:] = ret[n:,:] - ret[:-n,:]
    return ret[n - 1:,:] / n

def get_cos2(bonds,Nneigh=3):
    """

    gets chords of a chain
    then loops from within 2:-2 of an array
    calculates get_cos2_local
    averages it 

    todo: modify so it can understand variable number of neighbours
    make it faster (numba)

    """
    nleft = int(Nneigh)/2
    nright = Nneigh - nleft
    cos2 = 0.
    k = 0.0
    cos2_local = 0.
    Nbonds = len(bonds)
    AlignVec = moving_average(bonds,Nneigh)
    for i in range(nleft,Nbonds-nright):
        cos2_local = np.dot(AlignVec[i-2,:],bonds[i,:])
        cos2_local = 2.0*cos2_local**2-1.0
        cos2 += cos2_local
        k += 1
    cos2 /= k
    return cos2

u = Universe('../data/poly_40.psf', '../data/traj_40.dcd')
Nres = len(u.residues)

for ts in u.trajectory[1:-1:2]:
    # print u.atoms
    all_g2 = 0.
    for res in u.residues:
        chords = get_bondlist_coords(res)
        all_g2 += get_cos2(chords,4)
    print all_g2 / Nres

    # print get_cos2(chords)

