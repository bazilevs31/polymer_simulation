#!/bin/bash
#
#manual : ./create_list_cryst.sh <input data file> <name of dcd file to crop> <skip for dcd>
#output: <vmd file> <psf file> <dcd file>
#
datafile=$1
psffilename=$2
currentdir=$3


outdcd='trajSkipwrap.dcd'

echo "the data file name is $datafile"
echo "the psf file  is $psffilename"
echo "currennt dir is $currentdir"
echo "file is $currentdirvmd_data_to_pdbpsf.tcl "

rm $currentdir$outdcd

echo "
topo readlammpsdata $datafile angle 
animate write psf $psffilename.psf
animate write pdb $psffilename.pdb
exit
 " > end2end_pdbpsf.tcl 

# less vmd_data_to_pdbpsf.tcl

vmd -e end2end_pdbpsf.tcl -nt

# rm vmd_data_to_pdbpsf.tcl 

# ipython traj.py poly40




# Problem this script gets invoked by a python program from within other directory
# so when I invoke it creates tcl file here and therefore can't find anything
# what do I do?
# o
