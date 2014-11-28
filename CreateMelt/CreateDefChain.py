#!/home/vasiliy/anaconda/bin/python
from __future__ import print_function
import numpy as np
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    

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
def read_parameters():
    """
    read parameters from the commandline
    input 
    output Nchains, ChainLength
    """
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", dest="filename",
                        type=lambda x: is_valid_file(parser, x),
                        help="write report to FILE", metavar="FILE")
    parser.add_argument("-l", 
                        "--length",
                        dest="ChainLength", 
                        default=100, 
                        type=int, 
                        help="Chain length")
    parser.add_argument("-n", 
                        "--nchains",
                        dest="Nchains", 
                        default=120, 
                        type=int, 
                        help="Total number of chains")
    parser.add_argument("-q", "--quiet",
                        action="store_false", dest="verbose",
                        default=True,
                        help="don't print status messages to stdout")
    args = parser.parse_args()
    Nchains = args.Nchains
    ChainLength = args.ChainLength
    return Nchains, ChainLength
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
    Nchains, ChainLength = read_parameters()
    mymelt = mdmelt(Nchains, ChainLength)
    mymelt.write_to_file()

if __name__ == '__main__':
    main()