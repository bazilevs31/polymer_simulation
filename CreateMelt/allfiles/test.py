#!/home/vasiliy/anaconda/bin/python

from MDAnalysis import *
import os
# from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import argparse
import subprocess

# def read_parameters():
#     """
#     read parameters from the commandline
#     input 
#     output u, trajskip, endframe, psffile, Nsub, sthreshold
#     """
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command',help='commands')

#general trajectory parameters data file, psffile, trajectory, skip, endframe, startframe
traj_parser = subparsers.add_parser('traj', help='trajectory parser content')
traj_parser.add_argument("-d", "--data", dest="datafile", 
                default="./figures/polymer_0.8.data",
                type=lambda x: is_valid_file(parser, x),
                help="read datafile", metavar="FILE")
traj_parser.add_argument("-e", 
                "--endframe",
                dest="endframe", 
                default=-1, 
                type=int, 
                help="End frame of the trajectory file")
traj_parser.description="traj"

create_parser = subparsers.add_parser('create', help='create parser content')
#sparameter params
create_parser.add_argument("-g", 
            "--Nsub",
            dest="Nsub", 
            default=7, 
            type=int, 
            help="number of grid cells in each dimension")
create_parser.description="create"

args=parser.parse_args()

# traj = traj_parser.parse_args()
# create = create_parser.parse_args()
print parser.parse_args()
# print traj_parser.parse_args()
# return traj



np.savez('tmp', *[i*np.arange(10) for i in range(10)])

