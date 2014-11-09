from MDAnalysis import *
import numpy as np
from numpy import linalg as LA
from pylab import *
from MDAnalysis.analysis.distances import distance_array
from MDAnalysis.core.distances import calc_bonds 


# algorithm :
# loop over trajectory
# 	loop over atom indices 0,1,2,3 .. until half of the chain
# 		get the parameter Clast - Cfirst for all chains
# 		average over all chains(residues)
# 		(this is done)
#Author : Vasiliy Triandafilidi
name = "poly"
conf = name + ".psf"
traj = name + ".pdb"
skip = 0 # skip frames


def main():
	u = Universe(conf,traj)	
	nmol = len(list(u.residues))
	Nlen = len(u.residues[0].atoms)
	Nhalf = Nlen/2
	R = np.zeros((2,Nhalf))

	for ts in u.trajectory:
		print " frame ", ts.frame
		for n in xrange(0,Nhalf):
			npair = Nlen - n -1

			R[1,n] = npair - n

			#get the pairs of atoms with indices n-npair for all residues 
			ag1 = [myres.atoms[n].pos for myres in u.residues]
			ag1 = np.array(ag1)
			ag2 = [myres.atoms[npair].pos for myres in u.residues]
			ag2 = np.array(ag2)
			#calculate distance
			distance_array = calc_bonds(ag1,ag2)
			#average it
			r2_loc = np.mean(distance_array*distance_array)
			#divide <R(n)**2> by the n
			R[0,n] = r2_loc/R[1,n]
			print "n = ", n , " n* " , npair , " the n ", R[1,n] ," r2 = ", R[0,n], " r2_loc = ", r2_loc
		plot(R[1,:], R[0,:], 'r--', lw=2)
		xlabel("n")
		ylabel(r" <R^2>/n")
		plt.savefig(name + '.pdf')

if __name__ == '__main__':
	main()
