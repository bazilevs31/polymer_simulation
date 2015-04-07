#!/usr/bin/env python
import numpy as np
from MDAnalysis import *
from read_parameters import read_traj_vmd
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# check how does it work?
#the latest feb 18 - it works just fine, and its pretty fast

# I need to make an animation 
# where different chain lengths are being compared for their crystallinity

#DONE!

# Feb 19 2015
#I need to compare the results for different chain lengths


# now I need to implement this calculation on the cluster itself
# so right after the end of simulation it calculates the parameters

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

def get_chain_crystallinity(bonds,Nneigh=3):
    """
    input: bonds, Nneigh = number of neighbours to get the mean direction
    bonds = array of chain bonds
    gets chords of a chain
    then loops from within nleft:-nright of an array
    calculates the crystallinity of a chain
    
    crystallinity = aligned parts / all parts of a chain
    align part = cos2_local > 0.9 
    """
    nleft = int(Nneigh)/2  # the left part of a chain
    nright = Nneigh - nleft  # the right part of a chain which doesn't have any neighbours
    crystallinity = 0. 
    cos2_local = 0.
    kk=0.0
    Nbonds = len(bonds)
    AlignVec = moving_average(bonds,Nneigh)
    for i in range(nleft,Nbonds-nright):
        cos2_local = np.dot(AlignVec[i-nleft,:],bonds[i,:])
        cos2_local = 2.0*cos2_local**2-1.0
        if cos2_local>0.9:
            kk += 1.0  # if chain is aligned count the number of such chains
    if kk==0:
        crystallinity=0.0  # if there are no segments with aligned parts, i.e kk=0, then crystallinity == 0.
    else:
        crystallinity = kk/float(Nbonds-nleft-nright)
    return crystallinity

def save_plot(time,g2,psffile):
    """
    input time - array of time frames
    g2 - array of g2 crystallinity parameters
    psffile - name to save the file
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


def create_hist_chainlength(chainlengths,chaing2s,lmin = 40, lmax = 120, Nbins = 10):
    """
        input: Nres*2 array of chainlengths and crystallinity parameters for each chain
        psffile name for future files
        alghorithm :
        create a linspace lmin:dl:lmax
        for lmin+dl_i:
        search chainlengths who are: > lmin+dl_(i-1) and < lmin + dl_(i)
        add second array 
        cryst += array[1,0]
        kk+=1
        cryst /= 1
        histogram [:,0] = lmin+dl_i
        histogram[:,1] = cryst
    """
    bins = np.linspace(lmin,lmax,Nbins)
    dl = bins[1]-bins[0]
    # print "lengths " , len(bins)
    histogram = 0.0*bins
    numchains = chainlengths.shape[0]
    cryst = 0.0
    kk = 0
    for li,l in enumerate(bins):
        for i in range(numchains):
            if (chainlengths[i]>l) and (chainlengths[i]<l+dl):
                        cryst += chaing2s[i]
                        kk += 1
        if kk==0:
            cryst = 0
        else:
            cryst /= float(kk)
        histogram[li] = cryst
    return bins, histogram

def main():
    args = read_traj_vmd()
    psffile = os.path.splitext(args.psffile)[0]
    u = Universe(psffile+'.psf', 'trajectory_nve.dcd')
    Nres = len(u.residues)
    frame = []
    g2 = []
    chainlengths = []
    chaing2s = []
    res_g2 = 0.
    
    fig = plt.figure()
    plt.ylim(0,1)
    ims = []
    for ts in u.trajectory[args.startframe:args.endframe:args.trajskip]:
        all_g2 = 0.
        k = 0
        chainlengths = []
        chaing2s = []
        frame.append(ts.frame)
        for res in u.residues:
            chords = get_bondlist_coords(res)
            res_g2 = get_chain_crystallinity(chords,4)
            all_g2 += res_g2
            chainlengths.append(len(res))
            chaing2s.append(res_g2)
        chainlengths = np.array(chainlengths)
        chaing2s = np.array(chaing2s)
        bins, histogram = create_hist_chainlength(chainlengths,chaing2s)
        plt.ylim(0,1)
        im = plt.bar(bins,histogram,10.0)
        ims.append([im])
        plt.savefig('hist'+str(ts.frame)+'.png')
        plt.cla()
        print ("frame %d , g2 = %f" %(ts.frame, all_g2 / float(Nres)))
        g2.append(all_g2 / float(Nres))
    frame = np.array(frame)
    g2 = np.array(g2)
    # os.system("convert -delay ")
    # save_plot(frame,g2,psffile)
    # plt.plot(frame,g2,'ro-')
    # plt.show()
    # ani.save('dynamic_images.mp4')
    # plt.show()

if __name__ == '__main__':
    main()