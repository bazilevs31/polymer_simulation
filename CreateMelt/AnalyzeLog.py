#!/usr/bin/env python

import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import read_parameters
from log import log as pizlog

# this program analyzes polymer equilibration log 
# to analyze it we use pizza.py program 
# parameters to analyze 
# Etot(t) T(t)
# Epot(t) V(t)
# Ebond(t) msd(t)
# 
# after analyzing it 
# plot all quantities using subplot
# 

args = read_parameters.read_log()
namelog = args.logfile

initoffset = args.initoffset
outfile = args.outfile


#pizza.py part we read the thermodynamic info into lg variable
#using the pizza.py script written by Steve Plimpton
lg = pizlog(namelog)

#now we read this lg to create a python dictionary that is easy to use 
#and to plot
thermodata = dict()
for names in lg.names:
    # if (names!='KinEng'):
    thermodata[str(names)]=np.array(lg.get(str(names)))
    thermodata[str(names)]=np.delete(thermodata[str(names)], range(initoffset))

numitems = len(thermodata)
x=thermodata['Step']/1e6



# Create the PdfPages object to which we will save the pages:
# The with statement makes sure that the PdfPages object is closed properly at
# the end of the block, even if an Exception occurs.
with PdfPages('./figures/'+outfile+'.pdf','w') as pdf:
# x = np.linspace(0, 10, 1000)

    for i,element in enumerate(thermodata):
        print i
        # plt.rc('text', usetex=True)
        plt.figure(figsize=(10, 6))
        plt.plot(x, thermodata[str(element)],'b-')
        plt.title(str(element))
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

    # We can also set the file's metadata via the PdfPages object:
    d = pdf.infodict()
    d['Title'] = 'equilibration of polymer thermodynamic log'
    d['Author'] = u'Vasiliy M. Triandafilidi'
    d['Subject'] = 'How to plot lammps log file thermodynamic entries'
    d['Keywords'] = 'equilibration lammps log pizza'
    d['CreationDate'] = datetime.datetime(2014, 01, 07)
    d['ModDate'] = datetime.datetime.today()