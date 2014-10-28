#!/bin/bash

echo "==========================="
echo " "
echo "doing short nve clean_and_join"
echo " "
echo "==========================="


file_without_angles_dihedrals=$1
file_with_angles_dihedrals=$2

#creating additional files for generating angle bond topology
echo "1    1  1  1  1    *  *  * " > dihedrals_by_type.txt
echo "1  * * *   * * " > angles_by_type.txt


# sed -i '/improper/d' result_without.data
./gen_all_angles_topo.sh $file_without_angles_dihedrals  $file_with_angles_dihedrals

rm -f $file_without_angles_dihedrals
rm -f *.txt
rm -f *.info
rm -f result_without.data
rm -f poly.new
rm -f polymer_result.data

sed -i '/improper/d' $file_with_angles_dihedrals


