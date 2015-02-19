#!/usr/bin/env python

from MDAnalysis import Universe
import os
import subprocess
import argparse
# from argparse import ArgumentDefaultsHelpFormatter

def read_parameters():
    """
    read parameters from the commandline
    input 
    output u, trajskip, endframe, psffile, Nsub, sthreshold
    """
    # parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(description=__doc__,
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    subparsers = parser.add_subparsers(dest='commands',help='Commands for analyzing trajectory or creating a melt')

    simple_parser = subparsers.add_parser('simple', help='simple parser with ./figures/lammps and trajectory_nve.dcd')
    simple_parser.add_argument("-d", "--data", dest="datafile", 
                        default="./figures/lammps.data",
                        type=lambda x: is_valid_file(parser, x),
                        help="read datafile type ")
    simple_parser.add_argument("-s", 
                    "--trajskip",
                    dest="trajskip", 
                    default=100, 
                    type=int, 
                    help="How many steps are to be skipped when trajectory \
                                        file is being red\
                                        (needs to be > 1, < number of frames) )")
    simple_parser.add_argument("-t", "--trajectory", dest="traj", 
                        default="trajectory_nve.dcd",
                        type=lambda x: is_valid_file(parser, x),
                        help="Input trajectory file)", metavar="FILE")
    simple_parser.add_argument("-f", "--psf", dest="psffile", help="Name of the future files, all other files will start \
                         with FILE", metavar="FILE")


    traj_parser = subparsers.add_parser('traj', help='trajectory parser content')
    #general trajectory parameters data file, psffile, trajectory, skip, endframe, startframe
    traj_parser.add_argument("-d", "--data", dest="datafile", 
                    default="./figures/polymer_0.8.data",
                    type=lambda x: is_valid_file(parser, x),
                    help="read datafile", metavar="FILE")
    traj_parser.add_argument("-f", "--psf", dest="psffile", help="Name of the future files, all other files will start \
                     with FILE", metavar="FILE")
    traj_parser.add_argument("-s",  "--trajskip", dest="trajskip", 
                    default=10, 
                    type=int, 
                    help="How many steps are to be skipped when trajectory \
                                        file is being red\
                                        (needs to be > 1, < number of frames) \
                                        type (default: %(default)s)")
    traj_parser.add_argument("-e", "--endframe", dest="endframe", 
                    default=-1, 
                    type=int, 
                    help="End frame of the trajectory file type (default: %(default)s)")
    traj_parser.add_argument("-t", "--trajectory", dest="traj", 
                        default="trajectory_nve.dcd",
                        type=lambda x: is_valid_file(parser, x),
                        help="Input trajectory file type (default: %(default)s)", metavar="FILE")
    traj_parser.add_argument("-st", 
                    "--startframe",
                    dest="startframe", 
                    default=1, 
                    type=int, 
                    help="Start frame of the trajectory file type (default: %(default)s)")
    traj_parser.add_argument("-w", 
                "--wrap",
                action="store_true",
                dest="wrap", 
                default=False,
                help="Do you need to use wrapped trajectory? type (default: %(default)s)")
    #sparameter params
    traj_parser.add_argument("-g", 
                "--Nsub",
                dest="Nsub", 
                default=7, 
                type=int, 
                help="number of grid cells in each dimension type (default: %(default)s)")
    traj_parser.add_argument("-l", 
                "--sthreshold",
                dest="sthreshold", 
                default=0.8, 
                type=float, 
                help="threshold for determining the crystalline domain type (default: %(default)s)")
    #rdf
    traj_parser.add_argument("-sm", 
            "--smax",
            dest="smax", 
            default=8.0, 
            type=float, 
            help="Distance cutoff, lj units type (default: %(default)s)")
    traj_parser.add_argument("-db", 
            "--deltabins",
            dest="db", 
            default=0.1, 
            type=float, 
            help="Bin size, lj units type (default: %(default)s)")
    traj_parser.description="traj"



    create_parser = subparsers.add_parser('create', help='create parser content')

    create_parser.add_argument ('-bi', '--bidisperse', dest='bichains', nargs=2, type=int, action='append',help='Import tuples of data \
    numberOfChains ChainLength')
    #create pd melt #create md melt
    create_parser.add_argument("-m", 
                        "--mu",
                        dest="mu", 
                        default=80, 
                        type=int, 
                        help="average chain length type (default: %(default)s)")
    create_parser.add_argument("-s", 
                        "--sigma",
                        dest="sigma", 
                        default=10, 
                        type=int, 
                        help="width of the chain length distribution type (default: %(default)s)")
    create_parser.add_argument("-nch", 
                        "--nchains",
                        dest="Nchains", 
                        default=500, 
                        type=int, 
                        help="Total number of chains type (default: %(default)s)")
    create_parser.add_argument("-Nb", 
                        "--Nbins",
                        dest="Nbins", 
                        default=10, 
                        type=int, 
                        help="Number of bins type (default: %(default)s)")
    create_parser.add_argument("-l", 
                        "--length",
                        dest="ChainLength", 
                        default=100, 
                        type=int, 
                        help="Chain length type (default: %(default)s)")


    plot_parser = subparsers.add_parser('plot', help='plot parser content')
    plot_parser.add_argument('-a', action='append', dest='collection',
                        type=lambda x: is_valid_file(parser, x),
                        default=[],
                        help='Add repeated values to a list type (default: %(default)s)',
                        )
    plot_parser.add_argument("-x", 
                    "--name_x",
                    dest="name_x", 
                    default='arr_0', 
                    type=str, 
                    help="x direction type (default: %(default)s)")
    plot_parser.add_argument("-y", 
                    "--name_y",
                    dest="name_y", 
                    default='arr_1', 
                    type=str, 
                    help="y direction type (default: %(default)s)")
    plot_parser.add_argument("-t", 
                    "--title",
                    dest="titlename", 
                    type=str, 
                    help="Name of the result pdf and npz files type (default: %(default)s)")
    plot_parser.add_argument("-b", 
                    "--boxes",
                    action="store_true",
                    dest="boxes", 
                    default=False,
                    help="Do you need boxes? type (default: %(default)s)")
    plot_parser.add_argument("-l", 
                    "--legend",
                    action="store_true",
                    dest="legend", 
                    default=False,
                    help="Do you need legend? type (default: %(default)s)")


    args = parser.parse_args()

    if args.commands=="traj":  
        psffile = del_endpsf(args.psffile)
        wrap = args.wrap
        #if we want to use the wrapped trajectory
        if wrap==True:
            psfpath = os.path.abspath(psffile+'.psf')
            trajpath = os.path.abspath('trajSkipwrap.dcd')
            if ((os.path.exists(psfpath)==True) and (os.path.exists(trajpath)==True)):
                u = Universe(psffile +".psf","trajSkipwrap.dcd")
            # elif ((os.path.exists(psfpath)==False) or (os.path.exists(trajpath)==False)):
            else:
                create_psf(args.datafile, args.traj, args.trajskip,psffile+".psf")
                u = Universe(psffile +".psf","trajSkipwrap.dcd")
        elif wrap==False:
            trajpath = os.path.abspath(args.traj)
            if os.path.exists(trajpath):
                u = Universe(psffile +".psf",args.traj)
            else:
                raise ValueError('Cant find trajectory file at %s' % trajpath)
        else:
            raise ValueError('Something is wrong with trajectory wrapping parameter')
        return u,args
    elif args.commands=="create":
        return args
    elif args.commands=="plot":
        return args
    elif args.commands=="simple":
        print args
        u = Universe(args.datafile,args.traj)
        psffile = del_endpsf(args.psffile)
        return u,args,psffile
    else:
        raise ValueError('You need to select either traj or create')

    #now just add what if I have create option how do I not return the Universe?
    #

def del_endpsf(x):
    """
    delete npz dimension of the file
    """
    if x[-4:] == '.psf':
        return ''.join(x.split())[:-4]
    else:
        return x

def is_valid_file(parser, arg):
    """
    Check if arg is a valid file 
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s doesn't exist " % arg)
    else:
        return arg

def create_psf(datafile,traj,trajskip,psffile,fileskip=4):
    """given data file produce psf file, read-eidt dcd file"""
    curdir = os.getcwd()
    curdir = curdir+"/"
    filestring = " ".join(("create_list_cryst.sh",datafile,traj,str(fileskip),psffile,curdir))
    os.system(filestring)
    return 0

def main():
    read_parameters()

if __name__ == '__main__':
    main()
