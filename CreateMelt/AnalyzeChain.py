#!/usr/bin/env python
import numpy as np
from MDAnalysis import *
from read_parameters import read_traj_vmd
import os
import matplotlib.pyplot as plt
# check how does it work?
#the latest feb 18 - it works just fine, and its pretty fast

# I need to make an animation 
# where different chain lengths are being compared for their crystallinity

#I need to compare the results for different chain lengths


# now I need to implement this calculation on the cluster itself
# so right after the end of simulation it calculates the parameters


#DONE!
# have to use it more now.
# I need to save the result in .npz and .pdf file format 


def get_bondlist_coords(u):
    """
    use universe of a domain
    generate normalized coordinates of bond vectors
    get universe , return bonds(coordinates)
    generate coor of all bonds(bond = chord i-1 - i+1 ), normalize it
    """
    bonds = u.bonds.atom2.positions - u.bonds.atom1.positions
    # angles = u.angles
    # bonds = angles.atom3.positions - angles.atom1.positions 
    # coords = angles.atom2.positions
    norm = np.linalg.norm(bonds,axis=1)
    bonds /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    return bonds

def moving_average(a, n=3) :
    ret = np.cumsum(a, axis=0, dtype=float)
    ret[n:,:] = ret[n:,:] - ret[:-n,:]
    return ret[n - 1:,:] / n

def get_cos2(bonds,Nneigh=3):
    """

    gets chords of a chain
    then loops from within 2:-2 of an array
    calculates get_cos2_local
    averages it 

    todo: modify so it can understand variable number of neighbours
    make it faster (numba)

    """
    nleft = int(Nneigh)/2
    nright = Nneigh - nleft
    cos2 = 0.
    cos2_local = 0.
    kk=0.0
    Nbonds = len(bonds)
    AlignVec = moving_average(bonds,Nneigh)
    for i in range(nleft,Nbonds-nright):
        cos2_local = np.dot(AlignVec[i-nleft,:],bonds[i,:])
        cos2_local = 2.0*cos2_local**2-1.0
        if cos2_local>0.9:
            # print cos2_local
            # cos2 += cos2_local
            kk += 1.0
            # print kk
    # print kk
    # cos2 = crystallinity
    if kk==0:
        cos2=0.0
    else:
        cos2 = kk/float(Nbonds-nleft-nright)
    # print " k = " , k
    return cos2

def save_plot(time,g2,psffile):
    """
    save plot 
    """
    curdir = os.getcwd()
    figuresdir = curdir+'/figures'
    if not os.path.exists(figuresdir):
        os.mkdir(figuresdir)
    plt.xlabel(r'$\mathrm{time}$')
    plt.ylabel(r'$\mathrm{g2}$')
    plt.grid(True)
    plt.title(r'$\mathrm{Crystallinity} } $'  )
    plt.plot(time, g2, 'bo-', label='$g_2$',lw=1.5)
    plt.legend(loc=4)
    plt.savefig(figuresdir + '/g2' + psffile + '.pdf')
    np.savez(figuresdir + '/g2' + psffile, time, g2)


def main():
    args = read_traj_vmd()
    curdir = os.getcwd()
    curdir = curdir+"/"
    psffile = os.path.splitext(args.psffile)[0]
    u = Universe(psffile+'.psf', curdir+'trajectory_nve.dcd')
    Nres = len(u.residues)
    frame = []
    g2 = []
    res_g2 = 0.
    for ts in u.trajectory[args.startframe:args.endframe:args.trajskip]:
        # print u.atoms
        all_g2 = 0.
        k = 0
        frame.append(ts.frame)
        for res in u.residues:
            chords = get_bondlist_coords(res)
            res_g2 = get_cos2(chords,4)
            # if res_g2>0.5:
            # k += 1
            # print res_g2
            all_g2 += res_g2
        print ("frame %d , g2 = %f" %(ts.frame, all_g2 / float(Nres)))
        g2.append(all_g2 / float(Nres))
    frame = np.array(frame)
    g2 = np.array(g2)
    save_plot(frame,g2,psffile)
    plt.plot(frame,g2,'ro-')
    plt.show()


if __name__ == '__main__':
    main()