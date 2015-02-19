#!/usr/bin/env python

from MDAnalysis import Universe
import os
import argparse
# from argparse import ArgumentDefaultsHelpFormatter

# New way of reading parameters
# it has different functions which are logical to have
# 
# traj: 
# read lammps.data
# read dcd
# wrap the coordinates
# the skip start endframe and other stufff
# 
# create polymer melt parser
# 
# 
# plot stuff parser

def read_traj():
    """
    read simple lammps datafile
    read trajectory 
    output: universe, filename
    """
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--data", dest="datafile", 
                    default="./figures/lammps.data",
                    type=lambda x: is_valid_file(parser, x),
                    help="provide correct lammps file, lammps.data ")
    parser.add_argument("-s", 
                "--trajskip",
                dest="trajskip", 
                default=100, 
                type=int, 
                help="How many steps are to be skipped when trajectory \
                                    file is being red\
                                    (needs to be > 1, < number of frames) )")
    parser.add_argument("-t", "--trajectory", dest="traj", 
                    default="trajectory_nve.dcd",
                    type=lambda x: is_valid_file(parser, x),
                    help="Input trajectory file", metavar="FILE")

    parser.add_argument("-f", "--psf", dest="psffile", help="Name of the future files, all other files will start \
                     with FILE", metavar="FILE")

    parser.add_argument("-e", "--endframe", dest="endframe", 
                    default=-1, 
                    type=int, 
                    help="End frame of the trajectory file type (default: %(default)s)")
    parser.add_argument("-st", 
                    "--startframe",
                    dest="startframe", 
                    default=1, 
                    type=int, 
                    help="Start frame of the trajectory file type (default: %(default)s)")
    parser.add_argument("-w", 
                "--wrap",
                action="store_true",
                dest="wrap", 
                default=False,
                help="Do you need to use wrapped trajectory? type (default: %(default)s)")
    args = parser.parse_args()
    # here need to process the info and write the information
    # wrap if needed
    # return the universe
    psffile = os.path.splitext(args.psffile)[0]
    u = Universe(args.datafile, args.traj)    
    return u,args,psffile

def read_plot():
    """read the ploting information
    output: the information for ploting
    """
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-a', action='append', dest='collection',
                        type=lambda x: is_valid_file(parser, x),
                        default=[],
                        help='Add repeated values to a list type (default: %(default)s)',
                        )
    parser.add_argument("-x", 
                    "--name_x",
                    dest="name_x", 
                    default='arr_0', 
                    type=str, 
                    help="x direction type (default: %(default)s)")
    parser.add_argument("-y", 
                    "--name_y",
                    dest="name_y", 
                    default='arr_1', 
                    type=str, 
                    help="y direction type (default: %(default)s)")
    parser.add_argument("-t", 
                    "--title",
                    dest="titlename", 
                    type=str, 
                    help="Name of the result pdf and npz files type (default: %(default)s)")
    parser.add_argument("-b", 
                    "--boxes",
                    action="store_true",
                    dest="boxes", 
                    default=False,
                    help="Do you need boxes? type (default: %(default)s)")
    parser.add_argument("-l", 
                    "--legend",
                    action="store_true",
                    dest="legend", 
                    default=False,
                    help="Do you need legend? type (default: %(default)s)")

    args = parser.parse_args()

    return args

def read_create():
    """read parameters for creating a polymer
    output args
    """
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument ('-bi', '--bidisperse', dest='bichains', nargs=2, type=int, action='append',help='Import tuples of data \
    numberOfChains ChainLength')
    #create pd melt #create md melt
    parser.add_argument("-m", 
                        "--mu",
                        dest="mu", 
                        default=80, 
                        type=int, 
                        help="average chain length type (default: %(default)s)")
    parser.add_argument("-s", 
                        "--sigma",
                        dest="sigma", 
                        default=10, 
                        type=int, 
                        help="width of the chain length distribution type (default: %(default)s)")
    parser.add_argument("-nch", 
                        "--nchains",
                        dest="Nchains", 
                        default=500, 
                        type=int, 
                        help="Total number of chains type (default: %(default)s)")
    parser.add_argument("-Nb", 
                        "--Nbins",
                        dest="Nbins", 
                        default=10, 
                        type=int, 
                        help="Number of bins type (default: %(default)s)")
    parser.add_argument("-l", 
                        "--length",
                        dest="ChainLength", 
                        default=100, 
                        type=int, 
                        help="Chain length type (default: %(default)s)")

    args = parser.parse_args()

    return args


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
    # read_parameters()
    # a = read_traj()
    a = read_plot()
    # a = read_create()

if __name__ == '__main__':
    main()
