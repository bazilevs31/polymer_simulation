from MDAnalysis import *
import numpy as np
import matplotlib.pyplot as plt
from numba.decorators import jit
def get_bondlist_coords(u):
    """
    use universe of a domain
    generate normalized coordinates of bond vectors
    get universe , return bonds(coordinates)
    generate coor of all bonds(bond = chord i-1 - i+1 ), normalize it
    """
    angles = u.angles
    bonds = angles.atom3.positions - angles.atom1.positions 
    # coords = angles.atom2.positions
    norm = np.linalg.norm(bonds,axis=1)
    bonds /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    return bonds

def get_alignvec(u, nf, nave=1,skip=1):
    """
    input: universe, number of frames, (optional nave=1,skip=1) number of frames to perform averaging
    output: total_chains_eigvec 
    loop over the last frames of trajectory
    get the result eigen vectors
    """
    startFrame = nf - nave
    endFrame = nf
    assert startFrame>0, "startFrame should be > 0"
    assert (startFrame<endFrame) , "startFrame should be less than endFrame"
    nf = int(abs(endFrame-startFrame)/skip) + 1
    Nres=len(u.residues)
    total_chains_eigvec=np.zeros((Nres,3),dtype=np.float32) 

    for ts in u.trajectory[startFrame:endFrame:skip]:
        total_chains_eigvec+=get_eigvecs(u)
    return total_chains_eigvec

def get_eigvecs(chain_universe):
    """
    input u 
    output local_chains_eigvec
    use coor - coordinates of bonds(chrods)
    generate a qab tensor of outer products
    gets uses coor of all bonds generated by get_bondlist_coords 
    returns local_chains_eigvec - array eigen vectors that show the alignment directions
    of chains
    """
    residues = chain_universe.residues
    Nres=len(residues)
    local_chains_eigvec=np.empty((Nres,3),dtype=np.float32)
    dij = np.eye(3, dtype=np.float32)
    dij /= float(2)
    qab = np.empty_like(dij)
    vecs = np.empty_like(dij)
    vals = np.empty(3,dtype=np.float32)
    for ires in range(Nres):
        coor = get_bondlist_coords(residues[ires])
        # coor = np.array([[1.0, 0.0, 0.0],[1.0, 0.0, 0.0]], dtype=np.float32)
        nq = coor.shape[0]
        qab = np.einsum('ij,ik->jk', coor, coor)
        qab *= float(3.0/(2.0*nq))
        qab -= dij
        vals, vecs = np.linalg.eig(qab)
        local_chains_eigvec[ires,:] = vecs[:,0]
    return local_chains_eigvec

# @jit('float32[:](float32[:,:],float32[:,:])',nopython=True)
# @jit
def get_alignparameters(A,B):
    """
    input A,B
    output set of cos^2(A[i,:]*B[i,:])) 
    how to assert in numba?
    this functions is needed to be numbified
    """
    N = A.shape[0]
    K = A.shape[1]
    Nb = B.shape[0]
    C = np.empty((N,K),dtype=np.float32)
    tmp = 0.0
    assert N==Nb, "N = %d, should be equal to Nb=%d" % (N,Nb)
    for i in range(N):
        tmp = 0.0
        for j in range(K):
            tmp+=A[i,j]*B[i,j]
        C[i] = tmp*tmp-1.0
    return C

def get_hist(p):
    """input: array of the chain alignments
    output: the histogrammed array(we can just use plt.hist)
    and make an animation out of it
    """
    # plt.hist(p,)



def main():
    """
    do the stuff
    """
    u=Universe("../data/poly_40.psf","../data/traj_40.dcd")
    lastframe = u.trajectory.numframes
    total_chains_eigvec=get_alignvec(u,lastframe)
    order = []
    time = []
    for ts in u.trajectory[1:-1:1]:
        frame_chains_eigvec = get_eigvecs(u)   
        align = get_alignparameters(total_chains_eigvec,frame_chains_eigvec)
        print "frame = %d, order = %f " %(ts.frame,align.sum())
        time.append(ts.frame)
        order.append(align.sum())
    plt.plot(np.array(time),np.array(order))
    plt.show()

if __name__ == '__main__':
    main()

# Future
# use the same method to annalyze polymmer order
# to do that just divide into grids and analyze the parameter
