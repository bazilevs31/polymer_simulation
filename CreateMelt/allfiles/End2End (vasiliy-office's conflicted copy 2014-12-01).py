#!/home/vasiliy/anaconda/bin/python

import numpy as np
from MDAnalysis import *
import matplotlib.pyplot as plt   # side-stepping mpl's backend
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

# u=Universe("poly300.psf", "poly300.pdb")
# u=Universe("../data/poly_40.psf", "../data/wraptraj_40.dcd")


class traj(object):
    """docstring for traj"""
    def __init__(self,time, s, psffile):
        self.time = time
        self.s = s
        self.psffile = psffile
    def get_currdir(self):
        """
        get current directory if it exists
        if not make one and return it
        """
        print ("current directory is")
        print(os.getcwd() + "\n")
        curdir = os.getcwd()
        figuresdir = curdir+'/figures'
        if not os.path.exists(figuresdir):
            os.mkdir(figuresdir)
        self.curdir = curdir
        self.figuresdir = figuresdir        
    def plot_rdf(self):
        self.get_currdir()
        # plt.axhline(y=-0.2, xmin=0.0, xmax=self.time.max(), 'g--', linewidth=0.5)
        plt.xlabel(r'$\mathrm{time}$')
        plt.ylabel(r'$\mathrm{s}$')
        plt.grid(True)
        plt.title(r'$\mathrm{Crystallinity} } $'  )
        plt.plot(self.time, self.s, 'bo-', label='$s$',lw=1.5)
        plt.legend()
        plt.savefig(self.figuresdir + '/s' + self.psffile + '.pdf')
        np.savez(self.figuresdir + '/s' + self.psffile, self.time, self.s)
def read_parameters():
    """
    read parameters from the commandline
    input 
    output u, trajskip, endframe, psffile, Nsub, sthreshold
    """
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--psf", dest="psffile", help="Write psffile to file, no .psf required", metavar="FILE")
    parser.add_argument("-d", "--data", dest="datafile", default="polymer_0.8.data",
            type=lambda x: is_valid_file(parser, x),
            help="read datafile", metavar="FILE")
    args = parser.parse_args()
    psffile = args.psffile
    datafile = args.datafile

    psfpath = os.path.abspath(psffile+'.psf')
    if os.path.exists(psfpath)==True:
        u = Universe(psffile +".psf",psffile +".pdb")
        return u, psffile      
    elif os.path.exists(psfpath)==False:
        create_psf(datafile,psffile)
        u = Universe(psffile +".psf",psffile +".pdb")
        return u, psffile
def is_valid_file(parser, arg):
    """
    Check if arg is a valid file 
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s doesn't exist " % arg)
    else:
        return arg
def create_psf(datafile,psffile):
    """given data file produce psf file, read-eidt dcd file"""
    curdir = os.getcwd()
    curdir = curdir+"/"
    filestring = " ".join(("create_pdb.sh",datafile,psffile,curdir))
    os.system(filestring)
    return 0

def get_r2n(u,psffile):
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
            distance_array = ag1-ag2
            distance_array.shape
            #average it
            r2_loc = np.mean(distance_array*distance_array)
            #divide <R(n)**2> by the n
            R[0,n] = r2_loc/R[1,n]
            print "n = ", n , " n* " , npair , " the n ", R[1,n] ," r2 = ", R[0,n], " r2_loc = ", r2_loc
        plt.plot(R[1,:], R[0,:], 'r--', lw=2)
        plt.xlabel("n")
        plt.ylabel(r" <R^2>/n")
        plt.savefig(psffile + '.pdf')


def main():
    """
    main program input : psffile(no dimension), datafile(with dimension), dcdfile(with dimension), dcdskip(integer)
    """
    s = []
    time = []
    u, psffile = read_parameters()
    get_r2n(u,psffile)



if __name__ == '__main__':
    main()
