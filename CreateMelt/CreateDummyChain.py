import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


# #TODO 
# use a MDanalysis trajectory to test how does this program work in a real world
# modify the program so it can analyze variable number of neighbours



# so I pretty much have the alghorithm for creating a set of arrays for testing 
# i also do have a alghorithm for analyzing the alignnment of a chain

# now I need to use this alghorithm for a system in a bulk

# I also need to use it for the chain alignnment histogramm

def create_chain_lin(num_atoms,rand_shift=0.01):
    """creaet a dummy array of atoms in a line"""
    chain = np.zeros((num_atoms,3))
    r0 = np.zeros(3)
    dr = np.ones(3)
    chain[0,:] = r0
    for i in range(num_atoms):
        rand_displace = rand_shift*np.random.rand(3)
        chain[i,:] = r0+(dr+rand_displace)*i
    return chain

def create_chain_circ(num_atoms):
    """
    create a dummy array of atoms forming a circle"""
    chain = np.zeros((num_atoms,3))
    r0 = np.ones(3)
    dr = np.ones(3)
    da = 2*np.pi/float(num_atoms)
    chain[0,:] = r0
    for i in range(num_atoms):
        angle = (i+1)*da
        displace = np.array([np.sin(angle),np.cos(angle),0.0])
        chain[i,:] = r0+displace
    return chain

def get_bondlist_coords(atoms):
    """
    use universe of a domain
    generate normalized coordinates of bond vectors
    get universe , return bonds(coordinates)
    generate coor of all bonds(bond = chord i-1 - i+1 ), normalize it
    """
    bonds = np.zeros((len(atoms)-1,3))
    for i in range(len(atoms)-1):
        bonds[i,:] = atoms[i+1,:] - atoms[i,:]
    norm = np.linalg.norm(bonds,axis=1)
    bonds /= norm[:, None] #the norm vector is a (nx1) and we have to create dummy directions -> (n,3)
    return bonds

def moving_average(a, n=3) :
    ret = np.cumsum(a, axis=0, dtype=float)
    ret[n:,:] = ret[n:,:] - ret[:-n,:]
    return ret[n - 1:,:] / n

def get_cos2(atoms,Nneigh=3):
    """

    gets chords of a chain
    then loops from within 2:-2 of an array
    calculates get_cos2_local
    averages it 

    todo: modify so it can understand variable number of neighbours
    make it faster (numba)

    """
    bonds = get_bondlist_coords(atoms)
    nleft = int(Nneigh)/2
    nright = Nneigh - nleft
    print nleft
    print nright
    cos2 = 0.
    k = 0.0
    cos2_local = 0.
    Nbonds = len(bonds)
    AlignVec = moving_average(bonds,Nneigh)
    print AlignVec.shape
    print bonds.shape
    # print AlignVec
    # print "loop"
    for i in range(nleft,Nbonds-nright):
        cos2_local = np.dot(AlignVec[i-2,:],bonds[i,:])
        # print cos2_local
        # print bonds[i,:]
        cos2_local = 2.0*cos2_local**2-1.0
        # print cos2_local
        # print cos2_local
        # print cos2_local
        cos2 += cos2_local
        k += 1
        # print " i ", i, " bonds ", bonds[i,:]

    # print AlignVec
    cos2 /= k
    # print cos2
    return cos2



# rspace = np.linspace(0.0001,0.1,40)
rspace = np.arange(100)*0.001
# rspace = np.arange(1)*0.1
for rd in rspace:
    linchain = create_chain_lin(200,rd)
    # linchords = get_bondlist_coords(linchain)
    # print linchords
    # print get_cos2(linchain)
    print "rand ", rd , " cos2 ", get_cos2(linchain,5)
    # fig = plt.figure()
    # ax = fig.add_subplot(111,projection='3d')
    # ax.scatter(linchain[:,0],linchain[:,1],linchain[:,2],zdir='x',c='red')
    # # plt.show()
    # plt.savefig('linchain.%s.png' % str(rd))

        
# linchain = create_chain_lin(600)
# circchain = create_chain_circ(600)
# # print linchain
# # print circchain
# # chords = get_bondlist_coords(linchain)
# circchords = get_bondlist_coords(circchain)
# linchords = get_bondlist_coords(linchain)
# print "lin", get_cos2(linchords)
# # print "circ", get_cos2(circchords)

# print circchords


# fig = plt.figure()
# ax = fig.add_subplot(111,projection='3d')
# # ax.scatter(linchain[:,0],linchain[:,1],linchain[:,2],zdir='z',c='red')
# ax.scatter(circchain[:,0],circchain[:,1],circchain[:,2],zdir='z',c='red')
# plt.show()
