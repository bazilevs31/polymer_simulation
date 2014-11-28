#!/home/vasiliy/anaconda/bin/python

# Purpose: Calculate radial distribution function  using Python and Numba library
# Author:  Triandafilidi Vasiliy , MSc student at CHBE UBC, Vancouver
# e-mail:  vtriandafilidi(at)chbe(dot)ubc(dot)ca
# Syntax:  python  python_numba_rdf.py
# Requires: poly.psf poly.pdb, numba library 

# Theory:
# http://en.wikipedia.org/wiki/Radial_distribution_function
# 
# 
# Copyright (c) 2014 Vasiliy Triandafilidi
# Released under the GNU Public Licence, v2 or any higher version 

from numba import jit, autojit,njit
import matplotlib.pyplot as plt 
import math
from MDAnalysis import *
import numpy as np 
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter



#get wrapped coordinates
#and get the nearest image distance
@jit('float32(float32,float32)',nopython=True)
def numbatrunc(a,l):
	a = abs(a)-l*int(abs(a)/l)
	if (a > l/2.0):
		return l - a
	else:
		return a

@jit('f8(f8)',nopython=True)
def CUB(x):
	return x**3.

#loop over all atoms 
#for ever atoms loop over the rest
#get the distance(consider pbc) histogramm it
@jit('void(float32[:,:],float32[:],float32,float32,float32)',nopython=True)
def pairwise_python(X,g,L,smax,db):
	""" 
	input X - array of atom positions, g(r), L(box), smax(cutoff), db(bins)
	"""
	M = X.shape[0]
	N = X.shape[1]
	nbins = int(smax/db)
	for i in range(M-1):
		# print " atom " , i
		for j in range(i+1,M):
			d = 0.0
			for k in range(N):
				tmp = X[i, k] - X[j, k]
				tmp = numbatrunc(tmp,L)
				d += tmp * tmp
			d = np.sqrt(d)
			if (d < smax):
				g[int(d/db)] += 2.0

#normalize the histogramm so the r->inf it -> 1.0
@jit('void(float32[:],float32,float32,int32)',nopython=True)
def normalise(g,L,db,N):
	"""
	input : g(r), L(box), db (bins), N(atoms)
	output : nothing(but g[:] is normalized)
	"""
	n = g.shape[0]
	# pairs = float(N)*(float(N)-1.0)/float(2)
	pairs = float(N)*(float(N))
	factor = (4./3.)*np.pi*pairs/CUB(L)
	density = N/CUB(L)
	for i in range(n):
		g[i] /= factor*(CUB(i+1)-CUB(i))*CUB(db)

class rdf(object):
	"""docstring for rdf"""
	def __init__(self, u, smax, db, trajskip, endframe, name):
		self.u = u
		self.smax = smax 
		self.db = db
		self.trajskip = trajskip
		self.endframe = endframe
		self.name = name
	def init(self):
		"""
		initialize and run everything
		"""
		a = self.u.selectAtoms("all")
		box = self.u.universe.dimensions[:3]
		aa = a.positions
		L = box[0]
		nbins = int(self.smax/self.db)
		print "nbins", nbins
		self.D = np.zeros(nbins, dtype=np.float32)
		self.bins = np.linspace(0,self.smax,nbins)

		pairwise_python(aa, self.D, L, self.smax, self.db)
		normalise(self.D,L,self.db,aa.shape[0])
		self.plot_rdf()
			
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
	
	def plot_rdf(self):
		self.get_currdir()
		plt.axhline(y=1.0, xmin=0.0, xmax=self.smax, linewidth=1.0, color = 'k')
		# plt.plot(self.bins,self.D,linewidth=2,color='green',linestyle='o-',label='psffile')
		plt.plot(self.bins,self.D, 'bo-', label='rdf',lw=1.5)

		plt.xlabel(r'$\mathrm{r,\ lj}$')
		plt.ylabel(r'$\mathrm{g(r)}$')
		plt.axis([0.0, self.smax*1.0, 0, 1.1*self.D.max()])
		plt.legend()
		plt.grid(True)
		plt.title(r'$\mathrm{Radial\ distribution\ function\ g(r)\ } $'  )
		plt.savefig(self.figuresdir + '/' + self.name + '.pdf')
		np.savez(self.figuresdir + '/' + self.name, self.bins, self.D)
		plt.show()


def read_parameters():
	"""
	read parameters from the commandline
	input 
	output u,smax, db, trajskip, endframe, name
	in future we can add psf from data
	"""
	parser = ArgumentParser(description=__doc__,
	                        formatter_class=ArgumentDefaultsHelpFormatter)
	parser.add_argument("-f", "--psf", dest="psffile",type=lambda x: is_valid_file(parser, x), help="Read FILE,  .psf required", metavar="FILE")
	parser.add_argument("-s", 
					"--trajskip",
                    dest="trajskip", 
                    default=1, 
                    type=int, 
                    help="Skip of the trajectory file")
	parser.add_argument("-nm", 
					"--name",
                    dest="name", 
                    default="rdf", 
                    type=str, 
                    help="Name of the result file, no .pdf required")
	parser.add_argument("-e", 
					"--endframe",
                    dest="endframe", 
                    default=-1, 
                    type=int, 
                    help="End file of the trajectory file")
	parser.add_argument("-m", 
				"--smax",
                dest="smax", 
                default=8.0, 
                type=float, 
                help="Distance cutoff, lj units")
	parser.add_argument("-d", 
				"--deltabins",
                dest="db", 
                default=0.1, 
                type=float, 
                help="Bin size, lj units")
	# parser.add_argument("-d", "--data", dest="datafile", default="polymer_0.8.data",
	#                     type=lambda x: is_valid_file(parser, x),
	#                     help="write report to FILE", metavar="FILE")
	parser.add_argument("-t", "--trajectory", dest="dcdinput", default="trajectory_nve.dcd",
	                    type=lambda x: is_valid_file(parser, x),
	                    help="write report to FILE", metavar="FILE")
	args = parser.parse_args()
	psffile = args.psffile
	trajskip = args.trajskip
	endframe = args.endframe
	db = args.db
	smax = args.smax
	dcdinput = args.dcdinput
	name = args.name
	# create_psf(datafile, dcdinput, trajskip,psffile+".psf")
	u = Universe(psffile, dcdinput)
	return u,smax, db, trajskip, endframe, name

def is_valid_file(parser, arg):
	"""
	Check if arg is a valid file 
	"""
	arg = os.path.abspath(arg)
	if not os.path.exists(arg):
		parser.error("The file %s doesn't exist " % arg)
	else:
		return arg

def main():
	u,smax, db, trajskip, endframe, name = read_parameters()
	myrdf = rdf(u,smax, db, trajskip, endframe, name)
	myrdf.init()


if __name__ == '__main__':
	main()