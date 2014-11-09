from MDAnalysis import *
import numpy as np
from numpy import linalg as LA
from pylab import *
from MDAnalysis.analysis.distances import distance_array
from MDAnalysis.core.distances import calc_bonds 

name = "poly"
conf = name + ".psf"
traj = name + ".pdb"
skip = 0 # skip frames

def main():
	u = Universe(conf, traj)
	R2=0.
	Rgyr=0.
	# x = np.zeros((len(u.residues),1))
	for ts in u.trajectory:
		R2 = np.sum(np.array([distance_sq_coords(myres.atoms[0].pos,myres.atoms[-1].pos) for myres in u.residues]))
		R2 /= len(u.residues)
		Rgyr += np.sum(np.array([np.square(myres.atoms.radiusOfGyration(pbc=False)) for myres in u.residues]))
		Rgyr /= len(u.residues)
		# Rgyr.append((u.trajectory.frame, R2**2/Rg**2.))
		print "frame number = ", ts.frame, " Rg2 = ", Rgyr, " R^2 = " , R2
	print "R2/Rg2 = ", R2/Rgyr
	print "ratio" , R2/(len(u.residues)*1.54**2.) 


def distance_sq_coords(coord1, coord2):
	diff = np.array(coord1)-np.array(coord2)
	x = np.dot(diff, diff)
	return x

if __name__ == '__main__':
	main()