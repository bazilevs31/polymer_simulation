from MDAnalysis import *
import numpy as np
from numpy import linalg as LA
from pylab import *
from MDAnalysis.analysis.distances import distance_array
from MDAnalysis.core.distances import calc_bonds 
import module_load_save as msave 


def main():
	u = initialize()
	R2=0.
	Rgyr=0.
	Rg_array=[]
	R2_array=[]
	ration_array=[]
	# x = np.zeros((len(u.residues),1))
	for ts in u.trajectory:
		R2 = np.sum(np.array([distance_sq_coords(myres.atoms[0].pos,myres.atoms[-1].pos) for myres in u.residues]))
		R2 /= len(u.residues)
		Rgyr = np.sum(np.array([myres.atoms.radiusOfGyration(pbc=False) for myres in u.residues]))
		Rgyr /= len(u.residues)
		Rgyr *= Rgyr
		Rg_array.append((u.trajectory.frame, Rgyr))
		R2_array.append((u.trajectory.frame, R2))
		ration_array.append((u.trajectory.frame, R2/Rgyr))
		# Rgyr.append((u.trajectory.frame, R2**2/Rg**2.))
		print "frame number = ", ts.frame, " Rg2 = ", Rgyr, " R^2 = " , R2
	# print "R2/Rg2 = ", R2/Rgyr
	# print "ratio" , R2/(len(u.residues)*1.54**2.)

	Rg_array=np.array(Rg_array)
	R2_array=np.array(R2_array)
	ration_array=np.array(ration_array)
	np.savez('rgpoly120.array', Rg_array[:,0],Rg_array[:,1])
	# msave.write_file(Rg_array[:,0],Rg_array[:,1], 'gyration_vs_time.dat')
	# msave.plot_file(Rg_array[:,0],Rg_array[:,1], 'gyration_vs_time.dat')
	# msave.write_file(R2_array[:,0],R2_array[:,1], 'endtoend_vs_time.dat')
	# msave.write_file(ration_array[:,0],ration_array[:,1], 'ratio_gyration_endtoend_vs_time.dat')
	# msave.plot_file(ration_array[:,0],ration_array[:,1], 'ratio_gyration_endtoend_vs_time.dat')

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
	finally:
		print("Inporting configuration " + str(inconf))

	try:
		intraj = sys.argv[2]
	except IOError:
	    print('cannot open', arg)
	finally:
		print("Importing trajectory" + str(intraj))
	# conf = commands.getoutput("ls | grep .psf")
	# traj = commands.getoutput("ls | grep .pdb")
	u = Universe (inconf, intraj)
	return u

if __name__ == '__main__':
	main()