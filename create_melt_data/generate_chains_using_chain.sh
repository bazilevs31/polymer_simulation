#!/bin/bash
output_file=$1
nchains=$2
nlen=$3

echo "==========================="
echo " "
echo "generating chains using chain.f"
echo " "
echo "==========================="





echo "Polymer chain definition

0.85          rhostar
59239884          random # seed (8 digits or less)
1               # of sets of chains (blank line + 6 values for each set)
0               molecule tag rule: 0 = by mol, 1 = from 1 end, 2 = from 2 ends

$nchains           number of chains
$nlen            monomers/chain
2               type of monomers (for output into LAMMPS file)
1               type of bonds (for output into LAMMPS file)
0.85            distance between monomers (in reduced units)
1.05            no distance less than this from site i-1 to i+1 (reduced unit) " > def.chain

gfortran chain.f -o chain
./chain < def.chain > $output_file


rm  -f chain
rm  -f def.chain