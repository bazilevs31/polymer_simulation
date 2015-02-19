#!/usr/bin/env python

import os
import argparse
# modules for readparameters



parser = argparse.ArgumentParser(description=__doc__,
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-f", "--psf", dest="psffile", help="Name of the future files, all other files will start \
                 with FILE", metavar="FILE")
args=parser.parse_args()
print args