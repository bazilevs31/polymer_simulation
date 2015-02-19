#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import os
import read_parameters 

class pdmelt():
    """create pd melt, save plot, save npz"""
    def __init__(self, mu, sigma, Nchains, Nbins):
        self.mu = mu
        self.sigma = sigma
        self.Nchains = Nchains
        self.Nbins = Nbins
        # self.filename = filename
        # self.curdir, self.figuresdir = self.get_currdir()
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
        # return currdir,figuresdir
    def create_hist(self):
        """
        prints parameters of the system
        plots the system built
        """
        self.get_currdir()
        mu = self.mu
        sigma = self.sigma
        # mu, sigma, Nchains = map(int, (mu, sigma, Nchains))
        x = self.mu + self.sigma*np.random.randn(self.Nchains)
        n, bins, patches = plt.hist(x, bins=self.Nbins,facecolor='green', alpha=0.75)
        # add a 'best fit' line
        print ( list(patches))
        Natoms = (n*bins[:-1]).sum()
        # y = Natoms*mlab.normpdf( bins, mu, sigma)
        # l = plt.plot(bins, y, 'r--', linewidth=1)
        print ("number   %d" % x.size)
        print ("number of chains are %d " % n.sum())
        print ("number of atoms is %d" % Natoms)
        
        plt.xlabel(r'$\mathrm{Chain\ length}$')
        plt.ylabel(r'$\mathrm{Number\ of\ chains}$')
        plt.title(r'$\mathrm{Polydisperse\ chains\ with }\ \mu=%d,\ \sigma=%d$' % (mu,sigma) )
        plt.axis([bins.min()-10, bins.max()+10, 0, n.max() + int(0.05*n.max())])
        plt.grid(True)
        plt.savefig(self.figuresdir + '/pd' + str(self.mu) + 'w' + str(self.sigma) + '.pdf')
        np.savez(self.figuresdir + '/pd' + str(self.mu) + 'w' + str(self.sigma), bins, n)
        plt.show()
        self.n = n
        self.bins = bins
    def write_to_file(self):
        """
        write created distribution to a file
        input mu, sigma, Nchains
        output ( creates a file pdMuSigma)
        """
        self.get_currdir()
        n = self.n
        bins = self.bins
        mu = self.mu
        sigma = self.sigma
        n=n.astype(int)
        bins=bins.astype(int)
        with open(self.curdir+'/pd' + str(mu) + 'w' + str(sigma) + '.chain', 'w') as f:
            f.write('Polymer chain definition\n\n\
        0.85          rhostar\n\
        %d          random # seed (8 digits or less)\n' % np.random.randint(int(1000*mu)))
            f.write("%s \n" % (len(bins)-1))
            f.write('0')
            f.write('\n')
            f.write('\n')
            for i in xrange(len(bins)-1):
                f.write("%s \n" % n[i])
                f.write("%s \n" % bins[i])
                f.write('1 \n')
                f.write('1 \n')
                f.write('0.85\n')
                f.write('1.05\n')
                f.write('\n')

def main():
    args = read_parameters.read_create_pd()
    mu, sigma, Nchains, Nbins = args.mu, args.sigma, args.Nchains, args.Nbins
    mymelt = pdmelt(mu,sigma,Nchains,Nbins)
    mymelt.create_hist()
    mymelt.write_to_file()

if __name__ == '__main__':
    main()

# for fitting data
    # from pylab import *
    # from numpy import loadtxt
    # from scipy.optimize import leastsq

    # fitfunc  = lambda p, x: p[0]*exp(-0.5*((x-p[1])/p[2])**2)+p[3]
    # errfunc  = lambda p, x, y: (y - fitfunc(p, x))

    # filename = "gaussdata.csv"
    # data     = loadtxt(filename,skiprows=1,delimiter=',')
    # xdata    = data[:,0]
    # ydata    = data[:,1]

    # init  = [1.0, 0.5, 0.5, 0.5]

    # out   = leastsq( errfunc, init, args=(xdata, ydata))
    # c = out[0]

    # print "A exp[-0.5((x-mu)/sigma)^2] + k "
    # print "Parent Coefficients:"
    # print "1.000, 0.200, 0.300, 0.625"
    # print "Fit Coefficients:"
    # print c[0],c[1],abs(c[2]),c[3]

    # plot(xdata, fitfunc(c, xdata))
    # plot(xdata, ydata)

    # title(r'$A = %.3f\  \mu = %.3f\  \sigma = %.3f\ k = %.3f $' %(c[0],c[1],abs(c[2]),c[3]));

    # show()    