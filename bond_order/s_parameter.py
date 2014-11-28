
from itertools import izip

import numpy as np
from MDAnalysis import *
from MDAnalysis.core.distances import * ##distance_array
from MDAnalysis.core import flags #flags

# u=Universe("poly300.psf", "poly300.pdb")
u=Universe("new.psf", "new.pdb")

flags['use_periodic_selections'] = True
flags['use_KDTree_routines'] = False


def get_qab(coor):
    #gets the Qab for all atoms and averages it
    nq = coor.shape[0]
    out = np.zeros((3, 3))
    # print "nq = ", nq
    out = np.zeros((3, 3))
    dij = np.eye(3)

    for i in xrange(0, nq):
        some = np.outer(coor[i], coor[i])
        out += some
        # print some-3.trace()
    out /= float(nq)
    return (out - dij/3.) 


def get_bond_list(my_u):
    #gets the universe creates a normalized bonds list
    # Make two atomgroups, each containing one atom from each bond
    bonds=my_u.selectBonds(('1','1'),)
    bondlist=bonds.bondlist
    at1 = [b.atom1 for b in bondlist]
    at2 = [b.atom2 for b in bondlist]
    ag1 = np.array([a.position for a in at1])
    ag2 = np.array([a.position for a in at2])
    # print ag1
    # print ag2
    # vecs = ag1.position - ag2.position # so this gives the vectors between bonds as np array
    vecs = ag1 - ag2 # so this gives the vectors between bonds as np array
    # norm = np.sqrt((vecs*vecs).sum(axis=1)) # normalise to unit vectors
    norm = np.linalg.norm(vecs,axis=1)
    vecs /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    # vecs  = 0.5*(vecs[1:] + vecs[:-1]) # this is the average of every two neigbour bonds
    return vecs




box = u.trajectory.ts.dimensions[:-3]

length_z = box[-1]
length_y = box[-2]
length_x = box[-3]
Nsub=7

arr_x=np.linspace(0.0,length_x,Nsub+1,endpoint=True)
arr_y=np.linspace(0.0,length_y,Nsub+1,endpoint=True)
arr_z=np.linspace(0.0,length_z,Nsub+1,endpoint=True)
delta_x=arr_x[1]-arr_x[0]
delta_y=arr_y[1]-arr_y[0]
delta_z=arr_z[1]-arr_z[0]
# dots_x=arr_x[1:-1]
# dots_y=arr_y[1:-1]
# dots_z=arr_z[1:-1]
dots_x=arr_x
dots_y=arr_y
dots_z=arr_z

atomselection=[]

count=0

# def get_selection(my_u):
# 	C='1'
# 	t_types={ 'phi': (C,C,C), }
# 	angles = dict((name,my_u.atoms.selectBonds(angle)) for name,angle in t_types.items())
# 	phis=angles['phi']
# 	return phis


for z in dots_z[0:-1]:
	ar_z = u.selectAtoms("prop  z >= " + str(z) + "  and  prop z < " + str(z+delta_z) )
	#ar_z is a planar selection
	# print "prop  z >= " + str(z) + "  and  prop z <= " + str(z+delta_z)
	print " z = ", z
	for y in dots_y[0:-1]:
		#ater this step ar_y is a line
		ar_y = ar_z.selectAtoms("prop  y >= " + str(y) + "  and  prop y < " + str(y+delta_y) )
		# print " y = ", y
		for x in dots_x[0:-1]:
			#ater this step ar_x is a dot
			print "i am here", count
			ar_x = ar_y.selectAtoms("prop  x >= " + str(x) + "  and  prop x < " + str(x+delta_x) )
			print ar_x.atoms
			coor=(get_bond_list(ar_x))
			qab=get_qab(coor)
			s=np.sqrt(1.5*np.trace(qab*qab))
			ar_x.set_bfactor(s)
			atomselection.append(ar_x)
			count+=1
			# print count
			# print " x = ", x

#get indices of atoms and then assign the bffactor just for the index of the atom
#in this case there is no need to assemble the parts into one big atomselection res
# to do that just get the indices of atoms in ar_x
# then just loop for atoms in u and assign bfactor of this atoms


# at5=atomselection[5]
# at5.set_bfactor(0.5)


res=atomselection[0]
# print res.selectBonds(('1','1'),)
# res+=[i for i in atomselection[1:]]

for i in xrange(1,len(atomselection)):
    # print atomselection[i]
    res+=atomselection[i]
allatoms=u.selectAtoms("all")
allatoms.write('poly60.pdb')
# allatom = u.sele

