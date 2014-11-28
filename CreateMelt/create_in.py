#!/home/vasiliy/anaconda/bin

from __future__ import print_function
import argparse
import numpy as np
import os
import sys

# parser = argparse.ArgumentParser(description='Generate lammps input file')
# parser.add_argument("namedatafile", help="Get lammps data file")
# parser.add_argument("drun", help="Running step of which numcool will consist of (if drun=1M, numcool=10, then totaltime=10M")
# parser.add_argument("", help="Get number of Chains")
# parser.add_argument("ChainLength", help="Get Chain length (number of monomers per chain)")
# args = parser.parse_args()
# Nchains = args.Nchains
# ChainLength = args.ChainLength

# Nchains, ChainLength = map(int, (Nchains, ChainLength))


# input format:
# in_create.py <namesdatafile> <drun> nve <no parameters> cool <Temp_cool_1> <Temp_cool_2> <numcool> rest <Temp_rest_1> <numrest>
# first is always nve

sim_steps=[] #list of strings
numsteps_cool=[]
numsteps_rest=[]
Temp_cool=[] # list of pairs (,)
Temp_rest=[] # list of Temps
namedatafile=sys.argv[1]
drun = sys.argv[2]
sim_steps.append(sys.argv[3])
numofargs = len(sys.argv)
i=4
while i<numofargs:
    # i += 1
    sim_steps.append(sys.argv[i])
    if sim_steps[-1]=='cool':
        i += 4
        Temp_cool.append((sys.argv[i-3],sys.argv[i-2]))
        numsteps_cool.append(sys.argv[i-1])
    elif sim_steps[-1]=='rest':
        i += 3
        Temp_rest.append((sys.argv[i-2]))
        numsteps_rest.append(sys.argv[i-1])


    

# drun = 1000
# numcool = 2
# numrest = 2
# totalcool = numcool*drun
# totalrest = numrest*drun
# Temp_high = 0.8
# Temp_low = 0.5
# Temp_cool_1 = 0.8
# Temp_cool_2 = 0.5
# Temp_rest_1 = 0.6


# sim_steps = ['nve','cool','rest']


intro_lines = "\n\
variable        Pstop equal 8.0 \n\
variable        dump_thermo equal 100 \n\
variable        dump_traj equal 10000 \n\
\n\
\n\
units           lj \n\
boundary        p p p \n\
atom_style      angle \n\
pair_style  lj96/cut 1.0188  \n\
pair_modify shift yes \n\
bond_style      harmonic \n\
angle_style   table spline 181 \n"
intro_lines += "read_data " + namedatafile + " \n"
intro_lines += " pair_coeff * * 0.37775 0.89 \n\
bond_coeff * 1352.0 0.5  \n\
angle_coeff * /home/vasiliy/cgpva.table CG_PVA \n\
special_bonds   lj 0.0 0.0 1.0 \n\
neighbor        0.4 bin \n\
neigh_modify    every 1 once no cluster yes \n"



dump_lines= "dump           dump_traj all dcd ${dump_traj} trajectory_${simname}.dcd \n\
dump_modify     dump_traj sort id unwrap yes"


#############################
#   variables
############################

run_cool = "\n run      %d start 0 stop %d \n " # % (drun,totalcool)
run_cool += "write_data     ${simname}.*.data \n "

run_rest = "\n run      %d start 0 stop %d \n " # % (drun,totalrest)
run_rest += "write_data     ${simname}.*.data \n "

datawrite_unfix = "\n\
unfix       1\n\
unfix       2\n\
write_data  ${simname}.final.data \n \n"

nve_sim = " \n\
fix             1 all nve \n\
thermo          100\n\
timestep        0.005\n\
run             100\n\
unfix           1\n \n \n \
"
rest_sim = " \n\
next simname \n \
fix             1 all npt temp %s %s 100 iso ${Pstop} ${Pstop} 1000 drag 1.0 \n\
fix             2 all momentum 10 linear 1 1 1 angular \n\
thermo_style    custom step temp press density vol  pe ke epair ebond eangle edihed etotal \n\
thermo          ${dump_thermo} \n\
timestep        0.005\n\
reset_timestep  0\n " # %(Temp1, Temp2)


cool_sim = "\n\
next simname \n \
fix             1 all npt temp %s %s  100 iso ${Pstop} ${Pstop} 1000 drag 1.0 \n\
fix             2 all momentum 10 linear 1 1 1 angular \n\
thermo_style    custom step temp press density vol  pe ke epair ebond eangle edihed etotal\n\
thermo          ${dump_thermo}\n\
timestep                0.005\n\
reset_timestep  0 \n \n "   # %(Temp1, Temp2)


#############################
#   variables
############################


icool,irest = 0, 0
numcool,numrest = 0, 0

with open('in.lammps', 'w') as f:
    # f.write("Lammps input file for simulating cooling and resting")
    f.write("variable   simname index")
    f.writelines((" %s " % l for l in sim_steps))
    f.write("\n")
    f.write(intro_lines)
    f.write(dump_lines)

    for item_sim in sim_steps:
        if item_sim=='nve':
            print " writing " + item_sim
            f.write(nve_sim)
        elif item_sim=='cool':
            print " writing " + item_sim
            f.write(cool_sim % Temp_cool[icool])
            numcool = int(numsteps_cool[icool])
            # numcool = 1
            for irun in range(numcool):
                f.write(run_cool  % (int(drun),numcool*int(drun)) )
            f.write(datawrite_unfix)
            icool += 1
        elif item_sim=='rest':
            print " writing " + item_sim
            f.write(rest_sim % (Temp_rest[irest],Temp_rest[irest]))
            numrest = int(numsteps_rest[irest])
            for irun in range(numrest):
                f.write(run_rest % (int(drun), numrest*int(drun)) )
            f.write(datawrite_unfix)
            irest += 1
        else:
            print "Unknown type, please check the input"




