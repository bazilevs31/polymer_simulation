#!/bin/bash

input_data=$1
output_data=$2


echo "==========================="
echo " "
echo "doing short nve equilibraing"
echo " "
echo "==========================="

echo "
# This is the Lammps input sctipt for simulating a polyethylene

variable 		simname index min equil_nve nve 

variable 		Temp equal 800.0
variable 		T1 equal 500.0
variable 		Pstop equal 1.0
variable 		dump_traj equal 1000
variable 		dump_thermo equal 50

units			real
boundary 		p p p 
atom_style		molecular


pair_style 		lj/cut  10.25
bond_style 		harmonic
angle_style 	harmonic
dihedral_style 	class2

read_data 		$input_data

pair_coeff 		* * 0.112 4.01

bond_coeff 		* 350. 1.53
angle_coeff 	* 60. 109.
dihedral_coeff  * 0.81 0. -0.43 180. 1.62 0.
dihedral_coeff  * mbt  0.0 0.0 0.0   0.0
dihedral_coeff  * ebt  0.0 0.0 0.0   0.0 0.0 0.0   0.0  0.0
dihedral_coeff  * at   0.0 0.0 0.0   0.0 0.0 0.0   0.0  0.0
dihedral_coeff  * aat  0.0  0  0
dihedral_coeff  * bb13 0.0  0.0  0.0


#dihedral paper \Sigma K_n*(1-cos(n\phi - \phi_0))
#dihedral lammps opls \Sigma K_n*(1+cos(n\phi - \phi_0)) with the plus 
special_bonds 	dreiding 

neighbor		0.4 bin
neigh_modify	every 1 once no cluster yes 
timestep  		2.0
# run_style respa 4 2 2 2 inner 2 4.5 6.0 middle 3 8.0 9.825 outer 4 

compute			1 all gyration

# fix 1 all nve 
# thermo 50
# run 1000

print \"done with the input\"
print \"doing \${simname}\"

write_restart 	restart.\${simname}
write_data 		data.\${simname}

print \"=============================\"
print \"                             \"
print \"done with the \${simname}\"
next 			simname
print \"doing \${simname}\"
print \"                             \"
print \"=============================\"


velocity 		all create \${Temp} 1231

fix 			CENTER_of_mass all recenter INIT INIT INIT


dump 			all_dump all dcd \${dump_traj} trajectory_all.dcd

log 			log.nvt.\${simname}
fix				1 all nve/limit 0.05
fix				2 all langevin \${Temp} \${Temp} 10.0 904297
thermo_style	custom step temp press vol epair ebond eangle edihed etotal
thermo          10
timestep		0.5
run				50
# run 			1000
unfix 			1
unfix 			2
write_restart 	tmp.\${simname}.*
write_data 		tmp.\${simname}.*

fix				1 all nve/limit 0.1
fix				2 all langevin \${Temp} \${Temp} 10.0 904297
thermo_style	custom step temp press vol epair ebond eangle edihed etotal
thermo          10
timestep		0.5
run				50
# run 			1000
unfix 			1
unfix 			2
write_restart 	tmp.\${simname}.*
write_data 		tmp.\${simname}.*

print \"=============================\"
print \"                             \"
print \"done with the \${simname}\"
next 			simname
print \"doing \${simname}\"
print \"                             \"
print \"=============================\"


fix				1 all nve
fix				2 all langevin \${Temp} \${Temp} 10.0 904297
thermo_style	custom step temp press vol epair ebond eangle edihed etotal
thermo          100
timestep		0.5
run				50000
# run 			1000
unfix 			1
unfix 			2
write_data 		$output_data

" > in_short_nvelimit.lammps


mpirun -np 4 lmp_ubuntu -in in_short_nvelimit.lammps


rm -f tmp.*
rm -f trajectory_all*
rm -f in_short_nvelimit.lammps