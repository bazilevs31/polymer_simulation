#!/bin/bash


# here is the main file for creating a polymer melt
# input : DATA_file_input = initial melt created by chain.f that has only fene Bonds
# output : DATA_file_output = final melt that has all angles, dihedrals, that has correct mass and 
# the real units
# length conversion rule: length_old = 0.85  sigma (from def.chain file) , length_new = 1.54 A 
# therefore length_new = length_old*1.54/0.85
# mass was 1 -> 14.0

# structure 

# lj_without_to_real_with.sh  input_data output_data
# get all the initial information from input file
# and splits it into series of *.info files
# then it modifies each of the *.info files

# join_polymers.sh some_tmp_output
# joins together *.info

# clean_and_join.sh some_tmp_output output_data
# gets the some_tmp_output file and adds angles and dihedrals

#Author: Vasiliy Triandafilidi, MS at UBC 

rm -f *.info

DATA_file_input=$1
DATA_file_output=$2
nchain=$3
nlen=$4

let natoms=$nchain*$nlen
let nbond=($nlen-1)*nchain
let nangle=($nlen-2)*$nchain
let ndih=($nlen-3)*$nchain

cp $DATA_file_input poly.new



echo "==========================="
echo " "
echo "lj units to real"
echo " "
echo "==========================="






#from begining to atomtypes(non  inclusive by deleting the last line) to 1.info
# sed -n '1,/atom types/p' poly.new > 1.info
# sed -i '$d' 1.info



# #getting the atomtypes and adding the number o angles and dihedrals
# less poly.new | grep types > tmp2
# awk '{print 1 " " $2 " " $3}' tmp2 > 2.info
# rm tmp2


echo "LAMMPS  data file

         $natoms  atoms
         $nbond  bonds
         $nangle  angles
         $ndih  dihedrals

           1  atom types
           1  bond types
           1  angle types
           1  dihedral types

" > 1.info


# getting the box values and changing units
less poly.new | grep hi > tmp3
# awk '{print $1*1.54/0.85 " " $2*1.54/0.85 " " $3 " " $4}' tmp3 > 3.info
awk '{print $1*1.54/0.85 " " $2*1.54/0.85 " " $3 " " $4}' tmp3 > 2.info
rm tmp3
sed -i  '1i\\' 2.info


# sed -n '/Masses/,/Atoms/ p' poly.new > 4.info

echo "Masses

  1  14.0

Atoms " > 3.info 


#put middle section to new
sed -n '/Atoms/,/Velocities/{//!p}' poly.new > coordinates
#get rid of the empty lines
sed -i '/^\s*$/d' coordinates
#change the content of the lines
awk '{print  $1, "\t", $2, "\t", $3, "\t", $4*1.54/0.85, "\t", $5*1.54/0.85, "\t", $6*1.54/0.85, "\t", $7, "\t", $8, "\t", $9 }' coordinates > 4.info
#add an empty line to the begining 
sed -i  '1i\\' 4.info
rm coordinates

#put everything from bond to the end to 3.info
sed -n '/Bonds/,$p' poly.new > 5.info
sed -i  '1i\\' 5.info



touch polymer_without_real_angles.data
./join_polymers.sh polymer_without_real_angles.data

./clean_and_join.sh polymer_without_real_angles.data  $DATA_file_output