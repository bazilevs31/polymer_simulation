#!/home/vasiliy/anaconda/bin/python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os


def del_end(x):
    """
    delete npz dimension of the file
    """
    if x[-4:] == '.npz':
        return ''.join(x.split())[:-4]
    else:
        return x
        
def get_currdir():
    """
    get current directory if it exists
    if not make one and return it
    """
    print "doing animation"
    print "current directory is"
    print os.getcwd() + "\n"
    curdir = os.getcwd()
    figuresdir = curdir+'/figures'
    if not os.path.exists(figuresdir):
        os.mkdir(figuresdir)
    print "the figuresdir has been created"
    return figuresdir

def plotrdf(inname,outname):
    """
    plot animation of an evolution of a rdf function 
    """
    try:
        inname = del_end(inname)
        print "I am loading the file"
        npz=np.load(inname+'.npz')
        print "the file has been loaded"
    except:
        raise ValueError('cant open inname = %s.npz' % inname)
    Nframes = len(npz.items())-2
    y1 = npz['arr_1']; x = npz['arr_0']
    xmin = x.min(); xmax = 1.1*x.max()
    ymin = y1.min(); ymax = 1.1*y1.max()
    print "plotting"
    def animate(nframe):
        plt.cla()
        y = npz['arr_'+str(nframe+1)]
        plt.axhline(y=1.0, xmin=0.0, xmax=xmax, linewidth=1.0, color = 'k')
        plt.plot(x,y, 'bo-', label='rdf',lw=1.5)
        plt.xlim(xmin,xmax); plt.ylim(ymin,ymax)
        plt.xlabel(r'$\mathrm{r,\ lj}$')
        plt.ylabel(r'$\mathrm{g(r)}$')
        plt.legend()
        plt.grid(True)
        plt.title(r'$\mathrm{Radial\ distribution\ function\ g(r)\  frame =  %.2f} $' % (1.*nframe/Nframes) )


    fig = plt.figure(figsize=(6,5))  
    figuresdir = get_currdir()
    anim = animation.FuncAnimation(fig, animate, frames=Nframes)
    anim.save(figuresdir+'/'+outname+'.gif', writer='imagemagick', fps=4)
    return  None


def plotend2end(inname,outname):
    """
    plot animation of an evolution of an end2end function
    """
    try:
        inname = del_end(inname)
        print "I am loading the file"
        npz=np.load(inname+'.npz')
        print "the file has been loaded"
    except:
        raise ValueError('cant open inname = %s.npz' % inname)
    Nframes = len(npz.items())-2
    y1 = npz['arr_1']; x = npz['arr_0']
    xmin = x.min(); xmax = 1.1*x.max()
    ymin = y1.min(); ymax = 1.1*y1.max()
    print "plotting"
    def animate(nframe):
        plt.cla()
        y = npz['arr_'+str(nframe+1)]
        plt.axhline(y=1.0, xmin=0.0, xmax=xmax, linewidth=1.0, color = 'k')
        # plt.plot(x,y, 'bo-', label='rdf',lw=1.5)
        plt.plot(x,y, '-', label='rdf',lw=1.5)
        plt.xlim(xmin,xmax); plt.ylim(ymin,ymax)
        plt.xlabel(r'$\mathrm{r,\ lj}$')
        plt.ylabel(r'$\mathrm{g(r)}$')
        plt.legend()
        plt.grid(True)
        plt.title(r'$\mathrm{End to End distance\  frame =  %.2f} $' % (1.*nframe/Nframes) )


    fig = plt.figure(figsize=(6,5))  
    figuresdir = get_currdir()
    anim = animation.FuncAnimation(fig, animate, frames=Nframes)
    anim.save(figuresdir+'/'+outname+'.gif', writer='imagemagick', fps=4)
    return  None

def main():
    plotrdf('rdf','testout')

if __name__ == '__main__':
    main()
