#!/bin/bash

nchains=300
nlen=40


#run the generate chains using chain.f 
#input: input.data | number of chains | length of the polymers 
./generate_chains_using_chain.sh polymer_melt_using_chain.data $nchains $nlen

#equilibrate via a lammps run with lj units and dpd/fene potential 
#input: input.data | intermediate.data|
./equilibrate_kremer.sh polymer_melt_using_chain.data equilibrated.data

#prepare data file for the normal lammps simulation
#i.e lj units -> real units, bond+atoms -> atoms+bonds+angles+dihedrals
#input: intermediate.data | final.data | number of chains | length of the polymers
./lj_without_to_real_with.sh equilibrated.data equilibrated_full.data  $nchains $nlen

#run short lammps simulation with short nvelimit
./short_lammps_sim_nvelimit.sh equilibrated_full.data result.data

cp result.data ~/Dropbox/Lammps_simulation/
#leave only useful information
ls | grep -v -E 'chain.f|*.sh|result.data' | xargs rm
# rm -f polymer_equilibrated.data
# rm -f polymer_melt_using_chain.data
# ./lj_without_to_real_with.sh polymer_melt_using_chain.data 

