#!/usr/bin/env python

import os
import argparse
# modules for readparameters


def read_traj_vmd():
    """
    read parameters from the commandline
    input 
    output datafile,trajectoryfile, trajskip, startframe, endframe, psffile
    uses vmd pluging to create a psf topology file
    """
    # parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # inputtrajfiles = parser.add_mutually_exclusive_group()
    # inputtrajfiles.add_argument("-f", "--psf", dest="psffile",
    #                  default="./figures/polymer_0.8.psf",
    #                  type=lambda x: is_valid_file(parser, x),
    #                  help="Name of the future files, all other files will start with FILE", 
    #                  metavar="FILE")
    # inputtrajfiles.add_argument("-d", "--data", dest="datafile", 
    #                 default="./figures/polymer_0.8.data",
    #                 type=lambda x: is_valid_file(parser, x),
    #                 help="read datafile and if exists then convert it to psf file by invoking a vmd script", 
    #                 metavar="FILE")
    parser.add_argument("-f", "--psf", dest="psffile",
                     help="Name of the future files, all other files will start with FILE", 
                     metavar="FILE")
    parser.add_argument("-d", "--data", dest="datafile", 
                    default="./figures/polymer_0.8.data",
                    type=lambda x: is_valid_file(parser, x),
                    help="read datafile and if exists then convert it to psf file by invoking a vmd script", 
                    metavar="FILE")

    parser.add_argument("-t", "--trajectroy", dest="traj", 
                        default="trajectory_nve.dcd",
                        type=lambda x: is_valid_file(parser, x),
                        help="Input trajectory file)", metavar="FILE")
    parser.add_argument("-s",  "--trajskip", dest="trajskip", 
                    default=10, 
                    type=int, 
                    help="How many steps are to be skipped when trajectory \
                                        file is being red\
                                        (needs to be > 1, < number of frames) \
                                        type (default: %(default)s)")
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

    args = parser.parse_args()
    create_psf(args)
    return args




def read_log():
    """
    provide information for logfile
    output: args , containing logfile, name of the output file
    """

    parser = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        
    parser.add_argument("-l", "--log", dest="logfile", 
                        default="./figures/log.kremer",
                        help="read logfile to analyze")
    parser.add_argument("-s", 
                    "--stride",
                    dest="initoffset", 
                    default=100, 
                    type=int, 
                    help="How many first steps are to be skipped, because they are ususally too big")

    parser.add_argument("-o", 
                    "--output",
                    dest="outfile", 
                    default="equilibration_thermo.pdf", 
                    help="results of the logfile thermo info ploting will be saved here")

    args = parser.parse_args()
    return args

def read_pbs():
    """
    read information about the pbs file you want to create
    this read pbs can read what you want to do 
    -about creating polymers
    -running the simulation including the equilibration 
    -analazying the results, using certain program

    TODO: for analyzing part choose what kind of analysis you do want to do
    
    """
    parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # group = parser.add_mutually_exclusive_group(help='What do you want to do create melt or run sim')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--create', action='store_true',help='Create and equilibrate the run')
    group.add_argument('--run', action='store_true', help='Run the simulation')
    group.add_argument('--analyze', action='store_true', help='Analyze the alignment using AnalyzeTrueg2.py')
    
    parser.add_argument("-p", 
                    "--procs",
                    dest="procs", 
                    default=12, 
                    type=int, 
                    help="Number of processors")
    parser.add_argument("-n", 
                    "--nodes",
                    dest="nodes", 
                    default=5, 
                    type=int, 
                    help="Number of nodes") 
    parser.add_argument("-m", 
                    "--memmory",
                    dest="memmory", 
                    default=600, 
                    type=int, 
                    help="Memmory to use")
    parser.add_argument("-wm", 
                    "--wallminutes",
                    dest="wallminutes", 
                    default=0, 
                    type=int, 
                    help="Walltime minutes")
    parser.add_argument("-wh", 
                    "--wallhours",
                    dest="wallhours", 
                    default=8, 
                    type=int, 
                    help="Number of nodes")
    parser.add_argument("-name", 
                    "--pbsname",
                    dest="pbsname", 
                    default='poly', 
                    type=str, 
                    help="Name of pbs file")

    args = parser.parse_args()
    return args

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

def read_create_mono():
    """
    create a monodisperse chains
    """
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-nch", 
                        "--nchains",
                        dest="Nchains", 
                        default=500, 
                        type=int, 
                        help="Total number of chains type (default: %(default)s)")
    parser.add_argument("-l", 
                        "--length",
                        dest="ChainLength", 
                        default=100, 
                        type=int, 
                        help="Chain length type (default: %(default)s)")

    args = parser.parse_args()

    return args

def read_create_pd():
    """
    create a polydisperse chains
    input: 
    mu - average chain length
    sigma - chain length distribution width
    Nchains - number of chains 
    Nbins - number of bins to discretize the distribution
    """
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

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
    args = parser.parse_args()

    return args

def read_create_ndisp():
    """
    create a ndisperse chains
    input should be done in data tuples
    (#of chains, chain length) (#number of chains, chain length) ... 

    example:
    for the case of a bidisperse system with 100 C100 and 50 C20 :
        (100,100), (50,20)
    """
    parser = argparse.ArgumentParser(description=__doc__,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument ('-bi', '--bidisperse', dest='bichains', nargs=2, type=int, action='append',help='Import tuples of data \
    numberOfChains ChainLength')
    #create pd melt #create md melt
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

def create_psf(args):
    """given data file produce psf file, read-eidt dcd file"""
    psffile = os.path.splitext(args.psffile)[0]
    datafile = os.path.splitext(args.datafile)[0]
    curdir = os.getcwd()
    curdir = curdir+"/"
    filestring = " ".join(("create_list_cryst.sh ",datafile,psffile,curdir))
    os.system(filestring)
    return args

def main():
    """main
    """
    # print 1
    # read_parameters()
    read_traj_vmd()
    # print a
    # b = read_create_ndisp()
    # print b
    # c = read_log()
    # print c 
    # d = read_pbs()
    # print d
    # e = read_plot()
    # print e 
    # f = read_traj()
    # print f

if __name__ == '__main__':
    main()