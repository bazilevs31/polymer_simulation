import numpy as np
from MDAnalysis import *
from MDAnalysis.core.distances import * ##distance_array
from MDAnalysis.core import flags #flags



def get_qab(coor):
# """gets uses coor of all bonds generated by get_bondlist_coords 
# returns qab tensor averaged for all atoms in the current frame"""
    nq = coor.shape[0]
    # print "nq = ", nq
    out = np.empty((3, 3),dtype='float32')
    dij = np.eye(3,dtype='float32')
    out = np.einsum('ij,ik->jk', coor, coor)
    return 1.5*out / float(nq) - 0.5*dij


def get_bondlist_coords(u):
# """get universe , return bonds(coordinates)
# 
# generate coor of all bonds(bond = chord i-1 - i+1 ), normalize it"""
    angles = u.angles
    bonds = angles.atom3.positions - angles.atom1.positions 
    # coords = angles.atom2.positions
    norm = np.linalg.norm(bonds,axis=1)
    bonds /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    return bonds


# coords = np.random.rand(1000,3)
# Natoms = coords.shape[0]
u=Universe("../data/poly_40.psf", "../data/traj_40.dcd")
u.trajectory[-1]
Nsub = 8
atoms_tot = 0
l = u.trajectory.ts.dimensions[1]
grid=np.linspace(0.0,l,Nsub+1,endpoint=True)
delta = grid[1] - grid[0]


for z in grid[:-1]:
    cut_z = u.selectAtoms("prop  z >= " + str(z) + "  and  prop z < " + str(z+delta) )
    for y in grid[:-1]:
        cut_y = cut_z.selectAtoms("prop  y >= " + str(y) + "  and  prop y < " + str(y+delta) )
        for x in grid[:-1]:
            cut_x = cut_y.selectAtoms("prop  x >= " + str(x) + "  and  prop x < " + str(x+delta) )
            # atoms_here = len(cut_x.atoms)
            # print "here atoms " , atoms_here
            # atoms_tot += atoms_here
            qab=get_qab(get_bondlist_coords(cut_x))
            s=np.sqrt(1.5*np.trace(qab*qab))
            cut_x.set_bfactor(s)
            # atomselection.append(cut_x)











# def get_outer_numba(arra):
#   return outer product of a 3d array

# out += np.outer(coor[i], coor[i])




# for i in range(N):
#   ix, iy, iz = int(coords[i,0]/deltax),int(coords[i,1]/deltaz),int(coords[i,2]/deltaz)
#   bcell[ix,iy,iz,0] += get_bfactor_numba(bonds[i])
#   bcell[ix,iy,iz,1] += 1.0

# bcell[:,:,:,0] /= bcell[:,:,:,1]

