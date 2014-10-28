#!/bin/bash




#equilibration of the polymers

input_data_file=$1
output_data_file=$2



echo "==========================="
echo " "
echo "doing Kremer-Grest equilibration"
echo " "
echo "==========================="


# rm in_equil.lammps
echo "
# Kremer-Grest model.

units lj
atom_style bond

special_bonds lj/coul 0 1 1

read_data $input_data_file

neighbor 0.4 bin
neigh_modify every 1 delay 1
comm_modify vel yes


bond_style fene
bond_coeff * 30.0 1.5 1.0 1.0

dump 			mydump all dcd 5000 temporary_traj.dcd
timestep 0.01
thermo 100



pair_style dpd 1.0 1.0 122347
pair_coeff * * 25 4.5 1.0


velocity all create 1.0 17786140 

fix 1 all nve/limit 0.05
run 500
unfix 1
fix 1 all nve
run 50000

write_data tmp_restart_dpd.data

pair_coeff * * 50.0 4.5 1.0
velocity all create 1.0 15086120
run 50
pair_coeff * * 100.0 4.5 1.0
velocity all create 1.0 15786120 
run 50
pair_coeff * * 150.0 4.5 1.0
velocity all create 1.0 15486120
run 50
pair_coeff * * 200.0 4.5 1.0
velocity all create 1.0 17986120
run 100
pair_coeff * * 250.0 4.5 1.0
velocity all create 1.0 15006120
run 100
pair_coeff * * 500.0 4.5 1.0
velocity all create 1.0 15087720
run 100
pair_coeff * * 1000.0 4.5 1.0
velocity all create 1.0 15086189
run 100
write_data tmp_restart_dpd1.data

pair_style hybrid/overlay lj/cut 1.122462 dpd/tstat 1.0 1.0 1.122462 122347
pair_modify shift yes
pair_coeff * * lj/cut 1.0 1.0 1.122462
pair_coeff * * dpd/tstat 4.5 1.122462
velocity all create 1.0 1508612013
run 50
velocity all create 1.0 15086121
run 50
velocity all create 1.0 15086111
run 50
write_data tmp_restart_push.data
velocity all create 1.0 15086125
run 100000

write_data $output_data_file " > in_equil.lammps



mpirun -np 4 lmp_ubuntu -in in_equil.lammps

rm -f log.*
rm -f tmp_restart_*
rm  -f temporary_traj*
rm -f in_equil.lammps

