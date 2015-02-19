#!/usr/bin/env python

from __future__ import print_function
import numpy as np
import os
import read_parameters    

class mdmelt():
    """create pd melt, save plot, save npz"""
    def __init__(self, Nchains, ChainLength):
        self.Nchains = Nchains
        self.ChainLength = ChainLength
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
    def write_to_file(self):
        """
        write created distribution to a file
        input Nchains, ChainLength
        output ( def.chain)
        """
        self.get_currdir()
        with open(self.curdir+'/def' + str(self.ChainLength) +'.chain', 'w') as f:
            f.write('Polymer chain definition \n\n \
        0.85          rhostar \n \
        %d          random # seed (8 digits or less)\n ' % np.random.randint(int(102220*self.Nchains)))
            f.write('1\n0\n\n')

            f.write("%s \n" % self.ChainLength)
            f.write("%s \n" % self.Nchains)
            f.write('1 \n')
            f.write('1 \n ')
            f.write('0.85 \n ')
            f.write('1.05 \n')
            f.write('\n')


def main():
    args = read_parameters.read_create_mono()
    Nchains, ChainLength = args.Nchains, args.ChainLength
    mymelt = mdmelt(Nchains, ChainLength)
    mymelt.write_to_file()

if __name__ == '__main__':
    main()