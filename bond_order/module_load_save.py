from itertools import izip
import numpy
import commands
import sys

def write_file(array_1, array_2, filename):
	radii = array_1
	rdf = array_2
	#this function writes files of two arrays into a file
	commands.getoutput("mkdir output")
	outfile = './output/' + filename
	with open(outfile,'w') as output:
	    for radius,gofr in izip(radii, rdf):
	        output.write("%(radius)8.3f \t %(gofr)8.3f\n" % vars())
	print "g(r) data written to %(outfile)r" % vars()

def plot_file(array_1, array_2, filename):

	try:
	    import matplotlib
	    matplotlib.use('agg')  # no interactive plotting, only save figures
	    import pylab
	    have_matplotlib = True
	except ImportError:
	    have_matplotlib = False
	
	# this function plots two arrays and saves files
	radii = array_1
	rdf = array_2
	outfile = './figures/' + filename
	commands.getoutput("mkdir figures")
	if have_matplotlib:
	    matplotlib.rc('font', size=14)
	    matplotlib.rc('figure', figsize=(5, 4))
	    pylab.clf()
	    pylab.plot(radii, rdf, linewidth=3)
	    pylab.xlabel(r"distance $r$ in $\AA$")
	    pylab.ylabel(r"radial distribution function $g(r)$")
	    pylab.savefig(outfile + ".pdf")
	    pylab.savefig(outfile + ".png")
	    print "Figure written to ./figures/" + filename  + "{pdf,png}"

if __name__ == '__main__':
	# test1.py executed as script
	# do something
	some_func()