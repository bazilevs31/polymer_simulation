#!/home/vasiliy/anaconda/bin/python

import numpy as np
import fortnew as ft  #f2py module for analyzing the traj(it should be in the path)
from MDAnalysis import *
import sys
import os
import subprocess#!/home/vasiliy/anaconda/bin/python

import numpy as np
import fortnew as ft  #f2py module for analyzing the traj(it should be in the path)
from MDAnalysis import *
import matplotlib.pyplot as plt   # side-stepping mpl's backend
import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import subprocess

# subprocess.call(['./test.sh'])

def read_parameters():
	"""
	read parameters from the commandline
	input 
	output u, trajskip, endframe
	"""
	parser = ArgumentParser(description=__doc__,
	                        formatter_class=ArgumentDefaultsHelpFormatter)
	parser.add_argument("-f", "--psf", dest="psffile", help="Write psffile to file, no .psf required", metavar="FILE")
	parser.add_argument("-s", 
					"--trajskip",
                    dest="trajskip", 
                    default=20, 
                    type=int, 
                    help="Skip of the trajectory file")
	parser.add_argument("-e", 
					"--endframe",
                    dest="endframe", 
                    default=-1, 
                    type=int, 
                    help="End file of the trajectory file")
	parser.add_argument("-d", "--data", dest="datafile", default="polymer_0.8.data",
	                    type=lambda x: is_valid_file(parser, x),
	                    help="write report to FILE", metavar="FILE")
	parser.add_argument("-t", "--trajectory", dest="dcdinput", default="trajectory_nve.dcd",
	                    type=lambda x: is_valid_file(parser, x),
	                    help="write report to FILE", metavar="FILE")
	args = parser.parse_args()
	psffile = args.psffile
	trajskip = args.trajskip
	endframe = args.endframe
	datafile = args.datafile
	dcdinput = args.dcdinput
	psfpath = os.path.abspath(psffile+'.psf')
	if os.path.exists(psfpath)==True:
		u = Universe(psffile +".psf","trajSkipwrap.dcd")
		return u, trajskip, endframe , psffile		
	elif os.path.exists(psfpath)==False:
		create_psf(datafile, dcdinput, trajskip,psffile+".psf")
		u = Universe(psffile +".psf","trajSkipwrap.dcd")
		return u, trajskip, endframe, psffile
def is_valid_file(parser, arg):
	"""
	Check if arg is a valid file 
	"""
	arg = os.path.abspath(arg)
	if not os.path.exists(arg):
		parser.error("The file %s doesn't exist " % arg)
	else:
		return arg

def create_psf(datafile,dcdinput,trajskip,psffile):
	"""given data file produce psf file, read-eidt dcd file"""
	curdir = os.getcwd()
	curdir = curdir+"/"
	filestring = " ".join(("create_list_cryst.sh",datafile,dcdinput,str(trajskip),psffile,curdir))
	print filestring
	os.system(filestring)
	return 0

def main():
	"""main program input : psffile(no dimension), datafile(with dimension), dcdfile(with dimension), dcdskip(integer)"""
	u, trajskip, endframe, psffile = read_parameters()
	time = []
	g2 = []

	for ts in u.trajectory[1:endframe:trajskip]:
		R2=0.
		Rgyr=0.
		Rgyr = np.sum(np.array([myres.atoms.radiusOfGyration(pbc=False) for myres in u.residues]))
		Rgyr /= len(u.residues)
		time.append(ts.frame)
		g2.append(Rgyr)
		print ts.frame , "  ", Rgyr
	       
	g2 = np.array(g2)
	time = np.array(time)
	np.savez("gyr"+psffile,time=time,g2=g2)

if __name__ == '__main__':
	main()


# print(os.getcwd()+"/" + "\n")
# to get the current directory
#
#npz=np.load('../coords.txt.npz')
#atoms=npz['atoms']
#bonds=npz['bonds']
