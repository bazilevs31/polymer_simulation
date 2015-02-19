#!/usr/bin/env python

import numpy as np
try:
    import fortrnew as ft
except ImportError:
    import fortranoffice as ft

from MDAnalysis import *
import matplotlib.pyplot as plt   # side-stepping mpl's backend
import os
import readparameters

#Trajectory analysis
# 1) analyze g2 alignment parameter 
# 2) analyze gyr parameter
# 3) analyze R2 end to end distance
# 4) analyze R2/gyr^2 parameter
# plot and store all variables to the figures folder
# 


# subprocess.call(['./test.sh'])

def get_bonds(u):
    """given universe return chords of the (i+1-i-1) bonds and coords of central i atoms"""
    angles = u.angles
    chords = angles.atom3.positions - angles.atom1.positions 
    coords = angles.atom2.positions
    norm = np.linalg.norm(chords,axis=1)
    chords /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    return chords,coords
def distance_sq_coords(coord1, coord2):
    diff = np.array(coord1)-np.array(coord2)
    x = np.dot(diff, diff)
    return x
class traj(object):
    """docstring for traj"""
    def __init__(self,time, g2, gyr, gr2, psffile):
        self.time = time
        self.g2 = g2
        self.gyr = gyr
        self.gr2 = gr2
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
        self.curdir = curdi
r        self.figuresdir = figuresdir        
    def plot_rdf(self):
        self.get_currdir()
        # plt.axhline(y=-0.2, xmin=0.0, xmax=self.time.max(), 'g--', linewidth=0.5)
        plt.xlabel(r'$\mathrm{time}$')
        plt.ylabel(r'$\mathrm{g2}$')
        plt.grid(True)
        plt.title(r'$\mathrm{Crystallinity} } $'  )
        plt.plot(self.time, self.g2, 'bo-', label='$g_2$',lw=1.5)
        plt.legend()
        plt.savefig(self.figuresdir + '/g2' + self.psffile + '.pdf')
        np.savez(self.figuresdir + '/g2' + self.psffile, self.time, self.g2)
        np.savez(self.figuresdir + '/gyr' + self.psffile, self.time, self.gyr)
        np.savez(self.figuresdir + '/gr2' + self.psffile, self.time, self.gr2)
        plt.ylabel(r'$\mathrm{R_g/R^2}$')
        plt.title(r'$\mathrm{R_g/R^2} } $'  )
        plt.legend()
        plt.plot(self.time, self.gr2/self.gyr, 'go-', label='$R^2$',lw=1.5)
        plt.savefig(self.figuresdir + '/ratio' + self.psffile + '.pdf')


def main():
    """main program input : psffile(no dimension), datafile(with dimension), dcdfile(with dimension), dcdskip(integer)"""
    u,args = readparameters.read_parameters()
    trajskip, endframe,psffile = args.trajskip, args.endframe, args.psffile
    time, g2, gyr, gr2 = [], [], [], []
    Rgyr, R2 = 0.0, 0.0


    for ts in u.trajectory[1:endframe:trajskip]:
        a=u.selectAtoms("all")
        bonds, atoms = get_bonds(a)
        N=bonds.shape[0]
        s=0.0
        result =  ft.sparam(natoms=N,bonds=bonds,atoms=atoms,around=2.0,s=s)
        print "frame is " , ts.frame, " order = ", result 
        time.append(ts.frame)
        g2.append(result)
        
        # Rgyr = np.sum(np.array([myres.atoms.radiusOfGyration(pbc=True) for myres in u.residues]))
        # Rgyr /= len(u.residues)
        # gyr.append(Rgyr*Rgyr)

        # R2 = np.sum(np.array([distance_sq_coords(myres.atoms[0].pos,myres.atoms[-1].pos) for myres in u.residues]))
        # R2 /= len(u.residues)
        # gr2.append(R2)

           
    g2 = np.array(g2); gr2 = np.array(gr2); gyr = np.array(gyr); time = np.array(time)
    mytraj = traj(time, g2, gyr, gr2, psffile)
    mytraj.plot_rdf()


if __name__ == '__main__':
    main()


# print(os.getcwd()+"/" + "\n")
# to get the current directory
#
#npz=np.load('../coords.txt.npz')
#atoms=npz['atoms']
#bonds=npz['bonds']
