#!/bin/bash
#
#manual : ./create_list_cryst.sh <input data file> <name of dcd file to crop> <skip for dcd>
#output: <vmd file> <psf file> <dcd file>
#
datafile=$1
psffilename=$2
currentdir=$3

echo "the psf file  is $psffilename"
echo "currennt dir is $currentdir"
echo "file is $currentdirvmd_data_to_pdbpsf.tcl "

rm $currentdir$outdcd

echo "
package require topotools
topo readlammpsdata $datafile.data angle
animate write psf $psffilename.psf
exit


 " > vmd_data_to_pdbpsf.tcl 

# less vmd_data_to_pdbpsf.tcl

vmd -dispdev text -e  vmd_data_to_pdbpsf.tcl

# rm vmd_data_to_pdbpsf.tcl 

# ipython traj.py poly40




# Problem this script gets invoked by a python program from within other directory
# so when I invoke it creates tcl file here and therefore can't find anything
# what do I do?
# o
