"""
Example: Radial distribution function g(r)
==========================================

Calculating *g(r)* (radial distribution function) of water, taking
into account periodic boundaries.

Contains a few speed-ups over the most naive implementation
 - use self_distance_array() instead of distance_array() and pre-allocate
   dist array
 - use numpy in-place operations where possible
 - use 1D histogram function (instead of e.g. histogramdd())

Profiling shows that the computational bottleneck is the
:func:`numpy.histogram` function.
"""


from itertools import izip

import numpy

from MDAnalysis import *
from MDAnalysis.core.distances import * ##distance_array
import MDAnalysis.core.units            # for bulk water density
from subprocess import call, os
import commands

try:
    import matplotlib
    matplotlib.use('agg')  # no interactive plotting, only save figures
    import pylab
    have_matplotlib = True
except ImportError:
    have_matplotlib = False


conf = commands.getoutput("ls | grep .psf")
traj = commands.getoutput("ls | grep .pdb")
u = Universe (conf, traj)
solvent = u.selectAtoms("all")

dmin, dmax = 0.0, 8.0
nbins = 80

# set up rdf
rdf, edges = numpy.histogram([0], bins=nbins, range=(dmin, dmax))
rdf *= 0
rdf = rdf.astype(numpy.float64)  # avoid possible problems with '/' later on

n = solvent.numberOfAtoms()
dist = numpy.zeros((n*(n-1)/2,), dtype=numpy.float64)

print "Start: n = %d, size of dist = %d " % (n, len(dist))

boxvolume = 0
for ts in u.trajectory:
        print "Frame %4d" % ts.frame
        boxvolume += ts.volume      # correct unitcell volume
        coor = solvent.coordinates()
        # periodicity is NOT handled correctly in this example because
        # distance_array() only handles orthorhombic boxes correctly
        ##box = ts.dimensions[:3]     # fudge: only orthorhombic boxes handled correctly
        # DISABLE:
        box = None
        self_distance_array(coor, box, result=dist)  # use pre-allocated array, box not fully correct!!
        new_rdf, edges = numpy.histogram(dist, bins=nbins, range=(dmin, dmax))
        rdf += new_rdf
print

numframes = u.trajectory.numframes / u.trajectory.skip
boxvolume /= numframes    # average volume

# Normalize RDF
radii = 0.5*(edges[1:] + edges[:-1])
vol = (4./3.)*numpy.pi*(numpy.power(edges[1:],3)-numpy.power(edges[:-1], 3))
# normalization to the average density n/boxvolume in the simulation
density = n / boxvolume
# This is inaccurate when solutes take up substantial amount
# of space. In this case you might want to use
## import MDAnalysis.core.units
## density = MDAnalysis.core.units.convert(1.0, 'water', 'Angstrom^{-3}')
norm = density * (n-1)/2 * numframes
rdf /= norm * vol

call("mkdir output")
outfile = './output/rdf.dat'
with open(outfile,'w') as output:
    for radius,gofr in izip(radii, rdf):
        output.write("%(radius)8.3f \t %(gofr)8.3f\n" % vars())
print "g(r) data written to %(outfile)r" % vars()

if have_matplotlib:
    matplotlib.rc('font', size=14)
    matplotlib.rc('figure', figsize=(5, 4))
    pylab.clf()
    pylab.plot(radii, rdf, linewidth=3)
    pylab.xlabel(r"distance $r$ in $\AA$")
    pylab.ylabel(r"radial distribution function $g(r)$")
    pylab.savefig("./figures/rdffinal.pdf")
    pylab.savefig("./figures/rdf.png")
    print "Figure written to ./figures/rdf.{pdf,png}"
