from MDAnalysis import *
import numpy as np
from pylab import *


def main():
	u,foldername = initialize()
	R2=0.
	Rgyr=0.
	R2 = np.sum(np.array([distance_sq_coords(myres.atoms[0].pos,myres.atoms[-1].pos) for myres in u.residues]))
	R2 /= len(u.residues)
	Rgyr = np.sum(np.array([myres.atoms.radiusOfGyration(pbc=False) for myres in u.residues]))
	Rgyr /= len(u.residues)
	Rgyr *= Rgyr
	print "folder ", foldername, " ratio " , R2/Rgyr

def distance_sq_coords(coord1, coord2):
	diff = np.array(coord1)-np.array(coord2)
	x = np.dot(diff, diff)
	return x

def initialize():
	# print len(sys.argv)
	try:
		inconf = sys.argv[1]
	except IOError:
	    print('cannot open', arg)
	except (len(sys.argv)!=3):
		raise NameError('please provide 2 arguments')

	try:
		intraj = sys.argv[2]
	except IOError:
	    print('cannot open', arg)
	try:
		foldername = sys.argv[3]
	except IOError:
	    print('cannot open', arg)
	u = Universe (inconf, intraj)
	return u,foldername

if __name__ == '__main__':
	main()