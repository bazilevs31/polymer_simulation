
import numpy as np

from MDAnalysis import *
from subprocess import call, os
import commands


def get_chords_j_around_i(ubond):
	#this functions gets the atomselection 
	# around current chord
	# and returns all the positions of chords
	#for given selection
	C='1'
	t_types={ 'phi_around': (C,C,C), }
	angles = dict((name,ubond.atoms.selectBonds(angle)) for name,angle in t_types.items())
	phis_around=angles['phi_around']
	chords = phis_around.atom3.positions - phis_around.atom1.positions 
	norm = np.linalg.norm(chords,axis=1)
	chords /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
	return chords

def get_averaged_cos(chord, ubond):
	chords = get_chords_j_around_i(ubond)
	return np.average(np.dot(chords, chord))

def initialize():
	# print len(sys.argv)
	# try:
	# 	inconf = sys.argv[1]
	# except IOError:
	#     print('cannot open', arg)
	# except (len(sys.argv)!=3):
	# 	raise NameError('please provide 2 arguments')
	# finally:
	# 	print("Inporting configuration " + str(inconf))

	# try:
	# 	intraj = sys.argv[2]
	# except IOError:
	#     print('cannot open', arg)
	# finally:
	# 	print("Importing trajectory" + str(intraj))
	inconf = commands.getoutput("ls | grep .psf")
	intraj = commands.getoutput("ls | grep .pdb")
	u = Universe (inconf, intraj)

	return u


# def main():
# do everything
#select the cutoff for the neighbour averaging
dist_around = 10.0

u = initialize()
C='1'
t_types={ 'phi': (C,C,C), }
angles = dict((name,u.atoms.selectBonds(angle)) for name,angle in t_types.items())
phis=angles['phi']
index = 0
cos = 0
cos_2i = 0.
for my_chord in phis:
	index += 1
	# ubond = u.selectAtoms("around 0.5 group poly", poly=my_chord)
	# print get_chords_j_around_i(ubond)
	# print "doing  chord ", my_chord 
	a1 = my_chord.atom2.pos
	b = ' '.join(str(n) for n in a1)
	ubond = u.selectAtoms("point " +  b  + " " + str(dist_around))
	# print "number of atoms around  " , len(ubond)
	chord = my_chord.atom3.pos - my_chord.atom1.pos
	chord /= np.linalg.norm(chord)
	# print chord
	# print get_chords_j_around_i(ubond)
	cos = 2*np.average(np.dot(get_chords_j_around_i(ubond),chord))**2 -1

	# cos = get_averaged_cos(chord, ubond)
	if (index%100==0):
		print "doing % " , 100.*float(ind	# try:
	# 	inconf = sys.argv[1]
	# except IOError:
	#     print('cannot open', arg)
	# except (len(sys.argv)!=3):
	# 	raise NameError('please provide 2 arguments')
	# finally:
	# 	print("Inporting configuration " + str(inconf))

	# try:
	# 	intraj = sys.argv[2]
	# except IOError:
	#     print('cannot open', arg)
	# finally:
	# 	print("Importing trajectory" + str(intraj))
ex)/float(len(phis)) , " parameter ", cos
	cos_2i += cos
cos_2i /= index
print cos_2i

#a way to solve it 
#a1=phis.atom1  and the same thing for a2 a3 and then select the smalest one
#but the thing is it doesn't work 
#it shows that they are of the same length
#

#another problem to solve is the different orientations of thhe chains
#i have no idea what to do whatsoever
 



#problem to solve 
# how to select only chords : three atom group of atoms
#any ideas?
#



# if __name__ == '__main__':
# 	main()