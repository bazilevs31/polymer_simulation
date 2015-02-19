#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import os
import read_parameters





def get_currdir():
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
	curdir = curdir
	figuresdir = figuresdir
	return curdir,figuresdir

def create_hist(bins,n):
	"""
	prints parameters of the system
	plots the system built
	nchains = n
	chainlength = bins
	"""
	curdir,figuresdir=get_currdir()

	plt.bar(bins,n,width=(bins[1]-bins[0])/2.0,facecolor='green', alpha=0.75)
	print bins
	print n

	plt.xlabel(r'$\mathrm{Chain\ length}$')
	plt.ylabel(r'$\mathrm{Number\ of\ chains}$')
	plt.title(r'$\mathrm{Ndisperse\ chains\ }$' )
	plt.axis([0.8*bins.min(), 1.2*bins.max(), 0, 1.1*n.max()])
	plt.grid(True)

	filename='BIchain'
	for i in range(len(n)):
		filename += "C"+str(bins[i])+"l"+str(n[i])

	# name1 = 'l'.join(map(str, bins))
	# name2 = 'n'.join(map(str, n))
	# filename = name1+'c'+name2
	plt.savefig(figuresdir + '/' + filename + '.pdf')
	np.savez(figuresdir + '/' + filename, bins, n)
	write_to_file(bins,n,filename)
	# plt.show()
	return None

def write_to_file(bins,n,name):
	"""
	write created distribution to a file
	input mu, sigma, Nchains
	output ( creates a file pdMuSigma)
	"""
	curdir,figuresdir=get_currdir()

	n=n.astype(int)
	bins=bins.astype(int)
	with open(name + '.chain', 'w') as f:
	    f.write('Polymer chain definition\n\n\
	0.85          rhostar\n\
	%d          random # seed (8 digits or less)\n' % np.random.randint(int(100000*bins.max())))
	    f.write("%s \n" % (len(bins)))
	    f.write('0')
	    f.write('\n')
	    f.write('\n')
	    for i in range(len(bins)):
	        f.write("%s \n" % n[i])
	        f.write("%s \n" % bins[i])
	        f.write('1 \n')
	        f.write('1 \n')
	        f.write('0.85\n')
	        f.write('1.05\n')
	        f.write('\n')

def main():
	args = read_parameters.read_create_ndisp()
	bichains = args.bichains
	bichains = np.array(bichains)
	nchains = bichains[:,0]
	chainlength = bichains[:,1]
	print args
	print "chains "
	print nchains
	create_hist(chainlength,nchains)
	# mymelt = pdmelt(mu,sigma,Nchains,Nbins)
	# mymelt.create_hist()
	# mymelt.write_to_file()

if __name__ == '__main__':
	main()