#!/home/vasiliy/anaconda/bin/python

import numpy as np
from MDAnalysis import *
import matplotlib.pyplot as plt   # side-stepping mpl's backend
import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import subprocess
import matplotlib.animation as animation


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
                    default=10, 
                    type=int, 
                    help="Skip of the trajectory file, together with the vmd skip it will be trajskip*4")
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
    print " I am here "
    psfpath = os.path.abspath(psffile+'.psf')
    if os.path.exists(psfpath)==True:
        u = Universe(psffile +".psf","trajectory_nve.dcd")
        return u, trajskip, endframe , psffile      
    elif os.path.exists(psfpath)==False:
        create_psf(datafile, dcdinput, trajskip,psffile+".psf")
        u = Universe(psffile +".psf","trajectory_nve.dcd")
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
    filestring = " ".join(("create_list_cryst.sh",datafile,dcdinput,str(5),psffile,curdir)) # here str(trajskip) = str(5)
    os.system(filestring)
    return 0




# u = Universe("../data/poly_40.psf","../data/traj_40.dcd")
# w = Writer("../data/traj_40_b.dcd", u.trajectory.numatoms)

u, trajskip, endframe, psffile = read_parameters()


maxlen=len(u.residues[0])
for res in u.residues:
	# print "I am here reslen %d" % len(res)
	if len(res)>maxlen:
		maxlen=len(res)
		# print "I am here"
print maxlen
u.atoms.set_name("C")

for ts in u.trajectory[1:-1:100]:
	print "frame %d" % ts.frame
	for res in u.residues:
		res.set_bfactor(len(res)/float(maxlen))
		# res.set_bfactor(len(res))
	# print res.bfactors.sum()
# print u.atoms.bfactors
		# res.set_bfactor(1.0)
		# print res.bfactors
allatoms=u.selectAtoms("all")
allatoms.set_bfactor(u.atoms.bfactors)
allatoms.write('poly60.pdb')
# u.atoms.set_bfactor(1.0)
# u.atoms.write("system.pdb")
# u1 = Universe(psffile+".psf","system.pdb")
# print u1.atoms.bfactors


# w = Writer(psffile+"b.dcd", u.trajectory.numatoms)
# for ts in u.trajectory[1:-1:100]:
#     w.write(ts)
# w.close_trajectory()
u1 = Universe(psffile+".psf","poly60.pdb")
print u1.atoms.bfactors


