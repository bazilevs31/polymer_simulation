#!/bin/bash

# convert standard to correct lammps data file that could be fed to mdanalysis
# it has correct format and therefore mdanalysis can read it
# algorithm grep the number of atoms 


datain="polymer_0.8.data"
dataout="lammps.data"


# grep number of atoms , bonds 
# generate number of angles
STR=$(less $datain | grep atoms)
LIT=$(echo $STR | grep -o [0-9]*)
natoms=$LIT

STRb=$(less $datain | grep bonds)
LITb=$(echo $STRb | grep -o [0-9]*)
nbonds=$LITb

# STRang=$(less $datain | grep angles)
# LITa=$(echo $STRang | grep -o [0-9]*)
# nangles=$LITa

let nangles=(2*$nbonds-$natoms)

DATE=`date +%d-%m-%Y:%H:%M`
echo "Proper lammps file for the Mdanalysis, last modified $DATE" > $dataout
echo " 
$natoms atoms
$nbonds bonds
$nangles angles

1 atom types
1 bond types
1 angle types
" >> $dataout

less polymer_0.8.data | egrep -i "lo.*hi" >> $dataout

echo "
Masses

1 1
" >> $dataout

# From Atoms keyword till the end keep it the same
sed -n '/Atoms/,$p' $datain >> $dataout

#get rid of the comments
sed -i 's:#.*$::g' $dataout
