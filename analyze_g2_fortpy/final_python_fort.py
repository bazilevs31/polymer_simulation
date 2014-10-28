import numpy as np 
from MDAnalysis import *
import get_arrays_produce_cos_ave_fort  as ft
from MDAnalysis.topology.LAMMPSParser import LAMMPSData


def get_bonds(u):
	#profiling shows this to be the most troubling part
	# angle=('1', '1', '1')
	# angles=u.atoms.selectBonds(angle)
	angles = u.angles
	chords = angles.atom3.positions - angles.atom1.positions 
	coords = angles.atom2.positions
	norm = np.linalg.norm(chords,axis=1)
	chords /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
	return chords,coords



filename='../polymer_300'
d = LAMMPSData(filename+".data")
d.writePSF(filename+".psf")
d.writePDB(filename+".pdb")

g2 = []
time = []

u = Universe(filename+".psf",filename+".pdb")


# for ts in u.trajectory[1:-1]:
for ts in u.trajectory:
	a=u.selectAtoms("all")
	bonds,atoms=get_bonds(a)
	s=0.0
	result =  ft.sparam(natoms=bonds.shape[0],bonds=bonds,atoms=atoms,around=2.0,s=s)
	g2.append(s)
	time.append(ts.frame)
	print result
    # print "frame is = ", ts.frame, "order = ", s