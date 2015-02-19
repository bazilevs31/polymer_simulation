#!/bin/bash
#
#manual : ./create_list_cryst.sh <input data file> <name of dcd file to crop> <skip for dcd>
#output: <vmd file> <psf file> <dcd file>
#
datafile=$1
dcdfile=$2
dcdskip=$3
psffilename=$4
currentdir=$5


outdcd='trajSkipwrap.dcd'

echo "the data file name is $datafile"
echo "the psf file  is $psffilename"
echo "currennt dir is $currentdir"
echo "file is $currentdirvmd_data_to_pdbpsf.tcl "

rm $currentdir$outdcd

echo "
topo readlammpsdata $datafile angle 
animate write psf $psffilename
animate read dcd $dcdfile skip $dcdskip waitfor all
pbc wrap -all
animate write dcd $currentdir$outdcd waitfor all
exit
 " > vmd_data_to_pdbpsf.tcl 

# less vmd_data_to_pdbpsf.tcl

vmd -e  vmd_data_to_pdbpsf.tcl -nt

# rm vmd_data_to_pdbpsf.tcl 

# ipython traj.py poly40




# Problem this script gets invoked by a python program from within other directory
# so when I invoke it creates tcl file here and therefore can't find anything
# what do I do?
# o
